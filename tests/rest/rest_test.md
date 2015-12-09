REST API Test Cases
===================

## Contents
- [REST API put, get methods for URL "/rest/v1/system"](#rest-api-put-get-methods-for-url-restv1system)
- [REST API get method for URl "/rest/v1/system/subsystems"](#rest-api-get-method-for-url-restv1systemsubsystems)
- [REST API put, get, delete methods for URL "/rest/v1/system/interfaces/{id}"](#rest-api-put-get-delete-methods-for-url-restv1systeminterfacesid)
- [REST API get method for URL "/rest/v1/system/vrfs"](#rest-api-get-method-for-url-restv1systemvrfs)
- [REST API get method for URL "/rest/v1/system/route_maps/{id}"](#rest-api-get-method-for-url-restv1systemroutemapsid)
- [REST API get method for URL "/rest/v1/system/interfaces"](#rest-api-get-method-for-url-restv1systeminterfaces)
- [REST API put method with invalid data for URLs](#rest-api-put-method-with-invalid-data-for-urls)
- [REST API login authentication](#rest-api-login-authentication)
- [REST API startup config verify](#rest-api-startup-config-verify)
- [Query port](#query-port)
- [Create a port](#create-a-port)
- [Update a port](#update-a-port)
- [Delete a port](#delete-a-port)
- [Query interface using recursive GET](#query-interface-using-recursive-get)
- [Query port with pagination](#query-port-with-pagination)
- [Sort ports by field](#sort-ports-by-field)
- [Sort ports by field combination](#sort-ports-by-field-combination)

##  REST API put, get methods for URL "/rest/v1/system"
### Objective
The objective of the test case is to configure the system through the Standard REST API PUT Method.
### Requirements
The requirements for this test case are:
- OpenSwitch
- Ubuntu Workstation

#### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
### Description
Configure the system through the Standard REST API PUT method.

> **STEPS:**

> 1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
> 2. Configure an IPV4 address on the switch management interfaces.
> 3. Configure the IPV4 address on the Ubuntu workstation.
> 4. Configure the system through the Standard REST API PUT method for the URI "/rest/v1/system".
> 5. Validate the system configuration with the HTTP return code for the URI "/rest/v1/system".
> 6. Execute the Standard REST API GET method for URI "/rest/v1/system".
> 7. Validate the GET method HTTP return code for "/rest/v1/system" and its respective values.

### Test result criteria
#### Test pass criteria
- The first test passes (steps 4 and 5), if the standard REST API PUT method returns HTTP code 200 OK for the URI "/ rest/v1/system".
- The second test passes (steps 6 and 7), if the standard REST API GET method returns HTTP code 200 OK for the URI "/rest/v1/system" and the returned data is identical to the date used for the PUT.
#### Test fail criteria
- The first test fails if the standard REST API PUT method does not return HTTP code 200 for the URI "/rest/v1/system".
- The second test fails if the standard REST API GET method does not return HTTP code 200 for the URI "/rest/v1/system" or the returned data is not identical to the data used for PUT.

##  REST API get method for URl "/rest/v1/system/subsystems"
### Objective
The objective of the test case is to validate the subsystem through the standard REST API GET method.
### Requirements
The requirements for this test case are:
- OpenSwitch
- Ubuntu Workstation

### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
### Description
This test case validates the subsystem through the standard REST API GET method.

> **STEPS:**

> 1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
> 2. Configure the IPV4 address on the switch management interfaces.
> 3. Configure the IPV4 address on the Ubuntu workstation.
> 4. Execute the Standard REST API GET method for URI "/rest/v1/system/subsystems".
> 5. Validate the GET method HTTP return code for "/rest/v1/system/subsystems" and its respective values.

### Test result criteria
#### Test pass criteria
The test passes if the standard REST API GET method returns HTTP code 200 for the URI "/r est/v1/system/subsystems" and the returned data is identical.
#### Test fail criteria
The test case is fails if the standard REST API GET method does not return the HTTP code 200 for the URI "/rest/v1/system/subsystems".

##  REST API put, get, delete methods for URL "/rest/v1/system/interfaces/{id}"
### Objective
The objective of the test case is to validate the "/rest/v1/system/interfaces/{id}" through the standard REST API GET method.
### Requirements
The requirements for this test case are:
- OpenSwitch
- Ubuntu Workstation
### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
### Description
The objective of the test case is to validate the "/rest/v1/system/interfaces/{id}" through the standard REST API GET method.

> **STEPS:**

> 1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
> 2. Configure the IPV4 address on the switch management interfaces.
> 3. Configure the IPV4 address on the Ubuntu workstation.
> **Test 1**
> 1. Configure the "/rest/v1/system/interfaces/{id}" through Standard REST API PUT method.
> 2. Validate the "/rest/v1/system/interfaces/{id}" configuration with the HTTP return code.
> **Test 2**
> 1. Execute the Standard REST API GET method for URI "/rest/v1/system/interfaces/{id}".
> 2. Validate the GET Method HTTP return code for "/rest/v1/system/interfaces/{id}" and its respective values.
> **Test 3**
> 1. Execute Standard REST API DELETE method for URI "/rest/v1/system/interfaces/{id}".
> 2. Validate the DELETE method HTTP return code for "/rest/v1/system/interfaces/{id}".
> **Test 4**
> 1. Execute Standard REST API GET Method for URI "/rest/v1/system/interfaces/{id}".
> 2. Validate the GET method HTTP return code for "/rest/v1/system/interfaces/{id}".

### Test result criteria
#### Test pass criteria
- The first test passes if the standard REST API PUT method returns HTTP code 200 OK for the URI "/rest/v1/system/interfaces/{id}".
- The second test passes if the standard REST API GET method returns HTTP code 200 OK for the URI "/rest/v1/system/interfaces/{id}" and the returned data is identical to the date used for the PUT.
- The third test passes if the standard REST API DELETE method returns HTTP code 204 for the URI "/rest/v1/system/interfaces/{id}".
- The fourth test passes, if the standard REST API GET method does not return HTTP code 200 OK for the URI "/rest/v1/system/interfaces/{id}".

#### Test fail criteria
- The first test fails if the standard REST API PUT method does not return HTTP code 200 for the URI "/rest/v1/system/interfaces/{id}".
- The second test fails if the standard REST API GET method does not return HTTP code 200 for the URI "/rest/v1/system/interfaces/{id}" or the returned data is not identical to the data used for PUT.
- The third test fails if the standard REST API DELETE method does not return HTTP code 204 for the URI "/rest/v1/system/interfaces/{id}".
- The fourth test fails if the standard REST API GET method returns HTTP code 200 OK for the URI "/rest/v1/system/interfaces/{id}".

##  REST API get method for URL "/rest/v1/system/vrfs"
### Objective
The objective of this test case is to validate the "/rest/v1/system/vrfs" through the standard REST API GET method.
### Requirements
The requirements for this test case are:
- OpenSwitch
- Ubuntu Workstation

### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
### Description
Validate the "/rest/v1/system/vrfs" through the standard REST API GET method.

> **STEPS:**

> 1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
> 2. Configure the IPV4 address on the switch management interfaces.
> 3. Configure the IPV4 address on the Ubuntu workstation.
> 4. Execute the Standard REST API GET Method for URI "/rest/v1/system/vrfs".
> 5. Validate the GET Method HTTP return code for "/rest/v1/system/vrfs" and its respective values.

### Test result criteria
#### Test pass criteria
The test case is passes if the standard REST API GET method returns HTTP code 200 for the URI "/rest/v1/system/vrfs" and if the returned data is identical.
#### Test fail criteria
The test case fails if the standard REST API GET method does not return HTTP code 200 for the URI "/rest/v1/system/vrfs".

##  REST API get method for URL "/rest/v1/system/route_maps/{id}"
### Objective
The objective of this test case is to validate the "/rest/v1/system/route_maps/{id}" through the standard REST API GET method.
### Requirements
The requirements for this test case are:
- OpenSwitch
- Ubuntu Workstation

### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
### Description
The test case validates the "/rest/v1/system/route_maps/{id}" through the standard REST API GET method.
> **STEPS:**

> 1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
> 2. Configure the IPV4 address on the switch management interfaces.
> 3. Configure the IPV4 address on the Ubuntu workstation.
> 4. Execute the Standard REST API GET Method for URI "/rest/v1/system/route_maps/{id}".
> 5. Validate the GET method HTTP return code for "/rest/v1/system/route_maps/{id}" and its respective values.

### Test result criteria
#### Test pass criteria
This test case passes if the standard REST API GET method returns HTTP code 200 for the URI "/rest/v1/system/route_maps/{id}" and the returned data is identical.
#### Test fail criteria
This test case fails if the standard REST API GET method does not return HTTP code 200 for the URI "/rest/v1/system/route_maps/{id}".

##  REST API get method for URL "/rest/v1/system/interfaces"
### Objective
The objective of the test case is to validate the "/rest/v1/system/interfaces" through the standard RESTAPI GET method.
### Requirements
The requirements for this test case are:
- OpenSwitch
- Ubuntu Workstation
-
### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
### Description
The test case validates the "/rest/v1/system/interfaces" through the standard RESTAPI GET method.

> **STEPS:**

> 1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
> 2. Configure the IPV4 address on the switch management interfaces.
> 3. Configure the IPV4 address on the Ubuntu workstation.
> 4. Execute the Standard REST API GET Method for URI "/rest/v1/system/interfaces".
> 5. Validate the GET method HTTP return code for "/rest/v1/system/interfaces" and its respective values.

### Test result criteria
#### Test pass criteria
The test case passes if the standard REST API GET method returns HTTP code 200 for the URI "/rest/v1/system/interfaces" and the returned data is identical.
#### Test fail criteria
The test case is fails if the standard REST API GET method does not return HTTP code 200 for the URI "/rest/v1/system/interfaces".

##  REST API put method with invalid data for URLs
### Objective
The objective of this test case is to configure the REST API PUT method with invalid data for URIs.
### Requirements
The requirements for this test case are:
- OpenSwitch
- Ubuntu Workstation

### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
### Description
Configure the REST API PUT method with invalid data for the URIs.

> **STEPS:**

> 1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
> 2. Configure the IPV4 address on the switch management interfaces.
> 3. Configure the IPV4 address on the Ubuntu workstation.
> 4. Configure the standard REST API PUT method with invalid data for URIs.
> 5. Validate that the standard REST API PUT method fails to configure with invalid data for all URIs.

### Test result criteria
#### Test pass criteria
This test case passes if the standard REST API PUT method with invalid data fails to return HTTP code 200 OK for the URIs.
#### Test fail criteria
This test case fails if the standard REST API PUT method with invalid data returns HTTP code 200 OK for the URIs.

## REST API login authentication
### Objective
The objective of this test case is to check login and authentication.
### Requirements
The requirements for this test case are:
- OpenSwitch
- Ubuntu Workstation

### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
### Description
This test case checks login and authentication.

> **STEPS:**

> 1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
> 2. Configure the IPV4 address on the switch management interfaces.
> 3. Configure the IPV4 address on the Ubuntu workstation.
> **Test 1**
> 1. Execute the Standard REST API POST method for the URI "/login" with valid credentials.
> 2. Validate the GET Method HTTP return code for the URI "/login".
> **Test 2**
> 1. Execute the Standard REST API POST method for URI "/login" with invalid credentials.
> 2. Validate that the GET method HTTP failed the return code for URI "/login".

### Test result criteria
#### Test pass criteria
- The first test passes if the standard REST API GET method returns HTTP code 200 OK for the URI "/login".
- The second test passes if the standard REST API GET method returns HTTP code 401 UNAUTHORIZED for the URI "/login".
#### Test fail criteria
- The first test fails if the standard REST API GET Method does not return HTTP code 200 for the URI "/login".
- The second test fails if the standard REST API GET Method does not return HTTP code 401 for the URI "/login".

## REST API startup config verify
### Objective
The objective for the test case is to verify that the REST API startup configuration works.
### Requirements
The requirements for this test case are:
- OpenSwitch
- Ubuntu Workstation
-
### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```
### Description
Verify that the REST API startup configuration works.

> **STEPS:**

> 1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
> 2. Configure the IPV4 address on the switch management interfaces.
> 3. Configure the IPV4 address on the Ubuntu workstation.
> 4. Execute Standard REST API PUT method for URI "/rest/v1/system" - 1st test case.
> 5. Execute Standard REST API GET method for URI "/rest/v1/system" - 2nd test case.

### Test result criteria
#### Test pass criteria
- The first test passes if the standard REST API PUT method returns HTTP code 200 OK for the URI "/rest/v1/system".
- The second test passes if the standard REST API GET method returns HTTP code 200 OK for the URI "/rest/v1/system" and the returned data is identical to the data used for the PUT.

#### Test fail criteria
- The first test fails if the standard REST API PUT method does not return HTTP code 200 for the URI "/rest/v1/system".
- The second test fails if the standard REST API GET method does not return HTTP code 200 for the URI "/rest/v1/system" or the returned data is not identical to the data used for PUT.

REST API ports Resource test cases
==================================

## Query port

### Objective
The test case verifies queries for:

- All ports
- A specific port
- A non-existent port

###  Requirements

Period after exist

### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test setup

** Switch 1 ** has a port with the name Port1 and with the following configuration data:

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1"],
"trunks": [413],
"ip4_address_secondary": ["192.168.0.1"],
"lacp": "active",
"bond_mode": "l2-src-dst-hash",
"tag": 654,
"vlan_mode": "trunk",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
"external_ids": {"extid1key": "extid1value"},
"bond_options": {},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {},
"ip4_address": "192.168.0.1",
"admin": "up"
}
}
```

### Description

1. Verify if the port is in the port list.

- a. Execute the GET request over /rest/v1/system/ports.
- b. Verify if the HTTP response is 200 OK.
- c. Confirm that the returned port list has at least one element.
- d. Ensure that URI /rest/v1/system/ports/Port1 is in the response data.

2. Verify if a specific port exists.

- Execute GET request over rest/v1/system/ports/Port1.
- a. Verify if the HTTP response is 200 OK.
- b. Confirm if the response data is not empty.
- c. Ensure that the response data has the keys: "configuration", "status" and "statistics".
- d. Verify if the configuration data is equal to the Port1 configuration data.

3. Verify if a non-existent port exists.
- a. Execute the GET request over rest/v1/system/ports/Port2.
- b. Verify if the HTTP response is 404 NOT FOUND.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

-Querying a port list for:
      -A 200 OK HTTP response.
      -At least one port in the port list.
      -A URI "rest/v1/system/ports/Port1" in the port list returned from the  rest/v1/system/ports URI.

- Querying Port1 for:
   - An HTTP response of 200 OK when doing a GET request over
     "rest/v1/system/ports/Port1".
   - A response data that is not empty
   - A response data that contains keys: "configuration", "status",
     and "statistics".
   - Preset port configuration data that is equal to Port1.

- Querying for an HTTP response of 404 NOT FOUND on a non-existent port:

#### Test fail criteria

This test fails when:

- Querying a post list for:
   - An HTTP response is not equal to 200 OK

   - A GET request to "rest/v1/system/ports" and "Port1" is in the Ports URI list.

- Performing a GET request over "rest/v1/system/ports/Port1" and the HTTP response is not equal to 404 NOT FOUND for Port1.

- Querying for a non-existent port and the HTTP response is not equal to 404 NOT FOUND.

## Create a port

### Objective

The test case verifies:
- Creating a port.
- Creating a port with the same name as another port.
- Port data such as ranges, types, allowed values, malformed JSON, and missing attributes.

###  Requirements

Bridge "bridge_normal" must exist.

### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test setup

### Description

#### Create port

1. Execute a POST request with /rest/v1/system/ports and with the following data and verify if the HTTP response is 201 CREATED.

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1"],
"trunks": [413],
"ip4_address_secondary": ["192.168.0.1"],
"lacp": "active",
"bond_mode": "l2-src-dst-hash",
"tag": 654,
"vlan_mode": "trunk",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
"external_ids": {"extid1key": "extid1value"},
"bond_options": {},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {},
"ip4_address": "192.168.0.1",
"admin": "up"
},
"referenced_by": [{"uri":"/rest/v1/system/bridges/bridge_normal"}]
}
```

2. Execute a GET request with /rest/v1/system/ports/Port1 and verify if the response is 200 OK.
3. Verify that the configuration response data from Step 2 is the same as the configuration data from Step 1.

#### Create an existing port
Verify that the HTTP response returns BAD_REQUEST when creating a existing port with the name "Port1".

1. Execute a POST request with /rest/v1/system/ports, and with the name "Port1".
```
"name": "Port1"
```
2. Confirm that the HTTP response is 400 BAD REQUEST.

#### Data validation

##### Data types validation

###### Invalid string type

1. Set the "ip4_address" value to:
```
"ip4_address": 192
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid string type

1. Set the "ip4_address" value to:
```
"ip4_address": "192.168.0.1"
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 201 CREATED.

###### Invalid integer type

1. Set the "tag" value to:
```
"tag": "675"
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid integer type

1. Set the "tag" value to:
```
"tag": 675
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 201 CREATED.

###### Invalid array type

1. Set the "trunks" value to:
```
"trunks": "654,675"
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid array type

1. Set the "trunks" value to:
```
"trunks": [654,675]
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 201 CREATED.

##### Ranges validation


###### Invalid range for string type

1. Set the "ip4_address" value to:
```
"ip4_address": "175.167.134.123/248"
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid range for string type

1. Set the "ip4_address" value to:
```
"ip4_address": "175.167.134.123/24"
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 201 CREATED.

###### Invalid range for integer type

1. Set the "tag" value to:
```
"tag": 4095
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid range for integer type

1. Set the "tag" value to:
```
"tag": 675
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 201 CREATED.

###### Invalid range for array type

1. Change the "interfaces" value to:
```
"interfaces": [ "/rest/v1/system/interfaces/1",
"/rest/v1/system/interfaces/2",
"/rest/v1/system/interfaces/3",
"/rest/v1/system/interfaces/4",
"/rest/v1/system/interfaces/5",
"/rest/v1/system/interfaces/6",
"/rest/v1/system/interfaces/7",
"/rest/v1/system/interfaces/8",
"/rest/v1/system/interfaces/9",
"/rest/v1/system/interfaces/10" ]
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid range for array type

1. Change the "interfaces" value to:
```
"interfaces": ["/rest/v1/system/interfaces/1"]
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 201 CREATED.

##### Allowed data values validation


###### Invalid data value

1. Change the "vlan_mode" value to:
```
"vlan_mode": "invalid_value"
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid data value

1. Change the "vlan_mode" value to:
```
"vlan_mode": "access"
```
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is 201 CREATED.

##### Missing attribute validation

1. Execute a POST request with /rest/v1/system/ports and without the "vlan_mode" attribute.
2. Verify that the HTTP Response is 400 BAD REQUEST.
3. Execute a POST request with /rest/v1/system/ports and with all the attributes.
4. Verify that the HTTP Response is 201 CREATED.

##### Unknown attribute validation

1. Execute a POST request with /rest/v1/system/ports and with an unknown attribute as follows:
```
"unknown_attribute": "unknown_value"
```
2. Verify that the HTTP response is 400 BAD REQUEST.
3. Execute a POST request with /rest/v1/system/ports and with all allowed attributes.
4. Verify that the HTTP Response is 201 CREATED.

##### Malformed json validation

1. Execute a POST request with /rest/v1/system/ports and with a semi-colon at the end of the json data.
2. Verify that the HTTP response is 400 BAD REQUEST.
3. Execute a POST request with /rest/v1/system/ports and without the semi-colon at the end of the json data.
4. Verify that the HTTP response is 201 CREATED.


### Test result criteria
#### Test pass criteria

The test is passing for "creating a new port" when the following results occur:

-The HTTP response is 200 OK.
-The HTTP response is 200 OK when executing a GET request with /rest/v1/system/ports/Port1.
-When the configuration data posted is the same as the retrieved port.

The test is passing for "creating a port with the same name as another port" when the HTTP response is 400 BAD REQUEST.

The test is passing for "creating a new port with a valid string type" when the HTTP response is 201 CREATED.

The test is passing for "creating a new port with a invalid string type" when the HTTP response is 400 BAD REQUEST.

The test is passing for "creating a new port with a valid integer type" when the HTTP response is 201 CREATED.

The test is passing for "creating a new port with an invalid array type" when the HTTP response is 400 BAD REQUEST.

The test is passing for "creating a new port with valid array type" when the HTTP response is 201 CREATED.

-The test is considered passing for "creating a new port with an invalid value on an attribute" when the HTTP response is 400 BAD REQUEST.

The test is passing for "creating a new port with a valid value on an attribute" when the HTTP response is 201 CREATED.

The test is passing for "creating a new port with a missing attribute" when the HTTP response is 400 BAD REQUEST.

The test is passing for "creating a new port with all the attributes" when the HTTP response is 201 CREATED

The test is passing for "creating a new port with an unknown attribute" when the HTTP response is 400 BAD REQUEST 735

The test is passing for "creating a new port with all allowed attributes" when the HTTP response is 201 CREATED.

The test is passing for "creating a new port with malformed json data" when the HTTP response is 400 BAD REQUEST.

The test is passing for "creating a new port with well-formed json data" when the HTTP response is 201 CREATED.

#### Test fail criteria

The test is failing for "creating a new port" when:

- The HTTP response is not equal to 200 OK.
- Executing a GET request with /rest/v1/system/ports/Port1 the HTTP response is not equal to 200 OK.
- The configuration data posted is not the same as the retrieved port.

The test is failing for "creating a port with the same name as another port" when the HTTP response is not equal 400 BAD REQUEST.

The test is failing for " creating a new port with an invalid string type" when the HTTP response is not equal 201 CREATED.

The test is failing for "creating a new port with an invalid string type" when the HTTP response is not equal 400 BAD REQUEST.

The test is failing for "creating a new port with a valid integer type" when the HTTP response is not equal to 201 CREATED.

The test is failing for "creating a new port with an invalid array type" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "creating a new port with valid array type" when the HTTP response is not equal to 201 CREATED.

The test is failing for "creating a new port with an invalid value on attribute" when the HTTP response is not equal 400 BAD REQUEST.

The test is failing for "creating a new port with a valid value on an attribute" when the HTTP response is not equal to 201 CREATED.

The test is failing for "creating a new port with a missing attribute" when the HTTP response is not equal 400 BAD REQUEST.

The test is failing for "creating a new port with with all the attributes" when the HTTP response is not equal to 201 CREATED.

The test is failing for "creating a new port with an unknown attribute" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "creating a new port with all allowed attributes" when the HTTP response is not equal to 201 CREATED.

The test is failing for "creating a new port with malformed json data" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "creating a new port with well-formed json data" when the HTTP response is not equal to 201 CREATED.


## Update a port

### Objective

The test case verifies the following:
- Modifying a port.
- Trying to modify the name of the port.
- Port data such as ranges, types, allowed values, malformed JSON, and missing attributes.

###  Requirements

Period after exist.

### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test setup

** Switch 1 ** has a port with the name "Port1" and with the following configuration data:

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1"],
"trunks": [413],
"ip4_address_secondary": ["192.168.0.1"],
"lacp": "active",
"bond_mode": "l2-src-dst-hash",
"tag": 654,
"vlan_mode": "trunk",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
"external_ids": {"extid1key": "extid1value"},
"bond_options": {},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {},
"ip4_address": "192.168.0.1",
"admin": "up"
}
}
```

### Description

#### Update port

1. Execute a PUT request with /rest/v1/system/ports/Port1 and with the following data. Verify that the HTTP response is 200 OK.

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1", "/rest/v1/system/interfaces/2"],
"trunks": [400],
"ip4_address_secondary": ["192.168.0.2"],
"lacp": "passive",
"bond_mode": "l3-src-dst-hash",
"tag": 600,
"vlan_mode": "access",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:8225",
"external_ids": {"extid2key": "extid2value"},
"bond_options": {},
"mac": "01:23:45:63:90:ab",
"other_config": {"cfg-2key": "cfg2val"},
"bond_active_slave": "slave1",
"ip6_address_secondary": ["2001:0db8:85a3:0000:0000:8a2e:0370:7224"],
"vlan_options": {},
"ip4_address": "192.168.0.2",
"admin": "up"
},
"referenced_by": [{"uri":"/rest/v1/system/bridges/bridge_normal"}]
}
```

2. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is 200 OK.
3. confirm that the configuration response data from Step 2 is the same as the configuration data from Step 1.

#### Update port using If-Match
1. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is 200 OK.
2. Read the entity tag provided by the server
3. Set the "tag" value to:
```
"tag": 601
```
4. Execute a PUT request with /rest/v1/system/ports/Port1 including and If-Match Header using entity tag read at step 2
5. Verify that the response is 200 OK
6. Confirm that tag value was updated

#### Update port using If-Match (star as etag)
1. Set the "tag" value to:
```
"tag": 602
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 including an If-Match Header using '"*"' as entity tag
3. Verify that the response is 200 OK
4. Confirm that tag value was updated

#### Update port using If-Match change applied
1. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is 200 OK.
2. Read the entity tag provided by the server
2. Execute a PUT request with /rest/v1/system/ports/Port1 including and If-Match Header using entity tag different than the one read at step 2
3. Verify that the response is 204 NO CONTENT

#### Update port using If-Match Precondition Failed
1. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is 200 OK.
2. Read the entity tag provided by the server
3. Set the "tag" value to:
```
"tag": 603
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 including and If-Match Header using entity tag different than the one read at step 2
3. Verify that the response is 412 PRECONDITION FAILED


#### Update port name

1. Set the name of the port to "Port2"
```
"name": "Port2"
```
2. Execute a PUT request with /rest/v1/system/ports/Port1.
3. Verify that the HTTP response is 200 OK.
4. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is 200 OK.
5. Confirm that the port is still named "Port1".

#### Data validation

##### Data types validation

###### Invalid string type

1. Set the "ip4_address" value to:
```
"ip4_address": 192
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid string type

1. Set the "ip4_address" value to:
```
"ip4_address": "192.168.0.1"
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify if the HTTP response is 200 OK.

###### Invalid integer type

1. Set the "tag" value to:
```
"tag": "675"
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid integer type

1. Set the "tag" value to:
```
"tag": 675
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 200 OK.

###### Invalid array type

1. Set the "trunks" value to:
```
"trunks": "654,675"
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid array type

1. Set the "trunks" value to:
```
"trunks": [654,675]
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 200 OK.

##### Ranges Validation


###### Invalid range for string type

1. Set the "ip4_address" value to:
```
"ip4_address": "175.167.134.123/248"
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid range for string type

1. Set the "ip4_address" value to:
```
"ip4_address": "175.167.134.123/24"
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 200 OK.

###### Invalid range for integer type

1. Set the "tag" value to:
```
"tag": 4095
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid range for integer type

1. Set the "tag" value to:
```
"tag": 675
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 200 OK.

###### Invalid range for array type

1. Change the "interfaces" value to:
```
"interfaces": [ "/rest/v1/system/interfaces/1",
"/rest/v1/system/interfaces/2",
"/rest/v1/system/interfaces/3",
"/rest/v1/system/interfaces/4",
"/rest/v1/system/interfaces/5",
"/rest/v1/system/interfaces/6",
"/rest/v1/system/interfaces/7",
"/rest/v1/system/interfaces/8",
"/rest/v1/system/interfaces/9",
"/rest/v1/system/interfaces/10" ]
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

##### Valid range for array type

1. Change the "interfaces" value to:
```
"interfaces": ["/rest/v1/system/interfaces/1"]
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 200 OK.

##### Allowed data values validation


###### Invalid data value

1. Change the "vlan_mode" value to:
```
"vlan_mode": "invalid_value"
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 400 BAD REQUEST.

###### Valid data value

1. Change the "vlan_mode" value to:
```
"vlan_mode": "access"
```
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is 200 OK.

##### Missing attribute validation

1. Execute a PUT request with /rest/v1/system/ports/Port1 and without the "vlan_mode" attribute.
2. Verify that the HTTP response is 400 BAD REQUEST.
3. Execute a PUT request over /rest/v1/system/ports/Port1 with all the attributes.
4. Confirm that the HTTP response is 200 OK.

##### Unknown attribute validation

1.  Execute a PUT request with /rest/v1/system/ports/Port1 and with an unknown attribute:
```
"unknown_attribute": "unknown_value"
```
2. Verify that the HTTP response is 400 BAD REQUEST.
3. Execute a PUT request with /rest/v1/system/ports/Port1 and with all allowed attributes.
4. Verify that the HTTP response is 200 OK.

##### Malformed json validation

1. Execute a PUT request with /rest/v1/system/ports/Port1 and with a semi-colon at the end of the json data.
2. Verify that the HTTP response is 400 BAD REQUEST.
3. Execute a PUT request with /rest/v1/system/ports/Port1 and without the semi-colon at the end of the json data.
4. Verify that the HTTP response is 200 OK.

### Test result criteria
#### Test pass criteria

The test is passing for "updating a port" when the following results occur:

- The HTTP response is 200 OK.
- The HTTP response is 200 OK when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is the same as that of the retrieved port.

The test is passing for "updating a port using If-Match" when the following results occur:
- The HTTP response is 200 OK.
- The HTTP response is 200 OK when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is the same as that of the retrieved port.

The test is passing for "updating a port using If-Match and * as etag" when the following results occur:
- The HTTP response is 200 OK.
- The HTTP response is 200 OK when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is the same as that of the retrieved port.

The test is passing for "updating a port using If-Match and a change already applied" when the The HTTP response is 200 OK.

The test is passing for "updating a port using If-Match and a not matching etag" when the The HTTP response is 412 PRECONDITION FAILED

The test is passing for "updating a port with the same name as another port" when the HTTP response is 400 BAD REQUEST.

The test is passing for "updating a port with a valid string type" when the HTTP response is 200 OK.

The test is passing for "updating a port with an invalid string type" when the HTTP response is 400 BAD REQUEST.

The test is passing for "updating a port with a valid integer type" when the HTTP response is 200 OK.

The test is passing for "updating a port with an invalid array type" when the HTTP response is 400 BAD REQUEST.

The test is passing for "updating a port with a valid array type" when the HTTP response is 200 OK.

The test is passing for "updating a port with an invalid value on an attribute" when the HTTP response is 400 BAD REQUEST.

The test is passing for "updating a port with a valid value on an attribute" when the HTTP response is 200 OK.

The test is passing for "updating a port with a missing attribute" when the HTTP response is 400 BAD REQUEST.

The test is passing for "updating a port with with all the attributes" when the HTTP response is 200 OK.

The test is passing for "updating a port with an unknown attribute" when the HTTP response is 400 BAD REQUEST.

The test is passing for "updating a port with all the allowed attributes" when the HTTP response is 200 OK.

The test is passing for "updating a port with malformed json data" when the HTTP response is 400 BAD REQUEST.

The test is passing for "updating a port with well-formed json data" when the HTTP response is 200 OK.

#### Test fail criteria

The test is failing for "updating a port" when the following occurs:

- The HTTP response is not equal to 200 OK.
- The HTTP response is not equal to 200 OK when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is not the same as the data on the retrieved port.

The test is failing for "updating a port using If-Match" when the following results occur:
- The HTTP response is not equal to 200 OK.
- The HTTP response is not equal to 200 OK when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is not the same as that of the retrieved port.

The test is failing for "updating a port using If-Match and * as etag" when the following results occur:
- The HTTP response is 200 OK.
- The HTTP response is 200 OK when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is the same as that of the retrieved port.

The test is failing for "updating a port using If-Match and a change already applied" when the The HTTP response is not equal to 204 NOT CONTENT.

The test is failing for "updating a port using If-Match and a not matching etag" when the The HTTP response is not equal to 412 PRECONDITION FAILED

The test is failing for "updating a port with the same name as another port" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "updating a port with a valid string type" when the HTTP response is not equal to 200 OK.

The test is failing for "updating a port with an invalid string type" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "updating a port with a valid integer type" when the HTTP response is not equal to 200 OK.

The test is failing for "updating a port with an invalid array type" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "updating a port with a valid array type" when the HTTP response is not equal to 200 OK.

The test is failing for "updating a port with an invalid value on an attribute" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "updating a port with a valid value on an attribute" when the HTTP response is not equal to 200 OK.

The test is failing for "updating a port with a missing attribute" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "updating a port with an unknown attribute" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "updating a port with an unknown attribute" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "updating a port with all the allowed attributes" when the HTTP response is not equal to 200 OK.

The test is failing for "updating a port with malformed json data" when the HTTP response is not equal to 400 BAD REQUEST.

The test is failing for "updating a port with well-formed json data" when the HTTP response is not equal to 200 OK.


## Delete a port

### Objective

This test case verifies that an existing port has been deleted.

### Requirements

Period after exist.

### Setup
#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test setup

** Switch 1 ** with a port named Port1 and the following configuration data:

```
{
"configuration": {
"name": "Port1",
"interfaces": ["/rest/v1/system/interfaces/1"],
"trunks": [413],
"ip4_address_secondary": ["192.168.0.1"],
"lacp": "active",
"bond_mode": "l2-src-dst-hash",
"tag": 654,
"vlan_mode": "trunk",
"ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
"external_ids": {"extid1key": "extid1value"},
"bond_options": {},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {},
"ip4_address": "192.168.0.1",
"admin": "up"
}
}
```

### Description

1. Execute a  DELETE request on  /rest/v1/system/ports/Port1 and verify that the HTTP response is 204 NOT CONTENT.
2. Execute a GET request on /rest/v1/system/ports and verify that the port is being deleted from the port list.
3. Execute a GET request on /rest/v1/ports/system/Port1 and verify that the HTTP response is 404 NOT FOUND.
4. Execute a DELETE request on /rest/v1/system/ports/Port2 and ensure that the  HTTP response is 404 NOT FOUND.
5. Execute a DELETE request on  /rest/v1/system/ports/Port1 using Conditional request If-Match and verify HTTP response is 412 PRECONDITION_FAILED and 204 NOT_CONTENT

### Test result criteria

#### Test pass criteria

The test is passing for "deleting an existing port" when the following occurs:

- The HTTP response is 204 NOT CONTENT.
- There is no URI "/rest/v1/system/ports/Port1" in the port list that is returned from the /rest/v1/system/ports URI.
- When doing a GET request on "/rest/v1/system/ports/Port1", the HTTP response is 404 NOT FOUND.
- The HTTP response is 412 PRECONDITION FAILED if Conditional request If-Match provided entity tag does not match the Port entity-tag
- The HTTP response is 204 NOT CONTENT if Conditional request If-Match provided entity tag matches the Port entity-tag
- There is no URI "/rest/v1/system/ports/Port1" in the port list that is returned from the /rest/v1/system/ports URI.
- When doing a GET request on "/rest/v1/system/ports/Port1", the HTTP response is 404 NOT FOUND.
The test case is passing for "deleting a non-existent" port when the HTTP response is 404 NOT FOUND 1284.

#### Test fail criteria

The test is passing for "deleting an existing port" when the following occurs:

- The HTTP response is not equal to 204 NOT CONTENT.
- When performing a GET request on "/rest/v1/system/ports", "Port1" is displayed in the ports URI list.
-The HTTP response is not equal to 404 NOT FOUND when doing a GET request on "/rest/v1/system/ports/Port1".

The test case is failing for "deleting a non-existent port" when the HTTP response is not equal to 404 NOT FOUND.


## Query interface using recursive GET

### Objective
The test case verifies queries for:

- All interfaces with depth equals zero
- All interfaces with no depth parameter
- A specific interface with depth equals one
- A specific interface with depth equals two
- A specific interface with negative depth value
- A specific interface with string depth value
- An interface with specific URI with depth equals one
- An interface with specific URI with depth equals two
- An interface with specific URI with negative depth value
- An interface with specific URI with string depth value
- An interface with specific URI with depth equals zero
- An interface with specific URI with no depth parameter

###  Requirements

- OpenSwitch
- Ubuntu Workstation

### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test setup

** Switch 1 ** has an interface with the name 50-1 and with the following configuration data:

```
{
"configuration": {
"other_config": {},
"name": "50-1",
"split_parent": ["/rest/v1/system/interfaces/50"],
"options": {},
"split_children": [],
"external_ids": {},
"type": "system",
"user_config": {}
}
}
```

### Description
The test case validates the recursivity through the standard REST API GET method.

1. Verify if returns a list of interface URIs by using depth equals zero.

 - a. Execute the GET request over /rest/v1/system/interfaces?depth=0.
 - b. Verify if the HTTP response is 200 OK.
 - c. Confirm that the returned interface list has at least one element.
 - d. Ensure that URI /rest/v1/system/interfaces/50 is in the response data.

2. Verify if returns a list of interface URIs by not using depth parameter.

 - a. Execute the GET request over /rest/v1/system/interfaces
 - b. Verify if the HTTP response is 200 OK.
 - c. Confirm that the returned interface list has at least one element.
 - d. Ensure that URI /rest/v1/system/interfaces/50 is in the response data.

3. Verify if returns an interface and first level data.

 - a. Execute the GET request over /rest/v1/system/interfaces?depth=1;name=50-1
 - b. Verify if the HTTP response is 200 OK.
 - c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
 - d. Ensure that inner data has the URI /rest/v1/system/interfaces/50 in the response data.

4. Verify if returns an interface and second level data.

 - a. Execute the GET request over /rest/v1/system/interfaces?depth=2;name=50-1
 - b. Verify if the HTTP response is 200 OK.
 - c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
 - d. Validate the second level depth returned interface object has Configuration, Statistics and Status keys present.
 - e. Ensure that second level of depth inner data has the URIs /rest/v1/system/interfaces/50-{1-4} in the response data.

5. Verify if response has a BAD_REQUEST status code by using a negative depth value.

 - a. Execute the GET request over /rest/v1/system/interfaces?depth=-1
 - b. Verify if the HTTP response is 400 BAD_REQUEST.

6. Verify if response has a BAD_REQUEST status code by using a string depth value.

 - a. Execute the GET request over /rest/v1/system/interfaces?depth=a
 - b. Verify if the HTTP response is 400 BAD_REQUEST.

7. Verify if returns an interface with specific URI and data in first level of depth.

 - a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=1
 - b. Verify if the HTTP response is 200 OK.
 - c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
 - d. Ensure that inner data has the URI /rest/v1/system/interfaces/50 in the response data.

8. Verify if returns an interface with specific URI and data in second level of depth.

 - a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=2
 - b. Verify if the HTTP response is 200 OK.
 - c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
 - d. Validate the second level depth returned interface object has Configuration, Statistics and Status keys present.
 - e. Ensure that second level of depth inner data has the URIs /rest/v1/system/interfaces/50-{1-4} in the response data.

9. Verify if returns a BAD_REQUEST status code by using a negative depth value with an specific URI.

 - a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=-1
 - b. Verify if the HTTP response is 400 BAD_REQUEST.

10. Verify if returns a BAD_REQUEST status code by using a string depth value with an specific URI.

 - a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=a
 - b. Verify if the HTTP response is 400 BAD_REQUEST.

11. Verify if returns an interface with specific URI by using depth equals zero.

 - a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=0
 - b. Verify if the HTTP response is 200 OK.
 - c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
 - d. Ensure that inner data has the URI /rest/v1/system/interfaces/50 in the response data.

12. Verify if returns an interface with specific URI by not using depth parameter.

 - a. Execute the GET request over /rest/v1/system/interfaces/50-1
 - b. Verify if the HTTP response is 200 OK.
 - c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
 - d. Ensure that inner data has the URI /rest/v1/system/interfaces/50 in the response data.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying an interface with the specified correct parameters in each step:
      - A 200 OK HTTP response.
      - The correct data is returned.
      - The data for the first and second level of depth is as expected according to the parameters.

- Querying an interface list with the specified correct parameters in each step:
      - A 200 OK HTTP response.
      - The data is in the interface list returned as expected.

- Querying an interface list with the specified incorrect parameters, such as negative depth or invalid character such a string, results in a BAD_REQUEST.

- Querying an interface with the specified name and depth parameter equals zero returns a 400 BAD_REQUEST

#### Test fail criteria

This test fails when:

- Querying an interface with the specified correct parameters in each step:
      - A 200 OK HTTP response is not received.
      - The incorrect data is returned.
      - The data for the first and second level of depth is not as expected according to the parameters.

- Querying an interface list with the specified correct parameters in each step:
      - A 200 OK HTTP response is not received.
      - The data is not in the interface list returned.

- Querying an interface list with the specified incorrect parameters, such as negative depth or invalid character such a string, results in anything other than BAD_REQUEST.

- Querying an interface with the specified name and depth parameter equals zero returns anything other than BAD_REQUEST


## Query port with pagination

### Objective
The test case verifies:

1. Query all ports with no pagination offset set
2. Query all ports with no pagination limit set
3. Query all ports with no pagination offset or limit set
4. Query all ports with negative pagination offset set
5. Query all ports with negative pagination limit set
6. Query all ports with pagination offset set greater than data set's size
7. Query all ports with pagination offset + limit greater than data set's size
8. Query specific a port with only pagination offset set
9. Query specific a port with only pagination limit set
10. Query specific a port with both pagination offset and limit set
11. Query first 10 ports using pagination indexes
11. Query last 10 ports using pagination indexes


###  Requirements

Period after exist
Depth is set to 1 in all queries
Port list is sorted by name

### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test setup

** Switch 1 ** has 100 ports (plus the default port named bridge_normal) with the name in the format PortN where N is a number between 0 and 99, each port has the following configuration data:

```
{
    "configuration": {
        "name": "PortN",
        "interfaces": ["/rest/v1/system/interfaces/1"],
        "trunks": [413],
        "ip4_address_secondary": ["192.168.1.1"],
        "lacp": "active",
        "bond_mode": "l2-src-dst-hash",
        "tag": 654,
        "vlan_mode": "trunk",
        "ip6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "external_ids": {"extid1key": "extid1value"},
        "bond_options": {},
        "mac": "01:23:45:67:89:ab",
        "other_config": {"cfg-1key": "cfg1val"},
        "bond_active_slave": "null",
        "ip6_address_secondary": ["01:23:45:67:89:ab"],
        "vlan_options": {},
        "ip4_address": "192.168.0.1",
        "admin": "up"
    },
    "referenced_by": [{"uri": "/rest/v1/system/bridges/bridge_normal"}]
}

```

### Description

1. Query all ports with no pagination offset set

- a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;limit=5"
- b. Verify if the HTTP response is 200 OK.
- c. Confirm that the returned port list has exactly 5 elements
- d. Ensure the first port in the list is 'bridge_normal', which means offset defaulted to 0

2. Query all ports with no pagination limit set

- a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=91"
- b. Verify if the HTTP response is 200 OK.
- c. Confirm that the returned port list has exactly 10 elements
- d. Ensure the first port in the list is 'Port90' and the last one is 'Port99, which means limit defaulted to the remainder size

3. Query all ports with no pagination offset or limit set

- a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name"
- b. Verify if the HTTP response is 200 OK.
- c. Confirm that the returned port list has exactly 101 elements

4. Query all ports with negative pagination offset set

- a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=-1;limit=10"
- b. Verify if the HTTP response is 400 BAD_REQUEST.

5. Query all ports with negative pagination limit set

- a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=5;limit=-1"
- b. Verify if the HTTP response is 400 BAD_REQUEST.

6. Query all ports with pagination offset set greater than data set's size

- a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=200"
- b. Verify if the HTTP response is 400 BAD_REQUEST.

7. Query all ports with pagination offset + limit greater than data set's size

- a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=91;limit=20"
- b. Verify if the HTTP response is 200 OK.
- c. Confirm that the returned port list has exactly 10 elements
- d. Ensure the first port in the list is 'Port90' and the last one is 'Port99, which means limit defaulted to the remainder size

8. Query specific a port with only pagination offset set

- a. Execute a GET request over /rest/v1/system/ports/bridge_normal with the following parameters: "?depth=1;offset=5"
- b. Verify if the HTTP response is 400 BAD_REQUEST.

9. Query specific a port with only pagination limit set

- a. Execute a GET request over /rest/v1/system/ports/bridge_normal with the following parameters: "?depth=1;limit=10"
- b. Verify if the HTTP response is 400 BAD_REQUEST.

10. Query specific a port with both pagination offset and limit set

- a. Execute a GET request over /rest/v1/system/ports/bridge_normal with the following parameters: "?depth=1;offset=0;limit=10"
- b. Verify if the HTTP response is 400 BAD_REQUEST.

11. Query first 10 ports using pagination indexes

- a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=0;limit=10"
- b. Verify if the HTTP response is 200 OK.
- c. Confirm that the returned port list has exactly 10 elements
- d. Ensure the first port in the list is 'bridge_normal' and the last one is 'Port16'

11. Query last 10 ports using pagination indexes

- a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=91;limit=10"
- b. Verify if the HTTP response is 200 OK.
- c. Confirm that the returned port list has exactly 10 elements
- d. Ensure the first port in the list is 'Port90' and the last one is 'Port99'

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying a port list with the specified correct parameters in each step:
      - A 200 OK HTTP response.
      - The correct number of ports is returned.
      - The first and last ports in the list is as expected according to the parameters.

- Querying a port list with the specified incorrect parameters, such as negative indexes or out of range indexes, results in a BAD_REQUEST.

- Querying bridge_normal with pagination parameters returns a 400 BAD_REQUEST

#### Test fail criteria

This test fails when:

- Querying a port list with the specified correct parameters in each step:
      - A 200 OK HTTP response is not received.
      - An incorrect number of ports is returned.
      - The first and last ports in the list are not as expected according to the parameters.

- Querying a port list with the specified incorrect parameters, such as negative indexes or out of range indexes, results in anything other than BAD_REQUEST.

- Querying bridge_normal with pagination parameters returns anything other than BAD_REQUEST


## Sort ports by field

### Objective

This test case verifies if the port list retrieved is sorted by a field.

### Requirements

Period after exist
Depth is set to 1 in all queries

### Setup
#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test setup

** Switch 1 ** with 10 ports with the following configuration data:
Where index is a number between 1 and 10.
```
{
    "configuration": {
        "name": "Port-(index)",
        "interfaces": ["/rest/v1/system/interfaces/1"],
        "trunks": [413],
        "ip4_address_secondary": ["192.168.1.{index}"],
        "lacp": ["active"],
        "bond_mode": ["l2-src-dst-hash"],
        "tag": 654,
        "vlan_mode": "trunk",
        "ip6_address": ["2001:0db8:85a3:0000:0000:8a2e:0370:{index with format 0000}"],
        "external_ids": {"extid1key": "extid1value"},
        "bond_options": {},
        "mac": ["01:23:45:67:89:(index_hex)"],
        "other_config": {"cfg-1key": "cfg1val"},
        "bond_active_slave": "null",
        "ip6_address_secondary": \
            ["2001:0db8:85a3:0000:0000:8a2e:0371:{index with format 0000}"],
        "vlan_options": {},
        "ip4_address": "192.168.0.{index}",
        "admin": "up"
    },
    "referenced_by": [{"uri": "/rest/v1/system/bridges/bridge_normal"}]
}
```

### Description

Allowed sort fields:
```
name
interfaces
trunks
ip4_address
ip4_address_secondary
lacp
bond_mode
tag
vlan_mode
mac
bond_active_slave
ip6_address
ip6_address_secondary
admin
```

Sort by allowed sort field (ascending mode)

For each allowed sort field exececute the following steps:
1. Execute a GET request on /rest/v1/system/ports?depth=1;sort={field_name} and verify that response is 200 OK.
2. Verify if the result is being ordered by the provided field name

Sort by allowed sort field (descending mode)

For each allowed sort field exececute the following steps:
1. Execute a GET request on /rest/v1/system/ports?depth=1;sort=-{field_name} and verify that response is 200 OK.
2. Verify if the result is being ordered by the provided field name

### Test result criteria

#### Test pass criteria

This test passes by meeting the following criteria:

- The HTTP response is 200 OK.
- The response has 10 ports
- The ports are sorted ascending/descending by the field name

#### Test fail criteria

This test fails when:

- The HTTP response is not equal to 200 OK.
- The response doesn't have 10 ports
- The port aren't sorted ascending/descending by the field name


## Sort ports by field combination

### Objective

This test case verifies if the port list retrieved is sorted ascending/descending by a combination of fields.

### Requirements

Period after exist
Depth is set to 1 in all queries

### Setup
#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

#### Test setup

** Switch 1 ** with 10 ports with the following configuration data:
Where index is a number between 1 and 10.
```
{
    "configuration": {
        "name": "Port-(index)",
        "interfaces": ["/rest/v1/system/interfaces/1"],
        "trunks": [413],
        "ip4_address_secondary": ["192.168.1.{index}"],
        "lacp": ["active"],
        "bond_mode": ["l2-src-dst-hash"],
        "tag": 654,
        "vlan_mode": "trunk",
        "ip6_address": ["2001:0db8:85a3:0000:0000:8a2e:0370:{index with format 0000}"],
        "external_ids": {"extid1key": "extid1value"},
        "bond_options": {},
        "mac": ["01:23:45:67:89:(index_hex)"],
        "other_config": {"cfg-1key": "cfg1val"},
        "bond_active_slave": "null",
        "ip6_address_secondary": \
            ["2001:0db8:85a3:0000:0000:8a2e:0371:{index with format 0000}"],
        "vlan_options": {},
        "ip4_address": "192.168.0.{index}",
        "admin": "up"
    },
    "referenced_by": [{"uri": "/rest/v1/system/bridges/bridge_normal"}]
}
```
The admin field of each port has the following values:
```
Port1: 	 admin = "up"
Port2: 	 admin = "down"
Port3: 	 admin = "up"
Port4: 	 admin = "down"
Port5: 	 admin = "up"
Port6: 	 admin = "down"
Port7: 	 admin = "up"
Port8: 	 admin = "down"
Port9: 	 admin = "up"
Port10:	 admin = "down"
```

### Description
Sort by admin and name (Ascending mode)

1. Execute a GET request on /rest/v1/system/ports?depth=1;sort=admin,name and verify that response is 200 OK.
2. Verify if the result is being ordered by the provided fields. First by admin and the by name.

Sort by admin and name (Descending mode)

1. Execute a GET request on /rest/v1/system/ports?depth=1;sort=-admin,name and verify that response is 200 OK.
2. Verify if the result is being ordered by the provided fields. First by admin and the by name.

### Test result criteria

#### Test pass criteria

This test passes by meeting the following criteria:

- The HTTP response is 200 OK.
- The response has 10 ports
- The result is sorted ascending/descending by the combination of fields

Expected result when sort mode is ascending:
```
admin = down, name = Port10
admin = down, name = Port2
admin = down, name = Port4
admin = down, name = Port6
admin = down, name = Port8
admin = up, name = Port1
admin = up, name = Port3
admin = up, name = Port5
admin = up, name = Port7
admin = up, name = Port9
```

Expected result when sort mode is descending:
```
admin = up, name = Port9
admin = up, name = Port7
admin = up, name = Port5
admin = up, name = Port3
admin = up, name = Port1
admin = down, name = Port8
admin = down, name = Port6
admin = down, name = Port4
admin = down, name = Port2
admin = down, name = Port10
```

#### Test fail criteria

The test fails when:

- The HTTP response is not 200 OK.
- The response doesn't have 10 ports
- The result is not sorted ascending/descending by the combination of fields
