# High level design of OF-DPA OpenFlow Hybrid Switch Feature

The OF-DPA OpenFlow Hybrid Switch Feature is contained within the ASIC plugins that implement it. One such ASIC plugin is the OpenNSL plugin.

Code in the ops-switchd repository contains an implementation of an OpenFlow agent. This implementation comes from the Open vSwitch code on which ops-switchd is based. Information about the OpenFlow agent from Open vSwitch can be found in the ovs repository ([openswitch/ovs](http://git.openswitch.net/cgit/openswitch/ovs)).

The OpenNSL plugin in the ops-switchd-opennsl-plugin repository is an example of an ASIC plugin that implements the OF-DPA OpenFlow Hybrid Switch. The details of the design are found in DESIGN.md document found in the ops-switchd-opennsl-plugin repository. This serves as a reference for the OpenNSL implementation or for adding support to other ASIC plugin implementations.
