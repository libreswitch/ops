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
    +----+       +----+     |       |    |
                            +-------> E3 |
                                    |    |
                                    +----+
    ```
#### IPv4
|Entity | IPv4 Address | IPv4 Route(s)
|-------|--------------|---------------------------
|Host H1| 20.0.0.10/24 | 0.0.0.0/0 -> 20.0.0.1 (D1)
|DUT D1 | 1.0.0.2/24   | 70.0.0.0/24-> 1.0.0.1 (E1)
|DUT D1 | 2.0.0.2/24   |               2.0.0.1 (E2)
|DUT D1 | 3.0.0.2/24   |               3.0.0.1 (E3)
|ECMP E1| 1.0.0.1/24   | 20.0.0.0/24-> 1.0.0.2 (D1)
|ECMP E2| 2.0.0.1/24   | 20.0.0.0/24-> 2.0.0.2 (D1)
|ECMP E3| 3.0.0.1/24   | 20.0.0.0/24-> 3.0.0.2 (D1)

#### IPv6
|Entity | IPv6 Address | IPv6 Route(s)
|-------|--------------|--------------
|Host H1| 20::10/64    | 0::0/0 -> 20::1 (D1)
|DUT D1 | 1001::1/64   | 70::0/64 -> 1001::1 (E1)
|DUT D1 | 1002::2/64   |             1002::1 (E2)
|DUT D1 | 1003::2/64   |             1003::1 (E3)
|ECMP E1| 1001::1/64   | 20::0/64 -> 1001::2 (D1)
|ECMP E2| 1002::1/64   | 20::0/64 -> 1002::2 (D1)
|ECMP E3| 1003::1/64   | 20::0/64 -> 1003::2 (D1)

### Description
1. Verify ECMP and hashing by all fields are enabled `show ip ecmp`.
1. Assign IPv4 and IPv6 address to interfaces on the host, switch and ECMP
   next hops.
1. Configure a route (R1) on the switch with multiple nexthops corresponding
   to the ECMP next hops.
1. On each nexthop listen for inbound traffic on the interface connected to the
   switch.
1. On the host, generate L4 packets destined for route R1, varying the packet
   L3 and L4 information. Send one packet at a time.
1. Examine packets received at the next hops for source and destination.

### Test Result Criteria
#### Test Pass Criteria
- Source IP in the packets should be distributed evenly among
  the nexthops if the original outbound packet L3 and L4 information is
  sufficiently varied.
- Packets with a given set of source and destination L3 and L4 information
  should arrive at one and only one nexthop.

#### Test Fail Criteria
- Packets are dropped.
- Packets are seen by only one next hop.
- Packets with a given set of source and destination L3 and L4 information
  are distributed among multiple nexthops.

### Variation: Hashing Fields
Repeat the above setup and procedure with the following changes:

1. Generate packets such that all packets differ only in L3 source information.
1. Send these packets with default settings and verify traffic is distributed
   among nexthops.
1. Disable L3 source hashing `ip ecmp load-blance src-ip disable`.
1. Use `show ip ecmp` to verify L3 source hashing is disabled.
1. Send the same packets again and verify all traffic is routed to a single
   next hop.
1. Re-enable L3 source hashing `no ip ecmp load-blance src-ip disable`.
1. Repeat with L3 destination, L4 source, and L4 destination.

### Variation: Disable ECMP
Repeat the above setup and procedure with the following changes:

1. Generate packets such that all packets differ in L3/L4 fields.
1. Send these packets with default settings and verify traffic is distributed
   among nexthops.
1. Disable ECMP entirely `ip ecmp disable`.
1. Use `show ip ecmp` to verify ECMP is disabled.
1. Send the same packets again and verify all traffic is routed to a single
   next hop.
1. Re-enable ECMP `no ip ecmp disable`.

### Test Result Criteria
#### Test Pass Criteria
- Packets should be distributed evenly among the nexthops with default settings.
- Packets should be seen by a single nexthop when the varying hash parameter
  is disabled.

#### Test Fail Criteria
- Packets are all seen by a single nexthop in the default case.
- Packets are distrubuted when the varying hash parameter is disabled.
- Packets are dropped.

### Objective
Check resilient ECMP.

### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops/tests/test_layer3_ft_ecmp_resilient.py` (Resilient ECMP)
- **FT File**: `ops/tests/test_layer3_ft_ecmp_resilient_ipv6.py` (IPv6
  Resilient ECMP)

### Setup
#### Topology Diagram
Same as above

### Description
1. Assign IPv4 and IPv6 address to interfaces on the host, switch and
   ECMP next hops.
1. Configure a route (R1) on the switch with multiple nexthops corresponding
   to the ECMP next hops.
1. On the next hops, listen for packets on the interface connected to the switch.
1. On the host, generate a stream of packets destined for route R1
   where each packet within a stream has the same source and destination
   L3 and L4 information.
1. Note which nexthop is selected (N1)
#### Case 1: Disable an un-selected nexthop
1. Disable one of the other nexthops (N2).
1. Generate a new stream of packets destined for route R1.
#### Case 2: Re-enabled un-selected nexthop.
1. Re-enable nexthop N2.
1. Generate a new stream of packets destined for route R1.
#### Case 3: Disable the selected nexthop.
1. Disable nexthop N1.
1. Generate a new stream of packets destined for route R1.
#### Case 4: Re-enable the selected nexthop.
1. Re-enable nexthop N1.
1. Generate a new stream of packets destined for route R1.


### Test Result Criteria
#### Test Pass Criteria
- In each case, packets should arrive at one and only one nexthop.
- In Case 1, traffic *must not* shift to another nexthop.
- In Case 2, traffic _may_ shift to another nexthop depending on the hardware
  implementation [1], but should still select one and only one nexthop.
- In Case 3, traffic *must* shift to one and only one nexthop.
- In Case 4, traffic _may_ shift to another nexthop depending on the hardware
  implementation [1], but should still select one and only one nexthop.

[1] In some implementations, removing a nexthop will not shift traffic, because
entries in the ECMP group corresponding to the lost nexthop are simply
overwritten with new values. In the case of _adding_ a nexthop, however,
existing entries are overwritten or the ECMP group table size is increased,
which can cause traffic to shift due to overwiting entries or a larger modulus
for hash operations.

#### Test Fail Criteria
- Packets associated with a single stream arrive at multiple nexthops.
- Packets are dropped.

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
