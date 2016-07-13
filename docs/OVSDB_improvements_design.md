# OVSDB Improvements

The Open vSwitch Data Base (OVSDB) was designed and implemented taking into
consideration the requirements of the Open vSwitch community. Now that the
OpenSwitch uses OVSDB as one of its core functionality, new use cases appear.
To address them some improvements to OVSDB are been implemented.

This document describes the design of those improvements to OVSDB. These
improvements are currently available only for the C IDL.

## Improvements
1. [Partial update of map columns](#Partial-update-of-map-columns)
2. [On-demand fetching of non-monitored data](#On-demand-fetching-of-non-monitored-data)
3. [Compound indexes](#Compound-Indexes)
4. [jemalloc Memory Allocator](#jemalloc-Memory-Allocator)
5. [Priority Sessions](#Priority-Sessions)
6. [Wait Monitoring and Blocking Waits](#Wait-Monitoring-and-Blocking-Waits)

## Partial update of map columns

### Problem statement

In the current OVSDB IDL implementation, every time an element of either a map
or set column has to be modified, the entire content of the column is
sent to the server to be updated. This is not a major problem if the
information contained in the column for the corresponding row is
small, but there are cases where these columns can have a significant
amount of elements per row, or these values are updated frequently,
therefore the cost of the modifications becomes high in terms of time and
bandwidth.

### Solution

#### Overview

The OVSDB IDL code was modified to support the RFC 7047 'mutate'
operation, to allow sending partial modifications on map columns to
the server.

The functionality is exposed to clients in the OVSDB IDL. This was
implemented through map operations.

A map operation is defined as an insertion, update, or deletion of a
key-value pair inside a map. This solution aims to minimize the amount of map
operations that are send to the OVSDB server when a transaction is committed.
To do so, for each transaction a list of map operations is created for every
column on the row on which a map operation is performed. When a new map
operation is requested on the same column, the corresponding list is checked to
verify if a previous operations was performed on the same key inside the same
transaction. If there is no previous operation, then the new operation is just
added into the list. But if there was a previous operation on the same key, then
the previous operation is collapsed with the new operation into a single one
that preserves the final result as if both operations were performed
sequentially. This design also keeps a small memory footprint during
transactions.

As an example, if a client using the IDL updates several times the
value for the same key, the functions will ensure that only the last
value is send to the server, instead of multiple updates. Or, if the
client inserts a key-value, and later on deletes the key before
inside the same transaction, then both actions cancel out and no map operation
is send for that key.

When a transaction is committed, the map operations lists are checked and all
map operations that belong to the same map are grouped together into a single
JSON RPC "mutate" operation. Each map operation is translated in terms of
"insert" or "delete" mutators. Then the "mutate" operation is added to
the operations that will be send to the server.

Once the transaction is finished, all map operation lists are cleared and
deleted, so the next transaction starts with a clean board for map operations.

Using different structures and logic to handle map operations, instead
of trying to force the current structures (like 'old' and 'new' datums
in the row) to handle then, ensures that map operations won't mess up
with the current logic to generate JSON messages for other operations.

#### Implementation

New functions were created in `vswitch-idl.c` that can be used to modify
individual elements inside map columns. The code generator automatically detects
when the table contains a map column and generates the corresponding functions
to insert, update, and delete the elements given a key/value information.

## On-demand fetching of non-monitored data

### Problem statement

The current OVSDB IDL only supports reading from columns that are part of the
local database replica, i.e. that are being monitored. When an IDL is being
initialized, it is necessary to register which table and columns will be added
and automatically synchronized in the local database replica. In order to do so,
the IDL sends a monitor request to the OVSDB server using the columns registered
by the user. Then, the OVSDB server will send notifications with the database
changes that affect the monitored columns.

The messages exchanged between the server and each IDL, generate traffic and
require memory and processing time in both the server and the client side. This
could represent a waste of resources for daemons or processes that do not access
the database frequently or in cases where the data is updated more frequently
than it is required by a process.

### Solution

#### Overview

A new column mode called `OVSDB_IDL_ON_DEMAND` was added. The IDL users still
need to register the table columns to be replicated, but now there is also an
option to set it on-demand. The on-demand columns are not updated by the IDL
automatically, they are updated on-demand when the process explicitly asks the
IDL to fetch the information. When this happens, the IDL sends a select
operation to request the data from the server. After calling `ovsdb_idl_run`,
the IDL updates the replica with the information received from the server.

An on-demand column will have its default value if it has never been updated.
This can happen if: 1) the user has not called explicitly a fetch operation over
it, or 2) the server response with the actual value has not been
received/processed. After the first update, any on-demand column will keep the
last value fetched from the OVSDB server.

With this new column mode, the state of the replica could diverge from the
database (as some of the columns could be outdated). It is responsibility of the
process using the IDL to update the on-demand columns before using then.

To reduce the traffic needed to retrieve the data from the server. The IDL was
provided with functions that allows retrieving the value of a on-demand column
at three different levels: row, column, and table.

Requesting a column value at a row level, fetches the value of the given value
for an specific row. The IDL sends a select operation to the server. In all
levels, the the uuid of the rows are requested because it is needed in order to
update the local replica.

The on-demand column fetch request for a row are traduced to:

```
{
"op": "select",
"table": "<table-name>",
"where": "[uuid == <row_uuid>]"
"columns": "<column-name>, uuid"
}
```
Once the request is sent, the row is marked with a pending fetch request. It
will be pending until the replica is updated with the server reply.

The on-demand column fetch request are traduced to:
```
{
"op": "select",
"table": "<table-name>",
"where": "[]"
"columns": "<column-name>, uuid"
}
```

After the request is sent, the column is marked with a pending fetch request.
Even if there are a pending rows with a request over this column, the column
will be considered as pending only during the time between the column request
and the moment when the replica is updated with the server reply.

For the on-demand table fetch request, the IDL generates a request similar to
the one used for fetching a single row, but all the on-demand columns of the
table are requested.

```
{
"op": "select",
"table": "<table-name>",
"where": "[]"
"columns": "<on-demand-column-1>,...,<on-demand-column-n>, uuid"
}
```

Once the request is sent, the column is marked with a pending fetch request. It
will be pending until the replica is updated with the server reply. Once again,
the function that indicates if the table has a pending fetch operation consider
only request done at a table level. Request at row and column level are not
taken into consideration.

After the user does a fetch request, it will need to call ```ovsdb_idl_run```
to get the reply from the server. The IDL sequence number is updated when an
on-demand column is updated. Note that getting the value of on-demand column is
slower that reading the values directly from the cache, as they are fetched
from the server in the moment their are needed. This is the trade off for not
keeping everything monitored, and is something that needs to be taken into
consideration to take the decision of using this feature.

When the IDL processes the server reply, the value of the on-demand column, will
be accessible in the replica as any ordinary column. The IDL now provide new
functions that takes as an argument a row, column, or a table, and returns if
there is an ongoing fetch request on it. These functions allows the user to
verify if a fetch operation done over a given level (row, column or table) has
been processed.

Each level is independent. For example, the function
`ovsdb_idl_is_table_fetch_pending` will return true only if there is an ongoing
fetch operation at the table level. It will return false even if there are
pending fetch requests over rows or columns of the same table.


## Compound Indexes

### Fast lookups

Depending on the topology, the route table of a network device could manage
thousands of routes. Commands such as "show ip route <*specific route*>" would
need to do a sequential lookup of the routing table to find the specific route.
With an index created, the lookup time could be faster.

This same scenario could be applied to other features such as Access List rules
and even interfaces lists.

### Lexicographic order

There are several cases where retrieving data in lexicographic order is needed.
For example, SNMP. When an administrator or even a NMS would like to retrieve
data from a specific device, it's possible that they will request data from full
tables instead of just specific values. Also, they would like to have this
information displayed in lexicographic order. This operation could be done by
the SNMP daemon or by the CLI, but it would be better if the database could
provide the data ready for consumption. Also, duplicate efforts by different
processes will be avoided. Another use case for requesting data in lexicographic
order is for user interfaces (web or CLI) where it would be better and quicker
if the DB sends the data sorted instead of letting each process to sort the data
by itself.

## Implementation

The proposal is to create a data structure in memory that contains pointers to
the rows where the desired information is stored. This data structure can be
traversed in the order specified when creating the index.

An index can be defined over any number of columns, and support the following
options:

-   Add a column with type string, int or real (using default comparators).
-   Select ordering direction of a column (must be selected when creating the
    index).
-   Use a custom iterator (eg: treat a string column like a IP, or sort by the
    value of "config" key in a map).

For querying the index the user must create a cursor. That cursor points to a
position in the sorted data structure. With that, the user can perform lookups
(by key) and/or get the following rows. The user can also compare the current
value of the cursor to a record.

For faster lookups, user would need to provide a key which will be used for
finding the specific rows that meet this criteria. This key could be an IP
address, a MAC address, an ACL rule, etc. When the information is found in
the data structure the user's cursor is updated to point to the row. If
several rows match the query then the user can get easily the next row
updating the cursor.

For accessing data in lexicographic order, the user can use the ranged
iterators. Those iterators needs a cursor, and a "from" and "to" value.

One of the potential issues of this solution is the memory consumption of the
new data structures. However, since it will only contain pointers, it's not
expected that it consumes too much memory.

Another potential issue is the time needed to create the data structure and the
time needed to add/remove elements. The indexes are always synchronized with the
replica. For this reason it must be important that the comparison functions
(built-in and user provided) are FAST. However, these operations are not as
common as looking up for data, so it's not expected these operations affects the
system significatively.

At this point, a skiplist is the data structure selected as the best fit.
A skiplist is a datastructure that offers log( n )
retrieval/insertions/deletions, and O(1) "find next" operations.

To implement the indexes in the C IDL the following changes in the IDL were
made:

-   For each column, new function `int comparator(void*, void*)` that allows to
    compare two ovsrec structs (by that column) were added. These function are
    created only for the columns with type string, int, or real. Each column has
    a pointer to this function (or NULL).
-   Each table, now has a hash table with the indexes (keyed by index name).



It's important to mention that all changes will be done in the IDL. There are no
changes to the OVSDB server or the OVSDB protocol.

                     +---------------------------------------------------------+
                     |                                                         |
        +------------+---Client changes to data                            IDL |
        |            |                                                         |
    +---v---+        |                                                         |
    | OVSDB +----------->OVSDB Notification                                    |
    +-------+        |   +                                                     |
                     |   |   +------------+                                    |
                     |   |   |            |                                    |
                     |   |   | Insert Row +----> Insert row to indexes         |
                     |   |   |            |                   ^                |
                     |   +-> | Modify Row +-------------------+                |
                     |       |            |                   v                |
                     |       | Delete Row +----> Delete row from indexes       |
                     |       |            |                                    |
                     |       +----+-------+                                    |
                     |            |                                            |
                     |            +-> IDL Replica                              |
                     |                                                         |
                     +---------------------------------------------------------+


## jemalloc Memory Allocator

### Background

OVSDB-Server performs a lot of memory-related operations. Many of those are
related to allocating small pieces of memory. It requests and releases memory
continually for creating and destroying objects like dynamic strings, json
objects, etc.

Tests revealed that by replacing the GLibC memory allocator with the [jemalloc]
(http://www.canonware.com/jemalloc) memory allocator, OVSDB-Server's
performance can be significantly improved, and also, in some cases, can reduce
the memory usage.

### Implementation

ops-openvswitch is configured with jemalloc in the LIBS variable. Therefore,
ovsdb-server and other components (including the IDL) from this repo are
using jemalloc.

### Notes for developers

If a daemon isn't linking with jemalloc then changing to jemalloc is very easy.
There are two options:
1. Rebuild the daemon using the library (and changing the building instructions)
2. Change how the daemon is loaded (systemd scripts).

### Rebuild the daemon with jemalloc support

In this case, libjemalloc must be compiled as a library. Change the automake,
CMakeLists.txt or configure scripts in order to use the flag -ljemalloc. Your
Yocto recipe must include jemalloc as a RDEPENDS and DEPENDS dependency.

### systemd script

In this case, add the following line (under [Service]) to your script:

    Environment="LD_PRELOAD=/lib/libjemalloc.so.2"

The daemon's Yocto recipe also needs to specify jemalloc as a RDEPENDS
dependency.

## Performance Improvements

Several tests (insertion, updates, pubsub and transaction size) were run in
order to compare the GLibC performance and memory usage along both jemalloc
and tcmalloc memory allocators.

The results showed favorable results for jemalloc library.

- Update 1: Each of 10 parallel workers do 25000 updates over 1000 rows.
- Update 2: Each of 10 parallel workers do 25000 updates over 200000 rows.
- Insert: Each of 10 parallel workers insert 25000 rows.
- Message Queue Simulation: One producer waits for requests (requested by 10
  parallel workers).
  For each request the producer updates 512 rows, composed of one map column
  with 256 elements.
- Transaction Size: The program inserts 100, 1000, 10000, 100000 and 500000
  rows, alternating between inserting all the rows in the same transaction, or
  inserting one row per transaction.

| Test     |   GLibC   |  jemalloc  |  tcmalloc  |
|----------|-----------|------------|------------|
| Update 1 |   28s     |    24s     |    31s     |
| Update 2 |   57s     |    38s     |    33s     |
| Insert   |   38s     |    32s     |    27s     |
| Queue    |    4s     |     4s     |     4s     |
| Size     |  129.92s  |   119.87s  |   114.21s  |
|            Duration (seconds)                  |


| Test     |   GLibC   |  jemalloc  |  tcmalloc  |
|----------|-----------|------------|------------|
| Update 1 |    7.35   |    18.92   |   171.42   |
| Update 2 | 1090.7    |    82.88   |   111.08   |
| Insert   |   66.66   |    57.86   |   127.56   |
| Queue    | 1094.40   |    28.13   |   270.47   |
| Size     |  410.17   |   116.50   |   114.21   |
|        Memory Usage (RSS, megabytes)           |

The results show a consistent better results of jemalloc over GLibC memory
allocator.
TCMalloc was faster in some benchmarks, but uses a lot more of RAM than
jemalloc.

## Priority Sessions

### Background
Different clients have different response time requirements from the OVSDB. A
program used by a user could wait a little more than a daemon critical for the
correct operation of the switch.

With *priority sessions* it is possible to identify the clients within the OVSDB
Server, and the server assigns a higher priority to the process that need it the
most.

This feature is composed of:

* A new JSON RPC method (`identify`), that the client uses to identify
  the session in the server.
* A file given to the OVSDB Server, that has the priority that must be
  assigned to each identifier.
* An ovs-appctl command to reload that list.
* The required changes in the OVSDB Server to implement the feature.
* The ability to call the `identify` command from the ovsdb-client
  (mostly for testing purposes).

### Changes to JSON RPC

The method `identify` was introduced. It has a single parameter the
name or identifier of the session. The response is a integer between 0 and 15
(including both) with the priority assigned by the server.

```
/* Request: */
{
    "method": "identify",
    "params": [{"name": "<name or identifier of the session"}],
    "id": ...
}

/* Response: */
{
    "error": null,
    "result": {"priority": <integer between [0, 15]>,
                "uuid": "server's uuid'"},
    "id": ...
}
```

In case that the server doesn't support this method then it will respond with
an error.

### Priorization Algorithm

The priority sessions feature has 16 different priorities, being 8 the default
priority, 0 the highest priority and 15 the lowest priority.

The OVSDB Server process the requests inside a loop that iterates over all the
connections. With this feature the OVSDB Server responds only to the sessions
with the corresponding priority.

The sessions with priority 0 are executed always, the sessions with priority 1
are executed in 15 of each 16 iterations, the sessions with priority 2 are
executed in 14 of each 16 iterations and so on. Therefore, the sessions are
executed in at least the following percentage of iterations:

| Priority | Percent of Iterations (at least) |
|:--------:|:----------------------:|
| 0  | 100.00% |
| 1  | 93.75%  |
| 2  | 87.50%  |
| 3  | 81.25%  |
| 4  | 75.00%  |
| 5  | 68.75%  |
| 6  | 62.50%  |
| 7  | 56.25%  |
| 8  | 50.00%  |
| 9  | 43.75%  |
| 10 | 37.50%  |
| 11 | 31.25%  |
| 12 | 25.00%  |
| 13 | 18.75%  |
| 14 | 12.50%  |
| 15 | 6.25%   |

To avoid iterations in which the OVSDB Server "does nothing" it process the
transactions from sessions with a lower priority, in case it doesn't have any
other session with the "current priority" (or a higher priority).

### Priorities file

Instead of allowing the client to request a priority, this system works with a
priority file. This is a json file that has a JSON map with the identifiers and
the assigned priority, like this:

```
{
    "0": ["criticald", "cruciald", "urgentd"],
    "7": ["exampled],
    "15": ["notimportantd", "notcriticald"]
}
```

In case that an identifier wasn't specified in this file then the OVSDB Server
assigns it the default priority (8). The file can be reloaded at runtime, using
an ovs-appctl command.

## Wait Monitoring and Blocking Waits

The Wait Monitoring Functionality introduces several new methods and operations
over the RFC 7047 that allow to:

* Receive a notification when other client performs a blocking wait over OVSDB
  rows or columns for some table.
* The client can wait until the monitoring process unblock the blocking wait
  before attempting other operations, like read or write from OVSDB.

Those new operations allow the clients to implement synchronization mechanisms
over OVSDB, for example, a client can delay a read until other client finishes
writing the requested data.

### Changes over RFC 7047
#### Wait Monitor
The `wait_monitor` request allows the client to be notified whenever there is
a delayed transaction waiting on certain columns.

The request object has the following members:

* `"method": "wait_monitor"`
* `"params": [<db-name>, <nonnull-json-value>, <wait-monitor-requests>*]`
* `"id": <nonnull-json-value>`

The `<nonnull-json-value>` parameter in “params” is used to match subsequent
`wait_update`s notifications (see below) to this request. The
`<wait-monitor-requests>` object describe the columns to be tracked.

`<wait-monitor-requests>`
An JSON object with the following fields:
* `"table": Name of the table (string)`
* `"columns": [<column>*]`

The response object has the following members:

- `"result": Number of columns “wait monitored” in this request.`
- `"error": null`
- `"id": same “id” as request`

Subsequently, when waits to the specified columns are issued, changes are
automatically sent to the client using the
[Wait Update Notification](Wait Update Notification). This monitoring persists
until the JSON-RPC session terminates or until the client sends a
`wait_monitor_cancel` JSON-RPC request.

This operation is idempotent, and doesn’t fail if the columns were already
`wait monitored`.

#### Wait Monitor Cancellation

The `wait_monitor_cancel` request cancels a previously issued `wait_monitor`
request. The request object members are:

* `method`: `wait_monitor`
* `params`: `[<db-name>, <wait-monitor-cancel-requests>*]`
* `id`: `<nonnull-json-value>`

The `<wait-monitor-cancel-requests>` follow the same format of
`<wait-monitor-requests>`. No more `wait_update` messages will be sent for
those "wait monitored" columns.

The response object has the following members:

* `"result": <Number of columns “wait unmonitored” in this request>`
* `"error”: null`
* `"id": <same “id” as request>`

#### Wait Update Notification

The `wait_update` notification allows a client to notify a session that is wait
monitoring any of the requested columns whenever any transaction become blocked,
 “waiting” on the tables/columns that the client previously sent `wait_monitor`
 for or unblocked for such a `blocking_wait` for any reason.

The notification has the following members:

* `"method": "wait_update"`
* `"params": [<json-object>]`


The `<json-object>` in params is a JSON object with the information required by
the client to process the request. The members of the JSON object in `params`
are:

- `"update_id": <integer>`
- `"state": "start" | "done": current wait update state`
- `"table": <string>: name of table`
- `"rows": [<row uuid>*]`
- `"columns": [<column-name>*]`

The `update_id` member is an integer used to uniquely identify each of the
`wait_update` messages the ovsdb-server is processing.

The `state` member may be set to `start` or `done` according to the processing
stage of the request: the first `wait_update` message with `state` set to
`start` is used to communicate to a wait monitoring session about the cells that
 need to be updated to the database. This `wait_update` transaction should be
 unblocked using a `wait_unblock` message sent by the wait
monitoring session, and then a second `wait_update` with `state` set to `done`
should be sent to the monitoring session to conclude blocking wait request.

The `table` member specifies the name of the table in the request as a string.

The request includes a vector `rows` with each of the row’s UUID converted to
string in JSON format and a JSON array `columns` with each of the column names
as an element.

In case the transaction includes a column which is not being updated by any
wait monitoring session, the `wait_update` messages for the transaction should
not be sent and an error condition should be returned instead.

#### Blocking wait

The "blocking_wait" object contains the following members:

* `"op": "blocking_wait"        required`
* `"timeout": <integer>         optional`
* `"table": <table>             required`
* `"columns":[<column>*]        required`
* `"rows": [<row>*]             required`

There is no corresponding result object.

The operation waits until all the wait-monitors that received wait-update
notification send appropriate wait-unblock messages, get cancelled or the
connection to them is dropped.

If "timeout" is specified, then the transaction aborts after the specified
number of milliseconds. The transaction is guaranteed to be attempted at
least once before it aborts. A "timeout" of 0 will abort the transaction
immediatly.

The errors that may be returned are one of:

* `"error": "timed out"`
  * The "timeout" was reached before the transaction was able to complete.
* `"error": "wait unsatisfiable"`
  * At least one of the wait-monitors that received a wait-update notification
  regarding this request dropped the connection, therefore this operation can’t
  be ever unblocked.
