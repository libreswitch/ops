# MSTP feature
## Contents
- [Overview](#overview)
- [MSTP Structure](#mstp-structure)
    - [Types of multiple spanning tree instances](#types-of-multiple-spanning-tree-instances)
        - [Internal spanning tree instance (IST Instance)](#ist-instance)
        - [Multiple spanning tree instance (MSTI)](#mst-instance)
- [How MSTP Operates](#how-mstp-operates)
- [Terminology](#terminology)
    - [Common and internal spanning tree (CIST)](#t_cist)
    - [Internal spanning tree (IST)](#t_ist)
    - [MSTP (Multiple Spanning Tree Protocol)](#t_mstp)
    - [MSTP BPDU (Bridge Protocol Data Unit)](#t_bpdu)
    - [MSTP bridge](#t_bridge)
    - [MSTP region](#t_region)
- [Operating rules](#operating-rules)
- [Usage scenarios](#usage-scenarios)
    - [Setting up scenario 1 basic configuration](#setting-up-scenario-1-basic-configuration)
        - [Physical Topology](#physical-topology)
        - [Logical Topology](#logical-topology)
    - [Configure MSTP global parameters](#configure-mstp-global-parameters)
    - [Configure MSTP optional parameters](#configure-mstp-optional-parameters)
    - [Verifying scenario 1 configuration](#verifying-scenario-1-configuration)
    - [Troubleshooting](#troubleshooting)
        - [Additional tips for troubleshooting](#additional-tips-for-troubleshooting)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The MSTP feature is used for preventing loops in a network. Without a spanning tree, having more than one active path between a pair of nodes causes loops in the network, which can result in duplication of messages and lead to a “broadcast storm” that might bring down the network.

- The Multliple Spanning Tree Protocol (MSTP) (802.1s) ensures that only one active path exists between any two nodes in a spanning tree instance.
- A spanning tree instance comprises a unique set of VLANs, and belongs to a specific spanning tree region.
- A region can comprise multiple spanning tree instances (each with a different set of VLANs), and allows one active path among regions in a network.
- Applying VLAN tagging to the ports in a multiple-instance spanning tree network enables blocking of redundant links in one instance while allowing forwarding over the same links for non-redundant use by another instance.

This feature currently works on a physical interface and LAGs.

## MSTP Structure
MSTP maps active, separate paths through separate spanning tree instances and between MST regions. Each MST region comprises one or more MSTP switches.

- The common and internal spanning tree (CIST) identifies the regions in a network and administers the CIST root bridge for the network, the root bridge for each region, and the root bridge for each spanning tree instance in each region.
- The CIST root administers the connectivity among the MST regions in a bridged network.
- An MST region comprises the VLANs configured on physically connected MSTP switches. All switches in a given region must be configured with the same VLANs and Multiple Spanning Tree Instances (MSTIs).
- The internal spanning tree (IST) administers the topology within a given MST region. When a switch is configured for MSTP operation, the switch automatically includes all of the static VLANs configured on the switch in a single, active spanning tree topology (instance) within the IST. This is termed the “IST instance”. Any VLANs you subsequently configure on the switch are added to this IST instance. To create separate forwarding paths within a region, group specific VLANs into different multiple spanning tree instances (MSTIs).

#### Types of multiple spanning tree instances
A network can have several MSTP regions. An MSTP region has multiple spanning tree instances. Each instance defines a single forwarding topology for an exclusive set of VLANs.
<div id='ist-instance'/>
##### Internal spanning tree instance (IST instance)
This is the default spanning tree instance in any MST region. It provides the root switch for the region and comprises all VLANs configured on the switches in the region that are not specifically assigned to multiple spanning tree instances (MSTIs, described below). All VLANs in the IST instance of a region are part of the same, single spanning tree topology, which allows only one forwarding path between any two nodes belonging to any of the VLANs included in the IST instance. All switches in the region must belong to the set of VLANs that comprise the IST instance.
<div id='mst-instance'/>
##### Multiple spanning tree instance (MSTI)
This type of configurable spanning tree instance comprises all static VLANs specifically assign to it, and must include at least one VLAN. The VLAN(s) assigned to an MSTI must initially exist in the IST instance of the same MST region. When a static VLAN is assigned to an MSTI, the switch removes the VLAN from the IST instance. (Thus, a VLAN is assigned to only one MSTI in a given region.) All VLANs in an MSTI operate as part of the same single spanning tree topology.

## How MSTP Operates
- In the factory default configuration, spanning tree operation is off. Also, the switch retains its currently configured spanning tree parameter settings when disabled. Thus, if spanning tree is disabled, then later re-enabled, the parameter settings are the same as before spanning tree was disabled.
- All MSTP switches in a given region must be configured with the same VLANs. Also, each MSTP switch within the same region must have the same VLAN-to-instance assignments. (A VLAN can belong to only one instance within any region.) Within a region:
    - All of the VLANs belonging to a given instance compose a single, active spanning tree topology for that instance.
    - Each instance operates independently of other regions.
    - Between regions there is a single, active spanning tree topology.

## Terminology
<div id='t_cist'/>
### Common and internal spanning tree (CIST)
Comprises all LANs and MSTP regions in a network. The CIST automatically determines the MST regions in a network and defines the root bridge (switch) and designated port for each region. The CIST includes the Common Spanning Tree (CST), the Internal Spanning Tree (IST) within each region, and any multiple spanning-tree instances (MSTIs) in a region.

<div id='t_ist'/>
### Internal spanning tree (IST)
Comprises all VLANs within a region that are not assigned to a MSTI configured within the region. All MSTP switches in a region should belong to the IST. In a given region “X”, the IST root switch is the regional root switch and provides information on region “X” to other regions.

<div id='t_mstp'/>
#### MSTP (Multiple Spanning Tree Protocol)
A network supporting MSTP allows multiple spanning tree instances within configured regions, and a single spanning tree among regions.

<div id='t_bpdu'/>
### MSTP BPDU (Bridge Protocol Data Unit)
BPDUs carry region-specific information, such as the region identifier (region name and revision number). If a switch receives an MSTP BPDU with a region identifier that differs from its own, then the port on which that BPDU was received is on the boundary of the region in which the switch resides.

<div id='t_bridge'/>
### MSTP bridge
In this manual, an MSTP bridge is a switch (or another 802.1s compatible device) configured for MSTP operation.

<div id='t_region'/>
### MST region
A MST region forms a multiple spanning tree domain and is a component of a single spanning tree domain within a network. For switches internal to the MST region:
- All switches have identical MST configuration identifiers (region name and revision number).
- All switches have identical VLAN assignments to the region’s IST and (optional) MST instances.
- One switch functions as the designated bridge (IST root) for the region.
- No switch has a point-to-point connection to a bridging device that cannot process MSTP BPDUs.

##Operating rules
- All switches in a region must be configured with the same set of VLANs, as well as the same MST configuration name and MST configuration number.
- Within a region, a VLAN can be allocated to either a single MSTI or to the region’s IST instance.
- All switches in a region must have the same VLAN ID to MST instance and VLAN ID to IST instance assignments.
- There is one root MST switch per configured MST instance.
- Within any region, the root switch for the IST instance is also the root switch for the region. Because boundary ports provide the VLAN connectivity between regions, all boundary ports on a region's root switch should be configured as members of all static VLANs defined in the region.
- There is one root switch for the CIST. Note that the per-port hello-time parameter assignments on the CIST root switch propagate to the ports on downstream switches in the network, and override the hello-time configured on the downstream switch ports.
- Where multiple MST regions exist in a network, there is only one active, physical communication path between any two regions, or between an MST region and an STP or RSTP switch. MSTP blocks any other physical paths as long as the currently active path remains in service.
- Within an MSTI, there is one spanning tree (one physical, communication path) between any two nodes. That is, within an MSTI, there is one instance of spanning tree, regardless of how many VLANs belong to the MSTI. Within an IST instance, there is also one spanning tree across all VLANs belonging to the IST instance.
- An MSTI comprises a unique set of VLANs and forms a single spanning tree instance within the region to which it belongs.
- An MSTI should have at least one VLAN configured to it.
- Removing an MSTI through CLI or REST moves the configured VLANs from MSTI to IST.
- Communication between MST regions uses a single spanning tree.
- If a port on a switch configured for MSTP receives a legacy (STP/802.1D or RSTP/802.1w) BPDU, it automatically operates as a legacy port. In this case, the MSTP switch interoperates with the connected STP or RSTP switch as a separate MST region.
- Within an MST region, there is one logical forwarding topology per instance, and each instance comprises a unique set of VLANs. Where multiple paths exist between a pair of nodes using VLANs belonging to the same instance, all but one of those paths is blocked for that instance. However, if there are different paths in different instances, all such paths are available for traffic. Separate forwarding paths exist through separate spanning tree instances.
- A port can have different states (forwarding or blocking) for different instances (which represent different forwarding paths).

## Usage scenarios
### Setting up scenario 1 basic configuration
Create a three switch topology as specified below.
#### Physical Topology
 ```
+-----------------------------------------------------------------------------+
|    Region "A": Physical Topology                                            |
|                            +----------------+                               |
|                Link-2      +      SW_1      +      Link-1                   |
|          +-----------------+                +----------------+              |
|          |                 +                +                |              |
|          |                 +----------------+                |              |
|          +                                                   +              |
|   +------+---------+                                +--------+--------+     |
|   |                |            lINK-3              +                 |     |
|   |     SW_3       +--------------------------------+      SW_2       |     |
|   |                |                                +                 |     |
|   +----------------+                                +-----------------+     |
|                                                                             |
+-----------------------------------------------------------------------------+
```

Configure instance 1 and 2 as specified below:

    VLANS      | Instance 1 | Instance 2
    -----    | ---------- | ---------
    10,11,12 | Yes           | No
    20,21,22 | No           | Yes

The logical and physical topologies resulting from these VLAN/instance groupings result in blocking on different links for different VLANs:
#### Logical Topology
   ```
+-----------------------------------------------------------------------------+
|  Logical topology for Instance-1                                            |
|                           +--------------------+                            |
|              Link-2       |       SW-1         |   Link-1                   |
|         +-----------------+ Root for Instance 1+---------------+            |
|         |                 |  VLANs = 10,11,12  |               |            |
|         |                 +--------------------+               |            |
|         |                                                      |            |
|         |                                                      |            |
|  +------+----------+                                  +--------+---------+  |
|  |     SW-2        |           Link-3(Blocked)        |     SW-3         |  |
|  |  Instance-1     +----------------------------------+  Instance-1      |  |
|  | VLANs = 10,11,12|                                  | VLANS = 10,11,12 |  |
|  +-----------------+                                  +------------------+  |
|                                                                             |
+-----------------------------------------------------------------------------+
```
 ```
+-----------------------------------------------------------------------------+
|  Logical topology for Instance-2                                            |
|                           +--------------------+                            |
|              Link-2       |       SW-1         |   Link-1(Blocked)          |
|         +-----------------+ Root for Instance 2+---------------+            |
|         |                 |  VLANs = 20,21,22  |               |            |
|         |                 +--------------------+               |            |
|         |                                                      |            |
|         |                                                      |            |
|  +------+----------+                                  +--------+---------+  |
|  |     SW-2        |           Link-3                 |     SW-3         |  |
|  |  Instance-2     +----------------------------------+  Instance-2      |  |
|  | VLANs = 20,21,22|                                  | VLANS = 20,21,22 |  |
|  +-----------------+                                  +------------------+  |
|                                                                             |
+-----------------------------------------------------------------------------+
```

MSTP uses VLANs to create multiple spanning trees in a network, which significantly improves network resource utilization while maintaining a loop-free environment. Thus, where a port belongs to multiple VLANs, it may be dynamically blocked in one spanning tree instance, but forwarding in another instance. This achieves load-balancing across the network while keeping the switch’s CPU load at a moderate level (by aggregating multiple VLANs in a single spanning tree instance).

### Configure MSTP global parameters
Configure the same region name and revision number in all three switches:
```
spanning-tree config-name mst
spanning-tree config-revision 1
spanning-tree
```
Create two MSTP instances and map the VLANS as shown below:
```
spanning-tree instance 1 vlan 10
spanning-tree instance 1 vlan 11
spanning-tree instance 1 vlan 12

spanning-tree instance 2 vlan 20
spanning-tree instance 2 vlan 21
spanning-tree instance 2 vlan 22
```

### Configure MSTP optional parameters

        spanning-tree max-hops 10
        spanning-tree hello-time 8
        spanning-tree forward-delay 8

### Verifying scenario 1 configuration

MSTP details on Root switch:

```
    switch# sh spanning-tree mst detail
    #### MST0
    Vlans mapped:  1-9,11-4095
    Bridge         Address:70:72:cf:03:d3:e9    priority:32768
    Root
    Regional Root
    Operational    Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6
    Configured     Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6

    Port           Role           State      Cost       Priority   Type
    -------------- -------------- ---------- ---------- ---------- ----------
    1              Designated     Forwarding 0          128        point_to_point
    2              Designated     Forwarding 0          128        point_to_point

    #### MST1
    Vlans mapped:  10
    Bridge         Address:70:72:cf:03:d3:e9    Priority:32768
    Root           Address:70:72:cf:03:d3:e9    Priority:32769
                   Port:, Cost:20000, Rem Hops:0

    Port           Role           State      Cost    Priority   Type
    -------------- -------------- ---------- ------- ---------- ----------
    1              Designated     Forwarding 0       128        point_to_point
    2              Designated     Forwarding 0       128        point_to_point

    Port 1
    Designated root address            : 70:72:cf:03:d3:e9
    Designated regional root address   : 70:72:cf:03:d3:e9
    Designated bridge address          : 32768.0.70:72:cf:03:d3:e9
    Timers:    Message expires in 1 sec, Forward delay expiry:18, Forward transitions:18
    Bpdus sent 183, received 4

    Port 2
    Designated root address            : 70:72:cf:03:d3:e9
    Designated regional root address   : 70:72:cf:03:d3:e9
    Designated bridge address          : 32768.0.70:72:cf:03:d3:e9
    Timers:    Message expires in 1 sec, Forward delay expiry:18, Forward transitions:18
    Bpdus sent 183, received 4
```
MSTP details on Non-Root switch:
```
    switch# sh spanning-tree mst detail
    #### MST0
    Vlans mapped:  1-9,11-4095
    Bridge         Address:70:72:cf:e7:25:b1    priority:32768
    Operational    Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6
    Configured     Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6

    Port           Role           State      Cost       Priority   Type
    -------------- -------------- ---------- ---------- ---------- ----------
    1              Root           Forwarding 2000000    128        point_to_point
    2              Alternate      Blocking   4000000    128        point_to_point


    #### MST1
    Vlans mapped:  10
    Bridge         Address:70:72:cf:e7:25:b1    Priority:32768
    Root           Address:70:72:cf:3b:ea:a4    Priority:32769
                   Port:1, Cost:4000000, Rem Hops:20

    Port           Role           State      Cost    Priority   Type
    -------------- -------------- ---------- ------- ---------- ----------
    1              Root           Forwarding 2000000 128        point_to_point
    2              Alternate      Blocking   2000000 128        point_to_point

    Port 1
    Designated root address            : 70:72:cf:3b:ea:a4
    Designated regional root address   : 70:72:cf:e7:25:b1
    Designated bridge address          : 32768.0.70:72:cf:e7:25:b1
    Timers:    Message expires in 0 sec, Forward delay expiry:0, Forward transitions:0
    Bpdus sent 4, received 1853

    Port 2
    Designated root address            : 70:72:cf:3b:ea:a4
    Designated regional root address   : 70:72:cf:e7:25:b1
    Designated bridge address          : 32768.0.70:72:cf:e7:25:b1
    Timers:    Message expires in 0 sec, Forward delay expiry:0, Forward transitions:0
    Bpdus sent 5, received 1854

    switch#
```

### Troubleshooting
Duplicate packets on a VLAN, or packets not arriving on a LAN at all.
   - The allocation of VLANs to MSTIs may not be identical among all switches in a region.
   - Check the current instance to VLAN mapping by `show spanning-tree mst-config`:
       ```
        switch# sh spanning-tree mst-config
      MST configuration information
         MST config ID        : mst2
         MST config revision  : 2
         MST config digest    : 870555C957F1B44530B7D56FD4716ADF
         Number of instances  : 1

      Instance ID     Member VLANs
      --------------- ----------------------------------
      1               10,11,12
      2               20,21,22
      switch#
      ```
A switch intended to operate within a region does not receive traffic from other switches in the region.
   - An MSTP switch intended for a particular region may not have the same configuration name or region revision number as the other switches intended for the same region.
   - The set of VLANs configured on the switch may not match the set of VLANs configured on other switches in the intended region.
   - Check the config-name and revision using the `show running-config spanning-tree` command or the `show spanning-tree mst-config` command.

MSTP port roles are always blocked.
   - Check that the admin status for the corresponding ports are up using the `show interface` command:
    ```
    switch# show interface 1

    Interface 1 is up
     Admin state is up
     Hardware: Ethernet, MAC Address: 70:72:cf:3b:ea:a4
     MTU 1500
     Full-duplex
     qos trust none
     qos queue-profile default
     qos schedule-profile default
     Speed 1000 Mb/s
     Auto-Negotiation is turned on
     Input flow-control is off, output flow-control is off
     RX
             5037 input packets         548385 bytes
                0 input error                0 dropped
                0 CRC/FCS
     TX
           135373 output packets      17976260 bytes
                0 input error                0 dropped
                0 collision

    switch#
    ```

The network is not stable, convergence restarts after every few seconds.
   - Check the BPDU statistics using the `show spanning-tree detail` command.
   - Root bridge should not receive any non-root bridge BPDU after convergence is completed.
   - The `Number of topology changes` value should not increase rapidly if no network changes are happening.
   - On non-root bridges BPDU received should not increase, and on the other way BPDU sent count should not increase.
    ```
        switch# sh spanning-tree detail
        MST0
          Spanning tree status: Enabled
          Root ID    Priority   : 32768
                     MAC-Address: 70:72:cf:3b:ea:a4
                     This bridge is the root
                     Hello time(in seconds):2  Max Age(in seconds):20  Forward Delay(in seconds):15

          Bridge ID  Priority  : 32768
                     MAC-Address: 70:72:cf:3b:ea:a4
                     Hello time(in seconds):2  Max Age(in seconds):20  Forward Delay(in seconds):15

        Port         Role           State      Cost    Priority   Type
        ------------ -------------- ---------- ------- ---------- ----------
        1            Designated     Forwarding 0       128        point_to_point
        2            Designated     Forwarding 0       128        point_to_point

        Topology change flag          : True
        Number of topology changes    : 2
        Last topology change occurred : 247012 seconds ago
        Timers:    Hello expiry  1 , Forward delay expiry 0

        Port 1
        Designated root has priority               :32768 Address: 70:72:cf:3b:ea:a4
        Designated bridge has priority             :32768 Address: 70:72:cf:3b:ea:a4
        Designated port                            :1
        Number of transitions to forwarding state  : 0
        Bpdus sent 123508, received 2

        Port 2
        Designated root has priority               :32768 Address: 70:72:cf:3b:ea:a4
        Designated bridge has priority             :32768 Address: 70:72:cf:3b:ea:a4
        Designated port                            :2
        Number of transitions to forwarding state  : 0
        Bpdus sent 123508, received 2
    ```

   - Root switch should not get multiple topology change events from other non-root bridges. Check this using the `show events category mstp` command.
```
        2016-06-04:12:06:51.683147|ops-stpd|23012|LOG_INFO|CIST - Topology Change generated on port 1 going in to forwarding
        2016-06-04:12:06:51.686827|ops-stpd|23012|LOG_INFO|CIST - Topology Change generated on port 2 going in to forwarding
        2016-06-04:12:06:51.689134|ops-stpd|23001|LOG_INFO|MSTP Enabled
        2016-06-04:12:06:51.700332|ops-stpd|23011|LOG_INFO|Topology Change received on port 1 for CIST from source: 48:0f:cf:af:d3:93
        2016-06-04:12:06:51.705785|ops-stpd|23011|LOG_INFO|Topology Change received on port 2 for CIST from source: 48:0f:cf:af:65:b9
        2016-06-04:12:06:52.987110|ops-stpd|23011|LOG_INFO|Topology Change received on port 2 for CIST from source: 48:0f:cf:af:65:b9
        2016-06-04:12:09:07.348952|ops-stpd|23011|LOG_INFO|Topology Change received on port 2 for CIST from source: 48:0f:cf:af:65:b9
        2016-06-04:12:09:08.986934|ops-stpd|23011|LOG_INFO|Topology Change received on port 2 for CIST from source: 48:0f:cf:af:65:b9
        2016-06-04:12:09:11.707898|ops-stpd|23011|LOG_INFO|Topology Change received on port 2 for CIST from source: 48:0f:cf:af:65:b9
        2016-06-04:12:09:11.725218|ops-stpd|23011|LOG_INFO|Topology Change received on port 1 for CIST from source: 48:0f:cf:af:d3:93
        2016-06-04:12:09:12.986157|ops-stpd|23011|LOG_INFO|Topology Change received on port 2 for CIST from source: 48:0f:cf:af:65:b9
        2016-06-04:12:09:13.641048|ops-stpd|23011|LOG_INFO|Topology Change received on port 1 for CIST from source: 48:0f:cf:af:d3:93
        2016-06-04:12:09:17.044583|ops-stpd|23011|LOG_INFO|Topology Change received on port 1 for CIST from source: 48:0f:cf:af:d3:93
        2016-06-04:12:09:17.474762|ops-stpd|23011|LOG_INFO|Topology Change received on port 2 for CIST from source: 48:0f:cf:af:65:b9
        2016-06-04:12:09:18.986615|ops-stpd|23011|LOG_INFO|Topology Change received on port 2 for CIST from source: 48:0f:cf:af:65:b9
        2016-06-04:12:09:23.577870|ops-stpd|23012|LOG_INFO|CIST - Topology Change generated on port 1 going in to forwarding
        2016-06-04:12:09:23.578935|ops-stpd|23012|LOG_INFO|MSTI 1 - Topology Change generated on port 1 going in to forwarding
        2016-06-04:12:09:23.582833|ops-stpd|23012|LOG_INFO|CIST - Topology Change generated on port 2 going in to forwarding
        2016-06-04:12:09:23.583842|ops-stpd|23012|LOG_INFO|MSTI 1 - Topology Change generated on port 2 going in to forwarding
        2016-06-04:12:09:23.586780|ops-stpd|23001|LOG_INFO|MSTP Enabled
```

#### Additional tips for troubleshooting
Data can be retrieved from the MSTP daemon by running the `diag-dump mstp basic` command.

```
   switch# diag-dump mstp basic
   =========================================================================
   [Start] Feature mstp Time : Mon Jun 20 12:36:05 2016

   =========================================================================
   -------------------------------------------------------------------------
   [Start] Daemon ops-stpd
   -------------------------------------------------------------------------
   MSTP CIST Config OVSDB info:
   MSTP VLANs:
   MSTP CIST Priority 8
   MSTP CIST Hello Time 2
   MSTP CIST Forward Delay 15
   MSTP CIST Max Age 20
   MSTP CIST Max Hop Count 20
   MSTP CIST Tx Hold Count 6
   mstpEnabled       : Yes
   valid             : Yes
   cistRootPortID    : port#=0, priority=0
   CistBridgeTimes   : {fwdDelay=15 maxAge=20 messageAge=0 hops=20}
   cistRootTimes     : {fwdDelay=15 maxAge=20 messageAge=0 hops=20}
   cistRootHelloTime : 0
   BridgeIdentifier  : {mac=70:72:cf:18:3e:0c priority=32768 sysID=0}
   CistBridgePriority:
           rootID      {mac=70:72:cf:18:3e:0c priority=32768 sysID=0}
           extRootPathCost=0
           rgnRootID   {mac=70:72:cf:18:3e:0c priority=32768 sysID=0}
           intRootPathCost=0
           dsnBridgeID {mac=70:72:cf:18:3e:0c priority=32768 sysID=0}
           dsnPortID=(0;0)
   cistRootPriority  :
           rootID      {mac=70:72:cf:18:3e:0c priority=32768 sysID=0}
           extRootPathCost=0
           rgnRootID   {mac=70:72:cf:18:3e:0c priority=32768 sysID=0}
           intRootPathCost=0
           dsnBridgeID {mac=70:72:cf:18:3e:0c priority=32768 sysID=0}
           dsnPortID=(0;0)
   SM states         : PRS=ROLE_SELECTION
   TC Trap Control   : false
   MSTP CIST Lport : 2
   MSTP CIST PORT Priority : 8
   MSTP CIST PORT Admin Path Cost : 0
   MSTP CIST PORT Admin Edge port : 0
   MSTP CIST PORT BPDUS RX Enable : 0
   MSTP CIST PORT BPDUS TX Enable : 0
   MSTP CIST PORT Restricted Port Role : 0
   MSTP CIST PORT Restricted Port Tcn : 0
   MSTP CIST PORT BPDU Guard : 0
   MSTP CIST PORT LOOP Guard : 0
   MSTP CIST PORT ROOT Guard : 0
   MSTP CIST PORT BPDU Filter : 0
   SM Timers     : fdWhile=0 rrWhile=0 rbWhile=0 tcWhile=0 rcvdInfoWhile=0
   Perf Params   : InternalPortPathCost=2000000, useCfgPathCost=F
   Per-Port Vars :
     portId=(128;2) infoIs=MINE rcvdInfo=INFERIOR_ROOT_ALT
     role=DESIGNATED selectedRole=DESIGNATED
     cistDesignatedTimes={fwdDelay=15 maxAge=20 messageAge=0 hops=20}
     cistMsgTimes       ={fwdDelay=15 maxAge=20 messageAge=0 hops=19 helloTime=2}
     cistPortTimes      ={fwdDelay=15 maxAge=20 messageAge=0 hops=20 helloTime=2}
     cistDesignatedPriority=
        {rootID     =(70:72:cf:18:3e:0c;32768;0) : extRootPathCost=0 :
         rgnRootID  =(70:72:cf:18:3e:0c;32768;0) : intRootPathCost=0 :
         dsnBridgeID=(70:72:cf:18:3e:0c;32768;0} : dsnPortID=(128;2)}
     cistMsgPriority=
        {rootID     =(70:72:cf:18:3e:0c;32768;0} : extRootPathCost=0 :
         rgnRootID  =(70:72:cf:18:3e:0c;32768;0) : intRootPathCost=20000 :
         dsnBridgeID=(70:72:cf:5f:3e:25;32768;0) : dsnPortID=(128;1)}
     cistPortPriority=
        {rootID     =(70:72:cf:18:3e:0c;32768;0} : extRootPathCost=0
         rgnRootID  =(70:72:cf:18:3e:0c;32768;0) : intRootPathCost=0
         dsnBridgeID=(70:72:cf:18:3e:0c;32768;0) : dsnPortID=(128;2)}
   Flags    : FWD=1 FWDI=1 LRN=1  LRNI=1  PRPSD=0 PRPSI=0 RROOT=0 RSELT=0  SELTD=1
           AGR=1 AGRD=1 SYNC=0 SYNCD=1 TCPRP=0 UPDT=0  RCVTC=0 RCVMSG=0 CMSTR=0
   SM states: PIM=CURRENT       PRT=DSGN_PORT    PST=FORWARDING TCM=ACTIVE
   MSTP CIST Lport : 1
   MSTP CIST PORT Priority : 8
   MSTP CIST PORT Admin Path Cost : 0
   MSTP CIST PORT Admin Edge port : 0
   MSTP CIST PORT BPDUS RX Enable : 0
   MSTP CIST PORT BPDUS TX Enable : 0
   MSTP CIST PORT Restricted Port Role : 0
   MSTP CIST PORT Restricted Port Tcn : 0
   MSTP CIST PORT BPDU Guard : 0
   MSTP CIST PORT LOOP Guard : 0
   MSTP CIST PORT ROOT Guard : 0
   MSTP CIST PORT BPDU Filter : 0
   SM Timers     : fdWhile=0 rrWhile=0 rbWhile=0 tcWhile=0 rcvdInfoWhile=0
   Perf Params   : InternalPortPathCost=2000000, useCfgPathCost=F
   Per-Port Vars :
      portId=(128;1) infoIs=MINE rcvdInfo=INFERIOR_ROOT_ALT
      role=DESIGNATED selectedRole=DESIGNATED
      cistDesignatedTimes={fwdDelay=15 maxAge=20 messageAge=0 hops=20}
      cistMsgTimes       ={fwdDelay=15 maxAge=20 messageAge=0 hops=19 helloTime=2}
      cistPortTimes      ={fwdDelay=15 maxAge=20 messageAge=0 hops=20 helloTime=2}
      cistDesignatedPriority=
         {rootID     =(70:72:cf:18:3e:0c;32768;0) : extRootPathCost=0 :
          rgnRootID  =(70:72:cf:18:3e:0c;32768;0) : intRootPathCost=0 :
          dsnBridgeID=(70:72:cf:18:3e:0c;32768;0} : dsnPortID=(128;1)}
      cistMsgPriority=
         {rootID     =(70:72:cf:18:3e:0c;32768;0} : extRootPathCost=0 :
          rgnRootID  =(70:72:cf:18:3e:0c;32768;0) : intRootPathCost=2000000 :
          dsnBridgeID=(70:72:cf:36:0e:63;32768;0) : dsnPortID=(128;1)}
      cistPortPriority=
         {rootID     =(70:72:cf:18:3e:0c;32768;0} : extRootPathCost=0
          rgnRootID  =(70:72:cf:18:3e:0c;32768;0) : intRootPathCost=0
          dsnBridgeID=(70:72:cf:18:3e:0c;32768;0) : dsnPortID=(128;1)}
   Flags    : FWD=1 FWDI=1 LRN=1  LRNI=1  PRPSD=0 PRPSI=0 RROOT=0 RSELT=0  SELTD=1
              AGR=1 AGRD=1 SYNC=0 SYNCD=1 TCPRP=0 UPDT=0  RCVTC=0 RCVMSG=0 CMSTR=0
   SM states: PIM=CURRENT       PRT=DSGN_PORT    PST=FORWARDING TCM=ACTIVE
   MSTP MSTI Config OVSDB info:
   MSTP MSTI VLANs: 10
   MSTP MSTI Priority 8

   mstpEnabled       : Yes
   valid             : Yes
   vlanGroupNum      : 0
   mstiRootPortID    : port#=0, priority=0
   MstiBridgeTimes   : {hops=20}
   mstiRootTimes     : {hops=20}
   BridgeIdentifier  : {mac=70:72:cf:18:3e:0c priority=32768 sysID=1}
   MstiBridgePriority:
           rgnRootID   {mac=70:72:cf:18:3e:0c priority=32768 sysID=1}
           intRootPathCost=0
           dsnBridgeID {mac=70:72:cf:18:3e:0c priority=32768 sysID=1}
           dsnPortID=(0;0)
   mstiRootPriority  :
           rgnRootID   {mac=70:72:cf:18:3e:0c priority=32768 sysID=1}
           intRootPathCost=0
           dsnBridgeID {mac=70:72:cf:18:3e:0c priority=32768 sysID=1}
           dsnPortID=(0;0)
   SM states         : PRS=ROLE_SELECTION

   Total BPDU Filters activated: 0
   TC Trap Control   : false
   MSTP MSTI Lport : 2
   MSTP CIST PORT Priority : 8
   MSTP CIST PORT Admin Path Cost : 0

   SM Timers     : fdWhile=0 rrWhile=0 rbWhile=0 tcWhile=0 rcvdInfoWhile=0
   Perf Params   : InternalPortPathCost=2000000, useCfgPathCost=F
   Per-Port Vars :
       portId=(128;2) infoIs=MINE rcvdInfo=INFERIOR_ROOT_ALT
       role=DESIGNATED selectedRole=DESIGNATED
       mstiDesignatedTimes={hops=20}
       mstiMsgTimes       ={hops=19}
       mstiPortTimes      ={hops=20}
       mstiDesignatedPriority=
          {rgnRootID  =(70:72:cf:18:3e:0c;32768;1) : intRootPathCost=0 :
           dsnBridgeID=(70:72:cf:18:3e:0c;32768;1} : dsnPortID=(128;2)}
       mstiMsgPriority=
          {rgnRootID  =(70:72:cf:18:3e:0c;32768;1) : intRootPathCost=20000 :
           dsnBridgeID=(70:72:cf:5f:3e:25;32768;1} : dsnPortID=(128;1)}
       mstiPortPriority=
          {rgnRootID  =(70:72:cf:18:3e:0c;32768;1) : intRootPathCost=0 :
           dsnBridgeID=(70:72:cf:18:3e:0c;32768;1} : dsnPortID=(128;2)}
   Flags    : FWD=1 FWDI=1 LRN=1  LRNI=1  PRPSD=0 PRPSI=0 RROOT=0 RSELT=0 SELTD=1
              AGR=1 AGRD=1 SYNC=0 SYNCD=1 TCPRP=0 UPDT=0  RCVTC=0 RCVMSG=0
              MSTR=0       MSTRD=0
   SM states: PIM=CURRENT       PRT=DSGN_PORT    PST=FORWARDING TCM=ACTIVE

   MSTP MSTI Lport : 1
   MSTP CIST PORT Priority : 8
   MSTP CIST PORT Admin Path Cost : 0

   SM Timers     : fdWhile=0 rrWhile=0 rbWhile=0 tcWhile=0 rcvdInfoWhile=0
   Perf Params   : InternalPortPathCost=2000000, useCfgPathCost=F
   Per-Port Vars :
      portId=(128;1) infoIs=MINE rcvdInfo=INFERIOR_ROOT_ALT
      role=DESIGNATED selectedRole=DESIGNATED
      mstiDesignatedTimes={hops=20}
      mstiMsgTimes       ={hops=19}
      mstiPortTimes      ={hops=20}
      mstiDesignatedPriority=
         {rgnRootID  =(70:72:cf:18:3e:0c;32768;1) : intRootPathCost=0 :
          dsnBridgeID=(70:72:cf:18:3e:0c;32768;1} : dsnPortID=(128;1)}
      mstiMsgPriority=
         {rgnRootID  =(70:72:cf:18:3e:0c;32768;1) : intRootPathCost=2000000 :
          dsnBridgeID=(70:72:cf:36:0e:63;32768;1} : dsnPortID=(128;1)}
      mstiPortPriority=
         {rgnRootID  =(70:72:cf:18:3e:0c;32768;1) : intRootPathCost=0 :
          dsnBridgeID=(70:72:cf:18:3e:0c;32768;1} : dsnPortID=(128;1)}
   Flags    : FWD=1 FWDI=1 LRN=1  LRNI=1  PRPSD=0 PRPSI=0 RROOT=0 RSELT=0 SELTD=1
              AGR=1 AGRD=1 SYNC=0 SYNCD=1 TCPRP=0 UPDT=0  RCVTC=0 RCVMSG=0
              MSTR=0       MSTRD=0
   SM states: PIM=CURRENT       PRT=DSGN_PORT    PST=FORWARDING TCM=ACTIVE

   -------------------------------------------------------------------------
   [End] Daemon ops-stpd
   -------------------------------------------------------------------------
   =========================================================================
   [End] Feature mstp
   =========================================================================
   Diagnostic dump captured for feature mstp
   switch#
```

Information to debug an MSTP issue can be obtained by running the `show tech mstp` command:
```
   switch# show tech mstp
   ====================================================
   Show Tech executed on Mon Jun 20 05:47:40 2016
   ====================================================
   ====================================================
   [Begin] Feature mstp
   ====================================================

   *********************************
   Command : show spanning-tree detail
   *********************************
   MST0
     Spanning tree status: Enabled
     Root ID    Priority   : 32768
                MAC-Address: 70:72:cf:3b:ea:a4
                This bridge is the root
                Hello time(in seconds):2  Max Age(in seconds):20  Forward Delay(in seconds):15

     Bridge ID  Priority  : 32768
                MAC-Address: 70:72:cf:3b:ea:a4
                Hello time(in seconds):2  Max Age(in seconds):20  Forward Delay(in seconds):15

   Port         Role           State      Cost    Priority   Type
   ------------ -------------- ---------- ------- ---------- ----------
   1            Designated     Forwarding 0       128        point_to_point
   2            Designated     Forwarding 0       128        point_to_point

   Topology change flag          : True
   Number of topology changes    : 2
   Last topology change occurred : 248988 seconds ago
   Timers:    Hello expiry  1 , Forward delay expiry 0

   Port 1
   Designated root has priority               :32768 Address: 70:72:cf:3b:ea:a4
   Designated bridge has priority             :32768 Address: 70:72:cf:3b:ea:a4
   Designated port                            :1
   Number of transitions to forwarding state  : 0
   Bpdus sent 124496, received 2

   Port 2
   Designated root has priority               :32768 Address: 70:72:cf:3b:ea:a4
   Designated bridge has priority             :32768 Address: 70:72:cf:3b:ea:a4
   Designated port                            :2
   Number of transitions to forwarding state  : 0
   Bpdus sent 124496, received 2

   *********************************
   Command : show spanning-tree mst-config
   *********************************
   MST configuration information
      MST config ID        : mst2
      MST config revision  : 2
      MST config digest    : 870555C957F1B44530B7D56FD4716ADF
      Number of instances  : 1

   Instance ID     Member VLANs
   --------------- ----------------------------------
   1               10

   *********************************
   Command : show spanning-tree mst
   *********************************
   #### MST0
   Vlans mapped:  1-9,11-4095
   Bridge         Address:70:72:cf:3b:ea:a4    priority:32768
   Root
   Regional Root
   Operational    Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6
   Configured     Hello time(in seconds): 2  Forward delay(in seconds):15  Max-age(in seconds):20  txHoldCount(in pps): 6

   Port           Role           State      Cost       Priority   Type
   -------------- -------------- ---------- ---------- ---------- ----------
   1              Designated     Forwarding 0          128        point_to_point
   2              Designated     Forwarding 0          128        point_to_point

   #### MST1
   Vlans mapped:  10
   Bridge         Address:70:72:cf:3b:ea:a4    Priority:32768
   Root           Address:70:72:cf:3b:ea:a4    Priority:32769
                  Port:, Cost:0, Rem Hops:0

   Port           Role           State      Cost    Priority   Type
   -------------- -------------- ---------- ------- ---------- ----------
   1              Designated     Forwarding 0       128        point_to_point
   2              Designated     Forwarding 0       128        point_to_point

   ====================================================
   [End] Feature mstp
   ====================================================

   ====================================================
   Show Tech commands executed successfully
   ====================================================
```

##### MSTP events description

|Event                                                                |Example|
|----------------------------------------------------------------------|------------|
|MSTP Enabled                                                          |Spanning Tree Protocol enabled|
|MSTP Disabled                                                         |Spanning Tree Protocol disabled|
|{config_parameter} should be {value}                                  |FWD_DELAY should be >= 10|
|BPDU has {config_parameter} from port {value}                         |BPDU has FWD_DELAY 0 from port 1 |
|Root changed from {old_priority}:{old_mac} to {new_priority}:{new_mac}|Root changed from 8:23:0f:cf:ed:c3:51 to 8:48:0f:cf:af:d3:93|
|Port {port} disabled - BPDU received on protected port                |Port 1 disabled - BPDU received on protected port|
|{proto} starved for {pkt_type} on port {port} from {priority_mac}     |CIST starved for BPDU rx on port 1 from 8:48:0f:cf:af:d3:93|
|BPDU loss- port {port} moved to inconsistent state for {proto}        |BPDU loss- port 1 moved to inconsistent state for CIST|
|Topology Change received on port {port} for {proto} from source: {mac}|Topology Change received on port 1 for CIST from source: 48:0f:cf:af:d3:93|
|{proto} - Topology Change generated on port {port} going in to {state}|CIST - Topology Change generated on port 1 going in to forwarding|
|BPDU received on admin edge port {port}                               |BPDU received on admin edge port 1|
|Port {port} blocked on CIST                                           |Port 1 blocked on CIST|
|Port {port} unblocked on CIST                                         |Port 1 unblocked on CIST|
|Port {port} blocked on MST{instance}                                  |Port 1 blocked on MST2|
|Port {port} unblocked on MST{instance}                                |Port 1 unblocked for MST2|
|{proto} Root Port changed from {old_port} to {new_port}               |MSTP Root port chnaged from 2 to 1|

<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
## CLI
Click [here](http://git.openswitch.net/cgit/openswitch/ops/plain/docs/MSTP_cli.md) for the CLI commands related to the MSTP feature.

## Related features
When configuring the switch for MSTP, it might also be necessary to configure the [Physical Interface](/documents/user/interface_user_guide) so that the interface to which a neighbor is connected acts as expected.
