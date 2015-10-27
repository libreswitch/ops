 # Loopback Interface Commands

- [Configuration commands](#configuration-commands)
	- [Create loopback interface](#create-loopback-interface)
	- [Delete loopback interface](#delete-loopback-interface)
	- [Set/Unset IPv4 address](#setunset-ipv4-address)
	- [Set or unset IPv6 addresses](#set-or-unset-ipv6-addresses)
- [Display commands](#display-commands)
	- [Show running configuration](#show-running-configuration)
	- [Show loopback interfaces](#show-loopback-interfaces)
	- [Show loopback interface](#show-loopback-interface)
- [References](#references)
<!-- /TOC -->

## Configuration commands
### Create loopback interface
#### Syntax
```
interface loopback instance
```
#### Description
This command creates a loopback interface and enters loopback configuration mode.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax |	Description |
|-----------|----------|----------------------|
| **instance** | Required | Integer | loopback interface ID 1 to 2147483647 |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface loopback 1
ops-as5712(config-loopback-if)#
```
###  Delete loopback interface
#### Syntax
```
no interface loopback instance
```
#### Description
This command deletes a loopback interface.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax |	Description |
|-----------|----------|----------------------|
| **instance** | Required | Integer | loopback interface ID 1 to 2147483647 |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no interface loopback 1
```
###  Set/Unset IPv4 address
#### Syntax
```
[no] ip address <ipv4_address/prefix-length>
```
#### Description
This command sets the IPv4 address for a loopback interface.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv4_address/prefix-length* | Required | A.B.C.D/M | IPv4 address with prefix-length for the loopback interface |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface loopback 1
ops-as5712(config-loopback-if)# ip address 16.93.50.2/24
```
### Set or unset IPv6 addresses
#### Syntax
```
[no] ip address <ipv6_address/prefix-length>
```
#### Description
This command sets the IPv6 address for a loopback interface.
#### Authority
All Users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv6_address/prefix-length* | Required | X:X::X:X/P | IPv6 address with prefix-length for the loopback interface |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface loopback 1
ops-as5712(config-loopback-if)# ipv6 address fd00:5708::f02d:4df6/64
```
##Display commands
### Show running configuration
#### Syntax
`show running-config`
#### Description
This command displays all loopback interfaces.
#### Authority
All users
#### Examples
```
ops-as5712# show running-config
.............................
.............................
interface loopback 1
    no shutdown
    ip address 192.168.1.1/24
interface loopback 2
    no shutdown
    ip address 182.168.1.1/24
.............................
.............................
```
### Show loopback interfaces
#### Syntax
`show interface loopback [brief]`
#### Description
This command displays all configured loopback interfaces.
#### Authority
All users
#### Parameters
None
#### Examples
```
ops-as5712# show interface loopback
 Interface loopback 1 is up
 Admin state is up
 Hardware is Loopback
 IPv4 address 192.168.1.1/24
 Interface loopback 2 is up
 Admin state is up
 Hardware is Loopback
 IPv4 address 182.168.1.1/24
ops-as5712# show interface loopback brief
....................................................................................................
Loop         IPv4 Address    Status
Interface
...................................................................................................
  1          192.168.1.1/24    up
  2          192.168.1.2/24    up
```
### Show loopback interface
#### Syntax
`show interface loopback instance`
#### Description
This command displays the configuration and status of a loopback interface.
#### Authority
All users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **instance** | Required | Integer | loopback interface ID 1 to 2147483647 |
#### Examples
```
ops-as5712# show interface loopback 1
 Interface loopback 1 is up
 Admin state is up
 Hardware is Loopback
 IPv4 address 192.168.1.1/24
```
## References
* [Reference 1]`interface_cli.md`
* [Reference 2]`loopback_interface_design.md`
