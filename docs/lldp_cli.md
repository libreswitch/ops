LLDP Commands
======
## Contents

- [LLDP configuration commands](#lldp-configuration-commands)
	- [Enable LLDP](#enable-lldp)
	- [Disable LLDP](#disable-lldp)
	- [Clear LLDP counters](#clear-lldp-counters)
	- [Clear LLDP neighbor details](#clear-lldp-neighbor-details)
	- [Set LLDP holdtime](#set-lldp-holdtime)
	- [Set LLDP holdtime to default](#set-lldp-holdtime-to-default)
	- [Set LLDP reinit delay](#set-lldp-reinit-delay)
	- [Set LLDP reinit delay to default](#set-lldp-reinit-delay-to-default)
	- [Set management IP address](#set-management-ip-address)
	- [Remove management IP address](#remove-management-ip-address)
	- [Select TLVs](#select-tlvs)
	- [Remove TLVs](#remove-tlvs)
	- [Set LLDP timer](#set-lldp-timer)
	- [Set LLDP timer to default](#set-lldp-timer-to-default)
	- [Enable LLDP transmission](#enable-lldp-transmission)
	- [Disable LLDP transmission](#disable-lldp-transmission)
	- [Enable LLDP reception](#enable-lldp-reception)
	- [Disable LLDP reception](#disable-lldp-reception)
- [LLDP show commands](#lldp-show-commands)
	- [Show LLDP configuration](#show-lldp-configuration)
	- [Show LLDP TLV](#show-lldp-tlv)
	- [Show LLDP neighbor information](#show-lldp-neighbor-information)
	- [Show LLDP neighbor information for the interface](#show-lldp-neighbor-information-for-the-interface)
	- [Show LLDP statistics](#show-lldp-statistics)
	- [Show LLDP statistics for the interface](#show-lldp-statistics-for-the-interface)
	- [Show LLDP local device information](#show-lldp-local-device-information)

## LLDP configuration commands

All LLDP configuration commands except `lldp transmission` and `lldp reception` work in config context.
### Enable LLDP
#### Syntax
`lldp enable`
#### Description
This command enables the LLDP (Link Layer Discovery Protocol) feature in the device. By default, LLDP is enabled on the device.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# lldp enable
```
### Disable LLDP
#### Syntax
`no lldp enable`
#### Description
This command disables the LLDP (Link Layer Discovery Protocol) feature in the device.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no lldp enable
```
### Clear LLDP counters
#### Syntax
`lldp clear counters`
#### Description
This command clears LLDP neighbor counters.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# lldp clear counters
```
### Clear LLDP neighbor details
#### Syntax
`lldp clear neighbors`
#### Description
This command clears LLDP neighbor details.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# lldp clear neighbors
```
### Set LLDP holdtime
<!--Change the value of the anchor tag above, so this command can be directly linked. -->
#### Syntax
`lldp holdtime <time>`
#### Description
This command sets the amount of time (in seconds), a receiving device holds the information sent before discarding it.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *time* | Required | 2-10 | Select hold time between 2 and 10 seconds.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# lldp holdtime 5
```
### Set LLDP holdtime to default
#### Syntax
`no lldp holdtime`
#### Description
This command sets default values for the amount of time a receiving device should hold the information sent before discarding it. The default value is 4 seconds.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no lldp holdtime
```

### Set LLDP reinit delay
#### Syntax
`lldp reinit <time>`
#### Description
This command sets the amount of time (in seconds) to wait before performing LLDP initialization on any interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *time* | Required | 1-10 | Select reinit delay between 1 and 10 seconds.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# lldp reinit 5
```
### Set LLDP reinit delay to default
#### Syntax
`no lldp reinit`
#### Description
This command resets to default value the amount of time to wait before performing LLDP initialization on any interface. The default value is 2 seconds.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no lldp reinit
```

### Set management IP address
#### Syntax
`lldp management-address ( <ipv4_address> | <ipv6_address>)`
#### Description
This command sets the Management IP Address to be sent using LLDP TLV.
#### Authority
All users.
#### Parameters
Choose one of the following as parameters.

| Parameter | Syntax | Description |
|:-----------|:----------------:|:---------------------------------------|
| *ipv4_address* | A.B.C.D | Set IPV4 address as LLDP management address.
| *ipv6_address* | X:X::X:X | Set IPV6 address as LLDP management address.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# lldp management-address 16.93.49.9
ops-as5712(config)# lldp management-address 2001:db8:85a3::8a2e:370:7334
```
### Remove management IP address
#### Syntax
`no lldp management-address`
#### Description
This command removes the Management IP Address to be sent using LLDP TLV.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no lldp management-address
```
### Select TLVs
#### Syntax
`lldp select-tlv (management-address | port-description | port-vlan-id  | port-vlan-name | port-protocol-vlan-id | port-protocol-id | system-capabilities | system-description | system-name)`
#### Description
This command selects the TLVs to be sent and received in LLDP packets.
#### Authority
All users.
#### Parameters
Choose one of the following parameters.

| Parameter | Description |
|:-----------|:---------------------------------------|
| **management-address** | Select management-address TLV.
| **port-description**  | Select port-description TLV.
| **port-vlan-id**  | Select port-vlan-id TLV.
| **port-vlan-name** | Select port-vlan-name TLV.
| **port-protocol-vlan-id** | Select port-protocol-vlan-id TLV.
| **port-protocol-id**  | Select port-protocol-id TLV.
| **system-capabilities** | Select system-capabilities TLV.
| **system-description** | Select system-description TLV.
| **system-name** | Select system-name TLV.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# lldp select-tlv management-address
ops-as5712(config)# lldp select-tlv port-description
ops-as5712(config)# lldp select-tlv port-vlan-id
ops-as5712(config)# lldp select-tlv port-vlan-name
ops-as5712(config)# lldp select-tlv port-protocol-vlan-id
ops-as5712(config)# lldp select-tlv port-protocol-id
ops-as5712(config)# lldp select-tlv system-capabilities
ops-as5712(config)# lldp select-tlv system-description
ops-as5712(config)# lldp select-tlv system-name
```
### Remove TLVs
#### Syntax
`no lldp select-tlv (management-address | port-description | port-vlan-id  | port-vlan-name | port-protocol-vlan-id | port-protocol-id | system-capabilities | system-description | system-name)`
#### Description
This command removes the TLVs from being sent and received in LLDP packets.
#### Authority
All users.
#### Parameters
Choose one of the following parameters.

| Parameter | Description |
|:-----------|:---------------------------------------|
| **management-address** | Select management-address TLV.
| **port-description**  | Select port-description TLV.
| **port-vlan-id**  | Select port-vlan-id TLV.
| **port-vlan-name** | Select port-vlan-name TLV.
| **port-protocol-vlan-id** | Select port-protocol-vlan-id TLV.
| **port-protocol-id**  | Select port-protocol-id TLV.
| **system-capabilities** | Select system-capabilities TLV.
| **system-description** | Select system-description TLV.
| **system-name** | Select system-name TLV.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no lldp select-tlv management-address
ops-as5712(config)# no lldp select-tlv port-description
ops-as5712(config)# no lldp select-tlv port-vlan-id
ops-as5712(config)# no lldp select-tlv port-vlan-name
ops-as5712(config)# no lldp select-tlv port-protocol-vlan-id
ops-as5712(config)# no lldp select-tlv port-protocol-id
ops-as5712(config)# no lldp select-tlv system-capabilities
ops-as5712(config)# no lldp select-tlv system-description
ops-as5712(config)# no lldp select-tlv system-name
```
### Set LLDP timer
#### Syntax
`lldp timer <time>`
#### Description
This command sets the LLDP status update interval in seconds which are transmitted to neighbors.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *time* | Required | 5-32768| Select timer between 5 and 32768 seconds
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# lldp timer 7
```
### Set LLDP timer to default
#### Syntax
`no lldp timer`
#### Description
This command sets the default time interval for transmitting LLDP status updates to neighbors. The default value is 30 seconds.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no lldp timer
```
### Enable LLDP transmission
#### Syntax
`lldp transmit`
#### Description
This command enables LLDP transmission (TX) for a particular interface. This command only works in interface context.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# lldp transmit
```
### Disable LLDP transmission
#### Syntax
`no lldp transmit`
#### Description
This command disables LLDP transmission (TX) for a particular interface. This command only works in interface context.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no lldp transmit
```
### Enable LLDP reception
#### Syntax
`lldp receive`
#### Description
This command enables LLDP reception (RX) for a particular interface. This command only works in interface context.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# lldp receive
```
### Disable LLDP reception
#### Syntax
`no lldp receive`
#### Description
This command disables LLDP reception (RX) for a particular interface. This command only works in interface context.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no lldp receive
```

## LLDP show commands
### Show LLDP configuration
#### Syntax
`show lldp configuration`
#### Description
This command displays various switch LLDP configurations. The configuration includes the LLDP timer, transmission status, reception status, selected TLVs and so on.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show lldp configuration
LLDP Global Configuration:

LLDP Enabled :No
LLDP Transmit Interval :30
LLDP Hold time Multiplier :4

TLVs advertised:
Management Address
Port description
Port VLAN-ID
Port Protocol VLAN-ID
Port VLAN Name
Port Protocol-ID
System capabilities
System description
System name

LLDP Port Configuration:

Port  Transmission-enabled     Receive-enabled
1      Yes                               Yes
10     Yes                               Yes
11     Yes                               Yes
12     Yes                               Yes
13     Yes                               Yes
...........
...........
```
### Show LLDP TLV
#### Syntax
`show lldp tlv`
#### Description
This command displays TLVs that will be sent and received in LLDP packets.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show lldp tlv

TLVs advertised:
Management Adress
Port description
Port VLAN-ID
Port Protocol VLAN-ID
Port VLAN Name
Port Protocol-ID
System capabilities
System description
System name
```
### Show LLDP neighbor information
#### Syntax
`show lldp neighbor-info`
#### Description
This command displays information about the switch's neighbors.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show lldp neighbor-info

Total neighbor entries : 1
Total neighbor entries deleted : 0
Total neighbor entries dropped : 0
Total neighbor entries aged-out : 0

Local Port     Neighbor Chassis-ID      Neighbor Port-ID         TTL
1                 10:60:4b:39:3e:80      1                      120
2
3
-----------
-----------
```
### Show LLDP neighbor information for the interface
#### Syntax
`show lldp neighbor-info <interface>`
#### Description
This command displays detailed information about a particular neighbor connected to a particular interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. System defined. |
#### Examples
```
ops-as5712# show lldp neighbor-info 1
Port                           : 1
Neighbor entries               : 1
Neighbor entries deleted       : 0
Neighbor entries dropped       : 0
Neighbor entries age-out       : 0
Neighbor Chassis-Name          : HP-3800-24G-PoEP-2XG
Neighbor Chassis-Description   : HP J9587A 3800-24G-PoE+-2XG Switch, revision KA.15.15.0006, ROM KA.15.09 (/ws/swbuildm/rel_nashville_qaoff/code/build/tam(swbuildm_rel_nashville_qaoff_rel_nashville))
Neighbor Chassis-ID            : 10:60:4b:39:3e:80
Neighbor Management-Address    : 192.168.1.1
Chassis Capabilities Available : Bridge, Router
Chassis Capabilities Enabled   : Bridge
Neighbor Port-ID               : 1
TTL                            : 120
```
### Show LLDP statistics
#### Syntax
`show lldp statistics`
#### Description
This command displays global LLDP statistics such as packet counts, unknown TLV received and so on.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# show lldp statistics
LLDP Global statistics:

Total Packets transmitted : 9
Total Packets received : 12
Total Packet received and discarded : 0
Total TLVs unrecognized : 0
LLDP Port Statistics:
Port-ID   Tx-Packets     Rx-packets     Rx-discarded        TLVs-Unknown
1          9                12                  0                  0
10         0                0                   0                  0
...........
...........
```
### Show LLDP statistics for the interface
#### Syntax
`show lldp statistics <interface>`
#### Description
This command displays LLDP statistics for a particular interface such as packet counts, unknown TLV received and so on.
#### Authority
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. System defined. |
#### Examples
```
ops-as5712# show lldp statistics 1
LLDP statistics:

Port Name: 1
Packets transmitted :20
Packets received :23
Packets received and discarded :0
Packets received and unrecognized :0
```

### Show LLDP local device information
#### Syntax
`show lldp local-device`
#### Description
This command displays information advertised by the switch if LLDP feature is enabled by user.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
If all ports are administratively down and link state is down, only global info will be displayed.
```
ops-as5712# show lldp local-device
Global Data
---------------

Chassis-id             : 48:0f:cf:af:50:c9
System Name            : switch
System Description     : OpenSwitch 0.1.0 (basil) Linux 3.9.11 #1 SMP Fri Sep 11 19:46:19 UTC 2015 x86_64
Management Address     : 120.92.155.52
Capabilities Available : Bridge, Router
Capabilities Enabled   : Bridge, Router
TTL                    : 120

```

If port 1 is administratively down and the link state is up, global info and only active port details are displayed.
```
Global Data
---------------

Chassis-id             : 48:0f:cf:af:50:c9
System Name            : switch
System Description     : OpenSwitch 0.1.0 (basil) Linux 3.9.11 #1 SMP Fri Sep 11 19:46:19 UTC 2015 x86_64
Management Address     : 120.92.155.52
Capabilities Available : Bridge, Router
Capabilities Enabled   : Bridge, Router
TTL                    : 120

Port Based Data:
----------------

Port-ID           : 1
Port-Description  : "1"

```
If the VLANs are configured on the active ports, the VLAN-Id and VLAN name are displayed along with port details.

The VLAN is configured in access mode (vlan access 100).

```
Global Data
---------------

Chassis-id             : 48:0f:cf:af:50:c9
System Name            : switch
System Description     : OpenSwitch 0.1.0 (basil) Linux 3.9.11 #1 SMP Fri Sep 11 19:46:19 UTC 2015 x86_64
Management Address     : 120.92.155.52
Capabilities Available : Bridge, Router
Capabilities Enabled   : Bridge, Router
TTL                    : 120

Port Based Data:
----------------

Port-ID           : 1
Port-Description  : "1"
Port VLAN Id      : 100
VLAN-Ids          : 100
VLAN Name         : VLAN100

```
The VLAN is configured in trunk mode (vlan trunk 200 300).
```
Global Data
---------------

Chassis-id             : 48:0f:cf:af:50:c9
System Name            : switch
System Description     : OpenSwitch 0.1.0 (basil) Linux 3.9.11 #1 SMP Fri Sep 11 19:46:19 UTC 2015 x86_64
Management Address     : 120.92.155.52
Capabilities Available : Bridge, Router
Capabilities Enabled   : Bridge, Router
TTL                    : 120

Port Based Data:
----------------

Port-ID           : 1
Port-Description  : "1"
Port VLAN Id      :
VLAN-Ids          : 200, 300
VLAN Name         : VLAN200, VLAN300

```
The VLAN is configured in native tagged or untagged mode (vlan native 100, vlan trunk 200 300).
```
Global Data
---------------

Chassis-id             : 48:0f:cf:af:50:c9
System Name            : switch
System Description     : OpenSwitch 0.1.0 (basil) Linux 3.9.11 #1 SMP Fri Sep 11 19:46:19 UTC 2015 x86_64
Management Address     : 120.92.155.52
Capabilities Available : Bridge, Router
Capabilities Enabled   : Bridge, Router
TTL                    : 120

Port Based Data:
----------------

Port-ID           : 1
Port-Description  : "1"
Port VLAN Id      : 100
VLAN-Ids          : 100, 200, 300
VLAN Name         : VLAN100, VLAN200, VLAN300

```
