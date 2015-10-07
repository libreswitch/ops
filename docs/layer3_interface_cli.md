# L3 Interfaces

## Contents

- [Configuration commands](#configuration-commands)
	- [routing](#routing)
	- [vrf attach](#vrf-attach)
	- [ip address](#ip-address)
	- [ipv6 address](#ipv6-address)
	- [interface vlan](#interface-vlan)
	- [interface](#interface)
- [Display commands](#display-commands)
	- [show interface](#show-interface)
	- [show interface vlan-name](#show-interface-vlan-name)


## Configuration commands

### routing

#### Syntax
Under the interface context.

`[no] routing`

#### Description
Enable/disable routing for the interface.

#### Authority
Admin.

#### Parameters
None.

#### Example
```
hostname(config-if)# routing
hostname(config-if)#
```

### vrf attach

#### Syntax
Under the interface context.

`[no] vrf attach <vrf-name>`

#### Description
Attach/detach an interface to/from a VRF.

#### Authority
Admin.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|--------|------------------------|
| *vrf-name*  | Required | String |  The name of the VRF. |

#### Example
Attach an interface to a VRF (interface: 1, VRF: myVRF)
```
hostname(config)# interface 1
hostname(config-if)# vrf attach myVRF
hostname(config-if)#
```

### ip address

#### Syntax
Under the interface context.

`[no] ip address <address/mask> [secondary]`

#### Description
Configures an IPv4 address to the specified interface.

#### Authority
Admin.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|--------|------------------------|
| *address/mask*  | Required |A.B.C.D/M | The address and mask. |
| **secondary**  | Optional | Literal | Configures a secondary address.|


#### Example
Configures an IPv4 address on the interface.
```
hostname(config-if)# interface 1
hostname(config-if)# ip address 172.16.100.10/24
hostname(config-if)#
```

### ipv6 address

#### Syntax
Under the interface context.

`[no] ipv6 address <address/prefix> [secondary]`

#### Description
Configures an IPv6 address to the specified interface.

#### Authority
Admin.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|--------|------------------------|
| *address/prefix*  | Required |X:X::X:X/P | The address and prefix length.|
| **secondary**  | Optional | Literal | Configures a secondary address.|


#### Example
Configures an IPv6 address on the interface.
```
hostname(config)# interface 1
hostname(config-if)# ipv6 address fd00:5708::f02d:4df6/64
hostname(config-if)#
```

### interface vlan

#### Syntax
Under the config context.

`[no] interface vlan <vlan-id>`

#### Description
This command lets you create and configure a L3 VLAN interface corresponding to the specified VLAN ID.

#### Authority
Admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-id*  | Required  |1-4094 |	The VLAN ID |
| **no** | Optional | Literal | Removes the VLAN interface corresponding to the specified VLAN ID |

#### Example

```
hostname(config)# interface vlan 101
hostname(config-if-vlan)#
```

### interface

#### Syntax

Under the config context

`[no] interface <vlan-name>`

#### Description
This command lets you create and configure a L3 VLAN interface corresponding to the specified VLAN name.

#### Authority
Admin

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-name*  | Required  |String  |	The VLAN name |
| **no** | Optional | Literal | Removes the VLAN interface corresponding to the specified VLAN name |

#### Example

```
hostname(config)# interface vlan101
hostname(config-if-vlan)#
```

## Display commands

### show interface

#### Syntax
Under privileged mode.

`show interface [brief | mgmt]`

#### Description
Displays information for the interfaces including statistics, configuration and interface state.

#### Authority
Operator.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|--------|------------------------|
| **brief**   | Optional | Literal | Displays brief information of the interfaces.|
| **mgmt**   | Optional | Literal | Displays the management interface details.|

#### Example

Show management interface details
```
hostname# show interface mgmt
  Address Mode                  : dhcp
  IPv4 address/subnet-mask      : 120.92.216.83/25
  Default gateway IPv4          : 120.92.216.1
  IPv6 address/prefix           :
  IPv6 link local address/prefix: fe80::4a0f:cfff:feaf:216/64
  Default gateway IPv6          :
  Primary Nameserver            :
  Secondary Nameserver          :
```
Show specific interface in detail mode (interface: 1)
```
hostname# show interface 1

Interface 1 is up
 Admin state is up
 Hardware: Ethernet, MAC Address: 48:0f:cf:af:02:17
 MTU 1500
 Full-duplex
 Speed 1000 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RX
            0 input packets              0 bytes
            0 input error                0 dropped
            0 short frame                0 overrun
            0 CRC/FCS
 TX
            0 output packets             0 bytes
            0 input error               21 dropped
            0 collision
```
Show specific interface in brief mode (interface: 1)
```
hostname# show interface 1 brief

--------------------------------------------------------------------------------
Ethernet      VLAN    Type Mode   Status  Reason                   Speed     Port
Interface                                                          (Mb/s)    Ch#
--------------------------------------------------------------------------------
 1            --      eth  --     up                               1000     --
```

### show interface vlan-name

#### Syntax
Under privileged mode.

`show interface <vlan-name>`

#### Description
This command displays the interface VLAN configuration.

#### Authority
Operator

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-name*  | Required  |String  |	The VLAN name. |

#### Example
The following example displays the VLAN interface configuration for VLAN: vlan101:
```
hostname# show interface vlan101

Interface vlan101 is down (Administratively down)
 Admin state is down
 Hardware: Ethernet, MAC Address: 48:0f:cf:af:02:17
```
