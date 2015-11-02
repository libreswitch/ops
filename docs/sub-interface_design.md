# High-level Sub-interface Design

## Contents
- [Introduction](#introduction)
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
	- [intfd](#intfd)
	- [portd](#portd)
	- [vswitchd](#vswitchd)
- [OVSDB-Schema](#ovsdb-schema)
	- [Port table](#port-table)
	- [Interface table](#interface-table)
- [Functionality](#functionality)
	- [Sub-interfaces](#sub-interfaces)
	- [Interface type](#interface-type)
- [References](#references)

## Introduction
Sub-interfaces are used on L3 routers to support router-on-a-stick configurations, to allow separating traffic on a particular VLAN to a separate port, and to selectively apply policies on the routers. Open vSwitch Database has port and interface tables to manage the physical and logical interfaces configured on the OpenSwitch. A sub-interface is a logical interface allowing layer 3 configurations, and layer 2 configurations on a single interface. One interface may be split into multiple logical interfaces, each having a different network IP address and a dot1q encapsulation VLAN number. VLAN is used to switch the incoming packets and tag the outgoing packets. IP address is used to route the packets.


## Design choices
The OVS schema for interfaces and ports was adopted for maximum compatibility with Open vSwitch. Existing port table and interface table schemas are extended to support sub-interfaces. An alternate approach is to add a new table for sub-interfaces, as they have a mix of port and interface table columns. Current design adheres to the port and interface design. The addition/update/deletion functions of the sub-interface and loopback interface are handled by extending the functionalities of **intfd** and **portd**. No new daemon is introduced for sub-interface.


## Participating modules
Sub-interfaces are primarily managed by **portd**, **intfd**, and **vswitchd**. See the respective component's documentation for more details about these daemons.

```
                                 ovsdb                   +--------+
                    +-----------------------------+  +---+ portd  |
                    |                             |  |   |        |
   +--------+       |                             |  |   +--------+
   |        |       |                             |  |   +--------+
   |  cli   +---------->  ***   port tbl  *** <------+---+        |
   |        |       |                 ^           |      | intfd  |
   |        +----------> *** interface|tbl*** <----------+        |
   +--------+       |           ^     |           |      +--------+
                    +-----------|-----|-----------+
                                |     |
                                |     |
                              +-+-----+------+
                              |              |
                              |   vswitchd   |
                              |              |
                              +--------------+

```


### intfd
The [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN) reads information from the port and the interface tables. The intfd determines if an interface should be brought up, based upon user configuration and state information. The intfd updates the **hw_intf_config** field to tell **vswitchd** if an interface is to be enabled or disabled in hardware. When the parent interface is configured as administratively down, all of its sub-interfaces are brought down. Sub-interfaces are brought up when the parent interface is up, as well as the sub-interface. If the parent interface is link_down, all of its sub-interfaces are also down.

### portd
The [Port Daemon (portd)](http://www.openswitch.net/documents/dev/ops-portd/DESIGN) reads information from the port table. User configurations like IP address, Dot1q encapsulation, VLAN Id, etc. are validated by portd. The portd updates the **hw_config** field to notify **vswitchd** when the user configures any of these parameters. Using netlink interface, kernel interfaces for sub-intefaces are created by **portd**. When the parent interface is configured as an L2 interface by "no routing" command, all of its sub-interfaces will be removed.

### vswitchd
The [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN) is the daemon that ultimately drives control to, and reports state and statistics from, the switching ASIC. It monitors the **hw_intf_config** field, and takes appropriate action in the hardware. For the switch image, **vswitchd** calls the BCM plug-in APIs to configure the ASIC, and also sets up the Linux kernel virtual interfaces. For the host based VSI image, it sets up the interfaces in Linux.


## OVSDB-Schema


### Port table
```
Port:interfaces  (cli, rest, etc) - uuid of corresponding interface row entry
Port:name        (cli, rest, etc) - Sub-interface name as "parent_interface"."sub-interface"
Port:trunks      (cli, rest, etc) - The dot1q encapsulation VLAN id.
Port:vlan_mode   (cli, rest, etc) - Always set to “trunk”.
Port:ip4_address (cli, rest, etc) - User configured IP address.
Port:hw_config   (intfd)          - for vswitchd to consume.

```
See the [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN) and the [Port Daemon (portd)](http://www.openswitch.net/documents/dev/ops-portd/DESIGN).



### Interface table
```
Interface:name             (cli, rest, etc) - sub-interface name, identical to port row entry.
Interface:statistics       (vswitchd)       - statistics of the sub-interface.
Interface:user_config      (cli, rest, etc) - administrative state (up/down) of the sub-interface.
Interface:hw_intf_config   (intfd)          - for vswitchd to consume the user configurations.
Interface:subintf_parent   (cli, rest, etc) - contains the uuid of parent interface and the encapsulation vlan id. Populated only for subinterface row.
Interface:type             (cli, rest, etc) - new type `vlansubint` is added to denote sub-interfaces
```
See the [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN), and the [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN).
Refer to the OVSDB-Schema section in the [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN) for other rows and their usage.


## Functionality
### Sub-interfaces
* Creation of sub-interfaces
While creating a sub-interface, a port table entry and an interface table entry are created. The naming convention used for sub-interface is parent_interface.subinterface_number. The port table has an interface row that contains the uuid of the sub-interface entry. Other fields like ip4_address, trunks, and vlan_mode are populated by the configuring daemon, such as **clid** or **restd**. The interface table has the administrative up/down and statistics. The port table entry will be attached to both the VRF table and the bridge table. The column subintf_parent of interface table entry is updated with the dot1q encapsulation vlan id and the parent interface's uuid mapping.

* Handling parent interface config changes
Configuring the parent interface as an L2 interface removes all of the sub-interfaces created under it. Administratively bringing down the parent interface brings the state of it down, and brings down all of its sub-interfaces. Common properties like MTU and speed, are copied to the interface table entries for all of the sub-interfaces when the properties are configured on the parent interface.

* Handling parent interface state changes
When the parent interface is down, all of its sub-interfaces are brought down.


### Interface type
The **interface:type** field identifies the interface type. All physical interfaces, those representing true hardware physical interfaces (face-plate interfaces), are of the type **system**. There are other interfaces used for internal communication purposes that are of the type **internal**. Interfaces of the type **internal** are not directly managed or configured by users. Sub-interfaces are identified by the **vlansubint** type.

## References
* [Interface Daemon (intfd)](http://www.openswitch.net/documents/dev/ops-intfd/DESIGN)
* [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/documents/dev/ops-openvswitch/DESIGN)
* [Port Daemon (portd)](http://www.openswitch.net/documents/dev/ops-portd/DESIGN)
