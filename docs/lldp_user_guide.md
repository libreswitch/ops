LLDP
======

## Contents
- [Contents](#contents)
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuring LLDP](#configuring-lldp)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Setting up optional configurations](#setting-up-optional-configurations)
	- [Verifying the configuration](#verifying-the-configuration)
		- [Viewing LLDP Global Information](#viewing-lldp-global-information)
		- [Viewing LLDP Neighbors](#viewing-lldp-neighbors)
		- [Viewing LLDP statistics](#viewing-lldp-statistics)
		- [Viewing LLDP TLVs](#viewing-lldp-tlvs)
		- [Viewing LLDP local device information](#viewing-lldp-local-device-information)
	- [Troubleshooting the configuration](#troubleshooting-the-configuration)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The Link Layer Discovery Protocol (LLDP) is an industry-standard, vendor-neutral method to allow networked devices to advertise capabilities, discover and identify other LLDP enabled devices and gather information in a LAN. The following bullet list contains some of the information gathered by LLDP:

- System name and description
- Port name and description
- VLAN name and identifier
- IP network management address
- Device Capabilities (for example, switch, router, or server)
- MAC address and physical layer information
- Power information

## Prerequisites
All the DUT interfaces (at least the interfaces that are connected to other devices) must be administratively up.

## Configuring LLDP
### Setting up the basic configuration
1. Configure the terminal to change the vtysh context to config context with the following commands:
```
ops-as5712# configure terminal
ops-as5712(config)#
```

2. Enable LLDP globally on the switch with the following command:
```
ops-as5712(config)# lldp enable
ops-as5712(config)#
```
Once LLDP is enabled, the switch begins to transmit advertisements from those ports that are configured to send LLDP packets.

3. Enable LLDP on interface.
By using the `lldp transmit` and `lldp receive` commands, LLDP can be enabled or disabled on individual interfaces or configured to only
send or only receive LLDP packets. Consider interface 1 which is connected to neighbor device,
```
ops-as5712(config)# interface 1
ops-as5712(config-if)# lldp receive
ops-as5712(config-if)#
ops-as5712(config-if)# lldp transmit
ops-as5712(config-if)#
```

### Setting up optional configurations

1. Setting the LLDP Timer.
The `lldp timer` command specifies the time in seconds between LLDP updates sent by the switch.
```
ops-as5712(config)# lldp timer 120
ops-as5712(config)#
```
The `no lldp timer` commands reverts the LLDP timer to its default value of 30 seconds.
```
ops-as5712(config)# no lldp timer
ops-as5712(config)#
```

2. Setting the LLDP Hold Time.
The `lldp holdtime` command sets the amount of time a receiving device should retain the information sent by the device.
```
ops-as5712(config)# lldp holdtime 5
ops-as5712(config)#
```
The `no lldp holdtime` commands reverts the LLDP timer to its default value of four seconds.
```
ops-as5712(config)# no lldp holdtime
ops-as5712(config)#
```

3. Set the LLDP reinitialization delay value.
The `lldp reinit` command sets the amount of time to wait before performing LLDP initialization on any interface.
```
ops-as5712(config)# lldp reinit 5
ops-as5712(config)#
```
The `no lldp reinit` command reverts the reinitialization delay value to its default of two seconds.
```
ops-as5712(config)# no lldp reinit
ops-as5712(config)#
```

4. Set the IP address to be used in the Management Address TLV.
The `lldp management-address` command specifies the IP address used in the management address LLDP type-length-value (TLV) triplets. If this command is not configured, the IP address assigned to the management interface will be used in the management address LLDP type-length-value (TLV) triplets.
```
ops-as5712(config)# lldp management-address 16.93.49.1
ops-as5712(config)#
```

5. Select LLDP TLV.
The `lldp select-tlv` command configures the type, length, and value (TLV) to send in LLDP packets. The `no lldp select-tlv` command removes the TLV configuration.
```
ops-as5712(config)# lldp select-tlv system-capabilities
ops-as5712(config)#
ops-as5712(config)# lldp select-tlv port-description
ops-as5712(config)#
```

6. Clearing the LLDP Counters.
The `lldp clear counters` command resets the LLDP traffic counters to zero.
```
ops-as5712(config)# lldp clear counters
ops-as5712(config)#
```

7. Clearing the LLDP neighbor information.
The `lldp clear neighbors` command clears neighbor information.
```
ops-as5712(config)# lldp clear neighbors
ops-as5712(config)#
```

### Verifying the configuration
##### Viewing LLDP Global Information
The `show lldp configuration` command displays LLDP configuration information configured above.
```
ops-as5712# show lldp configuration
LLDP Global Configuration:


LLDP Enabled :Yes
LLDP Transmit Interval :120
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
1            Yes                    Yes
10           Yes                    Yes
..................................
..................................
```

##### Viewing LLDP Neighbors
The `show lldp neighbor-info` command displays information about LLDP neighbors.
```
ops-as5712# show lldp neighbor-info

Total neighbor entries : 0
Total neighbor entries deleted : 0
Total neighbor entries dropped : 0
Total neighbor entries aged-out : 0

Local Port     Neighbor Chassis-ID      Neighbor Port-ID         TTL
1
2
3
.......................
.......................
```
The `show lldp neighbor-info <interface>` command shows LLDP neighbors for a particular interface.
```
ops-as5712# show lldp neighbor-info 1
Port                           : 1
Neighbor entries               : 0
Neighbor entries deleted       : 0
Neighbor entries dropped       : 0
Neighbor entries age-out       : 0
Neighbor Chassis-Name          :
Neighbor Chassis-Description   :
Neighbor Chassis-ID            :
Chassis Capabilities Available :
Chassis Capabilities Enabled   :
Neighbor Port-ID               :
TTL                            :
ops-as5712#
```

##### Viewing LLDP statistics
The `show lldp statistics` command displays the LLDP traffic information for the switch.
```
ops-as5712# show lldp statistics
LLDP Global statistics:

Total Packets transmitted : 35
Total Packets received : 0
Total Packet received and discarded : 0
Total TLVs unrecognized : 0
LLDP Port Statistics:
Port-ID   Tx-Packets     Rx-packets     Rx-discarded        TLVs-Unknown
1              34            0                 0                    0
10              0            0                 0                    0
................
................
```

The `show lldp statistics <interface>` command shows LLDP traffic information for a particular interface.

```
ops-as5712# show lldp statistics 1
LLDP statistics:

Port Name: 1
Packets transmitted :36
Packets received :0
Packets received and discarded :0
Packets received and unrecognized :0
ops-as5712#
```

##### Viewing LLDP TLVs
The `show lldp tlv` command displays the LLDP TLVs to be sent and received.
```
ops-as5712# show lld tlv

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
ops-as5712#
```

##### Viewing LLDP local device information
The `show lldp local-device` command displays the information advertised by the switch if the LLDP feature is enabled by the user. For example:
```
ops-as5712# show lldp local-device

Global Data
---------------

Chassis-id              : 48:0f:cf:af:50:c9
System Name            : switch
Systen Description     : OpenSwitch 0.1.0 (basil) Linux 3.9.11 #1 SMP Fri Sep 11 19:46:19 UTC 2015 x86_64
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

### Troubleshooting the configuration

#### Condition
- LLDP Neighbor information is not displayed even if neighbor is present.
- System description is not displayed in neighbor info.

#### Cause
- Interface may be down.
- Neighbor may not support LLDP or feature is not enabled.
- system description TLV may not be selected.

#### Remedy
- Make interface administratively up by using 'no shutdown' command. Refer physical interface command reference. Neighbor should support LLDP feature and enabled.
- Select system description TLV using 'lldp select-tlv' command.

## CLI
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](/documents/user/lldp_cli) for the CLI commands related to the LLDP feature.

## Related features
When configuring the switch for LLDP, it might also be necessary to configure [Physical Interface](/documents/user/interface_user_guide) so that interface to which neighbor is connected will act as expected.
