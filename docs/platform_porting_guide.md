# Platform

## Contents

- [Overview](#overview)
- [Add a configuration for a device](#add-a-configuration-for-a-device)
- [Hardware description files](#hardware-description-files)
- [Support new connector type](#support-new-connector-type)
- [Adding a binary to OpenSwitch](#adding-a-binary-to-openswitch)
- [OpenSwitch plugin for a platform or ASIC](#openswitch-plugin-for-a-platform-or-asic)
	- [Netdev layer](#netdev-layer)
	- [Ofproto layer](#ofproto-layer)

## Overview
This document can be used by platform vendors to port a new platform to OpenSwitch.

## Add a configuration for a device
1. Before building OpenSwitch, the new target platform needs to be added to the ops-build:
   Create a new directory for the new platform target with the name `meta-platform-openswitch-<platform_name>` where <platform_name> is the name of the new platform. This directory should be created in the openswitch workspace: $ <work_dir>/yocto/openswitch.
2. To configure the target platform use following command:
	`make configure <platform_name>`

### References
Refer to the following files in the OpenSwitch sandbox:
1)	[yocto/openswitch/meta-platform-openswitch-as6712](http://git.openswitch.net/cgit/openswitch/ops-build/tree/yocto/openswitch/meta-platform-openswitch-as6712?id=6eb61667d36816a9a94aeb04f67b1c8efd58 "meta-platform-openswitch-as6712")
2)	This commit has changes made to add AS6712 at https://review.openswitch.net/#/c/1766/

## Hardware description files
To add the hardware description file support for the new platform, add the files using the path [openswitch/ops-config-yaml](http://git.openswitch.net/cgit/openswitch/ops-config-yaml/) in the directory `<vendor_name>/<platform_name>`.

### References
In the OpenSwitch sandbox, refer to the [openswitch/ops-config-yaml](http://git.openswitch.net/cgit/openswitch/ops-config-yaml/) repository:
1) [Accton/AS6712-32X](http://git.openswitch.net/cgit/openswitch/ops-hw-config/tree/Accton/AS6712-32X)
2) [README.md](http://git.openswitch.net/cgit/openswitch/ops-hw-config/tree/README.md)

## Support a new connector type
OpenSwitch supports different connectors such as CR4 and SR4.
To add a new connector type, modify the following:
1. Make changes to the header files.
2. Handle conditions such as parsing functions and "if & switch cases" for the new connector.

### References
To add support for new connector types refer to the following repositories:
- [openswitch/ops-intfd](http://git.openswitch.net/cgit/openswitch/ops-intfd/)
	- intfd.h
	- intfd_ovsdb_if.c
	- intfd_utils.c
- [openswitch/ops-openvswitch](http://git.openswitch.net/cgit/openswitch/ops-openvswitch/)
	- openswitch-idl.h
- [openswitch/ops-pmd](http://git.openswitch.net/cgit/openswitch/ops-pmd/)
	- plug.h
	- pmd.h
	- plug.c
	- pm_detect.c

**Note:** The above file list is for reference, changes are not limited to the files in the list.

## Adding a binary to OpenSwitch
If the new platform needs to add a binary for proprietary code from the vendor, then the  binary can be included by listing the location of the file in a bit bake file.

For example, for the AS6712 or AS5712 platforms, OpenSwitch uses platform specific binaries for the platforms. To point to a custom binary file locally:
1) Change the SRC_URI path to the local path of the tarball file:
`yocto/openswitch/meta-distro-openswitch/recipes-asic/opennsl/opennsl-cdp_3.0.0.2.bb`.
An example for AS6712:
`SRC_URI = "file:///home/username/download/opennsl-3.0.0.2-cdp-as6712.tar.bz2 \ "`
2) Enter the `make` command to build OpenSwitch.

## OpenSwitch plugin for a platform or ASIC

The OpenSwitch `switchd` plugin is the platform specific driver that calls into ASIC SDKs. Every ASIC platform needs to implement its own plugin layer. The plugin is a dynamically loaded library during runtime using the library “ldl”. The ops-switchd daemon looks in the following location for the plugins:
`/usr/lib/openvswitch/plugins/`

The platform independent `ops-switchd` calls the `switchd` plugin using the standard interfaces that are defined in two different layers, netdev and ofproto.

### Netdev layer
This layer is responsible for configuring physical layer configurations into ASIC that correspond to the Interface Table in OVSDB, such as speed, mtu, duplex, admin, and state. The layer also reports the interface "transmit and receive" statistics from the hardware. There are multiple netdev classes defined in the plugin, with each class representing a different type of interface:

- system:  Physical front panel ports in the platform.
- internal: Internal logical interfaces such as the bridge interface and Switch Virtual Interfaces (SVI) for inter-VLAN routing.
- loopback: Layer 3 loopback interfaces.
- subinterface: Layer 3 subinterfaces to divide a physical interface into multiple virtual interfaces using dot1q VLAN tagging.

Functions, with different implementations if needed, are registered for each of the classes.
Refer to the opennsl plugin implementation for this layer:
https://git.openswitch.net/cgit/openswitch/ops-switchd-opennsl-plugin/tree/src/netdev-bcmsdk.c

### Ofproto layer
This layer is responsible for configuring all logical layer configurations into ASIC that correspond to the Port Table in OVSDB, such as LAG, VLAN, IP addresses, neighbors, and routes.
The bundle_set is the interface that is called for any Port Table changes. Other functions to support layer 3 configurations are also registered by the ofproto layer.
Refer to the opennsl plugin implementation for this layer:
https://git.openswitch.net/cgit/openswitch/ops-switchd-opennsl-plugin/tree/src/ofproto-bcm-provider.c
