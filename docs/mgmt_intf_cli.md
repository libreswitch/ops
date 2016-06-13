# Management Interface Commands

## Contents
- [Configuration commands](#configuration-commands)
	- [interface mgmt](#interface-mgmt)
	- [ip static](#ip-static)
	- [ip dhcp](#ip-dhcp)
	- [default-gateway](#default-gateway)
	- [nameserver](#nameserver)
- [Display commands](#display-commands)
	- [show interface mgmt](#show-interface-mgmt)
	- [show running-config](#show-running-config)
	- [show running-config interface mgmt](#show-running-config-interface-mgmt)
- [Hostname commands](#hostname-commands)
	- [hostname](#hostname)
	- [show hostname](#show-hostname)
- [Domain name commands](#domain-name-commands)
	- [domain-name](#domain-name)
	- [show domain-name](#show-domain-name)


## Configuration commands

### interface mgmt

#### Syntax
```
interface mgmt
```

#### Description
Switches to management interface configuration mode from configuration mode. All the management interface commands are available in this mode only.

#### Command mode
Configuration mode (config).

#### Authority
Admin.

#### Parameters
None.

#### Example

###### Switching to management interface mode
```
switch(config)# interface mgmt
switch(config-if-mgmt)#
```


### ip static

#### Syntax
```
ip static <address>/<mask>
```

#### Description
Assigns a static IP address to the management interface. You can assign both an IPv4 and IPv6 address at the same time.

#### Command mode
Management interface mode (config-if-mgmt).

#### Authority
Admin.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *address* | Required | String | Static IP address in either IPv4 format (A.B.C.D), or IPv6 format (X:X::X:X). Reserved, multicast, broadcast, and loopback addresses are not allowed.|
| *mask* | Required | Integer | Subnet mask associated with the static address in CIDR format. |

#### Examples

###### Setting an IPv4 address on the management interface
```
switch(config-if-mgmt)# ip static 192.168.1.10/16
```

###### Setting an IPv6 address on the management interface
```
switch(config-if-mgmt)# ip static 2001:db8:0:1::129/64
```


### ip dhcp

#### Syntax
```
ip dhcp
```

#### Description
Enables the DHCP client on the management interface. When enabled, the management interface attempts to retrieve its configuration settings from a DHCP server. If successful, these settings overwrite any statically configured values.

#### Command mode
Management interface mode (config-if-mgmt).

#### Authority
Admin.

#### Parameters
None.

#### Example

###### Enabling DHCP on the management interface
```
switch(config-if-mgmt)# ip dhcp
```


### default-gateway

#### Syntax
```
default-gateway <gateway-address>
no default-gateway <gateway-address>
```

#### Description
Defines the default gateway when a static IP address is set on the management interface. An IPv4 default gateway can be configured only if an IPv4 address is configured on the management interface. An IPv6 default gateway can be configured only if an IPv6 address is configured on the management interface. It is possible to configure both an IPv4 and IPv6 address.

Use the `no` form of this command to remove a default gateway.

#### Command mode
Management interface mode (config-if-mgmt).

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *gateway_address* | Required | String | Gateway IP address in either IPv4 format (A.B.C.D), or IPv6 format (X:X::X:X). Reserved IP, Multicast IP, Broadcast IP, and loopback addresses are not allowed.|

#### Examples

###### Setting the default gateway using IPv4
```
switch(config-if-mgmt)# default-gateway 192.168.1.5
```

###### Setting the default gateway using IPv6
```
switch(config-if-mgmt)# default-gateway 2001:db8:0:1::128
```

###### Removing the default gateway using IPv4
```
switch(config-if-mgmt)# no default-gateway 192.168.1.5
```

###### Removing the default gateway using IPv6
```
switch(config-if-mgmt)# no default-gateway 2001:db8:0:1::128
```


### nameserver

#### Syntax
```
nameserver <address-1> [<address-2>]
no nameserver <address-1> [<address-2>]
```
#### Description
Configures the address of the primary and secondary DNS servers when the management interface is configured with a static IP address. It is possible to configure both IPv4 and IPv6 addresses. It is also possible to configure one DNS server with an IPv4 address and the other one with an IPv6 address. An IPv4 DNS server can be configured only if an IPv4 address is configured on the management interface. An IPv6 DNS server can be configured only if an IPv6 address is configured on the management interface.

Use the `no` form of this command to remove a DNS server. You cannot remove the secondary DNS server without first removing the primary DNS server.

#### Command mode
Management interface mode (config-if-mgmt).

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *address-1* | Required | String | IP address of the primary DNS server in either IPv4 format (A.B.C.D), or IPv6 format (X:X::X:X). Reserved, multicast, broadcast, and loopback addresses are not allowed.|
| *address-2* | Required | String | IP address of the primary DNS server in either IPv4 format (A.B.C.D), or IPv6 format (X:X::X:X). Reserved, multicast, broadcast, and loopback addresses are not allowed.|

#### Examples

###### Setting the primary DNS server using IPv4
```
switch(config-if-mgmt)# nameserver 192.168.1.1
```

###### Setting the primary and secondary DNS server using IPv4
```
switch(config-if-mgmt)# nameserver 192.168.1.2 192.168.1.3
```

###### Setting the primary DNS server using IPv6
```
switch(config-if-mgmt)# nameserver 2001:db8:0:1::100
```

###### Setting the primary and secondary DNS server using IPv6
```
switch(config-if-mgmt)# nameserver 2001:db8:0:2::100 2001:db8:0:3::150
```

###### Removing the primary and secondary DNS server using IPv4
```
switch(config-if-mgmt)# no nameserver 192.168.1.2 192.168.1.3
```

###### Removing the primary and secondary DNS server using IPv6
```
switch(config-if-mgmt)# no nameserver 2001:db8:0:2::100 2001:db8:0:3::150
```




## Display commands

### show interface mgmt

#### Syntax
```
show interface mgmt
```

#### Description
Displays the current configuration of the management interface.

#### Command mode
Enable mode.

#### Authority
All users.

#### Parameters
None.

#### Example
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


### show running-config

#### Syntax
```
show running-config
```

#### Description
Use this command to display the current configuration of the switch.

#### Command mode
Enable mode.

#### Authority
Admin.

#### Parameters
None.

#### Example
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


### show running-config interface mgmt

#### Syntax
```
show running-config interface mgmt
```

#### Description
Displays the current configuration of the switch from interface mode.

#### Command mode
Enable mode.

#### Authority
Admin.

#### Parameters
None.

#### Example

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

## Hostname commands

### hostname

#### Syntax
```
hostname <name>
no hostname
```

#### Description
Configures the hostname assigned to the switch. The hostname is shown as part of each CLI prompt. The default hostname is `switch`.

Use the `no` form of this command to set the hostname to the default value.

#### Command mode
Enable mode.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *name* | Required | String | Hostname starting with a letter and having a maximum length of 32 characters. |

#### Example

###### Setting and then removing the host name "new-name"
```
switch(config)# hostname new-name
new-name(config)# no hostname
```


### show hostname

#### Syntax
```
show hostname
```

#### Description
Displays the currently configured hostname.

#### Command mode
Enable mode.

#### Authority
All users.

#### Parameters
None.

#### Example
```
switch# show hostname
switch
```

## Domain name commands

### domain-name

#### Syntax
```
domain-name <name>
no domain-name
```

#### Description
Sets the domain name of the switch.

Use the `no` form of this command to remove the domain name.

#### Command mode
Configuration mode (config).

#### Authority
Admin.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *name* | Required | String | Domain name starting with a letter and having a maximum length of 32 characters. |

#### Examples

###### Setting the domain name to "example.com"
```
switch(config)# domain-name example.com
switch(config)# do show domain-name
example.com
```

###### Removing the domain
```
switch(config)# no domain-name
switch(config)# do show domain-name

switch(config)#
```
Note: The `do` options runs a command in the enable mode.


### show domain-name

#### Syntax
```
show domain-name
```

#### Description
Displays the domain name currently assigned to the switch.

#### Command mode
Enable mode.

#### Authority
All users.

#### Parameters
None.

#### Example

###### Setting the domain to "example.com" and then displaying it
```
switch(config)# domain-name example.com
switch(config)# exit
switch# show domain-name
example.com
```
