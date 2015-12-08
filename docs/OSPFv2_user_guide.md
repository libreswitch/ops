# OSPFv2

## Table of contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [List of abbreviations](#list-of-abbreviations)
- [How to use the feature](#how-to-use-the-feature)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Setting up the optional configuration](#setting-up-the-optional-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
	- [Troubleshooting the configuration](#troubleshooting-the-configuration)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
OSPFv2 is an interior gateway protocol (IGP) that routes packets within a single autonomous system (AS). OSPFv2 uses link-state information to make routing decisions and route calculations using the Dijkstra's shortest-path-first (SPF) algorithm. Each router runs the OSPFv2 floods link-state advertisements throughout the AS or area that contains information about that router’s attached interfaces and routing metrics. Each router uses the information in these link-state advertisements to calculate the least cost path to each network and populates the routing information base for the router.

## Prerequisites

User must be familiar with OSPFv2 fundamentals and have the following set up:
- Access to the switch and be logged in.
- Configured at least one interface for IPv4 that can communicate with peering OSPFv2 router.
- Enabled IPv4 routing feature.

## List of abbreviations
|Abbreviation   | Expansion   |
|---|---|
|  BDR | Backup Designated Router  |
|  DR | Designated Router  |
|  OSPF |  Open Shortest Path First |
|  SPF | Shortest Path First  |

## How to use the feature
### Setting up the basic configuration
**1. Enabling OSPFv2**
** Creating an OSPFV2 instance**
    Create the OSPFv2 instance using the command `router ospf` in configuration context. When a router instance is created it is enabled by default.

** Configuring OSPFv2 network for an area**
	Specify the OSPFv2 enabled interface(s) using the command `network <network_prefix> area (<area_ip>|<area_id>)` in router ospf context. If any interfaces has a primary IPv4 address enabled on the subnetwork which is matching to the "network" or subset of the "network", then those will participate in the OSPFv2. i.e., OSPFv2 protocol will be enabled on those interfaces.

**2. Configuring router id**
	Configure router id using the command, `router-id <A.B.C.D>` in router ospf context. If the router id is not configured then the dynamic router id provided by the routing manager daemon i.e. zebra will be used.


### Setting up the optional configuration

**1. Configuring OSPFv2 authentication**
** Configuring authentication for an area**
	Configure authentication for all networks in an area using `area  (<area_ip>|<area_id>) authentication [message-digest]` command in router ospf context and `ip ospf authentication-key <key>` and `ip ospf message-digest-key <key_id> md5 <message_digest_key>` command in the interface context.

** Configuring authentication for an interface**
	Configure authentication for individual interfaces using `ip ospf authentication {message-digest}`, `ip ospf authentication-key <key>` and `ip ospf message-digest-key <key_id> md5 <message_digest_key>` command in the interface context.

** Configuring authentication for virtual links**
	The authentication type for the virtual link can be configured using the command `area (<area_ip>|<area_id>) virtual-link <remote_address> {authentication (message-digest|
null)}` in router ospf context.

**2. Configuring OSPFv2 interface parameters**
** Modifying the default timers**
	Modify the default value of the timers such as dead interval, hello interval, and retransmit interval by using the following commands in the interface context:
    - Dead interval: `ip ospf dead-interval <dead_interval>`
    - Hello interval: `ip ospf hello-interval <hello_interval>`
    - retransmit interval: `ip ospf retransmit-interval <retransmit_interval>`

** Configuring OSPFv2 priority **
	Configure the OSPFv2 priority for the interface using the `ip ospf priority <priority_value>` command in the interface context.

** Configuring OSPFv2 network type **
	Configure the OSPFv2 network type for the interface using the `ip ospf network (broadcast|point-to-point)` command in the interface context.

** Configuring interface cost **
	Configure the interface cost using the `ip ospf cost <interface_cost>` command in the interface context.

**3. Configuring OSPFv2 area **

** Configuring route summarizations**
	Summarize the routes matching address/mask using the `area (<area_ip>|<area_id>) range <ipv4_address> {cost <range_cost> | not-advertise}` command in the router ospf context.

** Configuring virtual links**
	The virtual link can be configured using the command `area (<area_ip>|<area_id>) virtual-link <remote_address>` in router ospf context.

** Configuring NSSA**
	Configure an area as not so stubby using the `area (<area_ip>|<area_id>) nssa {translate-candidate|translate-never|translate-always} [no-summary]` command in the router ospf context.

** Configuring stub areas**
	Use the `area (<area_ip>|<area_id>) stub` command in the router ospf context to set the area type as stub.

** Configuring totally stubby areas**
	Use the `area (<area_ip>|<area_id>) stub [no_summary]` command in the router ospf context to set the area type as a totally stubby area and prevent all summary route updates from going into the stub area.

** Configuring filter lists for border routers**
	Filter networks between OSPFv2 areas using the `area (<area_ip>|<area_id>) filter-list <list-name> (in|out)` command in the router ospf context. The filtering is done as per the prefix lists. Only use this command on area border routers.

**4. Redistributing routes into OSPFv2**
	Redistirbute routes originating from other protocols into OSPFv2 by using the `redistribute {bgp | connected | static}` command. The `default-metric <metric_value>` command in OSPFv2 router context sets the default metric to be used for redistributed routes.

**5. Configuring passive interface**
	An interface can be configured as passive interface using the `passive-interface <interface>` command in the router ospf context. To configure all the OSPFv2 enabled interfaces as passive, use the `passive-interface default` command in the router ospf context.

**6. Configuring NBMA neighbor**
	Configure NBMA neighbor address, poll interval and priority value using the `neighbor <neighbor_ip> {poll-interval <poll_value> | priority <priority_value>}` command in the router ospf context

For more OSPFv2 configurations refer to the [OSPFv2 command reference document](/documents/user/OSPFv2_cli).

### Verifying the configuration

 1. Verify the configured values and area related information using the `show ip ospf` command.
 2. For the interfaces related information and neighbors related information use `show ip ospf interface` and `show ip neighbor detail` commands respectively.
 3. The `show ip ospf database {asbr-summary|external|network|router|summary|nssa-external|opaque-link|opaque-area|opaque-as|max-age} [<lsa_id>] {self-originate | adv-router <router_id>}` command shows the OSPFv2 link state database summary.
 4. The OSPFv2 routing table can be verified using the `show ip ospf route` command.
 5. The configurations can be verified using the command `show running-config` or `show running-config router ospf`.
 An example of the `show running-config router ospf` command follows:
 ```
 Switch#show running-config router ospf
 !
 router ospf
     router-id 1.1.1.1
     network 10.0.0.0/24 area 100
     area  100 default-cost 2
     area 100 filter-list list2 out
	 area 100 virtual-link  100.0.1.1
     area 100 virtual-link  100.0.1.1 hello-interval 30
     area 100 virtual-link  100.0.1.1 retransmit-interval 30
```
 For more OSPFv2 configurations refer to the [OSPFv2 command reference document](/documents/user/OSPFv2_cli).

### Troubleshooting the configuration
The location of log files used to troubleshoot depends on the platform on which the OSPFv2 is running. For physical switch the logging is handled by VLOG and the log files are store at /var/log/messages. For simulated environment the log files are stored at /var/log/syslog/ of the virtual machine running the simulated image. Therefore it is generically mentioned as log files in the following scenarios.

#### Scenario 1
##### Condition
The OSPFv2 packets are not reaching the daemon.

##### Cause
1.  The user has not configured the router id in the router ospf context. This can be verified using the `show ip ospf` command. Furthermore, `ospfd` has not received a system global router-id.
2. OSPFv2 is not configured for any network. If this is the case, then `show ip ospf interface` command will not display any entry.
3. No interfaces have IPv4 address matching to any of the OSPFv2 enabled "networks". In this case the `show ip ospf interface` command will not display any entry.

##### Remedy
- The `show ip ospf` command output will display the configured router id value (if configured). If no router id value is displayed, then configure the router id using the command `router <router-id>` in the router ospf context.
- If `show ip ospf interface` is not displaying any entry or there is no entry matching the configured network range then configure proper network range using the command `network <network_prefix> area (<area_ip>|<area_id>)` in router ospf context.

#### Scenario 2
##### Condition
The neighbors are not discovered.

##### Cause
- The interface is passive. The `show ip ospf interface` command will display that interface is passive.
- The neighbors are not reachable. Check the reachability of the network using the ping command.

##### Remedy
- If the interface has been configured as passive, check if the configuration/ topology is correct.
- If network is not reachable then configure the required routes and default gateway to make the switches reachable.
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility such as `tcpdump` as an example.
- Check the log file for error messages.

#### Scenario 3
##### Condition
Neighbors are reachable but the adjacency is not formed.

##### Cause
- Area types are not matching. Check the area type using `show ip ospf interface` command.
- Peer's subnet and subnet mask are not matching for the connected interfaces. Check the interface value using `show ip ospf interface` command.
- Duplicate Router-id. Check the router id using `show ip ospf` command.

- DR Priority 0 for both the routers. Check the priority value using `show ip ospf interface` command.
- The authentication type or key is not matching. Check the log file for error messages for any authentication related failure.
- The neighbors are not in the same area. Check the area id using `show ip ospf` command.

The following causes can be verified using `show ip ospf interface` command:

- The timer intervals like hello interval or dead interval are not matching.
- MTU value is not matching and "mtu ignore" is not configured.
- Interface type mismatch.
- Duplicate interface IPv4 addresses.

##### Remedy
- If the log file contains any authentication related failure, then configure appropriate authentication method and keys using the command `ip ospf authentication {message-digest}` and `ip ospf authentication-key <key>` in the interface context.
- If any timer values are mismatching then configure appropriate timer values using the command `ip ospf {dead-interval <dead_interval> } | {hello-interval <hello_interval>} | mtu-ignore` in the interface context.
- If prirotiy is 0, configure proper priority values using the command `ip ospf priority <priority_value>` in the interface context.
- If areas are not matching then configure proper areas using the command `network <network_prefix> area (<area_ip>|<area_id>)` in router ospf context.
- If area type is mismatching then configure proper area type using `area (<area_ip>|<area_id>) nssa {translate-candidate|translate-never|translate-always} [no-summary]` command in router ospf context.
- For mismatching network types, configure matching network types using the command `ip ospf network (broadcast|point-to-point)` in the interface context.

If none of the above remedy works then
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility such as `tcpdump` as an example. If the packets are corrupted then there is a bug in the software.
- Check the log file for error messages.

#### Scenario 4
##### Condition
Neighbors are reachable. Adjacency is formed in some of the switches and not in others.

##### Cause
- The `show ip ospf neighbor` command displays some neighbors with states other than "full" state. On broadcast media and non-broadcast multiaccess networks, a router becomes full only with the designated router (DR) and the backup designated router (BDR); it stays in the 2-way state with all other neighbors.

##### Remedy
- If the state is "init", this implies that the local router is able to see the OSPFv2 hello from neighbors. But the neighbor has not seen OSPFv2 hello from local router. Check the reachability on both the sides using the ping command.
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility such as `tcpdump` as an example.
- Check if the configurations listed in "Setting up the basic configuration" are correct and valid.
- Check if any other configurations that were modified are valid. The `show running-config router ospf` command will list all the configurations made.

#### Scenario 5
##### Condition
No DR or BDR is seen in the network.

##### Cause
- If the priority is zero on all the OSPFv2 routers, then none of the routers are selected as DR or BDR. The `show ip osppf neighbor` command lists the neighbors and their priorities.

##### Remedy
- Configure any non-zero value as priority using the command `ip ospf priority <priority_value>` in the interface context.

#### Scenario 6
##### Condition
Routes are not being learnt or advertised.

##### Cause
- Adjacencies are not formed (neighbor fsm is not in "full" state). This can be verified using the `show ip ospf neighbor` command.
- No corresponding LSAs are present. The `show ip osppf database` command lists the LSA.

##### Remedy
- If the adjacencies are not formed then try the remedies listed in scenario "Neighbors are reachable but the adjacency is not formed" and "The neighbors are not discovered".
- Capture and validate the OSPFv2 protocol packets using any supported compatible packet capture utility such as `tcpdump` as an example.

#### Scenario 7
##### Condition
SPF algorithm is getting executed many times. This can be seen from the `show ip ospf` command.

##### Cause
- Links are flapping in the network. The change in the topology can be verified using the `show ip ospf database router` command.
- The SPF minimum hold time or maximum hold time is less. The SPF timer related configurations can be verified using `show ip ospf` command.

##### Remedy
- Go to each switch and check the interfaces using `show interface` command to identify the flapping link.
- Fine tune the SPF timer related configurations using `timers throttle spf <spf_delay_time> <spf_hold_time> <spf_maximum_time>` command in router ospf context.

#### Scenario 8
##### Condition
SPF algorithm is not getting executed. This can be seen from the `show ip ospf` command.

##### Cause
- The SPF minimum hold time or maximum hold time is set to very large values. The SPF timer related configurations can be verified using `show ip ospf` command.

##### Remedy
- Fine tune the SPF timer related configurations using `timers throttle spf <spf_delay_time> <spf_hold_time> <spf_maximum_time>` command in router ospf context.

## CLI
Click [here](/documents/user/OSPFv2_cli) for the CLI commands related to the OSPFv2 feature.

## Related features
None.
