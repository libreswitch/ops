#eBGP Command Reference
=======================

##Contents
- [eBGP configuration commands](#eBGP-configuration-commands)
	- [router bgp](#router-bgp)
	- [bgp router-id](#bgp-router-id)
	- [IPv4 network](#ipv4-network)
	- [maximum-paths](#maximum-paths)
	- [timers bgp](#timers-bgp)
	- [IPv6 network](#ipv6-network)
	- [bgp fast-external-failover](#bgp-fast-external-failover)
	- [bgp log-neighbor-changes](#bgp-log-neighbor-changes)
	- [redistribute routes](#redistribute-routes)
	- [eBGP neighbor commands](#eBGP-neighbor-commands)
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
	- [as-path access-list](#as-path-access-list)
- [Route-map configuration commands](#route-map-configuration-commands)
	- [route-map](#route-map)
	- [Route-map match](#route-map-match)
		- [match as-path](#match-as-path)
		- [match community](#match-community)
		- [match community exact-match](#match-community-exact-match)
		- [match extcommunity](#match-extcommunity)
		- [match ip address prefix-list](#match-ip-address-prefix-list)
		- [match ipv6 address prefix-list](#match-ipv6-address-prefix-list)
		- [match ipv6 next-hop](#match-ipv6-next-hop)
		- [match metric](#match-metric)
		- [match origin](#match-origin)
		- [match probability](#match-probability)
	- [Route-map set](#route-map-set)
		- [set aggregator](#set-aggregator)
		- [set as-path exclude](#set-as-path-exclude)
		- [set as-path prepend](#set-as-path-prepend)
		- [set atomic-aggregate](#set-atomic-aggregate)
		- [set comm-list delete](#set-comm-list-delete)
		- [set community](#set-community)
		- [set community rt](#set-community-rt)
		- [set extcommunity soo](#set-extcommunity-soo)
		- [set ipv6 next-hop global](#set-ipv6-next-hop-global)
		- [set local-preference](#set-local-preference)
		- [set metric](#set-metric)
		- [set origin](#set-origin)
		- [set weight](#set-weight)
	- [Route-map description](#route-map-description)
	- [Route-map call](#route-map-call)
	- [Route-map continue](#route-map-continue)
- [IP prefix-list configuration commands](#ip-prefix-list-configuration-commands)
	- [IPv4 prefix-list](#ipv4-prefix-list)
	- [IPv6 prefix-list](#ipv6-prefix-list)
- [Community lists configuration commands](#community-lists-configuration-commands)
- [Extended community lists configuration commands](#extended-community-lists-configuration-commands)
- [Display commands](#display-commands)
	- [show ip bgp](#show-ip-bgp)
	- [show ip bgp summary](#show-ip-bgp-summary)
	- [show bgp neighbors](#show-bgp-neighbors)
	- [show ip bgp route-map WORD](#show-ip-bgp-route-map-word)
	- [show ip prefix list](#show-ip-prefix-list)
	- [show ip prefix-list WORD seq num](#show-ip-prefix-list-word-seq-num)
	- [show ip prefix list detail WORD](#show-ip-prefix-list-detail-word)
	- [show ip prefix list summary WORD](#show-ip-prefix-list-summary-word)
	- [show ipv6 prefix list](#show-ipv6-prefix-list)
	- [show ipv6 prefix list WORD](#show-ipv6-prefix-list-word)
	- [show ipv6 prefix list WORD seq num](#show-ipv6-prefix-list-word-seq-num)
	- [show ipv6 prefix list detail](#show-ipv6-prefix-list-detail)
	- [show ipv6 prefix list detail WORD](#show-ipv6-prefix-list-detail-word)
	- [show ipv6 prefix list summary](#show-ipv6-prefix-list-summary)
	- [show ipv6 prefix list summary WORD](#show-ipv6-prefix-list-summary-word)
	- [show ipv6 prefix list WORD X:X::X:X/M](#show-ipv6-prefix-list-word-xxxxm)
	- [show ipv6 prefix list WORD X:X::X:X/M first match](#show-ipv6-prefix-list-word-xxxxm-first-match)
	- [show ipv6 prefix list WORD X:X::X:X/M longer](#show-ipv6-prefix-list-word-xxxxm-longer)
	- [show ip community-list](#show-ip-community-list)
	- [show ip extcommunity list](#show-ip-extcommunity-list)
	- [show as-path access list](#show-as-path-access-list)
	- [show as-path access list WORD](#show-as-path-access-list-word)

## eBGP configuration commands

### router bgp

To use the eBGP feature, first configure the eBGP router as shown below.

#### Syntax
```
[no] router bgp <asn>
```

#### Description
This command is used to configure the eBGP router. The Autonomous System (AS) number is needed to configure the eBGP router. The BGP protocol uses the AS number to detect whether the BGP connection is internal or external.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *asn*  | Required | 1 - 4294967295 | The AS number. |
| **no** | Optional | Literal | Destroys an eBGP router with the specified AS number. |

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
This command specifies the eBGP router-ID for an eBGP router.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *A.B.C.D*  | Required | A.B.C.D | The IPv4 address. |
| **no** | Optional | Literal | Deletes the eBGP router IP address. |

#### Examples
```
s1(config-router)# bgp router-id 10.1.2.1
s1(config-router)# no bgp router-id 10.1.2.1
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
| **no** | Optional | Literal | Removes the announced network for the eBGP router. |

#### Examples
The following configuration example shows that network 10.1.2.0/24 is announced to all neighbors:

```
s1(config-router)# network 10.1.2.0/24
s1(config)# do sh run
Current configuration:
!
router bgp 6001
     bgp router-id 10.1.2.1
     network 10.1.2.0/24
```

### maximum-paths
#### Syntax
```
[no] maximum-paths <num>
```

#### Description
This command sets the maximum number of paths for an eBGP router.

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
This command sets the keepalive interval and hold time for an eBGP router.

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
This command is used to enable fast external failover for eBGP directly connected peering sessions.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables eBGP fast external failover. |

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
This command enables logging of eBGP neighbor resets and status changes (up and down).

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
This command configures the route redistribution of the specified protocol or kind into eBGP; filtering the routes using the given route-map, if specified.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *name*  | Optional | String of maximum length 80 characters. | The route-map name. |
| **no** | Optional | Literal | Removes the redistribution of routes from eBGP. |

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

### eBGP neighbor commands
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
| **no** | Optional | Literal | Deletes a configured eBGP peer. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# no neighbor 10.1.2.1 remote-as 6002
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
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# neighbor 10.1.2.1 description peer1
```

#### neighbor password
##### Syntax
```
[no] neighbor <A.B.C.D> password <text>
```

##### Description
This command enables MD5 authentication on a TCP connection between eBGP peers.

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
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# neighbor 10.1.2.1 password secret
```

#### neighbor timers
##### Syntax
```
[no] neighbor <A.B.C.D> timers <keepalive> <holdtimer>
```

##### Description
This command sets the keepalive interval and hold time for a specific eBGP peer.

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
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# neighbor 10.1.2.1 timers 20 10
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
| *val* | Required| 1-10| Number of times eBGP allows an instance of AS to be in the AS_PATH. |
| **no** | Optional | Literal | Clears the state. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# neighbor 10.1.2.1 allowas-in 2
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
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# neighbor 10.1.2.1 remove-private-AS
```

#### neighbor soft-reconfiguration inbound
##### Syntax
```
[no] neighbor <A.B.C.D> soft-reconfiguration inbound
```

##### Description
This command enables software-based reconfiguration to generate inbound updates from a neighbor without clearing the eBGP session. Issue the `no` command to clear this state.

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
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# neighbor 10.1.2.1 soft-reconfiguration inbound
```

#### neighbor shutdown
##### Syntax
```
[no] neighbor <A.B.C.D> shutdown
```

##### Description
This command shuts down the peer. Use this syntax to preserve the neighbor configuration, but drop the eBGP peer state.

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
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# neighbor 10.1.2.1 shutdown
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
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# neighbor 10.1.2.1 peer-group pg1
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
s1(config-router)# neighbor 10.1.2.1 remote-as 6002
s1(config-router)# neighbor 10.1.2.1 route-map rm1 in
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
| *interval* | Required| 0-600 |  The time interval for sending eBGP routing updates in secs. |
| **no** | Optional | Literal | Deletes the advertisement interval for a configured eBGP peer. |

##### Examples
```
s1(config)# router bgp 6001
s1(config-router)# neighbor 10.1.2.1 advertisement-interval 400
s1(config-router)# no neighbor 10.1.2.1 advertisement-interval 400
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
This command attempts eBGP connections with external AS routers that are not directly connected.

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
s1(config-router)# neighbor 10.1.2.1 ebgp-multihop
s1(config-router)# no neighbor 10.1.2.1 ebgp-multihop
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
s1(config-router)# neighbor 192.18.1.1 filter-list 1 out
s1(config-router)# no neighbor 192.18.1.1 filter-list 1 out
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
s1(config-router)# neighbor 10.1.4.2 prefix-list abc in
s1(config-router)# no neighbor 10.1.4.2 prefix-list abc in
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
This command specifies the maximum number of hops to the eBGP peer.

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
### as-path access-list
#### Syntax
```
[no]  ip as-path access-list WORD <deny|permit> .LINE
```

#### Description
This command facilitates the configuration of access lists, based on autonomous system paths that control routing updates. Autonomous system paths are based on eBGP autonomous paths information. Access lists are filters that restrict the routing information that a router learns or advertises to and from a neighbor. Multiple eBGP peers or route maps can reference a single access list. These access lists can be applied to both inbound and outbound route updates. Each route update is passed through the access list. eBGP applies each rule in the access list in the order it appears in the list. When a route matches a rule, the decision to permit the route through or deny the route from the filter is made, and no further rules are processed. A regular expression is a pattern used to match against an input string. In eBGP, regular expression can be built to match information about an autonomous system path.

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
#### match as-path
##### Syntax
```
[no] match as-path WORD
```

##### Description
This command matches an eBGP autonomous system path access list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The AS path access list name. |
| **no** | Optional | Literal | Deletes the AS path access list entry. |

##### Examples
```
s1(config-route-map)# match as-path WORD
s1(config-route-map)# no match as-path WORD
s1(config-route-map)# no match as-path
```

#### match community
##### Syntax
```
[no] match community (<1-99>|<100-500>|WORD)
```

##### Description
This command matches an eBGP community. Use this command in route-map configuration mode.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-99>*  | Optional | 1-99 | The community list number (standard). |
| *<100-500>*  | Optional | 100-500 | The community list number (expanded). |
| *WORD*  | Optional | WORD | The community list name. |
| **no** | Optional | Literal | Removes the match community entry. |

##### Examples
```
s1(config-route-map)# match community 10
s1(config-route-map)# no match community 10
s1(config-route-map)# no match community
```

#### match community exact-match
##### Syntax
```
[no] match community (<1-99>|<100-500>|WORD) exact-match
```

##### Description
This command matches an eBGP community with an exact match of communities.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-99>*  | Optional | 1-99 | The community list number (standard). |
| *<100-500>*  | Optional | 100-500 | The community list number (expanded). |
| *WORD*  | Optional | WORD | The community list name. |
| *Exact-match*  | Required | exact-match | Does exact matching of communities. |
| **no** | Optional | Literal | Removes the match community exact-match entry. |

##### Examples
```
s1(config-route-map)# match community c1 exact-match
s1(config-route-map)# no match community c1 exact-match
```

#### match extcommunity
##### Syntax
```
[no] match extcommunity (<1-99>|<100-500>|WORD)
```

##### Description
This command matches the eBGP extended community list attributes. Use this command in route-map mode.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<1-99>*  | Optional | 1-99 | The extended community list number (standard). |
| *<100-500>*  | Optional | 100-500 | The extended community list number (expanded). |
| *WORD*  | Optional | WORD | The extended community list name. |
| **no** | Optional | Literal | Removes the match extcommunity entry. |

##### Examples
```
s1(config-route-map)# match extcommunity 10
s1(config-route-map)# no match extcommunity 10
s1(config-route-map)# no match extcommunity
```

#### match ip address prefix-list
##### Syntax
```
[no] match ip address prefix-list WORD
```

##### Description
To distribute any routes that have a destination network number address that is permitted by a prefix list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The IP prefix list name. |
| **no** | Optional | Literal | Removes the match ip address prefix-list entry. |

##### Examples
```
s1(config-route-map)# match ip address prefix-list pl1
s1(config-route-map)# no match ip address prefix-list pl1
s1(config-route-map)# no match ip address prefix-list
```

#### match ipv6 address prefix-list
##### Syntax
```
[no] match ipv6 address prefix-list WORD
```

##### Description
This command distributes IPv6 routes that have a prefix specified in an IPv6 prefix list.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | The IPv6 prefix list. |
| **no** | Optional | Literal | Removes the match ipv6 address prefix-list entry. |

##### Examples
```
s1(config-route-map)# match ipv6 address prefix-list p1
s1(config-route-map)# no match ipv6 address prefix-list p1
```

#### match ipv6 next-hop
##### Syntax
```
[no] match ipv6 next-hop X:X::X:X
```

##### Description
This command distributes IPv6 routes that have a specified next hop.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *X:X::X:X*  | Required | X:X::X:X | The IPv6 address of the next hop. |
| **no** | Optional | Literal | Removes the match ipv6 next-hop entry. |

##### Examples
```
s1(config-route-map)# match ipv6 next-hop 2001::1
s1(config-route-map)# no match ipv6 next-hop 2001::1
```

#### match metric
##### Syntax
```
[no] match metric <0-4294967295>
```

##### Description
This command redistributes routes with the specified metric.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<0-4294967295>*  | Required | Integer in the range <0-4294967295>. | The metric value. |
| **no** | Optional | Literal | Removes the match metric entry. |

##### Examples
```
s1(config-route-map)# match metric 400
s1(config-route-map)# no match metric 400
s1(config-route-map)# no match metric
```

#### match origin
##### Syntax
```
[no] match origin (egp|igp|incomplete)
```

##### Description
This command matches eBGP routes based on the origin of the specified route.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *EGP*  | Optional | egp | Remote egp. |
| *IGP*  | Optional | igp | Local igp .|
| *Incomplete*  | Optional | incomplete | Unknown heritage. |
| **no** | Optional | Literal | Removes the match origin entry. |

##### Examples
```
s1(config-route-map)# match origin egp
s1(config-route-map)# no match origin egp
s1(config-route-map)# no match origin
```

#### match probability
##### Syntax
```
[no] match probability <0-100>
```

##### Description
This command matches the portion of eBGP routes defined by a percentage value.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax | Description          |
|-----------|----------|----------------------|
| *<0-100>*  | Required | 0-100 | Percentage of routes. |
| **no** | Optional | Literal | Removes the match probability entry. |

##### Examples
```
s1(config-route-map)# match probability 50
s1(config-route-map)# no match probability 50
s1(config-route-map)# no match probability
```

### Route-map set
#### Syntax
```
Route-map Command: [no] set community <AA:NN> [additive]
Route-map Command: [no] set metric <val>
```

#### Description
The `set community` command sets the eBGP community attribute. The `set metric` command sets the eBGP attribute MED.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *AA:NN*  | Required | AS1:AS2 where AS is an integer in the range <1-4294967295>. | Sets the eBGP community attribute. |
| *val*  | Required | Integer in the range <0-4294967295>.  | Sets the metric value. |
| **no** | Optional | Literal | Clears the community attribute. |

#### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# set community 6001:7002 additive
s1(config-route-map)# set metric 100
s1(config-route-map)# no set metric 100
```

#### set aggregator
##### Syntax
```
[no] set aggregator as <value> <A.B.C.D>
```

##### Description
This command sets the originating AS of an aggregated route. The value specifies from which AS the aggregate route originated. The range is from 1 to 4294967295. The `set-aggregator-ip` value must also be set to further identify the originating AS.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in the range <1-4294967295>. | The AS value. |
| *A.B.C.D* | Required | String of 80 characters maximum length. | The IPv4 address of AS. |
| **no** | Optional | Literal | Clears the aggregator configuration for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set aggregator as 1 10.1.2.1
```

#### set as-path exclude
##### Syntax
```
[no] set as-path exclude .<value>
```

##### Description
This command excludes the given AS number from the AS_PATH.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in the range <1-4294967295>. | The AS value to be excluded from the AS_PATH. |
| **no** | Optional | Literal | Clears the AS value exclusion from the AS_PATH. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set as-path exclude 2
```

#### set as-path prepend
##### Syntax
```
[no] set as-path prepend .<value>
```

##### Description
This command prepends the given AS number to the AS_PATH.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in the range <1-4294967295>. | The AS value to be added to the AS_PATH. |
| **no** | Optional | Literal | Clears the AS value from the AS_PATH. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set as-path prepend 2
```

#### set atomic-aggregate
##### Syntax
```
[no] set atomic-aggregate
```

##### Description
This command enables a warning to upstream routers, through the ATOMIC_AGGREGATE attribute, that address aggregation has occurred on an aggregate route.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables the route-aggregation notification to upstream routers. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set atomic-aggregate
```

#### set comm-list delete
##### Syntax
```
[no] set comm-list <list-name> delete
```

##### Description
This command removes the COMMUNITY attributes from the eBGP routes identified in the specified community list. It also deletes matching communities for the route map.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *list-name* | Required | Integer in the range <1-99> or <100-500>, or a valid community string not exceeding 80 characters. | The community list name. |
| **no** | Optional | Literal | Deletes the community list exclusion under the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set comm-list 1 delete
```

#### set community
##### Syntax
```
[no] set community <list-name>
```

##### Description
This command sets the COMMUNITY attributes for route-map. The community number may be one of the following:
- aa:nn format
- local-AS|no-advertise|no-export|internet
- Additive
- None

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *list-name* | Required | An integer in the range <1-99> or <100-500>, or a valid community string not exceeding 80 characters. | The community list name. |
| **no** | Optional | Literal | Deletes the community list configuration under the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set community 6000:100
```

#### set community rt
##### Syntax
```
[no] set extcommunity rt <asn-community-identifier>
```

##### Description
This command sets the target extended community (in decimal notation) of an eBGP route. The COMMUNITY attribute value has the syntax AA:NN, where AA represents an AS or IP address, and NN is the community identifier.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *asn-community-identifier* | Required | AS1:AS2, where AS is an integer in the range <1 - 4294967295>, or a string not exceeding 80 characters. | The community attribute in the form of AA:nn or IP address:nn. |
| **no** | Optional | Literal | Deletes the configuration for the rt extended community list under the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set extcommunity rt 6000:100
s1(config-route-map)#set extcommunity rt 10.1.2.1:100
```

#### set extcommunity soo
##### Syntax
```
[no] set extcommunity soo <asn-community-identifier>
```

##### Description
This command sets the site-of-origin extended community (in decimal notation) of an eBGP route. The COMMUNITY attribute value has the syntax AA:NN, where AA represents an AS or IP address, and NN is the community identifier.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *asn-community-identifier* | Required | AS1:AS2, where AS is an integer in the range <1 - 4294967295>, or a string not exceeding 80 characters. | The community attribute in the form of AA:nn or IP address:nn. |
| **no** | Optional | Literal | Deletes the configuration for the site-of-origin extended community list under the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set extcommunity soo 6000:100
s1(config-route-map)#set extcommunity soo 10.1.2.1:100
```

#### set ipv6 next-hop global
##### Syntax
```
[no] set ipv6 next-hop global <X:X::X:X>
```

##### Description
This command sets the eBGP-4+ global IPv6 next hop address.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *X:X::X:X*  | Required | X:X::X:X | The IPv6 address. |
| **no** | Optional | Literal | Unsets the eBGP-4+ global IPv6 next hop address for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set ipv6 next-hop global 2001:db8:0:1
```

#### set local-preference
##### Syntax
```
[no] set local-preference <value>
```

##### Description
This command sets the BGP local preference and the local preference value of an IBGP route. The value is advertised to IBGP peers. The range is from 0 to 4294967295. A higher number signifies a preferred route among multiple routes to the same destination.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value* | Required | Integer in the range <0-4294967295>.  | The IPv6 address. |
| **no** | Optional | Literal | Unsets the BGP local preference for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set local-preference 1
```

#### set metric
##### Syntax
```
[no] set metric <expr>
```

##### Description
This command specifies the relative change of metric which is used with eBGP route advertisement. This command takes the route's current metric and increases or decreases it by a specified value before it is propagated. If the value is specified as negative and ends up being negative after the metric decrease, the value is interpreted as an increase in metric.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *expr* | Required | String of 80 characters maximum length. | The metric expression. |
| **no** | Optional | Literal | Unsets the eBGP local preference for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set metric +2

s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set metric -367
In this case -367 is treated as +367.
```

#### set origin
##### Syntax
```
[no] set origin <egp | igp | incomplete>
```

##### Description
This command sets the ORIGIN attribute of a local eBGP route to one of the following:
- `egp`: Sets the value to the Network Layer Reachablility Information (NLRI) learned from the Exterior Gateway Protocol (EGP).
- `igp`: Sets the value to the NLRI learned from a protocol internal to the originating AS.
- `incomplete`: If the value is not `egp` or `igp`.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| **egp** | Required | Literal  | Specifies the type-1 metric. |
| **igp** | Required | Literal  | Specifies the type-2 metric. |
| **incomplete** | Required | Literal  | Specifies the type-2 metric. |
| **no** | Optional | Literal | Unsets the eBGP origin attribute for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)#set origin egp
```

#### set weight
##### Syntax
```
[no] set weight <value>
```

##### Description
This command sets the weight of an eBGP route. A route`s weight has the most influence when two identical eBGP routes are compared. A higher number signifies a greater preference.

##### Authority
Admin user.

##### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *value*  | Required | Integer in the range <1-4294967295>. | The weight value. |
| **no** | Optional | Literal | Unsets the weight attribute for the route map. |

##### Examples
```
s1(config)# route-map RMAP1 deny 1
s1(config-route-map)# set weight 9
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
### IPv4 prefix-list
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
| *WORD*  | Required | String of maximum length 80 characters. | The IP prefix-list name. |
| *num*  | Required | 1-4294967295 | The sequence number. |
| *A.B.C.D/M*  | Required | A.B.C.D/M | The IPv4 prefix. |
| *0-32*  | Required | 0-32 | Minimum prefix length to be matched. |
| *0-32*  | Required | 0-32 | Maximum prefix length to be matched. |
| **no** | Optional | Literal |Deletes the IP prefix-list. |

#### Examples
```
s1(config)# ip prefix-list PLIST1 seq 5 deny 10.1.1.0/24
s1(config)# ip prefix-list PLIST2 seq 10 permit 10.2.2.0/24
s1(config)# no ip prefix-list PLIST1 seq 5 deny 10.3.2.0/24
s1(config)# no ip prefix-list PLIST2
```
### IPv6 prefix-list
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
This command defines a new community list. LINE is a string expression of the communities attribute. LINE can include a regular expression to match the communities attribute in eBGP updates. The community is compiled into a community structure. Multiple community lists can be defined under the same name. In that case, the match happens in user-defined order. Once the community list matches to the communities attribute in eBGP updates, it returns a permit or deny based on the community list definition. When there is no matched entry, deny is returned. When the community is empty, the system matches to any routes.

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
This command defines a new extended community list.  LINE is a string expression of the extended communities attribute, and can include a regular expression to match the extended communities attribute in eBGP updates.

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
This command displays eBGP routes from the BGP route table. When no route is specified, all IPv4 routes are displayed.

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

Local router-id 10.1.2.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 10.1.2.0/24       0.0.0.0                  0      0  32768  i
*> 10.2.3.0/24       10.10.10.2               0      0      0 2 5 i
*  10.3.4.0/24       10.20.20.2               0      0      0 3 5 i
*  10.4.5.0/24       10.30.30.2               0      0      0 4 5 i
Total number of entries 4
```

### show ip bgp summary
#### Syntax
```
show ip bgp summary
```

#### Description
The command provides a summary of the eBGP neighbor status.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```ditaa
s1# show ip bgp summary
BGP router identifier 10.1.2.1, local AS number 1
RIB entries 2
Peers 1

Neighbor             AS MsgRcvd MsgSent Up/Down  State
10.1.2.1               2       4       5 00:00:28 Established
```

### show bgp neighbors
#### Syntax
```
show bgp neighbors
```

#### Description
This command displays detailed information about eBGP neighbor connections.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```ditaa
s1# show bgp neighbors
  name: 10.1.2.1, remote-as: 6002
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

### show ip bgp route-map WORD
#### Syntax
```
show ip bgp route-map WORD
```

#### Description
This command displays route-map set and match attributes.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |  Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | WORD | Route-map name. |


#### Examples
```
s1# show ip bgp route-map BGP_IN
BGP route map table entry for BGP_IN
Entry 1:
     action : permit
     Set parameters :
     metric : 4
     aggregator_as : 1 10.1.2.1
     as_path_prepend : 1 1
     atomic_aggregate : true
     comm_list : test delete
     ipv6_next_hop_global : 2001::4
     local_preference : 33
     origin : egp
     weight : 44
     Match parameters :

s2# show ip bgp route-map BGP_OUT
BGP route map table entry for BGP_OUT
Entry 1:
     action : permit
     Set parameters :
     Match parameters :
     as_path : test
     origin : egp
     metric : 4
     probability : 20
```

### show ip prefix list
#### Syntax
```
show ip prefix list
```

#### Description
This command displays all ip prefix list configurations.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```
s1# show ip prefix-list
ip prefix-list BGP_IN_: 5 entries
   seq 5 deny 10.1.1.0/24
   seq 10 permit 10.2.2.0/24
   seq 15 permit 172.16.15.0/20 ge 21 le 28
   seq 20 permit 192.168.15.0/16 ge 19
   seq 25 deny 192.168.15.0/16 le 25
```

### show ip prefix-list WORD seq num
#### Syntax
```
show ip prefix list WORD seq <num>
```

#### Description
This command displays ip prefix list configuration with a specific name and sequence number.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IP prefix-list name. |
| *num*  | Required | 1-4294967295 | The sequence number. |

#### Examples
```
s1# show ip prefix-list BGP_IN_ seq 10
   seq 10 permit 10.1.0.0/24
```
### show ip prefix list detail WORD
#### Syntax
```
show ip prefix-list detail WORD
```

#### Description
This command displays the detailed IP prefix list configuration with a specific name.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IP prefix-list name. |

#### Examples
```
s1# show ip prefix-list detail BGP_IN_
ip prefix-list BGP_IN_:
   count: 5, sequences: 5 - 25
   seq 5 deny 10.1.0.0/24
   seq 10 permit 10.2.0.0/24
   seq 15 permit 172.16.15.0/20 ge 25 le 28
   seq 20 permit 192.168.15.0/16 ge 27
   seq 25 deny 192.168.15.0/16 le 25
```

### show ip prefix list summary WORD
#### Syntax
```
show ip prefix-list summary WORD
```

#### Description
This command displays the summarized ip prefix list configuration with a specific name.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IP prefix-list name. |

#### Examples
```
s1# show ip prefix-list summary BGP_IN_
ip prefix-list BGP_IN_:
   count: 5, sequences: 5 - 25
```
### show ipv6 prefix list
#### Syntax
```
show ipv6 prefix list
```

#### Description
This command displays all ipv6 prefix list configurations.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```
s1# show ipv6 prefix-list
ipv6 prefix-list BGP_IN: 5 entries
   Description: IPV6 Prefix Test
   seq 10 deny 9966:1:2::/64 ge 80 le 100
   seq 20 permit 7d5d:1:1::/64 le 70
   seq 30 permit 5d5d:1:1::/64 le 70
   seq 40 permit 2ccd:1:1::/64 ge 65
   seq 50 permit 4ddc:1:1::/64
```
### show ipv6 prefix list WORD
#### Syntax
```
show ipv6 prefix list WORD
```

#### Description
This command displays ipv6 prefix list configuration with a specific name.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IPv6 prefix-list name. |

#### Examples
```
s1# show ipv6 prefix-list BGP_IN
ipv6 prefix-list BGP_IN: 5 entries
   Description: IPV6 Prefix Test
   seq 10 deny 9966:1:2::/64 ge 80 le 100
   seq 20 permit 7d5d:1:1::/64 le 70
   seq 30 permit 5d5d:1:1::/64 le 70
   seq 40 permit 2ccd:1:1::/64 ge 65
   seq 50 permit 4ddc:1:1::/64
```
### show ipv6 prefix-list WORD seq num
#### Syntax
```
show ipv6 prefix list <WORD> seq <num>
```

#### Description
This command displays the ipv6 prefix list configuration with the specific name and sequence number.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IPv6 prefix-list name. |
| *num*  | Required | 1-4294967295 | The sequence number. |

#### Examples
```
s1# show ipv6 prefix-list BGP_IN seq 10
   seq 10 deny 9966:1:2::/64 ge 80 le 100
```

### show ipv6 prefix list detail
#### Syntax
```
show ipv6 prefix-list detail
```

#### Description
This command displays the detailed IP prefix list configuration.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```
s1# show ipv6 prefix-list detail
ipv6 prefix-list BGP_IN:
   Description: IPV6 Prefix Test
   count: 5, sequences: 10 - 50
   seq 10 deny 9966:1:2::/64 ge 80 le 100
   seq 20 permit 7d5d:1:1::/64 le 70
   seq 30 permit 5d5d:1:1::/64 le 70
   seq 40 permit 2ccd:1:1::/64 ge 65
   seq 50 permit 4ddc:1:1::/64
```

### show ipv6 prefix list detail WORD
#### Syntax
```
show ipv6 prefix-list detail WORD
```

#### Description
This command displays the detailed IP prefix list configuration with a specific name.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IPv6 prefix-list name. |

#### Examples
```
s1# show ipv6 prefix-list detail BGP_IN
ipv6 prefix-list BGP_IN:
   Description: IPV6 Prefix Test
   count: 5, sequences: 10 - 50
   seq 10 deny 9966:1:2::/64 ge 80 le 100
   seq 20 permit 7d5d:1:1::/64 le 70
   seq 30 permit 5d5d:1:1::/64 le 70
   seq 40 permit 2ccd:1:1::/64 ge 65
   seq 50 permit 4ddc:1:1::/64
```
### show ipv6 prefix list summary
#### Syntax
```
show ipv6 prefix-list summary
```

#### Description
This command displays the summarized ipv6 prefix list configuration.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```
s1# show ipv6 prefix-list summary
ipv6 prefix-list BGP_IN:
   Description: IPV6 Prefix Test
   count: 5, sequences: 10 - 50
```

### show ipv6 prefix list summary WORD
#### Syntax
```
show ipv6 prefix-list summary WORD
```

#### Description
This command displays the summarized ipv6 prefix list configuration with a specific name.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IPv6 prefix-list name. |

#### Examples
```
s1# show ipv6 prefix-list summary BGP_IN
ipv6 prefix-list BGP_IN:
   Description: IPV6 Prefix Test
   count: 5, sequences: 10 - 50
```
### show ipv6 prefix list WORD X:X::X:X/M
#### Syntax
```
show ipv6 prefix list WORD X:X::X:X/M
```

#### Description
This command displays the ipv6 prefix list configuration with a specific name and ipv6 address.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IPv6 prefix-list name. |
| *X:X::X:X/M*  | Required | X:X::X:X/M | The IPv6 address with prefix length M. |

#### Examples
```
s1# show ipv6 prefix-list BGP_IN 9966:1:2::/64
   seq 10 deny 9966:1:2::/64 ge 80 le 100
   seq 80 permit 9966:1:2::/64 ge 110
```

### show ipv6 prefix list WORD X:X::X:X/M first-match
#### Syntax
```
show ipv6 prefix list WORD first-match
```

#### Description
This command displays the first ipv6 prefix list configuration with a specific name and ipv6 address.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IPv6 prefix-list name. |
| *X:X::X:X/M*  | Required | X:X::X:X/M | The IPv6 address with prefix length M. |

#### Examples
```
s1# show ipv6 prefix-list BGP_IN 9966:1:2::/64 first-match
   seq 10 deny 9966:1:2::/64 ge 80 le 100
```

### show ipv6 prefix list WORD X:X::X:X/M longer
#### Syntax
```
show ipv6 prefix list WORD longer.
```

#### Description
This command displays the ipv6 prefix list configuration with a specific name, ipv6 address, and prefix-length greater than or equal to 'M'.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The IPv6 prefix-list name. |
| *X:X::X:X/M*  | Required | X:X::X:X/M | The IPv6 address with prefix length M. |

#### Examples
```
s1# show ipv6  prefix-list BGP_IN 9966:1:2::/64 longer
   seq 10 deny 9966:1:2::/64 ge 80 le 100
   seq 60 permit 9966:1:2::/70
   seq 80 permit 9966:1:2::/64 ge 110
```

### show ip community list
#### Syntax
```
show ip community list
```

#### Description
This command displays all community list configurations.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```
s1# show ip community-list
ip community-list BGPClist
    permit 2:0
    deny 4:0
```
### show ip extcommunity list
#### Syntax
```
show ip extcommunity list
```

#### Description
This command displays all extended community list configuration.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```
s1# show ip extcommunity-list
ip extcommunity-list BGPClist
    permit 2:0
    deny 4:0
```

### show as-path access list
#### Syntax
```
show ip as-path-access-list
```

#### Description
This command displays all as-path access list configuration.

#### Authority
Admin user.

#### Parameters
None

#### Examples
```
s1# show ip as-path-access-list
ip as-path access-list BGP_Filter
    permit 3
    deny 2
```

### show as-path access list WORD
#### Syntax
```
show ip as-path-access-list WORD
```

#### Description
This command displays the as-path access list configuration with a specific name.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |       Description          |
|-----------|----------|----------------------|
| *WORD*  | Required | String of 80 characters maximum length. | The as-path-access-list name. |

#### Examples
```
s1# show ip as-path-access-list BGP_Filter
ip as-path access-list BGP_Filter
    permit 3
    deny 2
```
## CLI
 
Click [here](http://www.openswitch.net/documents/user/bgp_cli) for CLI commands related to the eBGP feature.
