# OF-DPA OpenFlow Hybrid Switch Functionality Guide

## Contents
- [Overview](#overview)
- [OpenFlow Pipeline](#openflow-pipeline)
	- [Ingress Port Flow Table](#ingress-port-flow-table)
	- [VLAN Flow Table](#vlan-flow-table)
	- [Termination MAC Flow Table](#termination-mac-flow-table)
	- [Bridging Flow Table](#bridging-flow-table)
	- [Policy ACL Flow Table](#policy-acl-flow-table)
	- [L2 Interface Group Entry](#l2-interface-group-entry)
- [OpenFlow Hybrid Switch (OF-DPA) Configuration](#openflow-hybrid-switch-of-dpa-configuration)
	- [Creating the OF-DPA Bridge Table Entry](#creating-the-of-dpa-bridge-table-entry)
	- [Creating Port Table Entries Assigned to the OF-DPA Bridge](#creating-port-table-entries-assigned-to-the-of-dpa-bridge)
	- [Enabling Interfaces Associated with Ports](#enabling-interfaces-associated-with-ports)
	- [Configuring the OpenFlow Agent to Communicate with OpenFlow Controllers](#configuring-the-openflow-agent-to-communicate-with-openflow-controllers)
- [Using the OpenFlow Protocol to Configure Forwarding](#using-the-openflow-protocol-to-configure-forwarding)
- [Configuration Example](#configuration-example)

## Overview

An OpenFlow hybrid switch supports both OpenFlow operation and &quot;normal&quot; Ethernet switching operation. Various models for organizing OpenFlow hybrid switches are possible. The OF-DPA OpenFlow Hybrid Switch is one specific implementation of an OpenFlow hybrid switch. Other OpenFlow hybrid switch designs are possible. Such alternate designs may use different operational and configuration methods than the OF-DPA OpenFlow Hybrid Switch model.

The model employed in the OF-DPA OpenFlow Hybrid Switch is referred to as &quot;Ships in the Night&quot;. In this model, the physical switch is partitioned by assigning ports to either the OpenFlow switch or the traditional switch (bridge_normal). This is accomplished using an OVSDB Bridge table entry representing the OF-DPA OpenFlow pipeline. This bridge entry has the datapath_type column set to &quot;ofdpa&quot;. The OpenFlow related code in the switch driver plugin uses the datapath_type value to verify that OpenFlow configuration is installed on ports assigned to the OF-DPA bridge.

According to the OpenFlow Switch Specification, an OpenFlow hybrid switch should provide a classification mechanism that routes traffic to either the OpenFlow pipeline or the normal pipeline. The mechanism used in the OF-DPA OpenFlow Hybrid Switch is based on the port the packet enters the switch. A port is under the control of the OF-DPA pipeline when the port is associated with an entry in the bridge table whose datapath_type is &quot;ofdpa&quot;.

Once configured, the switch contains two independent forwarding pipelines. One pipeline is an OpenFlow pipeline that processes packets based on OpenFlow policy contained in the flow and group table entries installed by an OpenFlow Controller. The other pipeline is the traditional OPS forwarding pipeline. Packets entering physical ports are operated on by the forwarding pipeline corresponding to the bridge configured to contain the port. Following the &quot;Ships in the Night&quot; model, packets remain within a single pipeline and egress a physical port also assigned to the same pipeline.

In order to support the OF-DPA OpenFlow Hybrid Switch, the ASIC plugin implements the APIs required to support the OF-DPA pipeline model. One ASIC plugin that supports this is the OpenNSL plugin. Please see DESIGN.md in the ops-switchd-opennsl-plugin repository for more information. Other plugins may also support the OF-DPA OpenFlow Hybrid Switch feature in later releases.

## OpenFlow Pipeline

An OpenFlow switch's pipeline is described by its Table Type Pattern (TTP) as defined by the Open Networking Foundation (ONF). A TTP is an abstract switch model that describes specific switch forwarding behaviors that an OpenFlow controller can program via the OpenFlow-Switch protocol. A TTP represents the flow processing capabilities of an OpenFlow Switch.

The OF-DPA pipeline supports the configuration of L2 bridges programmed by OpenFlow controllers. The L2 bridges may be programmed to isolate virtual tenant networks on shared network infrastructure.

Packets are assigned to a virtual tenant by classifying packets based on port, or the combination of port and VLAN. This assignment is done by programming the VLAN table to set the Tunnel-ID metadata for the packet. This Tunnel-ID is used in place of a VLAN ID to look up the forwarding destination. The controller programs a Bridging table flow entry to match the MAC address and the Tunnel-ID.

The flow tables used by the OF-DPA pipeline are shown in the following diagram.

```ditaa

            +--------+     +--------+    +-------------+
            |        |     |        |    |             |
+------+    | Ingress|     | VLAN   |    | Termination |
| port +----> Port   +----->        +----> MAC         +--+
+------+    |        |     |        |    |             |  |
            |        |     |        |    |             |  |
            |        |     |        |    |             |  |
            +--------+     +--------+    +-------------+  |
                                                          |
         +------------------------------------------------+
         |  +----------+    +-----------+
         |  |          |    |           |
         |  | Bridging |    | Policy    |    +---------+    +------+
         +-->          +----> ACL       +----> actions +----> port |
            |          |    |           |    +---------+    +------+
            |          |    |           |
            |          |    |           |
            +----------+    +-----------+
```

Not all of the tables in this diagram are active in this version. Some are placeholders for future use. The inactive flow tables have built-in default flow entries for now and cannot be programmed with flow entries. OpenFlow flow entries contain a &quot;Goto-Table&quot; instruction with specific table ID number. Including tables that will be used in future implementations helps preserve backward compatibility with OpenFlow configurations used in the current TTP.

The flow table IDs for each table are:

Table Name | Table ID
-----------|---------
Ingress Port | 0
VLAN | 10
Termination MAC | 20
Bridging | 50
Policy ACL | 60


### Ingress Port Flow Table

This is a placeholder flow table. No flows can be added to this table by the controller.

### VLAN Flow Table

Flows in this table match on port or port and VLAN. The port must be assigned to the OF-DPA bridge for the flow to be added. The set-field action setting the tunnel-id metadata is applied to matching packets. The Goto-Table instruction must specify the Termination MAC flow table.

|name | IN_PORT | match_type | VLAN_VID | match_type | GOTO_TABLE | APPLY_ACTIONS
|:----|:--------|:-----------|:---------|:-----------|:-----------|:-------------
|Tunnel Assignment - VLAN Tagged     | &lt;ofport&gt; | exact | &lt;vid&gt;&#124;0x1000 | exact | Termination MAC | SET_FIELD TUNNEL_ID &lt;tunnel_id&gt;
|Tunnel Assignment - Untagged        | &lt;ofport&gt; | exact | 0                       | exact | Termination MAC | SET_FIELD TUNNEL_ID &lt;tunnel_id&gt;
|Tunnel Assignment - Priority Tagged | &lt;ofport&gt; | exact | 0x1000                  | exact | Termination MAC | SET_FIELD TUNNEL_ID &lt;tunnel_id&gt;
|Tunnel Assignment - All On Port     | &lt;ofport&gt; | exact |                         |       | Termination MAC | SET_FIELD TUNNEL_ID &lt;tunnel_id&gt;


### Termination MAC Flow Table

This is a placeholder flow table. No flows can be added to this table by the controller.

### Bridging Flow Table

Flows in this table match on tunnel-id and destination MAC. The flow entry must include a group action in the write-actions instruction. The Goto-Table instruction must specify the Policy ACL flow table.

|name | ETH_DST | match_type | TUNNEL_ID | match_type | GOTO_TABLE | WRITE_ACTIONS
|:----|:--------|:-----------|:----------|:-----------|:-----------|:-------------
|Unicast Overlay Bridging | &lt;mac&gt; | exact | &lt;tunnel_id&gt; | exact | Policy ACL | GROUP &lt;L2 Interface&gt;


### Policy ACL Flow Table

This is a placeholder flow table. No flows can be added to this table by the controller.

### L2 Interface Group Entry

The current TTP uses one type of group entry. This is called an L2 Interface group.

In OF-DPA, group ID is used to convey information about the group entry contents. Part of this information is the group entry type within OF-DPA. L2 Interface Group enries are assigned type == 0.

The group ID for this type of group entry is made up of the following fields:

bits: |[31:28]|[27:16]|[15:0]
------|-------|-------|------
content:|Type|VLAN ID|Port

As an example, the ID for an L2 Interface group entry that specifies VLAN ID 100 (0x64) and port 7 (0x0007) is 6553607 (0x00640007).

The action bucket for an L2 Interface Group entry specifies the port the packet is transmitted from. The port must be assigned to the OF-DPA bridge. The action set may also include the pop_vlan action which causes packets to be sent untagged.


## OF-DPA OpenFlow Hybrid Switch (OF-DPA) Configuration

The OF-DPA OpenFlow Hybrid Switch feature is configured by adding and updating entries in the OVSDB. The Bridge, Port, Interface, and Controller tables are used. There are multiple ways to change OVSDB content. These include the ovs-vsctl utility, the Swagger UI RESTful API, and from a remote system using the OVSDB protocol (RFC 7047).

The following sections show the steps to configure the switch for OpenFlow Hybrid Switch operation. The examples shown use invocations of ovs-vsctl from the OPS switch's console. More information about ovs-vsctl commands is available in the man pages for this utility. These configuration examples illustrate the OVSDB content required and can be used to determine how the same elements are configured using other methods.

### Creating the OF-DPA Bridge Table Entry

The OF-DPA pipeline is represented by an entry in the Bridge table. OPS automatically creates and configures an entry in the Bridge table named bridge_normal. A second Bridge table entry is created for the OF-DPA pipeline. The name of this bridge is not important, but the entry's datapath_type must be set to ofdpa. In the following examples, the bridge representing the OF-DPA pipeline is named bridge_ofdpa.

The following example adds a bridge named bridge_ofdpa and sets its datpath_type to ofdpa.
```
root@switch:~# ovs-vsctl add-br bridge_ofdpa
root@switch:~# ovs-vsctl set Bridge bridge_ofdpa datapath_type=ofdpa
```

### Creating Port Table Entries Assigned to the OF-DPA Bridge

As discussed above, the method used to determine which pipeline processes a packet is by the port the packet ingresses. In order for a packet to be handled by the OF-DPA pipeline, it must enter the switch via a port assigned to the OF-DPA bridge.

The following example assigns ports 1 and 2 to the OF-DPA bridge called bridge_ofdpa.
```
root@switch:~# ovs-vsctl add-port bridge_ofdpa 1
root@switch:~# ovs-vsctl add-port bridge_ofdpa 2
```

The ports are associated with entries in the Interface table. The Interface table entry with the same name as the port is bound to the port. After the port is added to the bridge, the interface is assigned an OpenFlow port number. The OpenFlow port number value, used in all OpenFlow configuration to identify the port, is recorded in the ofport column of the Interface table entry.

In the example above, the resulting OVSDB content is:
```
root@switch:~# ovsdb-client dump Interface _uuid name ofport
Interface table
_uuid                                name          ofport
------------------------------------ ------------- ------
7553f083-eace-4ea0-8618-e3abb39d4764 "1"           1
6b5fc1a1-0b8a-49dd-95f0-21aa8b9b8b56 "10"          []
c5d786b8-c41a-4e0b-b52c-b6342e39a297 "11"          []
db9ea0c3-abab-4162-9aab-d4ebd60b0ee8 "12"          []
7f2509f0-dee5-4d32-8f70-4cc5b6d4290f "13"          []
e194c580-de9a-453a-ab35-0a348a861965 "14"          []
6d4d8cf7-3b8d-485f-959c-e956fd699e10 "15"          []
1462895e-6e2d-4b76-82d5-0895c60b29fe "16"          []
aafb2a54-2bf8-4eb9-993b-fb8973d5a427 "17"          []
7dc31b97-66dc-4b13-9994-267c7d1ab663 "18"          []
b8feb9aa-b65f-4cb0-bc81-79b8d87adb9b "19"          []
7b7cace3-4ce2-4404-8122-0b0471e640df "2"           2
...
```

_NOTE:_ The initial implementation assigns OpenFlow port numbers based on the order the ports are added to the bridge. In the case above, port 1 is first port to be added to the OpenFlow Bridge so it is assigned ofport == 1. The same follows for port 2 getting ofport == 2. However, since the ofport value assignment is automatically generated, the ofport value may not correspond to the port name. That is, continuing the example, if port 14 is added to the OpenFlow bridge next, it will be assigned ofport == 3. This creates a dependency between the configuration order of the OVSDB content and the ofport values assigned. This is acceptable for experimentation with the initial OpenFlow Hybrid Switch feature, but an enhancement is planned to make the ofport assignment deterministic. After that change, the ofport value will be the same as the port name (that is, the Interface table entry associated with the Port table entry named &quot;14&quot; will be assigned ofport == 14).

### Enabling Interfaces Associated with Ports

Interfaces associated with ports added to the OF-DPA bridge need to be administratively enabled to transition to link up. This is done by setting the admin key in the user_config column of the Interface table entries.

For example:
```
root@switch:~# ovs-vsctl add Interface 1 user_config admin=up
root@switch:~# ovs-vsctl add Interface 2 user_config admin=up
```

### Configuring the OpenFlow Agent to Communicate with OpenFlow Controllers

Communication with an OpenFlow controller is configured by updating the Controller table. OpenFlow messages are sent to the switch to configure the OpenFlow pipeline. There are many options regarding how the agent and controller communicate. For experimentation, it is possible to use the ovs-ofctl utility on the switch's console to send OpenFlow messages to the agent on the same switch. However, in most cases, the OpenFlow controller is another system.

Example configuring the agent to accept an OpenFlow connection from a controller with a specific IP address and the default port over TCP:
```
root@switch:~# ovs-vsctl set-controller bridge_ofdpa tcp:[OpenFlow Controller IP]
```
Example configuring the agent to accept an OpenFlow connection from a controller at any IP address and the default port over TCP:
```
root@switch:~# ovs-vsctl set-controller bridge_ofdpa ptcp:
```

## Using the OpenFlow Protocol to Configure Forwarding

Once the OpenFlow Hybrid switch is configured, various OpenFlow controllers can be used to program the OpenFlow pipeline. These include ODL, Ryu, dpctl, ovs-ofctl, and many others. Examples here use the ovs-ofctl utility on the local switch.

The following example sets up the OF-DPA pipeline to forward packets matching the flow configuration to be switched from port 1 to port 2. The processing steps in the OF-DPA pipeline are:

 1. Assign packets tagged with VLAN 100 arriving on port 1 to to tunnel_id 343
 1. Packets assigned to tunnel_id 343 with a destination MAC equal to 00:00:00:00:00:11 are handled using L2 Interface entry 0x00640002
 1. The L2 Interface entry specifies the packets are sent out port 2 tagged
```
root@switch:~# ovs-ofctl -O OpenFlow13 add-group bridge_ofdpa group_id=0x00640002,type=all,bucket=output:2

root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=10,in_port=1,dl_vlan=100,actions=set_field:343-\>tunnel_id,goto_table:20

root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=50,tunnel_id=343,dl_dst=00:00:00:00:00:11,actions=group:0x00640002,goto_table:60
```

## Configuration Example

This section shows a simple use case and how it is configured using OpenFlow. The diagram below illustrates the network used for this example.

```ditaa
+----------+                                                            +----------+
|          |                                                            |          |
| Server A +----------+                                          +------+ Server C |
|          |          |1 +-----------+            +-----------+ 1|      |          |
+----------+          +--+           |            |           +--+      +----------+
MAC:                     |           | 3        3 |           |                 MAC:
00:00:00:00:00:11        |  Switch 1 +------------+  Switch 2 |    00:00:00:00:00:33
                       2 |           |            |           | 2
+----------+          +--+           |            |           +--+      +----------+
|          |          |  +-----------+            +-----------+  |      |          |
| Server B +----------+                                          +------+ Server D |
|          |                                                            |          |
+----------+                                                            +----------+
MAC:                                                                            MAC:
00:00:00:00:00:22                                                  00:00:00:00:00:44
```

In this use case, packets from the servers are sent tagged. Servers A and C are able to communicate and servers B and D are able to communicate. On the link between switches 1 and 2, packets are sent with VLAN tags. Packets sent between server A and server C are sent on this link using VLAN 100 and packets between server B and D are sent using VLAN 200. This results in the traffic between the one pair of servers being isolated from the other pair.

Following a packet through the OF-DPA pipeline from server A to server C the packet is presented to each flow table in order.

First, in switch 1, the VLAN flow table matches on the packet's incoming ofport and whether it arrived tagged. In this case the flow matches packets entering ofport == 1 that are tagged with VLAN ID 100. The action for the matching flow entry is to perform a SET_FIELD TUNNEL_ID action setting the packet's TUNNEL_ID metadata to 343. The goto instruction links to the Termination MAC flow table which is inactive in this version. The Termination MAC table has a default action of goto Bridging.

At the Bridging flow table, the flow entries match on the packet's destination Ethernet MAC address and the TUNNEL_ID metadata assigned in the VLAN flow table. Packets from server A to server C have a destination MAC address of 00:00:00:00:00:33 and TUNNEL_ID of 343. Matching packets are handled by the L2 Interface group entry in the flow. In this case the L2 Interface group entry's ID is 0x00640003.

The L2 Interface group entry (0x00640003) specifies that packets using the group entry are sent out port 3 tagged with the VLAN tag equal to 100.

On switch 2, the VLAN flow table matches the packet arriving on port 3 with a VLAN tag equal to 100. The actions for this flow entry are to SET_FIELD TUNNEL_ID to 343. In the Bridging table, packets with destination MAC of 00:00:00:00:00:33 and TUNNEL_ID of 343 are handled by the L2 Interface group entry 0x00640001.

The L2 Interface group entry (0x00640001) specifies that packets using the group entry are sent out port 1 with a VLAN tag.

The other paths between servers follow a similar path with the appropriate TUNNEL_ID and VLAN ID values used.

The following shows the commands to configure the OF-DPA pipeline using the ovs-vsctl and ovs-ofctl utilities.

On both switches:
```
root@switch:~# ovs-vsctl add-br bridge_ofdpa
root@switch:~# ovs-vsctl set Bridge bridge_ofdpa datapath_type=ofdpa
root@switch:~# ovs-vsctl add-port bridge_ofdpa 1
root@switch:~# ovs-vsctl add-port bridge_ofdpa 2
root@switch:~# ovs-vsctl add-port bridge_ofdpa 3
root@switch:~# ovs-vsctl add Interface 1 user_config admin=up
root@switch:~# ovs-vsctl add Interface 2 user_config admin=up
root@switch:~# ovs-vsctl add Interface 3 user_config admin=up


root@switch:~# ovs-ofctl -O OpenFlow13 add-group bridge_ofdpa group_id=0x00640001,type=all,bucket=output:1
root@switch:~# ovs-ofctl -O OpenFlow13 add-group bridge_ofdpa group_id=0x00c80002,type=all,bucket=output:2
root@switch:~# ovs-ofctl -O OpenFlow13 add-group bridge_ofdpa group_id=0x00640003,type=all,bucket=output:3
root@switch:~# ovs-ofctl -O OpenFlow13 add-group bridge_ofdpa group_id=0x00c80003,type=all,bucket=output:3

root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=10,in_port=1,dl_vlan=100,actions=set_field:343-\>tunnel_id,goto_table:20
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=10,in_port=3,dl_vlan=100,actions=set_field:343-\>tunnel_id,goto_table:20

root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=10,in_port=2,dl_vlan=200,actions=set_field:632-\>tunnel_id,goto_table:20
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=10,in_port=3,dl_vlan=200,actions=set_field:632-\>tunnel_id,goto_table:20
```
On Switch 1:
```
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=50,tunnel_id=343,dl_dst=00:00:00:00:00:11,actions=group:0x00640001,goto_table:60
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=50,tunnel_id=343,dl_dst=00:00:00:00:00:33,actions=group:0x00640003,goto_table:60
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=50,tunnel_id=632,dl_dst=00:00:00:00:00:22,actions=group:0x00c80002,goto_table:60
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=50,tunnel_id=632,dl_dst=00:00:00:00:00:44,actions=group:0x00c80003,goto_table:60
```

On Switch 2:
```
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=50,tunnel_id=343,dl_dst=00:00:00:00:00:33,actions=group:0x00640001,goto_table:60
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=50,tunnel_id=343,dl_dst=00:00:00:00:00:11,actions=group:0x00640003,goto_table:60
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=50,tunnel_id=632,dl_dst=00:00:00:00:00:44,actions=group:0x00c80002,goto_table:60
root@switch:~# ovs-ofctl -O OpenFlow13 add-flow bridge_ofdpa table=50,tunnel_id=632,dl_dst=00:00:00:00:00:22,actions=group:0x00c80003,goto_table:60
```
