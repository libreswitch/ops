# TACACS+

## Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Limitations](#limitations)
- [Defaults](#defaults)
- [Configuring TACACS+](#configuring-tacacs)
  - [Adding global timeout](#adding-global-timeout)
  - [Deleting global timeout](#deleting-global-timeout)
  - [Adding global passkey](#adding-global-passkey)
  - [Deleting global passkey](#deleting-global-passkey)
  - [Adding global authentication mechanism](#adding-global-authentication-mechanism)
  - [Deleting global authentication mechanism](#deleting-global-authentication-mechanism)
  - [Adding a server](#adding-a-server)
  - [Deleting a server](#deleting-a-server)
  - [Adding a server-group](#adding-a-server-group)
  - [Deleting a server-group](#deleting-a-server-group)
  - [Configuring authentication sequence](#configuring-authentication-sequence)
  - [Deleting authentication sequence](#deleting-authentication-sequence)
  - [Enabling authentication fail-through](#enabling-authentication-fail-through)
  - [Disabling authentication fail-through](#disabling-authentication-fail-through)
  - [Configuring AAA authorization with fallback](#configuring-aaa-authorization-with-fallback)
  - [Deleting AAA authorization with fallback](#deleting-aaa-authorization-with-fallback)
- [Verifying AAA configuration](#verifying-aaa-configuration)
  - [Viewing global config and TACACS+ servers](#viewing-global-config-and-tacacs-servers)
  - [Viewing TACACS+ server groups](#viewing-tacacs-server-groups)
  - [Viewing AAA Authentication sequence](#viewing-aaa-authentication-sequence)
  - [Viewing AAA Authorization information](#viewing-aaa-authorization-information)
  - [Viewing Privilege level information for current user](#viewing-privilege-level-information-for-current-user)
- [REST Custom Validations](#rest-custom-validations)
- [MIB](#mib)
- [Supportability](#supportability)
  - [Logging](#logging)
    - [Diagnostics](#diagnostics)
    - [Details of Protocol Support](#details-of-protocol-support)
    - [Related features](#related-features)

## Overview
TACACS+ is a protocol that handles authentication, authorization, and accounting (AAA) services.
TACACS+ client functionality is supported on the switch.

## Prerequisites
- A TACACS+ server (either local or remote) is needed for AAA services.
- OpenSwitch needs to have management interface UP and enabled.

## Limitations
- A maximum of 64 TACACS+ servers can be configured.
- Server can be configured with a unicast IPV4/IPV6 address or FQDN.
- A maximum of 28 user-defined AAA servers-groups can be configured.
- Session-type (console/ssh/telnet) configuration provided together as 'default' configuration for authentication.
- TACACS+ server reachability is over the management interface.

## Defaults
- The default authentication tcp-port is 49.
- The default authentication timeout value is five.
- The default authentication key (shared-secret between client and server) is testing123-1.
- The default authentication-protocol is pap.

## Configuring TACACS+
Configure the terminal to change the CLI context to config context with the following commands:
```
switch# configure terminal
switch(config)#
```

### Adding global timeout
#### Syntax
` tacacs-server timeout <1-60>`
#### Description
The timeout value specifies the number of seconds to wait for a response from the TACACS+ server before moving to next TACACS+ server.
If not specified, a default value of five seconds is used.
This can be over-ridden by a fine-grained per server timeout while configuring individual servers.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax | Description |
|-----------|----------|--------|-------------|
| *1-60* | Required | 1-60 | Timeout value |
#### Examples
```
switch(config)# tacacs-server timeout 10
```

### Deleting global timeout
#### Syntax
`no tacacs-server timeout`
#### Description
Reset the global timeout to default authentication timeout value *5*
```
switch(config)# no tacacs-server timeout
```
#### Authority
All users.
#### Examples
```
switch(config)# no tacacs-server timeout
```

### Adding global passkey
#### Syntax
`tacacs-server key WORD`
#### Description
This key is used as shared-secret for encrypting the communication between all tacacs-server and OpenSwitch.
This can be over-ridden by a fine-grained per server passkey configuration.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax | Description |
|-----------|----------|--------|-------------|
| *WORD* | Required | String of maximum length 32 characters |  The key used while communicating with the server |
#### Examples
```
switch(config)# tacacs-server key testing-key
```
The length of key should be less than 32 characters.

### Deleting global passkey
#### Syntax
`no tacacs-server key`
#### Description
Reset the global key to the default authentication key value of  *testing123-1*.
#### Authority
All users.
#### Examples
```
switch(config)# no tacacs-server key
```

### Adding global authentication mechanism
#### Syntax
`tacacs-server auth-type [pap/chap]`
#### Description
This is the authentication protocol which is used for communication with TACACS+ servers.
This can be over-ridden by a fine-grained per server auth-type configuration.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax | Description |
|-----------|----------|--------|-------------|
| *pap/chap* | Required | Literal | Authentication protocol name |
#### Examples
```
switch(config)# tacacs-server auth-type [pap/chap]
```

### Deleting global authentication mechanism
#### Syntax
`no tacacs-server auth-type`
#### Description
Reset the global authentication mechanism to the default authentication mechanism *pap*.
#### Authority
All users.
#### Examples

```
switch(config)# no tacacs-server auth-type
```

### Adding a server
#### Syntax
`tacacs-server host <FQDN/IPv4/IPv6 address> [key passkey] [timeout <1-60>] [port <1-65535>] [auth-type pap/chap]`
#### Description
Add a TACACS+ SERVER and the configured TACACS+ server is added to the default TACACS+ family group (named "tacacs_plus").
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax | Description |
|-----------|----------|--------|-------------|
| *FQDN/IPv4/IPv6* | Required | FQDN of maximum length 45 characters, IPv4 or IPv6  | The name or IPv4/IPv6 address of the server. |
| *passkey* | Optional | Key-string of maximum length 32 characters | The key used while communicating with the server |
| *1-60* | Optional | 1-60 | Timeout value |
| *1-65535* | Optional | 1-65535 | TCP port number |
| *pap/chap* | Optional | Literal | Authentication protocol name |
#### Examples
```
switch(config)# tacacs-server host 1.1.1.1
switch(config)# tacacs-server host 1.1.1.2 port 12
switch(config)# tacacs-server host abc.com timeout 15 port 22
switch(config)# tacacs-server host 2001:0db8:85a3:0000:0000:8a2e:0370:7334
switch(config)# tacacs-server host 1.1.1.3 key test-123 timeout 15 port 22 auth-type chap
```

### Deleting a server
#### Syntax
`tacacs-server host <FQDN/IPv4/IPv6> [port <1-65535>]`
#### Description
Delete a previously added TACACS+ server.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax | Description |
|-----------|----------|--------|-------------|
| *FQDN/IPv4/IPv6* | Required | FQDN of maximum length 45 characters, IPv4 or IPv6  | The name or IPv4/IPv6 address of the server. |
| *1-65535* | Optional | 1-65535 | TCP port number |
If a port number is not provided, the system will search the TACACS+ server by host name and default authentication port *49*.
#### Examples
```
switch(config)# no tacacs-server host 1.1.1.1
switch(config)# no tacacs-server host abc.com port 22
```

### Adding a server-group
#### Syntax
`aaa group server tacacs+ WORD`
#### Description
Create an AAA server-group that contains 0 or more preconfigured TACACS+ servers.
A maximum of 32 server-groups can be present in the system.
Out of these four (4) are default server-groups (local, radius, tacacs_plus, none).
Hence, 28 user-defined groups are allowed.
The user-defined group cannot be named "local", "radius", "tacacs_plus" or "none".
Predefined TACACS+ servers can then be added to this group.
The server continues to be part of the default "tacacs_plus" family group.
For authentication using a server-group, the servers are accessed in the
same order in which they were added to the group.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax | Description |
|-----------|----------|--------|-------------|
| *tacacs+* | Required | Literal | Create a TACACS+ server group. |
| *WORD* | Required | String of maximum length 32 | Server group name. |
#### Syntax
`server <FQDN/IPv4/IPv6> [port <1-65535>]`
#### Parameters
| Parameter | Status   | Syntax | Description |
|-----------|----------|--------|-------------|
| *FQDN/IPv4/IPv6* | Required | FQDN of maximum length 45 characters, IPv4 or IPv6  | The name or IPv4/IPv6 address of the server. |
| *1-65535* | Optional | 1-65535 | TCP port number |
If a port number is not provided, the system will search the TACACS+ server by host name and default authentication port *49*.
#### Examples
```
switch(config)# aaa group server tacacs+ sg1
switch(config-sg)# server 1.1.1.2 port 12
switch(config)# aaa group server tacacs+ sg2
switch(config-sg)# server 2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

### Deleting a server-group
#### Syntax
`no aaa group server tacacs+ WORD`
#### Description
Only a pre-configured user-defined TACACS+ server-group can be deleted.
The servers belonging to the group being deleted are still a part of the
default "tacacs_plus" family group.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax | Description |
|-----------|----------|--------|-------------|
| *tacacs+* | Required| Literal | Create a TACACS+ server group. |
| *WORD* | Required | String of maximum length 32 | Server group name. |
#### Examples
```
switch(config)# no aaa group server tacacs+ sg2
```

### Configuring authentication sequence
#### Syntax
`aaa authentication login default <local | group group-list>`
#### Description
Preconfigured server groups can be sequenced to be accessed for authentication.
The server groups will be accessed in the order in which they are mentioned.
Also the servers within the groups will be accessed in the order in which they were added to the group.
By default "local" authentication is triggered if no group is mentioned or if the mentioned list is exhausted.
All servers will be accessed in a fail-through manner if *aaa authentication allow-fail-through* is configured.
**fail-through** Upon failure in connection or failure in authentication, the next server will be reached out to.

#### Authority
All users.
#### Parameters
| Parameter  | Status   | Syntax  | Description |
|------------|----------|---------|-------------|
| *local*  | Optional | Literal | Enable local authentication. |
| *group-list* | Optional | String | Space separated group or family names  |
**Notes:**
1. Valid family names are: local, tacacs+ and radius .
2. Each group should be given only once in a group-list.
3. The 'local' literal can be given at most once, either before 'group' literal or as part of group-list.
4. Either the 'local' literal or user defined group-list must be given in command.

#### Examples
```
switch(config)# aaa authentication login default group sg1 tacacs_plus local
switch(config)# aaa authentication login default local
```

### Deleting authentication sequence
#### Syntax
`no aaa authentication login default`
#### Description
Remove a configured sequence of server-groups for authentication.
#### Authority
All users.
#### Examples
```
switch(config)# no aaa authentication login default
```

###Enabling authentication fail-through
#### Syntax
`aaa authentication allow-fail-through`
#### Description
Enables Authentication fail-through. If failed to authenticate on a TACACS+ or RADIUS server,
the system attempts to authenticate on the next TACACS+/RADIUS server according to the authentication priority sequence.
#### Authority
All users.
#### Examples
```
switch(config)# aaa authentication allow-fail-through
```

### Disabling authentication fail-through
#### Syntax
`no aaa authentication allow-fail-through`
#### Description
Disables Authentication fail-through. If failed to authenticate on a TACACS+ or RADIUS server,
the system will not attempt to authenticate on the next TACACS+/RADIUS server.
#### Authority
All users.
#### Examples
```
switch(config)# no aaa authentication allow-fail-through
```

### Configuring AAA Authorization with fallback

By issuing the `aaa authorization commands default` command, the user can configure Authorization on the switch.
 Fallback preference is dictated by the sequence of groups and none are entered by the user.
This command would mean that it would reach out to TACACS+ for each command entered for all users.

```
switch(config)# aaa authorization commands default {group <group-list> | none}
For example:
switch(config)# aaa authorization commands default group tacacs+ none
switch(config)# aaa authorization commands default group TacGroup1 tacacs+ none
```

### Deleting AAA Authorization with fallback

By issuing a `no aaa authorization commands default` command, the user can unconfigure AAA Authorization on the switch.
If AAA Authorization is not configured, it uses RBAC authorization.

```
switch(config)# no aaa authorization commands default
```
## Verifying AAA configuration
### Viewing global config and TACACS+ servers
#### Syntax
`show tacacs-server [detail]`
#### Description
The `show tacacs-server` and `show tacacs-server detail` commands display the configured TACACS+ servers.
Both the commands show the global parameters as well as per server configurations.
For TACACS+ server assigned to user defined groups, group priority
(the sequence of TACACS+ server assignment to user defined group) is displayed, otherwise default priority (the sequence of TACACS+ server creation) is displayed instead.
#### Authority
All users.
#### Parameters
| Parameter  | Status   | Syntax  | Description |
|------------|----------|---------|-------------|
| *detail*  | Optional | Literal | Display detailed TACACS+ servers information. |
#### Examples
```
switch# show tacacs-server

******* Global TACACS+ Configuration *******
Shared-Secret: testing123-1
Timeout: 5
Auth-Type: pap
Number of Servers: 3

------------------------------------------------------------------------------------------------
SERVER NAME                                   | PORT
------------------------------------------------------------------------------------------------
1.1.1.2                                       | 12
2001:0db8:85a3:0000:0000:8a2e:0370:7334       | 49
1.1.1.3                                       | 22

```
```
switch# show tacacs-server detail

******* Global TACACS+ Configuration *******
Shared-Secret: testing123-1
Timeout: 5
Auth-Type: pap
Number of Servers: 3

****** TACACS+ Server Information ******
Server-Name              : 1.1.1.2
Auth-Port                : 12
Shared-Secret (default)  : testing123-1
Timeout (default)        : 5
Auth-Type (default)      : pap
Server-Group             : sg1
Group-Priority           : 1

Server-Name              : 2001:0db8:85a3:0000:0000:8a2e:0370:7334
Auth-Port                : 49
Shared-Secret (default)  : testing123-1
Timeout (default)        : 5
Auth-Type (default)      : pap
Server-Group (default)   : tacacs_plus
Default-Priority         : 4

Server-Name              : 1.1.1.3
Auth-Port                : 22
Shared-Secret            : test-123
Timeout                  : 15
Auth-Type                : chap
Server-Group (default)   : tacacs_plus
Default-Priority         : 5

```

### Viewing TACACS+ server groups
#### Syntax
`show aaa server-group`
#### Description
Display a table of TACACS+ servers grouped by different TACACS+ server group assignment.
For TACACS+ server assigned to user defined groups, group priority (the sequence of TACACS+ server assignment to user defined group) is displayed,
otherwise default priority (the sequence of TACACS+ server creation) is displayed instead.
#### Authority
All users.
#### Examples
```
switch# show aaa server-groups

******* AAA Mechanism TACACS+ *******
------------------------------------------------------------------------------------------------
GROUP NAME                      | SERVER NAME                                  | PORT | PRIORITY
------------------------------------------------------------------------------------------------
sg1                             | 1.1.1.2                                      | 12   | 1
------------------------------------------------------------------------------------------------
tacacs_plus (default)           | 2001:0db8:85a3:0000:0000:8a2e:0370:7334      | 49   | 4
tacacs_plus (default)           | 1.1.1.3                                      | 22   | 5
------------------------------------------------------------------------------------------------

```

### Viewing AAA Authentication sequence
#### Syntax
`show aaa authentication`
#### Description
Display a table of server groups based on the sequence of authentication access.
**Note:** Group priority here represent the sequence of group, which is different from
TACACS+ server group priority (which is sequence of server assigned to group)
#### Authority
All users.
#### Examples
```
switch(config)# aaa authentication login default group sg1 tacacs_plus local
switch(config)# exit
switch# show aaa authentication
AAA Authentication:
  Fail-through                          : Disabled
  Fallback to local authentication      : Enabled

Default Authentication for All Channels:
------------------------------------------------------------------------------------------------
GROUP NAME                       | GROUP PRIORITY
------------------------------------------------------------------------------------------------
sg1                              | 1
tacacs_plus                      | 2
local                            | 3
```

### Viewing AAA Authorization sequence
#### Syntax
`show aaa authorization`
#### Description
The `show aaa authorization` command displays detailed information on Authorization configuration on the switch.
#### Authority
All users.
#### Examples
```
switch(config)# aaa authorization commands default group sg1 tacacs_plus none
switch(config)# exit
switch# show aaa authorization
Command Authorization sequence for default channel:
------------------------------------------------------------------------------------------------
GROUP NAME                       | GROUP PRIORITY
------------------------------------------------------------------------------------------------
sg1                              | 1
tacacs_plus                      | 2
none                             | 3
```

### Viewing Privilege level information for current user
#### Syntax
`show privilege-level`
#### Description
The 'show privilege-level' command displays the current user privilege level for the current session.
For example for user with ops_netop role, it would show as follows:
#### Authority
All users.
#### Examples
```
switch# show privilege-level
Privilege level is 14
```

## REST Custom Validations
TBD

## MIB
N/A

## Supportability

### Logging
TBD

### Diagnostics
TBD

## Details of Protocol Support
Please refer to ops-aaa-utils/AAA_Design.md for details about TACACS+ and RADIUS feature support.

## Related features

