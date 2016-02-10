# DHCP-Relay CLI Commands

## Contents

- [DHCP-Relay configuration commands](#dhcp-relay-configuration-commands)
    - [Configure dhcp-relay](#configure-dhcp-relay)
    - [Configure a helper-address](#configure-a-helper-address)
- [DHCP-Relay show commands](#dhcp-relay-show-commands)
    - [Show dhcp-relay configuration](#show-dhcp-relay-configuration)
    - [Show helper-address configuration](#show-helper-address-configuration)
    - [Show running configuration](#show-running-configuration)

## DHCP-Relay configuration commands
### Configure dhcp-relay
#### Syntax
`[no] dhcp-relay`
#### Description
This command works in the configuration context, and is used to enable/disable the DHCP-Relay feature on the device.

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
The helper address configuration is allowed only on data plane interfaces.
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
## DHCP-Relay show commands

### Show dhcp-relay configuration
#### Syntax
`show dhcp-relay`
#### Description
This command is used to display dhcp-relay configuration.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show dhcp-relay
  DHCP Relay Agent        : Enabled
```
### Show helper-address configuration
#### Syntax
`show ip helper-address [interface <interface-name>]`
#### Description
This command is used to display DHCP-Relay helper-address configuration.
#### Authority
All users.

#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *interface* | Optional | IFNAME | Name of the interface.|
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
### Show running configuration
#### Syntax
`show running-config
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
interface 1
    helper-address 192.168.10.1
    helper-address 192.168.20.1
interface 2
    helper-address 192.168.10.1

```
