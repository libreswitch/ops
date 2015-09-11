Layer 3 Test Cases
=======


## Contents

- [L3 interface configuration](#l3-interface-configuration)
- [Fastpath](#fastpath)
- [IPv4 static routes configuration](#ipv4-static-routes-configuration)
- [Delete IPv4 static routes](#delete-ipv4-static-routes)
- [IPv6 static routes configuration](#ipv6-static-routes-configuration)
- [Delete IPv6 static routes](#delete-ipv6-static-routes)

##  L3 interface configuration
### Objective
Test case checks L3 interface configuration by doing ping tests.
### Requirements
- Physical Switch/Workstations Test setup
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py` (L3 Interface & Fastpath for Directly Connected Hosts)

### Setup
#### Topology Diagram
    ```ditaa
    +--------+               +--------+                +--------+
    |        |               |        |                |        |
    |   H1   | <-------------+   S1   +--------------> |   H2   |
    |        |               |        |                |        |
    +--------+               +--------+                +--------+
    ```

### Description
1. Assign IPv4 and IPv6 address to an interface on the switch.
1. Connect a host to the switch and configure the host to be on the same subnet
as with switch.
1. Ping between the switch interface and the host.
### Test Result Criteria
#### Test Pass Criteria
Ping works fine.
#### Test Fail Criteria

##  Fastpath
### Objective
Test case checks if ping went through fastpath by checking hit bit in ASIC.
### Requirements
- Physical Switch/Workstations Test setup
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py` (L3 Interface & Fastpath for Directly Connected Hosts)

### Setup
#### Topology Diagram
    ```ditaa
    +--------+               +--------+                +--------+
    |        |               |        |                |        |
    |   H1   | <-------------+   S1   +--------------> |   H2   |
    |        |               |        |                |        |
    +--------+               +--------+                +--------+
    ```

### Description
1. Configure two L3 interfaces on switch.
        * **IPv4 addresses**: `10.0.0.1/24` and `11.0.0.24`.
        * **IPv6 addresses**: `2000::1/120` and `2002::1/120`
1. Connect two hosts to these interfaces.
        * **IPv4 address**: `10.0.0.10` and `11.0.0.10`
        * **IPv6 address**: `2000::2` and `2002::2`
1. Configure route on host1 to reach `11.0.0.0/24` network via `10.0.0.1`
1. Configure route on host1 to reach `2002::0/120` network via `2000::1`
1. Configure route on host2 to reach `10.0.0.0/24` network via `11.0.0.1`
1. Configure route on host2 to reach `2000::0/120` network via `2002::1`
1. Ping between hosts for both IPv4 and IPv6
### Test Result Criteria
#### Test Pass Criteria
Pings should go through fastpath.
Verify using `ovs-appctl plugin/debug l3host` and `ovs-appctl plugin/debug l3v6host`
The hit bit in ASIC entries for these hosts should be **y** indicating fast path traffic for these hosts were hit.
#### Test Fail Criteria

##  IPv4 static routes configuration
### Objective
Test case checks if ping works when IPv4 static routes are configured.
### Requirements
- Physical Switch/Workstations Test setup
- **FT File**: `ops-quagga/zebra/test/test_zebra_ft_l3static.py` (Static Routes IPv4)

### Setup
#### Topology Diagram

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
Configure a topology with 2 hosts and 2 switches, connected as shown in Topology Diagram.

**Host 1 Configuration**
```
ip addr add 10.0.10.1/24 dev eth1
ip route add 10.0.20.0/24 via 10.0.10.2
ip route add 10.0.30.0/24 via 10.0.10.2
```

**Host 2 Configuration**
```
ip addr add 10.0.30.1/24 dev eth1
ip route add 10.0.10.0/24 via 10.0.30.2
ip route add 10.0.20.0/24 via 10.0.30.2
```

**Switch 1 Configuration**
Run VTYSH Commands:
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

Run ovs-vsctl commands:
```
/usr/bin/ovs-vsctl set interface 1 user_config:admin=up
/usr/bin/ovs-vsctl set interface 2 user_config:admin=up
```

**Switch 2 Configuration**
Run VTYSH commands:
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

Run ovs-vsctl commands:
```
/usr/bin/ovs-vsctl set interface 1 user_config:admin=up
/usr/bin/ovs-vsctl set interface 2 user_config:admin=up
```

### Test Result Criteria
#### Test Pass Criteria
Ping from Host 1 to Host 2 works fine
#### Test Fail Criteria

## Delete IPv4 static routes
### Objective
Test case checks if ping fails when IPv4 static routes are deleted.
### Requirements
- Physical Switch/Workstations Test setup
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py` (L3 Interface & Fastpath for Directly Connected Hosts)

### Setup
#### Topology Diagram
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
Delete a route from one of the switches
Switch 1 Command:
```
root(config): no ip route 10.0.30.0/24 10.0.20.2
```
### Test Result Criteria
#### Test Pass Criteria
* Ping from Host 1 to Host 2 fails.
* If the routes gets added again, ping passes implying that the routes get correctly deleted
from the kernel and the database.
#### Test Fail Criteria

##  IPv6 static routes configuration
### Objective
Test case checks if ping works when IPv6 static routes are configured.
### Requirements
- Physical Switch/Workstations Test setup
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py` (L3 Interface & Fastpath for Directly Connected Hosts)

### Setup
#### Topology Diagram

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
Configure a topology with 2 hosts and 2 switches, connected as shown in
Toplogy Diagram.

**Host 1 Configuration**
```
ip addr add 2000::1/120 dev eth1
ip route add 2001::0/120 via 2000::2
ip route add 2002::0/120 via 2000::2
```

**Host 2 Configuration**
```
ip addr add 2002::1/120 dev eth1
ip route add 2000::0/120 via 2002::2
ip route add 2001::0/120 via 2002::2
```

**Switch 1 Configuration**

Run VTYSH commands:
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

Run ovs-vsctl commands:
```
/usr/bin/ovs-vsctl set interface 1 user_config:admin=up
/usr/bin/ovs-vsctl set interface 2 user_config:admin=up
```

**Switch 2 Configuration**

Run VTYSH commands:
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

Run ovs/vsctl commands:
```
/usr/bin/ovs-vsctl set interface 1 user_config:admin=up
/usr/bin/ovs-vsctl set interface 2 user_config:admin=up
```

### Test Result Criteria
#### Test Pass Criteria
Ping6 from Host 1 to Host 2 works fine
#### Test Fail Criteria

##  Delete IPv6 static routes
### Objective
Test case checks if ping fails when IPv6 static routes are deleted.
### Requirements
- Physical Switch/Workstations Test setup
- **FT File**: `ops-openvswitch/test/test_openvswitch_ft_l3_fastpath_connected.py` (L3 Interface & Fastpath for Directly Connected Hosts)

### Setup
#### Topology Diagram

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
Delete a route from one of the switches
Switch 1 Command:
```
root(config): no ipv6 route 2002::0/120 2001::2
```
### Test Result Criteria
#### Test Pass Criteria
* Ping6 from Host 1 to Host 2 fails.
* If the routes are added again, ping will succeed. Which means that it was failing because the routes were deleted correctly from the database and the kernel.
#### Test Fail Criteria

