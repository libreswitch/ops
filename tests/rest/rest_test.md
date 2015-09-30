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
"bond_options": {"key1": "value1"},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {"opt1key": "opt2val"},
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
"bond_options": {"key1": "value1"},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {"opt1key": "opt2val"},
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
"bond_options": {"key1": "value1"},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {"opt1key": "opt2val"},
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
"bond_options": {"key2": "value2"},
"mac": "01:23:45:63:90:ab",
"other_config": {"cfg-2key": "cfg2val"},
"bond_active_slave": "slave1",
"ip6_address_secondary": ["2001:0db8:85a3:0000:0000:8a2e:0370:7224"],
"vlan_options": {"opt1key": "opt3val"},
"ip4_address": "192.168.0.2",
"admin": "up"
},
"referenced_by": [{"uri":"/rest/v1/system/bridges/bridge_normal"}]
}
```

2. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is 200 OK.
3. confirm that the configuration response data from Step 2 is the same as the configuration data from Step 1.

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

##### Valid range for arry type

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
"bond_options": {"key1": "value1"},
"mac": "01:23:45:67:89:ab",
"other_config": {"cfg-1key": "cfg1val"},
"bond_active_slave": "null",
"ip6_address_secondary": ["01:23:45:67:89:ab"],
"vlan_options": {"opt1key": "opt2val"},
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

### Test result criteria

#### Test pass criteria

The test is passing for "deleting an existing port" when the following occurs:

- The HTTP response is 204 NOT CONTENT.
- There is no URI "/rest/v1/system/ports/Port1" in the port list that is returned from the /rest/v1/system/ports URI.
- When doing a GET request on "/rest/v1/system/ports/Port1", the HTTP response is 404 NOT FOUND.

The test case is passing for "deleting a non-existent" port when the HTTP response is 404 NOT FOUND 1284.

#### Test fail criteria

The test is passing for "deleting an existing port" when the following occurs:

- The HTTP response is not equal to 204 NOT CONTENT.
- When performing a GET request on "/rest/v1/system/ports", "Port1" is displayed in the ports URI list.
-The HTTP response is not equal to 404 NOT FOUND when doing a GET request on "/rest/v1/system/ports/Port1".

The test case is failing for "deleting a non-existent port" when the HTTP response is not equal to 404 NOT FOUND.
