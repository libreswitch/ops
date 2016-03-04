Layer 3 Test Cases
==================


## Contents

- [L3 interface configuration](#l3-interface-configuration)
- [Fastpath](#fastpath)
- [IPv4 static routes configuration](#ipv4-static-routes-configuration)
- [Delete IPv4 static routes](#delete-ipv4-static-routes)
- [IPv6 static routes configuration](#ipv6-static-routes-configuration)
- [Delete IPv6 static routes](#delete-ipv6-static-routes)
- [ECMP tests](#ecmp-tests)
- [LAG Fastpath](#lag-fastpath)

## L3 interface configuration
### Objective
This test verifies L3 interface configurations by executing ping tests.
### Requirements
- Physical switch/workstations test setup

- **FT File**: `ops/tests/test_layer3_ft_fastpath_connected.py` (L3 Interface & Fastpath for directly connected hosts)

### Setup
#### Topology diagram
```ditaa
    +--------+               +--------+                +--------+
    |        |               |        |                |        |
    |   H1   | <-------------+   S1   +--------------> |   H2   |
    |        |               |        |                |        |
    +--------+               +--------+                +--------+
```

### Description
1. Assign one IPv4 and one IPv6 address to an interface on the switch.
2. Connect a host to the switch and configure the host to be on the same subnet
as the switch.
3. Ping between the switch interface and the host.

### Test result criteria
#### Test pass criteria
The ping completes successfully.
#### Test fail criteria
The Pinging does not complete.

## Fastpath
### Objective
This test verifies that the ping went through fastpath by checking hit bit in ASIC.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/layer3/test_layer3_ft_fastpath_connected.py` (L3 Interface & Fastpath for directly connected hosts)

### Setup
#### Topology diagram
```ditaa
    +--------+               +--------+                +--------+
    |        |               |        |                |        |
    |   H1   | <-------------+   S1   +--------------> |   H2   |
    |        |               |        |                |        |
    +--------+               +--------+                +--------+
```

### Description
1. Configure two L3 interfaces on the switch.
        * **IPv4 addresses**: `10.0.0.1/24` and `11.0.0.24`.
        * **IPv6 addresses**: `2000::1/120` and `2002::1/120`
2. Connect two hosts to the following interfaces:
        * **IPv4 address**: `10.0.0.10` and `11.0.0.10`
        * **IPv6 address**: `2000::2` and `2002::2`
3. Configure route on host1 to reach the `11.0.0.0/24` network using the `10.0.0.1` IPv4 address.
4. Configure route on host1 to reach the `2002::0/120` network using the `2000::1` IPv4 address.
5. Configure route on host2 to reach the `10.0.0.0/24` network using the `11.0.0.1` IPv4 address.
6. Configure route on host2 to reach the `2000::0/120` network using the `2002::1` IPv4 address.
7. Ping between hosts for both IPv4 and IPv6 addresses.

### Test result criteria
#### Test pass criteria
Pings travel through fastpath without incident.
Verify this test using `ovs-appctl plugin/debug l3host` and `ovs-appctl plugin/debug l3v6host`. For these hosts, the hit bit in the ASIC entries show as **y** indicating that the host fast path traffic is updated.

#### Test fail criteria

## IPv4 static routes configuration
### Objective
This test case verifies that the ping works when IPv4 static routes are configured.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/test_layer3_ft_static_routes.py` (Static Routes IPv4)

### Setup
#### Topology diagram

```ditaa
                                                 +-------------+                              +-------------+
                                                1|             |2                            2|             |1
                   +----------------------------->  Switch 1   <------------------------------>  Switch 2   <------------------------------+
                   |                10.0.10.2/24 |             |10.0.20.1/24      10.0.20.2/24|             |10.0.30.2/24                  |
                   |                             +-------------+                              +-------------+                              |
                   |                          Routes configured on SW 1                    Routes configured on SW 2                       |
                   |                          ip route 10.0.30.0/24 10.0.20.2              ip route 10.0.10.0/24 10.0.20.1                 |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |h1-eth0                                                                                                         h2-eth0|
        +----------v--------+                                                                                                    +---------v---------+
        |                   |                                                                                                    |                   |
        |                   |                                                                                                    |                   |
        |      Host 1       | Routes configure on Host 1                                 Routes configure on Host 2              |      Host 2       |
        |                   | ip route add 10.0.20.0/24 via 10.0.10.2                    ip route add 10.0.10.0/24 via 10.0.30.2 |                   |
        |  IP: 10.0.10.1/24 | ip route add 10.0.30.0/24 via 10.0.10.2                    ip route add 10.0.20.0/24 via 10.0.30.2 |  IP: 10.0.30.1/24 |
        |                   |                                                                                                    |                   |
        +-------------------+                                                                                                    +-------------------+
```

### Description
Configure a topology with two hosts and two switches, connected as shown in the topology diagram.

**Host 1 configuration**
```
ip addr add 10.0.10.1/24 dev eth1
ip route add 10.0.20.0/24 via 10.0.10.2
ip route add 10.0.30.0/24 via 10.0.10.2
```

**Host 2 configuration**
```
ip addr add 10.0.30.1/24 dev eth1
ip route add 10.0.10.0/24 via 10.0.30.2
ip route add 10.0.20.0/24 via 10.0.30.2
```

**Switch 1 configuration**
1. Run the VTYSH Commands:
```
vtysh
conf term
interface 1
ip address 10.0.10.2/24
exit
interface 2
ip address 10.0.20.1/24
exit
ip route 10.0.30.0/24 10.0.20.2
exit
exit
```

2. Run the ovs-vsctl commands:
```
/usr/bin/ovs-vsctl set interface 1 user_config:admin=up
/usr/bin/ovs-vsctl set interface 2 user_config:admin=up
```

**Switch 2 configuration**
3. Run the VTYSH commands:
```
vtysh
conf term
interface 1
ip address 10.0.30.2/24
exit
interface 2
ip address 10.0.20.2/24
exit
ip route 10.0.10.0/24 10.0.20.1
exit
exit
```

4. Run the ovs-vsctl commands:
```
/usr/bin/ovs-vsctl set interface 1 user_config:admin=up
/usr/bin/ovs-vsctl set interface 2 user_config:admin=up
```

### Test result criteria
#### Test pass criteria
Pinging from host 1 to host 2 completes successfully.
#### Test fail criteria
Pinging from Host 1 to Host 2 does not complete.

## Delete IPv4 static routes
### Objective
This test case verifies that the ping fails when IPv4 static routes are deleted.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/test_layer3_ft_static_routes.py` (Static Routes IPv4)

### Setup
#### Topology diagram
```ditaa
                                                 +-------------+                              +-------------+
                                                1|             |2                            2|             |1
                   +----------------------------->  Switch 1   <------------------------------>  Switch 2   <------------------------------+
                   |                10.0.10.2/24 |             |10.0.20.1/24      10.0.20.2/24|             |10.0.30.2/24                  |
                   |                             +-------------+                              +-------------+                              |
                   |                          Routes configured on SW 1                    Routes configured on SW 2                       |
                   |                          ip route 10.0.30.0/24 10.0.20.2              ip route 10.0.10.0/24 10.0.20.1                 |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |h1-eth0                                                                                                         h2-eth0|
        +----------v--------+                                                                                                    +---------v---------+
        |                   |                                                                                                    |                   |
        |                   |                                                                                                    |                   |
        |      Host 1       | Routes configure on Host 1                                 Routes configure on Host 2              |      Host 2       |
        |                   | ip route add 10.0.20.0/24 via 10.0.10.2                    ip route add 10.0.10.0/24 via 10.0.30.2 |                   |
        |  IP: 10.0.10.1/24 | ip route add 10.0.30.0/24 via 10.0.10.2                    ip route add 10.0.20.0/24 via 10.0.30.2 |  IP: 10.0.30.1/24 |
        |                   |                                                                                                    |                   |
        +-------------------+                                                                                                    +-------------------+
```

### Description
Delete a route from one of the switches.
Switch 1 Command:
```
root(config): no ip route 10.0.30.0/24 10.0.20.2
```
### Test result criteria
#### Test pass criteria
* The ping from Host 1 to Host 2 does not complete.
* If the routes are added again, the ping passes because the routes were correctly deleted from the kernel and the database.

#### Test fail criteria
The ping from Host 1 to Host 2 does complete.

## IPv6 static routes configuration
### Objective
This test case verifies that the ping works when the IPv6 static routes are configured.

### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/test_layer3_ft_static_routes.py` (Static Routes IPv6)

### Setup
#### Topology diagram

```ditaa
                                                 +-------------+                              +-------------+
                                                1|             |2                            2|             |1
                   +----------------------------->  Switch 1   <------------------------------>  Switch 2   <------------------------------+
                   |                 2000::2/120 |             |2001::1/120        2001::2/120|             |2002::2/120                   |
                   |                             +-------------+                              +-------------+                              |
                   |                          Routes configured on SW 1                    Routes configured on SW 2                       |
                   |                          ipv6 route 2002::0/120 2001::2               ipv6 route 2000::0/120 2001::1                  |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |                                                                                                                       |
                   |h1-eth0                                                                                                         h2-eth0|
        +----------v--------+                                                                                                    +---------v---------+
        |                   |                                                                                                    |                   |
        |                   |                                                                                                    |                   |
        |      Host 1       | Routes configure on Host 1                                    Routes configure on Host 2           |      Host 2       |
        |                   | ip route add 2001::0/120 via 2000::2                          ip route add 2000::0/120 via 2002::2 |                   |
        |  IP: 2000::1/120  | ip route add 2002::0/120 via 2000::2                          ip route add 2001::0/120 via 2002::2 |  IP: 2002::1/120  |
        |                   |                                                                                                    |                   |
        +-------------------+                                                                                                    +-------------------+
```

### Description
Configure a topology with two hosts and two switches, connected as shown in the toplogy diagram.

**Host 1 configuration**
```
ip addr add 2000::1/120 dev eth1
ip route add 2001::0/120 via 2000::2
ip route add 2002::0/120 via 2000::2
```

**Host 2 configuration**
```
ip addr add 2002::1/120 dev eth1
ip route add 2000::0/120 via 2002::2
ip route add 2001::0/120 via 2002::2
```

**Switch 1 configuration**

1. Run the VTYSH commands:
```
vtysh
conf term
interface 1
ipv6 address 2000::2/120
exit
interface 2
ipv6 address 2001::1/120
exit

ipv6 route 2002::0/120 2001::2
exit
exit
```

2. Run the ovs-vsctl commands:
```
/usr/bin/ovs-vsctl set interface 1 user_config:admin=up
/usr/bin/ovs-vsctl set interface 2 user_config:admin=up
```

**Switch 2 configuration**

1. Run the VTYSH commands:
```
vtysh
conf term
interface 1
ipv6 address 2002::2/120
exit
interface 2
ipv6 address 2001::2/120
exit
ipv6 route 2000::0/120 2001::1
exit
exit
```

2. Run the ovs/vsctl commands:
```
/usr/bin/ovs-vsctl set interface 1 user_config:admin=up
/usr/bin/ovs-vsctl set interface 2 user_config:admin=up
```

### Test result criteria
#### Test pass criteria
Ping6 from Host 1 to Host 2 completes successfully.

#### Test fail criteria
Ping6 from Host 1 to Host 2 does not complete successfully.

## Delete IPv6 static routes
### Objective
This test case verifies that the ping fails when the IPv6 static routes are deleted.

### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/test_layer3_ft_static_routes.py` (Static Routes IPv6)

### Setup
#### Topology diagram

```ditaa
                                             +-------------+                              +-------------+
                                            1|             |2                            2|             |1
               +----------------------------->  Switch 1   <------------------------------>  Switch 2   <------------------------------+
               |                 2000::2/120 |             |2001::1/120        2001::2/120|             |2002::2/120                   |
               |                             +-------------+                              +-------------+                              |
               |                          Routes configured on SW 1                    Routes configured on SW 2                       |
               |                          ipv6 route 2002::0/120 2001::2               ipv6 route 2000::0/120 2001::1                  |
               |                                                                                                                       |
               |                                                                                                                       |
               |                                                                                                                       |
               |                                                                                                                       |
               |                                                                                                                       |
               |                                                                                                                       |
               |                                                                                                                       |
               |                                                                                                                       |
               |                                                                                                                       |
               |h1-eth0                                                                                                         h2-eth0|
    +----------v--------+                                                                                                    +---------v---------+
    |                   |                                                                                                    |                   |
    |                   |                                                                                                    |                   |
    |      Host 1       | Routes configure on Host 1                                    Routes configure on Host 2           |      Host 2       |
    |                   | ip route add 2001::0/120 via 2000::2                          ip route add 2000::0/120 via 2002::2 |                   |
    |  IP: 2000::1/120  | ip route add 2002::0/120 via 2000::2                          ip route add 2001::0/120 via 2002::2 |  IP: 2002::1/120  |
    |                   |                                                                                                    |                   |
    +-------------------+                                                                                                    +-------------------+
```

### Description
Delete a route from one of the switches.
Switch 1 command:
```
root(config): no ipv6 route 2002::0/120 2001::2
```

### Test result criteria
#### Test pass criteria
* Ping6 from Host 1 to Host 2 does not complete successfully.
* If the routes are added again, the ping is successful. This means that the ping is failing because the routes are deleted correctly from the database and the kernel.

#### Test fail criteria
Ping6 from Host 1 to Host 2 completes successfully.

## ECMP Tests
### Objective
Check ECMP load balancing distribution, inclusion/exclusion of various parameters.

### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/test_layer3_ft_ecmp_routing.py` (L3 ECMP Routing)

### Setup
#### Topology Diagram
    ```ditaa

                                    +----+
                                    |    |
                     +--------------> E1 |
                     |              |    |
                     |              +----+
                     |
                     |              +----+
                     |              |    |
                     |      +-------> E2 |
    +----+       +---v+     |       |    |
    |    |       |    <-----+       +----+
    | H1 <-------> D1 |
    |    |       |    <-----+       +----+
    +----+       +---^+     |       |    |
                     |      +-------> E3 |
                     |              |    |
                     |              +----+
                     |
                     |              +----+
                     |              |    |
                     +--------------> E4 |
                                    |    |
                                    +----+
    ```
|Entity | IPv4 Address | IPv4 Route(s)               | IPv6 Address | IPv6 Route(s)
|-------|--------------|-----------------------------|--------------|--------------
|Host H1| 20.0.0.10/24 | 0.0.0.0/0 -> 20.0.0.1 (D1)  | 20::10/64    | 0::0/0 -> 20::1 (D1)
|DUT D1 | 1.0.0.2/24   | 70.0.0.0/8 -> 1.0.0.1 (E1)  | 1::1/64      | 70::0/8 -> 1::1 (E1)
|DUT D1 | 2.0.0.2/24   |               2.0.0.1 (E2)  | 2::2/64      |            2::1 (E2)
|DUT D1 | 3.0.0.2/24   |               3.0.0.1 (E3)  | 3::2/64      |            3::1 (E3)
|DUT D1 | 4.0.0.2/24   |               4.0.0.1 (E4)  | 4::2/64      |            4::1 (E4)
|ECMP E1| 1.0.0.1/24   | none                        | 1::1/64      | none
|ECMP E2| 2.0.0.1/24   | none                        | 2::1/64      | none
|ECMP E3| 3.0.0.1/24   | none                        | 3::1/64      | none
|ECMP E4| 4.0.0.1/24   | none                        | 4::1/64      | none


### Description
1. Assign IPv4 and IPv6 address to interfaces on the host, switch and ECMP next hops.
1. Configure a route (R1) on the switch with multiple nexthops corresponding to the ECMP next hops.
1. On the host, listen for ICMP responses on the interface connected to the switch.
1. On the host, generate L4 packets destined for route R1, varying the packets' L3 and L4 information. Send one packet at a time.
1. Examine ICMP response packets' source IP information.

### Test Result Criteria
#### Test Pass Criteria
- Source IP in the ICMP response packets should be distributed evenly among the nexthops if the original outbound packets' L3 and L4 information is sufficiently varied.
- Source IP in the ICMP response packets should be from a single nexthop for packets with the same L3 and L4 source and destination information.

#### Test Fail Criteria
- Source IP in the ICMP response packets are all from a single nexthop.
- No ICMP response packets are received.

### Variation: Hashing Fields
Repeat the above setup and procedure with the following changes:
1. Generate packets such that all packets differ only in L3 source information.
1. Send these packets with default settings and verify traffic is distributed among nexthops.
1. Disable L3 source hashing.
1. Send the same packets again and verify all traffic is routed to a single next hop.
1. Repeat with L3 destination, L4 source, and L4 destination.

### Test Result Criteria
#### Test Pass Criteria
- Source IP in the ICMP response packets should be distributed evenly among the nexthops with default settings.
- Source IP in the ICMP response packets should be from a single nexthop when the varying hash parameter is disabled.

#### Test Fail Criteria
- Source IP in the ICMP response packets are all from a single nexthop in the default case.
- Source IP in the ICMP response packets are distrubuted when the varying hash parameter is disabled.
- No ICMP response packets are received.

### Objective
Check resilient ECMP.

### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/test_layer3_ft_ecmp_routing.py` (L3 ECMP Routing)

### Setup
#### Topology Diagram
Same as above

### Description
1. Assign IPv4 and IPv6 address to interfaces on the host, switch and ECMP next hops.
1. Configure a route (R1) on the switch with multiple nexthops corresponding to the ECMP next hops.
1. On the host, listen for ICMP responses on the interface connected to the switch.
1. On the host, generate multiple streams of packets destined for route R1 where each packet within a stream has the same source and destination L3 and L4 information.
1. Examine ICMP response packets' source IP information.
1. Disable one of the nexthops.
1. Generate new streams of packets destined for route R1.
1. Re-enable one of the nexthops.
1. Generate new streams of packets destined for route R1.

### Test Result Criteria
#### Test Pass Criteria
- Source IP in the ICMP response packets should be distributed evenly among the nexthops.
- Source IP in the ICMP response for each stream should remain the same throughout for each nexthop that is not added or removed.
- Source IP in the ICMP response for the stream destined for the nexthop that is removed should change to another nexthop and then should not change.
- Source IP in the ICMP response for the new streams (after the nexthop is re-added) should be distributed among all ECMP members.

#### Test Fail Criteria
- Source IP in the ICMP response packets for all streams are all from a single nexthop.
- Source IP in the ICMP response packets associated with a single stream vary.
- No ICMP response packets are received

## LAG Fastpath
### Objective
This test verifies that the ping went through fastpath with LAG configured on
both switches. This test case verifies that the ping works when IPv4 and IPv6
static routes are configured.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/test_layer3_ft_static_routes.py` (Static Routes IPv4 and IPv6)

### Setup
#### Topology diagram

```ditaa

        Routes configured on SW 1               Routes configured on SW 2
        ip route 10.0.30.0/24 10.0.20.2         ip route 10.0.10.0/24 10.0.20.1
        ip route 2002::/120 2001::2             ip route 2000::/120 2001::1

            +------------+                              +------------+
            |            | 2                          2 |            |
            |            <----------------------------->             |
            |            | (LAG 100)         (LAG  100) |            |
            |  Switch 1  | 10.0.20.1/24    10.0.20.2/24 |  Switch 2  |
            |            | 2001::1/120      2001::2/120 |            |
            |            <------------------------------>            |
            |            | 3                           3|            |
            +-----^------+                              +------^-----+
                1 | 10.0.10.2/24                            1 | 10.0.30.2/24
                  | 2000::2/120                               | 2002::2/120
                  |                                           |
                  |                                           |
                  |                                           |
                  |                                           |
                  | 10.0.10.1/24                 10.0.30.1/24 |
      (h1-eth0) 1 | 2000::1/120                   2002::1/120 | 1 (h2-eth0)
        +---------v---------+                       +---------v---------+
        |                   |                       |                   |
        |      Host 1       |                       |      Host 2       |
        |                   |                       |                   |
        +-------------------+                       +-------------------+

Routes configured on Host 1                 Routes configured on Host 2
ip route add 10.0.20.0/24 via 10.0.10.2     ip route add 10.0.10.0/24 via 10.0.30.2
ip route add 10.0.30.0/24 via 10.0.10.2     ip route add 10.0.20.0/24 via 10.0.30.2

ip route add 2001::0/120 via 2000::2        ip route add 2001::0/120 via 2002::1
ip route add 2002::0/120 via 2000::2        ip route add 2000::0/120 via 2002::1
```

### Description
Configure a topology with two hosts and two switches, connected as shown in the
topology diagram.

1. Configure LAG 100 to interface 2 on switch 1
    * **IPv4 address** `10.0.20.1/24`
    * **IPv6 address** `2001::1/120`
* Configure LAG 100 to interface 2 on switch 2
    * **IPv4 address** `10.0.20.2/24`
    * **IPv6 address** `2001::2/120`
* Configure two L3 interfaces on switch 1.
    * **IPv4 addresses**: `10.0.10.2/24` and `10.0.20.1/24`.
    * **IPv6 addresses**: `2000::2/120` and `2002::2/120`
* Configure two L3 interfaces on switch 2.
    * **IPv4 addresses**: `10.0.20.2/24` and `10.0.30.2/24`.
    * **IPv6 addresses**: `20001::2/120` and `2002::2/120`
* Connect two hosts to the following interfaces:
    * **IPv4 address**: `10.0.10.1/24` and `10.0.30.1/24`
    * **IPv6 address**: `2000::1/120` and `2002::1/120`
* Configure route on host1 to reach the `10.0.20.0/24` network using the `10.0.10.2` IPv4 address.
* Configure route on host1 to reach the `2001::0/120` network using the `2000::2` IPv6 address.
* Configure route on host1 to reach the `10.0.30.0/24` network using the `10.0.10.2` IPv4 address.
* Configure route on host1 to reach the `2002::0/120` network using the `2000::2` IPv6 address.
* Configure route on host2 to reach the `10.0.10.0/24` network using the `10.0.30.2` IPv4 address.
* Configure route on host2 to reach the `2000::0/120` network using the `2002::2` IPv6 address.
* Configure route on host2 to reach the `10.0.20.0/24` network using the `10.0.30.2` IPv4 address.
* Configure route on host2 to reach the `2001::0/120` network using the `2002::2` IPv6 address.
* Ping between hosts for both IPv4 and IPv6 addresses.
* Remove routes from switch 1 and switch 2.
* Ping between hosts for both IPv4 and IPv6 addresses.


### Test result criteria
#### Test pass criteria
- Ping from host 1 to host 2 completes successfully using IPv4 and IPv6 addresses when static routes are configured.
- Ping from host 2 to host 1 completes successfully using IPv4 and IPv6 addresses when static routes are configured.
- Ping from host 1 to host 2 completes unsuccessfully using IPv4 and IPv6 addresses when static routes are not configured.
- Ping from host 2 to host 1 completes unsuccessfully using IPv4 and IPv6 addresses when static routes are not configured.
#### Test fail criteria
- Ping from host 1 to host 2 completes unsuccessfully using IPv4 and IPv6 addresses when static routes are configured.
- Ping from host 2 to host 1 completes unsuccessfully using IPv4 and IPv6 addresses when static routes are configured.
- Ping from host 1 to host 2 completes successfully using IPv4 and IPv6 addresses when static routes are not configured.
- Ping from host 2 to host 1 completes successfully using IPv4 and IPv6 addresses when static routes are not configured.
