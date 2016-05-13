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
- [REST API method access](#rest-api-method-access)
- [REST API user account management](#rest-api-user-account-management)
- [REST API startup config verify](#rest-api-startup-config-verify)
- [REST API get method for ports](#rest-api-get-method-for-ports)
- [REST API post method for ports](#rest-api-post-method-for-ports)
- [REST API put method for ports](#rest-api-put-method-for-ports)
- [REST API delete method for ports](#rest-api-delete-method-for-ports)
- [REST API get method with recursion for interfaces](#rest-api-get-method-with-recursion-for-interfaces)
- [REST API get method with filtering for ports](#rest-api-get-method-with-filtering-for-ports)
- [REST API get method with pagination for ports](#rest-api-get-method-with-pagination-for-ports)
- [REST API get method and sort by field for ports](#rest-api-get-method-and-sort-by-field-for-ports)
- [REST API get method and sort by field combination for ports](#rest-api-get-method-and-sort-by-field-combination-for-ports)
- [REST API get method with specific column retrieval for interfaces](#rest-api-get-method-with-specific-column-retrieval-for-interfaces)
- [REST API patch method for system](#rest-api-patch-method-for-system)
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
  - [Create VLAN using an invalid other_config](#create-vlan-using-an-invalid-other_config)
  - [Create VLAN using an invalid external_ids](#create-vlan-using-an-invalid-external_ids)
  - [Create VLAN with missing fields](#create-vlan-with-missing-fields)
  - [Create a duplicated VLAN](#create-a-duplicated-vlan)
  - [Update VLAN name](#update-vlan-name)
  - [Update VLAN using an invalid name](#update-vlan-using-an-invalid-name)
  - [Update VLAN using an invalid ID](#update-vlan-using-an-invalid-id)
  - [Update VLAN using an invalid Description](#update-vlan-using-an-invalid-description)
  - [Update VLAN using an invalid Admin](#update-vlan-using-an-invalid-admin)
  - [Update VLAN using an invalid other_config](#update-vlan-using-an-invalid-other_config)
  - [Update VLAN using an invalid external_ids](#update-vlan-using-an-invalid-external_ids)
  - [Update VLAN with missing fields](#update-vlan-with-missing-fields)
  - [Delete non-existent VLAN](#delete-non-existent-vlan)
  - [Query VLANs filtered by name](#query-vlans-filtered-by-name)
  - [Query VLANs filtered by ID](#query-vlans-filtered-by-id)
  - [Query VLANs filtered by Description](#query-vlans-filtered-by-description)
  - [Query VLANs filtered by Admin](#query-vlans-filtered-by-admin)
  - [Update VLAN using If Match header with star Etag](#update-vlan-using-if-match-header-with-star-etag)
  - [Update VLAN using If Match header with a matching Etag](#update-vlan-using-if-match-header-with-a-matching-etag)
  - [Update VLAN using If Match header with a not matching Etag](#update-vlan-using-if-match-header-with-a-not-matching-etag)
  - [Create VLAN using If Match header with a matching Etag](#create-vlan-using-if-match-header-with-a-matching-etag)
  - [Create VLAN using If Match header with a not matching Etag](#create-vlan-using-if-match-header-with-a-not-matching-etag)
  - [Query all VLANs using If Match header with a matching Etag](#query-all-vlans-using-if-match-header-with-a-matching-etag)
  - [Query all VLANs using If Match header with a not matching Etag](#query-all-vlans-using-if-match-header-with-a-not-matching-etag)
  - [Query VLAN using If Match header with a matching Etag](#query-vlan-using-if-match-header-with-a-matching-etag)
  - [Query VLAN using If Match header with a not matching Etag](#query-vlan-using-if-match-header-with-a-not-matching-etag)
  - [Delete VLAN using If Match header with a matching Etag](#delete-vlan-using-if-match-header-with-a-matching-etag)
  - [Delete VLAN using If Match header with a not matching Etag](#delete-vlan-using-if-match-header-with-a-not-matching-etag)
- [Declarative configuration schema validations](#declarative-configuration-schema-validations)
- [Custom validators](#custom-validators)
- [HTTPS support](#https-support)
- [Auditlog support](#auditlog-support)
- [REST API Logs with No Filters](#rest-api-logs-no-filters)
- [REST API Logs with Pagination](#rest-api-logs-with-pagination)
- [REST API Logs with Invalid Filters](#rest-api-logs-with-invalid-filters)
- [REST API Logs with Priority](#rest-api-logs-with-priority)
- [REST API Logs with Since and Until](#rest-api-logs-with-since-and-until)
- [REST API Logs with Syslog Identifier](#rest-api-logs-with-syslog-identifier)



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

**URL `/rest/v1/system`**

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure an IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Configure the system through the Standard REST API PUT method for the URI `/rest/v1/system`.
5. Validate the system configuration with the HTTP return code for the URI `/rest/v1/system`.
6. Execute the Standard REST API GET method for URI `/rest/v1/system`.
7. Validate the GET method HTTP return code for `/rest/v1/system` and its respective values.

### Test result criteria
#### Test pass criteria
- The first test passes (steps 4 and 5), if the standard REST API PUT method returns HTTP code `200 OK` for the URI `/rest/v1/system`.
- The second test passes (steps 6 and 7), if the standard REST API GET method returns HTTP code `200 OK` for the URI `/rest/v1/system` and the returned data is identical to the date used for the PUT.

#### Test fail criteria
- The first test fails if the standard REST API PUT method does not return HTTP code `200 OK` for the URI `/rest/v1/system`.
- The second test fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI `/rest/v1/system` or the returned data is not identical to the data used for PUT.

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

**URL `/rest/v1/system/subsystems`**

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Execute the Standard REST API GET method for URI `/rest/v1/system/subsystems`.
5. Validate the GET method HTTP return code for `/rest/v1/system/subsystems` and its respective values.

### Test result criteria
#### Test pass criteria
The test passes if the standard REST API GET method returns HTTP code `200 OK` for the URI `/rest/v1/system/subsystems` and the returned data is identical.

#### Test fail criteria
The test case is fails if the standard REST API GET method does not return the HTTP code `200 OK` for the URI `/rest/v1/system/subsystems`.

## REST API get method for an interface
### Objective
The objective of the test case is to validate the `/rest/v1/system/interfaces/<id>` through the standard REST API GET method.

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
The objective of the test case is to validate the `/rest/v1/system/interfaces/<id>` through the standard REST API GET method.

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.

##### Test 1
1. Configure the `/rest/v1/system/interfaces/<id>` through Standard REST API PUT method.
2. Validate the `/rest/v1/system/interfaces/<id>` configuration with the HTTP return code.

##### Test 2
1. Execute the Standard REST API GET method for URI `/rest/v1/system/interfaces/<id>`.
2. Validate the GET Method HTTP return code for `/rest/v1/system/interfaces/<id>` and its respective values.

##### Test 3
1. Execute Standard REST API DELETE method for URI `/rest/v1/system/interfaces/<id>`.
2. Validate the DELETE method HTTP return code for `/rest/v1/system/interfaces/<id>`.

##### Test 4
1. Execute Standard REST API GET Method for URI `/rest/v1/system/interfaces/<id>`.
2. Validate the GET method HTTP return code for `/rest/v1/system/interfaces/<id>`.

### Test result criteria
#### Test pass criteria
- The first test passes if the standard REST API PUT method returns HTTP code `200 OK` for the URI `/rest/v1/system/interfaces/<id>`.
- The second test passes if the standard REST API GET method returns HTTP code `200 OK` for the URI `/rest/v1/system/interfaces/<id>` and the returned data is identical to the date used for the PUT.
- The third test passes if the standard REST API DELETE method returns HTTP code `204 NO CONTENT` for the URI `/rest/v1/system/interfaces/<id>`.
- The fourth test passes, if the standard REST API GET method does not return HTTP code `200 OK` for the URI `/rest/v1/system/interfaces/<id>`.

#### Test fail criteria
- The first test fails if the standard REST API PUT method does not return HTTP code `200 OK` for the URI `/rest/v1/system/interfaces/<id>`.
- The second test fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI `/rest/v1/system/interfaces/<id>` or the returned data is not identical to the data used for PUT.
- The third test fails if the standard REST API DELETE method does not return HTTP code `204 NO CONTENT` for the URI `/rest/v1/system/interfaces/<id>`.
- The fourth test fails if the standard REST API GET method returns HTTP code `200 OK` for the URI `/rest/v1/system/interfaces/<id>`.

## REST API get method for VRFS
### Objective
The objective of this test case is to validate the `/rest/v1/system/vrfs` through the standard REST API GET method.

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
Validate the `/rest/v1/system/vrfs` through the standard REST API GET method.

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Execute the Standard REST API GET Method for URI `/rest/v1/system/vrfs`.
5. Validate the GET Method HTTP return code for `/rest/v1/system/vrfs` and its respective values.

### Test result criteria
#### Test pass criteria
The test case is passes if the standard REST API GET method returns HTTP code `200 OK` for the URI `/rest/v1/system/vrfs` and if the returned data is identical.

#### Test fail criteria
The test case fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI `/rest/v1/system/vrfs`.

## REST API get method for route maps
### Objective
The objective of this test case is to validate the `/rest/v1/system/route_maps/<id>` through the standard REST API GET method.

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
The test case validates the `/rest/v1/system/route_maps/<id>` through the standard REST API GET method.

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Execute the Standard REST API GET Method for URI `/rest/v1/system/route_maps/<id>`.
5. Validate the GET method HTTP return code for `/rest/v1/system/route_maps/<id>` and its respective values.

### Test result criteria
#### Test pass criteria
This test case passes if the standard REST API GET method returns HTTP code `200 OK` for the URI `/rest/v1/system/route_maps/<id>` and the returned data is identical.

#### Test fail criteria
This test case fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI `/rest/v1/system/route_maps/<id>`.

## REST API get method for interfaces
### Objective
The objective of the test case is to validate the `/rest/v1/system/interfaces` through the standard REST API GET method.

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
The test case validates the `/rest/v1/system/interfaces` through the standard REST API GET method.

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.
4. Execute the Standard REST API GET Method for URI `/rest/v1/system/interfaces`.
5. Validate the GET method HTTP return code for `/rest/v1/system/interfaces` and its respective values.

### Test result criteria
#### Test pass criteria
The test case passes if the standard REST API GET method returns HTTP code `200 OK` for the URI `/rest/v1/system/interfaces` and the returned data is identical.

#### Test fail criteria
The test case is fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI `/rest/v1/system/interfaces`.

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

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology
diagram.
2. Configure the IPV4 address on the switch management interfaces.
3. Configure the IPV4 address on the Ubuntu workstation.

##### Test 1

1. Execute the GET method for URI `/login` while not logged in.
2. Validate that the GET method HTTP return code is `401 UNAUTHORIZED`.

##### Test 2

1. Execute the standard REST API POST method for URI `/login` with valid
credentials.
2. Validate that the POST method HTTP return code is `200 OK`.
3. Execute the GET method for URI `/login` using the cookie returned in the
POST's response.
4. Validate that the GET method HTTP return code for URI `/login` is `200 OK`.

##### Test 3

1. Execute the standard REST API POST method for URI `/login` with a correct
user but wrong password.
2. Validate that POST method HTTP return code is `401 UNAUTHORIZED`.

##### Test 4

1. Execute the standard REST API POST method for URI `/login` with a
non-existent user.
2. Validate that the POST method HTTP return code is `401 UNAUTHORIZED`.

##### Test 5

1. Execute the standard REST API POST method for URI `/login` with a user that
does have `READ_SWITCH_CONFIG` or `WRITE_SWITCH_CONFIG` permissions.
2. Validate that the POST method HTTP return code is `401 UNAUTHORIZED`.

### Test result criteria
#### Test pass criteria
- Test 1: the HTTP return code for the GET method on `/login` is `401 UNATHORIZED`.
- Test 2: the HTTP return code for the POST method on `/login` is `200 OK`, and
the HTTP return code for the GET method on `/login` is also `200 OK`.
- Test 3: the HTTP return code for the POST method on `/login` is `401 UNATHORIZED`.
- Test 4: the HTTP return code for the POST method on `/login` is `401 UNATHORIZED`.
- Test 5: the HTTP return code for the POST method on `/login` is `401 UNATHORIZED`.

#### Test fail criteria
- Test 1: the HTTP return code for the GET method on `/login` is not `401 UNATHORIZED`.
- Test 2: the HTTP return code for the POST method on `/login` is not `200 OK`,
and the HTTP return code for the GET method on `/login` is also not `200 OK`.
- Test 3: the HTTP return code for the POST method on `/login` is not `401 UNATHORIZED`.
- Test 4: the HTTP return code for the POST method on `/login` is not `401 UNATHORIZED`.
- Test 5: the HTTP return code for the POST method on `/login` is not `401 UNATHORIZED`.

## REST API method access

### Objective
The objective of the test case is to validate that REST methods (`GET`, `POST`,
`PUT`, `PATCH`, and `DELETE`) are restricted based on the user's permissions.

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

For testing purposes, a fixture function is executed for all tests described,
to obtain base test data from the default port and create a test port. This
base test data and test port are used later on each test to either create
another test port, or attempt to delete or modify the test port. The setup
steps for this are as follows:

1. Query the default port `/rest/v1/system/ports/bridge_normal` and save the
result as the base port data, to be available for all tests.
2. Modify the base port data, changing the port's name to `test_port`, and
create a new port with this data.
3. Upon test finalization, using the fixture's finalizer function, the test
port is deleted.

### Description

This test validates that REST methods (`GET`, `POST`, `PUT`, `PATCH`, and
`DELETE`) are restricted based on the user's permissions. Currently there are
only two permissions that allow a user to login and use REST: `READ_SWITCH_CONFIG`
and `WRITE_SWITCH_CONFIG`. These permissions map to REST methods as follows:

- `READ_SWITCH_CONFIG`: `GET`
- `WRITE_SWITCH_CONFIG`: `POST`, `PUT`, `PATCH`, `DELETE`

So, for example, if a user does not have the `WRITE_SWITCH_CONFIG`, they can't
execute a POST operation.

The following tests are performed while the default user `netop` is logged in:

1. Verify if the user can execute a POST command.
    a. Execute a POST command over `/rest/v1/system/ports`, using the base port
    data and naming the port `my_test_port`.
    b. Verify if the HTTP response is `201 CREATED`.

2. Verify if the user can execute a PUT command.
    a. Execute a PUT command over `/rest/v1/system/ports/test_port`, adding a
    `test` key with value `test` to the `other_config` column.
    b. Verify if the HTTP response is `200 OK`.

3. Verify if the user can execute a PATCH command.
    a. Execute a PATCH command over `/rest/v1/system/ports/test_port`, using
    the following PATCH data:

    ```
        [{"op": "add", "path": "/other_config", "value": {}},
         {"op": "add", path": "/other_config/patch_test", "value": "test"}]
    ```

    b. Verify if the HTTP response is `204 NO CONTENT`.

4. Verify if the user can execute a GET command.
    a. Execute a GET command over `/rest/v1/system/ports/test_port`.
    b. Verify if the HTTP response is `200 OK`.

5. Verify if the user can execute a DELETE command.
    a. Execute a DELETE command over `/rest/v1/system/ports/test_port`.
    b. Verify if the HTTP response is `204 NO CONTENT`.

6. Verify if the user can execute a GET command for the full-configuration
   resource.
    a. Execute a GET command over `/rest/v1/system/full-configuration`.
    b. Verify if the HTTP response is `200 OK`.

7. Verify if the user can execute a PUT command for the full-configuration
   resource.
    a. Execute a PUT command over `/rest/v1/system/full-configuration`, using
    the following data:

    ```
        {
            "System": {
                "hostname": "",
                "asset_tag_number": ""
            }
        }
    ```

    b. Verify if the HTTP response is `200 OK`.

8. Verify if the user can execute a GET command for the logs resource.
    a. Execute a GET command over `/rest/v1/logs`.
    b. Verify if the HTTP response is `200 OK`.

The following tests are intended to test the restriction of REST's methods
based on lack of permissions, while the `admin` user is logged in. However,
currently, REST allows authentication only for users with `READ_SWITCH_CONFIG`
and `WRITE_SWITCH_CONFIG` permissions; at the time of this writing, the only
user with either of these permissions is `netop`, which actually has both, so
you can't essentially test that a user without one of them can't execute a
method not allowed by the permission. Therefore, these tests are disabled in
production. In order to test the restriction is actually working, you have to
build a version of REST that would allow the `admin` user to authenticate (i.e.
by adding `SYS_MGMT` to the list of allowed permissions to login), re-enable
these tests, and run them locally, as the `admin` user does not currently have
either of the allowed permissions for executing REST methods. This is necessary
until there exists, by default, a user that would be allowed to authenticate
while having a different set of permissions that serves testing purposes.

9. Verify if the user can execute a POST command.
    a. Execute a POST command over `/rest/v1/system/ports`, using the base port
    data and naming the port `my_test_port`.
    b. Verify if the HTTP response is `403 FORBIDDEN`.

10. Verify if the user can execute a PUT command.
    a. Execute a PUT command over `/rest/v1/system/ports/test_port`, adding a
    `test` key with value `test` to the `other_config` column.
    b. Verify if the HTTP response is `403 FORBIDDEN`.

11. Verify if the user can execute a PATCH command.
    a. Execute a PATCH command over `/rest/v1/system/ports/test_port`, using
    the following PATCH data:

    ```
        [{"op": "add", "path": "/other_config", "value": {}},
         {"op": "add", path": "/other_config/patch_test", "value": "test"}]
    ```

    b. Verify if the HTTP response is `403 FORBIDDEN`.

12. Verify if the user can execute a GET command.
    a. Execute a GET command over `/rest/v1/system/ports/test_port`.
    b. Verify if the HTTP response is `403 FORBIDDEN`.

13. Verify if the user can execute a DELETE command.
    a. Execute a DELETE command over `/rest/v1/system/ports/test_port`.
    b. Verify if the HTTP response is `403 FORBIDDEN`.

14. Verify if the user can execute a GET command for the full-configuration
    resource.
    a. Execute a GET command over `/rest/v1/system/full-configuration`.
    b. Verify if the HTTP response is `403 FORBIDDEN`.

15. Verify if the user can execute a PUT command for the full-configuration
    resource.
    a. Execute a PUT command over `/rest/v1/system/full-configuration`, using
    the following data:

    ```
        {
            "System": {
                "hostname": "",
                "asset_tag_number": ""
            }
        }
    ```

    b. Verify if the HTTP response is `403 FORBIDDEN`.

16. Verify if the user can execute a GET command for the logs resource.
    a. Execute a GET command over `/rest/v1/logs`.
    b. Verify if the HTTP response is `403 FORBIDDEN`.

### Test result criteria
#### Test pass criteria

For tests executed while the `netop` user is logged in, the tests pass if the
following status codes are received per method:

- `GET`: `200 OK`
- `POST`: `201 CREATED`
- `PUT`: `200 OK`
- `PATCH`: `204 NO CONTENT`
- `DELETE`: `204 NO CONTENT`

For tests executed while the `admin` user is logged in, the tests pass if
`403 FORBIDDEN` is received as status code for all methods.

#### Test fail criteria

For tests executed while the `netop` user is logged in, the tests fail if the
following status codes are not received per method:

- `GET`: `200 OK`
- `POST`: `201 CREATED`
- `PUT`: `200 OK`
- `PATCH`: `204 NO CONTENT`
- `DELETE`: `204 NO CONTENT`

For tests executed while the `admin` user is logged in, the tests pass if
`403 FORBIDDEN` is not received as status code for all methods.

## REST API user account management

### Objective
The objective of this test case is to validate REST user account management for
self-password change and user permissions query through the `/account` resource.

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

This test case validates REST's `/account` resource's ability to change the
currently logged in user's password, through a PUT request, and query their
role and permissions, through a GET request.
Unless otherwise stated, the default user `netop` (password: `netop`) is logged
in, and the correct Cookie header is used for each request.

1. Verify the user can't change their own password when supplying a wrong
   current password.
    a. Execute a PUT request over `/account`, supplying an incorrect current
    password in the request body:

    ```
        {
            "configuration":
            {
                "password": "wrongpassword",
                "new_password": "newpassword"
            }
        }
    ```

    b. Verify if the HTTP status code is `401 UNAUTHORIZED`.

2. Verify the user can't change their own password when not supplying their
   current password.
    a. Execute a PUT request over `/account`, omitting the current password in
    the request body:

    ```
        {
            "configuration":
            {
                "new_password": "newpassword"
            }
        }
    ```

    b. Verify if the HTTP status code is `400 BAD REQUEST`.

3. Verify the user can't change their own password when not supplying a new
   password.
    a. Execute a PUT request over `/account`, omitting the new password in the
    request body:

    ```
        {
            "configuration":
            {
                "password": "netop"
            }
        }
    ```

    b. Verify if the HTTP status code is `400 BAD REQUEST`.

4. Verify the user can't change their own password when not logged in.
    a. Execute a PUT request over `/account`, without supplying a Cookie header,
    using the following data:

    ```
        {
            "configuration":
            {
                "password": "netop",
                "new_password": "newpassword"
            }
        }
    ```

    b. Verify if the HTTP status code is `401 UNAUTHORIZED`.

5. Verify a successful password change for the currently logged in user.
    a. Execute a PUT request over `/account`, using the following data:

    ```
        {
            "configuration":
            {
                "password": "netop",
                "new_password": "newpassword"
            }
        }
    ```

    b. Verify if the HTTP status code is `200 OK`.
    c. Using the cookie header from the PUT request, execute a GET request over
    `/account`
    d. Verify if the HTTP status code is `200 OK`

6. Verify the user's role and permissions can be queried while logged in.
    a. Execute a GET request over `/account`.
    b. Verify if the HTTP status code is `200 OK`
    c. Verify if the user's role is present in the response and it corresponds
    to `ops_netop`.
    d. Verify if the user's permissions are present in the response and that
    they include `READ_SWITCH_CONFIG` and `WRITE_SWITCH_CONFIG` permissions.

7. Verify the user's role and permission can't be queried while not logged in.
    a. Execute a GET request over `account`, without supplying a Cookie header.
    b. Verify if the HTTP status code is `401 UNAUTHORIZED`.

### Test result criteria
#### Test pass criteria

The test passes by meeting the following criteria for each sub test:

1. When using a wrong current password, a `401 UNAUTHORIZED` HTTP status code
is received.
2. When not supplying the user's current password, a `400 BAD REQUEST` HTTP
status code is received.
3. When not supplying a new current password, a `400 BAD REQUEST` HTTP status
code is received.
4. When attempting to change the password while not logged in, a `401 UNAUTHORIZED`
HTTP status code is received.
5. When logged in and while supplying all correct information, a `200 OK` HTTP
status code is received.
6. When logged in and the user's role and permissions are queried, a `200 OK`
HTTP status code is recieved and the user's role and permissions are the
expected ones.
7. When not logged in and the user's role and permissions are queried, a
`401 UNAUTHORIZED` HTTP status code is received.

#### Test fail criteria

The test fails for the following reasons for each sub test:

1. When using a wrong current password, other than `401 UNAUTHORIZED` HTTP
status code is received.
2. When not supplying the user's current password, other than `400 BAD REQUEST`
HTTP status code is received.
3. When not supplying a new current password, other than `400 BAD REQUEST` HTTP
status code is received.
4. When attempting to change the password while not logged in, other than
`401 UNAUTHORIZED` HTTP status code is received.
5. When logged in and while supplying all correct information, other than `200 OK`
HTTP status code is received.
6. When logged in and the user's role and permissions are queried, other than
`200 OK` HTTP status code is recieved or the user's role and permissions are
not the expected ones.
7. When not logged in and the user's role and permissions are queried, other
than `401 UNAUTHORIZED` HTTP status code is received.

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
4. Execute Standard REST API PUT method for URI `/rest/v1/system` - 1st test case.
5. Execute Standard REST API GET method for URI `/rest/v1/system` - 2nd test case.

### Test result criteria
#### Test pass criteria
- The first test passes if the standard REST API PUT method returns HTTP code `200 OK` for the URI `/rest/v1/system`.
- The second test passes if the standard REST API GET method returns HTTP code `200 OK` for the URI `/rest/v1/system` and the returned data is identical to the data used for the PUT.

#### Test fail criteria
- The first test fails if the standard REST API PUT method does not return HTTP code `200 OK` for the URI `/rest/v1/system`.
- The second test fails if the standard REST API GET method does not return HTTP code `200 OK` for the URI `/rest/v1/system` or the returned data is not identical to the data used for PUT.

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
    a. Execute the GET request over `/rest/v1/system/ports`.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has at least one element.
    d. Ensure that URI `/rest/v1/system/ports/Port1` is in the response data.

2. Verify if a specific port exists.
    a. Execute GET request over `rest/v1/system/ports/Port1`.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm if the response data is not empty.
    d. Ensure that the response data has the keys: "configuration", "status" and "statistics".
    e. Verify if the configuration data is equal to the Port1 configuration data.

3. Verify if a non-existent port exists.
    a. Execute the GET request over `rest/v1/system/ports/Port2`.
    b. Verify if the HTTP response is `404 NOT FOUND`.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying a port list for:
    - A `200 OK` HTTP response.
    - At least one port in the port list.
    - A URI `rest/v1/system/ports/Port1` in the port list returned from the  `rest/v1/system/ports` URI.

- Querying Port1 for:
    - An HTTP response of `200 OK` when doing a GET request over `rest/v1/system/ports/Port1`.
    - A response data that is not empty.
    - A response data that contains keys: "configuration", "status", and "statistics".
    - Preset port configuration data that is equal to Port1.

- Querying for an HTTP response of `404 NOT FOUND` on a non-existent port.

#### Test fail criteria

This test fails when:

- Querying a post list for:
    - An HTTP response is not equal to `200 OK`.
    - A GET request to `rest/v1/system/ports` and "Port1" is in the Ports URI list.

- Performing a GET request over `rest/v1/system/ports/Port1` and the HTTP response is not equal to `404 NOT FOUND` for Port1.

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

1. Execute a POST request with `/rest/v1/system/ports` and with the following data and verify if the HTTP response is `201 CREATED`.

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

2. Execute a GET request with `/rest/v1/system/ports/Port1` and verify if the response is `200 OK`.
3. Verify that the configuration response data from Step 2 is the same as the configuration data from Step 1.

#### Create an existing port
Verify that the HTTP response returns `400 BAD REQUEST` HTTP response when creating a existing port with the name "Port1".

1. Execute a POST request with `/rest/v1/system/ports,` and with the name "Port1": `"name": "Port1"`.
2. Confirm that the HTTP response is `400 BAD REQUEST`.

#### Data validation

##### Data types validation

###### Invalid string type

1. Set the "ip4_address" value to: `"ip4_address": 192`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid string type

1. Set the "ip4_address" value to: `"ip4_address": "192.168.0.1"`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

###### Invalid integer type

1. Set the "tag" value to: `"tag": "675"`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid integer type

1. Set the "tag" value to: `"tag": 675`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

###### Invalid array type

1. Set the "trunks" value to: `"trunks": "654,675"`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid array type

1. Set the "trunks" value to: `"trunks": [654,675]`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

##### Ranges validation

###### Invalid range for string type

1. Set the "ip4_address" value to: `"ip4_address": "175.167.134.123/248"`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for string type

1. Set the "ip4_address" value to: `"ip4_address": "175.167.134.123/24"`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

###### Invalid range for integer type

1. Set the "tag" value to: `"tag": 4095`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for integer type

1. Set the "tag" value to: `"tag": 675`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
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

2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for array type

1. Change the "interfaces" value to: `"interfaces": ["/rest/v1/system/interfaces/1"]`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

##### Allowed data values validation


###### Invalid data value

1. Change the "vlan_mode" value to: `"vlan_mode": "invalid_value"`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid data value

1. Change the "vlan_mode" value to: `"vlan_mode": "access"`.
2. Execute a POST request with `/rest/v1/system/ports` and with the port data changed.
3. Verify that the HTTP response is `201 CREATED`.

##### Missing attribute validation

1. Execute a POST request with `/rest/v1/system/ports` and without the "vlan_mode" attribute.
2. Verify that the HTTP Response is `400 BAD REQUEST`.
3. Execute a POST request with `/rest/v1/system/ports` and with all the attributes.
4. Verify that the HTTP Response is `201 CREATED`.

##### Unknown attribute validation

1. Execute a POST request with `/rest/v1/system/ports` and with an unknown attribute as follows: `"unknown_attribute": "unknown_value"`.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a POST request with `/rest/v1/system/ports` and with all allowed attributes.
4. Verify that the HTTP Response is `201 CREATED`.

##### Malformed json validation

1. Execute a POST request with `/rest/v1/system/ports` and with a semi-colon at the end of the json data.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a POST request with `/rest/v1/system/ports` and without the semi-colon at the end of the json data.
4. Verify that the HTTP response is `201 CREATED`.


### Test result criteria
#### Test pass criteria

The test is passing for "creating a new port" when the following results occur:

- The HTTP response is `200 OK`.
- The HTTP response is `200 OK` when executing a GET request with `/rest/v1/system/ports/Port1`.
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
- Executing a GET request with `/rest/v1/system/ports/Port1` the HTTP response is not equal to `200 OK`.
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

1. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the following data. Verify that the HTTP response is `200 OK`.

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

2. Execute a GET request with `/rest/v1/system/ports/Port1` and verify that the response is `200 OK`.
3. Confirm that the configuration response data from Step 2 is the same as the configuration data from Step 1.

#### Update port using If-Match
1. Execute a GET request with `/rest/v1/system/ports/Port1` and verify that the response is `200 OK`.
2. Read the entity tag provided by the server
3. Set the "tag" value to: `"tag": 601`.
4. Execute a PUT request with `/rest/v1/system/ports/Port1` including and If-Match Header using entity tag read at step 2.
5. Verify that the response is `200 OK`.
6. Confirm that tag value was updated.

#### Update port using If-Match (star as etag)
1. Set the "tag" value to: `"tag": 602`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` including an If-Match Header using '"*"' as entity tag
3. Verify that the response is `200 OK`.
4. Confirm that tag value was updated.

#### Update port using If-Match change applied
1. Execute a GET request with `/rest/v1/system/ports/Port1` and verify that the response is `200 OK`.
2. Read the entity tag provided by the server
3. Execute a PUT request with `/rest/v1/system/ports/Port1` including and If-Match Header using entity tag different than the one read at step 2.
4. Verify that the response is `204 NO CONTENT`.

#### Update port using If-Match Precondition Failed
1. Execute a GET request with `/rest/v1/system/ports/Port1` and verify that the response is `200 OK`.
2. Read the entity tag provided by the server.
3. Set the "tag" value to: `"tag": 603`.
4. Execute a PUT request with `/rest/v1/system/ports/Port1` including and If-Match Header using entity tag different than the one read at step 2.
5. Verify that the response is 412 PRECONDITION FAILED.


#### Update port name

1. Set the name of the port to "Port2": `"name": "Port2"`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1`.
3. Verify that the HTTP response is `200 OK`.
4. Execute a GET request with `/rest/v1/system/ports/Port1` and verify that the response is `200 OK`.
5. Confirm that the port is still named "Port1".

#### Data validation

##### Data types validation

###### Invalid string type

1. Set the "ip4_address" value to: `"ip4_address": 192`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid string type

1. Set the "ip4_address" value to: `"ip4_address": "192.168.0.1"`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify if the HTTP response is `200 OK`.

###### Invalid integer type

1. Set the "tag" value to: `"tag": "675"`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid integer type

1. Set the "tag" value to: `"tag": 675`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

###### Invalid array type

1. Set the "trunks" value to: `"trunks": "654,675"`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid array type

1. Set the "trunks" value to: `"trunks": [654,675]`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

##### Ranges Validation

###### Invalid range for string type

1. Set the "ip4_address" value to: `"ip4_address": "175.167.134.123/248"`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for string type

1. Set the "ip4_address" value to: `"ip4_address": "175.167.134.123/24"`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

###### Invalid range for integer type

1. Set the "tag" value to: `"tag": 4095`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid range for integer type

1. Set the "tag" value to: `"tag": 675`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
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

2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

##### Valid range for array type

1. Change the "interfaces" value to: `"interfaces": ["/rest/v1/system/interfaces/1"]`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

##### Allowed data values validation


###### Invalid data value

1. Change the "vlan_mode" value to: `"vlan_mode": "invalid_value"`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `400 BAD REQUEST`.

###### Valid data value

1. Change the "vlan_mode" value to: `"vlan_mode": "access"`.
2. Execute a PUT request with `/rest/v1/system/ports/Port1` and with the port data changed.
3. Verify that the HTTP response is `200 OK`.

##### Missing attribute validation

1. Execute a PUT request with `/rest/v1/system/ports/Port1` and without the "vlan_mode" attribute.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a PUT request over `/rest/v1/system/ports/Port1` with all the attributes.
4. Confirm that the HTTP response is `200 OK`.

##### Unknown attribute validation

1. Execute a PUT request with `/rest/v1/system/ports/Port1` and with an unknown attribute: `"unknown_attribute": "unknown_value"`.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a PUT request with `/rest/v1/system/ports/Port1` and with all allowed attributes.
4. Verify that the HTTP response is `200 OK`.

##### Malformed json validation

1. Execute a PUT request with `/rest/v1/system/ports/Port1` and with a semi-colon at the end of the json data.
2. Verify that the HTTP response is `400 BAD REQUEST`.
3. Execute a PUT request with `/rest/v1/system/ports/Port1` and without the semi-colon at the end of the json data.
4. Verify that the HTTP response is `200 OK`.

### Test result criteria
#### Test pass criteria

The test is passing for "updating a port" when the following results occur:

- The HTTP response is `200 OK`.
- The HTTP response is `200 OK` when executing a GET request with `/rest/v1/system/ports/Port1`.
- The configuration data posted is the same as that of the retrieved port.

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
- The HTTP response is not equal to `200 OK` when executing a GET request with `/rest/v1/system/ports/Port1`.
- The configuration data posted is not the same as the data on the retrieved port.

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

1. Execute a DELETE request on  `/rest/v1/system/ports/Port1` and verify that the HTTP response is `204 NOT CONTENT`.
2. Execute a GET request on `/rest/v1/system/ports` and verify that the port is being deleted from the port list.
3. Execute a GET request on `/rest/v1/ports/system/Port1` and verify that the HTTP response is `404 NOT FOUND`.
4. Execute a DELETE request on `/rest/v1/system/ports/Port2` and ensure that the  HTTP response is `404 NOT FOUND`.

### Test result criteria

#### Test pass criteria

The test is passing for "deleting an existing port" when the following occurs:

- The HTTP response is `204 NOT CONTENT`.
- There is no URI `/rest/v1/system/ports/Port1` in the port list that is returned from the `/rest/v1/system/ports` URI.
- When doing a GET request on `/rest/v1/system/ports/Port1`, the HTTP response is `404 NOT FOUND`.
- There is no URI `/rest/v1/system/ports/Port1` in the port list that is returned from the `/rest/v1/system/ports` URI.
- When doing a GET request on `/rest/v1/system/ports/Port1`, the HTTP response is `404 NOT FOUND`.

The test case is passing for "deleting a non-existent" port when the HTTP response is `404 NOT FOUND`.

#### Test fail criteria

The test is passing for "deleting an existing port" when the following occurs:

- The HTTP response is not equal to `204 NOT CONTENT`.
- When performing a GET request on `/rest/v1/system/ports`, "Port1" is displayed in the ports URI list.
- The HTTP response is not equal to `404 NOT FOUND` when doing a GET request on `/rest/v1/system/ports/Port1`.

The test case is failing for "deleting a non-existent port" when the HTTP response is not equal to `404 NOT FOUND`.

## REST API get method with recursion for interfaces

### Objective
The test case verifies queries for:

- All interfaces with depth equals zero
- All interfaces with no depth parameter
- A specific interface with depth equals one
- A specific interface with depth equals two
- A specific interface with depth equals to the max depth value (10)
- A specific interface with negative depth value
- A specific interface with string depth value
- An interface with specific URI with depth equals one
- An interface with specific URI with depth equals two
- An interface with specific URI with negative depth value
- An interface with specific URI with string depth value
- An interface with specific URI with depth equals zero
- An interface with specific URI with no depth parameter
- An interface with specific URI and depth out of range

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
Depth valid values are integer numbers between 0 and 10 inclusive.

1. Verify if returns a list of interface URIs by using depth equals zero.
    a. Execute the GET request over `/rest/v1/system/interfaces?depth=0`.
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned interface list has at least one element.
    d. Ensure that URI `/rest/v1/system/interfaces/50` is in the response data.

2. Verify if returns a list of interface URIs by not using depth parameter.
    a. Execute the GET request over `/rest/v1/system/interfaces`
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned interface list has at least one element.
    d. Ensure that URI `/rest/v1/system/interfaces/50` is in the response data.

3. Verify if returns an interface and first level data.
    a. Execute the GET request over `/rest/v1/system/interfaces?depth=1;name=50-1`
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Ensure that inner data has the URI `/rest/v1/system/interfaces/50` in the response data.

4. Verify if returns an interface and second level data.
    a. Execute the GET request over `/rest/v1/system/interfaces?depth=2;name=50-1`
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Validate the second level depth returned interface object has Configuration, Statistics and Status keys present.
    e. Ensure that second level of depth inner data has the URIs `/rest/v1/system/interfaces/50-<1-4>` in the response data.

5. Verify if returns an interface by using depth equals to the max depth value.
    a. Execute a GET request over `/rest/v1/system/interfaces?depth=10;name=50-1` and specific URI `/rest/v1/system/interfaces/50-1?depth=10`
    b. Verify if the HTTP response for both requests is `200 OK`.
    c. Validate the response data to ensure the integrity.

6. Verify if response has a `400 BAD REQUEST` HTTP response status code by using a depth value major than the max depth value.
    a. Execute the GET request over `/rest/v1/system/interfaces?depth=<100, 1000>`
    b. Verify if the HTTP response is `400 BAD REQUEST`.

7. Verify if response has a `400 BAD REQUEST` HTTP response status code by using a negative depth value.
    a. Execute the GET request over `/rest/v1/system/interfaces?depth=-1`
    b. Verify if the HTTP response is `400 BAD REQUEST`.

8. Verify if response has a `400 BAD REQUEST` HTTP response status code by using a string depth value.
    a. Execute the GET request over `/rest/v1/system/interfaces?depth=<a, one, *>`
    b. Verify if the HTTP response is `400 BAD REQUEST`.

9. Verify if returns an interface with specific URI and data in first level of depth.
    a. Execute the GET request over `/rest/v1/system/interfaces/50-1?depth=1`
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Ensure that inner data has the URI `/rest/v1/system/interfaces/50` in the response data.

10. Verify if returns an interface with specific URI and data in second level of depth.
    a. Execute the GET request over `/rest/v1/system/interfaces/50-1?depth=2`
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Validate the second level depth returned interface object has Configuration, Statistics and Status keys present.
    e. Ensure that second level of depth inner data has the URIs `/rest/v1/system/interfaces/50-<1-4>` in the response data.

11. Verify if returns a `400 BAD REQUEST` HTTP response status code by using a negative depth value with an specific URI.
    a. Execute the GET request over `/rest/v1/system/interfaces/50-1?depth=-1`
    b. Verify if the HTTP response is `400 BAD REQUEST`.

12. Verify if returns a `400 BAD REQUEST` HTTP response status code by using a string depth value with an specific URI.
    a. Execute the GET request over `/rest/v1/system/interfaces/50-1?depth=a`
    b. Verify if the HTTP response is `400 BAD REQUEST`.

13. Verify if returns an interface with specific URI by using depth equals zero.
    a. Execute the GET request over `/rest/v1/system/interfaces/50-1?depth=0`
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Ensure that inner data has the URI `/rest/v1/system/interfaces/50` in the response data.

14. Verify if returns an interface with specific URI by not using depth parameter.
    a. Execute the GET request over `/rest/v1/system/interfaces/50-1`
    b. Verify if the HTTP response is `200 OK`.
    c. Validate the first level depth returned interface object has Configuration, Statistics and Status keys present.
    d. Ensure that inner data has the URI `/rest/v1/system/interfaces/50` in the response data.

15. Verify if returns an interface with specific URI by using a depth value equal to 11 (value out of range).
    a. Execute the GET request over `/rest/v1/system/interfaces/50-1?depth=11`
    b. Verify if the HTTP response is `400 BAD REQUEST`.

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

## REST API get method with filtering for ports

### Objective
The test case verifies:

1. Query all ports filtering by name.
2. Query all ports filtering by name with invalid criteria.
3. Query all ports filtering by multiple valid filters with valid criteria.
4. Query all ports filtering by name but without the depth parameter.
5. Query all ports filtering with complex filter mac.
6. Query all ports filtering by interfaces.
7. Query all ports filtering by trunks.
8. Query all ports filtering by primary ip4 address.
9. Query all ports filtering by secondary ip4 address.
10. Query all ports filtering by lacp.
11. Query all ports filtering by bond mode.
12. Query all ports filtering by bond active slave.
13. Query all ports filtering by tag.
14. Query all ports filtering by vlan mode.
15. Query all ports filtering by mac.
16. Query all ports filtering by ipv6 address.
17. Query all ports filtering by ipv6 secondary address.
18. Query all ports filtering by admin.


### Requirements

- Period after exist
- Depth is set to 1 in all queries

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

**Switch 1** has 10 ports (plus the default port named bridge_normal) with the name in the format PortN where N is a number between 1 and 10, each port has the following configuration data:

```
{
    "configuration": {
        "name": "Port-<1-10>",
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

1. Query all ports filtering by name.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;name=Port-<1-10>"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 1 element.
    d. Ensure the port in the list is 'Port-<1-10>'.

2. Query all ports filtering by name with invalid criteria.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;name=invalid_criteria"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 0 elements.

3. Query all ports with invalid filter and invalid criteria.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;invalid_filter=invalid_criteria"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

4. Query all ports filtering by name but without the depth parameter.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?name=Port-1"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

5. Query all ports filtering by complex filter mac.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?selector=configuration;depth=1;mac=01:23:45:67:89:<01-10>
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 10 elements.

6. Query all ports filtering by interfaces.
    a. Update Port-<1-3> by replacing the current interfaces value with `/rest/v1/system/interfaces/3`
    b. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;interfaces=/rest/v1/system/interfaces/3"
    c. Verify if the HTTP response is `200 OK`.
    d. Confirm that the returned port list has exactly 3 elements.
    e. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;interfaces=/rest/v1/system/interfaces/1"
    f. Verify if the HTTP response is `200 OK`.
    g. Confirm that the returned port list has exactly 7 elements.

7. Query all ports filtering by trunks.
    a. Update Port-1, Port-3 and Port-5 by replacing the current trunks value with `414`
    b. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;trunks=414"
    c. Verify if the HTTP response is `200 OK`.
    d. Confirm that the returned port list has exactly 3 elements.
    e. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;trunks=413"
    f. Verify if the HTTP response is `200 OK`.
    g. Confirm that the returned port list has exactly 7 elements.

8. Query all ports filtering by primary ipv4 address.
    a. Execute a GET request for each port over `/rest/v1/system/ports` with the following parameters : "?depth=1;ip4_address=192.168.0.<1-10>"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 1 element.

9. Query all ports filtering by secondary ipv4 address.
    a. Execute a GET request for each port over `/rest/v1/system/ports` with the following parameters : "?depth=1;ip4_address_secondary=192.168.0.<1-10>"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 1 element.

10. Query all ports filtering by lacp.
    a. Update Port-1 and Port-2 by replacing the current lacp value with `passive, off` respectively.
    b. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;lacp=passive;lacp=off"
    c. Verify if the HTTP response is `200 OK`.
    d. Confirm that the returned port list has exactly 2 elements.
    e. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;lacp=active"
    f. Verify if the HTTP response is `200 OK`.
    g. Confirm that the returned port list has exactly 8 elements.

11. Query all ports filtering by bond mode.
    a. Update Port-1, Port-2 and Port-3 by replacing the bond_mode value with `l3-src-dst-hash`
    b. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;bond_mode=l3-src-dst-hash"
    c. Verify if the HTTP response is `200 OK`.
    d. Confirm that the returned port list has exactly 3 elements.
    e. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;bond_mode=l2-src-dst-hash"
    f. Verify if the HTTP response is `200 OK`.
    g. Confirm that the returned port list has exactly 7 elements.

12. Query all ports filtering by bond active slave.
    a. Update Port-<1-5> by replacing the bond_active_slave value with `00:98:76:54:32:10`
    b. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;bond_active_slave=00:98:76:54:32:10"
    c. Verify if the HTTP response is `200 OK`.
    d. Confirm that the returned port list has exactly 5 elements.
    e. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;bond_active_slave=null"
    f. Verify if the HTTP response is `200 OK`.
    g. Confirm that the returned port list has exactly 5 elements.

13. Query all ports filtering by tag.
    a. Update Port-<1-5> by replacing the tag value with `123`
    b. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;tag=123"
    c. Verify if the HTTP response is `200 OK`.
    d. Confirm that the returned port list has exactly 5 elements.
    e. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;tag=654"
    f. Verify if the HTTP response is `200 OK`.
    g. Confirm that the returned port list has exactly 5 elements.

14. Query all ports filtering by vlan mode.
    a. Update Port-<1-3> by replacing the vlan_mode value with `["access", "native-tagged", "native-untagged"]`
    b. Execute a GET request for each vlan mode in the list over `/rest/v1/system/ports` with the following parameters: "?depth=1;vlan_mode=<mode>"
    c. Verify if the HTTP response is `200 OK`.
    d. Confirm that the returned port list has exactly 1 elements.
    e. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;vlan_mode=trunk"
    f. Verify if the HTTP response is `200 OK`.
    g. Confirm that the returned port list has exactly 7 elements.

15. Query all ports filtering by mac.
    a. Execute a GET request for each mac over `/rest/v1/system/ports` with the following parameters: "?depth=1;mac=01:23:45:67:89:<01-10>"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 1 element.

16. Query all ports filtering by ipv6 address.
    a. Execute a GET request for each ip6_address over `/rest/v1/system/ports` with the following parameters: "?depth=1;ip6_address=2001:0db8:85a3:0000:0000:8a2e:0370:00<01-10>"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 1 element.

17. Query all ports filtering by ipv6 address secondary.
    a. Execute a GET request for each ip6_address_secondary over `/rest/v1/system/ports` with the following parameters: "?depth=1;ip6_address=2001:0db8:85a3:0000:0000:8a2e:0371:00<01-10>"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 1 element.

18. Query all ports filtering by admin.
    a. Update Port-<1-5> by replacing the admin value with `down`
    b. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;admin=down"
    c. Verify if the HTTP response is `200 OK`.
    d. Confirm that the returned port list has exactly 5 elements.
    e. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;admin=up"
    f. Verify if the HTTP response is `200 OK`.
    g. Confirm that the returned port list has exactly 5 elements.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying a port list with the specified correct parameters in each step:
    - A `200 OK` HTTP response.
    - The correct number of ports is returned.

#### Test fail criteria

This test fails when:

- Querying a port list with the specified correct parameters in each step:
    - A `200 OK` HTTP response is not received.
    - An incorrect number of ports is returned.

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
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;sort=name;limit=5"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 5 elements.
    d. Ensure the first port in the list is 'bridge_normal', which means offset defaulted to 0.

2. Query all ports with no pagination limit set.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;sort=name;offset=91"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 10 elements.
    d. Ensure the first port in the list is 'Port90' and the last one is 'Port99, which means limit defaulted to the remainder size.

3. Query all ports with no pagination offset or limit set.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;sort=name"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 101 elements.

4. Query all ports with negative pagination offset set.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;sort=name;offset=-1;limit=10"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

5. Query all ports with negative pagination limit set.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;sort=name;offset=5;limit=-1"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

6. Query all ports with pagination offset set greater than data set's size.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;sort=name;offset=200"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

7. Query all ports with pagination offset + limit greater than data set's size.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;sort=name;offset=91;limit=20"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 10 elements.
    d. Ensure the first port in the list is 'Port90' and the last one is 'Port99, which means limit defaulted to the remainder size.

8. Query specific a port with only pagination offset set.
    a. Execute a GET request over `/rest/v1/system/ports/bridge_normal` with the following parameters: "?depth=1;offset=5"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

9. Query specific a port with only pagination limit set.
    a. Execute a GET request over `/rest/v1/system/ports/bridge_normal` with the following parameters: "?depth=1;limit=10"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

10. Query specific a port with both pagination offset and limit set.
    a. Execute a GET request over `/rest/v1/system/ports/bridge_normal` with the following parameters: "?depth=1;offset=0;limit=10"
    b. Verify if the HTTP response is `400 BAD REQUEST`.

11. Query first 10 ports using pagination indexes.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;sort=name;offset=0;limit=10"
    b. Verify if the HTTP response is `200 OK`.
    c. Confirm that the returned port list has exactly 10 elements.
    d. Ensure the first port in the list is 'bridge_normal' and the last one is 'Port16'.

12. Query last 10 ports using pagination indexes.
    a. Execute a GET request over `/rest/v1/system/ports` with the following parameters: "?depth=1;sort=name;offset=91;limit=10"
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

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;sort=<field_name>`
and verify that response is `200 OK`.
2. Verify if the result is being ordered by the provided field name.

Sort by allowed sort field (descending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;sort=-<field_name>`
and verify that response is `200 OK`.
2. Verify if the result is being ordered by the provided field name.

Sort by using invalid column (ascending and descending mode).

1. Execute a GET request on `/rest/v1/system/ports?depth=1;sort=invalid_column`
and verify that response is `400 BAD REQUEST`.

Sort without using depth parameter (ascending and descending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?sort=<field_name>`
and verify that response is `400 BAD REQUEST`.

Sort by allowed sort field and offset equal to zero (ascending and descending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;offset=0;sort=-<field_name>`
and verify that response is `200 OK`.
2. Verify if returned all the results.

Sort by allowed sort field and offset with invalid criteria (ascending and descending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;offset=one;sort=<field_name>`
and verify that response is `400 BAD REQUEST`.

Sort by allowed sort field and limit equal to ten (ascending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;name=Port-1,Port-2,
Port-3,Port-4,Port-5,Port-6,Port-7,Port-8,Port-9,Port-10;limit=10;sort=name`
and verify that response is `200 OK`.
2. Verify if returned 10 ports in the results.

Sort by allowed sort field and limit equal to ten (descending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;name=Port-1,Port-2,
Port-3,Port-4,Port-5,Port-6,Port-7,Port-8,Port-9,Port-10;limit=10;sort=-name`
and verify that response is `200 OK`.
2. Verify if returned 10 ports in the results.

Sort by allowed sort field and limit higher to ten (ascending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;name=Port-1,Port-2,
Port-3,Port-4,Port-5,Port-6,Port-7,Port-8,Port-9,Port-10;limit=11;sort=name`
and verify that response is `200 OK`.
2. Verify if returned 10 ports in the results.

Sort by allowed sort field and limit higher to ten (descending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;name=-Port-1,Port-2,
Port-3,Port-4,Port-5,Port-6,Port-7,Port-8,Port-9,Port-10;limit=11;sort=<field_name>`
and verify that response is `200 OK`.
2. Verify if returned 10 ports in the results.

Sort by allowed sort field and limit equal to zero (ascending and descending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;limit=0;sort=<field_name>`
and verify that response is `400 BAD REQUEST`.

Sort by allowed sort field with offset equal to 9 and limit to two (ascending a descending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;name=-Port-1,Port-2,
Port-3,Port-4,Port-5,Port-6,Port-7,Port-8,Port-9,Port-10;offset=9;limit=2;
sort=<field_name>` and verify that response is `200 OK`.
2. Verify if returned only one port in the result.

Sort by allowed sort field and limit equal to negative value (ascending and descending mode).

For each allowed sort field execute the following steps:

1. Execute a GET request on `/rest/v1/system/ports?depth=1;limit=-1;sort=<field_name>`
and verify that response is `400 BAD REQUEST`.

### Test result criteria

#### Test pass criteria

This test passes by meeting the following criteria:

- The HTTP response is `200 OK`.
- The response has all the expected amount of ports.
- The ports are sorted ascending/descending by the field name.

#### Test fail criteria

This test fails when:

- The HTTP response is not equal to `200 OK`.
- The response doesn't have expected amount of ports.
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

1. Execute a GET request on `/rest/v1/system/ports?depth=1;sort=admin,name` and verify that response is `200 OK`.
2. Verify if the result is being ordered by the provided fields. First by admin and the by name.

Sort by all available keys (Ascending mode)

1. Execute a GET request on `/rest/v1/system/ports?depth=1;sort=<all available keys>` and verify that response is `200 OK`.
2. Verify if the result is being ordered by all the provided fields.

Sort by admin and name (Descending mode)

1. Execute a GET request on `/rest/v1/system/ports?depth=1;sort=-admin,name` and verify that response is `200 OK`.
2. Verify if the result is being ordered by the provided fields. First by admin and the by name.

Sort by all available keys (Descending mode)

1. Execute a GET request on `/rest/v1/system/ports?depth=1;sort=-<all available keys>` and verify that response is `200 OK`.
2. Verify if the result is being ordered by all the provided fields.

### Test result criteria

#### Test pass criteria

This test passes by meeting the following criteria:

- The HTTP response is `200 OK`.
- The response has 10 ports.
- The result is sorted ascending/descending by the combination of fields.

Expected result when sort mode is ascending and provided fields are "admin,name":

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

Expected result when sort mode is descending and provided fields are "-admin,name":

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

## REST API get method with specific column retrieval for interfaces

### Objective
The test case verifies queries for:

- Single column retrieval
- Multiple column retrieval
- Column retrieval without depth argument
- Column retrieval with empty columns argument
- Column retrieval with nonexistent column key
- Column retrieval with filter
- Column retrieval with pagination
- Column retrieval with depth greater than one
- Column retrieval in requests other than GET
- Column retrieval with all applicable arguments
- Column retrieval by adding columns argument by separate

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

### Description
The test case validates if the interface list retrieved it shows only the data with the specified columns through the standard REST API GET method.

1. Verify if specific column retrieval is applied in the GET request by using the columns argument for a single column.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;depth=1;sort=name;columns=name`.
    b. Verify if the HTTP response is `200 OK`.
    c. Validate if the list of interfaces has the exact amount of columns specified in the request.
    d. Confirm that interface resource returned the expected data.

2. Verify if specific column retrieval is applied in the GET request by using the columns argument for multiple columns.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;depth=1;sort=name;columns=name,type`.
    b. Verify if the HTTP response is `200 OK`.
    c. Validate if the list of interfaces has the exact amount of columns specified in the request.
    d. Confirm that interface resource returned the expected data.

3. Verify if specific column retrieval is invalid in the GET request by using the columns argument and no depth argument.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;sort=name;columns=name`.
    b. Verify if the HTTP response is `400 BAD REQUEST`.

4. Verify if specific column retrieval is invalid in the GET request by using the columns argument and no value.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;depth=1;sort=name;columns=`.
    b. Verify if the HTTP response is `400 BAD REQUEST`.

5. Verify if specific column retrieval is invalid in the GET request by using the columns argument and nonexistent key.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;depth=1;sort=name;columns=foo`.
    b. Verify if the HTTP response is `400 BAD REQUEST`.

6. Verify if specific column retrieval is applied in the GET request by using the columns and filter arguments.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;depth=1;sort=name;name=10;columns=name,type`.
    b. Verify if the HTTP response is `200 OK`.
    c. Validate if the list of interfaces has the exact amount of columns specified in the request.
    d. Confirm that interface resource returned the expected data.

7. Verify if specific column retrieval is applied in the GET request by using the columns and pagination arguments.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;depth=1;sort=name;limit=10;offset=10;columns=name,type`.
    b. Verify if the HTTP response is `200 OK`.
    c. Validate if the list of interfaces has the exact amount of columns specified in the request.
    d. Confirm that interface resource returned the expected data.

8. Verify if specific column retrieval is applied in the GET request by using the columns argument and depth argument equals 2.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;depth=2;sort=name;columns=name,type`.
    b. Verify if the HTTP response is `200 OK`.
    c. Validate if the list of interfaces has the exact amount of columns specified in the request.
    d. Confirm that interface resource returned the expected data.

9. Verify if specific column retrieval is invalid in requests other than GET.
    a. Execute the POST, PUT and DELETE request over `/rest/v1/system/interfaces?selector=configuration;depth=1;sort=name;columns=name`.
    b. Verify if the HTTP response is `400 BAD REQUEST`.

10. Verify if specific column retrieval is applied in the GET request by using the columns argument in combination with filter, sort and pagination.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;depth=1;sort=name;name=10;limit=1;columns=name,type`.
    b. Verify if the HTTP response is `200 OK`.
    c. Validate if the list of interfaces has the exact amount of columns specified in the request.
    d. Confirm that interface resource returned the expected data.

11. Verify if specific column retrieval is applied in the GET request by using the columns argument more than once as separate arguments.
    a. Execute the GET request over `/rest/v1/system/interfaces?selector=configuration;depth=1;sort=name;columns=name;columns=type`.
    b. Verify if the HTTP response is `200 OK`.
    c. Validate if the list of interfaces has the exact amount of columns specified in the request.
    d. Confirm that interface resource returned the expected data.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Using the columns argument with the specified correct value and depth greater than zero in the request:
    - A `200 OK` HTTP response.

- Using the columns argument with invalid values or a nonexistent keys results in the request:
    - A `400 BAD REQUEST` HTTP response.

- Using the columns argument in requests other than GET:
    - A `400 BAD REQUEST` HTTP response.

#### Test fail criteria

This test fails when:

- Using the columns argument with the specified correct value and depth greater than zero in the request:
    - A `400 BAD REQUEST` HTTP response or anything other than `200 OK` HTTP RESPONSE.

- Using the columns argument with invalid values or a nonexistent keys results in the request:
    - A `200 OK` HTTP response or anything other than `400 BAD REQUEST` HTTP RESPONSE.

- Using the columns argument in requests other than GET:
    - A `200 OK` HTTP response or anything other than `400 BAD REQUEST` HTTP RESPONSE.

## REST API patch method for system

### Objective
The test case verifies queries for:

- Add operation to set a field with a new value
- Add operation to set a field with a new value and invalid ETag
- Add operation to replace a existing field
- Add operation to set a field with an array type value
- Add operation to aggregate an object member
- Add operation to aggregate an empty optional member
- Add operation to set a field value with a malformed patch
- Add operation to set a field with a boolean type value
- Add operation to set multiple fields
- Test operation to verify a nonexisting value
- Test operation to verify a field by using a malformed path value
- Test operation to verify an existent value
- Copy operation to duplicate an existing value
- Copy operation to duplicate a nonexistent value
- Move operation to change of place an existing value
- Move operation to change of place a nonexistent value
- Replace operation to set a new value for an existing field
- Replace operation to set a new value for a nonexistent value

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

### Description
The test case validates add, copy, remove, replace, copy and move and test operations through the standard REST API PATCH method. If-Match header is optional for the standard REST API PATCH method and it's used in these tests to verify whether a change was made or not by checking the ETag or entity tag identifier.

1. Verify if a patch is applied using the add operation for a new value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "add", "path": "/dns_servers", "value": ["1.1.1.1"]}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the new value added.
    d. Confirm that the ETag is changed.

2. Verify if a patch is applied using the add operation for a new value using an invalid ETag.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        headers = {"If-Match": "abcdefghijklmnopqrstuvwxyz12345678901234"}
        patch = [{"op": "add", "path": "/dns_servers", "value": ["1.1.1.1"]}]
    ```
    b. Verify if the HTTP response is `412 PRECONDITION FAILED`.
    c. Confirm that the ETag remains the same.

3. Verify if a patch is applied using the add operation to replace an existing field.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "add", "path": "/dns_servers", "value": ["1.1.1.1"]},
         {"op": "add", "path": "/dns_servers", "value": ["1.2.3.4"]}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the replace value added.
    d. Confirm that the ETag is changed.

4. Verify if a patch is applied using the add operation for an array element.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "add", "path": "/dns_servers", "value": ["1.1.1.1"]},
         {"op": "add", "path": "/dns_servers/1", "value": "1.2.3.4"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the new values added.
    d. Confirm that the ETag is changed.

5. Verify if a patch is applied using the add operation for a new object member.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "add", "path": "/logrotate_config/maxsize", "value": "20"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the new object `logrotate_config` and `maxsize`
    value added.
    d. Confirm that the ETag is changed.

5. Verify if a patch is applied using the add operation for an empty optional member.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "add", "path": "/other_config/foo", "value": "bar"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the new object and value added.
    d. Confirm that the ETag is changed.

6. Verify if a patch is applied using the add operation with a malformed patch.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"path": "/dns_servers", "value": ["1.1.1.1"]}]
    ```
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the ETag remains the same.

7. Verify if a patch is applied using the add operation for a boolean element.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "add", "path": "/other_config/enable-statistics", "value": "true"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the new values added.
    d. Confirm that the ETag is changed.

8. Verify if a patch is applied using the add operation for multiple fields.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "add", "path": "/other_config/enable-statistics", "value": "true"},
         {"op": "add", "path": "/dns_servers", "value": ["1.1.1.1"]},
         {"op": "add", "path": "/other_config/foo", "value": "bar"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the new values added.
    d. Confirm that the ETag is changed.

9. Verify if a patch is applied using the Test operation for a nonexistent value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "test", "path": "/other_config/foo", "value": "bar"}]
    ```
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the ETag remains the same.

10. Verify if a patch is applied using the Test operation with a malformed path value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration` by using the values in the list with the patch below: `['a/b', '/ab', 'ab/', 'a//b', 'a///b', 'a\\/b']`
    ```
        [{'path': '/other_config', 'value': {}, 'op': 'add'},
         {'path': '/other_config/<list[item]>', 'value': 'test data', 'op': 'add'},
         {'path': '/other_config/<list[item]>', 'value': 'test data', 'op': 'test'}]
    ```
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the ETag remains the same.

11. Verify if a patch is applied using the Test operation for an existent value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "add", "path": "/dns_servers", "value": "1.1.1.1"},
         {"op": "test", "path": "/dns_servers", "value": "1.1.1.1"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that the ETag is changed.

12. Verify if a patch is applied using the Copy operation with an existent value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "copy", "from": "/other_config/foo",
          "path": "/other_config/copy_of_foo"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the copied value.
    d. Confirm that the ETag is changed.

13. Verify if a patch is applied using the Copy operation with a nonexistent value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "copy", "from": "/other_config/foo",
          "path": "/other_config/copy_of_foo"}]
    ```
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the ETag remains the same.

14. Verify if a patch is applied using the Move operation with an existent value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "move", "from": "/dns_servers/0",
          "path": "/other_config/dns_servers"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the moved value.
    d. Confirm that the ETag is changed.

15. Verify if a patch is applied using the Move operation with a nonexistent value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "move", "from": "/other_config/servers",
          "path": "/other_config/dns_servers"}]
    ```
    b. Verify if the HTTP response is `400 BAD REQUEST`.

16. Verify if a patch is applied using the Move operation with an invalid path.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "move", "from": "/other_config/abc",
          "path": "/other_config/abc/def"}]
    ```
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the ETag remains the same.

17. Verify if a patch is applied using the Replace operation with an existent value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "replace", "path": "/other_config/test", "value": "bar"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource has the replaced value.
    d. Confirm that the ETag is changed.

18. Verify if a patch is applied using the Replace operation with a nonexistent value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "replace", "path": "/other_config/non_existent_field",
          "value": "bar"}]
    ```
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Confirm that the ETag remains the same.

19. Verify if a patch is applied using the Remove operation with an existent value.
    a. Execute the PATCH request over `/rest/v1/system?selector=configuration`.
    ```
        [{"op": "remove", "path": "/other_config/test"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Confirm that system resource does not have the removed value.
    d. Confirm that the ETag is changed.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Applying a Patch with the specified correct parameters in each step:
    - A `204 NO CONTENT` HTTP response.

- Applying a Patch with invalid parameters or a malformed patch results in a `400 BAD REQUEST`.

- Applying a Patch with invalid ETag results in `412 PRECONDITION FAILED`

#### Test fail criteria

This test fails when:

- Applying a Patch with the specified correct parameters in each step:
    - A `400 BAD REQUEST` HTTP response.

- Applying a Patch with invalid parameters or a malformed patch results in a `204 NO CONTENT`.

- Applying a Patch with invalid ETag results in `204 NO CONTENT`

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
    1. Execute the GET request over `/rest/v1/system/bridges`.
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the response data is not empty.
    4. Verify if `/rest/v1/system/bridges/bridge_normal` is returned within the response data.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Querying bridges for:
    - A `200 OK` HTTP response.
    - At least one bridge in the bridge list.
    - A URI `/rest/v1/system/bridges/bridge_normal` in the bridge list returned from the `/rest/v1/system/bridges` URI.

#### Test fail criteria

This test fails when:

- Querying a bridge for:
    - An HTTP response is not equal to `200 OK`
    - A GET request to `/rest/v1/system/bridges` and `/rest/v1/system/bridges/bridge_normal` is in the Bridges URI list.

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
    1. Execute the GET request over `/rest/v1/system/bridges/bridge_normal`.
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
    - A GET request to `rest/v1/system/bridges/bridge_normal` and the VLANs URI list is not empty.

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
    1. Execute the GET request over `/rest/v1/system/bridges/bridge_normal`.
    2. Verify if the HTTP response is `200 OK`.
    3. Verify if the HTTP response is not empty.
    4. Verify if `/rest/v1/system/bridges/bridge_normal/vlans/fake_vlan` is in the VLAN URI list.

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
    - A GET request to `rest/v1/system/bridges/bridge_normal` and `/rest/v1/system/bridges/bridge_normal/vlans/fake_vlan` is not within VLANs URI list.

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
    1. Execute the GET request over `/rest/v1/system/bridges/bridge_normal/vlans/fake_vlan`.
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
    - A GET request to `rest/v1/system/bridges/bridge_normal` and info about `/rest/v1/system/bridges/bridge_normal/vlans/fake_vlan` is not within the HTTP response.

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
    1. Execute the GET request over `/rest/v1/system/bridges/bridge_normal/vlans/not_found`.
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
    - A GET request to `rest/v1/system/bridges/bridge_normal/vlans/not_found` and there is at least one VLAN in the HTTP response.

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
    1. Execute the POST request over `/rest/v1/system/bridges/bridge_normal/vlans`.
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
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is an empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `201 CREATED`.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is an error in the HTTP response.

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
    1. Execute the POST request over `/rest/v1/system/bridges/bridge_normal/vlans` using each configuration.
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
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is no error in the HTTP response.

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
    1. Execute the POST request over `/rest/v1/system/bridges/bridge_normal/vlans` using each configuration.
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
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is no error in the HTTP response.

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
    1. Execute the POST request over `/rest/v1/system/bridges/bridge_normal/vlans` using each configuration.
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
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is no error in the HTTP response.

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
    1. Execute the POST request over `/rest/v1/system/bridges/bridge_normal/vlans` using each configuration.
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
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is no error in the HTTP response.

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
    1. Execute the POST request over `/rest/v1/system/bridges/bridge_normal/vlans` using each configuration.
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
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is no error in the HTTP response.

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
    1. Execute the POST request over `/rest/v1/system/bridges/bridge_normal/vlans` using each configuration.
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
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is no error in the HTTP response.

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
    1. Execute the POST request over `/rest/v1/system/bridges/bridge_normal/vlans` using each configuration.
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
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is no error in the HTTP response.

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
    1. Execute the POST request over `/rest/v1/system/bridges/bridge_normal/vlans` using the following configuration:

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
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is an empty HTTP response.

- Creating the same VLAN for:
    - An HTTP `400 BAD REQUEST` response.
    - A POST request to `/rest/v1/system/bridges/bridge_normal/vlans/` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Creating a VLAN for:
    - An HTTP response is not equal to 200 CREATED.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is an error in the HTTP response.

- Creating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A POST request to `rest/v1/system/bridges/bridge_normal/vlans/` and there is no error in the HTTP response.

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
    1. Execute the PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test` with the name field with "fake_vlan".
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
    - A PUT request to `rest/v1/system/bridges/bridge_normal/vlans/test` and the HTTP response is not empty.

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
    1. Execute the PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test` with each configuration.
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
    - A PUT request to `/rest/v1/system/bridges/bridge_normal/vlans/test` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to `rest/v1/system/bridges/bridge_normal/vlans/test` and there is no error in the HTTP response.

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
    1. Execute the PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test` with each configuration.
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
    - A PUT request to `/rest/v1/system/bridges/bridge_normal/vlans/test` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to `rest/v1/system/bridges/bridge_normal/vlans/test` and there is no error in the HTTP response.

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
    1. Execute the PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test` with each configuration.
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
    - A PUT request to `/rest/v1/system/bridges/bridge_normal/vlans/test` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to `rest/v1/system/bridges/bridge_normal/vlans/test` and there is no error in the HTTP response.

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
    1. Execute the PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test` using each configuration.
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
    - A PUT request to `/rest/v1/system/bridges/bridge_normal/vlans/test` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to `rest/v1/system/bridges/bridge_normal/vlans/test` and there is no error in the HTTP response.

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
    1. Execute the PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test` using each configuration.
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
    - A PUT request to `/rest/v1/system/bridges/bridge_normal/vlans/test` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to `rest/v1/system/bridges/bridge_normal/vlans/test` and there is no error in the HTTP response.

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
    1. Execute the PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test` using each configuration.
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
    - A PUT request to `/rest/v1/system/bridges/bridge_normal/vlans/test` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to `rest/v1/system/bridges/bridge_normal/vlans/test` and there is no error in the HTTP response.

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

1. Execute the PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test` with each configuration.
2. Verify if the HTTP response is `400 BAD REQUEST`.
3. Confirm that the HTTP response is not empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Updating VLANs for:
    - An HTTP `400 BAD REQUEST` response.
    - A PUT request to `/rest/v1/system/bridges/bridge_normal/vlans/test` and there is a non-empty HTTP response.

#### Test fail criteria

This test fails when:

- Updating a VLAN for:
    - An HTTP response is not equal to `400 BAD REQUEST`.
    - A PUT request to `rest/v1/system/bridges/bridge_normal/vlans/test` and there is no error in the HTTP response.

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
    1. Execute the DELETE request over `/rest/v1/system/bridges/bridge_normal/vlans/not_found`.
    2. Verify if the HTTP response is `404 NOT FOUND`.
    3. Verify if the HTTP response is empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- Deleting VLAN for:
    - An HTTP `404 NOT FOUND` response.
    - A DELETE request to `/rest/v1/system/bridges/bridge_normal/vlans/not_dounf` and there is a empty HTTP response.

#### Test fail criteria

This test fails when:

- Deleting VLAN for:
    - An HTTP response is not equal to `404 NOT FOUND`.
    - A DELETE request to `rest/v1/system/bridges/bridge_normal/vlans/not_found` and there is a non-empty HTTP response.

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
    1. Execute the GET request over `/rest/v1/system/bridges/bridge_normal/vlans?depth=1;name=Vlan-<number>` for each VLAN added.
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
 - A GET request to `rest/v1/system/bridges/bridge_normal/vlans?depth=1;name=Vlan-<number>` and the test VLAN is not within the HTTP response.

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
    1. Execute the GET request over `/rest/v1/system/bridges/bridge_normal/vlans?depth=1;id=<number>` for each VLAN added.
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
    - A GET request to `rest/v1/system/bridges/bridge_normal/vlans?depth=1;id=Vlan-<number>` and the test VLAN is not within the HTTP response.

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
    1. Execute the GET request over `/rest/v1/system/bridges/bridge_normal/vlans?depth=1;description=fake_vlan` for each VLAN modified.
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
    - A GET request to `rest/v1/system/bridges/bridge_normal/vlans?depth=1;description=fake_vlan` and the test VLANs are not within the HTTP response.

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
    1. Execute the GET request over `/rest/v1/system/bridges/bridge_normal/vlans?depth=1;admin=down` for each VLAN modified.
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
    - A GET request to `rest/v1/system/bridges/bridge_normal/vlans?depth=1;admin=down` and the test VLANs are not within the HTTP response.

## Update VLAN using If Match header with star Etag

### Objective
The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans/<id>` through the standard REST API PUT method using If-Match header with the field value `*`.

###  Requirements

- Bridge Normal exists.
- A test VLAN added.

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be added with the following configuration:

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

Verify if VLAN was updated successfully using If-Match header using value `*` as Etag:
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration`.
 2. Modify VLAN description field: `"description": "Etag match"`
 3. Execute PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration` and include the If-Match Header using field value `*` as Etag.
 4. Verify if the HTTP response is `200 OK`.
 5. Verify if the HTTP response is empty.
 6. Confirm that the VLAN description field was updated.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- A `200 OK` HTTP response.
- The HTTP response is empty.
- The description field was modified.

#### Test fail criteria

This test fails when:

- The HTTP response is not equal to `200 OK`.
- HTTP response is not empty.
- The description field was not modified.

## Update VLAN using If Match header with a matching Etag

### Objective
The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans/<id>` through the standard REST API PUT method using If-Match header with a matching Etag.

###  Requirements

- Bridge Normal exists.
- A test VLAN added.

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be added with the following configuration:

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

Verify if VLAN was updated unsuccessfully using If-Match header with a matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Modify VLAN description field: `"description": "Etag match"`
 4. Execute PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration` and include the If-Match Header using the Etag read at step 2.
 5. Verify if the HTTP response is `200 OK`.
 6. Verify if the HTTP response is empty.
 7. Confirm that the VLAN description field was updated.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- A `200 OK` HTTP response.
- The HTTP response is empty.
- The description field was modified.

#### Test fail criteria

This test fails when:

- The HTTP response is not equal to `200 OK`.
- HTTP response is not empty.
- The description field was not modified.

## Update VLAN using If Match header with a not matching Etag

### Objective
The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans/<id>` through the standard REST API PUT method using If-Match header with a not matching Etag.

###  Requirements

- Bridge Normal exists.
- A test VLAN added.

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be added with the following configuration:

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

Verify if VLAN was not updated using If-Match header with a not matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Modify VLAN description field: `"description": "Etag match"`
 4. Change the Etag value read at step 2.
 5. Execute PUT request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration` and include the If-Match Header using the changed Etag from step 4.
 6. Verify if the HTTP response is `412 Precondition Failed`.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

A `412 Precondition Failed` HTTP response.

#### Test fail criteria

This test fails when the HTTP response is not equal to `412 Precondition Failed`.

## Create VLAN using If Match header with a matching Etag

### Objective

The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans` through the standard REST API POST method using If-Match header with a matching Etag.

###  Requirements

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be added with the following configuration:

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

Verify if VLAN was added successfully using If-Match header with a matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Execute POST request over `/rest/v1/system/bridges/bridge_normal/vlans?selector=configuration` and include the If-Match Header using the Etag read at step 2.
 4. Verify if the HTTP response is `201 CREATED`.
 5. Verify if the HTTP response is empty.
 6. Confirm that the VLAN description field was updated.

The new VLAN will have the following configuration data:
```
{
    "configuration": {
        "name": "VLAN2",
        "id": 2,
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

- A `201 Created` HTTP response.
- The HTTP response is empty.

#### Test fail criteria

This test fails when:

- The HTTP response is not equal to `201 Created`.
- HTTP response is not empty.

## Create VLAN using If Match header with a not matching Etag

### Objective
The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans` through the standard REST API POST method using If-Match header with a not matching Etag.

###  Requirements

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be added with the following configuration:

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

Verify if VLAN was not created using If-Match header with a not-matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Change the Etag value read at step 2.
 4. Execute POST request over `/rest/v1/system/bridges/bridge_normal/vlans?selector=configuration` and include the If-Match Header using the Etag read at step 4.
 5. Verify if the HTTP response is `412 Precondition Failed`

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

A `412 Precondition Failed` HTTP response.

#### Test fail criteria

This test fails when the HTTP response is not equal to `412 Precondition Failed`

## Query all VLANs using If Match header with a matching Etag

### Objective

The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans` through the standard REST API GET method using If-Match header with a matching Etag.

###  Requirements

- Bridge Normal exists.
- A test VLAN added.

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be added with the following configuration:

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

Verify if the VLANs are retrieved successfully using If-Match header with a matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Execute GET request over `/rest/v1/system/bridges/bridge_normal/vlans?selector=configuration` and include the If-Match Header using the Etag read at step 2.
 4. Verify if the HTTP response is `200 OK`.
 5. Verify if the HTTP response is not empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- A `200 OK` HTTP response.
- The HTTP response is not empty.

#### Test fail criteria

This test fails when:

- The HTTP response is not equal to `200 OK`.
- HTTP response is empty.

## Query all VLANs using If Match header with a not matching Etag

### Objective
The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans` through the standard REST API GET method using If-Match header with a not matching Etag.

###  Requirements

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be added with the following configuration:

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

Verify if the VLANs aren't retrieved using If-Match header with a not matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Change the Etag value read at step 2.
 4. Execute GET request over `/rest/v1/system/bridges/bridge_normal/vlans?selector=configuration` and include the If-Match Header using the Etag read at step 3.
 5. Verify if the HTTP response is `412 Precondition Failed`.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

A `412 Precondition Failed` HTTP response.

#### Test fail criteria

This test fails when the HTTP response is not equal to `412 Precondition Failed`.

## Query VLAN using If Match header with a matching Etag

### Objective

The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans/<id>` through the standard REST API GET method using If-Match header with a matching Etag.

###  Requirements

- Bridge Normal exists.
- A test VLAN added.

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be added with the following configuration:

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

Verify if the VLAN is retrieved successfully using If-Match header with a matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Execute GET request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration` and include the If-Match Header using the Etag read at step 2.
 4. Verify if the HTTP response is `200 OK`.
 5. Verify if the HTTP response is not empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- A `200 OK` HTTP response.
- The HTTP response is not empty.

#### Test fail criteria

This test fails when:

- The HTTP response is not equal to `200 OK`.
- HTTP response is empty.

## Query VLAN using If Match header with a not matching Etag

### Objective
The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans/<id>` through the standard REST API GET method using If-Match header with a not matching Etag.

###  Requirements

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be added with the following configuration:

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

Verify if the VLAN is not retrieved using If-Match header with a not matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Change the Etag value read at step 2.
 4. Execute GET request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration` and include the If-Match Header using the Etag read at step 3.
 5. Verify if the HTTP response is `412 Precondition Failed`.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

A `412 Precondition Failed` HTTP response.

#### Test fail criteria

This test fails when the HTTP response is not equal to `412 Precondition Failed`.

## Delete VLAN using If Match header with a matching Etag

### Objective

The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans/<id>` through the standard REST API DELETE method using If-Match header with a matching Etag.

###  Requirements

- Bridge Normal exists.
- A test VLAN added.

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be addded with the following configuration:

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

Add a VLAN to **Switch 1** with the following data:
```
{
    "configuration": {
        "name": "VLAN2",
        "id": 2,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description
Verify if the VLAN is deleted successfully using If-Match header with a matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans/VLAN2?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Execute DELETE request over `/rest/v1/system/bridges/bridge_normal/vlans/VLAN2?selector=configuration` and include the If-Match Header using the Etag read at step 2.
 4. Verify if the HTTP response is `204 No Content`.
 5. Verify if the HTTP response is not empty.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

- A `204 No Content` HTTP response.
- The HTTP response is empty.

#### Test fail criteria

This test fails when:

- The HTTP response is not equal to `204 No Content`.
- HTTP response is not empty.

## Delete VLAN using If Match header with a not matching Etag

### Objective
The objective of the test is to validate `rest/<version>/system/bridges/<id>/vlans/<id>` through the standard REST API DELETE method using If-Match header with a not matching Etag.

###  Requirements

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

**Switch 1** has bridge_normal configure by default.
**Switch 1** a test VLAN has to be addded with the following configuration:

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

Add a VLAN with the following data:
```
{
    "configuration": {
        "name": "VLAN2",
        "id": 2,
        "description": "test_vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}
```

### Description
Verify if the VLAN is not deleted using If-Match header with a not matching Etag.
 1. Execute a GET request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration`.
 2. Read Etag header field provided by the server.
 3. Change the Etag value read at step 2.
 4. Execute DELETE request over `/rest/v1/system/bridges/bridge_normal/vlans/test?selector=configuration` and include the If-Match Header using the Etag read at step 3.
 5. Verify if the HTTP response is `412 Precondition Failed`.

### Test result criteria
#### Test pass criteria

This test passes by meeting the following criteria:

A `412 Precondition Failed` HTTP response.

#### Test fail criteria

This test fails when the HTTP response is not equal to `412 Precondition Failed`.

## Declarative configuration schema validations
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

## Custom validators
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

## HTTPS support
All REST APIs use the HTTPS protocol to send requests to the REST server. The HTTPS protocol requires the SSL certificate and the private key for authentication of the REST server. It also provides encryption of the data exchanged.
The REST server by default uses a self-signed SSL certificate for this purpose. All of the REST test scripts use the same SSL certificate for testing purpose. The above tests are all modified to send an HTTPS request to the REST server. REST test scripts currently use two different test frameworks:`ops-vsi` and `ops-ft-framework`. The `ops-ft-framework` framework creates a virtual host running a generic Ubuntu image, which uses Python 2.7.6. The following change has been added to `ops-ft-framework` to set up an HTTPS connection with the REST server.

```ditaa
import ssl
import httplib
headers = {"Content-type": "application/json", "Accept": "text/plain"}
url = '/rest/v1/system/ports'
conn = httplib.HTTPSConnection(server_ip, 443, cert_file="/root/restEnv/server.crt", key_file="/root/restEnv/server.key")
conn.request('GET', url, None, headers)
response = conn.getresponse()

```

Scripts, using the `ops-vsi` framework run Python 2.7.9, introduces the SSL context. The following change is added in the library function to set up an HTTPS connection with the REST server. As this is a self-signed certificate, hostname is not being used. Hence, the `check_hostname` flag is set to false. For certificates obtained from a trusted certificate authority (CA), the `check_hostname flag` must be set to true.

```ditaa
import ssl
import httplib
headers = {"Content-type": "application/json", "Accept": "text/plain"}
sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
sslcontext.verify_mode = ssl.CERT_REQUIRED
sslcontext.check_hostname = False
src_path = os.path.dirname(os.path.realpath(__file__))
src_file = os.path.join(src_path, 'server.crt')
sslcontext.load_verify_locations(src_file)
url = '/rest/v1/system/ports'
conn = httplib.HTTPSConnection(server_ip, 443, context=sslcontext)
conn.request('GET', url, None, headers)
response = conn.getresponse()

```

## Auditlog support

### Objective
The test case verifies the Audit Log support in REST by logging events that
succeeded or failed for:

- Create, Update, Delete and Patch operations.

### Requirements
- OpenSwitch
- Ubuntu Workstation

### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|      Host      +---------+    OpenSwitch  |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

### Description
The test case validates the Auditlog integration with REST. Everything except
the standard REST API GET method is going to be tracked by the Auditlog daemon.

1. Verify if Auditlog registers a success event when a user login.
    a. Execute a POST request over `/login`.
    ```
        ?username="netop";password="netop"
    ```
    b. Validate that Auditlog registered the event.

2. Verify if Auditlog registers a success event when creating a Bridge.
    a. Execute a POST request over `/rest/v1/system/bridges`.
    ```
        {"configuration": {"datapath_type": "", "name": "br0"}}
    ```
    b. Verify if the HTTP response is `201 CREATED`.
    c. Validate that Auditlog registered the event.

3. Verify if Auditlog registers a failed event when creating a Bridge.
    a. Execute a POST request over `/rest/v1/system/bridges`.
    ```
        {"configuration": {"datapath_type": "", "name": "br0"}}
    ```
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Validate that Auditlog registered the event.

4. Verify if Auditlog registers a success event when updating a Bridge.
    a. Execute a PUT request over `/rest/v1/system/bridges/br0`.
    ```
        {"configuration": {"datapath_type": "bridge", "name": "br0"}}
    ```
    b. Verify if the HTTP response is `200 OK`.
    c. Validate that Auditlog registered the event.

5. Verify if Auditlog registers a failed event when updating a Bridge.
    a. Execute a PUT request over `/rest/v1/system/bridges`.
    ```
        {"configuration": {"datapath_type": "bridge", "name": "br0"}}
    ```
    b. Verify if the HTTP response is `405 METHOD NOT ALLOWED`.
    c. Validate that Auditlog registered the event.

6. Verify if Auditlog registers a success event when deleting a Bridge.
    a. Execute a DELETE request over `/rest/v1/system/bridges/br0`.
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Validate that Auditlog registered the event.

7. Verify if Auditlog registers a failed event when deleting a Bridge.
    a. Execute a DELETE request over `/rest/v1/system/bridges/br100`.
    b. Verify if the HTTP response is `404 NOT FOUND`.
    c. Validate that Auditlog registered the event.

8. Verify if Auditlog registers a success event when patching a Bridge.
    a. Execute a PATCH request over `/rest/v1/system/bridges/br0`.
    ```
        [{"op": "add", "path": "/datapath_type", "value": "bridge"}]
    ```
    b. Verify if the HTTP response is `204 NO CONTENT`.
    c. Validate that Auditlog registered the event.

9. Verify if Auditlog registers a failed event when patching a Bridge.
    a. Execute a PATCH request over `/rest/v1/system/bridges/br0`.
    ```
        [{"op": "add", "path": "/nonexistent_path", "value": "bridge"}]
    ```
    b. Verify if the HTTP response is `400 BAD REQUEST`.
    c. Validate that Auditlog registered the event.

### Test result criteria
#### Test pass criteria
For REST, the test case is considered passing if Auditlog registers all
events except for GET requests with the proper values, such as: type of
event, type of operation, REST user, HOST address and result(success or failed).

#### Test fail criteria
For REST, the test case is considered fail if Auditlog do not registers the
events for CREATE, PUT, PATCH and DELETE requests with the proper values,
such as: type of event, type of operation, REST user, HOST address and result
(success or failed).

## REST API Logs with No Filters
### Objective
The objective of the test case is to verify the logs API without any query
arguments passed in the URI

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
Get the systemd journal logs using REST API for LOGS. In case the response
contains more entries. ,the output should truncate to 1000 entries

**URL `/rest/v1/logs`**

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology
   diagram.
2. Execute the REST GET method  for URI: `/rest/v1/logs`
3. Verify the status code, response content and JSON format of the response
   data.
4. Verify whether the length of data is less than or equal to the 1000 entries.

### Test result criteria
#### Test pass criteria
- The GET test passes, if the REST API for LOGS returns HTTP method `200 OK`.
  Length of  the response should be less than or equal to 1000 entries.

#### Test fail criteria
- The GET test fails if the REST API method does not return HTTP code `200 OK`
  for the URI `/rest/v1/logs` or length of the response is more than 1000
  entries.


## REST API Logs with Pagination
### Objective
The objective of the test case is to verify the logs API and ensure different
combinations of pagination offset and limit parameters are working well with
the logs URI

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
Get the systemd journal logs using REST API for LOGS and then apply different
filter values of offset  and limit to test the pagination feature.

**URL `/rest/v1/logs?offset=<>&limit=<>`**

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology
   diagram.
2. Execute the REST GET method  for URI: `/rest/v1/logs?offset=<>&limit=<>`
3. Verify the status code, response content and JSON format of the response
   data.
4. Verify whether the length of data is less than or equal to the limit
   paramater passed in the URI.
5. Execute the REST GET method for URI: `/rest/v1/logs?offset=<>` where limit
   is None.
6. Verify the status code, response content and JSON format of the response
   data.
8. Execute the REST GET method for URI: `/rest/v1/logs?limit=<>` where offset
   is None.
9. Verify the status code, response content and JSON format of the response
   data.
10. Execute the REST GET method  for URI: `/rest/v1/logs?offset=1&limit=-1` by
    giving a negative number to the limit parameter.
11. Verify the status code.
12. Execute the REST GET method  for URI: `/rest/v1/logs?offset=-1&limit=10` by
    giving a negative number to the offset parameter.
13. Verify the status code.

### Test result criteria
#### Test pass criteria
- The first GET test passes, if the REST API for LOGS with both offset and
  limit returns HTTP method `200 OK`. Length of  the response should be less
  than or equal to the limit filter used in the URI.
- The second GET test passes if the REST API for LOGS with limit as None
  returns HTTP method `200OK`. Length of the response should be difference
  between length of the data and offset number.
- The third GET test passes if the REST API for LOGS with offset as None
  returns HTTP method `200OK`. Length of the response should be less than or
  equal to the limit filter.
- The fourth  GET test passes if the REST API for LOGS with negative limit
  returns HTTP method `400 BAD REQUEST`.
- The fifth  GET test passes if the REST API for LOGS with negative offset
  returns HTTP method `400 BAD REQUEST`.


#### Test fail criteria
- The first test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `/rest/v1/logs?ofset=<>&limit=<>` or length of the
  response is more than the limit parameter used.
- The second test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `/rest/v1/logs?offset=<>` or length of response is more
  than the difference between length of data and offset number used.
- The third test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `/rest/v1/logs?limit=<>` or length of response is more
  than the the limit parameter used.
- The fourth  GET test fails if the REST API for LOGS with negative limit does
  not return HTTP method `400 BAD REQUEST`.
- The fifth  GET test passes if the REST API for LOGS with negative offset
  does not return HTTP method `400 BAD REQUEST`.

## REST API Logs with Invalid Filters
### Objective
The objective of the test case is to verify and ensure that filters for logs
API other than the desired features are discarded and shown as an error

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
Get the systemd journal logs using REST API for LOGS with valid as well as
invalid filters to catch the desired response.

**URL `/rest/v1/logs?<>`**

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology
   diagram.
2. Execute the REST GET method  for URI: `/rest/v1/logs?priority=7` with valid
   filter.
3. Verify the status code, response content, JSON format and pagination for
   the response data.
4. Execute the REST GET method  for URI: `/rest/v1/logs?priory=7` with invalid
   filter.
5. Verify the status code, response content, JSON format and pagination for
   the response data.
6. Execute the REST GET method for URI: `/rest/v1/logs?priority=<0-7>` with
   valid data for priority filter.
7. Verify the status code, response content, JSON format and pagination for
   the response data.
8. Execute the REST GET method for URI: `/rest/v1/logs?priority=10` with
   invalid data for priority filter.
9. Verify the status code, response content, JSON format and pagination for
   the response data.

### Test result criteria
#### Test pass criteria
- The first test passes, if the response for REST call with valid filter
  returns HTTP method `200 OK`. Length of  the response should be less than or
  equal to the limit filter used in the URI.
- The second test passes if the response for REST call with invalid filter
  returns HTTP method `400 BAD_REQUEST`.
- The third test passes if the response for REST call with valid data returns
  HTTP method `200 OK`. Length of the response should be less than or equal to
  the limit filter used in the URI.
- The fourth test passes if the response for REST call with invalid data
  returns HTTP method `400 BAD_REQUEST`

#### Test fail criteria
- The first test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `/rest/v1/logs?priority=7` or length of the response is
  more than the limit parameter used.
- The second test fails if the REST API method does not return HTTP code
  `400 BAD_REQUEST` for the URI `/rest/v1/logs?priory=7`.
- The third test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `/rest/v1/logs?priority=7` or length of response is
  more than the the limit parameter used.
- The fourth test fails if the REST API method does not return HTTP code
  `400 BAD_REQUEST` for the URI `/rest/v1/logs?priory=8`.

## REST API Logs with Priority
### Objective
The objective of the test case is to verify the priority filter for logs API
is working fine with acceptable values and returns error in the case of
invalid priority values.

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
Get the systemd journal logs using REST API for LOGS with priority levels.

**URL `/rest/v1/logs?priority=<>&offset=<>&limit=<>`**

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology
   diagram.
2. Execute the REST GET method  for URI:
   `/rest/v1/logs?priority=6&offset=0&limit=10` .
3. Verify the status code, response content, JSON format and pagination for the
   response data.
4. Execute the REST GET method  for URI:
   `/rest/v1/logs?priory=-1&offset=0&limit=10` with a negative priority level.
5. Verify the status code returned error code 400.

### Test result criteria
#### Test pass criteria
- The first GET test passes, if the response for REST call with valid priority
  level returns HTTP method `200 OK`. Length of  the response should be less
  than or equal to the limit filter used in the URI.
- The second GET test passes if the response for REST call with a negative
  priority level returns HTTP method `400 BAD_REQUEST`.

#### Test fail criteria
- The first GET test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `/rest/v1/logs?priority=6&offset=0&limit=10` or length
  of the response is more than the limit parameter used.
- The second GET test fails if the REST API method does not return HTTP code
  `400 BAD_REQUEST` for the URI `/rest/v1/logs?priory=-1&offset=0&limit=10`.

## REST API Logs with Since and Until
### Objective
The objective of the test case is to verify the `since` and `until` filters for
logs API by giving different time formats.

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
Get the systemd journal logs using REST API for LOGS with priority levels.

**URL `/rest/v1/logs?since=<>&offset=<>&limit=<>`**
**URL `/rest/v1/logs?until=<>&offset=<>&limit=<>`**
#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology
   diagram.
2. Execute the REST GET method  for URI:
   `/rest/v1/logs?since=1 minute ago&offset=0&limit=10` .
3. Verify the status code, response content, JSON format and pagination for
   the response data.
4. Execute the REST GET method  for URI:
   `/rest/v1/logs?since=<current time stamp>&offset=0&limit=10`  by getting
   the current time stamp in YYYY-MM-DD HH:MM:SS format.
5. Verify the status code, response content, JSON format and pagination for
   the response data.
6. Execute the REST GET method  for URI:
   `/rest/v1/logs?until=now`.
7. Verify the status code, response content, JSON format and pagination for
   the response data.
8. Execute the REST GET method  for URI:
   `/rest/v1/logs?until=<current time stamp>&offset=0&limit=10` by getting the
   current time stamp in YYYY-MM-DD HH:MM:SS format .
9. Verify the status code, response content, JSON format and pagination for the
   response data.
10. Execute the REST GET method  for URI:
    `/rest/v1/logs?since=0000-00-00 00:00:00&offset=0&limit=10` by giving
    invalid time stamp.
11. Verify the status code.
12. Execute the REST GET method  for URI:
    `/rest/v1/logs?since=2020-01-01 01:01:00&offset=0&limit=10` by giving a
    future date.
13. Verify the status code and response content.
14. Execute the REST GET method fo URI:
    `/rest/vi/logs?since=-1 hour ago&offset=0&limit=10` by giving an invalid
    negative integer in relative word.
15. Verify the status code


### Test result criteria
#### Test pass criteria
- The first GET test passes, if the response for REST call with since =
  1 minute ago returns HTTP method `200 OK`. Length of  the response should be
  less than or equal to the limit filter used in the URI. Time stamp of the
  logs returned in the response must be less than 1 minute ago of the current
  time stamp.
- The second GET test passes if the response for the REST call with since =
  <current time stamp> returns HTTP method `200 OK`. Length of  the response
  should be less than or equal to the limit filter used in the URI. Time stamp
  of the logs returned in the response must be less than 1 minute ago current
  time stamp.
- The third GET test passes, if the response for REST call with until = now
  returns HTTP method `200 OK`. Length of  the response should be less than or
  equal to the limit filter used in the URI. Time stamp of the logs returned
  in the response must be less than 1 minute ago of the current time stamp.
- The fourth GET test passes, if the response for REST call with until =
  <current time stamp> returns HTTP method `200 OK`. Length of  the response
  should be less than or equal to the limit filter used in the URI. Time stamp
  of the logs returned in the response must be less than 1 minute ago of the
  current time stamp.
- The fifth GET test passes, if the response for the REST call with
  0000-00-00 00:00:00 timestamp returns HTTP method `400 BAD_REQUEST`.
- The sixth GET test passes, if the response for the REST call with timestap
  with future date returns HTTP method `200 OK` and the response content is
  empty as there will be no logs for the future time stamp.
- The seventh GET test passes, if the response for the REST call with negative
  integer for relative time keyword returns HTTPmethod `400 BAD_REQUEST`.

#### Test fail criteria
- The first GET test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `rest/v1/logs?since=1 minute ago&offset=0&limit=10` or
  length of the response is more than the limit parameter used or the logs time
  stamp in the response is not within the recent 1 minute time window or if the
  response is empty.
- The second GET test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `/rest/v1/logs?since=<current time stamp>&offset=0&limit=10`
  or length of the response is more than the limit parameter used or the logs
  time stamp in the response is not within the recent 1 minute time window or
  if the response is empty.
- The third GET test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `/rest/v1/logs?until=now&offset=0&limit=10` or length of
  the response is more than the limit parameter used or the logs time stamp in
  the response is not within the recent 1 minute time window or if the response
  is empty.
- The fourth GET test fails if the REST API method does not return HTTP code
  `200 OK` for the URI `/rest/v1/logs?until=<current time stamp>&offset=0&limit=10`
  or length of the response is more than the limit parameter used or the logs
  time stamp in the response is not within the recent 1 minute time window or
  if the response is empty.
- The fifth GET test fails, if the response for the REST call does not return
  HTTP method `400 BAD_REQUEST`.
- The sixth GET test fails, if the response for the REST call does not return
  HTTP method `200 OK` and the response content is not empty.
- The seventh GET test fails, if the response for the REST call with negative
  integer for relative time keyword does not return HTTPmethod
  `400 BAD_REQUEST`.

## REST API Logs with Syslog Identifier
### Objective
The objective of the test case is to verify the `SYSLOG_IDENTIFIER` filter for
logs API.

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
Get the systemd journal logs using REST API for LOGS with the SYSLOG_IDENTIFIER
filter.

**URL `/rest/v1/logs?SYSLOG_IDENTIFIER=<>&offset=<>&limit=<>`**

#### Steps

1. Connect OpenSwitch to the Ubuntu workstation as shown in the topology
   diagram.
2. Execute the REST GET method  for URI:
   `/rest/v1/logs?SYSLOG_INDENTIFIER=systemd&offset=0&limit=10` .
3. Verify the status code, response content, JSON format and pagination for the
   response data.

### Test result criteria
#### Test pass criteria
- The GET test passes, if the response for REST call returns HTTP method
  `200 OK`. Length of  the response should be less than or equal to the limit
  filter used in the URI. Response data is not empty and the response data
  consists of only systemd logs and not any other daemon logs.

#### Test fail criteria
- The GET test fails if the REST API method does not return HTTP code `200 OK`
  or the length of the response is more than the limit parameter used or the
  response data is empty or the response data consists of logs other than the
  systemd.

