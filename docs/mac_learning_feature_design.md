# MAC Learning Feature Design
-----------------------------

- [Overview](#overview)
- [OVSDB schema](#ovsdb-schema)
- [High Level Design](#high-level-design)
- [Design detail](#design-detail)
- [References](#references)


## Overview
-----------

MAC Learning is a process wherein the switch learns MAC addresses on the ports to avoid flooding.
ASIC learns the MAC addresses on all interfaces and the software maintains the MAC address table.


## OVSDB Schema
---------------

The following columns are written:
```
mac_addr: MAC address learnt
bridge: bridge reference
vlan: VLAN associated
from: Who has configured/learnt
port: Port reference
```


## High level design
--------------------

```
  +-------------+
  |             |
  |    OVSDB    |
  |             |
  +-------------+
      ^
      |4                                   ops-switchd process
  +---|------------------------------------------------------------+
  |   |                                                            |
  |   |                                                            |
  |   |    mac_learning_plugin                asic-plugin          |
  |   |   +-------------+         +-----------------------------+  |
  |   |   |    init (1) |         |                             |  |
  |   |   |             |   3     |                             |  |
  |   ----|----run------|---------|---> get_mac_learning_hmap() |  |
  |       |             |         |                             |  |
  |       |    wait (2) |         |                             |  |
  |       |             |         +-----------------------------+  |
  |       |    exit (5) |                                          |
  |       +-------------+                                          |
  +----------------------------------------------------------------+

```

The above diagram illustrates the steps:
1. When the process ops-switchd starts, the main thread invokes plugin_init(). This initialization is responsible for creating mac_learning plugin and registering for MAC table for read/write access.
2. Wait function registers the sequence change event.
3. Run function detects sequence change event, and invokes ASIC Plugin API to get the hmap.
4. Once the hmap is received, the main thread processes it and update the necessary changes in the OVSDB.
5. Destroy function removes any dynamically allocated memory during initialization.
[[Refer to details](#details) for further information related to MAC learning plugin]

## Design detail
----------------

MAC Learning feature design details:
- ASIC Plugin changes (ops-switchd, platform plugin)
   This comprises of the PD implementation of PI-PD API.
- MAC learning plugin (ops-switchd)
- Updating OVSDB (ops-switchd)

### Details
-----------

* ASIC Plugin changes

   ```
                                               switchd main thread
    +----------------------------------------------------------------------------------------------------+
    |      main() in ovs-vswitchd.c                      |            platform plugin                    |
    |                                                    |                                               |
    |      plugins_init() -------------------------------|---------------> init()                        |
    |                                                    |                                               |
    |                                                    |            get_mac_learning_hmap (added)      |
    +----------------------------------------------------------------------------------------------------+
   ```

   ASIC plugin is the infrastructure that uses plugin model instead of ofproto-provider APIs. This plugin extends the platform-specific functionality such that the APIs can be invoked independent of ofproto knowledge. This is extremely necessary in the case of MAC learning as the hmap to store the new entries of the L2 table is shared across all the ASICs.

* MAC Learning Plugin

   ```ditaa
    +--------------------------------------------------------------------------------------------------+
    |      main() in ovs-vswitchd.c                    |            mac_learning_plugin.c              |
    |                                                  |                                               |
    |      plugins_init() -----------------------------|---------------> init()                        |
    |                                                  |                                               |
    |                                                  |                                               |
    |      plugins_wait() -----------------------------|---------------> wait()                        |
    |                                                  |                                               |
    |                                                  |                                               |
    |      plugins_run() ------------------------------|---------------> run()                         |
    |                                                  |                                               |
    |                                                  |                                               |
    |      plugins_destroy() --------------------------|---------------> destroy()                     |
    |                                                  |                                               |
    +--------------------------------------------------------------------------------------------------+
   ```
   The MAC learning plugin is part of ops-switchd repository. This plugin is created to remove the dependency on customizing bridge.c for all features. It comprises of: init(), wait(), run() and destroy(). The order of execution is similar to bridge_init(), bridge_wait(), bridge_run() and bridge_destroy(). The init is called during the initialization; wait and run are in infinite loop until the process exits. When the process is terminated, destroy is invoked.

   - Init registers the plugin extension and bridge init event.
   - Wait registers for the sequence change event in order to get notifications from PD.
   - Run reconfigures the MAC Table in OVSDB based on the changes.
   - Destroy unregisters the plugin extension.

* Updating OVSDB

   OVSDB is updated by run() of the MAC learning plugin. It does check for the seq change event. If any change is detected, the ASIC plugin is used to invoke a PI-PD API to get the hmap. Based on the hmap contents, the OVSDB is updated.

## References
-------------

* [Openvswitch](http://openvswitch.org/)
* Component design: [ops-switchd-opennsl-plugin](/documents/dev/ops-switchd-opennsl-plugin/docs/mac_learning_design)
