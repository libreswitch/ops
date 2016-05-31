# L3 Subinterfaces

## Contents
<!-- TOC depth:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [L3 Subinterfaces](#l3-subinterfaces)
	- [Contents](#contents)
	- [Overview](#overview)
	- [Subinterface restrictions](#subinterface-restrictions)
	- [How to use the feature](#how-to-use-the-feature)
		- [Setting up the basic configuration](#setting-up-the-basic-configuration)
		- [Verifying the configuration](#verifying-the-configuration)
		- [Troubleshooting the configuration](#troubleshooting-the-configuration)
			- [Condition](#condition)
			- [Cause](#cause)
			- [Remedy](#remedy)
        - [CLI ##](#cli-)
                - [L3 subinterface event logs](#l3-subinterface-event-logs)
        - [Related features ##](#related-features-)
	- [L3 subinterface event logs](#l3-subinterface-event-logs)
	- [L3 subinterface diagnostic dump](#l3-subinterface-diagnostic-dump)
	- [Related features](#related-features)
<!-- /TOC -->

## Overview
L3 Subinterfaces are used to support router-on-a-stick configurations. Using router-on-a-stick configurations, you can separate traffic on a L3 physical interface based on VLAN and also apply policies on the subinterfaces.

An example use of L3 subinterfaces in a data center deployment is shown in this diagram. An L3 interface of a TOR switch is connected to the trunk port of a switch. All the outgoing traffic from the L3 interface of the TOR switch is tagged with a VLAN ID.  This enables the switch to forward the traffic on different VLANs. This is configured by creating L3 subinterfaces on the TOR switch and configuring the routing tables to forward the outgoing traffic on one of these subinterfaces while applying a different VLAN tag on each subinterface.
```ditaa

             +----------------------------+                   +------------------------------+
             |                            |                   |                              |
             |                            |                   |                              |
             |                            |                   |                              |
             |   OpenSwitch              +-+ VLAN1(Subintf1) +-+         L2 Switch           |
             |                    L3 I/F |||<--------------->|||Trunk                        |
             |                           |||<--------------->|||Port                         |
             |                           +-+ VLAN2(Subintf2) +-+                             |
             |                            |                   |                              |
             |                            |                   |                              |
             |                            |                   |                              |
             +----------------------------+                   +------------------------------+
```
## Subinterface restrictions

A subinterface cannot be assigned an IP address already used by any interfaces on the switch.

## How to use the feature

###Setting up the basic configuration

 1. Configure an interface as L3.
 2. Run the `no shut` command on the parent interface.
 3. Create a subinterface on the L3 interface.
 4. Assign dot1q encapsulation.
 5. Assign an IP address.
 6. Run the `no shut` command.
 7. Enable the subinterface.

###Verifying the configuration

Display the configured subinterfaces.

###Troubleshooting the configuration
#### Condition
Unable to create a subinterface.
#### Cause
The interface may be configured as an L2.
#### Remedy
Configure the interface as an L3 using the `routing` command.
## CLI ##
Click [CLI-TBL](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the L3 subinterface feature.
## L3 subinterface event logs
All the events related to subinterface configuration are logged in event log.

Following are the logged events:
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

##L3 subinterface diagnostic dump
Number of subinterfaces created can be dumped using diagnostic dump.

## Related features
When configuring the switch for an L3 subinterface feature, it might also be necessary to configure an interface. Browse to (http://www.openswitch.net/documents/user/layer3_interface_cli#routing) so that the parent interface is a L3 interface.
