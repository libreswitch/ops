#BGP Command Reference
=======================

##Contents
- [BGP configuration commands](#bgp-configuration-commands)
	- [router bgp](#router-bgp)
	- [bgp router-id](#bgp-router-id)
	- [IPv4 network](#ipv4-network)
	- [maximum-paths](#maximum-paths)
	- [timers bgp](#timers-bgp)
	- [IPv6 network](#ipv6-network)
	- [bgp fast-external-failover](#bgp-fast-external-failover)
	- [bgp log-neighbor-changes](#bgp-log-neighbor-changes)
	- [redistribute routes](#redistribute-routes)
	- [BGP neighbor commands](#bgp-neighbor-commands)
		- [neighbor remote-as](#neighbor-remote-as)
		- [neighbor description](#neighbor-description)
		- [neighbor password](#neighbor-password)
		- [neighbor timers](#neighbor-timers)
		- [neighbor allowas-in](#neighbor-allowas-in)
		- [neighbor remove-private-AS](#neighbor-remove-private-as)
		- [neighbor soft-reconfiguration inbound](#neighbor-soft-reconfiguration-inbound)
		- [neighbor shutdown](#neighbor-shutdown)
		- [neighbor peer-group](#neighbor-peer-group)
		- [neighbor route-map](#neighbor-route-map)
		- [neighbor advertisement-interval](#neighbor-advertisement-interval)
		- [neighbor ebgp-multihop](#neighbor-ebgp-multihop)
		- [neighbor filter-list](#neighbor-filter-list)
		- [neighbor prefix-list](#neighbor-prefix-list)
		- [neighbor soft-reconfiguration](#neighbor-soft-reconfiguration)
		- [neighbor ttl-security](#neighbor-ttl-security)
		- [neighbor update-source](#neighbor-update-source)
	- [as-path access-list](#as-path-access-list)
- [Route-map configuration commands](#route-map-configuration-commands)
	- [route-map](#route-map)
	- [Route-map match](#route-map-match)
		- [match prefix-list](#match-prefix-list)
	- [Route-map set](#route-map-set)
		- [set community](#set-community)
		- [set metric](#set-metric)
	- [Route-map description](#route-map-description)
- [IP prefix-list configuration commands](#ip-prefix-list-configuration-commands)
	- [IPv4 prefix-list](#ipv4-prefix-list)
	- [IPv6 prefix-list](#ipv6-prefix-list)
- [Community lists configuration commands](#community-lists-configuration-commands)
- [Extended community lists configuration commands](#extended-community-lists-configuration-commands)
- [Display commands](#display-commands)
	- [show ip bgp](#show-ip-bgp)
	- [show ip bgp summary](#show-ip-bgp-summary)
	- [show bgp neighbors](#show-bgp-neighbors)

## BGP configuration commands

### router bgp

To use the BGP feature, first configure the BGP router as shown below.

#### Syntax
```
[no] router bgp <asn>
```

#### Description
This command is used to configure the BGP router. The Autonomous System (AS) number is needed to configure the BGP router. The BGP protocol uses the AS number to detect whether the BGP connection is internal or external.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *asn*  | Required | 1 - 4294967295 | The AS number. |
| **no** | Optional | Literal | Destroys a BGP router with the specified AS number. |

#### Examples
```
s1(config)#router bgp 6001
s1(config)#no router bgp 6001
```

### bgp router-id
#### Syntax
```
[no] bgp router-id <A.B.C.D>
```

#### Description
This command specifies the BGP router-ID for a BGP router.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The IPv4 address. |
| **no** | Optional | Literal | Deletes the BGP router IP address. |

#### Examples
```
s1(config-router)# bgp router-id 9.0.0.1
s1(config-router)# no bgp router-id 9.0.0.1
```

### IPv4 network
#### Syntax
```
[no] network <A.B.C.D/M>
```

#### Description
This command adds the announcement network.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D/M*  | Required | A.B.C.D/M | IPv4 address with the prefix length.|
| **no** | Optional | Literal | Removes the announced network for the BGP router. |

#### Examples
The following configuration example shows that network 10.0.0.0/8 is announced to all neighbors:

```
s1(config-router)# network 10.0.0.0/8
s1(config)# do sh run
Current configuration:
!
router bgp 6001
     bgp router-id 9.0.0.1
     network 10.0.0.0/8
```

### maximum-paths
#### Syntax
```
[no] maximum-paths <num>
```

#### Description
This command sets the maximum number of paths for a BGP router.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *num*  | Required | 1-255 | Maximum number of paths. |
| **no** | Optional | Literal | Sets the maximum number of paths to the default value of 1. |


#### Examples
```
s1(config)# router bgp 6001
s1(config-router)# maximum-paths 5
```

### timers bgp
#### Syntax
```
[no] timers bgp <keepalive> <holdtime>
```

#### Description
This command sets the keepalive interval and hold time for a BGP router.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *Keepalive*  | Required | 0 - 65535 | The keepalive interval in seconds. |
| *holdtime* | Required| 0 - 65535 | Hold time in seconds. |
| **no** | Optional | Literal | Resets the keepalive and hold time values to their default values (60 seconds for the keepalive interval and 180 seconds for the hold time value).  |

#### Examples
```
s1(config)# router bgp 6001
s1(config-router)# timers bgp 60 30
```

### IPv6 network
#### Syntax
```
[no] network <X:X::X:X/M>
```

#### Description
This command advertises the IPv6 prefix network.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *X:X::X:X/M*  | Required | X:X::X:X/M | The IPv6 prefix address and prefix length. |
| **no** | Optional | Literal | Deletes the IPv6 prefix network. |

#### Examples
```
s1(config-router)# ipv6 bgp network 2001:1::1/64
s1(config-router)# no ipv6 bgp network 2001:1::1/64
```

### bgp fast-external-failover
#### Syntax
```
[no] bgp fast-external-failover
```

#### Description
This command is used to enable fast external failover for BGP directly connected peering sessions.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables BGP fast external failover. |

#### Examples
```
s1(config-router)# bgp fast-external-failover
s1(config-router)# no bgp fast-external-failover
```

### bgp log-neighbor-changes
#### Syntax
```
[no] bgp log-neighbor-changes
```

#### Description
This command enables logging of BGP neighbor resets and status changes (up and down).

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The IPv4 address. |
| **no** | Optional | Literal | Disables the logging of neighbor status changes. |

#### Examples
```
s1(config-router)# bgp log-neighbor-changes
s1(config-router)# no bgp log-neighbor-changes
```

### redistribute routes
#### Syntax
```
[no] redistribute <connected | static | ospf> route-map <name>
```
#### Description
This command configures the route redistribution of the specified protocol or kind into BGP; filtering the routes using the given route-map, if specified.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *name*  | Optional | String of maximum length 80 characters. | The route-map name. |
| **no** | Optional | Literal | Removes the redistribution of routes from BGP. |

#### Examples
```
s1(config)# router bgp 6001
s1(config-router)# redistribute kernel
s1(config-router)# redistribute connected
s1(config-router)# redistribute static
s1(config-router)# redistribute ospf
s1(config-router)# redistribute kernel route-map rm1
s1(config-router)# redistribute connected route-map rm1
s1(config-router)# redistribute static route-map rm1
s1(config-router)# redistribute ospf route-map rm1
```

### BGP neighbor commands
#### neighbor remote-as

##### Syntax
```
[no] neighbor <A.B.C.D> remote-as <asn>
```

##### Description
This command creates a neighbor whose remote-as is *asn*, an autonomous system number. Currently only IPv4 addresses are supported.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *asn* | Required| 1 - 4294967295 |  The autonomous system number of the peer. |
| **no** | Optional | Literal | Deletes a configured BGP peer. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# no neighbor 9.0.0.2 remote-as 6002
```

#### neighbor description
##### Syntax
```
[no] neighbor <A.B.C.D> description <text>
```

##### Description
This command sets the description for the peer.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *text* | Required| String of maximum length 80 characters. | Description of the peer. |
| **no** | Optional | Literal | Deletes the peer description. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 description peer1
```

#### neighbor password
##### Syntax
```
[no] neighbor <A.B.C.D> password <text>
```

##### Description
This command enables MD5 authentication on a TCP connection between BGP peers.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *text* | Required| String of maximum length 80 characters. | Password for the peer connection. |
| **no** | Optional | Literal | Disables authentication for the peer connection. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 password secret
```

#### neighbor timers
##### Syntax
```
[no] neighbor <A.B.C.D> timers <keepalive> <holdtimer>
```

##### Description
This command sets the keepalive interval and hold time for a specific BGP peer.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *Keepalive*  | Required | 0 - 65535 | The keepalive interval in seconds. |
| *holdtime* | Required| 0 - 65535 | The hold time in seconds. |
| **no** | Optional | Literal | Resets the keepalive and hold time values to their default values which are 0.  |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 timers 20 10
```

#### neighbor allowas-in
##### Syntax
```
[no] neighbor <A.B.C.D> allowas-in <val>
```

##### Description
This command specifies an allow-as-in occurrence number for an AS to be in the AS path. Issue the `no` command to clear the state.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *val* | Required| 1-10| Number of times BGP allows an instance of AS to be in the AS_PATH. |
| **no** | Optional | Literal | Clears the state. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 allowas-in 2
```

#### neighbor remove-private-AS

##### Syntax
```
[no] neighbor <A.B.C.D> remove-private-AS
```

##### Description
This command removes private AS numbers from the AS path in outbound routing updates.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| **no** | Optional | Literal |Resets to a cleared state (default). |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 remove-private-AS
```

#### neighbor soft-reconfiguration inbound
##### Syntax
```
[no] neighbor <A.B.C.D> soft-reconfiguration inbound
```

##### Description
This command enables software-based reconfiguration to generate inbound updates from a neighbor without clearing the BGP session. Issue the `no` command to clear this state.

##### Authority
admin

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| **no** | Optional | Literal |Resets to a cleared state (default). |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 soft-reconfiguration inbound
```

#### neighbor shutdown
##### Syntax
```
[no] neighbor <A.B.C.D> shutdown
```

##### Description
This command shuts down the peer. Use this syntax to preserve the neighbor configuration, but drop the BGP peer state.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| **no** | Optional | Literal | Deletes the neighbor state of the peer. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 shutdown
```

#### neighbor peer-group
##### Syntax
```
[no] neighbor <A.B.C.D> peer-group <name>
```

##### Description
This command assigns a neighbor to a peer-group.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *name*  | Required | String of maximum length 80 characters. | The peer-group name. |
| **no** | Optional | Literal | Removes the neighbor from the peer-group. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 peer-group pg1
```

#### neighbor route-map
##### Syntax
```
[no] neighbor <A.B.C.D> route-map <name> in|out
```
##### Description
This command applies a route-map on the neighbor for the direction given (in or out).

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *name*  | Required | String of maximum length of 80 characters. | The route-map name. |
| **no** | Optional | Literal |Removes the route-map for the neighbor. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 remote-as 6002
s1(config-router)# neighbor 9.0.0.2 route-map rm1 in
```

#### neighbor advertisement-interval

##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X> advertisement-interval <interval>
```

##### Description
This command sets the advertisement interval for route updates for a specified neighbor with an IPv4 or IPv6 address.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *interval* | Required| 0-600 |  The time interval for sending BGP routing updates in secs. |
| **no** | Optional | Literal | Deletes the advertisement interval for a configured BGP peer. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 9.0.0.2 advertisement-interval 400
s1(config-router)# no neighbor 9.0.0.2 advertisement-interval 400
```
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 2001:db8:0:1 advertisement-interval 400
s1(config-router)# no neighbor 2001:db8:0:1 advertisement-interval 400
```

#### neighbor ebgp-multihop
##### Syntax
```
[no] neighbor <A.B.C.D | X:X::X:X | peer_group_name> ebgp-multihop
```
##### Description
This command attempts BGP connections with external AS routers that are not directly connected.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Required | X:X::X:X | The peer IPv6 address. |
| *peer_group_name*  | Required | String of maximum length 80 characters. | The peer-group name. |
| **no** | Optional | Literal | Removes the ebgp-multihop configuration for the neighbor. |

##### Examples
```
s1(config-router)# neighbor 10.0.2.15 ebgp-multihop
s1(config-router)# no neighbor 10.0.2.15 ebgp-multihop
```

#### neighbor filter-list
##### Syntax
```
[no] neighbor <A.B.C.D|X:X::X:X|WORD> filter-list WORD (in|out)
```
##### Description
This command applies a filter list to the neighbor to filter incoming and outgoing routes.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |
| *WORD*  | Required | WORD | The AS_PATH access list name. |
| *in*  | Optional | in | Filters incoming routes. |
| *out*  | Optional | out | Filters outgoing routes. |

##### Examples
```
s1(config-router)# neighbor 172.16.1.1 filter-list 1 out
s1(config-router)# no neighbor 172.16.1.1 filter-list 1 out
```

#### neighbor prefix-list
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) prefix-list WORD (in|out)
```
##### Description
This command applies a prefix-list to the neighbor to filter updates to and from the neighbor.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |
| *WORD*  | Required | WORD | The name of a prefix list. |
| *in*  | Optional | in | Filters incoming routes. |
| *out*  | Optional | out | Filters outgoing routes. |

##### Examples
```
s1(config-router)# neighbor 10.23.4.2 prefix-list abc in
s1(config-router)# no neighbor 10.23.4.2 prefix-list abc in
```

#### neighbor soft-reconfiguration
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) soft-reconfiguration inbound
```
##### Description
This command allows an inbound soft reconfiguration of the neighbor.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |

##### Examples
```
s1(config-router)# neighbor 10.108.1.1 soft-reconfiguration inbound
s1(config-router)# no neighbor 10.108.1.1 soft-reconfiguration inbound
```

#### neighbor ttl-security
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) ttl-security hops <1-254>
```
##### Description
This command specifies the maximum number of hops to the BGP peer.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |
| *<1-254>*  | Required | 1-254 | The hop count. |

##### Examples
```
s1(config-router)# neighbor 10.1.1.1 ttl-security hops 2
s1(config-router)# no neighbor 10.1.1.1 ttl-security hops 2
```

#### neighbor update-source
##### Syntax
```
[no] neighbor (A.B.C.D|X:X::X:X|WORD) update-source (A.B.C.D|X:X::X:X|WORD)
```
##### Description
This command updates the neighbor's source address to use for the BGP session.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The peer IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The peer IPv6 address. |
| *WORD*  | Optional | WORD | The neighbor tag. |
| *A.B.C.D*  | Optional | A.B.C.D | The IPv4 address. |
| *X:X::X:X*  | Optional | X:X:X:X | The IPv6 address. |
| *WORD*  | Optional | WORD | The interface name. |

##### Examples
```
s1(config-router)# neighbor 10.0.0.1 update-source loopback0
s1(config-router)# no neighbor 10.0.0.1 update-source loopback0
```

### as-path access-list
#### Syntax
```
[no]  ip as-path access-list WORD <deny|permit> .LINE
```

#### Description
This command facilitates the configuration of access lists, based on autonomous system paths that control routing updates. Autonomous system paths are based on BGP autonomous paths information. Access lists are filters that restrict the routing information that a router learns or advertises to and from a neighbor. Multiple BGP peers or route maps can reference a single access list. These access lists can be applied to both inbound and outbound route updates. Each route update is passed through the access list. BGP applies each rule in the access list in the order it appears in the list. When a route matches a rule, the decision to permit the route through or deny the route from the filter is made, and no further rules are processed. A regular expression is a pattern used to match against an input string. In BGP, regular expression can be built to match information about an autonomous system path.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The access list name |
| **deny** | Required | Literal | Denies access for matching conditions. |
| **permit** | Required | Literal | Permits access for matching conditions. |
| *.LINE* | Required | String of maximum length 80 characters. | An autonomous system in the access list in the form of a regular expression. |
| **no** | Optional | Literal | Disables an access list rule. |

#### Examples
```
s1(config)#ip as-path access-list 1 permit _234_
s1(config)#ip as-path access-list 1 permit _345_
s1(config)#ip as-path access-list 1 deny any
```

## Route-map configuration commands

### route-map
#### Syntax
```
[no] route-map WORD <deny|permit> <order>
```

#### Description
This command configures the order of the entry in the route map name with either the permit or deny match policy.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The route map name. |
| *order*  | Required |1-65535| The order number of the route map. |
| **deny** | Required | Literal | Denies the order of the entry. |
| **permit** | Required | Literal | Permits the order of the entry. |
| **no** | Optional | Literal | Deletes the route map. |

#### Examples
```
s1(config)# route-map rm1 deny 1
```

### Route-map match
#### match prefix-list

##### Syntax
```
[no] match ip address prefix-list WORD
```

##### Description
This command configures a match clause for the route map to distribute any routes with a destination network number address that is permitted by a prefix-list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The IP prefix list name. |
| **no** | Optional | Literal | Deletes the match clause for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# match ip address prefix-list PLIST1
```

### Route-map set
#### Syntax
```
Route-map Command: [no] set community <AA:NN> [additive]
Route-map Command: [no] set metric <val>
```

#### Description
The `set community` command sets the BGP community attribute. The `set metric` command sets the BGP attribute MED.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *AA:NN*  | Required | AS1:AS2 where AS is an integer in the range <1-4294967295>. | Sets the BGP community attribute. |
| *val*  | Required | Integer in the range <0-4294967295>.  | Sets the metric value. |
| **no** | Optional | Literal | Clears the community attribute. |

#### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# set community 6001:7002 additive
s1(config-route-map)# set metric 100
s1(config-route-map)# no set metric 100
```

### Route-map description
#### Syntax
```
Route-map Command: [no] description <text>
```

#### Description
This command sets the route-map description.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *text*  | Required | String of maximum length 80 characters. | The route-map description. |
| **no** | Optional | Literal | Clears the description for the route map. |

#### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# description rmap-mcast
```

### Route-map call
#### Syntax
```
[no] call WORD
```
#### Description
This command jumps to another route map after match and set.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The target route map name. |
| **no** | Optional | Literal | Disables jumping to another route map. |

#### Examples
```
s1(config-route-map)# call rmap
s1(config-route-map)# no call
```

### Route-map continue
#### Syntax
```
[no] continue <1-65535>
```

#### Description
This command continues onto a different entry within the route map.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-65535>*  | Required | 1-65535 | The route map entry sequence number. |
| **no** | Optional | Literal | Disables continuing onto a different entry. |

#### Examples
```
s1(config-route-map)# continue 300
s1(config-route-map)# no continue 300
s1(config-route-map)# no continue
```

## IP prefix-list configuration commands
###  IPv4 prefix-list
#### Syntax
```
[no] ip prefix-list WORD seq <num> (deny|permit) <A.B.C.D/M|any>
[no] ip prefix-list WORD seq <num> (deny|permit) A.B.C.D/M le <0-32> ge <0-32>
[no] ip prefix-list WORD seq <num> (deny|permit) A.B.C.D/M ge <0-32>
[no] ip prefix-list WORD seq <num> (deny|permit) A.B.C.D/M le <0-32>
```

#### Description
The `ip prefix-list` command provides a powerful prefix-based filtering mechanism. It has prefix length range and sequential number specifications. You can add or delete prefix-based filters to arbitrary points of a prefix-list by using a sequential number specification. If `no ip prefix-list` is specified, it acts as a permit. If the  `ip prefix-list` is defined, and no match is found, the default deny is applied.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *name*  | Required | String of maximum length 80 characters. | The IP prefix-list name. |
| *num*  | Required | 1-4294967295 | The sequence number. |
| *A.B.C.D/M*  | Required | A.B.C.D/M | The IPv4 prefix. |
| *0-32*  | Required | 0-32 | Minimum prefix length to be matched. |
| *0-32*  | Required | 0-32 | Maximum prefix length to be matched. |
| **no** | Optional | Literal |Deletes the IP prefix-list. |

#### Examples
```
s1(config)# ip prefix-list PLIST1 seq 5 deny 11.0.0.0/8
s1(config)# ip prefix-list PLIST2 seq 10 permit 10.0.0.0/8
s1(config)# no ip prefix-list PLIST1 seq 5 deny 11.0.0.0/8
s1(config)# no ip prefix-list PLIST2
```
###  IPv6 prefix-list
#### Syntax
```
[no] ipv6 prefix-list WORD description .LINE
[no] ipv6 prefix-list WORD seq <num> <deny|permit> <X:X::X:X/M|any>
[no] ipv6 prefix-list WORD seq <num> <deny|permit> <X:X::X:X/M> ge <length>
[no] ipv6 prefix-list WORD seq <num> <deny|permit> <X:X::X:X/M> ge <length> le <length>
[no] ipv6 prefix-list WORD seq <num> <deny|permit> <X:X::X:X/M> le <length>
```

#### Description
The `ipv6 prefix-list` command provides IPv6 prefix-based filtering mechanism. Descriptions may be added to prefix lists. The `description` command adds a description to the prefix list. The `ge` command specifies prefix length, and the prefix list is applied if the prefix length is greater than or equal to the `ge` prefix length. The `le` command specifies prefix length, and the prefix list is be applied if the prefix length is less than or equal to the `le` prefix length. If `no ipv6 prefix-list` is specified, it acts as permit. If `ipv6 prefix-list` is defined, and no match is found, the default deny is applied.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length of 80 characters. | The IP prefix-list name. |
| *num*  | Required | 1-4294967295 | The sequence number. |
| *.LINE*  | Required | String of maximum length 80 characters. | The prefix list description |
| *X:X::X:X/M*  | Required | X:X::X:X/M | The IPv6 prefix. |
| *length* | Required | 0-128 | The prefix length. |
| **no** | Optional | Literal | Deletes the IPv6 prefix-list. |

#### Examples
```
s1(config)# ipv6 prefix-list COMMON-PREFIXES description prefixes
s1(config)# no ipv6 prefix-list COMMON-PREFIXES
s1(config)# ipv6 prefix-list COMMON-PREFIXES seq 5 permit 2001:0DB8:0000::/48
s1(config)# ipv6 prefix-list COMMON-PREFIXES seq 10 deny any
s1(config)# ipv6 prefix-list COMMON-PREFIXES seq 15 permit 2001:0DB8:0000::/48 ge 64
s1(config)# no ipv6 prefix-list COMMON-PREFIXES
s1(config)# ipv6 prefix-list PEER-A-PREFIXES seq 5 permit 2001:0DB8:AAAA::/48 ge 64 le 64
s1(config)# no ipv6 prefix-list PEER-A-PREFIXES
```


## Community lists configuration commands

#### Syntax
```
[no] ip  community-list WORD <deny|permit> .LINE
```

#### Description
This command defines a new community list. LINE is a string expression of the communities attribute. LINE can include a regular expression to match the communities attribute in BGP updates. The community is compiled into a community structure. Multiple community lists can be defined under the same name. In that case, the match happens in user-defined order. Once the community list matches to the communities attribute in BGP updates, it returns a permit or deny based on the community list definition. When there is no matched entry, deny is returned. When the community is empty, the system matches to any routes.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The community list name. |
| **deny** | Required | Literal | Denies access for matching conditions. |
| **permit** | Required | Literal | Permits access for matching conditions. |
| *.LINE* | Required | String of maximum length 80 characters. | Community numbers specified as regular expressions. |
| **no** | Optional | Literal | Deletes the rule for the specified community. |

#### Examples
```
S1(config)#ip community-list EXPANDED permit [1-2]00
S1(config)#ip community-list ANY-COMMUNITIES deny ^0:.*_
S1(config)#ip community-list ANY-COMMUNITIES deny ^65000:.*_
S1(config)#ip community-list ANY-COMMUNITIES permit .*
```


## Extended community lists configuration commands
#### Syntax
```
[no] ip extcommunity-list WORD <deny|permit> .LINE
```
#### Description
This command defines a new extended community list.  LINE is a string expression of the extended communities attribute, and can include a regular expression to match the extended communities attribute in BGP updates.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of maximum length 80 characters. | The extended community list name. |
| *.LINE*  | Required | String of maximum length 80 characters. | The string expression of the extended communities attribute. |
| **deny** | Required | Literal | Denies access for matching conditions. |
| **permit** | Required | Literal | Permits access for matching conditions. |
| **no** | Optional | Literal | Deletes the extended community list. |

#### Examples
```
s1(config)# ip extcommunity-list expanded ROUTES permit REGULAR_EXPRESSION
s1(config)# no ip extcommunity-list expanded ROUTES
```

##Display commands

### show ip bgp
#### Syntax
```
show ip bgp [A.B.C.D][A.B.C.D/M]
```

#### Description
This command displays BGP routes from the BGP route table. When no route is specified, all IPv4 routes are displayed.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Optional | A.B.C.D | The IPv4 prefix. |
| *A.B.C.D/M*  | Optional | A.B.C.D/M | The IPv4 prefix with prefix length. |

#### Examples
```ditaa
s1# show ip bgp
Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
              i internal, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete

Local router-id 9.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 11.0.0.0/8       0.0.0.0                  0      0  32768  i
*> 12.0.0.0/8       10.10.10.2               0      0      0 2 5 i
*  12.0.0.0/8       20.20.20.2               0      0      0 3 5 i
*  12.0.0.0/8       30.30.30.2               0      0      0 4 5 i
Total number of entries 4
```

### show ip bgp summary
#### Syntax
```
show ip bgp summary
```

#### Description
The command provides a summary of the BGP neighbor status.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```ditaa
s1# show ip bgp summary
BGP router identifier 9.0.0.1, local AS number 1
RIB entries 2
Peers 1

Neighbor             AS MsgRcvd MsgSent Up/Down  State
9.0.0.2               2       4       5 00:00:28 Established
```

###  show bgp neighbors
#### Syntax
```
show bgp neighbors
```

#### Description
This command displays detailed information about BGP neighbor connections.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```ditaa
s1# show bgp neighbors
  name: 9.0.0.2, remote-as: 6002
    state: undefined
    shutdown: yes
    description: peer1
    capability: undefined
    local_as: undefined
    local_interface: undefined
    inbound_soft_reconfiguration: yes
    maximum_prefix_limit: undefined
    tcp_port_number: undefined
    statistics:
  name: pg1, remote-as: undefined
    state: undefined
    shutdown: undefined
    description: undefined
    capability: undefined
    local_as: undefined
    local_interface: undefined
    inbound_soft_reconfiguration: undefined
    maximum_prefix_limit: undefined
    tcp_port_number: undefined
    statistics:
```
## CLI 
Click [here](http://www.openswitch.net/documents/user/bpg_cli) for CLI commands related to the BGP feature.
