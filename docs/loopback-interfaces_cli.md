 # Loopback Interface Commands

## Contents

- [Configuration commands](#configuration-commands)
	- [Create loopback interface](#create-loopback-interface)
	- [Delete loopback interface](#delete-loopback-interface)
	- [Set/Unset IPv4 address](#setunset-ipv4-address)
	- [Set or unset IPv6 addresses](#set-or-unset-ipv6-addresses)
- [Display commands](#display-commands)
	- [Show running configuration](#show-running-configuration)
	- [Show loopback interfaces](#show-loopback-interfaces)
	- [Show loopback interface](#show-loopback-interface)
- [Supportability Commands](#supportability-commands)
	- [Display event logs](#display-event-logs)
	- [Daignostic Dump](#daignostic-dump)
	- [show tech command](#show-tech-command)
- [References](#references)

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
##Supportability Commands
###Display event logs
####Syntax
show events category loopback
####Description
This command displays all the events logged by loopback interfaces.

Following events will be logged for loopback interfaces.
- Create loopback interface.
- Configure loopback interface with IPv4 address.
- Configure loopback interface with IPv6 address.
- Remove IPv4 address from loopback inetrface.
- Remove IPv6 address from loopback interface.
- Delete loopback interface.

####Authority
All users
####Examples
```
switch# show events category loopback
2016-05-31:06:25:43.691954|ops-portd|9001|LOG_INFO|Loopback Interface lo10, created
2016-05-31:07:09:03.390671|ops-portd|9001|LOG_INFO|Loopback Interface lo11, created
2016-05-31:07:09:10.847426|ops-portd|9003|LOG_INFO|Loopback Interface lo11, configured with ip address 101.2.2.2/24
```
###Daignostic Dump
####Syntax
diag-dump loopback basic
####Description
This command will dump number of created loopback interfaces.
####Authority
All users
####Examples
```
switch# diag-dump loopback basic
=========================================================================
[Start] Feature loopback Time : Tue May 31 07:19:40 2016

=========================================================================
-------------------------------------------------------------------------
[Start] Daemon ops-portd
-------------------------------------------------------------------------
Number of Configured loopback interfaces are : 2.

-------------------------------------------------------------------------
[End] Daemon ops-portd
-------------------------------------------------------------------------
=========================================================================
[End] Feature loopback
=========================================================================
```
###show tech command
####Syntax
show tech loopback
####Description
This command will display configurations configured to all the loopback interfaces.
####Authority
All users
####Examples
```
switch# show tech loopback
interface loopback 1
    no shutdown
    ip address 192.168.1.1/24
interface loopback 2
    no shutdown
    ip address 182.168.1.1/24
```
## References
* [Reference 1]`interface_cli.md`
* [Reference 2]`loopback_interface_design.md`
