# BGP

##Contents
   - [Overview](#overview)
   - [Setting up the basic configuration](#setting-up-the-basic-configuration)
   - [Setting up the optional configuration](#setting-up-the-optional-configuration)
   - [Verifying the configuration](#verifying-the-configuration)
   - [Troubleshooting the configuration](#troubleshooting-the-configuration)

## Overview
The Border Gateway Protocol (BGP) is the most commonly used as an **inter-AS** (autonomous system) routing protocol. The latest BGP version is 4. **BGP-4** supports Classless Inter-Domain Routing (CIDR). The BGP advertises the routes based on destinations as an IP prefix and not the network "class" within BGP.

BGP is a **path-vector** protocol that provides routing information across various BGP routers to be exchanged using destination-based forwarding. For example, the router sends packets based merely on the destination IP address carried in the IP header of the packet. In most cases, there are multiple routes to the same destination, BGP decides which route to choose using the path attributes, such as *Shortest AS_Path, Multi_Exit_Disc (Multi-exit discriminator, or MED), Origin, Next_hop, Local_pref,* and so on.

BGP provides routing for routers or switches or both, that can be deployed in ISP, Enterprise, and data center environments.

## Setting up the basic configuration
The following is the minimum configuration needed to set up the BGP router. The AS number is unique to the autonomous system, and is used to distinguish between internal, external, or both BGP connections. Enter the following commands in the order shown:

 1. The `router bgp <asn>` command enables the BGP router for the AS number. The AS number ranges from 1 to 65535.
 2. The `bgp router-id A.B.C.D` command sets the BGP router-id.

The BGP router can be disabled with the `no bgp router-id A.B.C.D` or `no bgp router-id` commands. The commands default the router-id to 0.0.0.0.

  Note: The `no router bgp <asn>` command disables the BGP process with the given AS number.

## Setting up the optional configuration
To set up the optional configuration:

- Enter the router bgp command with the required AS number. For example:
  `router bgp <asn>`
  The `router bgp <asn>` command enables the BGP router for the AS number. The AS numbers range from 1 to 65535.

- Set the BGP router id with the following command:
  `bgp router-id <A.B.C.D>`
  The BGP router can be disabled with the `no bgp router-id A.B.C.D` or `no bgp router-id` commands. The commands default the router-id to 0.0.0.0.

- Set up the maximum-paths with the following commands:
  `router bgp <asn>`, `maximum-paths <paths>`
  The maximum-paths command limits the maximum number of paths for BGP. If global ECMP is enabled, and BGP maximum-paths is set greater than the global maximum-paths, then the global setting overrides BGP maximum-paths. If global ECMP is disabled, then only single best path gets selected. BGP multiple-paths carries risks of routing oscillations if MED, IGP costs, and the BGP and IGP topologies are not cautiously considered. Since community and extended community are the aggregated attributes of the multi-path routes within AS path, BGP multi-pathing results in the propagated route having the attributes of the "best route" of the multi-path.
  The `no maximum-paths` defaults the number of maximum paths to 1.

- Set up timers with the following commands:
  `router bgp <asn>`, `timers bgp <keepalive> <holdtimer>`
  The `timers bgp <keepalive> <holdtimer>` command sets the keepalive interval and hold time for the BGP router.
  Timers can be set to default with the `no timers bgp <keepalive> <holdtimer>` command. The default keepalive interval is 180 seconds, and the default hold time is 60 seconds.

- To add a static network to the BGP routing table, enter the following commands:
  `router bgp <asn>`, `network <A.B.C.D/M>`
  It announces the specified network to all peers in the AS. The `no network <A.B.C.D/M>` command removes the announced network for this BGP router.

- Use the following commands to advertise the IPv6 prefix network:
  `router bgp <asn>`, `network <X:X::X:X/M>`
  Use this command in router configuration mode to advertise the specified prefix into the IPv6 BGP database.
  Use the `no network <X:X::X:X/M>` command to stop advertising the specified prefix into the IPv6 BGP database.

- Use the following commands to enable fast external failover for BGP directly connected peering sessions:
  `router bgp <asn>`, `bgp fast-external-failover`
  Use this command in router configuration mode to terminate external BGP sessions of any directly adjacent peer if the link used to reach the peer goes down, without waiting for the hold-down timer to expire.
  Use the `no bgp fast-external-failover` command to disable the BGP fast external failover.

- Use the following commands to enable logging of BGP neighbor status changes:
  `router bgp <asn>`, `bgp log-neighbor-changes`
  Use this command in router configuration mode to log changes in the status of BGP neighbors (up, down, reset).
  Use the `no bgp log-neighbor-changes` command to disallow log changes in the status of BGP neighbors.

- Enter the following neighbor configuration commands in the order shown:

 - Use the following commands to define a new peer with remote-as, where the asn and peer parameters are IPv4 addresses:
   `router bgp <asn>`, `neighbor <peer> remote-as <asn>`
   If remote-as is not configured, *bgpd* displays the error `can’t find neighbor peer`.
  The `no neighbor <peer>` command deletes the peer.

 - Set up the peer description with the following commands:
   `router bgp <asn>`, `neighbor <peer> description <some_description>`
   The `no  neighbor <peer> description` command deletes the neighbor description.

 - Enable MD5 authentication on a TCP connection between BGP peers with the following command:
   `router bgp <asn>`, `neighbor <peer> password <some_password>`
   The `no neighbor <peer> password <some_password>` command disables MD5 authentication on a TCP connection between BGP peers.

 - Set up the keepalive interval or hold time for a peer with the following commands:
   `router bgp <asn>`, `neighbor peer timers <keepalive> <holdtimer>`
   The `no neighbor peer timers <keepalive> <holdtimer>` command clears the keepalive interval and hold time for that peer.

 - Specify the number of times BGP allows an instance of AS to be in the AS path using the following commands:
   `router bgp <asn>`, `neighbor peer allowas-in <ASN_instances_allowed>`
   The ASN_instances_allowed range is from 1 to 10.
   The `no neighbor peer allowas-in <ASN_instances_allowed>` command prevents the AS number from being added to the AS path by setting the ASN_instances_allowed parameter to 0.

 - Remove private AS numbers from the AS path in outbound routing updates with the following commands:
   `router bgp <asn>`, `neighbor peer remove-private-AS`
   The `no neighbor peer remove-private-AS` command allows private AS numbers from the AS path in outbound routing updates.

 - Enable software-based reconfiguration to generate inbound updates from a neighbor without clearing the BGP session with the following commands:
  `router bgp <asn>`, `neighbor peer soft-reconfiguration inbound`
   The `no neighbor peer soft-reconfiguration inbound` command disables the software-based reconfiguration.

 - Set the advertisement interval for route updates for a specified neighbor or peer with an IPv4 or IPv6 address with the following commands:
   `router bgp <asn>`, `neighbor peer advertisement-interval <interval>`
   The time interval for sending BGP routing updates is in the range of 0 to 600 seconds. The default value is 30 seconds.
   The `no neighbor peer advertisement-interval <interval>` command unsets the advertisement interval for route updates for the specified neighbor or peer with an IPv4 or IPv6 address.

 - Configure a filter list on a neighbor to filter incoming and outgoing routes using the following commands:
   `router bgp <asn>`, `neighbor (A.B.C.D|X:X::X:X|WORD) filter-list WORD (in|out)`
   The `no neighbor (A.B.C.D|X:X::X:X|WORD) filter-list WORD (in|out)` command uninstalls the filter list.

 - Apply a prefix list on a neighbor to filter updates to and from the neighbor using the following command:
   `router bgp <asn>`, `neighbor (A.B.C.D|X:X::X:X|WORD) prefix-list WORD (in|out)`
   The `no neighbor (A.B.C.D|X:X::X:X|WORD) prefix-list WORD (in|out)` command uninstalls the applied prefix list.

 - Allow inbound soft reconfiguration for a neighbor using the following commands:
   `router bgp <asn>`, `neighbor (A.B.C.D|X:X::X:X|WORD) soft-reconfiguration inbound`
   The `no neighbor (A.B.C.D|X:X::X:X|WORD) soft-reconfiguration inbound` command disables the inbound soft reconfiguration.

 - Specify the maximum number of hops to the BGP peer using the following commands:
   `router bgp <asn>`, `neighbor (A.B.C.D|X:X::X:X|WORD) ttl-security hops <1-254>`
   The `no neighbor (A.B.C.D|X:X::X:X|WORD) ttl-security hops <1-254>` command disables the maximum number of hops specification.

- The peer-group is a collection of peers that share the same outbound policy. Neighbors belonging to the same peer-group might have different inbound policies. All peer commands are applicable to the peer-group as well. Following are the peer-group configuration commands.
  Enter the following BGP peer-group commands in the order shown:

 - Define a new peer-group with the < word > variable as the name of the peer-group using the following commands:
  `router bgp <asn>`, `neighbor <word> peer-group`
   The `neighbor <word> peer-group` command deletes the peer-group.

 - Bind a specific peer to the provided peer-group with the following commands:
   `router bgp <asn>`, `neighbor peer peer-group word`

- Following are the route map configuration commands:

 - Configure peer filtering of a given sequence number for a route map with the following command:
   `route-map <word> (deny|permit) <sequence_num>`
   The word variable is the name of the route map, and the sequence_num variable is an integer in the range from 1 to 65535.
   The `no route-map <word> (deny|permit) <sequence_num>` command deletes the route map. All route map commands should be executed under the `route-map <word> (deny|permit) <sequence_num>` context.

 - Assign a route map to the peer with the given direction using the following commands:
   `route-map <word> (deny|permit) <sequence_num>`, `neighbor <peer> route-map <word> in|out`
   The `no neighbor <peer> route-map <word> in|out` command removes the route map from the peer.

 - Add a route map description with the following command:
   `route-map <word> (deny|permit) <sequence_num>`, `description <some_route_map_description>`

 - Assign or change the community for a route map with the following command:
   `route-map <word> (deny|permit) <sequence_num>`, `set community .AA:NN additive`
   The `no set community .AA:NN additive` command removes the community.

 - Set or change the metric for a route map with the following command:
   `route-map <word> (deny|permit) <sequence_num>`, `set metric <0-4294967295>`
   This command can be used to overwrite a previously set metric.
   The `no set metric <0-4294967295>` command resets the metric to 0.

 - Set the metric value for the route, which is used with BGP route advertisement, using the following commands:
   `route-map <word> (deny|permit) <sequence_num>`, `set metric <value>`
   The value attribute is in the range 0 - 4294967295.
   The `no set metric <value>` command resets the metric for the route to 0.

 - To match an IP address prefix list, use the following commands:
   `route-map <word> (deny|permit) <sequence_num>`, `match ip address prefix-list WORD`
   Use this command in route map configuration mode to distribute any routes that have a destination network address that is permitted by the prefix list.
   The `no match ip address prefix-list WORD` command removes the match ip address prefix-list entry.


 - Configure the IP prefix list for a given route map with the following command:
   `ip prefix-list WORD seq <1-4294967295> (deny|permit) (A.B.C.D/M|any)`
   The `no ip prefix-list <word>seq <1-4294967295> (deny|permit) (A.B.C.D/M|any)` command deletes the IP prefix list for the given route map.

 - Configure the IP prefix list for a given route map with a prefix length specification using one of the following commands:
   `ip prefix-list WORD seq <1-4294967295>deny|permit <A.B.C.D/M>ge <length>`
   `ip prefix-list WORD seq <1-4294967295>deny|permit <A.B.C.D/M>ge <length>le <length>`
   `ip prefix-list WORD seq <1-4294967295>deny|permit <A.B.C.D/M>le <length>`
   The `no ip prefix-list WORD` command deletes the IP prefix list for the given route map.

 - Configure the IPv6 prefix list for a given route map with the following command:
   `ipv6 prefix-list WORD seq <1-4294967295>deny|permit <X:X::X:X/M|any>`
   The `no ipv6 prefix-list WORD` command deletes the IPv6 prefix list for the given route map.

 - Configure the IPv6 prefix list for a given route map with a prefix list description using the following command:
   `ipv6 prefix-list WORD description .LINE`
   The `no ipv6 prefix-list WORD` command deletes the IPv6 prefix list for the given route map.

 - Configure the IPv6 prefix list for a given route map with prefix length specification using one of the following commands:
   `ipv6 prefix-list WORD seq <1-4294967295>deny|permit <X:X::X:X/M>ge <length>`
   `ipv6 prefix-list WORD seq <1-4294967295>deny|permit <X:X::X:X/M>ge <length>le <length>`
   `ipv6 prefix-list WORD seq <1-4294967295>deny|permit <X:X::X:X/M>le <length>`
   The `no ipv6 prefix-list WORD` command deletes the IPv6 prefix list for the given route map.

- Facilitate the configuration of access lists based on autonomous system paths that control routing updates based on BGP autonomous paths information. Access lists are filters that restrict the routing information a router learns or advertises to and from a neighbor. Multiple BGP peers or route maps can reference a single access list. These access lists can be applied to both inbound route updates and outbound route updates. Each route update is passed through the access-list. BGP applies each rule in the access list in the order it appears in the list. When a route matches any rule, the decision to permit the route through the filter or deny is made, and no further rules are processed.
 Configure AS_PATH access lists using the following:
  `ip as-path access-list WORD  <deny | permit>.LINE`
  LINE is a pattern used to match against an input string. In BGP, a regular expression can be built to match information about an autonomous system path.
  The `no ip as-path access-list WORD <deny|permit>.LINE` command disables the access list configuration for AS_PATH.

- The community is compiled into a community structure. Multiple community lists can be defined under the same name. If that is the case, match happens in user-defined order. Once the community list matches to the communities attribute in BGP updates, the system returns either a permit or a deny response based on the community list definition. When there is no matched entry, deny is returned. When the community is empty, the system matches to any routes.
 Define a new community list as shown:
   `ip  community-list WORD <deny|permit>.LINE`
   The .LINE parameter is a string expression of communities attribute -->[1-2]00 , ^0:.*_, .*
   The WORD parameter is a string.
   The `no ip  community-list expanded WORD <deny|permit>.LINE` command disables community list for configured communities.

- Configure the extended community list with the following command:
  `ip extcommunity-list  WORD <deny|permit>.LINE`
  The `no ip extcommunity-list  WORD` command deletes the extended community list.

- Configure a prefix-list for a match on a given IP address with the following command:
   `match ip address prefix-list <word>`.
   The `no match ip address prefix-list <word>` command removes the rule for match on the IP address from the prefix list.

- The command `neighbor <ipv4_address | ipv6_address | peer_group_name>ebgp-multihop` attempts to connect to the external Autonomous System routers which are not directly connected. It takes either an IPv4 or IPv6 address or the peer-group name to establish a connection.
  To remove the ebgp-multihop configuration, use the `no neighbor <ipv4_address | ipv6_address | peer_group_name>ebgp-multihop` command.


## Verifying the configuration
Use the `show running-config` command to verify the configuration. All active configurations are displayed with the show running-config command. See the sample output below:

```
   s1# show running-config
  >Current configuration:
   !
   ip prefix-list BGP1 seq 5 permit 11.0.0.0/8
   ip prefix-list BGP1 seq 6 deny 12.0.0.0/8
   !
   route-map BGP2 permit 5
         description tsting route map description
         match ip address prefix-list bgp1
         set community 123:345 additive
         set metric 1000
   !
   router bgp 6001
         bgp router-id 9.0.0.1
         network 11.0.0.0/8
         maximum-paths 5
         timers bgp 3 10
         neighbor openswitch peer-group
         neighbor 9.0.0.2 remote-as 2
         neighbor 9.0.0.2 description abcd
         neighbor 9.0.0.2 password abcdef
         neighbor 9.0.0.2 timers 3 10
         neighbor 9.0.0.2 route-map BGP2 in
         neighbor 9.0.0.2 route-map BGP2 out
         neighbor 9.0.0.2 allowas-in 7
         neighbor 9.0.0.2 remove-private-AS
         neighbor 9.0.0.2 soft-reconfiguration inbound
         neighbor 9.0.0.2 peer-group openswitch
   !
```

## Troubleshooting the configuration

The following commands verify BGP route related information:

- The `show ip bgp` command verifies that all the routes are advertised from the peers.

```
   s1# show ip bgp
   Status codes: s suppressed, d damped, h history, * valid,>best, = multipath,
          i internal, S Stale, R Removed
   Origin codes: i - IGP, e - EGP, ? - incomplete
   Local router-id 9.0.0.2
   Network      Next Hop     Metric LocPrf Weight Path
  >11.0.0.0/8       9.0.0.1           0      0      0 1 i
  >12.0.0.0/8       0.0.0.0           0      0  32768  i
   Total number of entries 2
```

- For more information about a specific peer, use the `show` command.

```
   s1# show ip bgp 11.0.0.0/8
   BGP routing table entry for 11.0.0.0/8
   Paths: (1 available, best #1)
   AS: 1
       9.0.0.1 from 9.0.0.1
   Origin IGP, metric 0, localpref 0, weight 0, valid, external, best
   Last update: Thu Sep 24 22:45:52 2015
```

- The `show ip bgp summary` command provides peer status and additional neighbor information such as BGP packet statistics, total RIB entries, bgp router-id, and local AS number.

```
   s1# show ip bgp summary
   BGP router identifier 9.0.0.2, local AS number 2
   RIB entri es 2
   Peers 1
   Neighbor      AS MsgRcvd MsgSent Up/Down  State
```
- The `show ip bgp neighbors` command provides detailed information about the neighbor such as neighbor state, description, tcp port number, password (if any), and statistics.

```
   s1# show ip bgp neighbors
    name: 9.0.0.1, remote-as: 1
            state: Established
    description: abcd
    password: abcd
    tcp_port_number: 179
    statistics:
          bgp_peer_dropped_count: 1
          bgp_peer_dynamic_cap_in_count: 0
          bgp_peer_dynamic_cap_out_count: 0
          bgp_peer_established_count: 1
          bgp_peer_keepalive_in_count: 3
          bgp_peer_keepalive_out_count: 4
          bgp_peer_notify_in_count: 0
          bgp_peer_notify_out_count: 1
          bgp_peer_open_in_count: 1
          bgp_peer_open_out_count: 1
          bgp_peer_readtime: 25066
          bgp_peer_refresh_in_count: 0
          bgp_peer_refresh_out_count: 0
          bgp_peer_resettime: 25101
          bgp_peer_update_in_count: 2
          bgp_peer_update_out_count: 2
          bgp_peer_uptime: 25101
```
