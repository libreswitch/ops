# High level design of port state pecking order

Port state pecking order defines the mechanism used in the control path to
define and report the forwarding state of an interface or port based on the
state of different protocols and features with the capability to define the data
path's forwarding state of a physical interface or a logical port.

## Data path

The pecking order defines a set of layers that are used to report/determine the
interface or port state.  __Figure 1__ shows the main layers for interfaces,
ports and VLANs (STGs).  The priority is higher on the lowest layers, if a layer
is down or blocked then the layers above it are irrelevant.  In the figure the
admin state has the highest priority as it reflects the user configuration.  If
the admin state is "down" then the link and forwarding states are not relevant
for data or control path and the interface is down.  Similarly, if the link
state is down, the forwarding state is irrelevant for the control or data path.


```ditaa
+------------------+------------------+------------------+
|                  |                  |                  |
| +--------------+ | +--------------+ | +--------------+ |
|  Fwd State       |  Fwd State       |  Fwd State       |
|                  |                  |                  |
|                  |                  |                  |
| STG 1            | STG 2            | STG 3            |
+------------------+------------------+------------------+
|                                                        |
| +----------------------------------------------------+ |
|  Forwarding State                                      |
|                                                        |
| +----------------------------------------------------+ |
|  Admin State                                           |
|                                                        |
|                                                        |
|                                                        |
| Port/LAG 1                                             |
+--------------------------------------------------------+
|                           ||                           |
|   +--------------------+  ||  +--------------------+   |
|    Forwarding State       ||   Forwarding State        |
|                           ||                           |
|   +--------------------+  ||  +--------------------+   |
|    Link State             ||   Link State              |
|                           ||                           |
|   +--------------------+  ||  +--------------------+   |
|    Hw Status              ||   Hw Status               |
|                           ||                           |
|   +--------------------+  ||  +--------------------+   |
|    Admin State            ||   Admin State             |
|                           ||                           |
|                           ||                           |
|                           ||                           |
|  Interface A              || Interface B               |
+--------------------------------------------------------+


```
__Figure 1:__ Admin, Link and Forwarding state

The Hardware status is used to identify if everything that must be applied
to the hardware has been applied.  This is specially important for features like
ACLs, because if there are not enough resources in the system to apply the ACLs
the interface should not be brought up.

If both admin and link states are "up", then the forwarding state defines the
state of the interface.  For the data path, it is sufficient to know that the
forwarding state is "false" or "blocked".  There is no need to have more
details.

__Figure 1__ shows the hierarchy of the layers in an scenario where two
interfaces are aggregated in a LAG.  In this case, if just one interface gets
"blocked", for whatever reason, then the LAG keeps forwarding through the Other
interface.  When both interfaces get "blocked" then the Port/LAG gets blocked as
well.

At the STG level, used to represent a group of VLAN in a port, individual STGs
can be blocked.  Since STGs are lower in the hierarchy, the forwarding state of
interfaces or ports is not affected when an individual STG is blocked.  When a
port is blocked, then all the STGs on the port are blocked as the port is higher
in the hierarchy.

## Control Path

For the control path, it is required to have more details about why the
forwarding state is different from "forwarding".  The protocols controlling the
forwarding state need to know why an interface or port is blocked.

```ditaa
+-----------------------------------------------------+
 Forwarding State


 +----------------------------------+--------------+
  Interface Aggregation             | Blocked Reason
                                    |
                                    |
 +----------------------------------+--------------+
  Interface Loop Protection         | Blocked Reason
                                    |
                                    |
 +-------------------------------------------------+
  Interface Security                | Blocked Reason
                                    |
                                    |
 +-------------------------------------------------+
  Interface Health                  | Blocked Reason
                                    |
                                    |
+-----------------------------------+-----------------+
```
__Figure 2:__ Interface forwarding state layers

## Physical Interfaces

In order to keep the daemons implementing the protocols decoupled the forwarding
state is broken down into sublayers.  __Figure 2__ shows the control path
sublayers of an interface's forwarding state.  In this case again the lowest
layer has the highest priority.  Protocols daemons monitor the forwarding state,
if it changes to a value different from "forwarding" then each protocol checks
the control plane layers (forwarding state sublayers) to verify if it should
continue operating on the interface or consider the interface as blocked.

As an example in normal operation, a protocol to identify if an interface is
unidirectional like UDLD drives the state of the interface health, if it is
configured to do so. If UDLD asserts a interface as unidirectional, the
interface health layer gets blocked, which sets the overall data path forwarding
state as blocked too. If the interface is configured with a protocol like 802.1x
to authenticate and authorize users, then the daemon implementing the protocol
security gets notified about the forwarding state change.  This daemon also
monitors the state of the control layers that are bellow it, in this case it is
only the health layer.  If that layer is the one causing the "blocked" state
then the daemon halts its operation on that interface.  If the layers that is
causing the "blocked" state is above the security layer, then the security
protocol must continue its normal operation on the interface.

## Arbiter

Since there could be many owners of the state of a specific layer, it is not
efficient to have each protocol writing the layer's state.  Therefore, to
control the layer state (and the forwarding state as a whole) it is required to
have a daemon arbitrating based on the state of the protocols. The arbiter
monitors the state of all the protocols that can decide to block an interface or
port and sets the state of the control sublayer and forwarding layer.  If there
is more than one protocol that could drive the state of a particular sublayer,
the arbiter decides the priority and sets the owner of the sublayer.  This is
done so that multiple protocols can drive a sublayer.

Since the forwarding state apply for both physical interfaces and logical ports,
it is required to have two arbiters, one for interfaces and one for ports.

## logical ports

The case of logical ports is similar to the interfaces; however, there are some
differences that must be described.  __Figure 3__ shows the sublayers of a port.
The main difference of a port is that a port can aggregate multiple physical
interfaces.  Based on this, the lowest sublayer, highest priority on a port is
the port aggregation layer, witch summarizes the state of all the member
interfaces.

```ditaa
+-----------------------------------------------------+
 Forwarding State


 +----------------------------------+--------------+
  Port Loop Protection              | Blocked Reason
                                    |
                                    |
 +-------------------------------------------------+
  Port Aggregation                  | Blocked Reason
                                    |
                                    |
+-----------------------------------+-----------------+

```
__Figure 3:__ Port forwarding state layers

Other sublayers at the port level are used for protocols that operate at the
logical port level.

Additionally, according to __Figure 1__, a logical port/STG combination can be
"blocked".  For the control path, when an STG gets blocked, the protocols
working at the port level only get affected if interested in the VLANs
configured in the port.  If the STG containing the VLANs a protocols is
interested in gets "blocked" then the protocols considers the VLAN/Port
combination blocked.  Protocols working below the STG level, only care about the
Port's forwarding state.

## Default values

By default, the forwarding state layer and all the sublayers are forwarding.  So
that when a protocol is not supported or not running the interface or port does
not get blocked.

The arbiter can overwrite this default value (by writing in OVSDB)at any time
based on supported features and the configuration.

For example, if an interface is configured to use UDLD to verify that it is
bidirectional, but the correspondent interface does not have any UDLD
information, the arbiter sets the interface health state as "blocked" and the
owner as UDLD until it receives information from the protocol.  In this case
if the interface is also configured to use 802.1x, then the 802.1x daemon does
not run on the interface until the health layer indicates that it should be
forwarding.

## Design choices

* Interface and Port state layers are defined to determine/drive the data path
state. The layers are:
  * Admin: The value is defined by the user.  As this indicates the user's
  intent, it has the highest priority in the pecking order.  The value of this
  layer comes from the configuration and exists for both interfaces and ports
  * Link: The value is defined by the hardware.  If the admin state is up, then
  the link state is used to identify if the interface is operational.  As this
  identifies physical state it only makes sense for physical interfaces
  * Forwarding: The value is defined by the running protocols configured on the
  interface/port.

* Control path sublayers are defined in the forwarding layer.  Protocols daemons
monitor the sublayers of their interest to determine if they should run the
protocol or not.  The control path sublayers are defined separately for
interfaces and ports:
  * Interface sublayers:
    * Interface health:  Groups all protocols used to monitor the interface
    health.  Some examples are UDLD or DLDP.  This interfaces has the highest
    priority in the pecking order
    * Interface security:  Groups the protocols used for security purposes. Some
    examples are: MACSec, 802.1x
    * Interface Loop Protection:  Groups the protocols used to protect the
    interfaces against loops.  Some examples are STP, Loop-Protect.
    * Interface aggregation:  Groups the protocols related to interface
    aggregation.  Some examples are LACP and MLAG
  * Port sublayers:
    * Port Aggregation: Aggregates the state of the interfaces that are members
    of the port.  If there is only a single interface in the port, then this
    value is used by the arbiter to mirror the interface state.  If the port is
    a LAG (has multiple interfaces) then the arbiter uses this sublayer to
    aggregate the forwarding state of all the members.  This way, protocols
    operating at the port level do not have to check individual interfaces
    * Port Loop Protection: Groups all protocols used to prevent loops at the
    port level.  Some examples are MSTP, RRPP.


## Participating modules
```ditaa
+---------------+                                  +---------------+
|               |                                  |               |
|               |                                  |               |
|    ops-cli    |                                  |   ops-restd   |
|               |                                  |               |
|               |                                  |               |
+-------^-------+                                  +-------^-------+
        |                                                  |
        |                                                  |
        |                                                  |
        |                                                  |
+-------v--------------------------------------------------v----------+
|                                                                     |
|                              OVSDB                                  |
|                                                                     |
+-------^------------^------------^------------^-----------^----------+
        |            |            |            |           |
        |            |            |            |           |
        |            |            |            |           |
        |            |            |            |           |
+-------v-------+    |    +-------+-------+    |   +-------v-------+
|               |    |    |               |    |   |               |
|               |    |    |               |    |   |               |
|   ops-portd   |    |    |   ops-lacpd   |    |   |  ops-switchd  |
|               |    |    |               |    |   |               |
|               |    |    |               |    |   |               |
+---------------+    |    +---------------+    |   +---------------+
                     |                         |
             +-------v-------+         +-------v-------+
             |               |         |               |
             |               |         |               |
             |   ops-mstpd   |         |   ops-intfd   |
             |               |         |               |
             |               |         |               |
             +---------------+         +---------------+
```
__Figure 4:__ Participating modules

The management interfaces participate in the pecking order defining the admin
state.  The user can set the admin state through the CLI or the REST API.

The link state is set by switchd, ops-lacpd and ops-mstpd are the daemons
implementing protocols that feed information into the arbiters.

The arbiters are implemented inside ops-intfd (for interfaces) and ops-portd for
ports.

## OVSDB-Schema

The admin state is written in the _Interface_ table in the `admin_state` column
and in the _Port_ table in the `admin` column.  The link state is kept in the
_Interface_ table in the `link_State` column.

The `hw_status` column contains information about hardware resource allocation
on the interface.  This is important for features like ACLs as not having enough
resources to apply defined ACLs in the hardware could mean a security issue. The
column defines two keys:
* `ready`: Specifies if all hardware resources have been applied. If set to
_"false"_ it means that not all configuration could be applied to the hardware.
When _"false"_ the forwarding state must be set as _"false"_ too.
* `ready_state_blocked_reason`: Specifies the reason why the hardware is not
ready.

The Forwarding state for interfaces is reported using the `fowarding_state`
key-value map in the _Interface_.  This map defines the following keys:

* `state`: Summarizes the forwarding state of the interface.  This key drives
forwarding state of the data path
* `interface_aggregation`:  Reports the forwarding state of the aggregation
sublayer
* `interface_aggregation_blocked_reason`:  Reports the asserting protocol that
is causing the interface aggregation to be different from "forwarding"

The forwarding state for ports is reported using the `forwarding_State`
key-value map in the _Port_ table.  This map defines the following keys:
* `state`: Summarizes the forwarding state of the port.  This key drives
forwarding state of the data path
* `port_aggregation`:  Reports the forwarding state of the aggregation
sublayer
* `port_aggregation_blocked_reason`:  Reports the asserting protocol that is
causing the port aggregation to be different from "forwarding"
* `port_loop_protection`:  Reports the forwarding state of the loop protection
sublayer
* `port_loop_protection_blocked_reason`:  Reports the asserting protocol that is
causing the port loop protection to be different from "forwarding"

----------
# References
* [lacpd design](/documents/dev/ops-lacpd/DESIGN)
* [lacp cli reference](/documents/user/lacp_cli)
* [portd design](/documents/dev/ops-portd/DESIGN)
