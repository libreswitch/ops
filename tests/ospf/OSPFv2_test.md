#OSPFv2 Test Cases

## Contents

<!-- TOC depth:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Verifying OSPFv2 router ID configurations](#verifying-ospfv2-router-id-configurations)
- [Test cases to verify OSPFv2 adjacencies](#test-cases-to-verify-ospfv2-adjacencies)
- [Test cases to verify the OSPFv2 designated router election process](#test-cases-to-verify-the-ospfv2-designated-router-election-process)
- [Test cases to verify OSPFv2 learning and advertising of routes](#test-cases-to-verify-ospfv2-learning-and-advertising-of-routes)
- [Test cases to verify OSPFv2 passive interface](#test-cases-to-verify-ospfv2-passive-interface)
- [Test cases to verify OSPFv2 inter area and ABR](#test-cases-to-verify-ospfv2-inter-area-and-abr)
- [Test cases to verify OSPFv2 authentication](#test-cases-to-verify-ospfv2-authentication)
- [Test cases to verify area as NSSA](#test-cases-to-verify-area-as-nssa)
- [Test cases to verify area as Stubby](#test-cases-to-verify-area-as-stubby)
- [Test cases to verify stub router advertisement](#test-cases-to-verify-stub-router-advertisement)
- [Test cases to verify virtual links](#test-cases-to-verify-virtual-links)
- [Test cases to verify SPF throttling](#test-cases-to-verify-spf-throttling)
- [Test cases to verify OSPFv2 area network filtering](#test-cases-to-verify-ospfv2-area-network-filtering)
- [Test cases to verify the best route selection by GNU Zebra](#test-cases-to-verify-the-best-route-selection-by-gnu-zebra)
- [Test cases to verify OSPFv2 performance](#test-cases-to-verify-ospfv2-performance)
- [Future extensions](#future-extensions)
<!-- /TOC -->

## Verifying OSPFv2 router ID configurations

### Objective
Verify the system global and router instance level, and the router ID configurations.
### Requirements
Two switches are required for this test.

### Setup

#### Topology diagram

```ditaa

 +------------+           +--------------+
 |            |           |              |
 |  Switch 1 1+-----------+1  Switch 2   |
 |            |           |              |
 +------------+           +--------------+
```
### Verifying that the dynamic router ID is selected
**Test case 1.01**
### Precondition
The system global router ID and router instance level router ID are not configured.

### Description
When the hello packets are sent out, the router ID is selected from the GNU Zebra.

### Test result criteria
#### Test pass criteria
The test case is successful if the hello packet contains the router ID that was allocated dynamically by GNU Zebra. The adjacency should be formed between switch 1 and switch 2. This can be verified using the `show ip ospf neighbor`command .
#### Test fail criteria
The test case fails if:
- The hello packets are not sent out. The hello packets are not sent out if the router ID is not allocated by RTM.
- The adjacency is not formed between switch 1 and switch 2.

### Verifying that the globally configured router ID is not selected when dynamic router ID is present
**Test case 1.02**
### Precondition
The following IDs are not configured

- The global router ID
- The router ID in router ospf context

### Description
Check the router id assigned by GNU Zebra. Configure the global router ID using the `router-id <A.B.C.D>` command in configuration context. The hello packets do not contain the router ID that was configured in configuration context. The ospfd daemon continues to use the router ID it was using earlier.

A configuration example follows:
```
switch#config t
switch(conf)#router-id 1.2.3.4
```

### Test result criteria
#### Test pass criteria
The test case is successful if
The hello packet does not have the router ID that was configured in configuration context but has the router ID that was previously assigned by the GNU Zebra. The adjacency should be formed between switch 1 and switch 2. This can be verified using the `show ip ospf neighbor`command.
#### Test fail criteria
The test case is a failure if:
- The hello packet contains the router ID that was configured in configuration context.
- The adjacency is not formed between switch 1 and switch 2.

### Verifying that the global router ID is used after the global router ID is removed
**Test case 1.03**
### Preconditions
- The global router ID is configured.
- The router ID is not configured in router ospf context.

### Description
Remove the global router ID using the `no router-id` command in configuration context. The hello packets contain the router ID that was previously configured in configuration context.
A configuration example follows:
```
switch#config t
switch(conf)#no router-id
```

### Test result criteria
#### Test pass criteria
The test case is successful if the hello packet has the router ID that was configured in the configuration context. The adjacency should be formed between switch 1 and switch 2. This can be verified using the `show ip ospf neighbor`command.
#### Test fail criteria
The test case fails if:
- The hello packet does not contain the router ID that was configured in the configuration context.
- The adjacency is not formed between switch 1 and switch 2.

### Verifying that the router ID configured in router ospf context is selected
**Test case 1.04**
### Precondition
 - The global router ID is not configured.
 - The router ID is not configured in router ospf context.

### Description
Configure the instance level router id using the  `router-id <A.B.C.D>` command in router ospf context. The hello packets contain the router ID that was configured in router ospf context.
The configuration example follows:
```
switch#config t
switch(conf)#router ospf
switch(config-router)#router-id 1.2.3.4
```

### Test result criteria
#### Test pass criteria
The test case is successful if the hello packet has the router id that is configured in router ospf context. The adjacency should be formed between switch 1 and switch 2. This can be verified using the `show ip ospf neighbor`command.
#### Test fail criteria
The test case fails if the hello packet does not contain the router ID that is configured in router ospf context or the adjacency is not formed between switch 1 and switch 2.

### Verifying that the instance level router id is used even after removing it
**Test case 1.05**
### Precondition
 - The global router id is not configured
 - The router ID is configured in router ospf context

### Description
Remove the instance level router id using the `no router-id` command in router ospf context. The hello packets  contain the router ID that was previously configured in router ospf context, as the ospfd daemon continues to use the router ID that was configured.
A configuration example follows:
```
switch#config t
switch(conf)#router ospf
switch(config-router)#no router-id
```

### Test result criteria
#### Test pass criteria
The test case is successful if the hello packet contains the router id that was configured in router ospf context. The adjacency should be formed between switch 1 and switch 2. This can be verified using the`show ip ospf neighbor` command.
#### Test fail criteria
The test case fails if the hello packet does not contain the router id that was configured in router ospf context or the adjacency is not formed between switch 1 and switch 2.

### Verifying that the globally configured router id is not selected when the instance level router id is removed
**Test case 1.06**
### Precondition
 - The global router id is configured
 - The router ID is configured in router ospf context.

### Description
Remove the instance level router ID using the `no router-id` command in router ospf context. The hello packets contain the router ID that was previously configured in router ospf context as the ospfd daemon will continue to use the router ID that was configured.
A configuration example follows:
```
switch#config t
switch(conf)#router-id 2.3.4.5
switch(conf)#router ospf
switch(conf)#router-id 1.2.3.4
switch(config-router)#no router-id
```

### Test result criteria
#### Test pass criteria
The test case is successful if the hello packet has the router id that was configured in router ospf context. The adjacency should be formed between switch 1 and switch 2. This can be verified using the `show ip ospf neighbor` command.
#### Test fail criteria
The test case fails if the hello packet does not contain the router ID that was configured in router ospf context or if the adjacency is not formed between switch 1 and switch 2.

## Test cases to verify OSPFv2 adjacencies
### Objective
Verify the OSPFv2 adjacency related functionality.
### Requirements
Four switches are required for this test case.

### Setup

#### Topology diagram

```ditaa
+---------------+             +---------------+          +---------------+
|               |    Area 0   |               |  Area 1  |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+1  Switch 3    |
|               |             |               |          |               |
|               |             |               |          |               |
+---------------+             +---------------+          +---------------+
```

### Test case to verify that the neighbors are discovered
**Test case 2.01**
### Precondition
 None

### Description
The hello packets are exchanged between the adjacent switches. Capture the packets using packet capture tools like tcpdump and check if the hello packets are exchanged. Also neighbors are present in the neighbor table. This can be verified using the`show ip ospf neighbor` command.

A configuration example follows:
```
SWITCH 1
switch#config t
switch(conf)#router ospf
switch(conf)#network 10.10.10.0/24 area 0

SWITCH 2
switch#config t
switch(conf)#router ospf
switch(conf)#network 10.10.10.0/24 area 0
switch(conf)#network 20.20.20.0/24 area 1

SWITCH 3
switch#config t
switch(conf)#router ospf
switch(conf)#network 20.20.20.0/24 area 1
```
### Test result criteria
#### Test pass criteria
The test case is successful if the `show ip ospf neighbor` displays the neighbors.
#### Test fail criteria
The test case is a failure if the `show ip ospf neighbor` does not display the neighbors.

### Test case to verify that the adjacency is impacted when OSPFv2 is disabled and enabled
**Test case 2.02**
### Precondition
The neighbors are already discovered and adjacency is formed.

### Description
The  `show ip ospf neighbor` command displays the neighbor details.
- When OSPFv2 is disabled in switch 1 using the `no router ospf` command in configuration context, the adjacency between switch 1 and switch 2 should be torn down. But the adjacency between switch 2 and switch 3 should not be disturbed. This can be verified using the `show ip ospf neighbor`command in switch 2.
- Now restore the adjacency using the `no router ospf` command in configuration context in switch 1. The adjacency between switch 1 and switch 2 should be restored.
A configuration example follows:
```
SWITCH 1
switch#config t
switch(conf)#no router ospf
switch(conf)#router ospf
switch(conf)#network 10.10.10.0/24 area 0
```

### Test result criteria
#### Test pass criteria
The test case is successful if:
When the OSPFv2 is disbled in switch 1:
- The neighbor entry of switch 1 is removed in switch 2.
- The neighbor entry of switch 3 is present in switch 2.
When the OSPFv2 is enabled in switch 1:
- The neighbor entry of switch 1 is present in switch 2.

#### Test fail criteria
The test case fails if:
- The neighbor entry of switch 1 is not removed in switch 2 when the OSPFv2 is disabled.
- The neighbor entry of switch 1 is not present in switch 2 when the OSPFv2 is enabled.

### Test case to verify that adjacency is impacted when dead timer is changed
**Test case 2.03**
### Precondition
The neighbors are already discovered and adjacency is formed.

### Description
The `show ip ospf neighbor detail` command displays the neighbor details. Modify the dead timer in switch 2 using the command `ip ospf dead-interval <dead_interval>` in the interface context. The adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be torn down. This can be verified using the `show ip ospf neighbor` command in switch 1 and switch 2.
The adjacency is formed again when the same dead interval is configured in all the switches.
A configuration example follows:
```
switch#config t
switch(conf)#interface 1
switch(config-if)#ip ospf dead-interval 50
switch(conf)#interface 2
switch(config-if)#ip ospf dead-interval 50
```
### Test result criteria
#### Test pass criteria
The test case is successful if the neighbor entry of switch 2 is removed in switch 1 and switch 3. And adjacency is formed again when same dead interval is configured in switch 1 and switch 3.

#### Test fail criteria
The test case is a failure if the neighbor entry of switch 2 is not removed in switch 1 and switch 3. Or adjacency is not formed again when same dead interval is configured in switch 1 and switch 3.

### Test case to verify that adjacency is impacted when hello timer is changed
**Test case 2.04**
### Precondition
The neighbors are already discovered and adjacency is formed.

### Description
The `show ip ospf neighbor detail`  command displays the neighbor details. Modify the hello timer in switch 2 using the `ip ospf hello-interval <hello_interval>` command in the interface context. The adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be torn down. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.
The adjacency is formed again when the same hello interval is configured in all the switches.
A configuration example follows:
```
switch#config t
switch(conf)#interface 1
switch(config-if)#ip ospf hello-interval 50
switch(conf)#interface 2
switch(config-if)#ip ospf hello-interval 50
```

### Test result criteria
#### Test pass criteria
The test case is successful if the neighbor entry of switch 2 is removed in switch 1 and switch 3. And adjacency is formed again when same dead interval is configured in switch 1 and switch 3.

#### Test fail criteria
The test case fails if the neighbor entry of switch 2 is not removed in switch 1 and switch 3. Or adjacency is not formed again when same dead interval is configured in switch 1 and switch 3.

### Test case to verify that adjacency is impacted when MTU mismatches
**Test case 2.05**
### Precondition
The Neighbors are already discovered and adjacency is formed.

### Description
The `show ip ospf neighbor detail` command displays the neighbor details.
- Modify the mtu value in switch 2 using the command `mtu <mtu-value>` in the interface context.
- The adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be torn down, since by default the mtu-ignore flag is set to false. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.
- Now set the mtu-ignore flag using the `ip ospf mtu-ignore` command in the interface context.
- The adjacency between switch 1 and switch 2 and switch 2 and switch 3 should be restored. This can be verified using the command `show ip ospf neighbor` in switch 1 and switch 2.

A configuration example follows:
```
switch#config t
switch(conf)#interface 1
switch(config-if)#mtu 700
switch(config-if)#ip ospf mtu-ignore
switch(conf)#interface 2
switch(config-if)#mtu 700
switch(config-if)#ip ospf mtu-ignore
```

### Test result criteria
#### Test pass criteria
The test case is successful if:
- The neighbor entry of switch 2 is removed in switch 1 and switch 3 when mtu-ignore flag is unset.
- The neighbor entry of switch 2 is present in switch 1 and switch 3 when mtu-ignore flag is set.

#### Test fail criteria
The test case is a failure if:
- The neighbor entry of switch 2 is not removed in switch 1 and switch 3 when mtu-ignore flag is unset.
- The neighbor entry of switch 2 is not present in switch 1 and switch 3 when mtu-ignore flag is set.

### Test case to verify that neighbor adjacencies are formed when link is point to point
**Test case 2.06**
### Precondition
 None

### Description
Configure the link between switch 1 and switch 2 as point to point using the `ip ospf network point-to-point`  command in interface context. The`show ip ospf neighbor detail`command displays the neighbor details. The adjacency between switch 1 and switch 2 is formed. This can be verified using the`show ip ospf neighbor`command in switch 1 and switch 2.
A configuration example follows:
```
switch# configure terminal
switch# router ospf
switch(config-router)# neighbor 16.77.114.14 priority 20 poll-interval 40
switch(conf)#interface 1
switch(config-if)#ip ospf network point-to-point
```

### Test result criteria
#### Test pass criteria
The test case is successful if the neighbor entry of switch 2 is present in switch 1 and vice versa.
#### Test fail criteria
The test case fails if the neighbor entry of switch 2 is not present in switch 1 and vice versa.


## Test cases to verify the OSPFv2 designated router election process
### Objective
Verify the OSPFv2 designated router election process.

### Requirements
Three switches are required for this test.

### Setup

#### Topology diagram

```ditaa
                     +---------------+
                     | L2            |
                   1 | Switch        |
     +---------------+               +-------------------------+
     |               |               |3                        |
     |               +---------------+                         |
     |                           |2                            |
     |1                          |1                            |1
+---------------+             +---------------+          +---------------+
|               |             |               |          |               |
| Switch 1      |             |   Switch 2    |          |   Switch 3    |
|               |             |               |          |               |
|               |             |               |          |               |
+---------------+             +---------------+          +---------------+

```

### Test case to verify that the DR and BDR is selected
**Test case 3.01**
### Precondition
The priorities of switch 1, switch 2 and switch 3 are all same and is of default value.

### Description
Configure the router id in switch 2 using the `router-id 4.4.4.4` command in router ospf context. Similarly configure the router id `router-id 2.2.2.2` and `router-id 1.1.1.1` in switch 1 and switch 3 respectively.
The `show ip ospf interface` command is used to display the DR, BDR and priority information.

A configuration example follows:
```
SWITCH 1
switch# configure terminal
switch# router ospf
switch(config-router)# router-id 2.2.2.2

SWITCH 2
switch# configure terminal
switch# router ospf
switch(config-router)# router-id 4.4.4.4

SWITCH 3
switch# configure terminal
switch# router ospf
switch(config-router)# router-id 1.1.1.1

```

### Test result criteria
#### Test pass criteria
The test case is successful if switch 2 is selected as DR, switch 1 is BDR and switch 3 is other-DR.
#### Test fail criteria
The test case fails if switch 2 is not selected as DR, switch 1 is not BDR or switch 3 is not other-DR.

### Test case to verify that the BDR is selected as DR
**Test case 3.02**
### Precondition
 - Switch 1 is DR
 - Switch 2 is BDR
 - Switch 3 is DROther
 - Priority of Switch 1, Switch 2 and Switch 3 is 15, 10 and 5 respectively

### Description
Configure the priority in switch 1 as 0 using the`ip ospf priority <priority_value>`command in interface context.  Switch 2 should become the DR now, Switch 3 becomes the BDR and Switch 1 becomes the DROther. The `show ip ospf interface`command is used to display the DR, BDR and priority information.
A configuration example follows:
```
SWITCH 1
switch(conf)#interface 1
switch(config-if)#ip ospf priority 0
```

### Test result criteria
#### Test pass criteria
The test case is successful if switch 2 is selected as DR, Switch 3 as BDR and Switch 1 as DROther.
#### Test fail criteria
The test case fails if switch 2 is not selected as the DR or Switch 3 as BDR and Switch 1 as DROther.

### Test case to verify that the BDR is selected as DR when priority values are changed
**Test case 3.03**
### Precondition
 - Switch 1 is DROther
 - Switch 2 is DR
 - Switch 3 as BDR

### Description
Configure the priority of switch 3 using the  `ip ospf priority <priority_value>` command in interface context. The priority value is set such that switch 3 has a higher priority than switch 2.  The `show ip ospf interface` command is used to display the DR, BDR and priority information.
A configuration example follows:
```
SWITCH 1
switch(conf)#interface 1
switch(config-if)#ip ospf priority 0

SWITCH 2
switch(conf)#interface 1
switch(config-if)#ip ospf priority 10

SWITCH 3
switch(conf)#interface 1
switch(config-if)#ip ospf priority 20

```

### Test result criteria
#### Test pass criteria
The test case is successful if switch 3 is selected as a DR and switch 2 is selected as a BDR.
#### Test fail criteria
The test case fails if switch 3 is not selected as a DR or switch 2 is not selected as a BDR.

### Test case to verify that the DR election is triggered when router IDs are changed.
**Test case 3.04**
### Precondition
- The priorities of switch 1, switch 2 and switch 3 are all same (default value).
- The router ID of switch 1, switch 2 and switch 3 is 4.4.4.4, 2.2.2.2 and 1.1.1.1.
- Switch 1 is a DR, switch 2 is a BDR and switch 3 is an other-DR.

### Description
Configure the router ID in switch 3 using the `router-id 5.5.5.5`command in router ospf context. The `show ip ospf interface` command is used to display the DR, BDR, and priority information.
A configuration example follows:
```
SWITCH 3
switch# configure terminal
switch# router ospf
switch(config-router)# router-id 5.5.5.5

```

### Test result criteria
#### Test pass criteria
The test case is successful if switch 3 is selected as a DR, switch 1 is selected as a BDR and switch 2 is selected as an other-DR.
#### Test fail criteria
The test case fails if switch 3 is not selected as a DR, switch 1 is not selected as a BDR or switch 2 is not selected as an other-DR.

### Test case to verify that the no switch is elected DR when priority of all switches are 0.
**Test case 3.05**
### Precondition
The priorities of switch 1, switch 2 and switch 3 are all zero (0).

### Description
Since the priority of all the switches is zero (0), none of the switches are elected as DR or BDR.
A configuration example follows:
```
SWITCH 1
switch(conf)#interface 1
switch(config-if)#ip ospf priority 0

SWITCH 2
switch(conf)#interface 1
switch(config-if)#ip ospf priority 0

SWITCH 3
switch(conf)#interface 1
switch(config-if)#ip ospf priority 0
```

### Test result criteria
#### Test pass criteria
The test case is successful if none of the switches are elected as BR or DR.
#### Test fail criteria
The test case fails if any of the switches are elected as BR or DR.

## Test cases to verify OSPFv2 learning and advertising of routes
### Objective
Verify the OSPFv2 learning and advertising of routes learned.

### Requirements
Three switches are required for this test.

### Setup

#### Topology diagram

```ditaa
+---------------+             +---------------+          +---------------+
|               |             |               |          |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+2  Switch 3    |
|               |             |               |          |               |
|      2        |             |               |          |       1       |
+------+--------+             +---------------+          +-------+-------+
       |                                                         |
       |                                                         |
       |                                                         |
       |                                                         |
+------+--------+                                         +------+--------+
|      1        |                                         |      1        |
|  Host1        |                                         |  Host2        |
|               |                                         |               |
+---------------+                                         +---------------+
```

### Test case to verify redistribution of static routes
**Test case 4.01**
### Precondition
The neighbors have been discovered and adjacency is formed.

### Description
Configure the static routes in switch 2 using the `ip route A.B.C.D/M (<nexthop-ip> | <interface>) {distance}`command in configuration context. Redistribute the routes to the neighbors using the `redistribute static` command in router ospf context.
The `show rib` command in switch 1 is used to verify the routes redistributed by Switch 2.
A configuration example follows:
```
SWITCH 2
switch(conf)#interface 1
switch(config-if)# no shutdown
switch(config-if)# exit
switch(config)# ip route  192.168.1.0/24 1
switch(config)# ip route  192.168.2.0/24 1
switch(config)# ip route  192.168.3.0/24 1
switch# router ospf
switch(config-router)# redistribute static
```

### Test result criteria
#### Test pass criteria
The test case is successful if `show rib` command in switch 1 contains the routes advertised or redistributed by Switch 2.
#### Test fail criteria
The test case fails if `show rib` command in switch 1 does not contain the routes advertised or redistributed by Switch 2.

### Test case to verify redistribution of connected routes
**Test case 4.02**
### Precondition
The neighbors have been discovered and adjacency is formed.

### Description
Configure interfaces in switch 2. Redistribute the routes to the neighbors using the `redistribute connected` command in router ospf context.
The `show rib` command in switch 1 is used to verify the routes redistributed by Switch 2.
A configuration example follows:
```
SWITCH 1
switch# router ospf
switch(config-router)# redistribute connected
```

### Test result criteria
#### Test pass criteria
The test case is successful if the `show rib` command in switch 1 contains the routes advertised or redistributed by Switch 2.
#### Test fail criteria
The test case is a failure if the `show rib` command in switch 1 does not contain the routes advertised or redistributed by Switch 2.

### Test case to verify redistribution of bgp routes
**Test case 4.03**
### Precondition
The neighbors have been discovered and adjacency is formed.

### Description
Enable BGP in switch 2. Redistribute the routes learned through the BGP routing protocol to the neighbors using the `redistribute bgp` command in router ospf context.
The `show rib` command in switch 1 is used to verify the routes redistributed by Switch 2.
A configuration example follows:
```
SWITCH 1
switch(conf)# router ospf
switch(config-router)# router-id 1.1.1.1
switch(config-router)# network 10.10.10.0/24 area 0

SWITCH 2
switch(conf)# router ospf
switch(config-router)# router-id 2.2.2.2
switch(config-router)# network 10.10.10.0/24 area 0
switch(config-router)# redistribute bgp
switch(conf)# router bgp 1
switch(config-router)# network 20.20.20.0/24

SWITCH 3
switch(conf)# router bgp 1
switch(config-router)# network 20.20.20.0/24
```

### Test result criteria
#### Test pass criteria
The test case is successful if `show rib` command in switch 1 contains the routes advertised or redistributed by Switch 2.
#### Test fail criteria
The test case fails if `show rib` command in switch 1 does not contain the routes advertised or redistributed by Switch 2.

### Test case to verify redistribution of default route
**Test case 4.04**
### Precondition
The neighbors have been discovered and adjacency is formed.

### Description
Enable default route (0.0.0.0 subnet) redistribution on Switch 1 using `default-information originate` command. If `default-information originate always` command is used then the default route will be advertised even when there is no default route present in the switch 1 itself. The `show rib` command in switch 2 is used to verify the default route redistributed by Switch 1.

A configuration example follows:
```
SWITCH 1
switch(conf)# ip route 0.0.0.0/0 1
switch(conf)# router ospf
switch(config-router)# default-information originate always
```

### Test result criteria
#### Test pass criteria
The test case is successful if `show rib` command in switch 2 contains the default route advertised or redistributed by Switch 1.
#### Test fail criteria
The test case fails if `show rib` command in switch 2 does not contain the default route advertised or redistributed by Switch 1.

## Test cases to verify OSPFv2 passive interface
### Objective
Verify the OSPFv2 passive interface behavior.

### Requirements
Three switches are required for this test.

### Setup

#### Topology diagram

```ditaa
+---------------+             +---------------+          +---------------+
|               |             |               |          |               |
| Switch 1     1+-------------+1  Switch 2   2+----------+2  Switch 3    |
|               |             |               |          |               |
|               |             |               |          |        1      |
+---------------+             +---------------+          +--------+------+
                                                                  |
                                                                  |
                                                                  |
                                                                  |
                                                         +--------+-------+
                                                         |        1       |
                                                         |                |
                                                         |  Host 1        |
                                                         |                |
                                                         +----------------+

```

### Test case to verify passive interface behavior
**Test case 5.01**
### Precondition
- The neighbors have been discovered and adjacency is formed.
- OSPF is enabled on interface 1 of switch1, interface 1 and 2 of switch 2 and interface 1 and 2 of switch3.
- The connected subnetwork on switch 2 is advertised in the switch 2 router LSAs.

### Description
- Configure interface 2 of switch 2 as a passive interface using the `passive-interface <interface>` command in router ospf context.
- The adjacency with the switch 3 should be torn.
- When a static route is configured in switch 2 to reach switch 3, the switch 3 should be pingable from switch 1.
- The `show ip ospf route` command in switch 2 should not show any routes of switch 3.
- Now make the interface 2 in switch 2 as non passive interface using the command `no passive-interface <interface>`.

A configuration example follows:
```
SWITCH 2
switch(conf)# router ospf
switch(config-router)# passive-interface 2
switch(config-router)# no passive-interface 2
```

### Test result criteria
#### Test pass criteria
When the interface is configured as passive interface:
- The test case is successful if the `show ip ospf neighbor` command in switch 2 does not display switch 3. Also the `show ip ospf routes` command in switch 1 does not display the routes of the connected subnetwork (routes of OSPFv2 interfaces in switch 3) on switch 2 and switch 1.

When the interface is reverted to normal interface from passive interface:
- The test case is successful if the `show ip ospf neighbor` command in switch 2 displays switch 3.

#### Test fail criteria
When the interface is configured as passive interface:
- The test case fails if `show ip ospf neighbor` command in switch 2 displays switch 3.

When the interface is reverted to normal interface from passive interface:
- The test case fails if the `show ip ospf neighbor` command in switch 2 does not display switch 3.

### Test case to verify behaviour when passive interface default is set
**Test case 5.02**
### Precondition
- The neighbors have been discovered and adjacency is formed.
- OSPF is enabled on interface 1 of switch1, interface 1 and 2 of switch 2 and interface 1 and 2 of switch3.

### Description
- Configure all interfaces of switch 2 as passive using the `passive-interface default` command in router ospf context.
- The adjacency with the switch 3 should be torn.
- When a static route is configured in switch 2 to reach switch 3, the switch 3 should be pingable from switch 1.
- The `show ip ospf route` command in switch 2 should not show any routes of switch 3.
- Now make the interface 2 in switch 2 as non passive interface using the command `no passive-interface default` command in router ospf context.
A configuration example follows:
```
SWITCH 2
switch(conf)# router ospf
switch(config-router)# passive-interface default
switch(config-router)# no passive-interface default
```

### Test result criteria
#### Test pass criteria
When the interface is configured as passive interface:
- The test case is successful if the `show ip ospf neighbor` command in switch 3 does not display switch 2.
When the interface is reverted to normal interface from passive interface:
- The test case is successful if the `show ip ospf neighbor` command in switch 3 displays switch 2.

#### Test fail criteria
When the interface is configured as passive interface:
- The test case fails if the `show ip ospf neighbor` command in switch 3 displays switch 2.
When the interface is reverted to normal interface from passive interface:
- The test case is successful if the `show ip ospf neighbor` command in switch 3 does not display switch 2.

### Test case to verify behaviour when passive interface is configured as not passive
**Test case 5.03**
### Preconditions
 - The passive interface default flag is set on all the switches.
 - Interface 1 in switch 1 is configured as a passive interface.

### Description
Change interface 1 from passive to a non-passive interface using the  `no passive-interface <ifname>` command in router ospf context. Since the passive interface default flag is set, the interface continues to be passive.
A configuration example follows:
```
SWITCH 2
switch(conf)# router ospf
switch(config-router)# passive-interface default
switch(config-router)# no passive-interface 1
```

### Test result criteria
#### Test pass criteria
The test case is successful if the `show ip ospf neighbor` command in switch 3 does not display switch 2.
#### Test fail criteria
The test case fails if the `show ip ospf neighbor`command in switch 3 displays switch 2.

## Test cases to verify OSPFv2 inter area and ABR
### Objective
Verify the OSPFv2 inter-area and ABR functionality.

### Requirements
Four switches are required for this test.
### Setup

#### Topology diagram

```ditaa
+---------------+             +---------------+          +---------------+         +-------------+
|               |             |               |          |               |         |             |
|  Switch 1    1+-------------+1 Switch 2    2+----------+2  Switch 3   1+---------+1   Switch 4 |
|               |   Area 100  |               |  Area 0  |               | Area 200|             |
|     2         |             |               |          |               |         |             |
+-----+---------+             +---------------+          +---------------+         +-------------+
      |
      |
      | Area 100
      |
      |
+-----+---------+
|     2         |
| Switch 5      |
|               |
|               |
+---------------+
```

### Test case to verify ABR
**Test case 6.01**
### Precondition
The neighbors have been discovered and adjacency is formed.

### Description
Configure the following using the `network <A.B.C.D/M> area <area-id>` command in router ospf context:
**Note:** Switch 2 and switch 3 will act as ABRs.
- Interface 1 of switch 1 and interface 1 of switch 2 in Area 100
- Interface 2 of switch 3 and interface 2 of switch 2 in Area 0
- Interface 1 of switch 3 and interface 1 of switch 4 in Area 200

### Test result criteria
#### Test pass criteria
The test case is successful if the`show rib` command in switch 3 and switch 4 displays connected routes of the interfaces running OSPFv2 in switch 1.
#### Test fail criteria
The test case fails if the`show rib`command in switch 3 and switch 4 does not display connected routes of the interfaces running OSPFv2 in switch 1.

### Test case to verify learnt routes are removed in inter-area, when switch in another area goes down
**Test case 6.02**
### Precondition
The neighbors have been discovered and adjacency is formed.

### Description
1. Configure the following using the `network <A.B.C.D/M> area <area-id>` command in router ospf context. Switch 2 and switch 3 will act as ABRs.

	- Interface 1 of switch 1 and interface 1 of switch 2 in Area 100
	- Interface 2 of switch 3 and interface 2 of switch 2 in Area 0
	- Interface 1 of switch 3 and interface 1 of switch 4 in Area 200

2. Reboot switch 1.

### Test result criteria
#### Test pass criteria
The test case is successful if the `show rib` command in switch 3 and switch 4 does not display the connected routes of the interfaces running OSPFv2 on switch 1.
#### Test fail criteria
The test case fails if the  `show rib` command in switch 3 and switch 4 displays connected routes of the interfaces running OSPFv2 on switch 1.

### Test case to verify ABR learns and distributes networks in between the OSPFv2 areas
**Test case 6.03**
### Precondition
 - Neighbors have been discovered and adjacency is formed
 - Switch 5 has OSPFv2 enabled

### Description

Configure the following using the `network <A.B.C.D/M> area <area-id>` command in router ospf context:

**Note:** Switch 2 and switch 3 will act as ABRs.
- Interface 1 of switch 1 and interface 1 of switch 2 in Area 100
- Interface 2 of switch 3 and interface 2 of switch 2 in Area 0
- Interface 1 of switch 3 and interface 1 of switch 4 in Area 200

The OSPFv2 interfaces in switch 5 will be distributed via LSA.

### Test result criteria
#### Test pass criteria
The test case is successful if the `show rib` command in switch 3 and switch 4 displays connected routes of the interfaces running OSPFv2 in switch 1 and if the `show ip ospf database summary` command displays the routes learned from switch 1.
#### Test fail criteria
The test case fails if the `show rib` command in switch 3 and switch 4 does not display connected routes of the interfaces running OSPFv2 in switch 1.

### Test case to verify ABR distributes summarized routes
**Test case 6.04**
### Precondition
 - Neighbors have been discovered and adjacency is formed
 - Switch 1 has learned routes 10.10.10.1/24 and 10.10.20.1/24

### Description

Configure the following using the `network <A.B.C.D/M> area <area-id>` command in router ospf context:

**Note:** Switch 2 and switch 3 will act as ABRs.
- Interface 1 of switch 1 and interface 1 of switch 2 in Area 100
- Interface 2 of switch 3 and interface 2 of switch 2 in Area 0
- Interface 1 of switch 3 and interface 1 of switch 4 in Area 200


### Test result criteria
#### Test pass criteria
The test case is successful if the `show rib`command in switch 3 and switch 4 displays connected routes of the interfaces running OSPFv2 in switch 1 summarized as 10.10.0.0/16.
#### Test fail criteria
The test case fails if the `show rib` command in switch 3 and switch 4 does not display connected routes of the interfaces running OSPFv2 in switch 1 summarized as 10.10.0.0/16.

## Test cases to verify OSPFv2 authentication
### Objective
Verify OSPF authentication-related configurations in router and interface context.

### Requirements
Two switches are required for this test.
### Setup

#### Topology diagram

```ditaa
+---------------+          +---------------+
|               |  Area 1  |               |
|   Switch 2   2+----------+2  Switch 3    |
|               |          |               |
|               |          |               |
+---------------+          +---------------+

```

### Test case to verify md5 authentication in interface context
**Test case 7.01**
### Precondition
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description
- Configure the MD5 authentication in interface 2 of switch 2 using the `ip ospf authentication {message-digest}` and the `ip ospf authentication-key <key>` commands in interface context.
- Now the adjacency between switch 2 and switch 3 should be torn.
- Configure the md5 authentication in interface 2 of switch 3 using the command `ip ospf authentication {message-digest}` and `ip ospf authentication-key <key>` in interface context.
- Now the adjacency between switch 2 and switch 3 should be restored.

A configuration example follows:
```
SWITCH 2
switch(conf)#interface 2
switch(config-if)# ip ospf authentication message-digest
switch(config-if)# ip ospf message-digest-key 1 md5 sampleauth
switch(config-if)# exit

SWITCH 3
switch(conf)#interface 2
switch(config-if)# ip ospf authentication message-digest
switch(config-if)# ip ospf message-digest-key 1 md5 sampleauth
switch(config-if)# exit
```

### Test result criteria
#### Test pass criteria
When authentication is configured only on switch 2:
- The test case is successful if the `show ip ospf neighbor` command in switch 2 does not display switch 3.
When authentication is configured on switch 3 also:
- The test case is successful if the `show ip ospf neighbor` command used in switch 2 displays switch 3.

#### Test fail criteria
When authentication is configured only on switch 2:
- The test case fails if the`show ip ospf neighbor`command in switch 2 displays switch 3.
When authentication is configured on switch 3 also:
- The test case fails if the `show ip ospf neighbor` command used in switch 2 does not display switch 3.

### Test case to verify text authentication in interface context
**Test case 7.02**
### Precondition
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description
- Configure the text-based authentication in interface 2 of switch 2 using the  `ip ospf authentication` and `ip ospf authentication-key <key>` commands in interface context.
- Now the adjacency between switch 2 and switch 3 should be torn.
- Configure the text-based authentication in interface 2 of switch 3 using the  `ip ospf authentication` and `ip ospf authentication-key <key>` commands in interface context.
- Now the adjacency between switch 2 and switch 3 should be restored.

A configuration example follows:
```
SWITCH 2
switch(conf)#interface 2
switch(config-if)# ip ospf authentication
switch(config-if)# ip ospf authentication-key simpleauth
switch(config-if)# exit

SWITCH 3
switch(conf)#interface 2
switch(config-if)# ip ospf authentication
switch(config-if)# ip ospf authentication-key simpleauth
switch(config-if)# exit
```

#### Test result criteria
#### Test pass criteria
When authentication is configured only on switch 2:
- The test case is successful if the `show ip ospf neighbor` command in switch 2 does not display switch 3.
When authentication is configured on switch 3 also:
- The test case is successful if the `show ip ospf neighbor` command used in switch 2 displays switch 3.

#### Test fail criteria
When authentication is configured only on switch 2:
- The test case fails if the`show ip ospf neighbor`command in switch 2 displays switch 3.
When authentication is configured on switch 3 also:
- The test case fails if the `show ip ospf neighbor` command used in switch 2 does not display switch 3.

### Test case to verify MD5 authentication configured per area
**Test case 7.03**
### Precondition
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description
- Configure the MD5 authentication in switch 2 using the `area  (<area_ip>|<area_id>) authentication [message-digest]` command in router ospf context and `ip ospf authentication-key <key>` command in interface context.
- Now the adjacency between switch 2 and switch 3 should be torn.
- Configure the MD5 authentication in switch 3 using the `area  (<area_ip>|<area_id>) authentication [message-digest]` command in router ospf context and the `ip ospf authentication-key <key>` command in interface context.
- Now the adjacency between switch 2 and switch 3 should be restored.

A configuration example follows:
```
SWITCH 2
switch(conf)# router ospf
switch(config-router)# area 1 authentication message-digest
switch(config-if)# exit
switch(conf)#interface 2
switch(config-if)# ip ospf message-digest-key 1 md5 sampleauth
switch(config-if)# exit

SWITCH 3
switch(conf)# router ospf
switch(config-router)# area 1 authentication message-digest
switch(config-if)# exit
switch(conf)#interface 2
switch(config-if)# ip ospf message-digest-key 1 md5 sampleauth
switch(config-if)# exit
```

#### Test result criteria
#### Test pass criteria
When authentication is configured only on switch 2:
- The test case is successful if the `show ip ospf neighbor` command in switch 2 does not display switch 3.
When authentication is configured on switch 3 also:
- The test case is successful if the `show ip ospf neighbor` command used in switch 2 displays switch 3.

#### Test fail criteria
When authentication is configured only on switch 2:
- The test case fails if the`show ip ospf neighbor`command in switch 2 displays switch 3.
When authentication is configured on switch 3 also:
- The test case fails if the `show ip ospf neighbor` command used in switch 2 does not display switch 3.

### Test case to verify text-based authentication configured per area
**Test case 7.04**
### Precondition
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description
- Configure the text-based authentication in switch 2 using the `area  (<area_ip>|<area_id>) authentication` command in router ospf context and the `ip ospf authentication-key <key>` command in interface context.
- Now the adjacency between switch 2 and switch 3 should be torn.
- Configure the MD5 authentication in switch 3 using the `area  (<area_ip>|<area_id>) authentication [message-digest]` command in router ospf context and the `ip ospf authentication-key <key>` command in interface context.
- Now the adjacency between switch 2 and switch 3 should be restored.

A configuration example follows:
```
SWITCH 2
switch(conf)# router ospf
switch(config-router)# area 1 authentication
switch(config-if)# exit
switch(conf)#interface 2
switch(config-if)# ip ospf authentication-key simpleauth
switch(config-if)# exit

SWITCH 3
switch(conf)# router ospf
switch(config-router)# area 1 authentication
switch(config-if)# exit
switch(conf)#interface 2
switch(config-if)# ip ospf authentication-key simpleauth
switch(config-if)# exit
```

#### Test result criteria
#### Test pass criteria
When authentication is configured only on switch 2:
- The test case is successful if the `show ip ospf neighbor` command in switch 2 does not display switch 3.
When authentication is configured on switch 3 also:
- The test case is successful if the `show ip ospf neighbor` command used in switch 2 displays switch 3.

#### Test fail criteria
When authentication is configured only on switch 2:
- The test case fails if the`show ip ospf neighbor`command in switch 2 displays switch 3.
When authentication is configured on switch 3 also:
- The test case fails if the `show ip ospf neighbor` command used in switch 2 does not display switch 3.

### Test case to verify text-based authentication configured in interface context and MD5 authentication in router ospf context
**Test case 7.05**
### Precondition
 - Neighbors have been discovered and adjacency is formed
 - No authentication is configured

### Description

To set up this test:
1.	In switch 2, configure the text-based authentication in interface 2 using the `ip ospf authentication` and `ip ospf message-digest-key <key>` commands in interface context.
2.	 Configure the MD5-based authentication in switch 2 using the `area  (<area_ip>|<area_id>) authentication message-digest` command in router ospf context.
3.	In switch 3, configure the MD5-based authentication in switch 2 using the `area  (<area_ip>|<area_id>) authentication message-digest` command in router ospf context.
4.	Configure the key using the `ip ospf message-digest-key <key>` command in interface context. Now adjacency will be torn as the interface level configuration takes precedence.
5.	Now configure text-based authentication in interface 2 of switch 3 using the `ip ospf authentication` command.

A configuration example follows:
```
SWITCH 2
switch(conf)# router ospf
switch(config-router)# area 1 authentication message-digest
switch(config-if)# exit
switch(conf)#interface 2
switch(config-if)# ip ospf authentication
switch(config-if)# ip ospf authentication-key simpleauth
switch(config-if)# exit

SWITCH 3
switch(conf)# router ospf
switch(config-router)# area 1 authentication message-digest
switch(config-if)# exit
switch(conf)#interface 2
switch(config-if)# ip ospf authentication
switch(config-if)# ip ospf authentication-key simpleauth
switch(config-if)# exit
```
### Test result criteria
#### Test pass criteria
The test case is successful if the `show ip ospf neighbor` command used in switch 2 displays switch 3.
#### Test fail criteria
The test case fails if the `show ip ospf neighbor` command used in switch 2 does not display switch 3.

## Test cases to verify area as NSSA
### Objective

Verify that the NSSA (Not so stubby area) area configuration exists on ABR/ASBR. An NSSA is a type of stub area that can import autonomous system external routes and send them to other areas, but still cannot receive AS-external routes from other areas. NSSA is an extension of the stub area feature that allows the injection of external routes in a limited fashion into the stub area.

A case study simulates an NSSA working around the Stub Area problem of not being able to import external addresses by performing the following activities:

1.	The ASBR imports the external addresses with a type 7 LSA.
2.	The ABR converts the type 7 LSA to type 5 and floods it to other areas.
3.	The ABR acts as an "ASBR" for the other areas.

### Requirements
The requirements for this test case are:
 - One (1) DUT
 - Two (2) switches

### Setup

#### Topology diagram
Area 1 (DUT [ABR], Switch 1)
Area 0 (Switch 2[ASBR])
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                       1                2
                       |                |
                Area 1 |                | Area 0
                       3                4
                 +-----------+    +-----------+
                 |           |    |           |
                 | Switch 1  |    |  Switch 2 |
                 |           |    |           |
                 +-----------+    +-----------+
```
### Verify the area as NSSA
**Test case 8.01**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.

### Description
Configure the area as NSSA by executing these commands on the DUT and the Switch-1 of area 1.
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 1 nssa
```

### Test result criteria
#### Test pass criteria
The test is successful if the following characteristics are present after configuring the area as NSSA:
- No Type 5 LSAs are allowed in Area 1. This can be verified using by checking if there are no any external routes in Switch 1 when Switch 2 redistributes external (static, BGP or connected) routes.
- All external routes are injected into Area 1 as type 7 LSA. This can be verified using `show ip ospf database` to check if there are any NSSA-external LSAs on DUT(ABR) and Switch-1.
- All type 7 LSAs are translated into type 5 LSAs by the NSSA ABR (DUT) and are flooded into erst of the OSPF domain as type 5 LSAs. This can be verified by using `show ip ospf database` on Switch-2 and check all the NSSA-external LSAs (redistribute static, BGP or connected routes) on the DUT are translate to Type-5 external LSAs.
- N/P bit should be set in the Hello packet's option field. This could be verified using tcpdump on either of the DUT's or Switch-1's OSPF enabled interfaces.
- Ping is working on all routes.
- DUT and Switch-1 should have a default route (0.0.0.0) type-3 LSA. This can be verified using `show ip route` command on either DUT or Switch-1.

#### Test fail criteria
The test case fails if following occurs:
- Type 5 LSAs are allowed in Area 1. The test will fail if there is any external LSAs on Switch-1.
- All external routes are not inject to Area 1 as type 7 LSA.
- All type 7 LSAs are not translated into type 5 LSAs by the NSSA ABR (DUT).

### Verify the area as NSSA (Totally stubby)
**Test case 8.02**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.

### Description
Configure the area as NSSA (totally stubby), by executing these commands on the DUT (ABR).
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 nssa no-summary
```

### Test result criteria
#### Test pass criteria
This test is successful if the following characteristics exist after configuring the area as NSSA (totally stubby):
- No type 3 or 4 summary LSAs are allowed in Area 1. This means that inter-area routes depend on the default route alone. This can be verified using `show ip ospf database` command on Switch-1.
- Type 3 LSA in injected into Area 1 as a default route. This can be verified using `show ip ospf database` on switch-1 to check whether there is any default route summary LSA is present.
- N/P bit should be set in the Hello packet's option field. This could be verified using tcpdump on either of the DUT's or Switch-1's OSPF enabled interfaces.
- Ping is working on all routes exc.

#### Test fail criteria
The test case fails if the following occurs:
- Type 3 summary LSAs are allowed in area 1 (except default route).
- The ping does not work.

## Test cases to verify area as Stubby
### Objective
Verify that the OSPF non-backbone area can be configured as a stub. Stub networks have only a single attached router. Packets on a stub network always have either a source or a destination address belonging to that network. That is, all packets are either originated by or destined for a device on the network. The OSPF advertises host routes (with a mask of 255.255.255.255) as stub networks. Loopback interfaces are also considered stub networks and are advertised as host routes. An ASBR that is learning external destinations will advertise those destinations by flooding AS External LSAs throughout the OSPF autonomous system. In many cases, these External LSAs may make up a large percentage of the LSAs in the databases of every router. As in any area, all routers in a stub area must have identical link state databases. To ensure this condition, all stub routers set an E-bit flag in their Hello packets to zero so they will not accept a Hello from a router in which the E-bit is set to one. As a result, adjacencies will not be established with any router that is not configured as a stub router.
### Requirements
The requirements for this test case are:
 - One (1) DUT
 - Two (2) switches

### Setup
#### Topology diagram
Area 1 (DUT [ABR], Switch 1)
Area 0 (Switch 2[ASBR])
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                       1                2
                       |                |
                Area 1 |                | Area 0
                       3                4
                 +-----------+    +-----------+
                 |           |    |           |
                 | Switch 1  |    |  Switch 2 |
                 |           |    |           |
                 +-----------+    +-----------+
```
### Verify an area as stubby
**Test case 9.01**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.

### Description
Configure an area as stub by executing the following commands on the DUT and Switch-1 of area 1.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 stub
```

### Test result criteria
#### Test pass criteria
This test is successful if the following characteristics are present after configuring an area as a stub:
- All external routes are replaced with the default route, which can be verified using `show ip ospf database external` and `show ip ospf database summary` on DUT/Switch-1.
- Adjacency is not possible between a router in stubby area and router in non-stubby area.
- The Hello packets from the STUB network captured on tcpdump must have E-Bit of options flag set to 0.

#### Test fail criteria
The test case fails if the following occurs:
- The external routes are not replaced as the default route.
- Hello packets from the STUB network have E-bit set.

### Verify area as Totally stubby
**Test case 9.02**
#### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.

### Description
Configure an area as Totally stubby by executing these following commands on the DUT (ABR).
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 stub no-summary
```

### Test result criteria
#### Test pass criteria
This test is successful if the following characteristics are present after configuring area as totally stubby:
- All external and inter-area routes are replaced with default routes.
- Adjacency is not possible between a router in a stubby area and a router in a non-stubby area.
- The Hello packets from the STUB network captured on packet capture have the E-Bit of options flag set to 0.

#### Test fail criteria
The test case is a failure if following occurs:
- External and inter-area routes are not replaced with default routes.
- If adjacency is possible between routers in stubby and non-stubby areas.

## Test cases to verify stub router advertisement
### Objective
To verify that the stub router advertisement works, such as maximizing the cost metric of the DUT links. Stub routers do not forward traffic that is not destined for networks directly connected to it. The router becomes a stub router by maximizing the cost metric for the connected links.
### Requirements
The requirements for this test case are:
 - One (1) DUT
 - Two (2) switches

### Setup
#### Topology diagram
Area 1 (DUT, Switch 1, Switch 2)
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                       1                2
                Area 1 |                | Area 1
                       |                |
                       3                4
                 +-----------+    +-----------+
                 |           |    |           |
                 | Switch 1  |    |  Switch 2 |
                 |           |    |           |
                 +-----------+    +-----------+
```
### Verify DUT as a stub router
**Test case 10.01**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- There should be at least one network segment not directly connected to the DUT.

### Description
Configure the DUT as a stub router with the following commands:
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# max-metric router-lsa
```

### Test result criteria
#### Test pass criteria

This test is successful if the metric advertised by the stub-router (DUT) in it's router LSA is maximum (65535). This can be verified using `show ip ospf database router <stub-router-id>` on Switch-1 or Switch-2.

#### Test fail criteria
The test case fails if the metric advertised by the DUT in it's router LSA is value other than 65535.

### Verify DUT as stub router on startup
**Test case 10.02**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- There should be at least one network segment not directly connected to the DUT.

### Description
Configure the router as a stub router on start-up.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# max-metric router-lsa on-startup 3000
```

### Test result criteria
#### Test pass criteria
This test is successful in the following scenario:

For the first 3000 seconds after OSPF startup, the DUT acts as a stub router. After 3000 seconds into the OSPF startup, the switch becomes the normal router. The DUT advertise maximum metric (65535) in it's router LSA for 3000 seconds since OSPF startup and that the DUT advertise normal cost metric, either default 10 or whatever was configured earlier. This can be verified using `show ip ospf database router <stub-router-id>` on Switch-1/Switch-2.


#### Test fail criteria

This test fails if the DUT doesn't advertise maximize metric for 3000 seconds after OSPF startup. The test will also fail if the DUT doesn't advertise normal cost metric after 3000 seconds of OSPF startup.

##  Test cases to verify virtual links
### Objective
The objectives of this test case are:

- To verify that on configuring Virtual link at one end, the status of virtual-neighbor will be shown as down.
- To verify that Virtual link functionality works.

To accomplish this, all areas in an Open Shortest Path First (OSPF) autonomous system must be physically connected to the backbone area (Area 0), but some cases this setup  is not possible. Virtual links are used to connect to the backbone through a non-backbone area. Virtual links can also be used to connect two parts of a partitioned backbone through a non-backbone.


### Requirements
The requirements for this test case are:
 - One (1) DUT with four switches
 - tcpdump tool or packet sniffers.

### Setup
#### Topology Diagram

```ditaa
+---------------+             +---------------+          +---------------+         +-------------+
|               |             |               |          |               |         |             |
|  DUT         1+-------------+1 Switch 1    2+----------+2  Switch 2   1+---------+1   Switch 4 |
|  (Openswitch) |   Area 1    |               |  Area 0  |               | Area 2  |             |
|     2         |             |               |          |               |         |             |
+-----+---------+             +---------------+          +---------------+         +-------------+
      |
      |
      | Area 1
      |
      |
+-----+---------+
|     2         |
| Switch 3      |
|               |
|               |
+---------------+
```
### Verify the virtual link between DUT and remote ABR
**Test case 11.01**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT cannot be part of the backbone area.

### Description
Create a virtual link to remote ABR switch 2 from the DUT and vice versa.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 virtual-link  100.0.1.1
```

Before creating virtual links, the DUT and switch-4 will not form an adjacency. The `show ip ospf neighbor` command in DUT will not show switch-4 as a neighbor.
Configuring a virtual link on the DUT alone will not form an adjacency. The same configurations must be done on Switch-2 also.

### Test result criteria
#### Test pass criteria
- Hello packets are sent as unicast packets in virtual links. This can be verified using the packet capture tools.
- The DUT and Switch-1 form a neighbor relation. Verify this by displaying the `show ip ospf neighbor` command output.
- Switch-2 and Switch-4 should show the DUT and Switch-3 routes and the ping works on all routes. Verify this by displaying the `show ip ospf routes` command output.

#### Test fail criteria

The test case fails in the following instances:
- If an adjacency exists between the DUT and Switch-1 before creating a virtual link.
- If an adjacency is not established after creating virtual links on both switches.

### Verify virtual link authentication
**Test case 11.02**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT is not part of the backbone area.
- Virtual link is created between the DUT and switch-2.

### Description
Configure virtual link authentication.
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 1 virtual-link  100.0.1.1 message-digest-key  1 md5 openswitch
switch(config-router)# area 1 virtual-link  100.0.1.1 authentication message-digest
```

### Test result criteria
#### Test pass criteria
After configuring authentications, the OSPF packet header authentication field shows MD5 authentication. Verify this using the packet capture tools.

#### Test fail criteria
 This test case fails if the OSPF header in the packet sent in the virtual link does not contain the configured authentication field.

### Verify hello-interval, retransmit-interval, transmit-delay and dead-interval for virtual links
**Test case 11.03**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT is not part of the backbone area.
- Virtual link is created between the DUT and switch-2.

### Description
Configure the following for virtual links:
- hello-interval
- retransmit-interval
- transmit-delay
- dead-interval
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 virtual-link  100.0.1.1 hello-interval 30
switch(config-router)# area 1 virtual-link  100.0.1.1 retransmit-interval 30
switch(config-router)# area 1 virtual-link  100.0.1.1 transmit-delay 30
switch(config-router)# area 1 virtual-link  100.0.1.1 dead-interval 30
```

### Test result criteria
#### Test pass criteria
Configure different hello and dead intervals on a DUT and remoter ABR. This results  in the hello packets being dropped. Hello and dead intervals need to be same for both the DUT and the peer ABR (Switch-1).

#### Test fail criteria
the test case fails if the hello packets are sent and an adjacency is formed even when different hello and dead intervals are set on the DUT and switch-2.

### Verify deleting virtual links
**Test case 11.04**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT is not part of backbone area.
- Virtual link is created between the DUT and switch-2.

### Description
Delete virtual links with the remote ABR.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# no area 1 virtual-link  100.0.1.1
```

### Test result criteria
#### Test pass criteria
This test is successful if the adjacency ceases after deleting the virtual link between the DUT and switch-2.

#### Test fail criteria
This test fails if the adjacency persists between the DUT and Switch-2 even after deleting the virtual link.

### Verify virtual links on a stubby and a totally stubby area
**Test case 11.05**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT is not part of backbone area.
- Virtual link is created between the DUT and switch-2.

### Description
Confirm that configuring virtual links on a stubby and a totally stubby area does not work.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 stub
switch(config-router)# area 1 virtual-link  100.0.1.1
```
### Test result criteria
#### Test pass criteria
This test is successful if configuring virtual links on a stubby and a totally stubby area displays an error.

#### Test fail criteria
This test fails if configuring virtual links on a stubby and a totally stubby area succeeds.

### Verify virtual links on a passive interface
**Test case 11.06**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- The DUT is not part of the backbone area.
- Virtual link is created between the DUT and switch-2.

### Description
Configure an interface in which virtual links are configured as a passive interface using the `passive-interface <interface>` command in router ospf context.

```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# passive-interface 1
switch(config-router)# area 1 virtual-link  100.0.1.1
```

### Test result criteria
#### Test pass criteria
Configuring a passive interface on the virtual links breaks the adjacency. The `show ip ospf neighbor` command on switch 2 will not display switch 1.

#### Test fail criteria
This test fai8ls if the adjacency between switch 1 and switch 2 still exists.

## Test cases to verify SPF throttling
### Objective
To verify the OSPFv2 Shortest Path First (SPF) throttling functionality. The OSPF throttling feature makes it possible to configure SPF scheduling in a time interval of seconds and to potentially delay the SPF calculations during network instability. The SPF is scheduled to calculate the Shortest Path Tree (SPT) when there is a change in topology. One SPF run may include multiple topology change events. The current SPF interval is calculated and is twice as long as the previous interval until the value reaches the maximum wait time specified.
### Requirements
The requirements for this test case are:
 - One (1) DUT (ABR)
 - Three switches

### Setup
#### Topology diagram
Area 0 (Switch 3, DUT)
Area 1 (Switch 2, DUT)
Area 2 (Switch 1, DUT)
```ditaa
  +----------+           +------------------------------+          +-------------+
  |          | 1       2 |                              |          |             |
  | Switch 3 +-----------+             DUT              |3        4|   Switch 2  |
  |          |   Area 0  |         (OpenSwitch)         +----------+             |
  |          |           |                              |  Area 1  |             |
  +----------+           +------------------------------+          +-------------+
                                       1
                                       | Area 2
                                       |
                                       3
                                 +-----------+
                                 |           |
                                 | Switch 1  |
                                 |           |
                                 +-----------+
```
### Test case 12.01 : Verify SPF throttling parameters
**Test case 12.01**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- Adjacency should be established between routers and topology is stable unless changed manually.

### Description
Configure the SPF throttling parameters
Set the SPF throttling parameters on the DUT as follows:
- Delay=100 milliseconds
- Initial hold time=100000 milliseconds
- Max hold time=300000 milliseconds

```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# timers throttle spf 100 100000 300000
```

Do a topology change manually such as deleting a DUT link for verifying the SPF timers effect.
### Test result criteria
#### Test pass criteria
- Verify that the SPF timers are set properly by displaying the `show ip ospf` command output.
- Verify that SPF is run at the interval of 100 secs. This can be verified in the logs. The adjacency formed should remain intact, and can be verified by displaying the `show ip ospf neighbor` command output. Again, run the SPF at 200 secs (previous 100 sec x 2).

#### Test fail criteria
Test cases fail if the SPF is not calculated within the configured values.

## Test cases to verify OSPFv2 area network filtering
### Objective
To verify the OSPF area network filtering functionality. Filtering Type-3 summary-LSAs to and from the area using the prefix lists. Run these test cases in ABR only.
### Requirements
The requirements for this test case are:
 - One (1) DUT (ABR)
 - Two switches

### Setup
#### Topology Diagram
Area 1 (Switch 1, DUT)
Area 0 (Switch 2, DUT)
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                       1                2
                       | Area 1         | Area 0
                       |                |
                       3                4
                 +-----------+    +-----------+
                 |           |    |           |
                 | Switch 1  |    |  Switch 2 |
                 |           |    |           |
                 +-----------+    +-----------+
```
### Verify filtering type-3 LSA into the area as per a preconfigured prefix list
**Test case 13.01**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- Adjacency is established between routers.
- Prefix filter list is already configured for both ingress and egress.

### Description

The DUT advertises the OSPFv2 routes it learned from Switch 1 in type 3 LSAs. To advertize DUT routes:

1. Configure 10.10.10.0/24 and 10.10.20.0/24 networks in Switch 1.
2. Enable summarization in the DUT using the command `area (<area_ip>|<area_id>) range <ipv4_address>` in router ospf context. So the routes learned from Switch 1 will be summarized and advertised in the DUT.
3. Configure the area to filter type-3 LSAs into the area as per a preconfigured prefix list. The filter list prefix (10.10.0.0/16) is already configured with the list name *list1*. These commands filter any type-3 LSA matching prefix 10.10.0.0/16 and keep them from entering area 1, as the DUT is an ABR.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 filter-list list1 in
switch(config-router)# area 1 range 10.10.0.0
```

### Test result criteria
#### Test pass criteria
This test is successful if the type-3 LSAs matching the 10.10.0.0/16 prefix is filtered out and cannot enter area 1. Display the `show ip ospf database` command output executed on Switch-1 to verify.

#### Test fail criteria
This test fails if any LSA matching 10.10.0.0/16 prefix enters area 1.

### Verify filtering type-3 LSA out of the area as per a preconfigured prefix list
**Test case 12.02**
### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- Adjacency is established between routers.
- Prefix filter list is already configured for both ingress and egress.

### Description

The DUT advertises the OSPFv2 routes it learned from Switch 1 in type 3 LSAs. To advertize DUT routes:

1. Configure 10.10.10.0/24 and 10.10.20.0/24 networks in Switch 1.
2. Enable a summarization in DUT using the `area (<area_ip>|<area_id>) range <ipv4_address>` command in router ospf context. So the routes learned from Switch 1 will be summarized and advertised in the DUT.
3. Configure the area to filter type-3 LSAs out of the area as per a preconfigured prefix list. The filter list prefix (100.10.0.0/16) is already configured with the list name *list1*. These commands (executed on DUT) filter any type-3 LSA matching prefix 100.10.0.0/16 from going out of the area 1, as the DUT is an ABR.
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# area 1 filter-list list1 out
```

### Test result criteria
#### Test pass criteria
Verify that the type-3 LSAs matching 100.10.0.0/16 prefix is filtered out from entering area 0 using the `show ip ospf database` command output, executed on switch-2.

#### Test fail criteria
This test fails if any type-3 LSA matching 100.10.0.0/16 prefix enters area 0.

## Test cases to verify the best route selection by GNU Zebra
### Objective
To verify that the best route is always selected for routing, when multiple protocols have routes to the same network segment. When multiple protocols (including static routes) have routes to the same network segment, then the GNU Zebra ensures that  the best route is always selected depending on the distance. The lower the distance, the increased chance  there is for the route to be selected.
### Requirements
The requirements for this test case are:
 - One (1) DUT
 - One (1) switches

### Setup
#### Topology diagram
Area 1 (Switch 1, DUT)
```ditaa
                +------------------------------+
                |                              |
                |              DUT             |
                |         (OpenSwitch)         |
                |                              |
                +------------------------------+
                               1
                               | Area 1
                               |
                               2
                       +---------------+
                       |               |
                       |   Switch 1    |
                       |               |
                       +---------------+
```
### Verify best route selection by GNU Zebra
**Test case 13.01**
#### Precondition
- OSPF areas are created.
- All interfaces belonging to the OSPF areas are active.
- Adjacency is established between routers and Switch-1 is configured for network 10.10.10.0/24.
- OSPF route for network 10.10.10.0/24 network is installed.

### Description
Configure the OSPF distance and add the static route for network 10.10.10.0/24 (executed on DUT).
```
switch# configure terminal
switch(config)# router ospf
switch(config-router)# distance 90
switch(config-router)# exit
switch(config)# ip route 10.10.10.0/24 1 100
switch(config)#
```
The static route is added for interface 1 on the DUT with a distance of 100. Redistribute either connected or static route from Switch-1.
### Test result criteria
#### Test pass criteria
Verify that the OSPF route is selected for routing by displaying the `show rib` command output. The selected route for network 10.10.10.0/24 will the route entry that is prefixed with symbol `*` which in this case would be the OSPF route. Following is the example of route entry:
```
*10.10.10.0/24,  1 unicast next-hops
	*via  10.10.10.2,  [90/20],  ospf
10.10.10.0/24,  1 unicast next-hops
	*via  1,  [100/0],  static
```

#### Test fail criteria
The test fails if the static route is selected instead of the OSPF route.


## Test cases to verify OSPFv2 performance
### Objective
Verify the perfomance of the ospfd daemon.

### Requirements
The requirements for this test case are:
 - One (1) DUT
 - Nine (9) switches

### Setup

#### Topology diagram

```ditaa

+---------------+             +---------------+          +---------------+         +-------------+
|               |             |               |          |               |         |             |
|  DUT         1+-------------+1 Switch 1    2+----------+2  Switch 2   1+---------+1   Switch 4 |
|  (Openswitch) |   Area 1    |               |  Area 0  |               | Area 2  |             |
|     2         |             |               |          |               |         |             |
+-----+---------+             +---------------+          +---------------+         +----------+--+
      |                                                                                       |
      |                                                                                       |
      | Area 1                                                                                |
      |                                                                                       |Area 2
      |                                                                                       |
+-----+---------+          +---------------+        +---------------+    +---------------+    |
|     2         |  Area 1  |               |        |               |    |               |    |
| Switch 3    1 +----------+1 Switch 5     |        |  Switch 6    2+----+1 Switch 7    2+----+
|               |          |               |        |               |    |               |
|      3        |          |               |        |               |    |       3       |
+------+--------+          +---------------+        +---------------+    +-------+-------+
       |                                                            Area 2       |
       |                                                                         |
       |Area 1                                                                   | Area 2
       |                                                                         |
+------+--------+                                                        +-------+-------+
|      3        |                                                        |       3       |
|1 Switch 9    2|                                                        |1 Switch 8    2|
|               |                                                        |               |
|      4        |                                                        |       4       |
+---------------+                                                        +---------------+
       |                                                                         |
       |                                                                         |
       |                                                                         |
       |                                                                         |
+------+--------+                                                        +-------+-------+
|      1        |                                                        |       1       |
|  Host 1       |                                                        |    Host 2     |
|               |                                                        |               |
|               |                                                        |               |
+---------------+                                                        +---------------+


```
### Verifying the performance of OSPFv2
**Test case 14.01**
### Precondition
 - The `ospfd` daemon is running.
 - The areas are configured as shown in the topology

### Description
- The ospfd daemon is running in all the switches and is able to learn and advertise the routes.
- The adjacency is formed
- The host 1 is able to ping host 2 without significant delay.(Delay range: TBD)

The following values are to be decided after preliminary analysis and benchmarking:
- Maximum number of OSPFv2 routes learnt.
- Maximum number of interfaces on which OSPFv2 can be enabled and still maintain adjacency.
- Maximum number of routes redistributed by OSPFv2.
- Convergence time for maximum adjacency supported.
- Traffic outage interval when there is topological change in the network.

### Test result criteria
#### Test pass criteria
The test case is successful if the `ps` command lists the PID of `ospfd` daemon and `show ip ospg neighbor` command displays the neighbors when the OSPFv2 is enabled on maximum number of interfaces and is pumped with maximum number of routes.

#### Test fail criteria
The test case fails if the `ospfd` daemon is not listed in the `ps` command or the `show ip ospg neighbor` command does not display the neighbors when the OSPFv2 is enabled on maximum number of interfaces and is pumped with maximum number of routes.

## Future extensions
The testcases for following categories will be added once they are supported:
- OSPFv2 support in LAG ports.
- OSPFv2 running on loopback interface.
- OSPFv2 support for jumbo frames.
- OSPFv2 daemon restartability
- OSPFv2 NBMA support
