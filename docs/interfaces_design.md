# High-level design of interfaces
OpenSwitch manages physical interfaces primarily through the Open vSwitch database interface and port tables.  The [System Daemon (sysd)](http://www.openswitch.net/ops-sysd/DESIGN.md) pushes the physical interface information into the interface table during a boot. Although the [Interface Daemon (intfd)](http://www.openswitch.net/ops-intfd/DESIGN.md) sees these physical interfaces, it does not bring these interfaces "up" if a configuration has not been supplied. Only after a user has configured a valid port in the port table with a reference to that physical interface in the interface table, does the Interface Daemon notify the vSwitch Daemon (vswitchd) that a physical interface is to be enabled.

The [Pluggable Module Daemon (pmd)](http://www.openswitch.net/ops-pmd/DESIGN.md) continuously monitors for the insertion or removal of pluggable transceivers, updates the database accordingly, and turns on and off lasers for optical transceivers when notified.

## Design choices
The OVS schema for interfaces and ports was adopted for maximum compatibility with Open vSwitch.

## Participating modules
Interfaces are primarily managed by four daemons; sysd, intfd, pmd, and vswitchd. Please see their respective component documentation for more details for these daemons.

```
                                 ovsdb
                    +-----------------------------+
   +--------+       |                             |      +--------+
   |        +----------> ***subsystems tbl***     |      |        |
   |        |       |                             |      |        |
   |  sysd  |       |    ***    port tbl  *** <----------+  intfd |
   |        |       |                 ^           |      |        |
   |        +----------> *** interface|tbl*** <----------+        |
   +--------+       |           ^     |           |      +--------+
                    +-----------|-----|-----------+
                         +------+     |
                         |      |     |
                   +-----+--+ +-+-----+------+
                   |        | |              |
                   |  pmd   | |   vswitchd   |
                   |        | |              |
                   +--------+ +--------------+

```
### sysd
[System Daemon (sysd)](http://www.openswitch.net/ops-sysd/DESIGN.md) reads the hardware description files and populates the physical interfaces into the interface table, along with a reference for each back to the subsystem table. Fields populated by sysd include "name" and "hw_intf_info". These fields specify for the other daemons which functionality is supported for each physical interface.

### intfd
[Interface Daemon (intfd)](http://www.openswitch.net/ops-intfd/DESIGN.md) reads information from the port table and the interface table. intfd determines if an interface should be brought "up", based on user configuration and state information. intfd updates the hw_intf_config field to tell vswitchd if an interface is to be enabled or disabled in hardware.

### pmd
[Pluggable Module Daemon (pmd)](http://www.openswitch.net/ops-pmd/DESIGN.md) monitors pluggable module status via i2c and updates the "pm_info" field. This information is used by intfd as it determines the state and capabilities of the interface. If an interface is enabled, pmd will turn the laser on for optical transceivers.

### vswitchd
[Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/ops-openvswitch/DESIGN.md) is the daemon that ultimately drives control to and reports state and statistics from the switching ASIC. It monitors the "hw_intf_config" field and takes appropriate action in hardware.


## OVSDB-Schema
### Subsystem table
```
Subsystem:interfaces - A set containing each physical interface that is a member of this subsystem.
```
See [System Daemon (sysd)](http://www.openswitch.net/ops-sysd/DESIGN.md).

### Port table
```
Port:interfaces - A set containing 1 to 8 interfaces that belong to this port.
```
See [Interface Daemon (intfd)](http://www.openswitch.net/ops-intfd/DESIGN.md)

### Interface table
```
Interface:name (sysd)
Interface:mac_in_use (sysd, set to default value of open_vswitch:system_mac)
Interface:pm_info (pmd)
Interface:statistics (vswitchd)
Interface:user_config (cli, rest, etc)
Interface:hw_intf_config (intfd)
Interface:hw_intf_info (sysd)
Interface:split_parent (sysd)
Interface:split_children (sysd)
```
See [Pluggable Module Daemon (pmd)](http://www.openswitch.net/ops-pmd/DESIGN.md), [Interface Daemon (intfd)](http://www.openswitch.net/ops-intfd/DESIGN.md), and [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/ops-openvswitch/DESIGN.md)

## Functionality
### Slit interfaces
QSFP+ interfaces support "splitter cables". These are cables that have a QSFP+ transceiver on one end, with the cable splitting into four separate cables, each terminated with an SFP+ transceiver. This cable takes the four 10-Gb lanes used for 40-Gb QSFP+ modules and separates them into four individual 10-Gb cables, each with a single 10-Gb lane.  Only QSFP+ interfaces can be split.

The [hardware description files](http://www.openswitch.net/ops-config-as5712/DESIGN.md) contain information for each physical interface. This information specifies the capability of the physical interface (face-plate interface) and it also indicates if an interface can be split.

[sysd](http://www.openswitch.net/ops-sysd/DESIGN.md) adds a row into the interface table for each physical interface identified in the hardware description files. When a QSFP+ interface is identified as splittable, sysd creates five entries instead of only one.

The first entry is the "parent" interface, which has the capabilities for the interface when the interface is not configured for "split".  The remaining four interfaces are "child" interfaces and they have the capabilities for the interface when the interface is configured for "split".

The system daemons use the first "parent" interface row when the user configuration parameter "lane\_split" is set to "no-split". Likewise, the daemons use the four "child" interfaces when the user configuration parameter "lane\_split" is set to "split". The presence or type of transceiver is not relevant to whether an interface is "split" or not, only the value of "lane\_split". Note: The default for the user configuration parameter, if not present, is "no-split".

### Fixed interfaces
Face-plate interfaces that are fixed (not pluggable) have the interface:hw_intf_info:pluggable field set to "false". This tells [pmd](http://www.openswitch.net/ops-pmd/DESIGN.md) to ignore this interface. For now, fixed fiber interfaces are not supported, as pmd is responsible for turning lasers on and off, and it currently ignores fixed interfaces.

### Pluggable modules
SFP/SFP+ and QSFP+ modules are supported. See [Pluggable Module Daemon (pmd)](http://www.openswitch.net/ops-pmd/DESIGN.md) and [hardware description files](http://www.openswitch.net/ops-config-as5712/DESIGN.md) for additional information.

### Interface Type
The interface:type field identifies the interface type. All physical interfaces, those representing true hardware physical interfaces (aka face-plate interfaces), are of type "system". There are other interfaces used for internal communication purposes that are of type "internal". Interfaces of type "internal" are not managed or configured directly by users.

### MAC Assignment
A MAC address is assigned to each interface by [sysd](http://www.openswitch.net/ops-sysd/DESIGN.md) when the interface is first added to the Interface table. Since the MAC does not need to be unique, all physical interfaces get assigned the "system MAC", which is pulled from open_vswitch:system_mac.

## References
* [Pluggable Module Daemon (pmd)](http://www.openswitch.net/ops-pmd/DESIGN.md)
* [Interface Daemon (intfd)](http://www.openswitch.net/ops-intfd/DESIGN.md)
* [Virtual Switch Daemon (vswitchd)](http://www.openswitch.net/ops-openvswitch/DESIGN.md)
* [System Daemon (sysd)](http://www.openswitch.net/ops-sysd/DESIGN.md)
* [hardware description files](http://www.openswitch.net/ops-config-as5712/DESIGN.md)
