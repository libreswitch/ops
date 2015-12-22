REST API Test Cases
===================

## Contents
- [REST API put method for system](#rest-api-put-method-for-system)
- [REST API get method for subsystems](#rest-api-get-method-for-subsystems)
- [REST API get method for an interface](#rest-api-get-method-for-an-interface)
- [REST API get method for VRFS](#rest-api-get-method-for-vrfs)
- [REST API get method for route maps](#rest-api-get-method-for-route-maps)
- [REST API get method for interfaces](#rest-api-get-method-for-interfaces)
- [REST API put method with invalid data for URLs](#rest-api-put-method-with-invalid-data-for-urls)
- [REST API login authentication](#rest-api-login-authentication)
- [REST API startup config verify](#rest-api-startup-config-verify)
- [REST API get method for users](#rest-api-get-method-for-users)
- [REST API post method for users](#rest-api-post-method-for-users)
- [REST API delete method for users](#rest-api-delete-method-for-users)
- [REST API put method for users](#rest-api-put-method-for-users)
- [REST API get method for ports](#rest-api-get-method-for-ports)
- [REST API post method for ports](#rest-api-post-method-for-ports)
- [REST API put method for ports](#rest-api-put-method-for-ports)
- [REST API delete method for ports](#rest-api-delete-method-for-ports)
- [REST API get method with recursion support for interfaces](#rest-api-get-method-with-recursion-for-interfaces)
- [REST API get method with pagination for ports](#rest-api-get-method-with-pagination-for-ports)
- [REST API get method and sort by field for ports](#rest-api-get-method-and-sort-by-field-for-ports)
- [REST API get method and sort by field combination for ports](#rest-api-get-method-and-sort-by-field-combination-for-ports)
- [REST API VLANs Resource test cases](#rest-api-vlans-resource-test-cases)
  - [Query Bridge Normal](#query-bridge-normal)
  - [Query existent VLANs](#query-existent-vlans)
  - [Query existent VLAN by name](#query-existent-vlan-by-name)
  - [Query non-existent VLAN by name](#query-non-existent-vlan-by-name)
  - [Create VLAN](#create-vlan)
  - [Create VLAN using an invalid name](#create-vlan-using-an-invalid-name)
  - [Create VLAN using an invalid ID](#create-vlan-using-an-invalid-id)
  - [Create VLAN using an invalid Description](#create-vlan-using-an-invalid-description)
  - [Create VLAN using an invalid Admin](#create-vlan-using-an-invalid-admin)
  - [Create VLAN using an invalid other_config](#create-vlan-using-an-invalid-otherconfig)
  - [Create VLAN using an invalid external_ids](#create-vlan-using-an-invalid-externalids)
  - [Create VLAN with missing fields](#create-vlan-with-missing-fields)
  - [Create a duplicated VLAN](#create-a-duplicated-vlan)
  - [Update VLAN name](#update-vlan-name)
  - [Update VLAN using an invalid name](#update-vlan-using-an-invalid-name)
  - [Update VLAN using an invalid ID](#update-vlan-using-an-invalid-id)
  - [Update VLAN using an invalid Description](#update-vlan-using-an-invalid-description)
  - [Update VLAN using an invalid Admin](#update-vlan-using-an-invalid-admin)
  - [Update VLAN using an invalid other_config](#update-vlan-using-an-invalid-otherconfig)
  - [Update VLAN using an invalid external_ids](#update-vlan-using-an-invalid-externalids)
  - [Update VLAN with missing fields](#update-vlan-with-missing-fields)
  - [Delete non-existent VLAN](#delete-non-existent-vlan)
  - [Query VLANs filtered by name](#query-vlans-filtered-by-name)
  - [Query VLANs filtered by ID](#query-vlans-filtered-by-id)
  - [Query VLANs filtered by Description](#query-vlans-filtered-by-description)
  - [Query VLANs filtered by Admin](#query-vlans-filtered-by-admin)
- [Declarative configuration schema validations](#declarative-configuration-schema-validations)
- [Custom validators](#custom-validators)

## REST API put method for system
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

**URL "/rest/v1/system"**

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure an IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Configure the system through the Standard REST API PUT method for the URI "/rest/v1/system".
5. Validate the system configuration with the HTTP return code for the URI "/rest/v1/system".
6. Execute the Standard REST API GET method for URI "/rest/v1/system".
7. Validate the GET method HTTP return code for "/rest/v1/system" and its respective values.

### Test result criteria
#### Test pass criteria
- The first test passes (steps 4 and 5), if the standard REST API PUT method returns HTTP code `200 OK` for the URI "/ rest/v1/system".
- The second test passes (steps 6 and 7), if the standard REST API GET method returns HTTP code `200 OK` for the URI "/rest/v1/system" and the returned data is identical to the date used for the PUT.

#### Test fail criteria
- The first test fails if the standard REST API PUT method does not return HTTP code `200 OK` for the URI "/rest/v1/system".
- The second test fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI "/rest/v1/system" or the returned data is not identical to the data used for PUT.

## REST API get method for subsystems
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

**URL "/rest/v1/system/subsystems"**

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Execute the Standard REST API GET method for URI "/rest/v1/system/subsystems".
5. Validate the GET method HTTP return code for "/rest/v1/system/subsystems" and its respective values.

### Test result criteria
#### Test pass criteria
The test passes if the standard REST API GET method returns HTTP code `200 OK` for the URI "/rest/v1/system/subsystems" and the returned data is identical.

#### Test fail criteria
The test case is fails if the standard REST API GET method does not return the HTTP code `200 OK` for the URI "/rest/v1/system/subsystems".

## REST API get method for an interface
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

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.

##### Test 1
1. Configure the "/rest/v1/system/interfaces/{id}" through Standard REST API PUT method.
2. Validate the "/rest/v1/system/interfaces/{id}" configuration with the HTTP return code.

##### Test 2
1. Execute the Standard REST API GET method for URI "/rest/v1/system/interfaces/{id}".
2. Validate the GET Method HTTP return code for "/rest/v1/system/interfaces/{id}" and its respective values.

##### Test 3
1. Execute Standard REST API DELETE method for URI "/rest/v1/system/interfaces/{id}".
2. Validate the DELETE method HTTP return code for "/rest/v1/system/interfaces/{id}".

##### Test 4
1. Execute Standard REST API GET Method for URI "/rest/v1/system/interfaces/{id}".
2. Validate the GET method HTTP return code for "/rest/v1/system/interfaces/{id}".

### Test result criteria
#### Test pass criteria
- The first test passes if the standard REST API PUT method returns HTTP code `200 OK` for the URI "/rest/v1/system/interfaces/{id}".
- The second test passes if the standard REST API GET method returns HTTP code `200 OK` for the URI "/rest/v1/system/interfaces/{id}" and the returned data is identical to the date used for the PUT.
- The third test passes if the standard REST API DELETE method returns HTTP code `204 NO CONTENT` for the URI "/rest/v1/system/interfaces/{id}".
- The fourth test passes, if the standard REST API GET method does not return HTTP code `200 OK` for the URI "/rest/v1/system/interfaces/{id}".

#### Test fail criteria
- The first test fails if the standard REST API PUT method does not return HTTP code `200 OK` for the URI "/rest/v1/system/interfaces/{id}".
- The second test fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI "/rest/v1/system/interfaces/{id}" or the returned data is not identical to the data used for PUT.
- The third test fails if the standard REST API DELETE method does not return HTTP code `204 NO CONTENT` for the URI "/rest/v1/system/interfaces/{id}".
- The fourth test fails if the standard REST API GET method returns HTTP code `200 OK` for the URI "/rest/v1/system/interfaces/{id}".

## REST API get method for VRFS
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

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Execute the Standard REST API GET Method for URI "/rest/v1/system/vrfs".
5. Validate the GET Method HTTP return code for "/rest/v1/system/vrfs" and its respective values.

### Test result criteria
#### Test pass criteria
The test case is passes if the standard REST API GET method returns HTTP code `200 OK` for the URI "/rest/v1/system/vrfs" and if the returned data is identical.

#### Test fail criteria
The test case fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI "/rest/v1/system/vrfs".

## REST API get method for route maps
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

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Execute the Standard REST API GET Method for URI "/rest/v1/system/route_maps/{id}".
5. Validate the GET method HTTP return code for "/rest/v1/system/route_maps/{id}" and its respective values.

### Test result criteria
#### Test pass criteria
This test case passes if the standard REST API GET method returns HTTP code `200 OK` for the URI "/rest/v1/system/route_maps/{id}" and the returned data is identical.

#### Test fail criteria
This test case fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI "/rest/v1/system/route_maps/{id}".

## REST API get method for interfaces
### Objective
The objective of the test case is to validate the "/rest/v1/system/interfaces" through the standard REST API GET method.

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
The test case validates the "/rest/v1/system/interfaces" through the standard REST API GET method.

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Execute the Standard REST API GET Method for URI "/rest/v1/system/interfaces".
5. Validate the GET method HTTP return code for "/rest/v1/system/interfaces" and its respective values.

### Test result criteria
#### Test pass criteria
The test case passes if the standard REST API GET method returns HTTP code `200 OK` for the URI "/rest/v1/system/interfaces" and the returned data is identical.

#### Test fail criteria
The test case is fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI "/rest/v1/system/interfaces".

## REST API put method with invalid data for URLs
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

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Configure the standard REST API PUT method with invalid data for URIs.
5. Validate that the standard REST API PUT method fails to configure with invalid data for all URIs.

### Test result criteria
#### Test pass criteria
This test case passes if the standard REST API PUT method with invalid data fails to return HTTP code `200 OK` for the URIs.

#### Test fail criteria
This test case fails if the standard REST API PUT method with invalid data returns HTTP code `200 OK` for the URIs.

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

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.

##### Test 1

1. Execute the Standard REST API POST method for the URI "/login" with valid credentials.
2. Validate the GET Method HTTP return code for the URI "/login".

##### Test 2

1. Execute the Standard REST API POST method for URI "/login" with invalid credentials.
2. Validate that the GET method HTTP failed the return code for URI "/login".

### Test result criteria
#### Test pass criteria
- The first test passes if the standard REST API GET method returns HTTP code `200 OK` for the URI "/login".
- The second test passes if the standard REST API GET method returns HTTP code `401 UNAUTHORIZED` for the URI "/login".

#### Test fail criteria
- The first test fails if the standard REST API GET Method does not return HTTP code `200 OK` for the URI "/login".
- The second test fails if the standard REST API GET Method does not return HTTP `401 UNAUTHORIZED` for the URI "/login".

## REST API startup config verify
### Objective
The objective for the test case is to verify that the REST API startup configuration works.

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
Verify that the REST API startup configuration works.

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Execute Standard REST API PUT method for URI "/rest/v1/system" - 1st test case.
5. Execute Standard REST API GET method for URI "/rest/v1/system" - 2nd test case.

### Test result criteria
#### Test pass criteria
- The first test passes if the standard REST API PUT method returns HTTP code `200 OK` for the URI "/rest/v1/system".
- The second test passes if the standard REST API GET method returns HTTP code `200 OK` for the URI "/rest/v1/system" and the returned data is identical to the data used for the PUT.

#### Test fail criteria
- The first test fails if the standard REST API PUT method does not return HTTP code `200 OK` for the URI "/rest/v1/system".
- The second test fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI "/rest/v1/system" or the returned data is not identical to the data used for PUT.

## REST API get method for users

### Objective
The objective of the test case is to validate the "/rest/v1/system/users" through the standard REST API GET method.

### Requirements
The requirements for this test case are:

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

### Description

The test case validates the "/rest/v1/system/users" through the standard REST API GET method.

1. Verify if the GET method returns a json object with a list of users by creating 100 new users that are part of ovsdb_users group.
    a. Execute the GET request over /rest/v1/system/users.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned user list has the expected data.

2. Verify if the GET method returns a json object with a list of users by creating 11 new users and only 10 are part of ovsdb_users group.
    a. Execute the GET request over /rest/v1/system/users.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned user list has the expected data.

3. Verify if the GET method returns a json object with a list of users by creating 10 new users that are part of ovsdb_users group and have extra arguments in the creation command.
    a. Execute the GET request over /rest/v1/system/users.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned user list has the expected data.

4. Verify if the GET method returns a json object with the default user.
    a. Execute the GET request over /rest/v1/system/users.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned user list has the expected data.


### Test result criteria
#### Test pass criteria

This tests passes by meeting the following criteria:

- A `200 OK` HTTP response.
- The correct data is returned.

#### Test fail criteria

- A `400 BAD REQUEST` HTTP response.
- The incorrect data is returned.

## REST API post method for users

### Objective
The objective of the test is to validate the "/rest/v1/system/users" through the standard REST API POST method.

### Requirements
The requirements for this test case are:

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

### Description
The test case validates the "/rest/v1/system/users" through the standard REST API POST method.

1. Verify that the request passes when trying to create a new user with a valid username and password.
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "test_user",
                "password": "test_password"
            }
        }
        ```

    b. Verify if the HTTP response is `201 CREATED`.
    c. Execute a GET request over /rest/v1/system/users.
    d. Confirm that the user is in the returned user list.

2. Verify that the request passes when trying to create a new user with a 32 characters username:
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "password": "test_password"
            }
        }
        ```

    b. Verify if the HTTP response is `201 CREATED`.
    c. Execute a GET request over /rest/v1/system/users.
    d. Confirm that the user is in the returned user list.

3. Verify that the request fails when trying to create a new user with an empty username:
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "",
                "password": "test_password"
            }
        }
        ```

    b. Verify if the HTTP response is `400 BAD REQUEST`.

4. Verify that the request fails when trying to create a new user with a space as username:
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": " ",
                "password": "test_password"
            }
        }
        ```

    b. Verify if the HTTP response is `400 BAD REQUEST`.

5. Verify that the request fails when trying to create a new user with a username longer than 32 characters:
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "password": "test_password"
            }
        }
        ```

    b. Verify if the HTTP response is `400 BAD REQUEST`.

6. Verify that the request fails when trying to create a new user with a username that contains the following not allowed symbols: #(){}[]?\~/+-*=|^$%.;,:"´
    a. Execute the POST request over /rest/v1/system/users with each of the not allowed symbols
    b. Verify if the HTTP response is `400 BAD REQUEST`.

7. Verify that the request passes when trying to create a new user with a long password
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "test_user",
                "password": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            }
        }
        ```

    b. Verify if the HTTP response is `201 CREATED`.
    c. Execute a GET request over /rest/v1/system/users.
    d. Confirm that the user is in the returned user list.

8. Verify that the request fails when trying to create a new user with a empty username and password
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "",
                "password": ""
            }
        }
        ```

    b. Verify if the HTTP response is `400 BAD REQUEST`.

9. Verify that the request fails when trying to create a new user with a valid username and empty password
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "test_user",
                "password": ""
            }
        }
        ```

    b. Verify if the HTTP response is `400 BAD REQUEST`.

10. Verify that the request fails when trying to create an existent user
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "existent_user",
                "password": "password"
            }
        }
        ```

    b. Execute the POST request over /rest/v1/system/users with the same data that (a):
    c. Verify if the HTTP response is `400 BAD REQUEST`.

11. Verify that the request passes when trying to create two user with the same password and check if hashed password is different in the shadow file.
    a. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "test_user_pass_1",
                "password": "same_password"
            }
        }
        ```

    b. Verify if the HTTP response is `201 CREATED`.
    c. Execute the POST request over /rest/v1/system/users with the following data:

        ```
        {
            "configuration":
            {
                "username": "test_user_pass_2",
                "password": "same_password"
            }
        }
        ```

    d. Verify if the HTTP response is `201 CREATED`.
    e. Execute a GET request over /rest/v1/system/users.
    f. Confirm that the users is in the returned user list.
    g. Read the /etc/shadow file and the users hashed password.
    h. Verify if both hashed password are different.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- The following message is displayed when trying to create a valid user:

    A `201 CREATED` HTTP response.

- The following error message is displayed when trying to create a user with and invalid username (empty, a space, invalid characters, more than 32 characters)

    A `400 BAD REQUEST` HTTP response.

- The following message is displayed when trying to create a user with a long password.

    A `201 CREATED` HTTP response.

- The following error message is displayed when trying to create a user with an empty username and password

    A `400 BAD REQUEST` HTTP response.

- The following error message is displayed when trying to create a user with a valid username and empty password

    A `400 BAD REQUEST` HTTP response.

- The following error message is displayed when trying to create an existent user

    A `400 BAD REQUEST` HTTP response.

- Creating two users with the differents usernames and same password, both users have the different hashed passwords in the /etc/shadow file.

#### Test fail criteria

This test fails when:

- The following message or anything other than `201 CREATED` is displayed when trying to create user with a valid username:

    A `201 CREATED` HTTP response.

- The following error message or anything other than `400 BAD REQUEST` is displayed when trying to create a user with an invalid username (empty, a space, invalid characters, more than 32 characters)

    A `400 BAD REQUEST` HTTP response.

- The following message or anything other than `201 CREATED` is displayed when trying to create user with a long password:

    A `201 CREATED` HTTP response.

- The following error message or anything other than `400 BAD REQUEST` is displayed when trying to create user with an empty username and password:

    A `400 BAD REQUEST` HTTP response.

- The following error message or anything other than `400 BAD REQUEST` is displayed when trying to create user with a valid username and empty password:

    A `400 BAD REQUEST` HTTP response.

- The following error message or anything other than `400 BAD REQUEST` is displayed when trying to create user an existent user:

    A `400 BAD REQUEST` HTTP response.

- Creating two users with the differents usernames and same password, both users have the same hashed passwords in the /etc/shadow file.

## REST API delete method for users

### Objective
The objective of the test case is to validate the "/rest/v1/system/users/{id}" through the standard REST API DELETE method.

### Requirements
The requirements for this test case are:

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

### Description
The test case validates the "/rest/v1/system/users/{id}" through the standard REST API DELETE method.

1. Verify that the request passes when trying to delete a new user who is part of ovsdb_users group and is not logged in.
    a. Execute the DELETE request over /rest/v1/system/users/{id}.
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that the returned user list has the expected data.

2. Verify that the request fails when trying to delete a new user who is part of ovsdb_users group and is logged in.
    a. Execute the DELETE request over /rest/v1/system/users/{id}.
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the returned user list has the expected data.

3. Verify that the request fails when trying to delete the current user and is logged in.
    a. Execute the DELETE request over /rest/v1/system/users/{id}.
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the returned user list has the expected data.

4. Verify that the request fails after trying to delete a nonexistent user.
    a. Execute the DELETE request over /rest/v1/system/users/{id}.
    b. Verify if the HTTP response is `400 BAD REQUEST`.

5. Verify that the request fails after trying to delete a new user who is not part of the ovsdb_users group.
    a. Execute the DELETE request over /rest/v1/system/users/{id}.
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the returned user list has the expected data.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- The following error message is displayed when trying to delete a valid user that is currently not logged:

    A `204 NO CONTENT` HTTP response.

- The following error message is displayed when trying to delete a valid user currently logged in:

    A `400 BAD REQUEST` HTTP response.

- The following error message is displayed when trying to delete a nonexistent user:

    A `400 BAD REQUEST` HTTP response.

- The following error message is displayed when trying to delete a user who is not part of ovsdb_users group:

    A `400 BAD REQUEST` HTTP response.

#### Test fail criteria

This test fails when:

- The following error message or anything other than `204 NO CONTENT` is displayed when trying to delete a valid user currently not logged:

    A `400 BAD REQUEST` HTTP response.

- Deleting a valid user currently logged in, the following error message or anything other than `400 BAD REQUEST`is displayed:

    A `204 NO CONTENT` HTTP response.

- Deleting a nonexistent user anything other than a `400 BAD REQUEST` HTTP response is displayed.

- Deleting a user who is not part of the ovsdb_users group, the following error message or anything other than a `400 BAD REQUEST` HTTP response is displayed:

    A `204 NO CONTENT` HTTP response.

## REST API put method for users

### Objective
The objective of the test case is to validate the "/rest/v1/system/users/{id}" through the standard REST API PUT method.

### Requirements
The requirements for this test case are:

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

**Switch 1** must have a user to test with the following configuration data:

```
{
    "configuration":
    {
        "username": "test_user_0"
        "password": "test"
    }
}
```

### Description
The test case validates the "/rest/v1/system/users/{id}" through the standard REST API PUT method.

1. Verify that the request passes when trying to update the password of a user, who is also part of ovsdb_users group but is not logged in.
    a. Execute the PUT request over /rest/v1/system/users/{id} with the following data:

        ```
        {
            "configuration":
            {
                "password": "test_password"
            }
        }
        ```

    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the user can log in with the new password.

2. Verify that the request fails when trying to update a user with an empty password, and the user is part of the ovsdb_users group.
    a. Execute the PUT request over /rest/v1/system/users/{id} with the following data:

        ```
        {
            "configuration":
            {
                "password": ""
            }
        }
        ```

    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the user can still log in with the current password.

3. Verify that the request fails when trying to update a nonexistent user.
    a. Execute the PUT request over /rest/v1/system/users/{id} with the following data:

        ```
        {
            "configuration":
            {
                "password": "test_password"
            }
        }
        ```

    b. Verify if the HTTP response is `400 BAD REQUEST`.

4. Verify that the request fails after trying to update the password of a user who is not part of the ovsdb_users group.
    a. Execute the PUT request over /rest/v1/system/users/{id} with the following data:

        ```
        {
            "configuration":
            {
                "password": "test_password"
            }
        }
        ```

    b. Verify if the HTTP response is `400 BAD REQUEST`.

5. Verify that the request fails after trying to update the password of a user who is part of the ovsdb_users group and then try to log in with the old password.
    a. Execute the PUT request over /rest/v1/system/users/{id} with the following data:

        ```
        {
            "configuration":
            {
                "password": "test_password"
            }
        }
        ```

    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the user cannot log in with the old password.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- The following message is displayed when trying to update a valid user that has a proper password and is part of ovsb_users group:

    A `200 OK` HTTP response.

- The following error message is displayed when trying to update a valid user that has an incorrect password and is part of ovsb_users group:

    A `400 BAD REQUEST` HTTP response.

- The following error message is displayed when trying to update a nonexistent user:

    A `400 BAD REQUEST` HTTP response.

- The following error message is displayed when trying to update a authorized user that has a valid password but is not part of ovsb_users group:

    A `400 BAD REQUEST` HTTP response.

- The following error message is displayed when trying to log in with the old password instead of the recently updated password:

    A `400 BAD REQUEST` HTTP response.

#### Test fail criteria

This test fails when:

- The following error message is displayed when trying to update an authorized user that has a proper password and is part of ovsb_users group:

    Anything other than  a `200 OK` HTTP response.

- The following message is displayed when trying to update a valid user that has an incorrect password and is a part of ovsb_users group:

    Anything other than  a `400 BAD REQUEST` HTTP response.

- The following message is displayed when trying to update an nonexistent user:

    Anything other than  a `400 BAD REQUEST` HTTP response.

- The following message is displayed when trying to update an authorized user that has a valid password, but is not part of ovsb_users group:

    Anything other than  a `400 BAD REQUEST` HTTP response.

- The following message is displayed when trying to log in with an old password instead of the recently updated password:

    Anything other than  a `400 BAD REQUEST` HTTP response.

REST API ports Resource test cases
==================================

## REST API get method for ports

### Objective
The test case verifies queries for:

- All ports
- A specific port
- A non-existent port

### Requirements

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

**Switch 1** has a port with the name Port1 and with the following configuration data:

```
{
    "configuration":
    {
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
    a. Execute the GET request over /rest/v1/system/ports.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has at least one element.
    d. Ensure that URI /rest/v1/system/ports/Port1 is in the response data.

2. Verify if a specific port exists.
    a. Execute GET request over rest/v1/system/ports/Port1.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm if the response data is not empty.
    d. Ensure that the response data has the keys: "configuration", "status" and "statistics".
    e. Verify if the configuration data is equal to the Port1 configuration data.

3. Verify if a non-existent port exists.
    a. Execute the GET request over rest/v1/system/ports/Port2.
    b. Verify if the HTTP response is `404 NOT FOUND`.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying a port list for:
    - A `200 OK` HTTP response.
    - At least one port in the port list.
    - A URI "rest/v1/system/ports/Port1" in the port list returned from the  rest/v1/system/ports URI.

- Querying Port1 for:
    - An HTTP response of `200 OK` when doing a GET request over "rest/v1/system/ports/Port1".
    - A response data that is not empty.
    - A response data that contains keys: "configuration", "status", and "statistics".
    - Preset port configuration data that is equal to Port1.

- Querying for an HTTP response of `404 NOT FOUND` on a non-existent port.

#### Test fail criteria

This test fails when:

- Querying a post list for:
    - An HTTP response is not equal to `200 OK`.
    - A GET request to "rest/v1/system/ports" and "Port1" is in the Ports URI list.

- Performing a GET request over "rest/v1/system/ports/Port1" and the HTTP response is not equal to `404 NOT FOUND` for Port1.

- Querying for a non-existent port and the HTTP response is not equal to `404 NOT FOUND`.

## REST API post method for ports

### Objective

The test case verifies:

- Creating a port.
- Creating a port with the same name as another port.
- Port data such as ranges, types, allowed values, malformed JSON, and missing attributes.

### Requirements

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

1. Execute a POST request with /rest/v1/system/ports and with the following data and verify if the HTTP response is `201 CREATED`.

    ```
    {
        "configuration":
        {
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

2. Execute a GET request with /rest/v1/system/ports/Port1 and verify if the response is `200 OK`.
3. Verify that the configuration response data from Step 2 is the same as the configuration data from Step 1.

#### Create an existing port
Verify that the HTTP response returns `400 BAD REQUEST` HTTP response when creating a existing port with the name "Port1".

1. Execute a POST request with /rest/v1/system/ports, and with the name "Port1": `"name": "Port1"`.
2. Confirm that the HTTP response is `400 BAD REQUEST`.

#### Data validation

##### Data types validation

###### Invalid string type

1. Set the "ip4_address" value to: `"ip4_address": 192`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid string type

1. Set the "ip4_address" value to: `"ip4_address": "192.168.0.1"`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

###### Invalid integer type

1. Set the "tag" value to: `"tag": "675"`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid integer type

1. Set the "tag" value to: `"tag": 675`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

###### Invalid array type

1. Set the "trunks" value to: `"trunks": "654,675"`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid array type

1. Set the "trunks" value to: `"trunks": [654,675]`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

##### Ranges validation

###### Invalid range for string type

1. Set the "ip4_address" value to: `"ip4_address": "175.167.134.123/248"`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for string type

1. Set the "ip4_address" value to: `"ip4_address": "175.167.134.123/24"`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

###### Invalid range for integer type

1. Set the "tag" value to: `"tag": 4095`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for integer type

1. Set the "tag" value to: `"tag": 675`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

###### Invalid range for array type

1. Change the "interfaces" value to:

    ```
    "interfaces": ["/rest/v1/system/interfaces/1",
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
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for array type

1. Change the "interfaces" value to: `"interfaces": ["/rest/v1/system/interfaces/1"]`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

##### Allowed data values validation


###### Invalid data value

1. Change the "vlan_mode" value to: `"vlan_mode": "invalid_value"`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid data value

1. Change the "vlan_mode" value to: `"vlan_mode": "access"`.
2. Execute a POST request with /rest/v1/system/ports and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

##### Missing attribute validation

1. Execute a POST request with /rest/v1/system/ports and without the "vlan_mode" attribute.
2. Verify that the HTTP Response is `400 BAD REQUEST`.
3. Execute a POST request with /rest/v1/system/ports and with all the attributes.
4. Verify that the HTTP Response is `201 CREATED`.

##### Unknown attribute validation

1. Execute a POST request with /rest/v1/system/ports and with an unknown attribute as follows: `"unknown_attribute": "unknown_value"`.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a POST request with /rest/v1/system/ports and with all allowed attributes.
4. Verify that the HTTP Response is `201 CREATED`.

##### Malformed json validation

1. Execute a POST request with /rest/v1/system/ports and with a semi-colon at the end of the json data.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a POST request with /rest/v1/system/ports and without the semi-colon at the end of the json data.
4. Verify that the HTTP response is `201 CREATED`.


### Test result criteria
#### Test pass criteria

The test is passing for "creating a new port" when the following results occur:

- The HTTP response is `200 OK`.
- The HTTP response is `200 OK` when executing a GET request with /rest/v1/system/ports/Port1.
- When the configuration data posted is the same as the retrieved port.

The test is passing for "creating a port with the same name as another port" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "creating a new port with a valid string type" when the HTTP response is `201 CREATED`.

The test is passing for "creating a new port with a invalid string type" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "creating a new port with a valid integer type" when the HTTP response is `201 CREATED`.

The test is passing for "creating a new port with an invalid array type" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "creating a new port with valid array type" when the HTTP response is `201 CREATED`.

The test is considered passing for "creating a new port with an invalid value on an attribute" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "creating a new port with a valid value on an attribute" when the HTTP response is `201 CREATED`.

The test is passing for "creating a new port with a missing attribute" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "creating a new port with all the attributes" when the HTTP response is `201 CREATED`.

The test is passing for "creating a new port with an unknown attribute" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "creating a new port with all allowed attributes" when the HTTP response is `201 CREATED`.

The test is passing for "creating a new port with malformed json data" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "creating a new port with well-formed json data" when the HTTP response is `201 CREATED`.

#### Test fail criteria

The test is failing for "creating a new port" when:

- The HTTP response is not equal to `200 OK`.
- Executing a GET request with /rest/v1/system/ports/Port1 the HTTP response is not equal to `200 OK`.
- The configuration data posted is not the same as the retrieved port.

The test is failing for "creating a port with the same name as another port" when the HTTP response is not equal `400 BAD REQUEST`.

The test is failing for " creating a new port with an invalid string type" when the HTTP response is not equal `201 CREATED`.

The test is failing for "creating a new port with an invalid string type" when the HTTP response is not equal `400 BAD REQUEST`.

The test is failing for "creating a new port with a valid integer type" when the HTTP response is not equal to `201 CREATED`.

The test is failing for "creating a new port with an invalid array type" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "creating a new port with valid array type" when the HTTP response is not equal to `201 CREATED`.

The test is failing for "creating a new port with an invalid value on attribute" when the HTTP response is not equal `400 BAD REQUEST`.

The test is failing for "creating a new port with a valid value on an attribute" when the HTTP response is not equal to `201 CREATED`.

The test is failing for "creating a new port with a missing attribute" when the HTTP response is not equal `400 BAD REQUEST`.

The test is failing for "creating a new port with with all the attributes" when the HTTP response is not equal to `201 CREATED`.

The test is failing for "creating a new port with an unknown attribute" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "creating a new port with all allowed attributes" when the HTTP response is not equal to `201 CREATED`.

The test is failing for "creating a new port with malformed json data" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "creating a new port with well-formed json data" when the HTTP response is not equal to `201 CREATED`.


## REST API put method for ports

### Objective

The test case verifies the following:

- Modifying a port.
- Trying to modify the name of the port.
- Port data such as ranges, types, allowed values, malformed JSON, and missing attributes.

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

**Switch 1** has a port with the name "Port1" and with the following configuration data:

```
{
    "configuration":
    {
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

1. Execute a PUT request with /rest/v1/system/ports/Port1 and with the following data. Verify that the HTTP response is `200 OK`.

    ```
    {
        "configuration":
        {
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

2. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is `200 OK`.
3. Confirm that the configuration response data from Step 2 is the same as the configuration data from Step 1.

#### Update port using If-Match
1. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is `200 OK`.
2. Read the entity tag provided by the server
3. Set the "tag" value to: `"tag": 601`.
4. Execute a PUT request with /rest/v1/system/ports/Port1 including and If-Match Header using entity tag read at step 2.
5. Verify that the response is `200 OK`.
6. Confirm that tag value was updated.

#### Update port using If-Match (star as etag)
1. Set the "tag" value to: `"tag": 602`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 including an If-Match Header using '"*"' as entity tag
3. Verify that the response is `200 OK`.
4. Confirm that tag value was updated.

#### Update port using If-Match change applied
1. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is `200 OK`.
2. Read the entity tag provided by the server
3. Execute a PUT request with /rest/v1/system/ports/Port1 including and If-Match Header using entity tag different than the one read at step 2.
4. Verify that the response is `204 NO CONTENT`.

#### Update port using If-Match Precondition Failed
1. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is `200 OK`.
2. Read the entity tag provided by the server.
3. Set the "tag" value to: `"tag": 603`.
4. Execute a PUT request with /rest/v1/system/ports/Port1 including and If-Match Header using entity tag different than the one read at step 2.
5. Verify that the response is 412 PRECONDITION FAILED.


#### Update port name

1. Set the name of the port to "Port2": `"name": "Port2"`.
2. Execute a PUT request with /rest/v1/system/ports/Port1.
3. Verify that the HTTP response is `200 OK`.
4. Execute a GET request with /rest/v1/system/ports/Port1 and verify that the response is `200 OK`.
5. Confirm that the port is still named "Port1".

#### Data validation

##### Data types validation

###### Invalid string type

1. Set the "ip4_address" value to: `"ip4_address": 192`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid string type

1. Set the "ip4_address" value to: `"ip4_address": "192.168.0.1"`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify if the HTTP response is `200 OK`.

###### Invalid integer type

1. Set the "tag" value to: `"tag": "675"`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid integer type

1. Set the "tag" value to: `"tag": 675`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

###### Invalid array type

1. Set the "trunks" value to: `"trunks": "654,675"`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid array type

1. Set the "trunks" value to: `"trunks": [654,675]`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

##### Ranges Validation

###### Invalid range for string type

1. Set the "ip4_address" value to: `"ip4_address": "175.167.134.123/248"`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for string type

1. Set the "ip4_address" value to: `"ip4_address": "175.167.134.123/24"`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

###### Invalid range for integer type

1. Set the "tag" value to: `"tag": 4095`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for integer type

1. Set the "tag" value to: `"tag": 675`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

###### Invalid range for array type

1. Change the "interfaces" value to:

    ```
    "interfaces": ["/rest/v1/system/interfaces/1",
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
3. Verify that the HTTP response is `400 BAD REQUEST`.

##### Valid range for array type

1. Change the "interfaces" value to: `"interfaces": ["/rest/v1/system/interfaces/1"]`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

##### Allowed data values validation


###### Invalid data value

1. Change the "vlan_mode" value to: `"vlan_mode": "invalid_value"`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid data value

1. Change the "vlan_mode" value to: `"vlan_mode": "access"`.
2. Execute a PUT request with /rest/v1/system/ports/Port1 and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

##### Missing attribute validation

1. Execute a PUT request with /rest/v1/system/ports/Port1 and without the "vlan_mode" attribute.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a PUT request over /rest/v1/system/ports/Port1 with all the attributes.
4. Confirm that the HTTP response is `200 OK`.

##### Unknown attribute validation

1. Execute a PUT request with /rest/v1/system/ports/Port1 and with an unknown attribute: `"unknown_attribute": "unknown_value"`.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a PUT request with /rest/v1/system/ports/Port1 and with all allowed attributes.
4. Verify that the HTTP response is `200 OK`.

##### Malformed json validation

1. Execute a PUT request with /rest/v1/system/ports/Port1 and with a semi-colon at the end of the json data.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a PUT request with /rest/v1/system/ports/Port1 and without the semi-colon at the end of the json data.
4. Verify that the HTTP response is `200 OK`.

### Test result criteria
#### Test pass criteria

The test is passing for "updating a port" when the following results occur:

- The HTTP response is `200 OK`.
- The HTTP response is `200 OK` when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is the same as that of the retrieved port.

The test is passing for "updating a port using If-Match" when the following results occur:

- The HTTP response is `200 OK`.
- The HTTP response is `200 OK` when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is the same as that of the retrieved port.

The test is passing for "updating a port using If-Match and * as etag" when the following results occur:

- The HTTP response is `200 OK`.
- The HTTP response is `200 OK` when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is the same as that of the retrieved port.

The test is passing for "updating a port using If-Match and a change already applied" when the The HTTP response is `200 OK`.

The test is passing for "updating a port using If-Match and a not matching etag" when the The HTTP response is `412 PRECONDITION FAILED`.

The test is passing for "updating a port with the same name as another port" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "updating a port with a valid string type" when the HTTP response is `200 OK`.

The test is passing for "updating a port with an invalid string type" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "updating a port with a valid integer type" when the HTTP response is `200 OK`.

The test is passing for "updating a port with an invalid array type" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "updating a port with a valid array type" when the HTTP response is `200 OK`.

The test is passing for "updating a port with an invalid value on an attribute" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "updating a port with a valid value on an attribute" when the HTTP response is `200 OK`.

The test is passing for "updating a port with a missing attribute" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "updating a port with with all the attributes" when the HTTP response is `200 OK`.

The test is passing for "updating a port with an unknown attribute" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "updating a port with all the allowed attributes" when the HTTP response is `200 OK`.

The test is passing for "updating a port with malformed json data" when the HTTP response is `400 BAD REQUEST`.

The test is passing for "updating a port with well-formed json data" when the HTTP response is `200 OK`.

#### Test fail criteria

The test is failing for "updating a port" when the following occurs:

- The HTTP response is not equal to `200 OK`.
- The HTTP response is not equal to `200 OK` when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is not the same as the data on the retrieved port.

The test is failing for "updating a port using If-Match" when the following results occur:

- The HTTP response is not equal to `200 OK`.
- The HTTP response is not equal to `200 OK` when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is not the same as that of the retrieved port.

The test is failing for "updating a port using If-Match and * as etag" when the following results occur:

- The HTTP response is `200 OK`.
- The HTTP response is `200 OK` when executing a GET request with /rest/v1/system/ports/Port1.
- The configuration data posted is the same as that of the retrieved port.

The test is failing for "updating a port using If-Match and a change already applied" when the The HTTP response is not equal to `204 NOT CONTENT`.

The test is failing for "updating a port using If-Match and a not matching etag" when the The HTTP response is not equal to `412 PRECONDITION FAILED`.

The test is failing for "updating a port with the same name as another port" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "updating a port with a valid string type" when the HTTP response is not equal to `200 OK`.

The test is failing for "updating a port with an invalid string type" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "updating a port with a valid integer type" when the HTTP response is not equal to `200 OK`.

The test is failing for "updating a port with an invalid array type" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "updating a port with a valid array type" when the HTTP response is not equal to `200 OK`.

The test is failing for "updating a port with an invalid value on an attribute" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "updating a port with a valid value on an attribute" when the HTTP response is not equal to `200 OK`.

The test is failing for "updating a port with a missing attribute" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "updating a port with an unknown attribute" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "updating a port with an unknown attribute" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "updating a port with all the allowed attributes" when the HTTP response is not equal to `200 OK`.

The test is failing for "updating a port with malformed json data" when the HTTP response is not equal to `400 BAD REQUEST`.

The test is failing for "updating a port with well-formed json data" when the HTTP response is not equal to `200 OK`.


## REST API delete method for ports

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

**Switch 1** with a port named Port1 and the following configuration data:

```
{
    "configuration":
    {
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
        "other_config": {"cfg-1key": ""},
        "bond_active_slave": "null",
        "ip6_address_secondary": ["01:23:45:67:89:ab"],
        "vlan_options": {},
        "ip4_address": "192.168.0.1",
        "admin": "up"
    }
}
```

### Description

1. Execute a DELETE request on  /rest/v1/system/ports/Port1 and verify that the HTTP response is `204 NOT CONTENT`.
2. Execute a GET request on /rest/v1/system/ports and verify that the port is being deleted from the port list.
3. Execute a GET request on /rest/v1/ports/system/Port1 and verify that the HTTP response is `404 NOT FOUND`.
4. Execute a DELETE request on /rest/v1/system/ports/Port2 and ensure that the  HTTP response is `404 NOT FOUND`.
5. Execute a DELETE request on  /rest/v1/system/ports/Port1 using Conditional request If-Match and verify HTTP response is `412 PRECONDITION FAILED` and `204 NOT CONTENT`.

### Test result criteria

#### Test pass criteria

The test is passing for "deleting an existing port" when the following occurs:

- The HTTP response is `204 NOT CONTENT`.
- There is no URI "/rest/v1/system/ports/Port1" in the port list that is returned from the /rest/v1/system/ports URI.
- When doing a GET request on "/rest/v1/system/ports/Port1", the HTTP response is `404 NOT FOUND`.
- The HTTP response is `412 PRECONDITION FAILED` if Conditional request If-Match provided entity tag does not match the Port entity-tag.
- The HTTP response is `204 NOT CONTENT` if Conditional request If-Match provided entity tag matches the Port entity-tag.
- There is no URI "/rest/v1/system/ports/Port1" in the port list that is returned from the /rest/v1/system/ports URI.
- When doing a GET request on "/rest/v1/system/ports/Port1", the HTTP response is `404 NOT FOUND`.

The test case is passing for "deleting a non-existent" port when the HTTP response is `404 NOT FOUND`.

#### Test fail criteria

The test is passing for "deleting an existing port" when the following occurs:

- The HTTP response is not equal to `204 NOT CONTENT`.
- When performing a GET request on "/rest/v1/system/ports", "Port1" is displayed in the ports URI list.
- The HTTP response is not equal to `404 NOT FOUND` when doing a GET request on "/rest/v1/system/ports/Port1".

The test case is failing for "deleting a non-existent port" when the HTTP response is not equal to `404 NOT FOUND`.

## REST API get method with recursion for interfaces

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

### Requirements

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

**Switch 1** has an interface with the name 50-1 and with the following configuration data:

```
{
    "configuration":
    {
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
    a. Execute the GET request over /rest/v1/system/interfaces?depth=0.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned interface list has at least one element.
    d. Ensure that URI /rest/v1/system/interfaces/50 is in the response data.

2. Verify if returns a list of interface URIs by not using depth parameter.
    a. Execute the GET request over /rest/v1/system/interfaces
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned interface list has at least one element.
    d. Ensure that URI /rest/v1/system/interfaces/50 is in the response data.

3. Verify if returns an interface and first level data.
    a. Execute the GET request over /rest/v1/system/interfaces?depth=1;name=50-1
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Ensure that inner data has the URI /rest/v1/system/interfaces/50 in the response data.

4. Verify if returns an interface and second level data.
    a. Execute the GET request over /rest/v1/system/interfaces?depth=2;name=50-1
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Validate the second level depth returned interface object has Configuration, Statistics and Status keys present.
    e. Ensure that second level of depth inner data has the URIs /rest/v1/system/interfaces/50-{1-4} in the response data.

5. Verify if response has a `400 BAD REQUEST` HTTP response status code by using a negative depth value.
    a. Execute the GET request over /rest/v1/system/interfaces?depth=-1
    b. Verify if the HTTP response is `400 BAD REQUEST`.

6. Verify if response has a `400 BAD REQUEST` HTTP response status code by using a string depth value.
    a. Execute the GET request over /rest/v1/system/interfaces?depth=a
    b. Verify if the HTTP response is `400 BAD REQUEST`.

7. Verify if returns an interface with specific URI and data in first level of depth.
    a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=1
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Ensure that inner data has the URI /rest/v1/system/interfaces/50 in the response data.

8. Verify if returns an interface with specific URI and data in second level of depth.
    a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=2
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Validate the second level depth returned interface object has Configuration, Statistics and Status keys present.
    e. Ensure that second level of depth inner data has the URIs /rest/v1/system/interfaces/50-{1-4} in the response data.

9. Verify if returns a `400 BAD REQUEST` HTTP response status code by using a negative depth value with an specific URI.
    a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=-1
    b. Verify if the HTTP response is `400 BAD REQUEST`.

10. Verify if returns a `400 BAD REQUEST` HTTP response status code by using a string depth value with an specific URI.
    a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=a
    b. Verify if the HTTP response is `400 BAD REQUEST`.

11. Verify if returns an interface with specific URI by using depth equals zero.
    a. Execute the GET request over /rest/v1/system/interfaces/50-1?depth=0
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Ensure that inner data has the URI /rest/v1/system/interfaces/50 in the response data.

12. Verify if returns an interface with specific URI by not using depth parameter.
    a. Execute the GET request over /rest/v1/system/interfaces/50-1
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Ensure that inner data has the URI /rest/v1/system/interfaces/50 in the response data.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying an interface with the specified correct parameters in each step:
    - A `200 OK` HTTP response.
    - The correct data is returned.
    - The data for the first and second level of depth is as expected according to the parameters.

- Querying an interface list with the specified correct parameters in each step:
    - A `200 OK` HTTP response.
    - The data is in the interface list returned as expected.

- Querying an interface list with the specified incorrect parameters, such as negative depth or invalid character such a string, results in a `400 BAD REQUEST` HTTP response.

- Querying an interface with the specified name and depth parameter equals zero returns a `400 BAD REQUEST`.

#### Test fail criteria

This test fails when:

- Querying an interface with the specified correct parameters in each step:
    - A `200 OK` HTTP response is not received.
    - The incorrect data is returned.
    - The data for the first and second level of depth is not as expected according to the parameters.

- Querying an interface list with the specified correct parameters in each step:
    - A `200 OK` HTTP response is not received.
    - The data is not in the interface list returned.

- Querying an interface list with the specified incorrect parameters, such as negative depth or invalid character such a string, results in anything other than `400 BAD REQUEST` HTTP response.

- Querying an interface with the specified name and depth parameter equals zero returns anything other than `400 BAD REQUEST` HTTP response

## REST API get method with pagination for ports

### Objective
The test case verifies:

1. Query all ports with no pagination offset set.
2. Query all ports with no pagination limit set.
3. Query all ports with no pagination offset or limit set.
4. Query all ports with negative pagination offset set.
5. Query all ports with negative pagination limit set.
6. Query all ports with pagination offset set greater than data set's size.
7. Query all ports with pagination offset + limit greater than data set's size.
8. Query specific a port with only pagination offset set.
9. Query specific a port with only pagination limit set.
10. Query specific a port with both pagination offset and limit set.
11. Query first 10 ports using pagination indexes.
12. Query last 10 ports using pagination indexes.


### Requirements

- Period after exist
- Depth is set to 1 in all queries
- Port list is sorted by name

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

**Switch 1** has 100 ports (plus the default port named bridge_normal) with the name in the format PortN where N is a number between 0 and 99, each port has the following configuration data:

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

1. Query all ports with no pagination offset set.
    a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;limit=5"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 5 elements.
    d. Ensure the first port in the list is 'bridge_normal', which means offset defaulted to 0.

2. Query all ports with no pagination limit set.
    a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=91"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 10 elements.
    d. Ensure the first port in the list is 'Port90' and the last one is 'Port99, which means limit defaulted to the remainder size.

3. Query all ports with no pagination offset or limit set.
    a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 101 elements.

4. Query all ports with negative pagination offset set.
    a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=-1;limit=10"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

5. Query all ports with negative pagination limit set.
    a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=5;limit=-1"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

6. Query all ports with pagination offset set greater than data set's size.
    a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=200"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

7. Query all ports with pagination offset + limit greater than data set's size.
    a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=91;limit=20"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 10 elements.
    d. Ensure the first port in the list is 'Port90' and the last one is 'Port99, which means limit defaulted to the remainder size.

8. Query specific a port with only pagination offset set.
    a. Execute a GET request over /rest/v1/system/ports/bridge_normal with the following parameters: "?depth=1;offset=5"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

9. Query specific a port with only pagination limit set.
    a. Execute a GET request over /rest/v1/system/ports/bridge_normal with the following parameters: "?depth=1;limit=10"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

10. Query specific a port with both pagination offset and limit set.
    a. Execute a GET request over /rest/v1/system/ports/bridge_normal with the following parameters: "?depth=1;offset=0;limit=10"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

11. Query first 10 ports using pagination indexes.
    a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=0;limit=10"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 10 elements.
    d. Ensure the first port in the list is 'bridge_normal' and the last one is 'Port16'.

12. Query last 10 ports using pagination indexes.
    a. Execute a GET request over /rest/v1/system/ports with the following parameters: "?depth=1;sort=name;offset=91;limit=10"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 10 elements.
    d. Ensure the first port in the list is 'Port90' and the last one is 'Port99'.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying a port list with the specified correct parameters in each step:
    - A `200 OK` HTTP response.
    - The correct number of ports is returned.
    - The first and last ports in the list is as expected according to the parameters.

- Querying a port list with the specified incorrect parameters, such as negative indexes or out of range indexes, results in a `400 BAD REQUEST` HTTP response.

- Querying bridge_normal with pagination parameters returns a `400 BAD REQUEST`.

#### Test fail criteria

This test fails when:

- Querying a port list with the specified correct parameters in each step:
    - A `200 OK` HTTP response is not received.
    - An incorrect number of ports is returned.
    - The first and last ports in the list are not as expected according to the parameters.

- Querying a port list with the specified incorrect parameters, such as negative indexes or out of range indexes, results in anything other than `400 BAD REQUEST` HTTP response.

- Querying bridge_normal with pagination parameters returns anything other than `400 BAD REQUEST` HTTP response.


## REST API get method and sort by field for ports

### Objective

This test case verifies if the port list retrieved is sorted by a field.

### Requirements

- Period after exist.
- Depth is set to 1 in all queries.

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

**Switch 1** with 10 ports with the following configuration data, where index is a number between 1 and 10:

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

Sort by allowed sort field (ascending mode).

For each allowed sort field exececute the following steps:

1. Execute a GET request on /rest/v1/system/ports?depth=1;sort={field_name} and verify that response is `200 OK`.
2. Verify if the result is being ordered by the provided field name.

Sort by allowed sort field (descending mode).

For each allowed sort field exececute the following steps:

1. Execute a GET request on /rest/v1/system/ports?depth=1;sort=-{field_name} and verify that response is `200 OK`.
2. Verify if the result is being ordered by the provided field name.

### Test result criteria

#### Test pass criteria

This test passes by meeting the following criteria:

- The HTTP response is `200 OK`.
- The response has 10 ports.
- The ports are sorted ascending/descending by the field name.

#### Test fail criteria

This test fails when:

- The HTTP response is not equal to `200 OK`.
- The response doesn't have 10 ports.
- The port aren't sorted ascending/descending by the field name.


## REST API get method and sort by field combination for ports

### Objective

This test case verifies if the port list retrieved is sorted ascending/descending by a combination of fields.

### Requirements

- Period after exist.
- Depth is set to 1 in all queries.

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

**Switch 1** with 10 ports with the following configuration data, where index is a number between 1 and 10:

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
Port1:   admin = "up"
Port2:   admin = "down"
Port3:   admin = "up"
Port4:   admin = "down"
Port5:   admin = "up"
Port6:   admin = "down"
Port7:   admin = "up"
Port8:   admin = "down"
Port9:   admin = "up"
Port10:  admin = "down"
```

### Description
Sort by admin and name (Ascending mode)

1. Execute a GET request on /rest/v1/system/ports?depth=1;sort=admin,name and verify that response is `200 OK`.
2. Verify if the result is being ordered by the provided fields. First by admin and the by name.

Sort by admin and name (Descending mode)

1. Execute a GET request on /rest/v1/system/ports?depth=1;sort=-admin,name and verify that response is `200 OK`.
2. Verify if the result is being ordered by the provided fields. First by admin and the by name.

### Test result criteria

#### Test pass criteria

This test passes by meeting the following criteria:

- The HTTP response is `200 OK`.
- The response has 10 ports.
- The result is sorted ascending/descending by the combination of fields.

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

- The HTTP response is not `200 OK`.
- The response doesn't have 10 ports.
- The result is not sorted ascending/descending by the combination of fields.

REST API VLANs Resource test cases
==================================

## Query Bridge Normal

### Objective
The test case verifies queries for:

- Bridge Normal is present

### Requirements

- Bridge Normal exists

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if bridge_normal was created successfully.
    1. Execute the GET request over /rest/v1/system/bridges.
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the response data is not empty.
    4. Verify if /rest/v1/system/bridges/bridge_normal is returned within the response data.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying bridges for:
    - A `200 OK` HTTP response.
    - At least one bridge in the bridge list.
    - A URI "/rest/v1/system/bridges/bridge_normal" in the bridge list returned from the "/rest/v1/system/bridges" URI.

#### Test fail criteria

This test fails when:

- Querying a bridge for:
    - An HTTP response is not equal to `200 OK`
    - A GET request to "/rest/v1/system/bridges" and "/rest/v1/system/bridges/bridge_normal" is in the Bridges URI list.

## Query non-existent VLANs

### Objective
The test case verifies queries for:

- Non-existent VLANs in bridge_normal.

### Requirements

- Bridge Normal exists.

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was queried successfully:
    1. Execute the GET request over "/rest/v1/system/bridges/bridge_normal".
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the HTTP response data is empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying VLANs for:
    - A `200 OK` HTTP response.
    - No VLANs in VLANs URI list.

#### Test fail criteria

This test fails when:

- Querying a VLAN for:
    - An HTTP response is not equal to `200 OK`
    - A GET request to "rest/v1/system/bridges/bridge_normal" and the VLANs URI list is not empty.

## Query existent VLANs

### Objective
The test case verifies queries for:

- Existent VLAN

### Requirements

- Bridge Normal exists
- A test VLAN added to bridge normal

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "fake_vlan",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

- Verify if VLAN was queried successfully:
    1. Execute the GET request over "/rest/v1/system/bridges/bridge_normal".
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the HTTP response is not empty.
    4. Verify if "/rest/v1/system/bridges/bridge_normal/vlans/fake_vlan" is in the VLAN URI list.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying VLAN for:
    - A `200 OK` HTTP response.
    - Correct data is returned within the response.

#### Test fail criteria

This test fails when:

- Querying a VLAN for:
    - An HTTP response is not equal to `200 OK`
    - A GET request to "rest/v1/system/bridges/bridge_normal" and "/rest/v1/system/bridges/bridge_normal/vlans/fake_vlan" is not within VLANs URI list.

## Query existent VLAN by name

### Objective
The test case verifies queries for:

- Existent VLANs with name specified

### Requirements

- Bridge Normal exists
- A test VLAN added to bridge normal

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "fake_vlan",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

- Verify if VLAN was queried successfully:
    1. Execute the GET request over "/rest/v1/system/bridges/bridge_normal/vlans/fake_vlan".
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the HTTP response is not empty.
    4. Verify if the HTTP response data equals test VLAN in the "Configuration" section.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying VLANs for:
    - A `200 OK` HTTP response.
    - Correct data is returned within the response.

#### Test fail criteria

This test fails when:

- Querying a VLAN for:
    - An HTTP response is not equal to `200 OK`
    - A GET request to "rest/v1/system/bridges/bridge_normal" and info about "/rest/v1/system/bridges/bridge_normal/vlans/fake_vlan" is not within the HTTP response.

## Query non-existent VLAN by name

### Objective
The test case verifies queries for:

- Non-existent VLAN with name specified.

### Requirements

- Bridge Normal exists.

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was queried unsuccessfully:
    1. Execute the GET request over "/rest/v1/system/bridges/bridge_normal/vlans/not_found".
    2. Verify if the HTTP response is `404 NOT FOUND`.
    3. Verify if the HTTP response is empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying VLANs for:
    - A `404 NOT FOUND` HTTP response.
    - No VLAN is returned with the HTTP response data.

#### Test fail criteria

This test fails when:

- Querying a VLAN for:
    - An HTTP response is not equal to `404 NOT FOUND`.
    - A GET request to "rest/v1/system/bridges/bridge_normal/vlans/not_found" and there is at least one VLAN in the HTTP response.

## Create VLAN

### Objective
The test case verifies creation for:

- A non-existent VLAN.

### Requirements

- Bridge Normal exists.

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was created successfully:
    1. Execute the POST request over "/rest/v1/system/bridges/bridge_normal/vlans".
    2. Verify if the HTTP response is `201 CREATED`.
    3. Verify if the HTTP response is empty.

The new VLAN will have the following configuration:

```
{
    "configuration": {
        "name": "fake_vlan",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Creating VLAN for:
    - An HTTP `201 CREATED` response.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is an empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `201 CREATED`.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is an error in the HTTP response.

## Create VLAN using an invalid name

### Objective
The test case verifies creation for:

- A non-existent VLAN.

### Requirements

- Bridge Normal exists.

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was created unsuccessfully:
    1. Execute the POST request over "/rest/v1/system/bridges/bridge_normal/vlans" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": 1,
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Using an empty dictionary
```
{
    "configuration": {
        "name": {},
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": [],
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": ["test_vlan_1", "test_vlan_2"],
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": None,
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": True,
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Creating VLAN for:
    - An HTTP `400 BAD REQUEST` response.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is no error in the HTTP response.

## Create VLAN using an invalid ID

### Objective
The test case verifies creation for:

- A non-existent VLAN

### Requirements

- Bridge Normal exists

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was created unsuccessfully:
    1. Execute the POST request over "/rest/v1/system/bridges/bridge_normal/vlans" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an string
```
{
    "configuration": {
        "name": "test",
        "id": "id",
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Using an empty dictionary
```
{
    "configuration": {
        "name": "test",
        "id": {},
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": [],
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using one string in an array
```
{
    "configuration": {
        "name": "test",
        "id": ["id"],
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": ["test_vlan_1", "test_vlan_2"],
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": None,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": True,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Creating VLAN for:
    - A HTTP `400 BAD REQUEST` response.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is no error in the HTTP response.

## Create VLAN using an invalid Description

### Objective
The test case verifies creation for:

- A non-existent VLAN

### Requirements

- Bridge Normal exists

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was created unsuccessfully:
    1. Execute the POST request over "/rest/v1/system/bridges/bridge_normal/vlans" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": 1,
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Using an empty dictionary
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": {},
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": [],
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": ["test_vlan_1", "test_vlan_2"],
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": None,
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": True,
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Creating VLANs for:
    - A HTTP `400 BAD REQUEST` response.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is no error in the HTTP response.

## Create VLAN using an invalid Admin

### Objective
The test case verifies creation for:

- A non-existen VLAN

### Requirements

- Bridge Normal exists

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was created unsuccessfully:
    1. Execute the POST request over "/rest/v1/system/bridges/bridge_normal/vlans" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": 1,
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Using an invalid string
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": "admin",
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": [],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an invalid string in array
```
{
    "configuration": {
        "name": "test",
        "id": [],
        "description": "test_vlan",
        "admin": ["admin"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["test_vlan_1", "test_vlan_2"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": None,
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": True,
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Creating VLANs for:
    - An HTTP `400 BAD REQUEST` response.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is no error in the HTTP response.

## Create VLAN using an invalid other_config

### Objective
The test case verifies creation for:

- A non-existent VLAN

### Requirements

- Bridge Normal exists

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was created unsuccessfully:
    1. Execute the POST request over "/rest/v1/system/bridges/bridge_normal/vlans" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response data is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": 1,
        "external_ids": {}
    }
}
```

#### Using a string
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": "other_config",
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": [],
        "external_ids": {}
    }
}
```

##### Using one string in array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": ["other_config"],
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": ["test_vlan_1", "test_vlan_2"],
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": None,
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": True,
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Creating VLANs for:
    - An HTTP `400 BAD REQUEST` response.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is no error in the HTTP response.

## Create VLAN using an invalid external_ids

### Objective
The test case verifies creation for:

- A non-existent VLAN

### Requirements

- Bridge Normal exists

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was created unsuccessfully:
    1. Execute the POST request over "/rest/v1/system/bridges/bridge_normal/vlans" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": 1
    }
}
```

#### Using a string
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": "other_config"
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": []
    }
}
```

##### Using one string in array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": ["other_config"]
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": ["test_vlan_1", "test_vlan_2"]
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": None
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": True
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Creating VLAN for:
    - An HTTP `400 BAD REQUEST` response.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is no error in the HTTP response.

## Create VLAN with missing fields

### Objective
The test case verifies creation for:

- A non-existent VLAN

### Requirements

- Bridge Normal exists

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was created unsuccessfully:
    1. Execute the POST request over "/rest/v1/system/bridges/bridge_normal/vlans" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Without name
```
{
    "configuration": {
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Without ID
```
{
    "configuration": {
        "name": "test",
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Creating VLANs for:
    - An HTTP `400 BAD REQUEST` response.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is no error in the HTTP response.

## Create a duplicated VLAN

### Objective
The test case verifies creation for:

- An existent VLAN

### Requirements

- Bridge Normal exists

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if VLAN was created unsuccessfully.
    1. Execute the POST request over "/rest/v1/system/bridges/bridge_normal/vlans" using the following configuration:

        ```
        {
            "configuration": {
                "name": "fake_vlan",
                "id": 1,
                "description": "test_vlan",
                "admin": ["up"],
                "other_config": {},
                "external_ids": {}
            }
        }
        ```

    2. Verify if the HTTP response is `201 CREATED`.
    3. Verify if the HTTP response is empty.
    4. Execute the POST request again from above.
    5. Verify if the HTTP response is `400 BAD REQUEST`.
    6. Verify if the HTTP response is not empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Creating VLAN for:
    - An HTTP 200 CREATED response the first time.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is an empty HTTP response.

- Creating the same VLAN for:
    - An HTTP `400 BAD REQUEST` response.
    - A POST request to "/rest/v1/system/bridges/bridge_normal/vlans/" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to 200 CREATED.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is an error in the HTTP response.

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to "rest/v1/system/bridges/bridge_normal/vlans/" and there is no error in the HTTP response.

## Update VLAN name

### Objective
The test case verifies updates for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- A test VLAN added to bridge normal

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

- Verify if VLAN was updated successfully:
    1. Execute the PUT request over "/rest/v1/system/bridges/bridge_normal/vlans/test" with the name field with "fake_vlan".
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the HTTP response is not empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Updating VLAN for:
    - A `200 OK` HTTP response.
    - The HTTP response is empty.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `200 OK`.
    - A PUT request to "rest/v1/system/bridges/bridge_normal/vlans/test" and the HTTP response is not empty.

## Update VLAN using an invalid name

### Objective
The test case verifies updates for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- A test VLAN added

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

- Verify if VLAN was updated unsuccessfully:
    1. Execute the PUT request over "/rest/v1/system/bridges/bridge_normal/vlans/test" with each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": 1,
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Using an empty dictionary
```
{
    "configuration": {
        "name": {},
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": [],
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": ["test_vlan_1", "test_vlan_2"],
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": None,
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": True,
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Updating VLAN for:
    - An HTTP `400 BAD REQUEST` response.
    - A PUT request to "/rest/v1/system/bridges/bridge_normal/vlans/test" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to "rest/v1/system/bridges/bridge_normal/vlans/test" and there is no error in the HTTP response.

## Update VLAN using an invalid ID

### Objective
The test case verifies updates for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- A test VLAN added

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

- Verify if VLAN was updated unsuccessfully:
    1. Execute the PUT request over "/rest/v1/system/bridges/bridge_normal/vlans/test" with each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an string
```
{
    "configuration": {
        "name": "test",
        "id": "id",
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Using an empty dictionary
```
{
    "configuration": {
        "name": "test",
        "id": {},
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": [],
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using one string in an array
```
{
    "configuration": {
        "name": "test",
        "id": ["id"],
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": ["test_vlan_1", "test_vlan_2"],
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": None,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": True,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Updating VLAN for:
    - An HTTP `400 BAD REQUEST` response.
    - A PUT request to "/rest/v1/system/bridges/bridge_normal/vlans/test" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to "rest/v1/system/bridges/bridge_normal/vlans/test" and there is no error in the HTTP response.

## Update VLAN using an invalid Description

### Objective
The test case verifies updates for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- A test VLAN added

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

- Verify if VLAN was updated unsuccessfully:
    1. Execute the PUT request over "/rest/v1/system/bridges/bridge_normal/vlans/test" with each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": 1,
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Using an empty dictionary
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": {},
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": [],
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": ["test_vlan_1", "test_vlan_2"],
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": None,
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": True,
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Updating VLANs for:
    - An HTTP `400 BAD REQUEST` response.
    - A PUT request to "/rest/v1/system/bridges/bridge_normal/vlans/test" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to "rest/v1/system/bridges/bridge_normal/vlans/test" and there is no error in the HTTP response.

## Update VLAN using an invalid Admin

### Objective
The test case verifies updates for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- A test VLAN added

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

- Verify if VLAN was updated unsuccessfully:
    1. Execute the PUT request over "/rest/v1/system/bridges/bridge_normal/vlans/test" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": 1,
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Using an invalid string
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": "admin",
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": [],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using an invalid string in array
```
{
    "configuration": {
        "name": "test",
        "id": [],
        "description": "test_vlan",
        "admin": ["admin"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["test_vlan_1", "test_vlan_2"],
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": None,
        "other_config": {},
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": True,
        "other_config": {},
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Updating VLANs for:
    - An HTTP `400 BAD REQUEST` response.
    - A PUT request to "/rest/v1/system/bridges/bridge_normal/vlans/test" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to "rest/v1/system/bridges/bridge_normal/vlans/test" and there is no error in the HTTP response.

## Update VLAN using an invalid other_config

### Objective
The test case verifies updates for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- A test VLAN added

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

- Verify if VLAN was updated unsuccessfully:
    1. Execute the PUT request over "/rest/v1/system/bridges/bridge_normal/vlans/test" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": 1,
        "external_ids": {}
    }
}
```

#### Using a string
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": "other_config",
        "external_ids": {}
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": [],
        "external_ids": {}
    }
}
```

##### Using one string in array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": ["other_config"],
        "external_ids": {}
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": ["test_vlan_1", "test_vlan_2"],
        "external_ids": {}
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": None,
        "external_ids": {}
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": True,
        "external_ids": {}
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Updating VLAN for:
    - An HTTP `400 BAD REQUEST` response.
    - A PUT request to "/rest/v1/system/bridges/bridge_normal/vlans/test" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to "rest/v1/system/bridges/bridge_normal/vlans/test" and there is no error in the HTTP response.

## Update VLAN using an invalid external_ids

### Objective
The test case verifies updates for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- A test VLAN added

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

- Verify if VLAN was updated unsuccessfully:
    1. Execute the PUT request over "/rest/v1/system/bridges/bridge_normal/vlans/test" using each configuration.
    2. Verify if the HTTP response is `400 BAD REQUEST`.
    3. Verify if the HTTP response is not empty.

The new VLAN will have the following configurations:

#### Using an int
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": 1
    }
}
```

#### Using a string
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": "other_config"
    }
}
```

##### Using an empty array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": []
    }
}
```

##### Using one string in array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": ["other_config"]
    }
}
```

##### Using multiple string in an array
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": ["test_vlan_1", "test_vlan_2"]
    }
}
```

##### Using None
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": None
    }
}
```

##### Using a boolean
```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": True
    }
}
```

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Updating VLAN for:
    - An HTTP `400 BAD REQUEST` response.
    - A PUT request to "/rest/v1/system/bridges/bridge_normal/vlans/test" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to "rest/v1/system/bridges/bridge_normal/vlans/test" and there is no error in the HTTP response.

## Update VLAN with missing fields

### Objective
The test case verifies updates for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- A test VLAN added

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

**Switch 1** has bridge_normal configured by default. A test VLAN is added with the following configurations:

```
{
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description

Verify if VLAN was updated unsuccessfully. The new VLAN will have the following configurations:

#### Without name
```
{
    "configuration": {
        "id": 1,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

#### Without ID
```
{
    "configuration": {
        "name": "test",
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

1. Execute the PUT request over "/rest/v1/system/bridges/bridge_normal/vlans/test" with each configuration.
2. Verify if the HTTP response is `400 BAD REQUEST`.
3. Confirm that the HTTP response is not empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Updating VLANs for:
    - An HTTP `400 BAD REQUEST` response.
    - A PUT request to "/rest/v1/system/bridges/bridge_normal/vlans/test" and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to "rest/v1/system/bridges/bridge_normal/vlans/test" and there is no error in the HTTP response.

## Delete non-existent VLAN

### Objective
The test case verifies deletes for:

- A non-existent VLAN

### Requirements

- Bridge Normal exists

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

**Switch 1** has bridge_normal configured by default.

### Description

- Verify if non-existent VLAN was not deleted:
    1. Execute the DELETE request over "/rest/v1/system/bridges/bridge_normal/vlans/not_found".
    2. Verify if the HTTP response is `404 NOT FOUND`.
    3. Verify if the HTTP response is empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Deleting VLAN for:
    - An HTTP `404 NOT FOUND` response.
    - A DELETE request to "/rest/v1/system/bridges/bridge_normal/vlans/not_dounf" and there is a empty HTTP response.

#### Test fail criteria

This test fails when:

- Deleting VLAN for:
    - An HTTP response is not equal to `404 NOT FOUND`.
    - A DELETE request to "rest/v1/system/bridges/bridge_normal/vlans/not_found" and there is a non-empty HTTP response.

## Query VLANs filtered by name

### Objective
The test case verifies queries for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- 10 test VLANs added to bridge normal

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

**Switch 1** has bridge_normal configured by default. Ten test VLANs are added with the following configurations:

```
{
    "configuration": {
        "name": "Vlan-<number>",
        "id": <number>,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

The "number" will be from 1 to 10 respectively.

### Description

- Verify if VLAN was queried successfully:
    1. Execute the GET request over "/rest/v1/system/bridges/bridge_normal/vlans?depth=1;name=Vlan-<number>" for each VLAN added.
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the HTTP response is not empty.
    4. Verify if the HTTP response contains one VLAN.
    5. Verify if the retrieved VLAN name is correct.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying VLAN for:
 - A `200 OK` HTTP response.
 - Correct data is returned within the response.

#### Test fail criteria

This test fails when:

- Querying VLAN for:
 - An HTTP response is not equal to `200 OK`.
 - A GET request to "rest/v1/system/bridges/bridge_normal/vlans?depth=1;name=Vlan-<number>" and the test VLAN is not within the HTTP response.

## Query VLANs filtered by ID

### Objective
The test case verifies queries for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- 10 test VLANs added to bridge normal

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

**Switch 1** has bridge_normal configured by default. Ten test VLANs are added with the following configurations:

```
{
    "configuration": {
        "name": "Vlan-<number>",
        "id": <number>,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

The "number" will be from 1 to 10 respectively.

### Description

- Verify if the test VLAN is filtered by name:
    1. Execute the GET request over "/rest/v1/system/bridges/bridge_normal/vlans?depth=1;id=<number>" for each VLAN added.
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the HTTP response is not empty.
    4. Verify if the HTTP response contains one VLAN.
    5. Verify if the retrieved VLAN id is correct.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying VLAN for:
    - A `200 OK` HTTP response.
    - Correct data is returned within the response.

#### Test fail criteria

This test fails when:

- Querying VLAN for:
    - An HTTP response is not equal to `200 OK`.
    - A GET request to "rest/v1/system/bridges/bridge_normal/vlans?depth=1;id=Vlan-<number>" and the test VLAN is not within the HTTP response.

## Query VLANs filtered by Description

### Objective
The test case verifies queries for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- 10 test VLANs added to bridge normal

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

**Switch 1** has bridge_normal configured by default. Ten test VLANs are added with the following configurations:

```
{
    "configuration": {
        "name": "Vlan-<number>",
        "id": <number>,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

**Switch 1** 5 VLANs (from 1 to 5) descriptions have to modified with the following configurations:

```
{
    "configuration": {
        "name": "Vlan-<number>",
        "id": <number>,
        "description": "fake_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

The "number" will be from 1 to 10 respectively.

### Description

- Verify if VLAN was queried successfully:
    1. Execute the GET request over "/rest/v1/system/bridges/bridge_normal/vlans?depth=1;description=fake_vlan" for each VLAN modified.
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the HTTP response is not empty.
    4. Verify if the HTTP response contains five VLANs.
    5. Verify if the retrieved VLANs description are correct.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying VLAN for:
    - A `200 OK` HTTP response.
    - Correct data is returned within the response.

#### Test fail criteria

This test fails when:

- Querying VLAN for:
    - An HTTP response is not equal to `200 OK`.
    - A GET request to "rest/v1/system/bridges/bridge_normal/vlans?depth=1;description=fake_vlan" and the test VLANs are not within the HTTP response.

## Query VLANs filtered by Admin

### Objective
The test case verifies queries for:

- An existent VLAN

### Requirements

- Bridge Normal exists
- 10 test VLANs added to bridge normal

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

**Switch 1** has bridge_normal configured by default. Ten test VLANs are added with the following configurations:

```
{
    "configuration": {
        "name": "Vlan-<number>",
        "id": <number>,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

**Switch 1** 5 VLANs (from 1 to 5) descriptions have to modified with the following configurations:

```
{
    "configuration": {
        "name": "Vlan-<number>",
        "id": <number>,
        "description": "test_vlan",
        "admin": ["down"],
        "other_config": {},
        "external_ids": {}
    }
}
```

The "number" will be from 1 to 10 respectively.

### Description

- Verify if VLAN was queried successfully:
    1. Execute the GET request over "/rest/v1/system/bridges/bridge_normal/vlans?depth=1;admin=down" for each VLAN modified.
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the HTTP response is not empty.
    4. Verify if the HTTP response contains five VLANs.
    5. Verify if the retrieved VLANs description are correct.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying VLAN for:
    - A `200 OK` HTTP response.
    - Correct data is returned within the response.

#### Test fail criteria

This test fails when:

- Querying VLAN for:
    - An HTTP response is not equal to `200 OK`.
    - A GET request to "rest/v1/system/bridges/bridge_normal/vlans?depth=1;admin=down" and the test VLANs are not within the HTTP response.


##  Declarative configuration schema validations
### Objective
The test case verifies that the schema validations for the declarative configuration including incorrect data type, out of range, missing mandatory field, and invalid reference checking prevents invalid configurations from reaching the database.

### Requirements

Physical or virtual switches are required for this test.

### Setup
#### Topology diagram

```ditaa
    +----------------+         +----------------+
    |                |         |                |
    |                |         |                |
    |      Host      +---------+     Switch     |
    |                |         |                |
    |                |         |                |
    +----------------+         +----------------+
```

#### Test Setup
Two configurations are used for verifying that the schema validations are preventing invalid configurations.

**Valid Configuration**

```
{
    "Interface": {
        "49": {
            "name": "49",
            "type": "system"
        }
    },
    "Port": {
        "p1": {
            "admin": "up",
            "name": "p1",
            "vlan_mode": "trunk",
            "trunks": [1]
        }
    },
    "System": {
        "aaa": {
            "fallback": "false",
            "radius": "false"
        },
        "asset_tag_number": "",
        "bridges": {
            "bridge_normal": {
                "datapath_type": "",
                "name": "bridge_normal",
                "ports": [
                    "p1"
                ]
            }
        },
        "hostname": "ops",
        "subsystems": {
            "base": {
                "asset_tag_number": "Open Switch asset tag 222"
            }
        },
        "vrfs": {
            "vrf_default": {
                "name": "vrf_default"
            }
        }
    }
}
```

**Invalid Configuration**

```
{
    "Interface": {
        "49": {
            "name": 1,
            "type": "system"
        }
    },
    "Port": {
        "p1": {
            "admin": "up",
            "name": "p1",
            "vlan_mode": "trunk",
            "trunks": [0]
        }
    },
    "System": {
        "aaa": {
            "fallback": "false",
            "radius": "false"
        },
        "asset_tag_number": "",
        "bridges": {
            "bridge_normal": {
                "datapath_type": "",
                "name": "bridge_normal",
                "ports": [
                    "p2"
                ]
            }
        },
        "subsystems": {
            "base": {
                "asset_tag_number": "Open Switch asset tag 222"
            }
        },
        "vrfs": {
            "vrf_default": {
                "name": "vrf_default"
            }
        }
    }
}
```

### Description
The valid configuration confirms that the schema validations are not returning false positives. The invalid configuration is a modified version of the valid configuration for confirming that the different types of validations detect issues including incorrect data types, out of range values, missing mandatory fields, and invalid references. Schema validations are verified by performing the following steps:

1. Send a PUT request with the valid configurations to the `/rest/v1/system/full-configuration?type=running` path.
2. Verify that the request was successful by confirming that the return code is equal to `200`.
3. Confirm that the schema validations are verifying the data by attempting to send a PUT request to the `/rest/v1/system/full-configuration?type=running` path by using the invalid data. The invalid data removes the mandatory field `hostname` from `System`, sets an invalid reference in `bridge_normal` to `p2`, changes the type of the `name` field in interface `49`, and sets an out-of-range value for `trunks` for port `p1`.
4. Verify that the request was not successful by confirming that the return code is not equal to `200`.
5. To confirm that the error response is triggered by schema validations, verify that it contains an error message for each field with an invalid value in the response data.

### Test result criteria
#### Test pass criteria
The test case is considered passing if the PUT request using the valid data is successful and fails the second PUT request attempt using the invalid data. The response data must include an `error` field and an associated error message for each field.

#### Test fail criteria
The test is considered failing if the PUT request using the invalid data is successful. A successful response indicates that the schema validations did not detect errors in the data.

##  Custom validators
### Objective
This test case verifies that the custom validation framework invokes an implemented custom validator upon a POST request and also returns any issues.

### Requirements

- Physical or virtual switches
- `bgp_router.py` custom validator

The `bgp_router.py` is located in the `opsplugins` directory of the `ops-quagga` repository.

### Setup
#### Topology diagram

```ditaa
    +----------------+         +----------------+
    |                |         |                |
    |                |         |                |
    |      Host      +---------+     Switch     |
    |                |         |                |
    |                |         |                |
    +----------------+         +----------------+
```

#### Test Setup
Two BGP configurations are used for verifying the REST custom validations. The first BGP router configuration is used for the valid test case, and the second BGP router configuration is used for the invalid test case. The following configurations are used for testing REST custom validators:

**BGP Router 1 configuration for valid test caes**

```
{
    "configuration": {
        "always_compare_med": True,
        "asn": 6001
    }
}
```

**BGP Router 2 configuration for invalid test case**

```
{
    "configuration": {
        "always_compare_med": True,
        "asn": 6002
    }
}
```

Two configurations are used for verifying the declarative configuration custom validations. The first configuration is a full valid configuration, and the second configuration includes an invalid amount of BGP routers. Similar to the REST custom validation test, the DC test also tests BGP router configurations. The following configurations are used in the valid and invalid test cases:

**Valid Declarative Configuration**

```
{
    "Interface": {
        "49": {
            "name": "49",
            "type": "system"
        }
    },
    "Port": {
        "p1": {
            "admin": "up",
            "name": "p1",
            "vlan_mode": "trunk",
            "trunks": [1]
        }
    },
    "System": {
        "aaa": {
            "fallback": "false",
            "radius": "false"
        },
        "asset_tag_number": "",
        "bridges": {
            "bridge_normal": {
                "datapath_type": "",
                "name": "bridge_normal",
                "ports": [
                    "p1"
                ]
            }
        },
        "hostname": "ops",
        "subsystems": {
            "base": {
                "asset_tag_number": "Open Switch asset tag 222"
            }
        },
        "vrfs": {
            "vrf_default": {
                "name": "vrf_default"
            }
        }
    }
}
```

**Invalid Declarative Configuration**

```
{
    "Interface": {
        "49": {
            "name": "49",
            "type": "system"
        }
    },
    "Port": {
        "p1": {
            "admin": "up",
            "name": "p1",
            "vlan_mode": "trunk",
            "trunks": [1]
        }
    },
    "System": {
        "aaa": {
            "fallback": "false",
            "radius": "false"
        },
        "asset_tag_number": "",
        "bridges": {
            "bridge_normal": {
                "datapath_type": "",
                "name": "bridge_normal",
                "ports": [
                    "p1"
                ]
            }
        },
        "hostname": "ops",
        "subsystems": {
            "base": {
                "asset_tag_number": "Open Switch asset tag 222"
            }
        },
        "vrfs": {
            "vrf_default": {
                "bgp_routers": {
                    "6001": {
                        "always_compare_med": True
                    },
                    "6002": {
                        "always_compare_med": True
                    }
                },
                "name": "vrf_default"
            }
        }
    }
}
```

### Description
To verify that the custom validation framework invokes the custom validator for the BGP router resource, the BGP router validator responsible for checking the number of BGP routers will return an error response that also includes an error code. For the BGP router table, only one BGP router is permitted. The following steps verify the custom validation framework using REST:

1. Create a BGP router by sending BGP router 1 configurations as data in a POST request to the path `/rest/v1/system/vrfs/vrf_default/bgp_routers`.
2. Verify that the request was successful by confirming that the return code is equal to `201`.
3. Confirm the validator works by attempting to create another BGP router with a different ASN using BGP router 2 configurations as data sent in another POST request to the `/rest/v1/system/vrfs/vrf_default/bgp_routers` path.
4. Verify that the request was not successful by confirming that the return code is not equal to `201`.
5. To confirm that the error response was triggered by the custom validator, verify from the response data that it contains a `code` field.

The declarative custom validation is verified by the following steps:

1. Send a PUT request using the valid DC configuration to the path `/rest/v1/system/full-configuration?type=running`.
2. Verify that the request was successful by confirming that the return code is equal to `200`.
3. Confirm the validator works by attempting to configure two BGP routers in the declarative configuration using the invalid configuration.
4. Verify that the request was not successful by confirming that the return code is not equal to `200`.
5. To confirm that the error response was triggered by the custom validator, verify from the response data that it contains a `code` field.

### Test result criteria
#### Test pass criteria
For REST, the test case is considered passing if the request for creating the first BGP router is successful and fails the attempt to create a second BGP router with a different ASN. The response data must include an `error` field and an associated `code`. For the declarative configuration, the test is considered passing when the configuration includes two BGP routers and results in an error response prohibiting the configuration from being applied.

#### Test fail criteria
For REST, the test case is considered failing if the second request to create another BGP router is successful. A successful response indicates that the custom validation framework did not invoke the custom validator for the BGP router. Similarly, for the declarative configuration, the test case is considered failing if a successful response is received when configuring the invalid configuration.
