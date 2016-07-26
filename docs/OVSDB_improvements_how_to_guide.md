# OVSDB Improvements

The Open vSwitch Data Base (OVSDB) was designed and implemented taking into
consideration the requirements of the Open vSwitch community. Now that the
OpenSwitch uses OVSDB as one of its core functionality, new use cases appear.
To address them some improvements to OVSDB are been implemented.

This document describes how to use those improvements to OVSDB. These
improvements are currently available only for the C IDL.

## Improvements
1. [Partial update of map columns](#partial-map-updates)
2. [On-demand fetching of non-monitored data](#on-demand-fetching-of-non-monitored-data)
3. [Compound indexes](#compound-Indexes)
4. [Priority Sessions](#priority-sessions)
5. [Wait Monitoring and Blocking Waits](#wait-monitoring-and-blocking-waits)

## Partial update of map columns

### How to use this feature

The functions that handle this feature are named using the following format:
```
ovsrec_<table_name>_update_<column_name>_setkey()
```
and
```
ovsrec_<table_name>_update_<column_name>_delkey()
```

These functions take as parameters the row, the key to act on and the value (in
set functions only). The `_setkey()` functions can be used to insert a new
value (if the key doesn't exists in the map) or to update a value (if the key
already exists in the map). As an example, these are the generated functions to
modify the `external_ids` map column in the `controller` table:
```
void ovsrec_controller_update_external_ids_setkey(
const struct ovsrec_controller *row_to_modify,
char *new_key, char *new_value);

void ovsrec_controller_update_external_ids_delkey(
const struct ovsrec_controller *row_to_modify,
char *key_to_delete);
```

As usual, tables and columns must be registered in order to get rights to
read/write the columns as shown below:
```
ovsdb_idl_add_table(idl, &ovsrec_table_bridge);
ovsdb_idl_add_column(idl, &ovsrec_bridge_col_other_config);
ovsdb_idl_add_column(idl, &ovsrec_bridge_col_external_ids);
```

And the functions must be called in the middle of a transaction like this:
```
myRow = ovsrec_bridge_first(idl);
myTxn = ovsdb_idl_txn_create(idl);

other = ovsrec_bridge_get_other_config(myRow, OVSDB_TYPE_STRING, OVSDB_TYPE_STRING);
ovsrec_bridge_update_other_config_setkey(myRow, other->keys[0].string, "myList1");
ovsrec_bridge_update_external_ids_setkey(myRow, "ids2", "myids2");

ovsdb_idl_txn_commit_block(myTxn);
ovsdb_idl_txn_destroy(myTxn);
```

Similarly, for deleting an element of a map column, the corresponding function
call is:
```
myRow = ovsrec_bridge_first(idl);
myTxn = ovsdb_idl_txn_create(idl);

other = ovsrec_bridge_get_other_config(myRow, OVSDB_TYPE_STRING, OVSDB_TYPE_STRING);
ovsrec_bridge_update_other_config_delkey(myRow, other->keys[0].string);
ovsrec_bridge_update_external_ids_delkey(myRow, "ids2");

ovsdb_idl_txn_commit_block(myTxn);
ovsdb_idl_txn_destroy(myTxn);
```

## On-demand fetching of non-monitored data

### Changes to the C IDL

The following functions were added to the C IDL:

`ovsdb_idl_add_on_demand_column` Registers an on-demand column in the IDL.
The column will not be updated automatically. An on-demand column by definition
cannot be alerted nor monitored.

`ovsdb_idl_fetch_row` Fetches the value of an on-demand column of a given row.
Sets the pending_fetch field to true for the specified column in the row.

`ovsdb_idl_fetch_column` Fetches all the values of given on-demand column.
Sets the pending_fetch field of the column to true. This allows to read a
whole on-demand column without having to traverse through all is rows.

`ovsdb_idl_fetch_table` Fetches the values of all the on-demand columns of a
given table. Sets the pending_fetch field of the table to true.

`ovsdb_idl_is_row_fetch_pending` Indicates if a row has a fetch request pending.

This will be true during time between a call to `ovsdb_idl_fetch_row` and the
moment when the IDL receives the server reply and updates the replica.

`ovsdb_idl_is_column_fetch_pending` Indicates if a column has been updated since
last call to ovsdb_idl_fetch_column.

This will be true during time between a called to `ovsdb_idl_fetch_column` and
the moment when the IDL receives the server response and updates the replica.

`ovsdb_idl_is_table_fetch_pending`Indicates if a table has been updated since
last call to `ovsdb_idl_fetch_table`.

This will be true during time between a called to `ovsdb_idl_fetch_table` and
the moment when the IDL receives the server response and updates the replica.

### C API

To ease the usage of the on-demand feature, functions specific for each table
and column are generated as part of the IDL during compile time.

The examples below are for a table named "interface" and the column "name".
#### Row
```
void
ovsrec_interface_fetch_name(struct ovsdb_idl *, const struct ovsrec_interface *);


bool
ovsrec_interface_is_row_fetch_pending(const struct ovsrec_interface *);
```

#### Column
```
void
ovsrec_interface_fetch_col_name(struct ovsdb_idl *);


bool
ovsrec_interface_is_fetch_name_pending(const struct ovsdb_idl *);
```

#### Table
```
void
ovsrec_interface_fetch_table(struct ovsdb_idl *);

bool
ovsrec_interface_is_table_fetch_pending(const struct ovsdb_table *);

```

### How to use this feature

In order to retrieved an on-demand column these steps need to be followed:
1. Register the column as on-demand:
** Call ovsdb_idl_add_on_demand_column()`
2. Once the value is needed request it by calling the correspondent function.
* The function will dependent of the level of the request (row, column, or
table) and the name of the table and column.
For example, for requesting the column name from table interface at a row level
the function `ovsrec_interface_fetch_name()` needs be used.
3. Call `ovsdb_idl_run()` and check for changes in the sequence number. If the
sequence number changed, check if the request was already processed. To do this,
use the `*_is_pending()` functions needs to be used. For example current
example the correct function is: `ovsrec_interface_is_row_fetch_pending()`.

## Compound Indexes

### C IDL API

#### Indexes

The indexes are inserted in a hash table in each table in the IDL. This allow to
specify any number of indexes per table, with a custom collection of columns.

```
/* Definition of the index's struct. It's a opaque type. */
struct ovsdb_idl_index {
    struct skiplist *skiplist;
    const struct ovsdb_idl_column **columns;
    column_comparator *comparers;
    int *sorting_order;
    size_t n_columns;
    bool row_sync;
};
```

#### Cursors

The queries are done using cursor. A cursor is a struct that contains the
current ovsrec, current node (on the skiplist) and memory allocated to save
temporal records (needed by the comparator).

```
/* Definition of the cursor structure. */
struct ovsdb_idl_index_cursor {
    struct ovsdb_idl_index *index;
    struct skiplist_node *position;
};
```

### API

#### Index Creation

```
struct ovsdb_idl_index *ovsdb_idl_create_index(
    struct ovsdb_idl *idl,
    const struct ovsdb_idl_table_class *tc,
    const char *index_name);
```

Creates an index in a table. The columns must be configured afterwards. The
returned pointer doesn't need to be saved anywhere, except until all the index's
columns had been inserted.

```
void ovsdb_idl_index_add_column(struct ovsdb_idl_index *,
                                const struct ovsdb_idl_column *,
                                int order,
                                column_comparator custom_comparer
                               );
```

Allows to add a column to an existing index. If the column has a default
comparator then the custom comparator can be NULL, otherwise a custom comparator
must be passed.

#### Index Creation Example

```
/* Custom comparator for the column stringField at table Test */
int stringField_comparator(void *a, void *b) {
    struct ovsrec_test *AAA, *BBB;
    AAA = (struct ovsrec_test *)a;
    BBB = (struct ovsrec_test *)b;
    return strcmp(AAA->stringField, BBB->stringField);
}

void init_idl(struct ovsdb_idl **, char *remote) {
    /* Add the columns to the IDL */
    *idl = ovsdb_idl_create(remote, &ovsrec_idl_class, false, true);
    ovsdb_idl_add_table(*idl, &ovsrec_table_test);
    ovsdb_idl_add_column(*idl, &ovsrec_test_col_stringField);
    ovsdb_idl_add_column(*idl, &ovsrec_test_col_numericField);
    ovsdb_idl_add_column(*idl, &ovsrec_test_col_enumField);
    ovsdb_idl_add_column(*idl, &ovsrec_test_col_boolField);

    /* Create a index
     * This index is created using (stringField, numericField) as key. Also shows the usage
     * of some arguments of add column, althought for a string column is unnecesary to pass
     * a custom comparator.
     */
    struct ovsdb_idl_index *index;
    index = ovsdb_idl_create_index(*idl, &ovsrec_table_test, "by_stringField");
    ovsdb_idl_index_add_column(index, &ovsrec_test_col_stringField, OVSDB_INDEX_ASC, stringField_comparator);
    ovsdb_idl_index_add_column(index, &ovsrec_test_col_numericField, OVSDB_INDEX_DESC, NULL);
    /* Done. */
}
```

#### Indexes Querying

##### Iterators

The recommended way to do queries is using a "ranged foreach", an "equal
foreach" or a "full foreach" over an index. The mechanism works as follow:

1) Create a cursor 2) Pass the cursor, a row (ovsrec_...) and the values to the
iterator 3) Use the values

To create the cursor use the following code:

```
ovsdb_idl_index_cursor my_cursor;
ovsdb_idl_initialize_cursor(idl, &ovsrec_table_test, "by_stringField", &my_cursor);
```

Then that cursor can be used to do additional queries. The library implements
three different iterators: a range iterator, an equal iterator and iterator
over all the index. The range iterator receives two values and iterates over
all the records that are within that range (including both). The equal iterator
only iterates over the records that exactly match the value passed. The full
iterator iterates over all the rows in the index, in order.

Note that the index are *sorted by the "concatenation" of the values in each
indexed column*, so the ranged iterators returns all the values between
"from.col1 from.col2 ... from.coln" and "to.col1 to.col2 ... to.coln", *NOT
the rows with a value in column 1 between from.col1 and to.col1, and so on*.

The iterators are macros especific to each table. To use those iterators
consider the following code:

```
/* Equal Iterator
 * Iterates over all the records equal to value (by the indexed value)
 */
ovsrec_test *record;
ovsrec_test value;
value.stringField = "hello world";
OVSREC_TEST_FOR_EACH_EQUAL(record, &my_cursor, &value) {
    /* Can return zero, one or more records */
    assert(strcmp(record->stringField, "hello world") == 0);
    printf("Found one record with %s", record->stringField);
}

/*
 * Ranged iterator
 * Iterates over all the records between two values (including both)
 */
ovsrec_test value_from, value_to;
value_from.stringField = "aaa";
value_from.stringField = "mmm";
OVSREC_TEST_FOR_EACH_RANGE(record, &my_cursor, &value_from, &value_to) {
    /* Can return zero, one or more records */
    assert(strcmp("aaa", record->stringField) <= 0);
    assert(strcmp(record->stringField, "mmm") <= 0);
    printf("Found one record with %s", record->stringField);
}

/*
 * Iterator over all the index
 * Iterates over all the records in the index
 */
OVSREC_TEST_FOR_EACH_BYINDEX(record, &my_cursor) {
    /* Can return zero, one or more records */
    printf("Found one record with %s", record->stringField);
}
```
##### General Index Access

Although the iterators allow many use cases eventually they may not fit some. In
that case the indexes can be queried by a more general API. In fact, the
iterators were built over that functions.

```
int ovsrec_<table>_index_compare(struct ovsdb_idl_index_cursor *,
                                 const struct ovsrec_<table> *,
                                 const struct ovsrec_<table> *);
```

`ovsrec_<table>_index_compare` compares two rows using the same comparator used
in the cursor's index. The returned value is the same as strcmp, but defines a
specific behaviour when comparing pointers to NULL (NULL is always greater than
any other value, but when comparing NULL against NULL by definition return 1).

```
const struct ovsrec_<table> *ovsrec_<table>_index_first(struct ovsdb_idl_index_cursor *)
```

`ovsrec_<table>_index_next` moves the cursor to the first record in the index,
and return the replica's pointer to that row.

```
const struct ovsrec_<table> *ovsrec_<table>_index_next(struct ovsdb_idl_index_cursor *)
```

`ovsrec_<table>_index_next` moves the cursor to the next record in the index,
and return the replica's pointer to that row. If the cursor was in the last row
(or was already NULL) then returns NULL.

```
const struct ovsrec_<table> *ovsrec_<table>_index_find(struct ovsdb_idl_index_cursor *, const struct ovsrec_<table> *)
```

`ovsrec_<table>_index_find` moves the cursor to the first record in the index
that matches (by the index comparator) the given value, or NULL if none found.

```
const struct ovsrec_<table> *ovsrec_<table>_index_forward_to(struct ovsdb_idl_index_cursor *, const struct ovsrec_<table> *)
```

`ovsrec_<table>_index_forward_to` moves the cursor to the first record in the
index equal or greater than (by the index comparator) the given value, or NULL
if none found.

```
const struct ovsrec_<table> *ovsrec_<table>_index_get_data(const struct ovsdb_idl_index_cursor *)
```

`ovsrec_<table>_index_get_data` returns a pointer to the replica's row that is
pointed by the cursor, or NULL.

## Priority Sessions


### Usage from the C IDL

To change the priority of a session with the IDL run the command
`ovsdb_idl_set_identity`, that receives an IDL and the session name.
That function must be called after the IDL receives the initial replica.

With the function `ovsdb_idl_get_priority` the priority assigned by
the OVSDB Server can be retrieved (after an `ovsdb_idl_run`).

### Usage with ovsdb-client

Call the ovsdb-client with:
```
ovsdb-client identify <name>
```
It returns the priority assigned to <name> by the OVSDB Server.

### Priorities file

The priority file is a JSON file with the identifiers as keys,
and the corresponding priority as the value. For example:
```
{
    "0": ["criticald", "cruciald", "urgentd"],
    "7": ["exampled],
    "15": ["notimportantd", "notcriticald"]
}
```

The OVSDB Server receives the path to the priorities file with the
--priority-file flag.

That file can be updated and reloaded at runtime using ovs-appctl:
```
ovs-appctl -t ovsdb-server ovsdb-server/priority-reload
```

## Wait Monitoring and Blocking Waits

The wait monitoring feature can be divided in monitoring blocking waits and
performing blocking waits.

### Wait Monitoring

For monitoring a blocking wait the client must first tell OVSDB its intentions
of monitoring some columns in a table. In the JSON RPC protocol there are the
new methods `wait_monitor` and `wait_monitor_cancel` to do that.

When using the IDL the process is like follows:

```c
/* Allocate a struct ovsdb_idl_wait_monitor_request to store
 * the new wait monitored columns. */
struct ovsdb_idl_wait_monitor_request wait_monitor_request;

/* Initialize the request */
ovsdb_idl_wait_monitor_create_txn(idl, &wait_monitor_request);

/* Add or remove columns from the wait monitored columns set */
ovsdb_idl_wait_monitor_add_column(&wait_monitor_request,
                                  &ovsrec_table_example,
                                  &ovsrec_example_col_examplecolumn);
ovsdb_idl_wait_monitor_add_column(&wait_monitor_request,
                                  &ovsrec_table_example,
                                  &ovsrec_example_col_examplecolumn2);
ovsdb_idl_wait_monitor_remove_column(&wait_monitor_request,
                                     &ovsrec_table_example,
                                     &ovsrec_example_col_examplecolumn2);
ovsdb_idl_wait_monitor_add_column(&wait_monitor_request,
                                  &ovsrec_table_othertable,
                                  &ovsrec_example_col_column1);
/* Send the wait monitor request to OVSDB Server (and check the result) */
if (!ovsdb_idl_wait_monitor_send_txn(&wait_monitor_request)) {
    /* Handle error*/
}
```

The wait monitor request can be performed at any time during the execution of
the program.

### Processing blocking waits notifications

After the client performs a `wait_monitor` it will receive `wait_update`
notifications from the OVSDB Server, requesting it to unblock those waits. At
this moment the client can perform other actions, for example: updating data.

The client can iterate over the `wait_update` requests using the following code:

```c
struct ovsdb_idl_wait_update *req, *next;
WAIT_UPDATE_FOR_EACH_SAFE(req, next, idl) {
    /* Do something with req
     * struct ovsdb_idl_wait_update includes the requested
     * table, rows and columns.
     */

    /* Unblock the client's blocking_wait. If the blocking wait
     * isn't unblocked then it will timeout and the whole
     * transaction will fail. */
    ovsdb_idl_wait_unblock(idl, req);

    /* Remove the request from the requests list */
    ovsdb_idl_wait_update_destroy(req);
}
```

### Performing blocking waits
A client can perform a `blocking_wait` operation that blocks a transaction
until all the clients wait monitoring the columns requested unblock the
request.

With the IDL a `blocking_wait` is performed as follows:

```c
/* Create a transaction as usual */
txn = ovsdb_idl_txn_create(idl);
/* Create an ovsdb_idl_txn_wait_unblock */
struct ovsdb_idl_txn_wait_unblock *wait_req;
/* ovsdb_idl_txn_create_wait_until_unblock receives as parameter
 * the requested table, and a timeout in milliseconds. */
wait_req = ovsdb_idl_txn_create_wait_until_unblock(&ovsrec_table_example, 5000);
/* Add columns or rows as desired, both fields could be empty */
ovsdb_idl_txn_wait_until_unblock_add_column(wait_req, &ovsrec_example_col_testcolumn);
ovsdb_idl_txn_wait_until_unblock_add_row(wait_req, (struct ovsdb_idl_row*) ovsrec_example_first(idl));
/* Add the ovsdb_idl_txn_wait_unblock to the transaction */
ovsdb_idl_txn_add_wait_until_unblock(txn, wait_req);
/* Commit transaction, using the commit_block or the non-blocking commit */
status = ovsdb_idl_txn_commit_block(txn);
```
