MSTP commands
=============
# Contents
- [MSTP configuration commands](#mstp-configuration-commands)
	- [Config context commands](#config-context-commands)
		- [Enable MSTP protocol](#enable-mstp-protocol)
		- [Disable MSTP protocol](#disable-mstp-protocol)
		- [Set MSTP config name](#set-mstp-config-name)
		- [Set default MSTP config name](#set-default-mstp-config-name)
		- [Set MSTP config revision number](#set-mstp-config-revision-number)
		- [Set default MSTP config revision number](#set-default-mstp-config-revision-number)
		- [VLAN to an instance](#vlan-to-an-instance)
		- [Remove VLAN from instance](#remove-vlan-from-instance)
		- [Set forward delay](#set-forward-delay)
		- [Set default forward delay](#set-default-forward-delay)
		- [Set hello time](#set-hello-time)
		- [Set default hello time](#set-default-hello-time)
		- [Set MSTP priority](#set-MSTP-priority)
		- [Set default MSTP priority](#set-default-MSTP-priority)
		- [Set transmit hold count](#set-transmit-hold-count)
		- [Set default transmit hold count](#set-default-transmit-hold-count)
		- [Set max age](#set-max-age)
		- [Set default max age](#set-default-max-age)
		- [Set max hops](#set-max-hops)
		- [Set default max hops](#set-default-max-hops)
		- [Set instance priority](#set-instance-priority)
		- [Set instance default priority](#set-instance-default-priority)
	- [Interface context commands](#interface-context-commands)
		- [Set port type](#set-port-type)
		- [Set default port type](#set-default-port-type)
		- [Enable bpdu guard](#enable-bpdu-guard)
		- [Set default bpdu guard](#set-default-bpdu-guard)
		- [Enable loop guard](#enable-loop-guard)
		- [Set default loop guard](#set-default-loop-guard)
		- [Enable root guard](#enable-root-guard)
		- [Set default root guard](#set-default-root-guard)
		- [Enable bpdu filter](#enable-bpdu-filter)
		- [Set default bpdu filter](#set-default-bpdu-filter)
		- [Set instance cost](#set-instance-cost)
		- [Set instance default cost](#set-instance-default-cost)
		- [Set instance port priority](#set-instance-port-priority)
		- [Set instance default port priority](#set-instance-default-port-priority)
	- [MSTP show commands](#mstp-show-commands)
	    - [Show spanning tree global configuration](#show-spanning-tree-global-configuration)
		- [Show spanning tree detail configuration](#show-spanning-tree-detail-configuration)
		- [Show MSTP global configuration](#show-mstp-global-configuration)
		- [Show MSTP configuration](#show-mstp-configuration)
		- [Show MSTP detail configuration](#show-mstp-detail-configuration)
		- [Show MSTP instance configuration](#show-mstp-instance-configuration)
		- [Show MSTP instance detail configuration](#show-mstp-instance-detail-configuration)
		- [Show MSTP running configuration](#show-mstp-running-configuration)

# MSTP configuration commands
## Config context commands
### Enable MSTP protocol
#### Syntax ####
`spanning-tree`
#### Description ####
This command enables MSTP feature for all the instances.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch# spanning-tree
```
### Disable MSTP protocol
#### Syntax ####
`no spanning-tree`
#### Description ####
This command disables MSTP feature for all the instances.
#### Authority ####
All users.
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree
```
### Set MSTP config name
#### Syntax ####
`spanning-tree config-name <configuration-name>`
#### Description ####
This command sets config name for MSTP.
#### Authority ####
All users.
#### Parameters ####
| Parameter            | Status    | Description |
|:---------------------|:----------|:--------------|
| *configuration-name* | Required  | Specifies the MSTP configuration name(maximum 32 characters)|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree config-name MST0
```
### Set default MSTP config name
#### Syntax ####
`no spanning-tree config-name [<configuration-name>]`
#### Description ####
This command sets the default config name for all the instances, default is system MAC-Address.
#### Authority ####
All users.
#### Parameters ####
| Parameter     |  Status      | Description |
|:--------------|:-------------|:----------------|
| *config-name* | Optional     | Specifies the MSTP configuration name |
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree config-name
```
### Set MSTP config revision number
#### Syntax ####
`spanning-tree config-revision <revision-number>`
#### Description ####
This command sets config revision number for the all the instances.
#### Authority ####
All users.
#### Parameters ####
| Parameter         | Status   | Syntax    | Description |
|:------------------|:---------|:----------|:--------------|
| *revision-number* | Required | <1-65535> | Specifies the MSTP configuration revision number value|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree config-revision 40
```
### Set default MSTP config revision number
#### Syntax ####
`no spanning-tree config-revision [<revision-number>]`
#### Description ####
This command sets default config revision number for the all the instances, default value is 0.
#### Authority ####
All users.
#### Parameters ####
| Parameter         | Status   | Syntax      | Description |
|:------------------|:---------|:------------|:--------------|
| *revision-number* | Optional | <1-65535>   | Specifies the MSTP configuration revision number value|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree config-revision
```
### VLAN to an instance
#### Syntax ####
`spanning-tree instance <instance-id> vlan <VLAN-ID>`
#### Description ####
This command maps the VLAN-ID to corresponding  instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter     | Status   | Syntax    | Description   |
|:--------------|:---------|:----------|:--------------|
| *instance-id* | Required | <1-64>    | Specifies the MSTP instance number|
| *VLAN-ID*     | Required | <1-4094>  | Specifies the VLAN-ID number|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree instance 1 vlan 1
switch# spanning-tree instance 1 vlan 2
```
### Remove VLAN from instance
#### Syntax ####
`no spanning-tree instance <instance-id> vlan <VLAN-ID>`
#### Description ####
This command removes the VLAN-ID from the MSTP instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter     | Status   | Syntax    | Description   |
|:--------------|:---------|:----------|:--------------|
| *instance-id* | Required | <1-64>    | Specifies the MSTP instance number|
| *VLAN-ID*     | Required | <1-4094>  | Specifies the VLAN-ID number|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree instance 1 vlan 1
switch# no spanning-tree instance 1 vlan 2
```
###Set forward delay
#### Syntax ####
`spanning-tree forward-delay <delay-in-secs>`
#### Description ####
This command sets the forward-delay for the bridge.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *delay-in-secs*| Required | <4-30>    | Specifies the forward delay in seconds|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree forward-delay 6
```
###Set default forward delay
#### Syntax ####
`no spanning-tree forward-delay [<delay-in-secs>]`
#### Description ####
This command sets the default forward-delay for the bridge, default value is 15 seconds.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *delay-in-secs*| Optional | <4-30>    | Specifies the forward delay in seconds|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree forward-delay
```
###Set hello time
#### Syntax ####
`spanning-tree hello-time <hello-in-secs>`
#### Description ####
This command sets the hello interval for all the MSTP instances.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *hello-in-secs*| Required | <2-10>    | Specifies the hello interval in seconds|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree hello-time 6
```
###Set default hello time
#### Syntax ####
`no spanning-tree hello-time [<hello-in-secs>]`
#### Description ####
This command sets the default hello interval for all the MSTP instances, default value is 2 seconds.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *hello-in-secs*| Optional | <2-10>    | Specifies the hello interval in seconds|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree hello-time
```
###Set MSTP priority
#### Syntax ####
`spanning-tree priority <0-15>`
#### Description ####
This command sets the priority for all the MSTP instances.
The priority value will be derived by multiplying with value of 4096.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *priority*     | Required | <0-15>    | Specifies the priority|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree priority 12
```
###Set default MSTP priority
#### Syntax ####
`no spanning-tree priority [<0-15>]`
#### Description ####
This command sets the priority to its default value of 8 for all the MSTP instances.
The priority value will be derived by multiplying with value of 4096.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *priority*     | Optional | <0-15>    | Specifies the priority|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree priority 12
```
###Set transmit hold count
#### Syntax ####
`spanning-tree transmit-hold-count <0-10>`
#### Description ####
This command sets the txHoldCount for all the MSTP instances.
Used by protocol to limit the maximum transmission rate of MST BPDUs within the hello interval.
#### Authority ####
All users.
#### Parameters ####
| Parameter             | Status   | Syntax    | Description   |
|:--------------------- |:---------|:----------|:--------------|
| *transmit-hold-count* | Required | <0-10>    | Specifies the txHoldCount in pps|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree transmit-hold-count 5
```
###Set default transmit hold count
#### Syntax ####
`no spanning-tree transmit-hold-count [<0-10>]`
#### Description ####
This command sets the txHoldCount to its default value of 6 pps for all MST instances.
#### Authority ####
All users.
#### Parameters ####
| Parameter             | Status   | Syntax    | Description   |
|:--------------------- |:---------|:----------|:--------------|
| *transmit-hold-count* | Optional | <0-10>    | Specifies the txHoldCount|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree transmit-hold-count 5
```
###Set max age
#### Syntax ####
`spanning-tree max-age <age-in-secs>`
#### Description ####
This command sets the maximum age for all the MSTP instances.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *age-in-secs*  | Required | <6-30>    | Specifies the maximum age in seconds|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree max-age 10
```
###Set default max age
#### Syntax ####
`no spanning-tree max-age [<age-in-secs>]`
#### Description ####
This command sets the default max age for all the MSTP instances, default value is 20 seconds.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *age-in-secs*  | Optional | <6-30>    | Specifies the maximum age in seconds|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree max-age
```
###Set max hops
#### Syntax ####
`spanning-tree max-hops <hop-count>`
#### Description ####
This command sets the hop count for all the MSTP instances.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *hop-count*    | Required | <1-40>    | Specifies the maximum number of hops|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree max-hops 10
```
###Set default max hops
#### Syntax ####
`no spanning-tree max-hops [<hop-count>]`
#### Description ####
This command sets the default hop count for all the MSTP instances, default value is 20.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Syntax    | Description   |
|:-------------- |:---------|:----------|:--------------|
| *hop-count*    | Optional | <1-40>    | Specifies the maximum number of hops|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree max-hops
```
###Set instance priority
#### Syntax ####
`spanning-tree instance <1-64> priority <0-15>`
#### Description ####
This command sets the priority value for that particular instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Status   | Description   |
|:---------------- |:---------|:--------------|
| *instance-id*    | Required |Specifies the instance-id|
| *priority-value* | Required |Specifies the priority value|
#### Examples ####
```
switch# configure terminal
switch# spanning-tree instance 1 priority 5
```
###Set default instance priority
#### Syntax ####
`no spanning-tree instance <1-64> priority [<0-15>]`
#### Description ####
This command sets the default priority value for that particular instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Status   | Description   |
|:---------------- |:---------|:--------------|
| *instance-id*    | Required |Specifies the instance-id|
| *priority-value* | Optional |Specifies the priority value|
#### Examples ####
```
switch# configure terminal
switch# no spanning-tree instance 1 priority
```
##Interface context commands
###Set port type
#### Syntax ####
`spanning-tree port-type (admin-edge | admin-network)`
#### Description ####
This command sets the port-type for all the MSTP instances.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *admin-edge*   | Optional |Specifies the port as admin-edge|
| *admin-network*| Optional |Specifies the port as admin-network|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree port-type admin-edge
switch# spanning-tree port-type admin-network
```
###Set default port type
#### Syntax ####
`no spanning-tree port-type [admin-edge | admin-network]`
#### Description ####
This command sets the port-type to its default value of admin-network for all the MSTP instances.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *admin-edge*   | Optional |Specifies the port as admin-edge|
| *admin-network*| Optional |Specifies the port as admin-network|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# no spanning-tree port-type
```
###Enable bpdu guard
#### Syntax ####
`spanning-tree bpdu-guard [enable | disable]`
#### Description ####
This command enable the bpdu guard on the interfaces.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *bpdu-guard*   | Required |Specifies the bpdu-guard|
| *enable*       | Optional |Specifies the status parameter|
| *disable*      | Optional |Specifies the status parameter|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree bpdu-guard enable
```
###Set default bpdu guard
#### Syntax ####
`no spanning-tree bpdu-guard [enable | disable]`
#### Description ####
This command sets the bpdu guard status to its default value of disable on the interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *bpdu-guard*   | Required |Specifies the bpdu-guard|
| *enable*       | Optional |Specifies the status parameter|
| *disable*      | Optional |Specifies the status parameter|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree bpdu-guard
```
###Enable root guard
#### Syntax ####
`spanning-tree root-guard [enable | disable]`
#### Description ####
This command enable the root guard on the interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *root-guard*   | Required |Specifies the root-guard|
| *enable*       | Optional |Specifies the status parameter|
| *disable*      | Optional |Specifies the status parameter|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree root-guard enable
```
###Set default root guard
#### Syntax ####
`no spanning-tree root-guard [enable | disable]`
#### Description ####
This command sets the root guard status to its default value of disable on the interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *root-guard*   | Required |Specifies the root-guard|
| *enable*       | Optional |Specifies the status parameter|
| *disable*      | Optional |Specifies the status parameter|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree root-guard
```
###Enable loop guard
#### Syntax ####
`spanning-tree loop-guard [enable | disable]`
#### Description ####
This command enable the loop guard in the interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *loop-guard*   | Required |Specifies the loop-guard|
| *enable*       | Optional |Specifies the status parameter|
| *disable*      | Optional |Specifies the status parameter|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree loop-guard enable
```
###Set default loop guard
#### Syntax ####
`no spanning-tree loop-guard [enable | disable]`
#### Description ####
This command sets the loop guard status to its default value of disable on the interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *loop-guard*   | Required |Specifies the loop-guard|
| *enable*       | Optional |Specifies the status parameter|
| *disable*      | Optional |Specifies the status parameter|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree loop-guard
```
###Enable bpdu filter
#### Syntax ####
`spanning-tree bpdu-filter [enable | disable]`
#### Description ####
This command enable the bpdu filter in the interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *bpdu-filter*  | Required |Specifies the bpdu-filter|
| *enable*       | Optional |Specifies the status parameter|
| *disable*      | Optional |Specifies the status parameter|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree bpdu-guard enable
switch# spanning-tree root-guard disable
```
###Set default bpdu filter
#### Syntax ####
`no spanning-tree bpdu-filter [enable | disable]`
#### Description ####
This command sets the bpdu filter status to its default value of disable on the interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *bpdu-filter*  | Required |Specifies the bpdu-filter|
| *enable*       | Optional |Specifies the status parameter|
| *disable*      | Optional |Specifies the status parameter|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree bpdu-guard enable
switch# spanning-tree root-guard disable
```
###Set instance cost
#### Syntax ####
`spanning-tree instance <1-64> cost <1-200000000>`
#### Description ####
This command sets MSTP cost value for that particular instance.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *instance-id*  | Required |Specifies the instance-id|
| *cost-value*   | Required |Specifies the cost value|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree instance 1 cost 2000
```
###Set instance default cost
#### Syntax ####
`no spanning-tree instance <1-64> cost [<1-200000000>]`
#### Description ####
This command sets the default MSTP cost value for the instance to 20000.
#### Authority ####
All users.
#### Parameters ####
| Parameter      | Status   | Description   |
|:-------------- |:---------|:--------------|
| *instance-id*  | Required |Specifies the instance-id|
| *cost-value*   | Optional |Specifies the cost value|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# no spanning-tree instance 1 cost
```
###Set instance port priority
#### Syntax ####
`spanning-tree instance <1-64> port-priority <1-15>`
#### Description ####
This command sets MSTP port-priority value for that particular instance.
The priority value will be derived by multiplying with value of 16.
#### Authority ####
All users.
#### Parameters ####
| Parameter             | Status   | Description   |
|:--------------------- |:---------|:--------------|
| *instance-id*         | Required |Specifies the instance-id|
| *port-priority-value* | Required |Specifies the port-priority value|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# spanning-tree instance 1 port-priority 8
```
###Set instance default port priority
#### Syntax ####
`no spanning-tree instance <1-64> port-priority [<1-15>]`
#### Description ####
This command sets the port-priority to its default value of 8 for that MSTP instance.
The priority value will be derived by multiplying with value of 16.
#### Authority ####
All users.
#### Parameters ####
| Parameter             | Status   | Description   |
|:--------------------- |:---------|:--------------|
| *instance-id*         | Required |Specifies the instance-id|
| *port-priority-value* | Optional |Specifies the port-priority value|
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch# no spanning-tree instance 1 port-priority
```
# MSTP show commands
### Show spanning tree global configuration
#### Syntax ####
`show spanning-tree`
#### Description ####
This command shows priority, address, Hello-time, Max-age, Forward-delay for bridge and root node.
#### Authority ####
All users.
#### Examples ####
```
MST0
  Spanning tree status: Enabled
  Root ID    Priority    : 32768
             MAC-Address : 70:72:cf:e1:b9:16
             This bridge is the root
             Hello time(in seconds): 2  Max Age(in seconds): 20  Forward Delay(in seconds): 15


  Bridge ID  Priority    : 32768
             MAC-Address : 70:72:cf:e1:b9:16
             Hello time(in seconds): 2  Max Age(in seconds): 20  Forward Delay(in seconds): 15

Port           Role           State      Cost    Priority   Type
-------------- -------------- ---------- ------- ---------- ----------
1              disabled_port  Blocking   0       128        point_to_point
2              disabled_port  Blocking   0       128        point_to_point
```
### Show spanning tree detail configuration
#### Syntax ####
`show spanning-tree detail`
#### Description ####
This command shows detail information regarding CIST and corresponding port details.
#### Authority ####
All users.
#### Examples ####
```
MST0 is executing the mstp compatible Spanning Tree protocol
  Bridge Identifier has priority 12, address: 70:72:cf:55:33:cd
  Configured Hello time(in seconds): 5  Forward delay(in seconds): 5  Max-age(in seconds):10  txHoldCount(in pps): 5
  We are the root of the spanning tree
  Topology change flag not set
  Number of topology changes 0, last change occurred 48 seconds ago

  Times:  Hold          5  Topology chnage      0
          Hello         5  max age              10, forward delay      5
  Timers: Hello expiry  0  forward delay expiry 0

Port 1 of MST0 is disabled_port
Port path cost 0, Port priority 8
Designated root has priority 4, address 70:72:cf:e1:b9:16
Designated bridge has priority 4, address 70:72:cf:e1:b9:16
Designated port has priority 4, address 70:72:cf:e1:b9:16
Number of transitions to forwarding state: 0
Link type is point_to_point by default, Internal
Bpdus sent 0, received 0

Port 2 of MST0 is disabled_port
Port path cost 0, Port priority 8
Designated root has priority 4, address 70:72:cf:e1:b9:16
Designated bridge has priority 4, address 70:72:cf:e1:b9:16
Designated port has priority 4, address  70:72:cf:e1:b9:16
Number of transitions to forwarding state: 0
Link type is point_to_point by default, Internal
Bpdus sent 0, received 0
```
### Show MSTP global configuration
#### Syntax ####
`show spanning-tree mst-config`
#### Description ####
This command shows MSTP instance and corresponding VLANs.
#### Authority ####
All users.
#### Examples ####
```
MST configuration information
   MST config ID           : MST0
   MST config revision     : 33
   MST config digest       : 0x9bbda9c70d91f633e1e145fbcbf8d321
   Number of instances     : 2

Instance ID     Member VLANs
--------------- ----------------------------------
1               1,2
3               3
```
### Show MSTP configuration
#### Syntax ####
`show spanning-tree mst`
#### Description ####
This command shows global MSTP configuration.
#### Authority ####
All users.
#### Examples ####
```
#### MST0
Vlans mapped:
Bridge         Address:70:72:cf:84:d1:56    priority:8
Root
Regional Root
Operational    Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6
Configured     Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6

Port           Role           State      Cost       Priority   Type
-------------- -------------- ---------- ---------- ---------- ----------
1              Disabled       Blocking   0          8          point_to_point
2              Disabled       Blocking   0          8          point_to_point

#### MST1
Vlans mapped:  1
Bridge         Address:70:72:cf:84:d1:56    Priority:8
Root           Address:                     Priority:8
               Port:0, Cost:20000, Rem Hops:0

Port           Role           State      Cost    Priority   Type
-------------- -------------- ---------- ------- ---------- ----------
1              Disabled       Blocking   0       8          Point_to_point
2              Disabled       Blocking   0       8          Point_to_point
```
### Show MSTP detail configuration
#### Syntax ####
`show spanning-tree mst detail`
#### Description ####
This command shows detail MSTP CIST and all instance related information with port detail.
#### Authority ####
All users.
#### Examples ####
```
switch# show spanning-tree mst detail
#### MST0
Vlans mapped:
Bridge         Address:70:72:cf:84:d1:56    priority:8
Root
Regional Root
Operational    Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6
Configured     Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6

Port           Role           State      Cost       Priority   Type
-------------- -------------- ---------- ---------- ---------- ----------
1              Disabled       Blocking   0          8          point_to_point
2              Disabled       Blocking   0          8          point_to_point

#### MST1
Vlans mapped:  1
Bridge         Address:70:72:cf:84:d1:56    Priority:8
Root           Address:70:72:cf:05:02:b3    Priority:8
               Port:0, Cost:20000, Rem Hops:0

Port           Role           State      Cost    Priority   Type
-------------- -------------- ---------- ------- ---------- ----------
1              Disabled       Blocking   0       8          Point_to_point
2              Disabled       Blocking   0       8          Point_to_point

Port 1
Designated root address            : 70:72:cf:05:02:b3
Designated regional root address   : 70:72:cf:05:02:b3
Designated bridge address          : 70:72:cf:05:02:b3
Timers:    Message expires in 0 sec, Forward delay expiry:0, Forward transitions:0
Bpdus sent 0, received 0

Port 2
Designated root address            : 70:72:cf:05:02:b3
Designated regional root address   : 70:72:cf:05:02:b3
Designated bridge address          : 70:72:cf:05:02:b3
Timers:    Message expires in 0 sec, Forward delay expiry:0, Forward transitions:0
Bpdus sent 0, received 0
```
### Show MSTP instance configuration
#### Syntax ####
`show spanning-tree mst <1-64>`
#### Description ####
This command shows MSTP configurations for the given instance ID.
#### Authority ####
All users.
#### Examples ####
```
switch# sh spanning-tree mst 1
#### MST1
Vlans mapped:  1
Bridge         Address:70:72:cf:84:d1:56    Priority:8
Root           Address:                     Priority:8
               Port:0, Cost:20000, Rem Hops:0

Port           Role           State      Cost    Priority   Type
-------------- -------------- ---------- ------- ---------- ----------
1              Disabled       Blocking   0       8          Point_to_point
2              Disabled       Blocking   0       8          Point_to_point
```
### Show MSTP instance configuration
#### Syntax ####
`show spanning-tree mst <1-64> detail`
#### Description ####
This command shows MSTP configurations for the given instance ID with corresponding port details.
#### Authority ####
All users.
#### Examples ####
```
switch# show spanning-tree mst 1 detail
#### MST1
Vlans mapped:  1
Bridge         Address:70:72:cf:84:d1:56    Priority:8
Root           Address:                     Priority:8
               Port:0, Cost:20000, Rem Hops:0

Port           Role           State      Cost    Priority   Type
-------------- -------------- ---------- ------- ---------- ----------
1              Disabled       Blocking   0       8          Point_to_point
2              Disabled       Blocking   0       8          Point_to_point

Port 1
Designated root address            : 70:72:cf:55:33:cd
Designated regional root address   : 70:72:cf:55:33:cd
Designated bridge address          : 70:72:cf:55:33:cd
Timers:    Message expires in 0 sec, Forward delay expiry:0, Forward transitions:0
Bpdus sent 0, received 0

Port 2
Designated root address            : 70:72:cf:55:33:cd
Designated regional root address   : 70:72:cf:55:33:cd
Designated bridge address          : 70:72:cf:55:33:cd
Timers:    Message expires in 0 sec, Forward delay expiry:0, Forward transitions:0
Bpdus sent 0, received 0
```
### Show MSTP running configuration
#### Syntax ####
`show running-config spanning-tree`
#### Description ####
This command shows configured commands for MSTP.
#### Authority ####
All users.
#### Examples ####
```
!
spanning-tree
spanning-tree config-name MST0
spanning-tree config-revision 3
spanning-tree instance 1 vlan 2
spanning-tree instance 1 vlan 1
spanning-tree priority 12
spanning-tree hello-time 5
spanning-tree forward-delay 5
spanning-tree max-age 10
spanning-tree max-hops 10
spanning-tree transmit-hold-count 5
spanning-tree instance 1 priority 12
interface 2
    spanning-tree instance 1 cost 2000000
interface 1
    spanning-tree instance 1 port-priority 12
    spanning-tree instance 1 cost 200000
```
