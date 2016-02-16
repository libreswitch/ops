# High-level design of RBAC

## Contents
- [Overview](#overview)
	- [Responsibilities](#responsibilities)
	- [Design choices](#design-choices)
	- [Relationships to external OpenSwitch entities](#relationships-to-external-openswitch-entities)
		- [RBAC Interface](#rbac-interface)
		- [Restricting a User's Scope based on roles](#restricting-a-users-scope-based-on-roles)
			- [Restricting a User's Access in vtysh](#restricting-a-users-access-in-vtysh)
			- [Restricting a User's Access via the Web UI](#restricting-a-users-access-via-the-web-ui)
			- [Restricting a User's Access via SNMP](#restricting-a-users-access-via-snmp)
			- [Restricting a User's Access via REST API](#restricting-a-users-access-via-rest-api)
			- [Restricting a User's Access to OVSDB API](#restricting-a-users-access-to-ovsdb-api)
			- [Restricting a User's Access via Ansible](#restricting-a-users-access-via-ansible)
	- [OVSDB-Schema](#ovsdb-schema)
	- [Internal structure](#internal-structure)
		- [RBAC Roles](#rbac-roles)
		- [List of Permissions](#list-of-permissions)
		- [Creating Users and Assigning Roles](#creating-users-and-assigning-roles)
			- [Out of the box pre-created accounts](#out-of-the-box-pre-created-accounts)
			- [User account creation work flow](#user-account-creation-work-flow)
			- [Additional changes required to the current implementation Besides the changes above, some additional changes will need to be made to support RBAC.](#additional-changes-required-to-the-current-implementation-besides-the-changes-above-some-additional-changes-will-need-to-be-made-to-support-rbac)

# Overview
Role-Based Access Control (RBAC) is a method for allowing or restricting an authenticated user access to resources based on a role the user has been assigned. Roles are assigned to the user when the user's account is created.

In OpenSwitch we will be using these roles to restrict a user's access to configuration information and system password administration by granting each role a pre-defined list of permissions.


The diagram below shows the relationship between users, roles, and permissions.

```ditaa

     +---------+                                              +------------+
     | User 1  +---+                                     +----> Permission |
     |         |   |                                     |    |      A     |
     +---------+   |         +-------------------+       |    +------------+
                   |         |     Role Alpha    |       |
     +---------+   +--------->                   +-------+    +------------+
     | User 2  +---+         |                   |       +----> Permission |
     |         |             +-------------------+       |    |      B     |
     +---------+                                         |    +------------+
                                                         |
     +---------+             +-------------------+       |    +------------+
     | User 3  +-----+       |     Role Beta     |    +--+----> Permission |
     |         |     +------->                   +----+  |    |      C     |
     +---------+     |       |                   |    |  |    +------------+
                     |       +-------------------+    |  |
     +---------+     |                                |  |    +------------+
     | User 4  +-----+                                +--+----> Permission |
     |         |             +-------------------+    |  |    |      D     |
     +---------+             |    Role Gamma     |    |  |    +------------+
                       +----->                   +-+  |  |
     +---------+       |     |                   | |  |  |    +------------+
     | User 5  +-------+     +-------------------+ +--+--+----> Permission |
     |         |                                              |      E     |
     +---------+                                              +------------+
```

## Responsibilities

The RBAC module will be responsible for:
- Setting up the infrastructure so a user can be assigned to a role.
- Support an API that will allow OpenSwitch modules to check permissions for a given user.

## Design choices

The design choices made for the `RBAC` module are:
- Will initially support 2 roles (ops_admin, ops_netop). The scope of these roles will be discussed later in this document.
- Roles and their underlying permissions will be pre-defined and will not be customer modifiable.
- When a username is passed into any RBAC APIs it is assumed that the user has been authenticated.
- If an authenticated user has no associated role, they will be assigned the role of none and will have no permissions.
- Supporting user-defined roles or permissions will not be addressed at this time.

## Relationships to external OpenSwitch entities

The following diagram provides detailed description of relationships and interactions of the `RBAC` modules with other modules in the switch.

```ditaa
                                              Network
                                                 |
          +------------+----------+--------------+----+---------------+--------------+
          |            |          |                   |               |              |
    +-----v-----+      |     +----v------+       +----v------+  +-----v-----+  +-----v-----+
    | Ansible   |      |     | Web UI    |       | OVSDB API |  | SNMP      |  | vtysh     |
    |           |      |     |           <---+   |           |  |           |  |           |
    |           |      |     +----^------+   |   |           |  |           |  |           |
    |           |      |          |          |   |           |  |           |  |           |
    |           |  +---v----------v------+   |   |           |  |           |  |           |
    |           |  | REST API            |   |   |           |  |           |  |           |
    |           |  |                     <---+   |           |  |           |  |           |
    +-----------+  +---^-----------------+   |   +-----------+  +-----------+  +----^------+
                       |                     |                                      |
             +---------+                     +-------------------+             +----+
             |                                                   |             |
    +--------v---------+                                     +---v-------------v----------+
    | AAA              |                                     |  RBAC                      |
    | ops-aaa-util     |                                     |  check_user_permissions()  |
    |                  |                                     |  get_user_permissions()    |
    |                  |                                     |  get_user_role()           |
    +------------------+                                     +----------------------------+
```

### RBAC Interface

RBAC will support the following functions in both Python and "C" to allow modules to either check if a user has a specific permission or to retrieve a list of permissions for the specified user.
```
    check_user_permission(…) - Check if a user has been assigned a specific permission.
    get_user_permissions(…) – Get the list of permissions assigned to the user.
    get_user_role(…) – Get the role of the specified user.
```

Python examples of using the RBAC Interface.

```
  Boolean rbac.check_user_permission(username, permission)

  Example_usage of rbac.check_user_permission(username, permission):
      ......
      result = rbac.check_user_permission("user", rbac.WRITE_SWITCH_CONFIG)
      if result == True:
         /* User has write access to switch config */
         ...
      ......
```

```
  List rbac.get_user_permissions(username)

  Example_usage of rbac.get_user_permissions(username):
     ......
     permission_list = rbac.get_user_permissions("user")
     ......
     if rbac.READ_SWITCH_CONFIG in permissions_list:
         /* User has read access to the switch config */
         ...
     ......

     if rbac.WRITE_SWITCH_CONFIG in permissions_list:
         /* User has write access to the switch config */
         ...
```

```
  get_user_role(username)

  Example_usage of rbac.get_user_role(username):
     ......
     role_name = rbac.get_user_role("user")
     ......
```

C Examples of using the RBAC Interface.

```
      bool result;
      ......
      result = rbac_check_user_permission("user", WRITE_SWITCH_CONFIG);
      if (result == true) {
         /* User has write access to the switch config */
         ...
         }
      ......
```

```
     ......
     bool                 result;
     rbac_permissions_t   permission_list;
     result = rbac_get_user_permissions("user", &permission_list);
     if (result == true) {
        int i = 0;
        while (i < permission_list.count) {
           if (strcmp(permission_list.name[i], RBAC_READ_SWITCH_CONFIG) == 0) {
              /* User has read access to the switch config */
              }
           i++;
           ...
           }
        }
     .....
```

```
     .....
     bool           result;
     rbac_role_t    role;

     result = rbac_get_user_role("user", &role);
     if (result == true) {
        /* We have the users role name */
        }
     ......
```

### Restricting a User's Scope based on roles

This section outlines the responsibility OpenSwitch modules will have in restricting a user's access to resources.

#### Restricting a User's Access in vtysh

When vtysh is started the user has already been authenticated. Vtysh must make a call to RBAC to either check specific permissions or get the list of permissions accessible to the user. Vtysh must restrict the user from accessing information that is not allowed under their permission list depending on which role (ops_admin, ops_netop, none) the authenticated user has been assigned.

Bash access (start-shell) is no longer allowed in vtysh. In addition, vtysh restricts the use of system calls made by using seccomp or some equivalent functionality.

Vtysh is the shell that netop users are launched into. An admin user is launched into the Bash shell; however, they are able to run vtysh. If admin runs vtysh, a message will be displayed and control will return to the bash shell.

Below are examples on how the CLI might look depending on the role the user has:

For ops_netop
```
  clear        Reset functions
  configure    Configuration from vty interface
  copy         Copy from one config to another
  diag-dump    Show diagnostic information
  disable      Turn off privileged mode command
  end          End current mode and change to enable mode
  erase        Erase configuration
  exit         Exit current mode and down to previous mode
  list         Print command list
  password     Change user password
  ping         Ping Utility
  ping6        Ping Utility
  show         Show running system information
  traceroute   Trace the IPv4 route to a device on the network
  traceroute6  Trace the IPv6 route to a device on the network
```


#### Restricting a User's Access via the Web UI

The Web UI is using the REST API to authenticate the user and to retrieve a list of permissions accessible to the user. The permission list is passed to the Web UI so they can make decisions on what type of information they can present to the user.

#### Restricting a User's Access via SNMP

The SNMP interface is read-only, so there are no plans to place any limitations on this interface.
Access to this interface will be controlled by netop configuring the community name and other SNMP access control.

#### Restricting a User's Access via REST API

The REST API needs to authenticate the user (using AAA) for both network and Web UI access. The REST API calls RBAC to get the permission set of the user. If the user does not have the appropriate permissions to access the switch configuration, the REST API blocks the user from the switch configuration in OVSDB.

#### Restricting a User's Access to OVSDB API

Access to the OVSDB server from the Bash shell is restricted using the ovsdb-client group. Any Linux user given membership to this group will have read/write access to the OVSDB server via the ovsdb-client utility. Great care must be given before any Linux user is given membership to this group.

The builtin user "admin" will be created without membership in this group. The users with the ops_netop role should be created with membership in the ovsdb-client group.

#### Restricting a User's Access via Ansible

Ansible connects to the switch via SSH (key or user/pass) to do system configuration management and provisioning. Ansible will be using the admin account to interact with the switch.

## OVSDB-Schema

RBAC is not adding any data to the OVSDB Schema.

There is a desire to put role/permission mapping in OVSDB in the future, but due to lack of grandular access control, a netop user today could elevate their permission set.

## Internal structure

This section outlines the implementation to support RBAC.

### RBAC Roles

We are supporting 2 pre-defined roles. The table below briefly describes the permissions for each role. Any user created that is not a member of one of the two pre-defined roles has the role of "none" and will be restricted from accessing content in the the switch management interface (CLI, REST, Web UI) .

Built in Roles | Access
---------------|-------
ops_admin      |  * Default Bash shell(with sudo privileges)
               |  * No switch configuration from the management interfaces
               |  * Not a member of the ovsdb-client group
               |  * Firmware upgrades from the management interfaces
               |  * Change user's passwords from the management interfaces
ops_netop      |  * Default vtysh shell
               |  * No Bash access
               |  * View/Set switch configuration from the management interfaces
               |  * Change own password.
none           |  * No permissions

### List of Permissions

This table shows the permissions that are supported with a brief description of the behavior they allow. These permissions are mapped to user's role as described above.

Permission            | Access
----------------------|-------
READ_SWITCH_CONFIG    | Ability to read switch configuration information.
WRITE_SWITCH_CONFIG   | Ability to write switch configuration information.
SYS_MGMT              | System mgmt operations such as User Management and
                      | fw image download/upgrade.

### Creating Users and Assigning Roles

This section illustrates how the the user accounts will be created with a specified role.
```ditaa
                                              Network
                                                 |
          +------------+----------+--------------+----+---------------+--------------+
          |            |          |                   |               |              |
    +-----v-----+      |     +----v------+       +----v------+  +-----v-----+  +-----v-----+
    | Ansible   |      |     | Web UI    |       | OVSDB API |  | SNMP      |  | CLI       |
    |           |      |     |           |       |           |  |           |  |           |
    |           |      |     +----^------+       |           |  |           |  |           |
    |           |  +---v----------v------+       |           |  |           |  |           |
    |           |  | REST API            |       |           |  |           |  |           |
    |           |  |                     |       |           |  |           |  |           |
    +-----------+  +---------------------+       +-----------+  +-----------+  +-----------+


              +------------------------+                     +----------------------------+
              |                        |                     |  Linux commands            |
              | Admin from Bash shell  +--------------------->  useradd, userdel          |
              |                        |                     |                            |
              +------------------------+                     +----------------------------+
```

Currently, OpenSwitch's CLI and REST management interfaces adds a user by making a call to "useradd" and removes a user by calling "userdel". If these mgmt interfaces plan on supporting SYS_MGMT operations (admin operations) then they could support user add/del operations but they need to support roles when creating the users. Outside of the mgmt interfaces, user creation/deletion are be handled in the Bash shell by the system admin. To support the two roles, we are using UNIX groups (as shown below)

ovsdb-client:x:1020:

ops_admin:x:abcd:
ops_netop:x:abce:

The admin must create the user accounts the following way:

"/usr/sbin/useradd -g ops_admin -s /bin/bash admin_username"
"/usr/sbin/useradd -g ops_netop -G ovsdb-client -s /usr/bin/vtysh netop_username"

#### Out of the box pre-created accounts
The switch contains two pre-created user accounts:
* admin - A member of the ops_admin group with a default Bash shell with sudo privileges.
* netop - A member of both the ops_netop and ovsdb-client group and will have default vtysh shell.

#### User account creation work flow

All users on the OpenSwitch device must have local user accounts created before the user can log in. The Admin must create these accounts:

* All user accounts are created by the admin by using `useradd` command in Linux. The admin must follow the rules listed above to create users with the appropriate roles.

Note: The current RADIUS authentication workflow requires a local user account to be added (with or without password). We will continue to use this workflow and the role will be provided by local group membership assigned to the user.

#### Additional changes required to the current implementation Besides the changes above, some additional changes will need to be made to support RBAC.

* Remove "ovsdb-client" and "ovsdb_users" group members from having sudo priviledges.
* Allow "ops_admin" group members to have sudo priviledges.
* Add ops_admin and ops_netop groups to the /etc/group file.
* Remove the password for user "root".
* Create "admin" and "netop" accounts with appropriate group membership and permissions.
