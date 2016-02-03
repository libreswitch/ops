# Configuration Support for SNMP Support

## Contents

- [Manage SNMP agent configuration](#manage-snmp-agent-configuration)
- [Manage SNMP authentication and authorization](#manage-snmp-authentication-and-authorization)
- [Configuring SNMPv3 users](#configuring-snmpv3-users)
- [Configuring SNMP trap](#configuring-snmp-trap)
- [Configuring SNMPv3 trap](#configuring-snmpv3-trap)
- [Display commands](#display-commands)

## Manage SNMP agent configuration

### SNMP master agent configuration

The following command configures the port to which the SNMP master agent is bound.

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

## Manage SNMP authentication and authorization

### SNMPv1, SNMPv2c community strings

This command is used to configure community strings for the SNMP agent.

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

## Configuring SNMPv3 users

This command is used to configure the credentials of SNMPv3 user. The SNMPv3 provides secure access to devices by a combination of authenticating and encrypting SNMP protocol packets over the network.

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
| **md5 or sha** | Optional | Literal | The SNMPv3 authentication protocol can be either MD5 or SHA. Default is md5.|
| **WORD** | Required | String | The auth passphrase of the SNMPv3 user. It must be at least 8 characters in length.|
| **aes or des** | Optional | Literal | The SNMPv3 privacy protocol can be either aes or des. Default is aes.|
| **WORD** | Required | String | The privacy passphrase of the SNMPv3 user. It must be at least 8 characters in length.|

#### Examples

```
(config)# snmpv3 user Admin auth sha auth-pass mypassword priv des priv-pass myprivpass

(config)# no snmpv3 user Admin auth sha auth-pass mypassword priv des priv-pass myprivpass

```

## Configuring SNMP trap

This command is used to configure the trap receivers to which the SNMP agent can send trap notifications.

#### Syntax

```
[no] snmp-server host <A.B.C.D | X:X::X:X >  [trap] [version < v1 | v2c >] [community WORD] [port <UDP port>]
[no] snmp-server host <A.B.C.D | X:X::X:X >  [trap | inform] [version < v1 | v2c >] [community WORD] [port <UDP port>]
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
| **trap or inform** | Optional | trap or inform  | The SNMP notification type. Default is trap.|
| **v1 or v2c** | Optional | v1 or v2c  | The SNMP protocol version. Default is SNMPv2c.|
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

## Configuring SNMPv3 trap


This command is used to configure the trap receivers to which the SNMP agent can send SNMPv3 trap notifications.

#### Syntax

```
[no] snmp-server host <A.B.C.D | X:X::X:X >  [trap | inform] [version < v3 >] < auth | noauth | priv > user <WORD> [port <UDP port>]
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
| **auth or noauth or priv** | Required | auth | The SNMPv3 user authentication/encrption options.|
| **WORD** | Required | String | The SNMPv3 user name to be used in the SNMP trap notifications.|
| **UDP_port** | Optional | Integer | The port on which the trap receiver listens for SNMP trap notifications. Default is UDP port 162.|

#### Examples

```
(config)# snmp-server host 10.10.10.10 trap version v3 auth user Admin

(config)# no snmp-server host 10.10.10.10 trap version v3 auth user Admin

(config)# snmp-server host 10.10.10.10 trap version v3 auth user Admin port 2000

(config)# no snmp-server host 10.10.10.10 trap version v3 auth user Admin port 2000

```

## Display commands

### show snmp configuration

#### Syntax

```
show snmp configuration
```

#### Description

This command displays all the SNMP configuration with following information.

-   master agent port
-   community string
-   trap receivers
-   snmpv3 users

#### Authority

Admin User.

#### Parameters

N/A

#### Examples

```
switch# show snmp configuration

     Master Agent :
         Port    : 161 (Default)

     Community Names :
         private
         admin

      Trap Receivers:
      ------------------------------------------------------------------------
      Host            Port      Version  Type      CommunityName   SNMPv3 User
      ------------------------------------------------------------------------
      10.1.1.1        6000      SNMPv1   trap      private            -
      10.1.1.1        162       SNMPv2c  inform    public              -
      10.1.1.1        5000      SNMPv3   inform     -               Admin

     SNMPv3 Users :
     ---------------------------------
      User       AuthMode    PrivMode
     ---------------------------------
      Admin        MD5       AES
      Guest        MD5       AES

```

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

### show snmp-server hosts

#### Syntax

```
show snmp-server hosts
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

  switch# show snmp-server hosts

      Trap Receivers:
      ------------------------------------------------------------------------
      Host            Port      Version  Type      CommunityName   SNMPv3 User
      ------------------------------------------------------------------------
      10.1.1.1        6000      SNMPv1   trap      private            -
      10.1.1.1        162       SNMPv2c  inform    public              -
      10.1.1.1        5000      SNMPv3   inform     -              Admin


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
