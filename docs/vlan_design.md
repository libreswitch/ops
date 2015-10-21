High level design of VLAN
=========================
The VLAN feature allows a user to configure a switch to segregate network traffic by associating it with a VLAN identifier (VID). Even when traffic does not need to be segregated, it is still associated with a VLAN, although it may be the _default_ VLAN.

Each VLAN defined for a switch is recorded in the VLAN table in the database. A row in the VLAN table has several user configured values:

* name
  The alphanumeric name associated with the VLAN.
* id
  The VID for the VLAN.
* description
  A user provided description of teh VLAN.
* admin
  Configured state of the VLAN. If "down" (the default), packets on this VLAN are dropped by the switch.

The vland process monitors the VLAN table and determines state information for each row. The `oper_state` value indicates if the VLAN is operational.  If the VLAN is not operational, the `oper_state_reason` value indicates why the VLAN isn't operational ("ok", "admin\_down", "no\_member\_port", "unknown"). A VLAN must be configured to be administratively enabled by the user, as well as have ports (rows in the Port table) configured for the VLAN in order to be considered operational.

The `internal_usage:l3port` value indicates which port (if any) is using this VLAN internally for L3 operation.

Each row in the Port table has VLAN configuration (which may be default). The following VLAN types (specified in the `vlan_mode` field) are supported:

* trunk
  A trunk port carries packets on one or more VLANs specified in the `trunks` column (or all defined VLANs if `trunks` is empty or not specified). A packet that ingresses on a trunk port is in the VLAN specified in its 802.1Q header, or the default VLAN if the packet has no 802.1Q header. A packet that egresses through a trunk port will have an 802.1Q header if it has a nonzero VLAN ID.

  Any packet that ingresses on a trunk port tagged with a VLAN that the port does not trunk is dropped.
* access
  An access port carries packets on exactly one VLAN specified in the `tag` column. Packets egressing on an access port have no 802.1Q header.

  Any packet with an 802.1Q header with a nonzero VLAN ID that ingresses on an access port is dropped, regardless of whether the VLAN ID in the header is the access port's VLAN ID.
* native-tagged
  A native-tagged port resembles a trunk port, with the exception that a packet without an 802.1Q header that ingresses on a native-tagged port is in the "native VLAN" (specified in the `tag` column).
* native-untagged
  A native-untagged port resembles a native-tagged port, with the exception that a packet that egresses on a native-untagged port in the native VLAN will not have an 802.1Q header.

When the `vlan_mode` column is empty, the default mode is selected as follows:

* If `tag` contains a value, the port is an access port. The `trunks` column should be empty.
* Otherwise the port is a trunk port. The `trunks` column value is used if it is present.

The vland process is responsible for enabling and disabling the VLAN (through the VLAN table `hw_vlan_config:enable` column). The remainder of the business logic for VLAN operation is performed by switchd.

Design choices
--------------
N/A

Participating modules
---------------------
```ditaa
+--------+
|database|-------+
+-+-^----+       |
  | |            |
  | |            |
+-v-+-+      +---v---+
|>land|      |switchd|
+-----+      +---+---+
                 |
              +--v---+
              |SWITCH|
              +------+
```
As described above, vland monitors the VLAN and Port tables in the database and determines the operational state of each VLAN. The switchd process is responsible for monitoring the VLAN and Port tables and configuring the switch to operate in the defined configuration.

OVSDB-Schema
------------

The vland process monitors two tables in the database: VLAN and Port. In the Port table, vland examines the `vlan_mode`, `tag`, and `trunks` values to determine the VLAN mode and associated VLAN IDs.

* Port
  * name
  *  vlan\_mode
  *  tag
  *  trunks

In the VLAN table, vland examines the admin value as part of determining the operational state (and operational state reason) for the VLAN. The vland process writes the `hw_vlan_config`, `oper_state`, and `oper_state_reason` values. If the `internal_usage` column is set, vland ignores the VLAN.

* VLAN
  * name
  * id
  * admin
  * internal\_usage
  * hw\_vlan\_config
  * oper\_state
  * oper\_state\_reason


References
----------
* [vland design](/documents/dev/ops-vland/DESIGN)
