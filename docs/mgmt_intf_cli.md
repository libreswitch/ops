# Management Interface Commands

## Contents

- [Management interface configuration commands](#management-interface-configuration-commands)
	- [Management interface context command](#management-interface-context-command)
	- [Static mode configuration](#static-mode-configuration)
	- [DHCP mode configuration](#dhcp-mode-configuration)
	- [Default gateway configuration](#default-gateway-configuration)
	- [Nameserver configuration](#nameserver-configuration)
- [Management interface show commands](#management-interface-show-commands)
	- [show current configuration](#show-current-configuration)
		- [Syntax](#syntax)
		- [Description](#description)
		- [Authority](#authority)
		- [Parameters](#parameters)
		- [Examples](#examples)
	- [Show running configuration](#show-running-configuration)
	- [Show running configuration (interface context)](#show-running-configuration-interface-context)
- [Hostname configuration](#hostname-configuration)
	- [Hostname configuration commands](#hostname-configuration-commands)
	- [Hostname show commands](#hostname-show-commands)
- [Domain name configuration](#domain-name-configuration)
	- [Domain name configuration commands](#domain-name-configuration-commands)
	- [Domain name display commands](#domain-name-display-commands)

## Management interface configuration commands
### Management interface context command
#### Syntax
```
interface mgmt
```
#### Description
Use this command to switch to the management interface configuration context from the config context. All the management interface commands are available in this context only.

#### Authority
Admin user.

#### Parameters
None.

#### Example
```
switch# configure terminal
switch(config)# interface mgmt
switch(config-if-mgmt)#
```
### Static mode configuration

#### Syntax
```
ip static <address>/<mask>
```

#### Description
Use this command to assign a static IP address to the management interface. You can assign both an IPv4 and IPv6 address at the same time.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *address* | Required | A.B.C.D or X:X::X:X | Static IP address in either IPv4 or IPv6 format. Reserved, multicast, broadcast, and loopback addresses are not allowed.|
| *mask* | Required | M | Subnet mask associated with the static address in CIDR format. |


#### Examples
```
switch(config-if-mgmt)# ip static 192.168.1.10/16

switch(config-if-mgmt)# ip static 2001:db8:0:1::129/64
```

### DHCP mode configuration

#### Syntax
```
ip dhcp
```
#### Description
Use this command to enable the DHCP client on the management interface. When enabled, the management interface attempts to retrieve its configuration settings from a DHCP server. If successful, these settings overwrite any statically configured values.

#### Authority
Admin user.

#### Parameters
None.

#### Examples
```
switch(config-if-mgmt)# ip dhcp
```

### Default gateway configuration

#### Syntax
```
[no] default-gateway <gateway-address>
```
#### Description
Use this command to define the default gateway when a static IP address is set on the managment interface. An IPv4 default gateway can be configured only if an IPv4 address is configured on the management interface. An IPv6 default gateway can be configured only if an IPv6 address is configured on the management interface. It is possible to configure both an IPv4 and IPv6 address.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *gateway_address* | Required | A.B.C.D or X:X::X:X | Gateway IP address in either IPv4 or IPv6 format. Reserved IP, Multicast IP, Broadcast IP, and loopback addresses are not allowed.|
| *no* | Optional | Literal | Removes the specified default gateway address.|

#### Examples
```
switch(config-if-mgmt)# default-gateway 192.168.1.5
switch(config-if-mgmt)# default-gateway 2001:db8:0:1::128
switch(config-if-mgmt)# no default-gateway 192.168.1.5
switch(config-if-mgmt)# no default-gateway 2001:db8:0:1::128
```
### Nameserver configuration
#### Syntax
```
[no] nameserver <address-1> [<address-2>]
```
#### Description
Use this command to configure the address of the primary and secondary DNS servers when the management interface is configured with a static IP address. It is possible to configure both IPv4 and IPv6 addresses. It is also possible to configure one DNS server with an IPv4 address and the other one with an IPv6 address. An IPv4 DNS server can be configured only if an IPv4 address is configured on the management interface. An IPv6 DNS server can be configured only if an IPv6 address is configured on the management interface.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *address-1* | Required | A.B.C.D or X:X::X:X | IP address of the primary DNS server in either IPv4 or IPv6 format. Reserved IP, Multicast IP, Broadcast IP, and loopback addresses are not allowed.|
| *address-2* | Required | A.B.C.D or X:X::X:X | IP address of the secondary DNS server in either IPv4 or IPv6 format. Reserved IP, Multicast IP, Broadcast IP, and loopback addresses are not allowed.|
| *no* | Optional | Literal | Removes the specified DNS server. You cannot remove the secondary DNS server without first removing the primary DNS server.|

#### Examples
```
switch(config-if-mgmt)# nameserver 192.168.1.1
switch(config-if-mgmt)# nameserver 192.168.1.2 192.168.1.3
switch(config-if-mgmt)# nameserver 2001:db8:0:1::100
switch(config-if-mgmt)# nameserver 2001:db8:0:2::100 2001:db8:0:3::150
switch(config-if-mgmt)# no nameserver 192.168.1.2 192.168.1.3
switch(config-if-mgmt)# no nameserver 2001:db8:0:2::100 2001:db8:0:3::150
```
## Management interface show commands

### show current configuration

#### Syntax
```
show interface mgmt
```
#### Description
Use this command to display the current configuration of the management interface.

#### Authority
All users.

#### Parameters
None.

#### Examples
```
switch#show interface mgmt
  Address Mode                      : static
  IPv4 address/subnet-mask          : 192.168.1.100/16
  Default gateway IPv4              : 192.168.1.5
  IPv6 address/prefix               : 2001:db8:0:1::129/64
  IPv6 link local address/prefix    : fe80::7272:cfff:fefd:e485/64
  Default gateway IPv6              : 2001:db8:0:1::128
  Primary Nameserver                : 2001:db8:0:2::100
  Secondary Nameserver              : 2001:db8:0:3::150
```

### Show running configuration

#### Syntax
```
show running-config
```

#### Description
Use this command to display the current configuration of the switch.

#### Authority
Admin user.

#### Parameters
None.

#### Examples
The example shows the management interface information in the `show running-config` output.
```
switch# show running-config
  Current configuration:
  !
  hostname "new-name"
  !
  interface mgmt
      ip static 192.168.1.100/16
      ip static 2001:db8:0:1::129/64
      default-gateway 192.168.1.5
      default-gateway 2001:db8:0:1::128
      nameserver 2001:db8:0:2::100 2001:db8:0:3::150
```
### Show running configuration (interface context)

#### Syntax
```
show running-config interface mgmt
```
#### Description
Use this command to display the current configuration of the switch from the interface context.

#### Authority
Admin user.

#### Parameters
None.

#### Examples

```
switch# show running-config interface mgmt
Current configuration:
!
interface mgmt
    ip static 192.168.1.100/16
    ip static 2001:db8:0:1::129/64
    default-gateway 192.168.1.5
    default-gateway 2001:db8:0:1::128
    nameserver 2001:db8:0:2::100 2001:db8:0:3::150
```

## Hostname configuration

### Hostname configuration commands

#### Syntax
```
hostname <name>
no hostname
```
#### Description
Use this command to configure the hostname assigned to the switch. The hostname is shown at the start of each CLI prompt. The default hostname is **switch**.

#### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *name* | Required | String | Hostname starting with a letter and having a maximum length of 32 characters. |
| *no* | Required | Literal | Resets the host name back to the default value **switch**. |


#### Examples
```
switch(config)# hostname new-name
new-name(config)# no hostname
```
### Hostname show commands

#### Syntax
```
show hostname
```
#### Description
Use this command to display the currently configured hostname.

#### Authority
All users.

#### Parameters
None.

#### Examples
```
switch# show hostname
switch
```

## Domain name configuration
### Domain name configuration commands
#### Syntax
```
domain-name <name>
no domain-name
```
#### Description
Use this command to set the domain name of the switch.

#### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *name* | Required | String | Domain name starting with a letter and having a maximum length of 32 characters. |
| *no* | Required | Literal | Removes the domain name. |


#### Examples
```
switch(config)# hostname myswitch
myswitch(config)# domain-name example.com
myswitch(config)# do show domain-name
example.com
myswitch(config)# no domain-name
myswitch(config)# do show domain-name

myswitch(config)#
```
### Domain name display commands
#### Syntax
```
show domain-name
```
#### Description
Use this command to display the domain name currently assigned to the swtich.

#### Authority
All users.

#### Parameters
None.

#### Examples
```
switch(config)# domain-name example.com
switch(config)# exit
switch# show domain-name
example.com
```
