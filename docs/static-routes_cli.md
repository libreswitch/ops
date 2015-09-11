# Static routes

## Contents
- [Configuration commands](#configuration-commands)
	- [ip route](#ip-route)
	- [ipv6 route](#ipv6-route)
- [Display commands](#display-commands)
	- [show ip route](#show-ip-route)
	- [show ipv6 route](#show-ipv6-route)

## Configuration commands

###  ip route

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

IP route with nexthop (nexthop: 10.10.10.1):
```
hostname(config)# ip route 172.16.32.0/24 10.10.10.1
hostname(config)#
```
IP route with interface (interface: 32):
```
hostname(config)# ip route 172.16.32.0/24 32
hostname(config)#
```

###  ipv6 route

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

IP route with nexthop (nexthop: 2010:bda::):
```
hostname(config)# ipv6 route fde1:87a5:2185:a5fc::/64 2010:bda::
hostname(config)#
```
IP route with interface (interface: 32):
```
hostname(config)# ipv6 route fde1:87a5:2185:a5fc::/64 32
hostname(config)#
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
