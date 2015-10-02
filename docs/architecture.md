OpenSwitch Architecture
======================

Design principles
------------------
* Aggressive modularization / high availability
 * Central state database for configuration. statistics, status and all inter-module communication
 * No direct messaging between modules - pub/sub through database only
 * Isolated fault domains - modules should not know about each others failures
 * Independent restartability of modules
* Portability
 * All hardware specific code must be kept separate and replaceable
* Good open source citizenship
 * Reuse and contribute
 * Minimize forking, stay on the edge
 * Enable upstreaming by providing value to partner projects - Linux, OCP, OVS, Quagga etc.

Top level view of the system
----------------------------

```ditaa
Single instance of OpenSwitch                               ^
+------------------------------------------------------------------------+
|                                                           |            |
|  +------------------------+ +---------------+ +-----------v----------+ |
|  | L2/L3 protocol daemons | |System daemons | |Management/monitoring | |
|  | bgpd, lldpd, lacpd,... | |sysd, intfd,...| |CLI, Rest, Ansible,...| |
|  +--------^--------^------+ +--------^------+ +-----------^----------+ |
|           |        |                 |                    |            |
|           | +------v-----------------v--------------------v----------+ |
|           | |                                                        | |  RFC 7047
|           | |          System state database - OVSDB-Server          | |  protocol
|           | |                                                        <------------->
|           | +----------------------------^------------------------^--+ |
|           |                              |                        |    |
|           |            Hardware support  |     ops-switchd        |    |
|           |            daemons           |     +------------------v--+ | OpenFlow
|           |            +-----------------v---+ |   SDK independent   <------------->
|           |            |       ops-fand      | |        layer        | |
|           |            | - - - - - - - - - - | +---------------------+ |
|           |            |       ops-tempd     | |    SDK specific     | |   sFlow
|           |            | - - - - - - - - - - | |        plugin       +------------->
|           |            |       ops-powerd    | +---------------------+ |
|           |            |       ...           | |         SDK         | |
|           |            +----------^----------+ +----------^----------+ |
|    Kernel |                       |                       |            |
|  +-------------------------------------------------------------------+ |
|  | +------v-----------+ +---------v---------+  +----------v--------+ | |
|  | |                  | | I2C/other drivers |  |                   | | |
|  | |Virtual interfaces| +-------------------+  |     SDK driver    | | |
|  | |                  <------------------------>                   | | |
|  | +------------------+                        +-------------------+ | |
|  +-------------------------------------------------------------------+ |
|                                                                        |
+------------------------------------------------------------------------+


```
System state database (commonly referred as OVSDB across the system)
--------------------------------------------------------------------
As can be clearly seen in the above diagram, system state database is a central piece of the system.
It's connected to every user space module and contains all configuration, statuses and statistics for the entire system.

However, facilitation of the configuration and monitoring paths is not the main function of the database. The primary purpose of the central database is to provide an exclusive mechanism for different modules to communicate. In fact, separate modules are not allowed to exchange any information outside of the database.

Complying to this principle, makes the system more modular by removing direct dependencies across the modules. Instead of module A sending a message to module B, module A publishes an appropriate state to the database. Module B, or any other module in the system, is able to subscribe to that state and receives an update whenever the state changes. Module B may start before or after A, crash or restart, but it is always able to sync to the current state of the system.

### OVSDB-Server ###
OVSDB-Server is a mature in memory database that complies to OVSDB protocol, defined in RFC 7047. Database provides a comprehensive set of transactional operations as well as flexible capabilities of subscribing to changes happening in the data set. Being schema based, OVSDB allows for maintaining structural coherency of the contained state as well as advanced garbage collection.

While OVSDB protocol is currently used for internal communication between all the modules of the system and OVSDB-Server, it's envisioned that it's also going to be used where tight integration is required with external systems.

ops-switchd
-----------
The primary responsibility of ops-switchd is to translate the data model residing in OVSDB into ASIC specific SDK calls and vice versa.
In fact, ops-switchd is the only daemon that is allowed to access ASIC SDK.

Internal modularity of ops-switchd provides the ability to port OpenSwitch to different SDKs and their corresponding silicon. For more information on ASIC portability, refer to http://www.openswitch.net/documents/dev/porting-new-asic.

Being based on ovs-vswtchd from Open vSwitch, ops-switchd also contains Openflow agent and communicated directly to Openflow controllers. OpenFlow functionality is not yet supported (not connected to any ASIC SDK), but will be added in the future.

Hardware support daemons
------------------------
Hardware support daemons mediate between the kernel drivers of various peripheral devices and OVSDB. In the current implementation, I2C based peripherals are supported using [Config-YAML library](http://www.openswitch.net/documents/dev/ops-config-yaml)

For further information regarding specific daemons, refer to:
* [Fan daemon](http://www.openswitch.net/documents/dev/ops-fand/design)
* [Temperature daemon](http://www.openswitch.net/documents/dev/ops-tempd/design)
* [Power supply daemon](http://www.openswitch.net/documents/dev/ops-powerd/design)
* [LED daemon](http://www.openswitch.net/documents/dev/ops-ledd/design)
* [Pluggable modules daemon](http://www.openswitch.net/documents/dev/ops-pmd/design)

For further information on porting to new platforms (not ASICs), refer to ["porting to the new platform".](http://www.openswitch.net/documents/user/porting)

Virtual interfaces
------------------
While all state exchange in the system is supposed to be performed through OVSDB, control plane packets (L2 BPDUs or L3 protocol packets) are not true states of the system and must not traverse the database.

In order to accommodate control plane traffic, each physical port, as well as any logic interfaces like VLANs, LAGs, tunnels etc. have (or will have once implemented) virtual interface representation inside the kernel.

For physical ports, it's the responsibility of the SDK driver to create kernel interfaces (upon request of ops-switchd) and to forward packets correctly into/from those interfaces.

L2/L3 protocol daemons
----------------------
Each protocol resides in a separate daemon.
Protocol daemons gather packets from kernel interfaces by regular means of raw, UDP or TCP sockets.

For LLDP protocol, OpenSwitch integrates [lldpd daemon from Vincent Bernat](https://github.com/vincentbernat/lldpd). For further information, refer to [LLDP](http://www.openswitch.net/documents/dev/ops/lldp) feature documentation

LACP protocol implementation is contributed by HP. For further information, refer to [Link aggregation](http://www.openswitch.net/documents/dev/lag) documentation.

For L3 routing protocols, OpenSwitch integrates [Quagga suite](https://github.com/opensourcerouting/quagga). For further information refer to [L3 system](http://www.openswitch.net/documents/dev/ops/l3) documentation.

System daemons
--------------
System daemons are responsible for various pieces of functionality in the system, which essentially doesn't require external input or output besides manipulation of states in OVSDB:
* Initializing the System table row, detecting and provisioning subsystems - [ops-sysd](http://www.openswitch.net/documents/dev/ops-sysd/design)
* Saving and restoring startup configuration - [ops-cfgd](http://www.openswitch.net/documents/dev/ops-cfgd/design)
* Managing system ports enable/mtu/duplex/... logic - [ops-intfd](http://www.openswitch.net/documents/dev/ops-intfd/design)
* ...


Management/monitoring daemons
-----------------------------
While OVSDB protocol is a powerful tool, which can be used for managing OpenSwitch, it's not the most familiar one. Users might prefer CLI, REST API, Ansible, Chef etc.
Overall approach is to provide "adaptor" agents that would translate between the specific management approach and OVSDB.

Currently there are three management agents available:
* [CLI](http://www.openswitch.net/documents/dev/ops-cli/design)
* [REST API](http://www.openswitch.net/documents/dev/ops-restd/design)
* [Declarative configuration](http://www.openswitch.net/documents/dev/ops-restd/design)
