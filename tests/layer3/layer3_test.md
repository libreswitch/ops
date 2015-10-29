Layer 3 Test Cases
==================


## Contents

- [L3 interface configuration](#l3-interface-configuration)
- [Fastpath](#fastpath)
- [IPv4 static routes configuration](#ipv4-static-routes-configuration)
- [Delete IPv4 static routes](#delete-ipv4-static-routes)
- [IPv6 static routes configuration](#ipv6-static-routes-configuration)
- [Delete IPv6 static routes](#delete-ipv6-static-routes)

## L3 interface configuration
### Objective
This test verifies L3 interface configurations by executing ping tests.
### Requirements
- Physical switch/workstations test setup
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py` (L3 Interface & Fastpath for directly connected hosts)

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
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py` (L3 Interface & Fastpath for directly connected hosts)

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
- Physical Switch/Workstations Test setup
- **FT File**: `ops-quagga/zebra/test/test_zebra_ft_l3static.py` (Static Routes IPv4)

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
- Physical Switch/Workstations Test setup
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py`(L3 Interface & Fastpath for directly connected hosts)

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
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py` (L3 Interface & Fastpath for directly connected hosts)

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
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py` (L3 Interface & Fastpath for directly connected hosts)

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
