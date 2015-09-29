# Interface VLAN

## Contents
- [Configuration commands](#configuration-commands)
	- [interface vlan](#interface-vlan)
	- [interface](#interface)
- [Display commands](#display-commands)
	- [show interface](#show-interface)

## Configuration commands

###  interface vlan

##### Syntax
Under the config context.

`[no] interface vlan <vlan-id>`

##### Description
This command lets you access the interface VLAN configuration corresponding to the specified VLAN ID.

##### Authority
Admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-id*  | Required. |1-4094 |	The VLAN ID |
| **no** | Optional | Literal | Removes the VLAN interface corresponding to the specified VLAN ID |

##### Example

```
hostname(config)# interface vlan 101
hostname(config-if-vlan)#
```

###  interface

##### Syntax

Under the config context

`[no] interface <vlan-name>`

##### Description
This command lets you access the interface VLAN configuration corresponding to the specified VLAN name.

##### Authority
Admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-name*  | Required. |String. |	The VLAN name |
| **no** | Optional | Literal | Removes the VLAN interface corresponding to the specified VLAN name |

##### Example

```
hostname(config)# interface vlan101
hostname(config-if-vlan)#
```

## Display commands

### show interface

##### Syntax
Under privileged mode.

`show interface <vlan-name>`

#### Description
This command displays the interface VLAN configuration.

#### Authority
Operator

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *vlan-name*  | Required. |String. |	The VLAN name. |

##### Example
The following example displays the VLAN interface configuration for VLAN: vlan101:
```
hostname# show interface vlan101

Interface vlan101 is down (Administratively down)
 Admin state is down
 Hardware: Ethernet, MAC Address: 48:0f:cf:af:02:17
```
