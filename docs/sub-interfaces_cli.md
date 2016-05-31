# L3 Subinterfaces Commands

## Contents

- [Configuration commands](#configuration-commands)
	- [Create subinterface](#create-subinterface)
	- [Delete subinterface](#delete-subinterface)
	- [Set or unset IPv4 addresses](#set-or-unset-ipv4-addresses)
	- [Set or unset IPv6 addresses](#set-or-unset-ipv6-addresses)
	- [Set or unset an IEEE 802.1Q VLAN encapsulation](#set-or-unset-an-ieee-8021q-vlan-encapsulation)
	- [Enable interface](#enable-interface)
	- [Disable interface](#disable-interface)
- [Display commands](#display-commands)
	- [Show running configuration](#show-running-configuration)
	- [Show subinterfaces](#show-subinterfaces)
	- [Show subinterface](#show-subinterface)
- [References](#references)

## Configuration commands
###  Create subinterface
#### Syntax
```
interface L3_interface.subinterface
```
#### Description
This command creates a subinterface on an L3 interface and enters subinterface configuration mode.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax |	Description |
|-----------|----------|----------------------|
| **L3_interface** | Required | System defined | Name of the interface. System defined.  |
| **subinterface** | Required | Integer | Subinterface ID from 1 to 4294967293|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1.1
ops-as5712(config-subif)#
```
###  Delete subinterface
#### Syntax
```
no interface L3_interface.subinterface
```
#### Description
This command deletes a subinterface from an L3 interface.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax |	Description |
|-----------|----------|----------------------|
| **L3_interface** | Required | System defined | Name of the interface. System defined.  |
| **subinterface** | Required | Integer | Subinterface ID from 1 to 4294967293 |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no interface 1.1
```
### Set or unset IPv4 addresses
#### Syntax
```
[no] ip address <ipv4_address/prefix-length>
```
#### Description
This command sets or unsets the IPv4 address for a subinterface.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv4_address/prefix-length* | Required | A.B.C.D/M | IPV4 address with prefix-length for the subinterface |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1.1
ops-as5712(config-subif)# ip address 16.93.50.2/24
```
###  Set or unset IPv6 addresses
#### Syntax
```
[no] ipv6 address <ipv6_address/prefix-length>
```
#### Description
This command sets or unsets the IPv6 address for a subinterface.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv6_address/prefix-length* | Required | X:X::X:X/P | IPV6 address with prefix-length for the subinterface |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1.1
ops-as5712(config-subif)# ipv6 address fd00:5708::f02d:4df6/64
```
### Set or unset an IEEE 802.1Q VLAN encapsulation
#### Syntax
```
[no] encapsulation dot1Q  vlan-id
```
#### Description

There is no need to remove the old VLAN ID with the "no" option. Instead, enter the VLAN command with a different VLAN ID.
#### Authority
All users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlan-id* | Required | 1 - 4094  | Represents VLAN and takes values from 1 to 4094|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1.1
ops-as5712(config-subif)#encapsulation dot1Q 33
```
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1.1
ops-as5712(config-subif)#no encapsulation dot1Q 33
```
### Enable interface
#### Syntax
`no shutdown`
#### Description
This command enables a subinterface.
#### Authority
All Users
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1.1
ops-as5712(config-subif)# no shutdown
```
### Disable interface
#### Syntax
`shutdown`
#### Description
This command disables a subinterface.
#### Authority
All Users
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1.1
ops-as5712(config-if)# shutdown
```
## Display commands
### Show running configuration
#### Syntax
`show running-config`
#### Description
This command displays all configured subinterfaces.
#### Authority
All users
#### Examples
```
ops-as5712# show running-config
.............................
.............................
interface 1.1
    no shutdown
    ip address 192.168.1.1/24
interface 1.2
    no shutdown
    ip address 182.168.1.1/24
    encapsulation dot1Q 44
.............................
.............................
```
### Show subinterfaces
#### Syntax
`show interface <L3_interface> sub-interface [brief]`
#### Description
This command displays all configured subinterfaces. This command also optionally displays a particular L3 interface.
#### Authority
All users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **L3_interface** | Required | System defined | Name of the interface. System defined.  |
| **brief** | Optional| Literal  | Formats the output in tabular form.
#### Examples
```
ops-as5712# show interface 1 sub-interface
Interface 1.1 is down(Parent Interface Admin down)
 Admin state is down
 parent interface is 1
 encapsulation dot1Q 33
 Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
 IPv4 address 192.168.1.1/2
 Input flow-control is off, output flow-control is off
 RX
      0 input packets     0 bytes
      0 input error       0 dropped
      0 CRC/FCS
 TX
      0 output packets  0 bytes
      0 input error     0 dropped
      0 collision
Interface 1.2 is down(Parent Interface Admin down))
 Admin state is down
 parent interface is 1
 encapsulation dot1Q 44
 Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
 IPv4 address 182.168.1.1/2
 Input flow-control is off, output flow-control is off
 RX
      0 input packets     0 bytes
      0 input error       0 dropped
      0 CRC/FCS
 TX
      0 output packets  0 bytes
      0 input error     0 dropped
      0 collision

ops-as5712# show interface 1 sub-interface brief
....................................................................................................
Sub         VLAN   Type   Mode    Status   Reason                    Speed     Port
Interface                                                            (Mb/s)    Ch#
...................................................................................................
  1.1        33    eth     ..     down    Administratively down       auto     ..
  1.2        44    eth     ..     down    Administratively down       auto     ..
```
### Show subinterface
#### Syntax
`show interface <L3_interface.subinterface> [brief]`
#### Description
This command displays the configuration and status of a subinterface.
#### Authority
All users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **L3_interface** | Required | System defined | Name of the interface. System defined.  |
| **subinterface** | Required | Integer | Subinterface ID from 1 to 1024 |
| **brief** | Optional| Literal  | Formats the output in tabular form. |
#### Examples
```
ops-as5712# show interface 1.1
Interface 1.1 is down(Parent Interface Admin down)
 Admin state is down
 parent interface is 1
 encapsulation dot1Q 33
 Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
 IPv4 address 182.168.1.1/2
 Input flow-control is off, output flow-control is off
 RX
      0 input packets     0 bytes
      0 input error       0 dropped
      0 CRC/FCS
 TX
      0 output packets  0 bytes
      0 input error     0 dropped
      0 collision
ops-as5712# show interface 1.1 brief
....................................................................................................
Sub         VLAN   Type   Mode    Status   Reason                    Speed     Port
Interface                                                            (Mb/s)    Ch#
...................................................................................................
  1.1        33    eth     ..     down    Administratively down       auto     ..
```

##Supportability Commands
###Display event logs
####Syntax
show events category subinterface
####Description
This command displays all the events logged by sub-interfaces.

Following events will be logged for sub-interfaces.
- Create subinterface.
- Configure subinterface with IPv4 address.
- Configure subinterface with IPv6 address.
- Configure subinterface with encapsulation dot 1Q vlan ID.
- Configure subinterface with admin up.
- Configure subinterface with admin down.
- Remove IPv4 address.
- Remove IPv6 address.
- Remove encapsulation dot 1Q vlan ID.
- Delete subinterface.

####Authority
All users
####Examples
```
switch# show events category subinterafce
2016-05-31:06:26:27.363923|ops-portd|10001|LOG_INFO|Sub-Interface 4.5, created
2016-05-31:07:08:51.351755|ops-portd|10001|LOG_INFO|Sub-Interface 4.4, created
2016-05-31:07:08:57.418705|ops-portd|10003|LOG_INFO|Sub-Interface 4.4, configured with ip address 10.1.1.1/24
```
###Daignostic Dump
####Syntax
diag-dump subinterface basic
####Description
This command will dump number of created subinterfaces.
####Authority
All users
####Examples
```
switch# diag-dump subinterface basic
=========================================================================
[Start] Feature subinterface Time : Tue May 31 07:19:57 2016

=========================================================================
-------------------------------------------------------------------------
[Start] Daemon ops-portd
-------------------------------------------------------------------------
Number of Configured sub-interfaces are : 2.

-------------------------------------------------------------------------
[End] Daemon ops-portd
-------------------------------------------------------------------------
=========================================================================
[End] Feature subinterface
=========================================================================
```
##References
* [Reference 1]`interface_cli.md`
* [Reference 2]`sub-interface_design.md`
