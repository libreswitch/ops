# High Level Design of REST API

## Contents

- [Introduction](#introduction)
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [OVSDB schema](#ovsdb-schema)
- [User account management](#user-account-management)
- [HTTPS support](#https-support)
- [Logs support](#logs-support)
- [References](#references)

## Introduction
The feature is a combination of the REST API documentation rendering engine and the corresponding REST API service engine that serves the supported API functionalities.

## Design choices

This feature sets and changes switch configurations, as well as retrieves status and statistics information of the switch. It also serves as a building block for the web UI of the switch.

Its main function exposes operations on OVSDB through the REST API. The resources serviced by the API are therefore based on the schema of the OVSDB.

## Participating modules

This feature has two modules:
- REST daemon (restd) -- Serves REST API requests.
- REST API rendering (restapi) -- Configured so that it points to the same host and the same port as the entry point for all of the documented REST API operations.

```ditaa
           URL path
               +
               |
   +-----------+------------+
   +                        +
 /api                /rest/v1/system
   +                        +
   |                        |
   |                        |
   v                        v
REST API                REST API
rendering               servicing

```

The URL path name space is used to direct web requests to the appropriate module for processing according to the diagram above.

During the switch image build time, the REST API servicing module generates and installs the REST API documentation file in JSON format, for the REST API rendering module to use at runtime.

## OVSDB schema

The new OVSDB schema is an extended schema file based on the original OVSDB schema file. The new schema is marked with two additional groups of tags, which indicate how this feature exposes each resource through the REST API:

- The "category": ["configuration" | "status" | "statistics"] tags
indicate for each column of a table, whether the attribute is categorized as configuration (readable and writable), status (read-only), or statistics (mostly counters that change frequently). For those columns of the table that are not marked with any one of the category tags, they are not exposed in the REST API.

- The "relationship": ["1:m" | "m:1" | "reference"] tags
indicate for those columns pointing to other tables, whether the relationship between the table cited at the column and the current table is child ("1:m"), parent ("m:1"), or reference. The REST API utilizes this information to construct a resource structure among the tables in the schema file.

The two groups of tags can be used simultaneously when the column refers to another table. For the columns that are tagged with "relationship", the "category" tag can be either "configuration" (read-write) or "status" (read-only).

A sanitizing Python script is run to strip the extended schema file of the two groups of tags added, so that other modules that are aware of only the original OVSDB schema can operate as usual.

## User account management
### Design

The `/account` resource is available in the REST API, to allow the user to
change their own password and query their role and permissions. This resource
requires a user to be already logged in into the system. The request and
response bodies follow the "category" tags used in OVSDB resources.

### Account management API definitions

#### GET method
`GET https://10.10.0.1/account`

Returns a data structure containing the currently logged in user's role and
list of permissions within the "status" tag, along with a `200 OK` HTTP
response status code if the query is successful. A sample reponse data is as
follows:

```
    {
        "status": {
            "role": "ops_netop",
            "permissions": ["READ_SWITCH_CONFIG", "WRITE_SWITCH_CONFIG"]
        }
    }
```

#### PUT method
`PUT https://10.10.0.1/account`

Allows the currently logged in user to change their own password. A successful
password change is indicated by a `200 OK` HTTP reponse status code. The
request body must contain the user's current password and new password within
the "configuration" tag, as follows:


```
    {
        "configuration": {
            "password": "current_password",
            "new_password": "new_password"
        }
    }
```

## HTTPS support

The REST API runs only on the HTTPS protocol. The HTTPS protocol provides authentication of the REST server, and additionally provides encryption of exchanged data between the REST server and the client. Authentication/encryption is done by security protocols like SSL/TLS within the HTTP connection.

The REST server requires SSL certificate to run in HTTPS mode. A self-signed SSL certificate and private key files are pre-installed at "/etc/ssl/certs/server.crt" and "/etc/ssl/certs/server-private.key" respectively on the server. Steps to obtain a self-signed certificate are standard. The self-signed SSL certificate is mainly for development purposes and testing. For proper authentication, a user may have to purchase a SSL certificate for a specific hostname from a trusted Certificate Authority (CA), for example Symantec.

Once the SSL certificate is enrolled with a trusted CA, the certificate file and private key file are copied into predefined locations, "/etc/ssl/certs/server.crt" and "/etc/ssl/certs/server-private.key", on the REST server using scp. The client uses the CA certificate to verify the server authenticity when establishing an HTTPS connection.
Following is a sample client side code snippet that is compatible with Python 2.7.9 and retrieves ports information from a REST server:
```ditaa
import ssl
import httplib

sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
sslcontext.verify_mode = ssl.CERT_REQUIRED
sslcontext.check_hostname = True
sslcontext.load_verify_locations("/etc/ssl/certs/server.crt")
url = '/rest/v1/system/ports'
conn = httplib.HTTPSConnection("172.17.0.3", 443, context=sslcontext)
conn.request('GET', url, None, headers=_headers)
response = conn.getresponse()
```

Following is an example URL with HTTPS to query ports on the system from a web browser. HTTPS uses the default port 443 if not specified.
```
https://172.17.0.3/rest/v1/system/ports
```

## Logs Support
### Design
REST APIs for logs provides an interface to query the systemd journal. The API internally calls the `journalctl` Linux command to read the systemd journal. The `journalctl` command was chosen because it has several filtering options and is an easy tool for accessing all of the systemd/kernel logs. It also provides the output in JSON format which is required for REST. The REST server does not modify the output from the `journalctl` command as it is already in JSON format. Each log entry in the systemd journal is represented in JSON as shown below. The response may have several such entries depending on the filtering options.
```
{
        "__CURSOR" : "s=917df6ad70ee41cdba3f8fb28118e81b;i=4177e;b=78537df4874046d5ae9f251193b9f0bc;m=1b8905391e8;t=52b0c001a4714;x=75ceb440bae113ce",
        "__REALTIME_TIMESTAMP" : "1454705424877332",
        "__MONOTONIC_TIMESTAMP" : "1892207006184",
        "_BOOT_ID" : "78537df4874046d5ae9f251193b9f0bc",
        "_TRANSPORT" : "stdout",
        "PRIORITY" : "6",
        "SYSLOG_FACILITY" : "3",
        "SYSLOG_IDENTIFIER" : "ops_ntpd",
        "MESSAGE" : "2016-02-05T20:50:24Z |389737| ops-ntpd | INFO | Sync NTPD -> OVSDB : done",
        "_PID" : "230",
        "_UID" : "0",
        "_GID" : "0",
        "_COMM" : "python",
        "_EXE" : "/usr/bin/python2.7",
        "_CMDLINE" : "python /usr/bin/ops_ntpd",
        "_CAP_EFFECTIVE" : "3fffffffff",
        "_SYSTEMD_CGROUP" : "/system.slice/ops-ntpd.service",
        "_SYSTEMD_UNIT" : "ops-ntpd.service",
        "_SYSTEMD_SLICE" : "system.slice",
        "_MACHINE_ID" : "79f8ca920cda4483ac8d36f63c7dd5cb",
        "_HOSTNAME" : "switch"
}
```

### Log API definitions
`GET https://10.10.0.1/rest/v1/logs`
Returns the most recent 1000 log entries from the systemd journal in JSON. The response is displayed by the newest entries first. This number is not currently user configurable and is fixed at 1000. It can be made user configurable in the future, if needed.

`GET https://10.10.0.1/rest/v1/logs?priority=<0-7>`
Returns log output filtered by the given log priority level. Priority levels are similar to syslog levels 0-7. All logs with the given priority level or lower are returned.

`GET https://10.10.0.1/rest/v1/logs?since=yyyy-mm-dd hh:mm:ss&until=yyyy-mm-dd hh:mm:ss`
Returns the output filtered by the given time window.
Instead of a specific time, a user can also give relative words like "yesterday", "today", "now", "1 day ago", "1 hour ago", "1 minute ago". Words like "hour ago", "minute ago" and "day ago" must precede with a positive integer and can be in plural form too. For example, 2 hours ago or 1 hour ago. Words other than the ones mentioned above return an error.

`GET https://10.10.0.1/rest/v1/logs?since=2 hours ago`
Returns log entries generated in the past 2 hour time window.


`GET https://10.10.0.1/rest/v1/logs?after-cursor=cursor_string`
Returns logs *after* the location specified by the given cursor. The cursor is maintained by the systemd journald service per log entry, and is displayed in the response for each log entry.  If the user wants to retrieve logs since the last request, the user has to provide the cursor value of the last log entry returned in the previous request. Here is an example for cursor string: `s=66e980e3c7bc46bea313de741ce481bc;i=8598c;b=78537df4874046d5ae9f251193b9f0bc;m=285fc88ec04;t=52bd96c4fa130;x=2f797c4c0bb5eafc`


`GET https://10.10.0.1/rest/v1/logs?offset=<int>&limit=<int>`
As the log output can be huge, a user may request the number of log entries in a response. To do so, the user needs to pass `offset` and `limit` parameters. The `Offset` parameter is the starting log entry to obtain the results which starts with 0. The `limit` parameter defines the number of JSON log entries in the response and the valid range is 1 - 1000. These two parameters can be used along with other filtering parameters separated by `&`.
For example, to retrieve the first 10 logs since the bootup, use `GET https:////10.10.0.1/rest/v1/logs?offset=0&limit=10`. To retrieve the next 10 logs, use `GET https:////10.10.0.1/rest/v1/logs?offset=10&limit=10`. The offset in the next request is typically the previous offset plus the limit. Following is an example to request log entries filtered based on priority level 6, and limit 5 log entries in the response:
    `GET https://10.10.0.1/rest/v1/logs?priority=6&offset=0&limit=5`


`Get https://10.10.0.1/rest/v1/logs?<field>=<value>`
Returns log output based on the fields matched to the given value in the systemd journal. A user may give multiple match field/values in one request.
    If one match field is specified, all entries with a field matching the expression are returned in response.
    ` https://10.10.0.1/rest/v1/logs?MESSAGE_ID=50c0fa81c2a545ec982a54293f1b1945`
    If two different fields are matched, only entries matching both expressions at the same time are returned.
    `https://10.10.0.1/rest/v1/logs?MESSAGE_ID=50c0fa81c2a545ec982a54293f1b1945&SYSLOG_INDETIFIER=ops-bgpd`
    If two matches refer to the same field, all entries matching either expression are returned.
    `https://10.10.0.1/rest/v1/logs?_PID=150&_PID=178`

The following fields are supported:

|Field       | Description                                     |
|----------  |-------------------------------------------------|
|MESSAGE     | The exact log message that is expected.|
|MESSAGE_ID  | A 128-bit message identifier ID for recognizing certain message types. All openswitch events are stored with this message ID 50c0fa81c2a545ec982a54293f1b1945 in the systemd journal. Use this MESSAGE_ID to query all of the events.|
|PRIORITY     | A priority value between 0 ("emerg") and 7 ("debug").|
|SYSLOG_IDENTIFIER | Identifier string is the module generating the log message. Use this field to filter logs by a specific module.|
|_PID | The Process ID of the process that is generating the log entry.|
|_UID | The User ID of the process that is generating the log entry.|
|_GID | The Group ID of the process that is generating the log entry.|

Following is an example of a log API response with offset=0&limit=2 which limits the log entries to 2 in the response:
```
[{"_BOOT_ID": "f43a84807a2d4b1389c87867fe6aaec3", "__REALTIME_TIMESTAMP": "1455653778503173", "_CAP_EFFECTIVE": "25402800cf", "__MONOTONIC_TIMESTAMP": "1556353467723", "_SYSTEMD_UNIT": "systemd-journald.service", "_MACHINE_ID": "5f7d6bb2aee84e5cb5bb3007b2911e7d", "_PID": "20", "_CMDLINE": "/lib/systemd/systemd-journald", "_SYSTEMD_CGROUP": "/system.slice/systemd-journald.service", "_SYSTEMD_SLICE": "system.slice", "PRIORITY": "6", "_EXE": "/lib/systemd/systemd-journald", "_UID": "0", "_TRANSPORT": "driver", "_GID": "0", "__CURSOR": "s=4696aa7b4c7b4090850ee29b7748df5c;i=2;b=f43a84807a2d4b1389c87867fe6aaec3;m=16a5de5454b;t=52be8ce623605;x=7ac41464416ef406", "MESSAGE": "Runtime journal is using 8.0M (max allowed 197.4M, trying to leave 296.2M free of 1.9G available \uffffffe2\uffffff86\uffffff92 current limit 197.4M).", "MESSAGE_ID": "ec387f577b844b8fa948f33cad9a75e6", "_COMM": "systemd-journal", "_HOSTNAME": "f37f0cd9a774"}, {"_BOOT_ID": "f43a84807a2d4b1389c87867fe6aaec3", "__REALTIME_TIMESTAMP": "1455653778503270", "_CAP_EFFECTIVE": "25402800cf", "__MONOTONIC_TIMESTAMP": "1556353467820", "_SYSTEMD_UNIT": "systemd-journald.service", "_MACHINE_ID": "5f7d6bb2aee84e5cb5bb3007b2911e7d", "_PID": "20", "_CMDLINE": "/lib/systemd/systemd-journald", "_SYSTEMD_CGROUP": "/system.slice/systemd-journald.service", "_SYSTEMD_SLICE": "system.slice", "PRIORITY": "6", "_EXE": "/lib/systemd/systemd-journald", "_UID": "0", "_TRANSPORT": "driver", "_GID": "0", "__CURSOR": "s=4696aa7b4c7b4090850ee29b7748df5c;i=3;b=f43a84807a2d4b1389c87867fe6aaec3;m=16a5de545ac;t=52be8ce623666;x=568d82819815b54d", "MESSAGE": "Journal started", "MESSAGE_ID": "f77379a8490b408bbe5f6940505a777b", "_COMM": "systemd-journal", "_HOSTNAME": "f37f0cd9a774"}]
```

## References

* [REST API user guide](/documents/user/REST_API_user_guide)
* [REST API rendering component design](/documents/user/REST_API_design)
