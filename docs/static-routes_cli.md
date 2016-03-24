# Static routes

## Contents
- [Configuration commands](#configuration-commands)
	- [ip route](#ip-route)
	- [ipv6 route](#ipv6-route)
- [Display commands](#display-commands)
	- [show ip route](#show-ip-route)
	- [show ipv6 route](#show-ipv6-route)
- [References](#references)
## Configuration commands

### ip route

##### Syntax
Under the config context

`[no] ip route <destination> <nexthop | interface> [<distance>]`

##### Description
This command configures IPv4 static routes.

##### Authority
Admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *destination*  | Required | A.B.C.D/M |	The address and mask |
| *nexthop*  | Required | A.B.C.D |	The address of the nexthop |
| *interface*  | Required |String |	The name of the interface |
| *distance*  | Optional |1-255 |	Distance for this route. Default is 1 for static routes. |
| **no** | Optional | Literal | Removes the specified configuration for an IPv4 address |

##### Examples

Configuring IPv4 route with nexthop as an IP address (nexthop: 10.10.10.1):
```
hostname(config)# ip route 172.16.32.0/24 10.10.10.1
```
Configuring IPv4 route with nexthop as an interface (interface: 32):
```
hostname(config)# ip route 172.16.32.0/24 32
```
Configuring IPv4 route with nexthop as a VLAN interface (interface: vlan10):
```
hostname(config)# interface vlan10
hostname(config-if-vlan)# ip address 10.10.10.2/24
hostname(config-if-vlan)# exit
hostname(config)# ip route 172.16.32.0/24 vlan10
```
Configuring IPv4 route with nexthop as a subinterface (interface: 1.1):
```
hostname(config)# interface 1.1
hostname(config-subif)# ip address 10.10.10.3/24
hostname(config-subif)# exit
hostname(config)# ip route 172.16.32.0/24 1.1
```
Configuring IPv4 route with nexthop as a L3 LAG interface (interface: lag10):
```
hostname(config)# interface lag10
hostname(config-lag-if)# ip address 10.10.10.3/24
hostname(config-lag-if)# exit
hostname(config)# ip route 172.16.32.0/24 lag10
```
### ipv6 route

##### Syntax
Under the config context

`[no] ipv6 route <destination> <nexthop | interface> [<distance>]`

##### Description
This command configures IPv6 static routes.

##### Authority
Admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *destination*  | Required. | X:X::X:X/P  |	The address and prefix length. |
| *nexthop*  | Required. | X:X::X:X|	The address of the nexthop. |
| *interface*  | Required. |String |	The name of the interface. |
| *distance*  | Optional. |1-255 |	Distance for this route. Default is 1 for static routes. |
| **no** | Optional | Literal | Removes the specified configuration for an IPv6 address |

##### Examples

Configuring IPv6 route with nexthop as an IP address (nexthop: 2010:bda::):
```
hostname(config)# ipv6 route fde1:87a5:2185:a5fc::/64 2010:bda::
```
Configuring IPv6 route with nexthop as an interface (interface: 32):
```
hostname(config)# ipv6 route fde1:87a5:2185:a5fc::/64 32
```
Configuring IPv6 route with nexthop as a VLAN interface (interface: vlan10):
```
hostname(config)# interface vlan10
hostname(config-if-vlan)# ipv6 address 2001::1/120
hostname(config-if-vlan)# exit
hostname(config)# ipv6 route fde1:87a5:2185:a5fc::/64 vlan10
```
Configuring IPv6 route with nexthop as a subinterface (interface: 1.1):
```
hostname(config)# interface 1.1
hostname(config-subif)# ipv6 address 2001::2/120
hostname(config-subif)# exit
hostname(config)# ipv6 route fde1:87a5:2185:a5fc::/64 1.1
```
Configuring IPv6 route with nexthop as a L3 LAG interface (interface: lag10):
```
hostname(config)# interface lag10
hostname(config-lag-if)# ipv6 address 2001::3/120
hostname(config-lag-if)# exit
hostname(config)# ipv6 route fde1:87a5:2185:a5fc::/64 lag10
```

## Display commands

### show ip route

##### Syntax
Under privileged mode

`show ip route`

#### Description
This command displays the routing table.

#### Authority
Operator

##### Parameters

None

##### Example
```
hostname# show ip route

Displaying ipv4 routes selected for forwarding

'[x/y]' denotes [distance/metric]

10.10.10.0/24,  1 unicast next-hops
        via  1,  [0/0],  connected
172.16.32.0/24,  1 unicast next-hops
        via  10.10.10.1,  [1/0],  static
```

### show ipv6 route

##### Syntax
Under privileged mode

`show ipv6 route`

#### Description
This command displays the routing table.

#### Authority
Operator

##### Parameters

None

##### Example
```
hostname# show ipv6 route

Displaying ipv6 routes selected for forwarding

'[x/y]' denotes [distance/metric]

fde1:87a5:2185:a5fc::/64,  1 unicast next-hops
        via  2010:bda::,  [1/0],  static
2010:bda::/64,  1 unicast next-hops
        via  2,  [0/0],  connected

```
## References
* [Layer 3 Design](layer3_design)
* [Layer 3 User Guide](layer3_user_guide)
* [Interface VLAN](layer3_interface_cli)
* [Subinterface](sub-interfaces_cli)
* [LAG](interface_cli)