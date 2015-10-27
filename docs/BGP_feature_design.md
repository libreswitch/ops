#Overview of BGP Integration with OpenSwitch Architecture
OpenSwitch is designed to achieve optimal modularization, high availability, portability, extensibility, and unrestricted reuse of open source projects. The Quagga Border Gateway protocol (BGP) project is integrated as one of the OpenSwitch modules. BGP alone can provide complete dynamic routing for OpenSwitch. It can also work together with other protocols such as OSPF, ISIS and so on. This document mainly focuses on the role that BGP plays in the OpenSwitch architecture and its interaction with other modules. For the BGP internal design, see http://www.openswitch.net/documents/dev/ops-quagga/DESIGN. For the details of any other module that partcicipates with BGP and Openswitch, see the corresponding design module at http://www.openswitch.net/documents/dev/ops-xxx/DESIGN.

#Participating modules and data flow

Figure 1 indicates intermodule communications and BGP data flow through the OpenSwitch architecture.

```ditaa

    +------------------------------------------------------------------------+
    |                                BGP                                     |
    |                       (EBGP, IBGP, MPLSVPN)                            |
    +---^--------------------------------------^-----------------------------+
        |                                      |
      1 |                                    2 |
    +---v----+       +-------------+       +---v-----+        +--------------+
    |        |<----->|   Zebra     |<----->|         |<------>|   CLI/UI     |
    |   K    |       |   (RIB)     |       |         |        | Config/Show  |
    |        |       +-------------+       |         |        +--------------+
    |   E    |                             |         |
    |        |       +-------------+       |         |        +--------------+
    |   R    |<----->|   Arpmgrd   |<----->|         |<------>| OSPF ISIS RIP|
    |        |       |             |       |         |        |              |
    |   N    |       +-------------+       |    O    |        +--------------+
    |        |                             |         |
    |   E    |       +-------------+       |    V    |        +--------------+
    |        |<----->|   Portd     |<----->|         |<------>|   Policy     |
    |   L    |       | (interface) |       |    S    |        |              |
    |        |       +-------------+       |         |        +--------------+
    | (FIB)  |                             |    D    |
    |        |                             |         |        +--------------+
    +---^----+                             |    B    |<------>|    BFD       |
        |                                  |         |        |              |
      3 |                                  |         |        +--------------+
    +------------------------------+       |         |
    |   ASIC/HW Forwarding         |       |         |        +--------------+
    |           (FIB)              |       |         |<------>|    MPLS      |
    +--------------^---------------+       |         |        |  (LDP/RSVP)  |
                   |                       |         |        +--------------+
                   |                       |         |
    +--------------v---------------+       |         |        +--------------+
    |          Vswitchd            |<----->|         |<------>|  Multicast   |
    |                              |       |         |        | (PIM/IGMP)   |
    +------------------------------+       +---------+        +--------------+

                         Figure 1, BGP Routing Architecture Overview
```

##OVSDB
OVSDB serves as a central communication hub and all other modules communicate to and from BGP indirectly through OVSDB. As a result, BGP is shielded from all sorts of issues from other modules in the system. The OVSDB also provides a single data view to all modules in the system. All modules and OVSDB interact through publish and subscribe mechanisms.

##BGP
BGP is an exterior gateway protocol (EGP) that is designed to exchange routing information among routers and switches in various autonomous systems (AS). BGP runs on top of the TCP protocol.

##Kernel
All the BGP protocol control packets, such as open, update, keepalive, and notification are sent and received through the kernel (BGP<--->Kernel<--->ASIC). In addition to providing operating system functions and TCP for BGP, the kernel receives a copy of forwarding information base (FIB) and can do slow path forwarding compared to ASIC fast path forwarding.

##OSPF and ISIS
OSPF or ISIS are both link state interior gateway protocols (IGP) that are designed to discover the shortest paths through routers and switches in a single autonomous system. OSPF runs on top of the IP protocol. The OSPF process supports IPv4, and the OSPF3 supports IPv6. Unlike OSPF, ISIS runs natively on an L2 and it does not need interface addressing information to transmit a message. Therefore, it can route multiple protocols and support both IPv4 and IPv6. BGP often relies on IGP to resolve its protocol next hops.

##UI
The CLI or REST or both are responsible for BGP configurations, state monitoring, show commands, and debug dumping.

##Portd/interface
BGP receives interface up or down state changes, address notifications from Portd and state notifications from interface modules.

##Zebra
Zebra creates FIB by selecting active routes from all routes learned from all the protocols including BGP. On selecting the active routes, Zebra downloads FIB to the kernel, triggers the start of BGP route redistribution, and does next hop recursive resolution on behalf of BGP.

##BFD
Bidirectional Forwarding Detection (BFD) can be used to detect faults between two forwarding engines connected by a link. It provides low-overhead detection of faults on physical media that does not support failure detection itself, such as Ethernet, virtual circuits, and tunnels. BGP protocols can use BFD to receive faster notification of failing links using the native keepalive mechanism to play an important role for BGP fast convergence or fast recovering from link failures. Fast detection of failures is the key for BGP to converge quickly by using ECMP or add path.

##MPLS-LDP-RSVP
LDP and RSVP are both MPLS signaling protocols that are used to set up MPLS tunnels. In L3 VPN deployment, BGP relies on the MPLS tunnels to route VPN traffic.

##HA in OpenSwitch architecture
    - Non-stop forwarding or graceful restart (GR)
    - Non-stop routing (NSR)

##Policy
The routing policy in Quagga is a library. BGP includes all routing policy in the BGP process. Then it can be applied when importing or exporting BGP routes. The prefix list can be used for filtering, while the route map can be used to change BGP path attributes.


##Inter module data flows
###Path for BGP input:
    - Configurations:                     BGP <--- OVSDB <--- UI
    - Port/Interface up/down/addresss:    BGP <--- OVSDB <--- Portd
    - Redistributed routes:               BGP <--- OVSDB <--- Zebra
    - Recursive nexthop resolution:       BGP <--- OVSDB <--- Zebra
    - Route map configuration:            BGP <--- OVSDB <--- Policy
    - Protocol packets:                   BGP <--- Kernel <--- ASIC (3-1)

###Path for BGP output:
    - Best routes:                        BGP ---> OVSDB ---> Zebra
    - Local RIB:                          BGP ---> OVSDB
    - show/dump/statistics                BGP ---> OVSDB ---> UI
    - Advertise routes, keepalive etc:    BGP ---> Kernel ---> ASIC (1-3)


#OVSDB-Schema
------------
All BGP configurations originate from the OVSDB. The UI writes configurations to the OVSDB. There are two OVSDB tables designed for BGP configurations that correspond to three hierarchical levels of BGP configurations. The BGP router table is used for global BGP configurations. The BGP neighbor and peer group tables store group and peer level configurations. BGP subscribes to OVSDB, whenever there is a new configuration or if there are new configuration changes, BGP gets a notification, and picks up the new configurations, and then programs the BGP back end as if the configuration is accessed directly from the CLI.

After BGP selects the best paths, it writes the selected routes to the RIB table in the OVSDB, triggering the start of the FIB computation by Zebra. BGP also writes statistics to the OVSDB BGP tables.

##BGP and OVSDB table relationships
Figure 2 describes the interaction between the BGP and the OVSDB tables.

```ditaa

    +-------+        +------------+       +-------------+       +--------------+
    |       |   1    |            |       |             |       |              |
    |       <-------->   VRF      +------->  BGP_Router +-------> BGP_Neighbor |
    |       |        +------------+       +-------------+       +--------------+
    |       |
    |       |        +------------+       +-------------+
    |       |   2    |            |       |             |
    |       <--------+ Route_Map  +-------> Rt_Map_Entry|
    |       |        +------------+       +-------------+
    |       |
    |       |        +------------+       +-------------+
    |   B   |   3    |            |       |             |
    |       <--------+Prefix_List +-------> Plist_Entry |
    |       |        +------------+       +-------------+
    |       |
    |   G   |        +------------+        +-------------+
    |       |   4    | Global RIB |        |             |
    |       <--------+  FIB       |------->| Nexthop     |
    |       |        +------------+        +-------------+
    |   P   |
    |       |        +------------+       +-------------+
    |       |   5    |            |       |             |
    |       <--------+  Port      +-------> Interface   |
    |       |        +------------+       +-------------+
    |       |
    |       |        +------------+       +-------------+
    |       |   6    |            |       |             |
    |       +-------->  BGP_RIB   +-------> BGP_Nexthop |
    +-------+        +------------+       +-------------+

              Figure 2 BGP and OVSDB tables
```

Note: Route numbers correspond to the numbers displayed in Figure 2.

      - Route number 1 shows the relationship between the VRF, BGP_Router and the BGP_Neighbor tables. BGP subscribes to VRF, BGP_router, BGP_Neighbor tables for BGP configurations. BPG also publishes statistics to the three BGP tables.
      - Route number 2 displays the relationship between the BGP, Route_Map and Rt_Map_Entry. The BGP subscribes to the route map tables for route map configurations.
      - Route number 3 shows the relationship between the BGP, Prefix_List and the Plist_Entry. BGP subscribes to the prefix tables for prefix filter configurations.
      - Route 4 displays the BGP, global RIB and FIB relationship. BGP publishes the best paths to the global RIB table. BGP also subscribs to FIB for route redistribution and nexthop resolution.
      - Route 5 displays the BGP, port and Interface relationship. BGP subscribes to the port and interface table for interface states and addresses.
      - Route 6 shows the BGP sending local routes to the BGP_RIB table in the OVSDB that serves as a database for BGP internal data.

##TABLE SUMMARY
The following list summarizes the purpose of each of the tables and their corresponding tables in the OpenSwitch database. Each table is described in more detail following the summary table.

###Table 1 Table summary

```ditaa

    Table             |  Purpose
======================|=========================================================
    VRF               |  Virtual Routing and Forwarding
    BGP_Router        |  BGP configurations, statuses and statistics
    BGP_Neighbor      |  BGP peer groups, peers, statuses and statistics
    Route_Map         |  Route map to modify BGP path attributes
    Route_Map_Entry   |  Ordered entries of route map
    Prefix_List       |  Prefix list used to filter BGP routes
    Prefix_List_Entry |  Ordered entries of prefix list
    RIB/FIB           |  Routing Information Base and FIB
    Nexthop           |  Nexthops for IP routes
    Port              |  Physical port, including L3 interface addresses
    Interface         |  Interface state
    BGP_RIB           |  BGP private RIB, status and statistics
    BGP_Nexthop       |  BGP private next hops
----------------------|---------------------------------------------------------

```
###Table 2 Column summary for VRF table

```ditaa

    Column           |   Purpose
=====================|==========================================================
    Name             |   tag of vrf
---------------------|----------------------------------------------------------
    bgp_routers      |   references to BGP Router Table
---------------------|----------------------------------------------------------

```

###Table 3 Column summary for BGP_Router table

```ditaa

    Column           |   Purpose
=====================|==========================================================
  router_id          |   id of BGP router
---------------------|----------------------------------------------------------
  networks           |   BGP configured network routes
---------------------|----------------------------------------------------------
  maximum_paths      |   max ECMP path allowed, to enable ECMP
---------------------|----------------------------------------------------------
                     |   key              value
  timers             |   keepalive
                     |   holdtime
---------------------|----------------------------------------------------------
  redistribute       |   export routes from other protocols to BGP
---------------------|----------------------------------------------------------
  always_compare_med |   TBD
---------------------|----------------------------------------------------------
  deterministic_med  |   TBD
---------------------|----------------------------------------------------------
  gr_stale_timer     |   TBD
---------------------|----------------------------------------------------------
  bgp_neighbors      |   reference to BGP_Neighbor table
---------------------|----------------------------------------------------------
  fast-external-failover| TBD
---------------------|----------------------------------------------------------
  enforce-first-as   |   TBD
---------------------|----------------------------------------------------------
  aggregate-address  |   TBD
---------------------|----------------------------------------------------------
  cluster-id         |   TBD
---------------------|----------------------------------------------------------
  graceful-restart   |   Non-stop forwarding
---------------------|----------------------------------------------------------

```

###Table 4 Column summary for BGP_Neighbour table

```ditaa

    Column           |   Purpose
=====================|==========================================================
  is_peer_group      |   peer or peer group
---------------------|----------------------------------------------------------
  shutdown           |   Shutdown peer but keep configurations
---------------------|----------------------------------------------------------
  remove_private_as  |   Do not send private AS out of AS
---------------------|----------------------------------------------------------
  passive            |   Not sending open message
---------------------|----------------------------------------------------------
  bgp_peer_group     |   Peer pointing to peer group it belong to
---------------------|----------------------------------------------------------
  remote_as          |   AS number of a peer
---------------------|----------------------------------------------------------
  allow_as_in        |   Permit own AS appearing in the as path
---------------------|----------------------------------------------------------
  local_as           |   AS number of self
---------------------|----------------------------------------------------------
  weight             |   Local weight for best path selection
---------------------|----------------------------------------------------------
  tcp_port_number    |   TBD
---------------------|----------------------------------------------------------
  advertise_interval |   Mimum time to wait before advertise routes
---------------------|----------------------------------------------------------
  maximum_prefix     |   Maxinum number of prefix can receive from a peer
---------------------|----------------------------------------------------------
  capability         |  TBD
---------------------|----------------------------------------------------------
  override_capability|  TBD
---------------------|----------------------------------------------------------
  inbound_soft_reconfiguration | keep a copy of all received routes
---------------------|----------------------------------------------------------
  password           |   MD5 TCP password
---------------------|----------------------------------------------------------
                     |   key              value
  timers             |   keepalive
                     |   holdtime
---------------------|----------------------------------------------------------
                     |   key              value
  route_maps         |   in/out           pointer to a row of a Route_Map table
---------------------|----------------------------------------------------------
  statistics         |   Key                           value
                     |   bgp-peer-established-count
                     |   bgp-peer-dropped-count
                     |   bgp-peer-open_in-count
                     |   bgp-peer-open_out-count
                     |   bgp-peer-update_in-count
                     |   bgp-peer-update_out-count
                     |   bgp-peer-keepalive_in-count
                     |   bgp-peer-keepalive_out-count
                     |   bgp-peer-notify_in-count
                     |   bgp-peer-notify_out-count
                     |   bgp-peer-refresh_in-count: count of route refresh received
                     |   bgp-peer-refresh_out-count
                     |   bgp-peer-dynamic_cap_in-count: how many time dynamic cap send
                     |   bgp-peer-dynamic_cap_out-count: how many time dynamic cap send
                     |   bgp-peer-uptime: how long since peer is established
                     |   bgp-peer-readtime: when was last time u/k message received
                     |   bgp-peer-readtime: when was last time peer get reset
---------------------|----------------------------------------------------------
  timers connect     |   BGP connect tiemr
---------------------|----------------------------------------------------------
  advertisement-interval| Minimum gap between send updates
---------------------|----------------------------------------------------------
  capability dynamic |  Advertise dynamic capability
---------------------|----------------------------------------------------------
  capability orf     |  Advertise ORF capability of prefix list send/receive
---------------------|----------------------------------------------------------
  override-capability|  Override negotiation
---------------------|----------------------------------------------------------
  disable-connected-check| Multihop EBGP
---------------------|----------------------------------------------------------
  ebgp-multihop      |  Enable multihop EBGP
---------------------|----------------------------------------------------------
  next-hop-self      |  TBD
---------------------|----------------------------------------------------------
  route-reflector-client| Nbr as a RR client
---------------------|----------------------------------------------------------
  send-community     |  Send cummunity to this nbr
---------------------|----------------------------------------------------------
  ttl-security hops  |  Max hop to BGP peer
---------------------|----------------------------------------------------------

```


###Table 5 Column summary for Route_Map table

```ditaa

    Column         |   Purpose
===================|============================================================
  Name             |   tag of route map
-------------------|------------------------------------------------------------
  route_map_entries|   references to Route Map Entry Table
-------------------|------------------------------------------------------------

```

###Table 6 Column summary for Route_Map_Entry table

```ditaa

    Column     |   Purpose
===============|================================================================
    action     |   On match permit or deny
---------------|----------------------------------------------------------------
    continue   |   Continue on a entry <1-65536> within the route-map
---------------|----------------------------------------------------------------
    on match   |   On match goto <1-65535> or next
---------------|----------------------------------------------------------------
    call       |   Jump to another Route-Map WORD after match+set
---------------|----------------------------------------------------------------
    match      |   key                           value
               |----------------------------------------------------------------
               | as-path                      name of access list
               | community                    <1-99>|<100-500>|WORD
               | community                    <1-99>|<100-500>|WORD exact-match
               | extcommunity                 <1-99>|<100-500>|WORD
               | interface                    name of 1st hop interface
               | ip address  prefix-list      name of prefix list
               | ip address                   <1-199>|<1300-2699>|WORD of alist
               | ip next-hop prefix-list      name
               | ip next-hop                  <1-199>|<1300-2699>|WORD
               | ip route-source prefix-list
               | ip route-source              <1-199>|<1300-2699>|WORD
               | ipv6 address prefix-list
               | ipv6 address                 name
               | ipv6 next-hop                X:X::X:X
               | metric                       <0-4294967295>
               | origin                       egp|igp|incomplete
               | peer                         A.B.C.D|X:X::X:X
               | tag                          <0-65535>
---------------|----------------------------------------------------------------
    set        |   Key                       value
               |----------------------------------------------------------------
               |   aggregator  as           <1-4294967295> A.B.C.D
               |   as-path  exclude         <1-4294967295>
               |   as-path  prepend         <1-4294967295>
               |   atomic-aggregate
               |   comm-list                <1-99>|<100-500>|WORD delete
               |   community                AA:NN|AA:NN additive/none
               |   extcommunity  rt         ASN:nn_or_I-address:nn
               |   extcommunity  soo        ASN:nn_or_IP-address:nn
               |   forwarding-address       X:X::X:X
               |   ip next-hop              A.B.C.D/peer-address
               |   ipv6  next-hop  global   X:X::X:X
               |   ipv6  next-hop  local    X:X::X:X
               |   local-preference         <0-4294967295>
               |   metric                   <+/-metric>|<0-4294967295>
               |   origin                   egp|igp|incomplete
               |   originator-id            A.B.C.D
               |   src                      A.B.C.D
               |   tag                      <0-65535>
               |   vpnv4  next-hop          A.B.C.D
               |   weight                   <0-4294967295>
---------------|----------------------------------------------------------------

```

###Table 7 Column summary for Prefix_List table

```ditaa

    Column           |   Purpose
=====================|==========================================================
  Name               |   tag of prefix list
---------------------|----------------------------------------------------------
  prefix_list_entries|   references to Prefix List Entry Table
---------------------|----------------------------------------------------------

```

###Table 8 Column summary for Prefix_List_Entry table

```ditaa

    Column         |   Purpose
===================|============================================================
    action         |   permit or deny
-------------------|------------------------------------------------------------
    prefix         |   ip address
-------------------|------------------------------------------------------------
    ge             |   TBD
-------------------|------------------------------------------------------------
    le             |   TBD
-------------------|------------------------------------------------------------

```

###Table 9 Column summary for RIB (Route) table

```ditaa

    Column             |   Purpose
=======================|==========================================================
    vrf                |   back pointer to vrf table that this rib belong to
-----------------------|----------------------------------------------------------
    prefix             |   prefix/len
-----------------------|----------------------------------------------------------
    from               |   which protocol this prefix learned
-----------------------|----------------------------------------------------------
    address_family     |   IPv4, IPv6
-----------------------|----------------------------------------------------------
    sub_address_family |   Unicast, multicast
-----------------------|----------------------------------------------------------
    distance           |   Administrative preference of this route
-----------------------|----------------------------------------------------------
    metric             |   BGP MED value
-----------------------|----------------------------------------------------------
                       |   n_nexthops: count of nh
    nexthops           |   Array of pointer to next hop table row
-----------------------|----------------------------------------------------------
    selected           |   Active route
-----------------------|----------------------------------------------------------

```

###Table 10 Column summary for BGP RIB (BGP_Route) table

```ditaa

    Column             |   Purpose
=======================|==========================================================
    vrf                |   back pointer to vrf table that this rib belong to
-----------------------|----------------------------------------------------------
    prefix             |   prefix/len
-----------------------|----------------------------------------------------------
    address_family     |   IPv4, IPv6
-----------------------|----------------------------------------------------------
    sub_address_family |   Unicast, multicast
-----------------------|----------------------------------------------------------
    peer               |   BGP peer IPv4 address
-----------------------|----------------------------------------------------------
    distance           |   Administrative preference of this route
-----------------------|----------------------------------------------------------
    metric             |   BGP MED value
-----------------------|----------------------------------------------------------
                       |   n_nexthops: count of nh
    bgp_nexthops       |   Array of pointer to bgp next hop table row
-----------------------|----------------------------------------------------------
    path_attributes    |   key                      value
                       |----------------------------------------------------------
                       |   as-path
                       |   Origin
                       |   metric/MULTI_EXIT_DISC
                       |   local pref
                       |   community                7010:6010 7012:6012
                       |   excommunity
                       |   weight
                       |   ORIGINATOR_ID
                       |   CLUSTER_LIST
                       |   ADVERTISER
                       |   AGGREGATOR
-----------------------|----------------------------------------------------------
    flags              |   TBD
-----------------------|----------------------------------------------------------

```

###Table 11 Column summary for nexthop table

```ditaa

    Column           |   Purpose
=====================|==========================================================
    ip_address       |   nexthop ip address
---------------------|----------------------------------------------------------
    type             |   nexthop type  (unicast, multicast, indirect etc)
---------------------|----------------------------------------------------------
    ports            |   n_ports
                     |   array of pointer to Port table row
---------------------|----------------------------------------------------------
    selected         |   active nexthop
---------------------|----------------------------------------------------------
    weight           |   weight for unequal cost load balance
---------------------|----------------------------------------------------------

```

###Table 12 Column summary for BGP_Nexthop table

```ditaa

    Column           |   Purpose
=====================|==========================================================
    ip_address       |   nexthop ip address
---------------------|----------------------------------------------------------
    type             |   nexthop type  (unicast, multicast, indirect etc)
---------------------|----------------------------------------------------------
    Weight           |   TBD
---------------------|----------------------------------------------------------

```

###Table 13 Column summary for Port table

```ditaa

    Column           |   Purpose
=====================|==========================================================
    name             |   tag of port
---------------------|----------------------------------------------------------
    interfaces       |   references to Interface Table
---------------------|----------------------------------------------------------
    vlan_mode        |   trunk/access/native-tagged/native-untagged
---------------------|----------------------------------------------------------
    ip4_address      |   port IPv4 address
---------------------|----------------------------------------------------------
    ip6_address      |   port IPv6 address
---------------------|----------------------------------------------------------

```

###Table 14 Column summary for Interface table

```ditaa

    Column           |   Purpose
=====================|==========================================================
    name             |   tag of port
---------------------|----------------------------------------------------------
    name             |   tag of interface
---------------------|----------------------------------------------------------
    type             |   system/internal
---------------------|----------------------------------------------------------
    admin_state      |   up/down
---------------------|----------------------------------------------------------
    link_state       |   up/down
---------------------|----------------------------------------------------------

```


#References
----------
* [Archtecture](http://www.openswitch.net/documents/user/architecture)
* [BGP](https://www.ietf.org/rfc/rfc4271.txt)
* [Quagga](http://www.nongnu.org/quagga/docs.html)
* [OpenSwitch](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN)
* [Interface](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN)
