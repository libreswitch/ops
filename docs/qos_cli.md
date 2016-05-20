# Quality of Service Commands
<!-- Version 3 -->

## Contents
- [Definition of terms](#definition-of-terms)
- [QoS global configuration commands](#qos-global-configuration-commands)
  - [apply qos](#apply-qos)
  - [qos cos-map](#qos-cos-map)
  - [qos dscp-map](#qos-dscp-map)
  - [qos queue-profile](#qos-queue-profile)
  - [qos schedule-profile](#qos-schedule-profile)
  - [qos trust](#qos-trust)
- [QoS interface configuration commands](#qos-interface-configuration-commands)
  - [interface apply qos](#interface-apply-qos)
  - [interface qos dscp](#interface-qos-dscp)
  - [interface qos trust](#interface-qos-trust)
- [QoS queue profile configuration commands](#qos-queue-profile-configuration-commands)
  - [name](#name)
  - [map](#map)
- [QoS schedule profile configuration commands](#qos-schedule-profile-configuration-commands)
  - [strict](#strict)
  - [dwrr](#dwrr)
- [Display commands](#display-commands)
  - [show interface](#show-interface)
  - [show interface](#show-interface)
  - [show qos cos-map](#show-qos-cos-map)
  - [show qos dscp-map](#show-qos-dscp-map)
  - [show qos queue-profile](#show-qos-queue-profile)
  - [show qos schedule-profile](#show-qos-schedule-profile)
  - [show qos trust](#show-qos-trust)
  - [show running config](#show-running-config)
  - [show running config interface](#show-running-config-interface)
- [Common troubleshooting](#common-troubleshooting)

## Definition of terms
| Term | Description |
|:-----------|:---------------------------------------|
| **Class** | For networking, a set of packets sharing some common characteristic (for example, all IPv4 packets). |
| **Codepoint**| Used in two different ways -- either as the name of a packet header field, or as the name of the values carried within a packet header field. *Example 1: Priority Code Point (PCP) is the name of a field in the [IEEE 802.1Q](http://www.ieee802.org/1/pages/802.1Q.html) VLAN tag. Example 2: Differentiated Services codepoint (DSCP) is the name of values carried within the DS field of the header field.*
| **Color** | A metadata label associated with each packet within the switch with three values: green, yellow, or red. It is used by the switch when packets encounter congestion for a resource (queue) to distinguish which packets should be dropped. |
| **Class of Service (CoS)** | A 3-bit value used to mark packets with one of eight classes (levels of priority). It is carried within the Priority Code Point (PCP) field of the [IEEE 802.1Q](http://www.ieee802.org/1/pages/802.1Q.html) VLAN tag. |
| **Differentiated Services codepoint (DSCP)** | A 6-bit value used to mark packets for different per-hop behavior as originally defined by [IETF RFC 2474](https://tools.ietf.org/html/rfc2474). It is carried within the Differentiated Services (DS) field of the IPv4 or IPv6 header. |
| **Local-priority** | A metadata label associated with a packet within a network switch. It is used by the switch to distinguish packets for different treatment (for example, queue assignment). |
| **Metadata** | Information labels associated with each packet in the switch that are separate from the packet headers and data. These labels are used by the switch in its handling of the packet. For example, arrival port, egress port, VLAN membership, local priority, and color. |
| **Priority Code Point (PCP)** | The name of a 3-bit field in the [IEEE 802.1Q](http://www.ieee802.org/1/pages/802.1Q.html) VLAN tag. It carries the CoS value to mark a packet with one of 8 classes (priority levels). |
| **Quality of Service (QoS)** | General term used when describing or measuring performance. For networking, it means how different classes of packets are treated across the network or device. For more information, see [https://en.wikipedia.org/wiki/Quality_of_service](https://en.wikipedia.org/wiki/Quality_of_service). |
| **Traffic class (TC)** | General term for a set of packets sharing some common characteristic. It used to be the name of an 8-bit field in the IPv6 header originally defined by [IETF RFC 2460](https://tools.ietf.org/html/rfc2460#section-7). This field name was changed to Differentiated Services by [IETF RFC 2474](https://tools.ietf.org/html/rfc2474). |
| **Type of Service (ToS)** | General term when there are different levels of treatment (for example, fare class).  It used to be the name of an 8-bit field in the IPv4 header originally defined by [IETF RFC 791](https://tools.ietf.org/html/rfc791). This field name was changed to Differentiated Services by [IETF RFC 2474](https://tools.ietf.org/html/rfc2474)|


## QoS global configuration commands

These commands are entered in the global configuration context.

## apply qos

#### Syntax

`apply qos queue-profile <NAME> schedule-profile {<NAME> | strict}`

#### Description
The `apply qos` command in the global configuration context configures the given queue profile and schedule profile at the global level. Global profiles are configured on all Ethernet interfaces and LAGs that have not applied their own profiles.

**This may cause the interface(s) or LAG(s) to shut down briefly during the reconfiguration.**

For a queue profile to be complete and ready to be applied, all local priorities must be mapped to a queue.

For the schedule profile to be complete and ready to be applied, it must have a configuration for each queue defined by the queue profile. All queues must use the same algorithm except for the highest numbered queue, which may be "strict".

There is a special, pre-defined schedule-profile named "strict". It is always present and unalterable. The strict profile services all queues of an associated queue profile using the strict priority algorithm.

Both the queue profile and the schedule profile must specify the same number of queues.

An applied profile cannot be updated or deleted until such time that it is no longer applied.

The `no apply qos` command is disallowed in the global configuration context.  It is required to always have a global and schedule profile applied.  To cease the use of a profile, apply a different profile.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* | The name of the profile to apply
| *strict* | Use the strict schedule profile

#### Examples
```
switch# configure terminal
switch(config)# apply qos queue-profile default schedule-profile strict
```

#### Troubleshooting
See the [Common troubleshooting](#common-troubleshooting) section for error messages that may appear as the output of various commands.

If a profile fails to be applied to the hardware, then the desired configuration may differ from the actual configuration (known as "status"). In this case, the desired configuration and the actual configuration (status) would both be displayed by the `show interface` command. In the following example, the desired schedule profile is strict, but the actual schedule profile in hardware is default:
```
switch# configure terminal
switch(config)# apply qos queue-profile default schedule-profile strict
switch(config-if)# do show interface 1

Interface 1 is down (Administratively down)
 Admin state is down
 State information: admin_down
 Hardware: Ethernet, MAC Address: 70:72:cf:e7:cc:67
 MTU 1500
 Full-duplex
 qos trust none
 qos queue-profile default
 qos schedule-profile strict, status is default
 Speed 0 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RX
            0 input packets              0 bytes
            0 input error                0 dropped
            0 CRC/FCS
       L3:
            ucast: 0 packets, 0 bytes
            mcast: 0 packets, 0 bytes
 TX
            0 output packets             0 bytes
            0 input error                0 dropped
            0 collision
       L3:
            ucast: 0 packets, 0 bytes
            mcast: 0 packets, 0 bytes
```

| Error Message | Description |
|:-----------|:---------------------------------------|
| *The queue profile has local priority NUM assigned more than once.* | This error message occurs when an apply command is attempted for a queue profile for which the given local priority has been assigned to more than one queue. The solution is to remove the local priority from one of the queues in the queue profile.
| *The queue profile and the schedule profile cannot contain different queues.* | This error message occurs when an apply command is attempted for a queue profile and a schedule profile that have different queues configured. The solution is to add or remove queues from the queue profile or the schedule profile until they both have the same queues configured.
| *The queue profile and the schedule profile applied on port NUM cannot contain different queues.* | This error message occurs when an apply command is attempted for a queue profile that has a different number of queues than a schedule profile that is currently applied at the port level. The solution is to remove the port schedule profile override for the given port, or to modify the queue profile such that it has the same number of queues as the port schedule profile.
| *Profile NAME does not exist.* | This error can occur if an apply command is attempted for a queue profile or a schedule profile that does not exist. The solution is to create the missing queue profile or schedule profile.
| *The schedule profile must have the same algorithm assigned to each queue.* | This error can occur if an apply command is attempted for a schedule profile that does not have the same algorithm assigned to every queue. The solution is to change the algorithm assigned to each queue until all queues have the same algorithm assigned. The exception is that the highest priority queue is always allowed to be assigned the strict algorithm.

## qos cos-map

#### Syntax
`qos cos-map <0-7> local-priority <NUM> [color <COLOR>] [name <DESCRIPTION>]`
`no qos cos-map <0-7>`

#### Description
The **cos-map** command associates local-priority, color, and optionally a descriptive name to each 802.1 VLAN priority code point (COS).

This table is used when a port's QoS trust mode is set to "cos" to mark packets initial local-priority and color (see [qos trust](#qos-trust)).

The default color is "green". The default name is an empty string.

The **no cos-map** command will restore the assignments for a priority code point back to its factory default.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *COS* |  802.1 VLAN Priority Code Point from 0 to 7. |
| *NUM* |  Switch-specific local priority value. |
| *COLOR* | One of the following tokens: green, yellow, or red. |
| *DESCRIPTION* | Contains up to 64 characters for customer documentation. The allowed characters are alphanumeric, underscore ( _ ), hyphen ( - ), and dot ( . ). |

#### Examples
```
switch# configure terminal
switch(config)# qos cos-map 1 local-priority 2 color green name EntryName
```

## qos dscp-map

#### Syntax
`qos dscp-map <0-63> local-priority <NUM> [color <COLOR>] [name <DESCRIPTION>]`
`no qos dscp-map <0-63>`

#### Description
The `dscp-map` command associates local-priority, color, and optionally a descriptive name to each IP differentiated services code point (DSCP).  This command can optionally remark the incoming 802.1 VLAN CoS PCP.

This table is used when a port's  QoS trust mode is set to 'dscp' to assign the packets initial local-priority and color.

The default color is green.  The default name is an empty string.

The "no" form of the command restores the assignments for a code point back to its factory default.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *DSCP* | IP Differentiated Services Code Point from 0 to 63. |
| *NUM* |  ASIC-specific local priority value from 0 to 7. |
| *COLOR* | One of the following tokens: green, yellow, or red. |
| *DESCRIPTION* | Contains up to 64 characters for customer documentation. The allowed characters are alphanumeric, underscore ( _ ), hyphen ( - ), and dot ( . ). |

#### Examples
```
switch# configure terminal
switch(config)# qos dscp-map 1 local-priority 2 color green name EntryName
```

## qos queue-profile

#### Syntax
`qos queue-profile <NAME>`
`no qos queue-profile <NAME>`

#### Description
The `queue-profile` command is used to enter the queue-profile configuration context to create or edit a named queue profile.

The "no" form of the command deletes the named queue profile, if it is not currently applied.

##### Default profile

There is a special, pre-defined profile named "default". At installation, a factory supplied default queue-profile is automatically applied. The default profile is editable as long as it is not applied.

The `show qos queue-profile default` command displays current contents of the profile.

The profile named "default" cannot be deleted. The `no queue-profile default` command resets the default profile back to the factory supplied profile.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* | Contains up to 64 characters for customer documentation. The allowed characters are alphanumeric, underscore ( _ ), hyphen ( - ), and dot ( . ).

#### Examples
```
switch# configure terminal
switch(config)# qos queue-profile Profile_Name_v1
```

#### Troubleshooting
See the [Common troubleshooting](#common-troubleshooting) section for error messages that may appear as the output of various commands.

| Error Message | Description |
|:-----------|:---------------------------------------|
| *The profile name cannot be 'strict'.* | This error occurs when the profile name parameter is the reserved profile name "strict". The solution is to select another profile name that is not "strict".
| *An applied profile cannot be amended or deleted.* | This error occurs when an applied profile is attempted to be modified or deleted. The solution is to modify a different profile, or to apply a different profile so that the given profile can be modified.
| *A hardware default profile cannot be amended or deleted.* | This error occurs when the hardware default profile is attempted to be modified or deleted. The solution is to modify a different profile, since the hardware default profile cannot be modified.

## qos schedule-profile

#### Syntax
`qos schedule-profile <NAME>`
`no qos schedule-profile <NAME>`

#### Description
The `schedule-profile` command is used to enter the schedule-profile configuration context to create or edit a named schedule profile.

The "no" form of the command deletes the named schedule profile, if it is not currently applied.

##### Default schedule profile

There is a special, pre-defined profile named "default". At installation, a factory supplied default schedule-profile is automatically applied. The default profile is editable as long as it is not applied.

The `show qos schedule-profile default` command displays current contents of the profile.

The profile named "default" cannot be deleted. The `no schedule-profile default` command resets the default profile back to the factory supplied profile.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* | Contains up to 64 characters for customer documentation. The allowed characters are alphanumeric, underscore ( _ ), hyphen ( - ), and dot ( . ).

#### Examples
```
switch# configure terminal
switch(config)# qos schedule-profile Profile_Name_v2
```

#### Troubleshooting
See the [Common troubleshooting](#common-troubleshooting) section for error messages that may appear as the output of various commands.

| Error Message | Description |
|:-----------|:---------------------------------------|
| *The profile name cannot be 'strict'.* | This error occurs when the profile name parameter is the reserved profile name "strict". The solution is to select another profile name that is not "strict".
| *An applied profile cannot be amended or deleted.* | This error occurs when an applied profile is attempted to be modified or deleted. The solution is to modify a different profile, or to apply a different profile so that the given profile can be modified.
| *A hardware default profile cannot be amended or deleted.* | This error occurs when the hardware default profile is attempted to be modified or deleted. The solution is to modify a different profile, since the hardware default profile cannot be modified.

## qos trust

#### Syntax
`qos trust {none|cos|dscp}`
`no qos trust`

#### Description
The `trust` command configures one of three modes that be applied globally on all Ethernet interfaces and LAGs.  The modes determine which of any packet field values are used to assign the initial Local-priority and Color metadata values to the packet from the CoS or DSCP Map tables.

The `no qos trust` command restores the trust mode back to the factory default.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| none | Ignores all packet headers. The packet is initially assigned local_priority of zero and color of green.
| cos | For 802.1 VLAN tagged packets, use the priority code point field value of the outermost VLAN header as the index into the COS Map. If the packet is untagged, use the metadata values at index zero of the COS Map.
| dscp | For IP packets, use the DSCP value as the index into the DSCP Map. For non-IP packets with 802.1 VLAN tag(s), use the priority code point field value of the outermost tag header as the index into the CoS Map.  For untagged, non-IP packets, use the metadata values at index zero of the CoS Map.

#### Examples
```
switch# configure terminal
switch(config)# qos trust dscp
```

## QoS interface configuration commands

These commands are entered in the interface configuration context.

## interface apply qos

#### Syntax

`(config-if)# apply qos schedule-profile {<NAME> | strict}`
`(config-if)# no apply qos schedule-profile`

#### Description
The `apply qos` command in the Ethernet or LAG interface configuration context configures the given schedule profile just for that interface. It overrides any schedule-profile applied in the global context.

**This may cause the interface (or LAG) to shutdown briefly during the reconfiguration.**

**NOTE:** The same name as the currently applied schedule-profile can be applied in the global context. This guarantees that the interface always uses this schedule-profile, even when the global context schedule-profile subsequently changes.

For the schedule profile to be complete and ready to be applied, it must have a configuration for each queue defined by the queue profile. All queues must use the same algorithm (for examplem DWRR), except for the highest numbered queue, which may be "strict".

An applied profile cannot be updated or deleted until it is no longer applied.

##### Strict schedule profile
There is a special, pre-defined profile named "strict". It is always present and unalterable. The strict profile services all queues of an associated queue profile using strict priority scheduling.

The `no apply qos schedule-profile` command clears a schedule profile override for a given interface and the interface uses the global schedule profile. This is the only way to remove a schedule-profile override from the interface.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* | The name of the profile to apply. |
| *strict* | Use the strict schedule profile. |

#### Examples
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# apply qos schedule-profile strict
```

#### Troubleshooting
See the [Common troubleshooting](#common-troubleshooting) section for error messages that may appear as the output of various commands.

If a profile fails to be applied to the hardware, then the desired configuration may differ from the actual configuration (known as "status"). In this case, the desired configuration and the actual configuration (status) would both be displayed by the `show interface` command. In the following example, the desired schedule profile is "strict", but the actual schedule profile in hardware is "default":
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# apply qos schedule-profile strict
switch(config-if)# do show interface 1

Interface 1 is down (Administratively down)
 Admin state is down
 State information: admin_down
 Hardware: Ethernet, MAC Address: 70:72:cf:e7:cc:67
 MTU 1500
 Full-duplex
 qos trust none
 qos queue-profile default
 qos schedule-profile strict, status is default
 Speed 0 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RX
            0 input packets              0 bytes
            0 input error                0 dropped
            0 CRC/FCS
       L3:
            ucast: 0 packets, 0 bytes
            mcast: 0 packets, 0 bytes
 TX
            0 output packets             0 bytes
            0 input error                0 dropped
            0 collision
       L3:
            ucast: 0 packets, 0 bytes
            mcast: 0 packets, 0 bytes
```

| Error Message | Description |
|:-----------|:---------------------------------------|
| *The queue profile and the schedule profile cannot contain different queues.* | This error message occurs when an apply command is attempted for a queue profile and a schedule profile that have different queues configured. The solution is to add or remove queues from the queue profile or the schedule profile until they both have the same queues configured.
| *Profile NAME does not exist.* | This error can occur if an apply command is attempted for a queue profile or a schedule profile that does not exist. The solution is to create the missing queue profile or schedule profile.
| *The schedule profile must have the same algorithm assigned to each queue.* | This error can occur if an apply command is attempted for a schedule profile that does not have the same algorithm assigned to every queue. The solution is to change the algorithm assigned to each queue until all queues have the same algorithm assigned. The exception is that the highest priority queue is always allowed to be assigned the strict algorithm.

## interface qos dscp

#### Syntax

`(config-if)# qos dscp <0-63>`
`(config-if)# $ no qos dscp`

#### Description
The 'qos dscp' command in the Ethernet or LAG interface configuration context configures a DSCP override just for that interface. It is only allowed if the interface trust mode is "none".

**NOTE:** If a DSCP override has been configured, and the trust mode is subsequently set to "cos" or "dscp", then the DSCP override is ignored.

The `no qos dscp` command clears the DSCP override for the interface.

##### For all arriving IPv4 or IPv6 packets:
- Initial local-priority and color metadata are assigned from the DSCP map entry indexed by the DSCP override value.
- Remark the packet's DSCP in IPv4 or IPv6 DS header field with the DSCP override value.

##### For all arriving non-IP packets:
- Initial local-priority and color metadata are assigned from the CoS Map entry index 0.
- The CoS of all arriving tagged non-IP packets are unchanged.
  - If the packet is subsequently transmitted with a 802.1Q VLAN tag, the PCP field contains the unchanged CoS.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *<0-63>* | Index into the DSCP Map. |

#### Examples
```
switch# configure terminal
switch(config)# qos trust cos
switch(config)# interface 1
switch(config-if)# qos trust none
switch(config-if)# qos dscp 0
```

#### Troubleshooting
See the [Common troubleshooting](#common-troubleshooting) section for error messages that may appear as the output of various commands.

| Error Message | Description |
|:-----------|:---------------------------------------|
| *QoS DSCP override is only allowed if the port trust mode is 'none'.* | This error occurs when a DSCP override command is attempted when the port trust mode is "none". The solution is to configure the port trust mode to "none".

## interface qos trust

#### Syntax

`(config-if)# qos trust {none|cos|dscp}`
`(config-if)# $ no qos trust`

#### Description
The `qos trust` command in the Ethernet or LAG interface configuration context configures a trust mode override just for that interface. It overrides the trust mode applied in the global context.  The modes determine which of any packet field values are used to assign the initial Local-priority and Color metadata values to the packet from the CoS or DSCP Map tables.

The `no qos trust` command clears the trust mode override for a given interface and the interface will use the global schedule profile. This is the only way to remove a trust mode override from the interface.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| none | Ignores all packet headers. The packet is initially assigned local_priority of zero and color of green.
| cos | For 802.1 VLAN tagged packets, use the priority code point field value of the outermost VLAN header as the index into the COS Map. If the packet is untagged, use the metadata values at index zero of the COS Map.
| dscp | For IP packets, use the DSCP value as the index into the DSCP Map. For non-IP packets with 802.1 VLAN tag(s), use the priority code point field value of the outermost tag header as the index into the CoS Map.  For untagged, non-IP packets, use the metadata values at index zero of the CoS Map.

#### Examples
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# qos trust dscp
```

## QOS queue profile configuration commands

To enter the queue profile context, enter the [qos queue-profile](#qos-queue-profile) command. The following commands are available in queue profile context:
- name
- map

##### Queue numbering

Queues are numbered consecutively starting from zero.  Queue zero is the lowest priority queue.  The larger the queue number, the higher priority the queue has in scheduling algorithms (see [QOS Schedule Profile Configuration Commands](#qos-schedule-profile-configuration-commands)).  The maximum allowed queue number may vary by product.  For products supporting eight queues, the largest queue number is seven. Please refer to the product specifications for the maximum.

##### Default profile

There is a special, pre-defined profile named "default". At installation, a factory supplied default queue-profile is automatically applied. The default profile is editable as long as it is not applied.


## name

#### Syntax
`name queue <0-7> <DESCRIPTION>`
`no name queue <0-7>`

#### Description
The `name` command assigns a descriptive string to a queue number in a queue profile.  It has no effect on the product configuration.

The descriptive string contains up to 64 characters for customer documentation. The allowed characters are alphanumeric, underscore ( _ ), hyphen ( - ), and dot ( . ).

The `no name` command deletes the name of a queue number in a queue profile.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *QUEUE* |  The queue number from 0 to 7
| *DESCRIPTION* |  The  string to assign to the queue number

#### Examples
```
switch# configure terminal
switch(config)# qos queue-profile Profile_Name
switch(config-queue)# name queue 0 Scavenger_and_backup_data
```

#### Troubleshooting
See the [Common troubleshooting](#common-troubleshooting) section for error messages that may appear as the output of various commands.

| Error Message | Description |
|:-----------|:---------------------------------------|
| *Profile NAME does not have queue NUM configured.* | This error occurs when a "no" command is attempted for a queue that has not yet been configured. The solution is to first configure the queue.

## map

#### Syntax
`map queue <0-7> local-priority <0-7>`
`no map queue <0-7> [local-priority <0-7>]`

#### Description
The `map` command assigns a local priority to a queue number in a queue profile. Packets marked with that local-priority use the queue.

More than one local-priority can be assigned to use the same queue. A queue without any local-priorities assigned is not used to store packets.

For a queue profile to be suitable to be applied (see [apply qos](#apply-qos)), all local-priorities must be assigned to some queue in the profile.

The `no map` command removes the assignment of the local priority from the queue number. If no local priority is provided, then the assignment of all local priorities are removed from the queue.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *QUEUE* |  The queue number from 0 to 7
| *LOCAL_PRIORITY* |  The local priority to add or remove from the queue number

#### Examples
```
switch# configure terminal
switch(config)# qos queue-profile ProfileName
switch(config-queue)# map queue 0 local-priority 1
```

#### Troubleshooting
See the [Common troubleshooting](#common-troubleshooting) section for error messages that may appear as the output of various commands.

| Error Message | Description |
|:-----------|:---------------------------------------|
| *Profile NAME does not have queue NUM configured.* | This error occurs when a "no" command is attempted for a queue that has not yet been configured. The solution is to first configure the queue. |

## QoS schedule profile configuration commands

To enter the schedule profile context, enter the [qos schedule-profile](#qos-schedule-profile) command. The following commands are available in queue profile context:
- strict
- dwrr (deficit weighted round robin)

##### Queue numbering

Queues in a schedule profile are numbered consecutively starting from zero.  Queue zero is the lowest priority queue.  The larger the queue number the higher priority the queue has in scheduling algorithms.  The maximum allowed queue number may vary by product.  For products supporting eight queues, the largest queue number is seven. Please refer to the product specifications for the maximum.

##### Allowed forms

There are two allowed forms for schedule profiles:
1. All queues use the same scheduling algorithm (for example, dwrr).
2. The highest queue number uses Strict Priority, and all remaining (lower) queues use the same algorithm (for example, dwrr).

The second form supports priority scheduling behavior necessary for the [IEFT RFC 3246 Expedited Forwarding](https://tools.ietf.org/html/rfc3246) specification.

##### Default schedule profile

There is a special, pre-defined profile named "default". At installation, a factory supplied default schedule-profile is automatically applied. The default profile is editable as long as it is not applied.

##### Strict schedule profile
There is a special, pre-defined profile named "strict". It is always present and unalterable. The strict profile services all queues of an associated queue profile using the strict priority algorithm.

## strict

#### Syntax
`strict queue <0-7>`
`no strict queue <0-7>`

#### Description
The `strict` command assigns the strict priority algorithm to a queue. Strict priority services all packets waiting in a queue before any packets in lower priority queues are serviced.

The `no strict` command only clears the algorithm for a queue when the algorithm already assigned is Strict Priority.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *QUEUE* |  The queue number from 0 to 7. |

#### Examples
```
switch# configure terminal
switch(config)# qos schedule-profile Profile_1p7q
switch(config-schedule)# strict queue 7
```

#### Troubleshooting
See the [Common troubleshooting](#common-troubleshooting) section for error messages that may appear as the output of various commands.

| Error Message | Description |
|:-----------|:---------------------------------------|
| *Profile NAME does not have queue NUM configured.* | This error occurs when a "no" command is attempted for a queue that has not yet been configured. The solution is to first configure the queue. |

## dwrr

#### Syntax
`dwrr queue <0-7> weight <1-127>`
`no dwrr queue <0-7>`

#### Description
The `dwrr` command assigns the deficit weighted round robin algorithm and its byte weight to a queue.

Deficit weight round robin apportions available bandwidth among all non-empty queues in relation to their queue weights. A product will either support deficit weighted round robin or weighted round robin, but not both. See the specifications for the product.

The `no dwrr` command only clears the algorithm for a queue when the algorithm already assigned is deficit weighted round robin.

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *QUEUE* |  The queue number from 0 to 7
| *WEIGHT* |  The weight to use for the dwrr scheduling. |

#### Examples
```
switch# configure terminal
switch(config)# qos schedule-profile ProfileName
switch(config-schedule)# dwrr queue 0 weight 11
switch(config-schedule)# dwrr queue 1 weight 17
```

#### Troubleshooting
See the [Common troubleshooting](#common-troubleshooting) section for error messages that may appear as the output of various commands.

| Error Message | Description |
|:-----------|:---------------------------------------|
| *Profile NAME does not have queue NUM configured.* | This error occurs when a "no" command is attempted for a queue that has not yet been configured. The solution is to first configure the queue. |

## Display commands
The following commands show configuration and status information.


## show interface

#### Syntax
`show interface <INTERFACE>`

#### Description
This command's display includes the QoS settings that have been configured for an interface.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *INTERFACE* | Required | System defined | Name of the interface. |

#### Examples
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# qos trust dscp
switch(config-if)# end
switch# show interface 1

Interface 1 is down (Administratively down)
 Admin state is down
 State information: admin_down
 Hardware: Ethernet, MAC Address: 70:72:cf:fc:51:de
 MTU 0
 Half-duplex
 qos trust dscp
 Speed 0 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RX
            0 input packets              0 bytes
            0 input error                0 dropped
            0 CRC/FCS
 TX
            0 output packets             0 bytes
            0 input error                0 dropped
            0 collision

```


## show interface queues

#### Syntax
`show interface <INTERFACE> queues`

#### Description
This command displays statistics from each queue for an interface:
- Number of packets transmitted
- Number of bytes transmitted
- Number of packets that were not transmitted due to an error (for example: queue full)

Queues are numbered consecutively starting from zero. Queue zero is the lowest priority queue. The larger the queue number the higher priority the queue has in scheduling algorithms. The maximum allowed queue number may vary by product. For products supporting eight queues, the largest queue number is seven. Please refer to the product specifications for the maximum.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *INTERFACE* | Required | System defined | Name of the interface. |

#### Examples
```

switch# show interface 1 queues

Interface 1 is  (Administratively down)
 Admin state is down
 State information: admin_down
         Tx Packets             Tx Bytes  Tx Packet Errors
 Q0             100                 8000                 0
 Q1         1234567          12345678908                 5
 Q2              0                     0                 0
 Q3              0                     0                 0
 Q4              0                     0                 0
 Q5              0                     0                 0
 Q6              0                     0                 0
 Q7              0                     0                 0
```

## show qos cos-map

#### Syntax
`show qos cos-map [default]`

#### Description
This command displays the QoS cos-map.

#### Authority
All configuration users.

#### Parameters
The optional "default" parameter displays the factory default values.

#### Examples
```
switch# show qos cos-map default
code_point local_priority color   name
---------- -------------- ------- ----
0          1              green   Best_Effort
1          0              green   Background
2          2              green   Excellent_Effort
3          3              green   Critical_Applications
4          4              green   Video
5          5              green   Voice
6          6              green   Internetwork_Control
7          7              green   Network_Control
```

## show qos dscp-map

#### Syntax
`show qos dscp-map [default]`

#### Description
This command displays the QoS dscp-map.

#### Authority
All users.

#### Parameters
The optional "default" parameter displays the factory default values.

#### Examples
```
switch# show qos dscp-map default
code_point local_priority color   name
---------- -------------- ------- ----
0          0              green   "CS0"
1          0              green
2          0              green
3          0              green
4          0              green
5          0              green
6          0              green
7          0              green
8          1              green   "CS1"
9          1              green
10         1              green   "AF11"
11         1              green
12         1              yellow  "AF12"
13         1              green
14         1              red     "AF13"
15         1              green
16         2              green   "CS2"
17         2              green
18         2              green   "AF21"
19         2              green
20         2              yellow  "AF22"
21         2              green
22         2              red     "AF23"
23         2              green
24         3              green   "CS3"
25         3              green
26         3              green   "AF31"
27         3              green
28         3              yellow  "AF32"
29         3              green
30         3              red     "AF33"
31         3              green
32         4              green   "CS4"
33         4              green
34         4              green   "AF41"
35         4              green
36         4              yellow  "AF42"
37         4              green
38         4              red     "AF43"
39         4              green
40         5              green   "CS5"
41         5              green
42         5              green
43         5              green
44         5              green
45         5              green
46         5              green   "EF"
47         5              green
48         6              green   "CS6"
49         6              green
50         6              green
51         6              green
52         6              green
53         6              green
54         6              green
55         6              green
56         7              green   "CS7"
57         7              green
58         7              green
59         7              green
60         7              green
61         7              green
62         7              green
63         7              green
```

## show qos queue-profile

#### Syntax
`show qos queue-profile [{<NAME> | factory-default}]`

#### Description
When no parameter is provided, then a sorted list of defined profile names and their status is shown.

When a name is given, this command displays the details of the specified profile. The name "default" can be used to display the current details of that profile.

When the "factory-default" parameter is used in place of a name, then the factory supplied profile is displayed.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* |  The name of the profile to show. |
| *factory-default* |  Show the factory default profile. |

#### Examples
```
switch# show qos queue-profile factory-default
queue_num local_priorities name
--------- ---------------- ----
0         0                Scavenger_and_backup_data
1         1
2         2
3         3
4         4
5         5
6         6
7         7
```

## show qos schedule-profile

#### Syntax
`show qos schedule-profile [{<NAME> | factory-default}]`

#### Description
When no parameter is provided, then a sorted list of defined profile names and their status is shown.

When a name is given, this command displays the details of the specified profile. The name "default" can be used to display the current details of that profile.

When "factory-default" parameter is used in place of a name, then the factory supplied profile is displayed.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* |  The name of the profile to show. |
| *factory-default* |  Show the factory default profile. |

#### Examples
```
switch# show qos schedule-profile factory-default
queue_num algorithm weight
--------- --------- ------
0         dwrr      1
1         dwrr      1
2         dwrr      1
3         dwrr      1
4         dwrr      1
5         dwrr      1
6         dwrr      1
7         dwrr      1
```

## show qos trust

#### Syntax
`show qos trust [default]`

#### Description
This command displays the global QoS trust setting.

#### Authority
All users.

#### Parameters
The optional "default" parameter displays the factory default value.

#### Examples
```
switch# show qos trust default
qos trust none
```

## show running config

#### Syntax
`show running-config`

#### Description
This command displays the QoS settings that have been configured.

#### Authority
All users.

#### Parameters
No parameters.

#### Examples
```
switch# configure terminal
switch(config)# qos trust dscp
switch(config)# interface 1
switch(config-if)# qos trust cos
switch(config-if)# interface lag 10
switch(config-lag-if)# qos trust none
switch(config-lag-if)# end
switch# show running-config
Current configuration:
!
!
!
!
!
interface 1
    qos trust cos
interface lag 10
    qos trust none
qos trust dscp
```

## show running config interface

#### Syntax
`show running-config interface <interface>`

#### Description
This command displays the QoS settings that have been configured for an interface.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. |

#### Examples
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# qos trust dscp
switch(config-if)# end
switch# show running-config interface 1
interface 1
    qos trust dscp
   exit
```

## Common troubleshooting
The following error messages may appear as the output of various commands.

| Error Message | Description |
|:-----------|:---------------------------------------|
| *This field can have a length up to 64 characters.* | This error message occurs when a parameter is provided whose length is greater than 64 characters. The solution is to select a name that has 64 or fewer characters.
| *The allowed characters are alphanumeric, underscore ( _ ), hyphen ( - ), and dot ( . ).* | This error message occurs when a parameter is provided that contains illegal characters. The allowed characters are alphanumeric, underscore ( _ ), hyphen ( - ), and dot ( . ).
| *Unknown command* | This error message can occur if a required parameter is missing from the command, or if a given parameter is out of range. The solution is to ensure that all required parameters are specified for the command, and are within bounds.
| *Command incomplete* | This error message can occur if a required parameter is missing from the command. The solution is to ensure that all required parameters are specified for the command.
| *PROPERTY cannot be configured on a member of a LAG.* | This error message occurs if a command is attempted on an interface that is a member of a LAG. The solution is to execute the command on the LAG, or to remove the interface from the LAG.
