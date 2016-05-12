# High level design of link aggregation

Link aggregation (LAG) is a feature that takes two or more physical interfaces
creates a single virtual interface that aggregates them as if they were a single
physical link. The aggregation can be static, meaning that all links in the
aggregation are active, or dynamic using the link aggregation control protocol
(LACP) as defined in 802.1ax-2014. When dynamic LAG is used, the state of the
physical interfaces depends on the negotiation with the LACP partner.

Link aggregation is primarily implemented by the lacpd daemon. The lacpd daemon
manages both static and dynamic Link Aggregation Groups (LAGs). It is the
daemon's responsibility to determine which interfaces are configured and
eligible to participate in a LAG, and to change the interface state information
accordingly. This information is then used by switch daemon, to change the
hardware configuration of the switch chip to include (or exclude) the interface
in the hardware LAG.

A significant portion of the lacpd code is used to participate in the LACP
protocol to establish and maintain dynamic LAGs.

For the control traffic sent and received on the device's CPU and for the
container image the Linux bonding driver is used to aggregate the interfaces in
software. When a LAG is created, portd takes the interfaces participating in the
LAG and creates a Linux bond interface. For LAGs attached to a bridge, portd
adds them to the correspondent Linux bridge. For LAGs with L3 information and
attached to a VRF, portd applies the corresponding configuration on the bond
interface as it does for interfaces representing physical interfaces or VLANs.
Daemons only need to work with the bond interface instead of the individual
interfaces.

## Design choices

* The lacpd daemon manages both static and dynamic LAGs: The validation done for
static and dynamic LAGs is similar, so all validation is done in a single
daemon.
* Protocol and interface state is managed by lacpd: The state of the protocol is
managed by lacpd and it is posted in OVSDB. Based on the protocol state lacpd
sets the interface state (rx_enable and tx_disable)
* The portd daemon manages Linux bond interface: Portd takes care of configuring
other Linux interfaces and interface related setting such as VLANs, IP
addresses, etc. This daemon already has the code to manage interface state,
needed to add and remove slaves into the Linux bond. For these reasons portd
also takes the responsibility of creating, destroying and managing the slaves of
Linux bonds based on LAG's OVSDB information.

## Participating modules
```ditaa
+----------------------+                            +---------------------+
|                      |                            |                     |
|                      |                            |                     |
|        ops-cli       |                            |      ops-restd      |
|                      |                            |                     |
|                      |                            |                     |
+-----------^----------+                            +----------^----------+
            |                                                  |
            |                                                  |
            |                                                  |
            |                                                  |
+-----------v--------------------------------------------------v----------+
|                                                                         |
|                                  OVSDB                                  |
|                                                                         |
+-----------^-------------------------^------------------------^----------+
            |                         |                        |
            |                         |                        |
            |                         |                        |
            |                         |                        |
+-----------v----------+  +-----------+----------+  +----------v----------+
|                      |  |                      |  |                     |
|                      |  |                      |  |                     |
|       ops-portd      |  |       ops-lacpd      |  |     ops-switchd     |
|                      |  |                      |  |                     |
|                      |  |                      |  |                     |
+----+------------^----+  +----^-----------------+  +---------+-----------+
     |            |            |                              | User Space
+----------------------------------------------------------------------------+
     |            |            |                              | Kernel Space
+----v----+       |       +----v-----+                        |
|         |       |       |          |                        |
|         |       |       |          |                        |
| Bonding |       |       |  Linux   |                        |
| Driver  |       +------->Interfaces|                        |
|         |               |          |                        |
|         |               |          |                        |
+---------+               +----^-----+                        |
                               |                              | Kernel Space
+----------------------------------------------------------------------------+
                               |                              | Hardware
                          +-----------------------------------v----------+
                          |    |                                         |
                          |    |                    Hardware             |
                          |    |                                         |
                          +----------------------------------------------+
                               |
                          +----v----+
                          |         |
                          |  Peer   |
                          | Device  |
                          |         |
                          |         |
                          +---------+

```

The lacpd process subscribes to and examines the Port and Interface tables in
the database. The Port table defines LAGs (when configured with two or more
interfaces from the Interface table or when LACP is enabled), including the
general operation of LACP on the LAG if it is configured for dynamic operation.
The Interface table may define some optional parameters for LACP, as well as
containing the current operational state of the interface (including link state
  and link speed).

__Note:__ in order to be considered for inclusion in a LAG, an interface must be
linked and operating at the same speed and duplex as the member interface with
the highest priority in the LAG. The LACP protocol uses the state machines
described in 802.1ax-2014 to determine eligibility for participation.

If the port is configured for LACP, lacpd performs the LACP protocol negotiation
with the LACP peer on the corresponding L2 interface.

Once lacpd has determined that an interface is configured and eligible for
participation in a LAG, it changes the state information for the interface
(`hw_bond_config:tx_enable`, `hw_bond_config:rx_enable`).

The switchd daemon monitors the information in the interface hw_bond_config to
determine if the interface should be configured for participation in the LAG.

Mirroring the hardware configuration, the portd daemon (additionally to its
other responsibilities described in  the
[portd design](/documents/dev/ops-portd/DESIGN)) monitors the LAG configuration
and adds/removes Linux bond interfaces using the bonding driver. It also takes
care of adding and removing slaves to the bond when the configuration in OVSDB
changes.

## OVSDB-Schema
### Creating a LAG
The user establishes a LAG by creating a row in the _Port_ table by adding two
or references to interfaces in the `interfaces` column or by setting the `lacp`
column to _"active"_ or _"passive"_ __and__ by using _"lag#"_ (where _#_ is an
  integer) in the `name` of the port. The `name` value is used to create the
  Linux bond interface correspondent to the LAG.

Only interfaces of `type` _"system"_ can participate in LAG.

### Static and dynamic LAGs
The user configures the port for LACP operation by specifying the `lacp` value
as either _"active"_ or _"passive"_ (if _"passive"_, lacpd waits for the
connected peer to send LACP protocol packets before responding). Otherwise the
value defaults to _"off"_ , which disables LACP operation on the LAG (the LAG is
configured for static operation).

### Hashing algorithm
The user may configure the `bond_mode` value in the port to specify the type of
hash function the chip should use. There are three supported values for this:
* l2-src-dst-hash (_basic_)
* l3-src-dst-hash (_basic_)
* l3-l4-src-dst-hash (_advanced_)

The two _basic_ hash functions are common hash algorithms that should be
supported by every switch chip that implements link aggregation. The _advanced_
mode is supported based on the chip capabilities . The default value for
`bond_mode` is _"l3-src-dst-hash"_.

### LACP protocol configuration (Dynamic LAG)
#### _System_ Table
The LACP specification requires a system identification and a system priority to
be used by all interfaces participating in LACP negotiation. By default lacpd
uses the bridge's Ethernet address as the system id and the highest allowed
value for the system priority (lowest priority) of 65535. It is possible to set
these system-wide values using the _System_ Table `lacp_config` map's
`lacp-system-id` and 'lacp-system-pririty' keys.

#### _Port_ Table
The _Port_ table contains fields that allow the user to configure the behavior
of LACP. Additionally to the options described in the
["Creating a Lag"](#Creating a LAG) section to set the LACP mode, it is possible
to override the system-wide id and priority per LAG using the `other_config`
map. The `lacp-system-id` is used to override the system-wide identifier for the
LAG and the `lacp-system-priority` key to override the system-wide priority. If
those keys are not defined, LACP uses the _System_ table's definition or the
default values.

The `other_config` map has two more keys used for LACP. The `lacp-time` key is
used by lacpd to determine if the LACP protocol should send LACPDUs packets once
per second (_"fast"_) or once every 30 seconds (_"slow"_).

The `lacp-fallback` key is used to determine the behavior or a LAG using LACP to
negotiate when there is no partner. A value of _"true"_ means that the LAG
falls back to a mode defined by the lacp_fallback_mode. If set to _"false"_ the
LAG blocks all its members until it can negotiate with a partner.

The `lacp_fallback_mode` key is used to defined the mode to which the LAG falls
back when no partner is detected.  The _"priority"_ mode uses the value in the
`lacp_port_priority` key of the LAG members to define which interface is not
blocked and should go to collecting/distributing.  The _"all\_active"_ mode
keeps all interfaces in collecting/distributing.  __Note__ that this mode is
likely to create loops, it is recommended that this mode is only used to connect
with hosts.

The `lacp_fallback_timeout` key is used to determine the time during which
fallback will be active.  The timer starts counting when the interface's state
machine gets to the defaulted state.  When the timer expires the interfaces will
get blocked as if fallback were disabled.

#### _Interface_ Table
The lacpd daemon also monitors the `other_config` map in the Interface table for
interface specific configuration.

The lacpd process monitors the _Interface_ table to determine if a link has been
established for the interface `link_state` column and to determine what speed
the interface is operating at `link_speed` column and the duplex at
`link_duplex` column. Only interfaces in the _"up"_ state and with the same
speed and duplex can be active members of a LAG.

The lacpd daemon uses the `type` column to identify if the interface is eligible
to participate in the LAG. Only interfaces of type _"system"_ can be active
members of a LAG.

For LACP specific configuration, the `other_config` map has three LACP specific
keys. The `lacp-port-id` and `lacp-port-priority` keys are used to override the
default values for the interface's Id and priority that are used in the LACP
negotiation.

The `lacp-aggregation-key` key is used to identify the aggregation key of the
interface. When an interface is added to a LAG, it can only be eligible if the
aggregation key is the same as the one in the interface with the higher priority
in the LAG.

### LAG Status
#### _Port_ table
The _Port_ table uses the `lacp_status` column to report the LAG's state. The
`bond_speed` key is used to report the speed of the members interfaces, it is
just a copy of the speed of the member interface with the highest priority. The
`bond_status` key is used to report the aggregated state of the LAG. The _"ok"_
state means that at least one member is forwarding traffic, the _"down"_ state
means that no member is forwarding traffic and the _"defaulted"_ states means
that  no partner has been detected and the state of the LAG depends on the value
of the `other_config:lacp-fallback` key. The `bond_status_reason` indicates why
is the LAG _"down"_.

To summarize the LAG status, the _Port_ table uses the `bond_status` column.
The ops-lacpd daemon is responsible of updating this column as it has all
the required information. This column defines a key called `state`.  This state
reflects the state of the aggregation of all interfaces for static and dynamic
LAGs.  The possible values
are:
* "up": At least one of the member interfaces is "up" and should be in a
  forwarding state according to LACP state or LAG configuration.
* "blocked": All member interfaces are blocked by LACP (not in the collecting /
  distributing state) or not eligible to be members of the LAG.  When using
  LACP and the `lacp_status` column is "defaulted", the `state` column depends
  on the `other_config:lacp-fallback` key in the _Port_ table.  If it is true,
  then the value of `state` is forwarding, if it is false, then it should be
  blocked.
* "down": All member interfaces are either admin or link "down".

#### _Interface_ table
The lacpd process fills in status information in the _Interface_ table's rows
associated with a LAG. The `lacp_current` Boolean value indicates if lacpd has
current information from the peer for the interface (peer is sending timely
  LACPDUs). The `lacp_status` map includes the negotiation values from both the
  local (actor) and peer (partner) endpoints.

* `actor_system_id`
  Local endpoint system identifier (may be set by user config in System or Port
  tables). Used to identify the entire system.
* `actor_port_id`
  Local endpoint port identifier. Used to identify the specific interface.
* `actor_key`
  Local endpoint LAG key. Used to identify the LAG.
* `actor_state`
  Local endpoint LACP negotiation state information.
* `partner_system_id`
  Peer endpoint system identifier (may be set by user config in System or Port
  tables). Used to identify the entire system.
* `partner_port_id`
  Peer endpoint port identifier. Used to identify the specific interface.
* `partner_key`
  Peer endpoint LAG key. Used to identify the LAG.
* `partner_state`
  Peer endpoint LACP negotiation state information.

At the interface level, a `bond_status` column is used to summarize the state of
the aggregated link.  The ops-lacpd daemon is responsible of updating this
column as it has all the required information.  The `bond_state` column defines
one key called `state`.  If the interface is individual this column is empty.
This key has four possible values:

* "up": Indicates that the interface is up and should forwarding traffic
  according to LACP or LAG configuration.
* "blocked": Indicates that the interface should not be forwarding traffic in
  neither rx or tx direction
* "down": Indicates that the interface is down.  The main difference from
  "blocked" state is that when the interface is down it doesn't allow control
  traffic like LACPDUs to be forwarded/sent to the CPU

### LAG hardware configuration
When lacpd determines that an interface should be included in the operation of
the LAG (for either static or dynamic LAGs), it sets the `hw_bond_config` map
key values in the _Interface_ table to "true" (defaults to "false").

* `rx_enabled`
* `tx_enabled`

The lacpd daemon also sets the `hw_bond_config:bond_hw_handle` value to notify
the switchd process which LAG the interface should be included in (if any). This
is provided so that vswitchd does not have to replicate the code that lacpd uses
to associate Port and Interface table entries.

### Bonding driver
Similarly to switchd, portd checks the Port table configuration and
`hw_bond_config` to determine if an interface is eligible to be a member of a
LAG. Only eligible interfaces are added to the Linux bond.

References
----------
* [lacpd design](/documents/dev/ops-lacpd/DESIGN)
* [lacp cli reference](/documents/user/lacp_cli)
* [portd design](/documents/dev/ops-portd/DESIGN)
