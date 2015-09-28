High level design of link aggregation
=====================================

Link aggregation is primarily implemented by the lacpd daemon. The lacpd daemon manages both static and dynamic Link Aggregation Groups (LAGs). It is the daemon's responsibility to determine which interfaces are configured and eligible to participate in a LAG, and to change the interface state information accordingly. This information is then used by switch daemon, to change the hardware configuration of the switch chip to include (or exclude) the interface in the hardware LAG.

A significant portion of the lacpd code is used to participate in the LACP protocol to establish and maintain dynamic LAGs.

Design choices
--------------
N/A

Participating modules
---------------------
```ditaa
     +--------+
     |database+-------+
     +---+--^-+       |
         |  |         |
         |  |         |
       +-v--++    +---v---+
       |lacpd|    |switchd|
       +-+-^-+    +---+---+
         | |          |
+--------v-+--+    +--v---+
|L2 interfaces|    |SWITCH|
+-------------+    +------+
```

The lacpd process subscribes to and examines the Port and Interface tables in the databse. The Port table defines LAGs (when configured with two or more interfaces from the Interface table), including the general operation of LACP on the LAG if it is configured for dynamic operation. The Interface table may define some optional parameters for LACP, as well as containing the current operational state of the interface (including link state and link speed).

Note: in order to be considered for inclusion in a LAG, an interface must be linked and operating at the same speed as the first interface to join the LAG. The LACP protocol may use other factors to determine eligibility for participation.

If the port is configured for LACP, lacpd performs the LACP protocol negotiation on the corresponding L2 interface.

Once lacpd has determined that an interface is configured and eligible for participation in a LAG, it changes the state information for the interface (hw\_bond\_config:tx\_enable, hw\_bond\_config:tx\_disable).

The switchd daemon monitors the information in the interface hw\_bond\_config to determine if the interface should be configured for participation in the LAG.

OVSDB-Schema
------------
The user establishes a LAG by creating a row in the Port table with two or more interfaces configured. The user may configure the `bond_mode` value in the port to specify the type of hash function the chip should use. The two supported values for this are "l2-src-dst-hash" and "l3-src-dst-hash", as these are common hash algorithms that should be supported by every switch chip that implements link aggregation. The default value for `bond_mode` is "l3-src-dst-hash".

The user configures the port for LACP operation by specifying the `lacp` value as either "active" or "passive" (if "passive", lacpd waits for the connected peer to send LACP protocol packets before responding). Otherwise the value defaults to "off", which disables LACP operation on the LAG (the LAG is configured for static operation).

There are several additional values in the port row that the user may configure to change the behavior of the LACP protocol. The `other_config:lacp-system-id` overrides the system-wide identifier (MAC) for the LAG. The `other_config:lacp-system-priority` overrides the system-wide priority when participating in the LACP protocol. The `other_config:lacp-time` is used by lacpd to determine if the LACP protocol should request heartbeat packets once per second ("fast") or once every 30 seconds ("slow").

The user may configure the singleton System row with additional LACP settings. The `lacp_config:lacp-system-id` sets the system-wide identifier (MAC) for LACP. If not specified, the value is assumed to be the Ethernet MAC address assigned to the bridge. The `lacp_config:lacp-system-priority` sets the LACP protool priority (lower values have higher priority in making link status decisions).

The lacpd process monitors the Interface table to determine if a link has been established for the interface (`link_state`) and to determine what speed the interface is operating at (`link_speed`).

The lacpd process fills in status information in the Interface rows associated with a LAG. The `lacp_current` Boolean value indicates if lacpd has current information from the peer for the interface (peer is sending timely heartbeats). The `lacp_status` map includes the negotiation values from both the local (actor) and peer (partner) endpoints.

* actor\_system\_id
  Local endpoint system identifier (may be set by user config in System or Port tables). Used to identify the entire system.
* actor\_port\_id
  Local endpoint port identifier. Used to identify the specific interface.
* actor\_key
  Local endpoint LAG key. Used to identify the LAG.
* actor\_state
  Local endpoint LACP negotiation state information.
* partner\_system\_id
  Peer endpoint system identifier (may be set by user config in System or Port tables). Used to identify the entire system.
* partner\_port\_id
  Peer endpoint port identifier. Used to identify the specific interface.
* partner\_key
  Peer endpoint LAG key. Used to identify the LAG.
* partner\_state
  Peer endpoint LACP negotiation state information.


When lacpd determines that an interface should be included in the operation of the LAG (for either static or dynamic LAGs), it sets the `hw_bond_config` values to "true" (defaults to "false").

* rx\_enabled
* tx\_enabled

The lacpd daemon also sets the `hw_bond_config:bond_hw_handle` value to notify the switchd process which LAG the interface should be included in (if any). This is provided so that vswitchd does not have to replicate the code that lacpd uses to associate Port and Interface table entries.

References
----------
* [lacpd design](https://www.openswitch.net/documents/dev/ops-lacpd/DESIGN)
* [lacp cli reference](https://www.openswitch.net/documents/user/lacp_cli)
