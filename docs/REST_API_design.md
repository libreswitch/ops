# High Level Design of REST API

## Contents

- [Introduction](#introduction)
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [OVSDB schema](#ovsdb-schema)
- [HTTPS support](#https-support)
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
```https://172.17.0.3/rest/v1/system/ports```


## References

* [REST API user guide](/documents/user/REST_API_user_guide)
* [REST API rendering component design](/documents/user/REST_API_design)
