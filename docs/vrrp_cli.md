# VRRP commands
===============
#Contents
- [VRRP configuration commands](#vrrp-configuration-commands)
    - [Config context commands](#config-context-commands)
        - [Enable VRRP globally](#enable-vrrp-globally)
        - [Disable VRRP globally](#disable-vrrp-globally)
        - [Configure track object for interface](#configuring-track-object-for-interface)
        - [Configure track object for LAG interface](#configure-track-object-for-lag-interface)
        - [Delete track object](#delete-track-object)
    - [Interface context commands](#interface-context-commands)
        - [Create VRRP group](#create-vrrp-gorup)
        - [Delete VRRP group](#delete-vrrp-group)
    - [VRRP group context commands](#vrrp-group-context-commands)
        - [Configure protocol version](#configure-protocol-version)
        - [Assign virtual IP address to VRRP group](#assign-virtual-ip-address-to-vrrp-group)
        - [Remove virtual IP address from VRRP group](#remove-virtual-ip-address-from-vrrp-group)
        - [Set VRRP group priority](#set-vrrp-group-priority)
        - [Set default VRRP group priority](#set-default-vrrp-group-priority)
        - [Enable preempt](#enable-preempt)
        - [Disable preempt](#disable-preempt)
        - [Set preempt delay time](#set-preempt-delay-time)
        - [Set default preempt delay time](#set-default-preempt-delay-time)
        - [Set advertise time](#set-advertise-time)
        - [Set default advertise time](#set-default-advertise-time)
        - [Enable VRRP group operation](#enable-vrrp-group-operation)
        - [Disable VRRP group operation](#disable-vrrp-group-operation)
        - [Assign track object to VRRP group](#assign-track-object-to-vrrp-group)
        - [Remove track object from VRRP group](#remove-track-object-from-vrrp-group)
- [Track object show commands](#track-object-show-commands)
    - [Show track configuration](#show-track-configuration)
    - [Show track brief information](#show-track-brief-information)
- [VRRP show commands](#vrrp-show-commands)
    - [Show VRRP detail configuration](#show-vrrp-detail-configuration)
    - [Show VRRP brief configuration](#show-vrrp-brief-configration)
    - [Show VRRP interface configuration](#show-vrrp-interface-configuration)
    - [Show VRRP LAG interface configuration](#show-vrrp-lag-interface-configuration)
    - [Show VRRP VLAN interface configuration](#show-vrrp-vlan-interface-configuration)
    - [Show VRRP all statistics](#show-vrrp-all-statistics)
    - [Show VRRP interface statistics](#show-vrrp-interface-statistics)
    - [Show VRRP LAG interface statistics](#show-vrrp-lag-interface-statistics)
    - [Show VRRP VLAN interface statistics](#show-vrrp-vlan-interface-statistics)
    - [Show VRRP running configuration](#show-vrrp-running-configuration)

# VRRP configuration commands
## Config context commands
### Enable VRRP protocol
#### Syntax ####
`router vrrp`
#### Description ####
This command enables VRRP globally. You must globally enable the VRRP feature before you can configure and enable any VRRP groups.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)# router vrrp
```
### Disable VRRP protocol
#### Syntax ####
`no router vrrp`
#### Description ####
This command disables VRRP protocol globally.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)# no router vrrp
```
### Configure track object for interface
#### Syntax ####
`track <object-number> interface <ifname>`
#### Description ####
This command configures an interface to be tracked where changes in the state of the interface affect the priority of a VRRP group.
#### Authority ####
All users.
#### Parameters ####
| Parameter         | Status   | Syntax    | Description |
|:------------------|:---------|:----------|:--------------|
| *object-number*   | Required | <1-500>   | Specifies the track object number value|
| *ifname*          | Required | String    | Name of the interface |
#### Examples ####
```
switch# configure terminal
switch(config)# track 1 interface 10
```
### Configure track object for LAG interface
#### Syntax ####
`track <object-number> interface lag <lag-name>`
#### Description ####
This command configures a LAG interface to be tracked where changes in the state of the interface affect the priority of a VRRP group.
#### Authority ####
All users.
#### Parameters ####
| Parameter         | Status   | Syntax    | Description |
|:------------------|:---------|:----------|:--------------|
| *object-number*   | Required | <1-500>   | Specifies the track object number value|
| *lag-name*        | Required | String    | Name of the LAG interface |
#### Examples ####
```
switch# configure terminal
switch(config)# track 1 interface lag 100
```
### Delete track object
#### Syntax ####
`no track <object-number>`
#### Description ####
This command deletes a tracked object for an interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter         | Status   | Syntax    | Description |
|:------------------|:---------|:----------|:--------------|
| *object-number*   | Required | <1-500>   | Specifies the track object number value|
#### Examples ####
```
switch# configure terminal
switch(config)# no track 1
```
##Interface context commands
### Create VRRP group
#### Syntax ####
`vrrp <vrid> address-family (<ipv4> | <ipv6>)`
#### Description ####
This command creates a VRRP group and enters VRRP group configuration context.
#### Authority ####
All users.
#### Parameters ####
| Parameter         | Status   | Syntax    | Description |
|:------------------|:---------|:----------|:--------------|
| *vrid*            | Required | <1-255>   | Specifies the vrrp group number value|
#### Examples ####
```
switch# configure terminal
switch(config)#inerface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)#
```
### Delete VRRP group
#### Syntax ####
`no vrrp <vrid> address-family (<ipv4> | <ipv6>)`
#### Description ####
This command deletes a VRRP group.
#### Authority ####
All users.
#### Parameters ####
| Parameter         | Status   | Syntax    | Description |
|:------------------|:---------|:----------|:--------------|
| *vrid*            | Required | <1-255>   | Specifies the vrrp group number value|
#### Examples ####
```
switch# configure terminal
switch(config)# no vrrp 1 address-family ipv4
```
##VRRP group context commands
### Configuring VRRP protocol version
#### Syntax ####
`version <version-number>`
#### Description ####
This command sets protocol version for VRRP group, and the version change is allowed only for IPv4 address-family.
Default value is 2 for IPv4 address-family, and 3 for IPv6 address-family.

#### Authority ####
All users.
#### Parameters ####
| Parameter         | Status   | Syntax      | Description |
|:------------------|:---------|:------------|:--------------|
| *version-number*  | required | <2-3>       | Specifies the VRRP protocol version value|
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)#version 3
```
### Assign virtual IP address
#### Syntax ####
`address <ip-addres> (<primary> | <secondary>)`
#### Description ####
This command configures a primary or secondary IPv4 or IPv6 address for the VRRP group. To utilize secondary IP addresses in a VRRP group,
you must first configure a primary IP address on the same group.
#### Authority ####
All users.
#### Parameters ####
| Parameter     | Status   | Syntax    | Description   |
|:--------------|:---------|:----------|:--------------|
| *ip-address*  | Required | A.B.C.D or A:B::C:D   | Specifies the IPv4 or IPv6 address|
| *primary*     | Optional | Literal  | Configures a primary address|
| *secondary*   | Optional | Literal  | Configures a secondary address|
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)#address 10.0.0.1 primary

switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv6
switch(config-if-vrrp)#address 2001:0DB8::1 primary
```
### Delete virtual IP address
#### Syntax ####
`no address <ip-addres> (<primary> | <secondary>)`
#### Description ####
This command deletes a primary or secondary IPv4 or IPv6 address for the VRRP group.
#### Authority ####
All users.
#### Parameters ####
| Parameter     | Status   | Syntax    | Description   |
|:--------------|:---------|:----------|:--------------|
| *ip-address*  | Required | A.B.C.D or A:B::C:D   | Specifies the IPv4 or IPv6 address|
| *primary*     | Optional | Literal  | Deletes a primary address|
| *secondary*   | Optional | Literal  | Deletes a priamry address|
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)#no address 10.0.0.1 primary

switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv6
switch(config-if-vrrp)#no address 2001:0DB8::1 primary
```
###Set VRRP group priority
#### Syntax ####
`priority <1-254>`
#### Description ####
This command sets the priority for VRRP group, default value is 100.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)#priority 150
```
###Set default VRRP group priority
#### Syntax ####
`no priority <1-254>`
#### Description ####
This command sets the priority for VRRP group as default priority, default value is 100.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)#no priority
```
###Enable preempt option
#### Syntax ####
`preempt`
#### Description ####
This command enables the preempt option. Default value is enabled. In the default mode, a backup router coming
up with a higher priority than another backup that is currently operating as master will take over the master function.
This command applies to VRRP backup routers only and is used to minimize network disruption caused by unnecessary preemption
of the master operation among backup routers.

#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)#preempt
```
###Disable preempt option
#### Syntax ####
`no preempt`
#### Description ####
This command disables the preempt option. By default, preempt option is enabled, and in the default mode, a backup router coming
up with a higher priority than another backup that is currently operating as master will take over the master function.
This command disables this operation, thus preventing the higher-priority backup from taking over the master operation
from a lower-priority backup. This command does not prevent an owner router from resuming the master function
after recovering from being unavailable.

#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)# no preempt
```
###Set preempt delay time
#### Syntax ####
`preempt delay minimum <delay-in-secs>`
#### Description ####
This command sets time in seconds that this router will wait before taking control of the virtual IP, and beginning to route packets.
Default value is 0 seconds.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *delay-in-secs*| Required | <0-3600>  | Specifies the preempt delay value in seconds|
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)# preempt delay minimum 30
```
###Set default preempt delay time
#### Syntax ####
`no preempt delay`
#### Description ####
This command sets the preempt delay for VRRP group as default preempt delay second, default value is 0 seconds.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)# no preempt delay
```
###Set advertise time
#### Syntax ####
`timers advertise <advertise-in-milliseconds>`
#### Description ####
This command sets advertisement interval in milliseconds, default value is 1000.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *advertise-in-milliseconds*| required | <100-40950>   | Specifies the advertisement time in milliseconds|
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)# timers advertise 1000
```
###Set default advertise time
#### Syntax ####
`no timers advertise`
#### Description ####
This command sets advertisement interval to default interval in milliseconds, default value is 1000.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)# no timers advertise
```
###Enable VRRP group operation
#### Syntax ####
`no shutdown`
#### Description ####
This command enables VRRP group operation, default value is disabled.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)# no shutdown
```
###Disable VRRP group operation
#### Syntax ####
`shutdown`
#### Description ####
This command disables VRRP group operation, default value is disabled.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)# shutdown
```
###Set the track object to the VRRP group
#### Syntax ####
`track <object-number>`
#### Description ####
This command sets the track object number to the group.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *object-number*| required | <1-500>   | Specifies the track object number value|
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)# track 1
```
###Delete track object from the VRRP group
#### Syntax ####
`no track [<object-number>]`
#### Description ####
This command sets the track object number to the group.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *object-number*| optional | <1-500>   | Specifies the track object number value|
#### Examples ####
```
switch# configure terminal
switch(config)#interface 1
switch(config-if)#vrrp 1 address-family ipv4
switch(config-if-vrrp)# no track
```
# Track show commands
### show tracking objects formation
#### Syntax ####
`show track [<object-number>]`
#### Description ####
This command shows all or specific track object information.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Status     | Syntax           | Description   |
|:-----------------|:-----------|:----------------:|:--------------|
| *object-number*  | Optional   | <1-500>          | Specifies track object number value
#### Examples ####
```
switch# show track
Track 1
  Interface 1
  Interface is DOWN
```
### show tracking objects brief output
#### Syntax ####
`show track brief`
#### Description ####
This command shows brief information of all track objects.
#### Authority ####
All users.
#### Examples ####
```
switch# show track brief
Track  Interface       State

1        1              DOWN
```
# VRRP show commands
### show all vrrp information
#### Syntax ####
`show vrrp`
#### Description ####
This command shows all vrrp groups information.
#### Authority ####
All users.
#### Examples ####
```
switch# show vrrp

Interface 1 - Group 1 - Address-Family IPv4
  State is MASTER
  State duration 56 mins 57.826 secs
  Virtual IP address is 10.0.0.1
  Virtual MAC address is 00:00:5e:00:01:01
  Advertisement interval is 1000 msec
  Preemption enabled
  Priority is 100
  Master Router is 10.0.0.2 (local), priority is 100
  Master Advertisement interval is 1000 msec (expires in 631 msec)
  Master Down interval is unknown
  Tracked object id is 1, and state Down

Interface 2 - Group 1 - Address-Family IPv4
  State is INIT (Interface Down)
  State duration 45 mins 28.313 secs
  Virtual IP address is no address
  Virtual MAC address is 00:00:5e:00:01:01
  Advertisement interval is 1000 msec
  Preemption enabled
  Priority is 100
  Master Router is unknown, priority is unknown
  Master Advertisement interval is unknown
  Master Down interval is unknown

Interface 2 - Group 1 - Address-Family IPv6
  State is INIT (Interface Down)
  State duration 20 mins 19.794 secs
  Virtual IP address is no address
  Virtual secondary IP addresses:
    2201:13::110:4
  Virtual MAC address is 00:00:5e:00:02:01
  Advertisement interval is 1000 msec
  Preemption enabled
  Priority is 100
  Master Router is unknown, priority is unknown
  Master Advertisement interval is unknown
  Master Down interval is unknown
```
### show vrrp brief information
#### Syntax ####
`show vrrp brief`
#### Description ####
This command displays brief output of all VRRP groups.
#### Authority ####
All users.
#### Examples ####
```
switch# show vrrp brief
 Interface   Grp  A-F   Pri   Time Owner Pre State   Master addr/Group addr
  1           1   IPv4  100    0    N    Y   MASTER  10.0.0.2(local) 10.0.0.1
  2           1   IPv4  100    0    N    Y   INIT    AF-UNDEFINED no address
  2           1   IPv6  100    0    N    Y   INIT    AF-UNDEFINED no address
```
### show vrrp detail information
#### Syntax ####
`show vrrp detail`
#### Description ####
This command displays detail output of all VRRP groups.
#### Authority ####
All users.
#### Examples ####
```
switch# show vrrp detail
Interface 1 - Group 1 - Address-Family IPv4
  State is MASTER
  State duration 1 mins 35.486 secs
  Virtual IP address is 10.0.0.1
  Virtual MAC address is 00:00:5e:00:01:01
  Advertisement interval is 1000 msec
  Version 3
  Preemption enabled
  Priority is 100
  Master Router is 10.0.0.2 (local), priority is 100
  Master Advertisement interval is 1000 msec (expires in 268 msec)
  Master Down interval is unknown
  Tracked object id is 1, and state Down
  VRRPv3 Advertisements: sent 3931 (errors 0) - rcvd 0
  VRRPv2 Advertisements: sent 0 (errors 0) - rcvd 0
  Group Discarded Packets: 3537
    IP address Owner conflicts: 0
    IP address configuration mismatch : 3537
    Advert Interval errors : 0
    Adverts received in Init state: 0
    Invalid group other reason: 0
  Group State transition:
    Init to master: 0
    Init to backup: 2 (Last change Mon Jun 16 11:19:36.316 UTC)
    Backup to master: 2 (Last change Mon Jun 16 11:19:39.926 UTC)
    Master to backup: 0
    Master to init: 1 (Last change Mon Jun 16 11:17:49.978 UTC)
    Backup to init: 0

Interface 2 - Group 1 - Address-Family IPv4
  State is INIT (Interface Down)
  State duration 49 mins 23.507 secs
  Virtual IP address is no address
  Virtual MAC address is 00:00:5e:00:01:01
  Advertisement interval is 1000 msec
  Version 3
  Preemption enabled
  Priority is 100
  Master Router is unknown, priority is unknown
  Master Advertisement interval is unknown
  Master Down interval is unknown
  VRRPv3 Advertisements: sent 0 (errors 0) - rcvd 0
  VRRPv2 Advertisements: sent 0 (errors 0) - rcvd 0
  Group Discarded Packets: 0
    IP address Owner conflicts: 0
    IP address configuration mismatch : 0
    Advert Interval errors: 0
    Adverts received in Init state: 0
    Invalid group other reason: 0
  Group State transition:
    Init to master: 0
    Init to backup: 0
    Backup to master: 0
    Master to backup: 0
    Master to init: 0
    Backup to init: 0

Interface 2 - Group 1 - Address-Family IPv6
  State is INIT (Interface Down)
  State duration 24 mins 14.988 secs
  Virtual IP address is no address
  Virtual secondary IP addresses:
    2201:13::110:4
  Virtual MAC address is 00:00:5e:00:02:01
  Advertisement interval is 1000 msec
  Preemption enabled
  Priority is 100
  Master Router is unknown, priority is unknown
  Master Advertisement interval is unknown
  Master Down interval is unknown
  VRRPv3 Advertisements: sent 0 (errors 0) - rcvd 0
  VRRPv2 Advertisements: sent 0 (errors 0) - rcvd 0
  Group Discarded Packets: 0
    VRRPv2 incompatibility: 0
    IP address Owner conflicts: 0
    IP address configuration mismatch : 0
    Advert Interval errors : 0
    Adverts received in Init state: 0
    Invalid group other reason: 0
  Group State transition:
    Init to master: 0
    Init to backup: 0
    Backup to master: 0
    Master to backup: 0
    Master to init: 0
    Backup to init: 0
```
### show vrrp information for specific interface
#### Syntax ####
`show vrrp interface [<interface-name>]`
#### Description ####
This command displays VRRP info for a specified interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Status     | Syntax           | Description   |
|:-----------------|:-----------|:----------------:|:--------------|
| *interface_name* | Optional   | String           | Shows VRRP information only of a particular interface
#### Examples ####
```
switch# show vrrp interface 1

Interface 1 - Group 1 - Address-Family IPv4
  State is MASTER
  State duration 11 mins 21.617 secs
  Virtual IP address is 10.0.0.1
  Virtual MAC address is 00:00:5e:00:01:01
  Advertisement interval is 1000 msec
  Version 3
  Preemption enabled
  Priority is 100
  Master Router is 10.0.0.2 (local), priority is 100
  Master Advertisement interval is 1000 msec (expires in 11 msec)
  Master Down interval is unknown

```
### show vrrp information for specific LAG interface
#### Syntax ####
`show vrrp interface lag <lag-name>`
#### Description ####
This command displays VRRP info for a specified LAG interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Status     | Syntax           | Description   |
|:-----------------|:-----------|:----------------:|:--------------|
| *lag_name*       | Required   | String           | Shows VRRP information only of a particular LAG interface
#### Examples ####
```
switch# show vrrp interface lag10

Interface lag10 - Group 1 - Address-Family IPv4
  State is MASTER
  State duration 11 mins 21.617 secs
  Virtual IP address is 10.0.0.1
  Virtual MAC address is 00:00:5e:00:01:01
  Advertisement interval is 1000 msec
  Version 3
  Preemption enabled
  Priority is 100
  Master Router is 10.0.0.2 (local), priority is 100
  Master Advertisement interval is 1000 msec (expires in 11 msec)
  Master Down interval is unknown

```
### show vrrp information for specific VLAN interface
#### Syntax ####
`show vrrp interface vlan <vlan-number>`
#### Description ####
This command displays VRRP info for a specified VLAN interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Status     | Syntax           | Description   |
|:-----------------|:-----------|:----------------:|:--------------|
| *vlan-number*    | Required   | <1-4094>         | Shows VRRP information only of a particular VLAN interface
#### Examples ####
```
switch# show vrrp interface vlan 100

Interface vlan 100 - Group 1 - Address-Family IPv4
  State is MASTER
  State duration 11 mins 21.617 secs
  Virtual IP address is 10.0.0.1
  Virtual MAC address is 00:00:5e:00:01:01
  Advertisement interval is 1000 msec
  Version 3
  Preemption enabled
  Priority is 100
  Master Router is 10.0.0.2 (local), priority is 100
  Master Advertisement interval is 1000 msec (expires in 11 msec)
  Master Down interval is unknown
```
### show vrrp statistics information
#### Syntax ####
`show vrrp statistics`
#### Description ####
This command displays VRRP statistics information for all interfaces.
#### Authority ####
All users.
#### Examples ####
```
switch# show vrrp statistics

VRRP Statistics for interface 1 - Group 1 - Address-Family IPv4
  State is MASTER
  State duration 6 mins 55.006 secs
  VRRPv3 Advertisements: sent 4288 (errors 0) - rcvd 0
  VRRPv2 Advertisements: sent 0 (errors 0) - rcvd 0
  Group Discarded Packets: 3856
    IP address Owner conflicts: 0
    IP address configuration mismatch : 0
    Advert Interval errors : 0
    Adverts received in Init state: 0
    Invalid group other reason: 0
  Group State transition:
    Init to master: 0
    Init to backup: 2 (Last change Mon Jun 16 11:19:36.316 UTC)
    Backup to master: 2 (Last change Mon Jun 16 11:19:39.926 UTC)
    Master to backup: 0
    Master to init: 1 (Last change Mon Jun 16 11:17:49.978 UTC)
    Backup to init: 0

VRRP Statistics for Interface 2 - Group 1 - Address-Family IPv4
  State is INIT (Interface Down)
  State duration 54 mins 43.027 secs
  VRRPv3 Advertisements: sent 0 (errors 0) - rcvd 0
  VRRPv2 Advertisements: sent 0 (errors 0) - rcvd 0
  Group Discarded Packets: 0
    IP address Owner conflicts: 0
    Invalid address count: 0
    IP address configuration mismatch : 0
    Advert Interval errors : 0
    Adverts received in Init state: 0
    Invalid group other reason: 0
  Group State transition:
    Init to master: 0
    Init to backup: 0
    Backup to master: 0
    Master to backup: 0
    Master to init: 0
    Backup to init: 0

VRRP Statistics for Interface 2 - Group 1 - Address-Family IPv6
  State is INIT (Interface Down)
  State duration 29 mins 34.508 secs
  VRRPv3 Advertisements: sent 0 (errors 0) - rcvd 0
  VRRPv2 Advertisements: sent 0 (errors 0) - rcvd 0
  Group Discarded Packets: 0
    IP address Owner conflicts: 0
    IP address configuration mismatch : 0
    Advert Interval errors: 0
    Adverts received in Init state: 0
    Invalid group other reason: 0
  Group State transition:
    Init to master: 0
    Init to backup: 0
    Backup to master: 0
    Master to backup: 0
    Master to init: 0
    Backup to init: 0
```
### show vrrp statistics information for specific interface
#### Syntax ####
`show vrrp statistics interface <interface-name>`
#### Description ####
This command displays VRRP statistics information for specific interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Status     | Syntax           | Description   |
|:-----------------|:-----------|:----------------:|:--------------|
| *interface_name* | Optional   | String           | Shows VRRP statistics information only of a particular interface
#### Examples ####
```
switch# show vrrp statistics interface 1

VRRP Statistics for interface 1 - Group 1 - Address-Family IPv4
  State is MASTER
  State duration 6 mins 55.006 secs
  VRRPv3 Advertisements: sent 4288 (errors 0) - rcvd 0
  VRRPv2 Advertisements: sent 0 (errors 0) - rcvd 0
  Group Discarded Packets: 3856
    IP address Owner conflicts: 0
    IP address configuration mismatch : 0
    Advert Interval errors : 0
    Adverts received in Init state: 0
    Invalid group other reason: 0
  Group State transition:
    Init to master: 0
    Init to backup: 2 (Last change Mon Jun 16 11:19:36.316 UTC)
    Backup to master: 2 (Last change Mon Jun 16 11:19:39.926 UTC)
    Master to backup: 0
    Master to init: 1 (Last change Mon Jun 16 11:17:49.978 UTC)
    Backup to init: 0
```
### show vrrp statistics information for specific LAG interface
#### Syntax ####
`show vrrp statistics interface lag <lag-name>`
#### Description ####
This command displays VRRP statistics information for specific interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Status     | Syntax           | Description   |
|:-----------------|:-----------|:----------------:|:--------------|
| *lag-name*       | Required   | String           | Shows VRRP statistics information only of a particular LAG interface
#### Examples ####
```
switch# show vrrp statistics interface lag 10

VRRP Statistics for interface lag10 - Group 1 - Address-Family IPv4
  State is MASTER
  State duration 6 mins 55.006 secs
  VRRPv3 Advertisements: sent 4288 (errors 0) - rcvd 0
  VRRPv2 Advertisements: sent 0 (errors 0) - rcvd 0
  Group Discarded Packets: 3856
    IP address Owner conflicts: 0
    IP address configuration mismatch : 0
    Advert Interval errors : 0
    Adverts received in Init state: 0
    Invalid group other reason: 0
  Group State transition:
    Init to master: 0
    Init to backup: 2 (Last change Mon Jun 16 11:19:36.316 UTC)
    Backup to master: 2 (Last change Mon Jun 16 11:19:39.926 UTC)
    Master to backup: 0
    Master to init: 1 (Last change Mon Jun 16 11:17:49.978 UTC)
    Backup to init: 0
```
### show vrrp statistics information for specific VLAN interface
#### Syntax ####
`show vrrp statistics interface vlan <vlan-name>`
#### Description ####
This command displays VRRP statistics information for specific VLAN interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Status     | Syntax           | Description   |
|:-----------------|:-----------|:----------------:|:--------------|
| *vlan-name*      | Required   | String           | Shows VRRP statistics information only of a particular VLAN interface
#### Examples ####
```
switch# show vrrp statistics interface vlan 100

VRRP Statistics for interface vlan 100 - Group 1 - Address-Family IPv4
  State is MASTER
  State duration 6 mins 55.006 secs
  VRRPv3 Advertisements: sent 4288 (errors 0) - rcvd 0
  VRRPv2 Advertisements: sent 0 (errors 0) - rcvd 0
  Group Discarded Packets: 3856
    IP address Owner conflicts: 0
    IP address configuration mismatch : 0
    Advert Interval errors : 0
    Adverts received in Init state: 0
    Invalid group other reason: 0
  Group State transition:
    Init to master: 0
    Init to backup: 2 (Last change Mon Jun 16 11:19:36.316 UTC)
    Backup to master: 2 (Last change Mon Jun 16 11:19:39.926 UTC)
    Master to backup: 0
    Master to init: 1 (Last change Mon Jun 16 11:17:49.978 UTC)
    Backup to init: 0
```
### Show VRRP running configuration
#### Syntax ####
`show running-config vrrp`
#### Description ####
This command shows configured commands for VRRP.
#### Authority ####
All users.
#### Examples ####
```
!
router vrrp

interface 1
    vrrp 1 address-family ipv4
    address 10.0.0.1 primary
interface 2
    vrrp 1 address-family ipv4
    vrrp 1 address-family ipv6
    address 2201:13::110:4
```
