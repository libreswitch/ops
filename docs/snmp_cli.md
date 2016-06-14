# Configuration Support for SNMP Support

## Contents

- [Manage SNMP agent configuration](#manage-snmp-agent-configuration)
- [Manage SNMP authentication and authorization](#manage-snmp-authentication-and-authorization)
- [Configuring SNMPv3 users](#configuring-snmpv3-users)
- [Configuring SNMP trap](#configuring-snmp-trap)
- [Configuring SNMPv3 trap](#configuring-snmpv3-trap)
- [Configuring SNMP system MIB objects](#configuring-snmp-system-mib-objects)
- [Display commands](#display-commands)

## Manage SNMP agent configuration

### SNMP master agent configuration

The following command configures the port to which the SNMP master agent is bound.

###### Ovsdb tables/columns altered with the above configuration -
|Table|Column|key|data type|
|--------|----------|--------|
|System|other_config|snmp_agent_port|Integer|

###### Defaults
Default agent-port is 161.

#### Syntax

```
[no] snmp-server agent-port <1-65535>

```

#### Description

This command resets the SNMP master agent port to the default value of UDP port 161.

#### Authority

Admin user.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Resets the master agent port to default UDP port 161.|
| **<1-65535>** | Required | Integer | The port on which the SNMP master agent listens for SNMP requests.|

#### Examples

```

(config)# snmp-server  agent-port 2000

(config)# no snmp-server agent-port 2000

```

###JSON

CLI Command: snmp-server agent-port 5
REST Output:
  "other_config": {
            "snmp_agent_port": "5"
    },


## Manage SNMP authentication and authorization

### SNMPv1, SNMPv2c community strings

This command is used to configure community strings for the SNMP agent. Maximum of 10 SNMP communities can be configured. Default community is restored only when count of configured SNMP communities is zero.

###### Ovsdb tables/columns altered with the above configuration -
|Table|Column|key| data type|
|--------|----------|--------|--|
|System|snmp_communities|NA|string|

###### Defaults
Default snmp community is 'public'.

#### Syntax

```
[no] snmp-server community <WORD>
```

#### Description

This command adds/removes community strings.

#### Authority

Admin user.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Removes the specified community string.|
| **WORD** | Required | String | The name of the community string. Default is public.|

#### Examples

```
(config)# snmp-server community private

(config)# no snmp-server community private

```

###JSON
CLI Command: snmp-server community public
REST Output:
   "snmp_communities": [
       "public"
    ],


## Configuring SNMPv3 users

This command is used to configure the credentials of SNMPv3 user. The SNMPv3 provides secure access to devices by a combination of authenticating and encrypting SNMP protocol packets over the network.

###### Ovsdb tables/columns altered with the above configuration -
|Table|Column|key| data type|
|--------|----------|--------|--|
|SNMPv3_User|user_name|NA|string|
|SNMPv3_User|auth_protocol|NA|string|
|SNMPv3_User|auth_pass_phrase|NA|string|
|SNMPv3_User|priv_protocol|NA|string|
|SNMPv3_User|priv_pass_phrase|NA|string


#### Syntax

```
[no] snmpv3 user <WORD> [auth <md5 | sha>] auth-pass <WORD> [priv <aes | des>]
priv-pass <WORD>
```

#### Description

This command adds/removes SNMPv3 users.
#### Authority

Admin user.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Removes the specified SNMPv3 user.|
| **WORD** | Required | String | The name of the SNMPv3 user. |
| **md5 or sha** | Optional | Literal | The SNMPv3 authentication protocol can be either MD5 or SHA.|
| **WORD** | Required | String | The auth passphrase of the SNMPv3 user. It must be at least 8 characters in length.|
| **aes or des** | Optional | Literal | The SNMPv3 privacy protocol can be either aes or des.|
| **WORD** | Required | String | The privacy passphrase of the SNMPv3 user. It must be at least 8 characters in length.|

#### Examples

```
(config)# snmpv3 user Admin auth sha auth-pass mypassword priv des priv-pass myprivpass

(config)# no snmpv3 user Admin auth sha auth-pass mypassword priv des priv-pass myprivpass

```

###JSON
CLI Command: snmpv3 user Admin auth sha auth-pass mypassword priv des priv-   pass myprivpass
REST Output:
[
    "/rest/v1/system/snmpv3_users/Admin"
]

## Configuring SNMP trap

This command is used to configure the trap receivers to which the SNMP agent can send trap notifications.

###### Ovsdb tables/columns altered with the above configuration -
|Table|Column|key|data type|
|--------|----------|-------|-|
|SNMP_Trap|receiver_address|NA|IP address
|SNMP_Trap|type|NA|string|
|SNMP_Trap|version|NA|string|
|SNMP_Trap|community_name|NA|string|
|SNMP_Trap|receiver_udp_port|NA|Integer|

###### Defaults
community_name - public
receiver_udp_port - 162

#### Syntax

```
[no] snmp-server host <A.B.C.D | X:X::X:X >  [trap] [version < v1 | v2c >] [community WORD] [port <UDP port>]
[no] snmp-server host <A.B.C.D | X:X::X:X >  [trap | inform] [version < v2c >] [community WORD] [port <UDP port>]
```

#### Description

This command is used to configure the SNMP Trap receivers with IP and port, notification type, version, community string.

#### Authority

Admin user.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Removes the specified trap receiver configuration.|
| **A.B.C.D** | Required | A.B.C.D | Valid IPv4 address of the trap receiver.|
| **X:X::X:X** | Required | X:X::X:X | Valid IPv6 address of the trap receiver.|
| **trap or inform** | Optional | trap or inform  | The SNMP notification type.|
| **v1 or v2c** | Optional | v1 or v2c  | The SNMP protocol version.|
| **WORD** | Optional | String | The name of the community string to be used in the SNMP trap notifications. Default is public.|
| **UDP_port** | Optional | Integer | The port on which the trap receiver listens for SNMP trap notifications. Default is UDP port 162.|

#### Examples

```
(config)# snmp-server host 10.10.10.10 trap version v1

(config)# no snmp-server host 10.10.10.10 trap version v1

(config)# snmp-server host 10.10.10.10 trap version v2c community public

(config)# no snmp-server host 10.10.10.10 trap version v2c community public

(config)# snmp-server host 10.10.10.10 trap version v2c community public port 5000

(config)# no snmp-server host 10.10.10.10 trap version v2c community public port 5000

(config)# snmp-server host 10.10.10.10 inform version v2c community public

(config)# no snmp-server host 10.10.10.10 inform version v2c community public

(config)# snmp-server host 10.10.10.10 inform version v2c community public port 5000

(config)# no snmp-server host 10.10.10.10 inform version v2c community public port 5000

```

###JSON
CLI Command 1: snmp-server host 10.10.10.10 trap version v1
REST Output:
[    "/rest/v1/system/snmp_traps/10.10.10.10/162/%5Bu%27trap%27%5D/%5Bu%27v1%27%5D"
]

CLI Command 2: snmp-server host 10.10.10.10 inform version v2c community public port 5000
REST Ouptut:
 [    "/rest/v1/system/snmp_traps/10.10.10.10/162/%5Bu%27trap%27%5D/%5Bu%27v2c%27%5D",
    "/rest/v1/system/snmp_traps/10.10.10.10/5000/%5Bu%27inform%27%5D/%5Bu%27v2c%27%5D"
]

## Configuring SNMPv3 trap


This command is used to configure the trap receivers to which the SNMP agent can send SNMPv3 trap notifications. To configure SNMPv3 trap, a SNMPv3 user should exist.

###### Ovsdb tables/columns altered with the above configuration -
|Table|Column|key|data type|
|--------|----------|-------|-|
|SNMP_Trap|receiver_address|NA| IP address
|SNMP_Trap|type|NA|string|
|SNMP_Trap|version|NA|string |
|SNMP_Trap|community_name|NA|string |
|SNMP_Trap|receiver_udp_port|NA| Integer|

###### Defaults
receiver_udp_port - 162


#### Syntax

```
[no] snmp-server host <A.B.C.D | X:X::X:X >  [trap | inform] [version < v3 >] user <WORD> [port <UDP port>]
```

#### Description

This command is used to configure the SNMPv3 trap receivers with IP and port, trap version, SNMPv3 user credentials.

#### Authority

Admin user.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Removes the specified trap receiver configuration.|
| **A.B.C.D** | Required | A.B.C.D | Valid IPv4 address of the trap receiver.|
| **X:X::X:X** | Required | X:X::X:X | Valid IPv6 address of the trap receiver.|
| **trap or inform** | Optional | trap or inform  | The SNMP notification type. Default is trap.|
| **v3** | Required | v3 | The SNMP trap notification version. To send SNMPv3 trap/inform need to configured with option v3.|
| **WORD** | Required | String | The SNMPv3 user name to be used in the SNMP trap notifications.|
| **UDP_port** | Optional | Integer | The port on which the trap receiver listens for SNMP trap notifications. Default is UDP port 162.|

#### Examples

```
(config)# snmp-server host 10.10.10.10 trap version v3 auth user Admin

(config)# no snmp-server host 10.10.10.10 trap version v3 auth user Admin

(config)# snmp-server host 10.10.10.10 trap version v3 auth user Admin port 2000

(config)# no snmp-server host 10.10.10.10 trap version v3 auth user Admin port 2000

```

###JSON
CLI Command: snmp-server host 10.10.10.10 trap version v3 user Admin port 2000
REST Output:
[
    "/rest/v1/system/snmp_traps/10.10.10.10/162/%5Bu%27trap%27%5D/%5Bu%27v3%27%5D",
    "/rest/v1/system/snmp_traps/10.10.10.11/5000/%5Bu%27inform%27%5D/%5Bu%27v2c%27%5D",
    "/rest/v1/system/snmp_traps/10.10.10.10/162/%5Bu%27trap%27%5D/%5Bu%27v2c%27%5D",
    "/rest/v1/system/snmp_traps/10.10.10.10/5000/%5Bu%27inform%27%5D/%5Bu%27v2c%27%5D",
    "/rest/v1/system/snmp_traps/10.10.10.10/2000/%5Bu%27trap%27%5D/%5Bu%27v3%27%5D"
]



## Configuring SNMP system MIB objects


The following commands are used to configure the following SNMP system MIB objects -
- sysDescr
- sysLocation
- sysContact

###### Ovsdb tables/columns altered with the above configuration -
|Table|Column|key|data type|
|--------|----------|-------|-|
|System|other_config|system_contact|string|
|System|other_config|system_description|string|
|System|other_config|system_location|string|

#### Syntax

```
[no] snmp-server system-description .LINE
[no] snmp-server system-contact .LINE
[no] snmp-server system-location LINE
```

#### Description

This command is used to configure some SNMP ystem MIB objects.

#### Authority

Admin user.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Removes the specified trap receiver configuration.|
|system-description .LINE|required| array of string literals|Configures sysDescr|
|system-contact .LINE|required|array of string literals|Configures sysContact|
|system-location .LINE|required|array of string literals|Configures sysLocation|

#### Examples

```
switch(config)# snmp-server system-description this is openswitch system

switch(config)# snmp-server system-location Dock of the bay

switch(config)# snmp-server system-contact me@whatever.com

```

###JSON
CLI Command 1: snmp-server system-description This is OpenSwitch System

CLI Command 2: snmp-server system-location Dock of the bay

CLI Command 3: snmp-server system-contact web@ui.com

REST Ouput:
"other_config": {
    "system_contact": "web@ui.com",
    "system_location": "Dock of the bay",
    "system_description": "This is OpenSwitch System",
},



## Display commands



### show snmp community

#### Syntax

```
show snmp community
```

#### Description

This command displays details of all the configured community strings.

#### Authority

Admin User.

#### Parameters

N/A

#### Examples

```

    switch# show snmp community

    Community Names :
      private
      admin

```

### show snmp system

#### Syntax

```
show snmp system
```

#### Description

This command displays details of all the configured system MIB objects

#### Authority

Admin User.

#### Parameters

N/A

#### Examples

```

switch# show snmp system
SNMP system information
----------------------------
System description : this is openswitch system
System location : Dock of the bay
System contact : me@whatever.com

```

### show snmp trap

#### Syntax

```
show snmp trap
```

#### Description

This command displays details of all the configured trap receivers:

- Host IP Address
- Port
- SNMP version
- Notification type
- Community Name (SNMPv1/2c)
- SNMPv3 User

#### Authority

Admin User.

#### Parameters

N/A

#### Examples

```

  switch# show snmp trap
      Trap Receivers:
      -------------------------------------------------------
      Host            Port      Type     Version   SecName
      -------------------------------------------------------
      10.1.1.1        6000      trap     SNMPv1    private
      10.1.1.1        162       inform   SNMPv2c   public
      10.1.1.1        5000      inform   SNMPv3    -


```
### show snmpv3 users

#### Syntax

```
show snmpv3 users
```

#### Description

This command displays details of all the configured SNMPv3 users.

- User name
- Authentication protocol
- Privacy protocol

#### Authority

Admin user.

#### Parameters

N/A

#### Examples

```

  switch# show snmpv3 users
  SNMPv3 Users :
  ---------------------------------
    User       AuthMode    PrivMode
  ---------------------------------
    Admin        MD5       AES
    Guest        MD5       AES

```
