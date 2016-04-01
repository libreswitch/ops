# DHCP Relay CLI Commands

## Contents

- [DHCP relay configuration commands](#dhcp-relay-configuration-commands)
    - [Configure dhcp-relay](#configure-dhcp-relay)
    - [Configure a helper-address](#configure-a-helper-address)
- [DHCP relay option 82 configuration commands](#dhcp-relay-option-82-configuration-commands)
    - [Configure dhcp-relay option 82](#configure-dhcp-relay-option-82)
    - [Unconfigure dhcp-relay option 82](#unconfigure-dhcp-relay-option-82)
    - [Unconfigure response validation for the drop or replace policy of option 82](#unconfigure-response-validation-for-the-drop-or-replace-policy-of-option-82)
- [DHCP relay BOOTP gateway configuration commands](#dhcp-relay-bootp-gateway-configuration-commands)
    - [Configure DHCP relay bootp-gateway](#configure-dhcp-relay-bootp-gateway)
- [DHCP relay hop count increment configuration commands](#dhcp-relay-hop-count-increment-configuration-commands)
    - [Configure dhcp-relay hop-count-increment ](#configure-dhcp-relay-hop-count-increment)
- [DHCP relay show commands](#dhcp-relay-show-commands)
    - [Show dhcp-relay configuration](#show-dhcp-relay-configuration)
    - [Show helper-address configuration](#show-helper-address-configuration)
    - [Show bootp-gateway configuration](#show-bootp-gateway-configuration)
    - [Show running configuration](#show-running-configuration)

## DHCP relay configuration commands
### Configure dhcp-relay
#### Syntax
`[no] dhcp-relay`
#### Description
This command works in the configuration context, and is used to enable/disable the DHCP-relay feature on the device.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-relay
ops-as5712(config)# no dhcp-relay
```
### Configure a helper-address
#### Syntax
`[no] ip helper-address <IPv4-address>`
#### Description
This command is used to configure/unconfigure a remote DHCP server IP address on the device interface. Here the helper address is same as the DHCP server address. A maximum of 16 helper-addresses can be configured per interface.
Even if routing is disabled on an interface, helper address configuration is allowed, but interface DHCP-relay functionality will be inactive. In case a client has received an IP address, and no routing is configured, the IP address is valid on the client until the lease time expires. DHCP-relay is supported only for IPv4.
The helper address configuration is allowed only on data plane interfaces. The helper address should not be multicast or loopback address.
#### Authority
All users.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| *IPv4-address* | Required | A.B.C.D | A DHCP server IP address.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip helper-address 192.168.10.1
ops-as5712(config-if)# ip helper-address 192.168.20.1
ops-as5712(config-if)# no ip helper-address 192.168.10.1
ops-as5712(config-if)# no ip helper-address 192.168.20.1
ops-as5712(config)# interface 2
ops-as5712(config-if)# ip helper-address 192.168.30.1
```

## DHCP relay option 82 configuration commands
### Configure dhcp-relay option 82
#### Syntax
`dhcp-relay option 82 < replace [validate] | drop [validate] | keep | validate [replace | drop  ] >  [ ip | mac ]`
#### Description
This command is used to configure dhcp-relay option 82.
#### Authority
All users.
#### Parameters
Choose one of the parameters from the following table to identify the forward policy of option 82.

| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| *replace* | Required | string | Replaces the existing option 82 field.|
| *keep*    | Required | string | Keeps the existing option 82 field.|
| *drop*    | Required | string | Drops the option 82 packets.|

Choose one of the parameters from the following table to identify the remote ID:

| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| *mac* | Optional | string | Specifies the MAC address of the router.|
| *ip*  | Optional | string | Specifies the IP address of the interface on which the client DHCP packet enters the switch.|

| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| *validate*|Optional| string | Validates the DHCP server responses.|

#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-relay option 82 replace validate mac
```

### Unconfigure dhcp-relay option 82
#### Syntax
`no dhcp-relay option 82`
#### Description
This command is used to unconfigure dhcp-relay option 82.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no dhcp-relay option 82
```

### Unconfigure response validation for the drop or replace policy of option 82
#### Syntax
`no dhcp-relay option 82 validate`
#### Description
This command is used to unconfigure response validation only for the drop/replace policy.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no dhcp-relay option 82
```

## DHCP relay BOOTP gateway configuration commands
### Configure DHCP relay bootp-gateway
#### Syntax
`[no] ip bootp-gateway <IPv4-address>`
#### Description
This command is used to configure/unconfigure a gateway address for the DHCP relay agent
to use for DHCP requests, rather than the DHCP relay agent automatically assigning the lowest-numbered IP address.
This is supported only for IPv4.
The BOOTP gateway configuration is allowed only on data plane interfaces.
#### Authority
All users.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|---------------------------------------|
| *IPv4-address* | Required | A.B.C.D | A gateway address.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip bootp-gateway 1.1.1.1
ops-as5712(config)# interface 2
ops-as5712(config-if)# ip bootp-gateway 1.1.1.2
ops-as5712(config)# interface 3
ops-as5712(config-if)# ip bootp-gateway 1.1.1.3
ops-as5712(config-if)# no ip bootp-gateway 1.1.1.3
```

## DHCP relay hop count increment configuration commands
### Configure dhcp-relay hop-count-increment
#### Syntax
`[no] dhcp-relay hop-count-increment`
#### Description
This command works in the configuration context, and is used to enable/disable the DHCP relay hop count increment feature on the device.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-relay hop-count-increment
ops-as5712(config)# no dhcp-relay hop-count-increment
```
## DHCP relay show commands

### Show dhcp-relay configuration
#### Syntax
`show dhcp-relay`
#### Description
This command is used to display the DHCP relay configuration.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show dhcp-relay

 DHCP Relay Agent                 : Enabled
 DHCP Request Hop Count Increment : Enabled
 Option 82                        : Disabled
 Response Validation              : Disabled
 Option 82 Handle Policy          : replace
 Remote ID                        : mac

 DHCP Relay Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  60         10         60         10

  DHCP Relay Option 82 Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  50         8          50         8
```

### Show helper-address configuration
#### Syntax
`show ip helper-address [interface <interface-name>]`
#### Description
This command is used to display the DHCP relay helper-address configuration.
#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *interface* | Optional | IFNAME | The name of the interface.|
#### Examples
```
ops-as5712# show ip helper-address
 IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
  192.168.20.1
  192.168.10.1

 Interface: 2
  IP Helper Address
  -----------------
  192.168.10.1

ops-as5712# show ip helper-address interface 1
 IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
  192.168.20.1
  192.168.10.1

```

### Show bootp-gateway configuration
#### Syntax
`show dhcp-relay bootp-gateway [interface <interface-name>]`
#### Description
This command is used to display the DHCP relay BOOTP gateway configuration.
#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *interface* | Optional | IFNAME | The name of the interface.|
#### Examples
```
ops-as5712# show dhcp-relay bootp-gateway

 BOOTP Gateway Entries

 Interface            BOOTP Gateway
 -------------------- ---------------
 1                    1.1.1.1
 2                    1.1.1.2

ops-as5712# show ip helper-address interface 1
 BOOTP Gateway Entries

 Interface            BOOTP Gateway
 -------------------- ---------------
 1                    1.1.1.1

```

### Show running configuration
#### Syntax
`show running-config`
#### Description
This command displays the current non-default configuration on the switch.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show running-config
Current configuration:
!
!
!
no dhcp-relay
no dhcp-relay hop-count-increment
interface 1
    helper-address 192.168.10.1
    helper-address 192.168.20.1
    ip bootp-gateway 1.1.1.1
interface 2
    helper-address 192.168.10.1
    ip bootp-gateway 1.1.1.2

```