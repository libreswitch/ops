Porting OpenSwitch
==================
OpenSwitch was designed to be highly portable to new forwarding ASICs and encompassing platforms.
Below is a high level description of steps to be taken when approaching either of these tasks.

## Contents
- [Contents](#contents)
- [Porting to a different ASIC](#porting-to-a-different-asic)
	- [Interface between SDK independent layer and a plugin](#interface-between-sdk-independent-layer-and-a-plugin)
	- [Currently supported plugins](#currently-supported-plugins)
	- [Alternatives in building a driver for additional ASICs](#alternatives-in-building-a-driver-for-additional-asics)
		- [Providing OpenNSL compatible SDK](#providing-opennsl-compatible-sdk)
		- [Building a new plugin](#building-a-new-plugin)
- [Porting to a different platform](#porting-to-a-different-platform)

## Porting to a different ASIC
As further explained in [OpenSwitch Architecture](/documents/user/architecture),
ops-switchd is conceptually constructed out of three layers -
SDK independent layer, SDK specific plugin and ASIC SDK itself.

SDK independent layer resides in openswitch/ops-openvswitch repository, mainly in vswitch/  and ofproto/ directories.
It's responsible for communicating to OVSDB-server and Openflow controllers.

SDK specific plugins are essentially ASIC drivers of OpenSwitch system.
Each plugin resides in a separate repository called openswitch/ops-switchd-[underlying SDK]-plugin.
Build process in the plugin repositories results in a dynamically linked library.
When started, ops-switchd searches for these libraries in a predefined path and loads the libraries.

The way that SDK itself is loaded and operated is specific to the plugin.

### Interface between SDK independent layer and a plugin
OpenSwitch is heavily based on Open vSwitch. ops-switchd is an extension of ovs-vswitchd.
In the future, the goal for OpenSwitch would be to find an effective way to collaborate
between the projects in order to allow development of shared code in the upstream Open vSwitch.

As such, interface between platform independent and SDK specific plugins of ops-switchd is an
extension of "OFProto provider" and "NetDev provider" interfaces that can be found in Open vSwitch.
Both of these interfaces together comprise an interface of ops-switchd plugins.

The original Open vSwitch interfaces were extended to support full configurability of the interfaces,
layer 3 configuration and any other data plane specific features, which are not supported
(and not necessarily needed) in the virtual switch.

For more details on the specific APIs of the plugin interface, please refer to
http://git.openswitch.net/cgit/openswitch/ops-openvswitch/tree/lib/netdev-provider.h
and http://git.openswitch.net/cgit/openswitch/ops-openvswitch/tree/ofproto/ofproto-provider.h.

### Currently supported plugins
OpenSwitch currently supports two plugins:
* OpenNSL plugin - interfaces [OpenNSL SDK](https://github.com/Broadcom-Switch/OpenNSL) and supports Broadcom Trident II ASIC.
* Docker container plugin - allows OpenSwitch to operate inside Docker container, where pure Open vSwitch is used as an ASIC emulation.

### Alternatives in building a driver for additional ASICs
There are two major options for those who consider porting OpenSwitch to another set of ASICs.
OpenSwitch project is agnostic to the specific choice, which would be made by maintainers of the specific drivers.

#### Providing OpenNSL compatible SDK
Given that OpenSwitch already maintains OpenNSL plugin, this would be the fastest and least maintenance elaborate option for ASICs,
whose capabilities are sufficiently covered by OpenNSL.
For more details on OpenNSL API specification please refer to https://github.com/Broadcom-Switch/OpenNSL/tree/master/doc.

#### Building a new plugin
If specific ASIC provides capabilities, which are not expected to be covered by OpenNSL specification,
then the best choice would be to implement and maintain a new plugin.
Such a plugin might either address a specific ASIC family or a set of ASIC families that agree to provide common SDK API.

## Porting to a different platform
Aside from basic choice of ASIC, major platform differences are in the port counts/configurations and peripherals
management - temperature, power supplies, LEDs.
OpenSwitch design attempts to abstract those differences into a set of YAML files that explain the specific configuration,
I2C bus parameters etc.
In order to support a new platform, new set of YAML description files has to be created in openswitch/ops-hw-config repository.
Please refer to /documents/dev/ops-hw-config/design for more details.
