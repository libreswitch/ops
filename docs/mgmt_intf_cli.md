# Configuration support for management interface

## Contents

- [Management interface configuration commands](#management-interface-configuration-commands)
	- [Management interface context command](#management-interface-context-command)
	- [Static mode configuration](#static-mode-configuration)
	- [DHCP mode configuration](#dhcp-mode-configuration)
	- [Default gateway configuration](#default-gateway-configuration)
	- [Nameserver configuration](#nameserver-configuration)
- [Management interface show commands](#management-interface-show-commands)
	- [show command](#show-command)
	- [Show running configuration](#show-running-configuration)
	- [Show running configuration from interface level](#show-running-configuration-from-interface-level)
- [Hostname configuration](#hostname-configuration)
	- [Hostname configuration commands](#hostname-configuration-commands)

## Management interface configuration commands
### Management interface context command
This command is used to switch to the management interface context.
#### Syntax
```
interface mgmt
```
#### Description
This command is used to switch to the management interface. All the management interface commands are available in this context only.
#### Authority
Admin
#### Parameters
None

#### Examples
```
	(conf #) interface mgmt
```
### Static mode configuration
This command is used to configure the management interface mode as static.
#### Syntax
```
ip static { ipv4/subnet-mask | ipv6/subnet-mask}
```
#### Description
This command is used to configure the IP address of the management interface. Both Ipv4 and IPv6 addresses are supported. The subnet mask is specified in CIDR format for both IPv4 and Ipv6 addresses.
#### Authority
Admin
#### Parameters
This command is executed in the management interface context.

The user can configure all valid IPv4 and IPv6 addresses. Reserved IP, Multicast IP, Broadcast IP, and loopback addresses are not allowed. However, only one IP address can be configured per address family.
#### Examples
```
	as5712(config-if-mgmt)#ip static 192.168.1.10/16

	as5712(config-if-mgmt)#ip static 2001:db8:0:1::129/64
```
### DHCP mode configuration
This command configures the management interface mode as DHCP.
#### Syntax
```
ip dhcp
```
#### Description
When the mode is set to dhcp, the IP and other management interface attributes are received from the DHCP server. Any static configuration set up earlier is removed when the mode is changed to dhcp.
#### Authority
Admin
#### Parameters
None
#### Examples
```
	as5712(config-if-mgmt)#ip dhcp
```
### Default gateway configuration
This command configures the IPv4 and IPv6 default gateway.
#### Syntax
```
[no] default-gateway {ipv4-address | ipv6-address}
```
#### Description
The default gateway configuration is allowed only in static mode. An IPv4 default gateway can be configured only if an IPv4 address is configured on the management interface. An IPv6 default gateway can be configured only if an IPv6 address is configured on the management interface. It is possible to configure both IPv4 and IPv6 addresses.
#### Authority
Admin
#### Parameters
This command is executed in the management interface context.

All valid IPv4 and IPv6 addresses can be configured. Reserved IP, Multicast IP, Broadcast IP, and loopback addresses are not allowed.
However, only one IP can be configured per address family.

When “no” is specified, the default gateway is removed. If the user tries to remove a default gateway that was not configured, an error message is displayed.
#### Examples
```
	as5712(config-if-mgmt)#default-gateway 192.168.1.5
	as5712(config-if-mgmt)#default-gateway 2001:db8:0:1::128
	as5712(config-if-mgmt)#no default-gateway 192.168.1.5
	as5712(config-if-mgmt)#no default-gateway 2001:db8:0:1::128
```
### Nameserver configuration
This command configures the nameserver.
#### Syntax
```
[no] nameserver address-1 [address-2]
```
#### Description
The nameserver configuration is allowed in static mode only. It is possible to configure both IPv4 and IPv6 addresses. It is also possible to configure one nameserver as IPv4 address and the other one as IPv6 address. An IPv4 nameserver can be configured only if an IPv4 address is configured on the management interface. An IPv6 nameserver can be configured only if an IPv6 address is configured on the management interface.
#### Authority
Admin
#### Parameters
This command is executed in the management interface context.

All valid IPv4 and IPv6 address can be configured. Reserved IP, Multicast IP, Broadcast IP, and loopback addresses are not allowed.

Address-1 is configured as the primary nameserver and Address-2 (if specified) is configured as the secondary nameserver.

When "no" is specified the namserver targeted is removed. If the user tries to remove a nameserver that is not configured, an error message is displayed. It is not possible to remove the secondary nameserver without removing the primary nameserver.
#### Examples
```
	as5712(config-if-mgmt)#nameserver 192.168.1.1
	as5712(config-if-mgmt)#nameserver 192.168.1.2 192.168.1.3
	as5712(config-if-mgmt)#nameserver 2001:db8:0:1::100
	as5712(config-if-mgmt)#nameserver 2001:db8:0:2::100 2001:db8:0:3::150
	as5712(config-if-mgmt)#no nameserver 192.168.1.2 192.168.1.3
	as5712(config-if-mgmt)#no nameserver 2001:db8:0:2::100 2001:db8:0:3::150
```
## Management interface show commands
### show command
#### Syntax
```
show interface mgmt
```
#### Description
The show command displays the management interface attributes such as IP, subnet, default gateway, and nameserver.
#### Authority
all users
#### Parameters
None
#### Examples
```
	as5712#show interface mgmt
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
This command displays the switch configuration.
#### Authority
admin
#### Parameters
None
#### Examples
The example shows the management interface information in the `show running-config` output.
```
	as5712# show running-config
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
### Show running configuration from interface level
#### Syntax
```
show running-config interface mgmt
```
#### Description
This command displays the switch configuration at the interface level.
#### Authority
admin
#### Parameters
None
#### Examples

```
	as5712# show running-config interface mgmt
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
These commands are used to configure the system hostname.
#### Syntax
```
hostname <name>
no hostname
```
#### Description
Command "hostname <name>" is used to configure the hostname of the system through CLI. Command "no hostname" reconfigures the system hostname to default value "switch".
#### Authority
Admin
#### Parameters
User can configure hostname as alphanumeric string. First letter must be alphabet and the maximum length of the string can be 32.
#### Examples
```
    switch(config)#hostname new-name
    new-name(config)#no hostname
    switch(config)#

```
