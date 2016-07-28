## Contents

  * [High-level design of LLDP](#high-level-design-of-lldp)
    * [Design choices](#design-choices)
    * [TLVs supported](#tlvs-supported)
    * [LLDP configurations, defaults and range](#lldp-configurations-defaults-and-range)
      * [System level configuration](#system-level-configuration)
      * [Per interface configuration](#per-interface-configuration)
    * [Interactions with OVSDB and Kernel](#interactions-with-ovsdb-and-kernel)
    * [OVSDB-Schema](#ovsdb-schema)
      * [System table](#system-table)
      * [Interface table](#interface-table)
    * [LLDP packets to CPU](#lldp-packets-to-cpu)
    * [References](#references)

# High-level design of LLDP
LLDP is used by networking devices to advertise identities and capabilities at the link layer. The [LLDP daemon (lldpd)](/documents/dev/ops-lldpd/DESIGN) is responsible for sending and receiving LLDP advertisements over the switch interfaces and populating the neighbors discovered in the OVSDB interface table. The daemon receives global LLDP configurations from the System:other_config column in the OVSDB and per interface configurations from the Interface:other_config column.  The daemon is also responsible for maintaining global and per interface LLDP statistics and writing them to the OVSDB. When the device boots up, LLDP is enabled by default.

## Design choices
There were multiple open source choices for the LLDP daemon such as "lldpad" from http://open-lldp.org/, "ladvd" from https://github.com/sspans/ladvd and "lldpd" from http://vincentbernat.github.io/lldpd/. The "lldpd" implementation from http://vincentbernat.github.io/lldpd/ has been selected due to the following considerations:

* It is a popular implementation on Linux
* It has support for many advanced TLV
* OS specific code is well abstracted


## TLVs supported

The following TLVs are supported in OpenSwitch:

- Chassis-ID
- Port-ID
- TTL
- System capabilities (optional)
- System description (optional)
- System name (optional)
- Management address (optional)
- Port description (optional)
- Port VLAN ID (optional)
- Port and Protocol VLAN ID (optional)
- Port VLAN Name (optional)
- Port Protocol ID (optional)

The TLVs are supported both for transmission and reception.

## LLDP configurations, defaults and range
###System level configuration
- Enable/Disable - LLDP is "disabled" by default.
- Per optional TLV enable/disable transmission - All TLVs are "enabled" by default. Example: management-address.
- Management address to be advertised.
- Transmit timer - This configuration determines how frequently to transmit. Range is between 5-32768 seconds. Default is 30 seconds.
- Hold time - This configuration determines how many transmit cycles the neighbor holds our values. Each transmit cycle will be as long as the time specified in seconds by the "transmit timer". The range is between 2-10 and the default is 4 transmit cycles.

###Per interface configuration
- Enable/Disable - This is "enabled: by default (Note that the system-wide disable has a precedence)
- Receive/Transmit - Receive and Transmit is the default (note that the interface level disable has a precedence). The supported modes are off, rx, rx and rxtx.

## Interactions with OVSDB and Kernel
* LLDP daemon receives configurations from OVSDB
* LLDP daemon transmits LLDP frames on the Linux kernel interfaces
* LLDP daemon receives LLDP frames on the Linux kernel interfaces
* LLDP daemon writes neighbors and statistics to OVSDB

```ditaa
+----------------------------------------+      +------------+
|               LLDP Daemon              |      |    OVSDB   |
|  +--------------+   +---------+ Global Configs| +--------+ |
|  |              |   |         +<----------------+ System | |
|  |              |   | LLDPD   |  Global stats | | Table  | |
|  |  Opensource  |   | OVSDB   | -------+------> |        | |
|  |    lldpd     +<->+Interface|        |      | +--------+ |
|  |              |   |         | Interface cfg | +--------+ |
|  |              |   |         +<--------------+-+        | |
|  |              |   |         | Neighbors/stats |        | |
|  +--------------+   +---------+ --------------> |Interface |
+---^-----^------------------------^-----+      | |  Table | |
    |     |                        |            | |        | |
    |     |    LLDP frames rx/tx   |            | +--------+ |
    v     v                        v            +------------+
+---+-----+------------------------+------+
|                KERNEL                   |
|  +-+   +-+  . . . . . . . .     +-+     |
|  +-+   +-+   interfaces         +-+     |
|                                         |
+-----------------------------------------+

```

## OVSDB-Schema
### System table
```
System:other_config
Keys:
lldp_enable
lldp_tlv_mgmt_addr_enable
lldp_tlv_port_desc_enable
lldp_tlv_port_vlan_enable
lldp_tlv_sys_cap_enable
lldp_tlv_sys_desc_enable
lldp_tlv_sys_name_enable
lldp_mgmt_addr
lldp_tx_interval
lldp_hold

System:statistics
Keys:
lldp_table_inserts
lldp_table_deletes
lldp_table_drops
lldp_table_ageouts
```

### Interface table
```
Interface:other_config
Keys:
lldp_enable_dir ("off","rx","tx","rxtx")

Interface:status
Keys:
lldp_local_port_vlan
lldp_local_port_desc

Interface:statistics
Keys:
lldp_tx
lldp_rx
lldp_rx_discard
lldp_rx_tlv_disc

Interface:lldp_neighbor_info
Keys:
port_description
port_id
port_protocol
port_pvid
chassis_description
chassis_id
chassis_id_subtype
chassis_name
chassis_capability_available
chassis_capability_enabled
mgmt_ip_list
mgmt_iface_list
vlan_name_list
vlan_id_list
```
There are other neighbor attributes (MAC/PHY information) supported by opensource lldpd, which will be populated in the Interface:lldp_neighbor_info but not captured in the above list. Refer to http://git.openswitch.net/cgit/openswitch/ops/tree/schema/vswitch.xml to see a complete list.


## LLDP packets to CPU
The platform-specific code is responsible for punting the LLDP protocol frames from ASIC up to kernel interface.


## References
* http://vincentbernat.github.io/lldpd/
