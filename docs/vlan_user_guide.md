## VLANs


## Contents
- [Overview](#overview)
- [Configuring a VLAN](#configuring-a-vlan)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
- [Configuring internal VLAN range](#configuring-internal-vlan-range)
- [Troubleshooting](#troubleshooting)
	- [Troubleshooting an internal VLAN](#troubleshooting-an-internal-vlan)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
This guide provides detail for managing and monitoring VLANs on the switch. All the VLAN configurations work in VLAN context. For a VLAN to have a physical existance, it has to be associated with one of the interfaces.
All such configurations work in the interface context. VLAN mandates the associated interface to be non-routing interface. When the VLAN is created, by default it is not associated with any interface. To configure this feature, see [Setting up the basic configuration](#setting-up-the-basic-configuration).

The main use of VLANs is to provide network segmentation. VLANs also address issues, such as scalability, security and network management.

## Configuring a VLAN
### Setting up the basic configuration
1. Create a VLAN.
The `vlan <vlanid>` command creates a VLAN with a given ID and changes the vtysh context to VLAN. If the VLAN already exists, it then changes the context to VLAN. The `vlanid`' in the command depicts the name of the VLAN, which is replaced with VLAN '12' in the following example:
```
switch# configure terminal
switch(config)# vlan 12
switch(config-vlan)#
```
The `no vlan ID` command deletes the VLAN.
```
switch(config)# no vlan 12
switch(config)
```
2. Enable the VLAN.
The `no shutdown` command enables a particular VLAN. Once the VLAN is enabled all the configurations take effect.
```
switch(config-vlan)#no shutdown
switch(config-vlan)#
```
The `shutdown` command disables a particular VLAN.
```
switch(config-vlan)#shutdown
switch(config-vlan)#
```

3. Add VLAN access to the interface or LAG interface.
The `vlan access ID` command adds an access VLAN to the interface. If the interface is already associated with an access VLAN, then this command overrides the previous configuration. Only one access VLAN can be associated with the interface.
```
switch# config terminal
switch(config)# interface 2
switch(config-if)#no routing
switch(config-if)#vlan access 20
```
The `no vlan access` command removes the access VLAN from the interface.
```
switch(config-if)#no vlan access
```

4. Adding trunk native VLAN.
The `vlan trunk native ID` command adds a trunk native VLAN to the interface or LAG interface. With this configuration on the interface, all the untagged packets are allowed in the native VLAN.
```
switch# config terminal
switch(config)# interface 21
switch(config-if)#no routing
switch(config-if)#vlan trunk native 1
```
```
switch# config terminal
switch(config)#interface lag 21
switch(config-lag-if)#no routing
switch(config-lag-if)#vlan trunk native 1
```
The 'no vlan trunk native' command removes trunk native VLAN  from the interface.
```
switch(config-if)#no vlan trunk native
```
```
switch(config-lag-if)#no vlan trunk native
```

5. Adding trunk VLAN.
The `vlan trunk allowed ID` command lets you specify the VLAN allowed in the trunk. Multiple VLANs can be allowed on a trunk.
```
switch# config terminal
switch(config)# interface 21
switch(config-if)#no routing
switch(config-if)#vlan trunk allowed 1
```
```
switch# config terminal
switch(config)#interface lag 21
switch(config-lag-if)#no routing
switch(config-lag-if)#vlan trunk allowed 1
```
The `no vlan trunk native` command removes the trunk native VLAN specified by ID from the trunk allowed list.
```
switch(config-if)#no vlan trunk allowed 1
```
```
switch(config-lag-if)#no vlan trunk allowed 1
```

6. Add tagging on a native VLAN.
The `vlan trunk allowed ID` command specifies the VLAN allowed in the trunk. Multiple VLANs can be allowed in a trunk.
```
switch# config terminal
switch(config)# interface 21
switch(config-if)#no routing
switch(config-if)#vlan trunk native tag
```
```
switch# config terminal
switch(config)# interface lag 21
switch(config-lag-if)#no routing
switch(config-lag-if)#vlan trunk native tag
```
The `no vlan trunk native tag` command disables tagging on native VLANs.
```
switch(config-if)#vlan trunk native tag
```
```
switch(config-lag-if)#vlan trunk native tag
```
### Verifying the configuration
1. Viewing a VLAN summary.
The `show vlan summary` displays a VLAN summary. The following summary displays a list of configured VLANs:
```
switch# show running-config
Current configuration:
!
vlan 3003
vlan 1
    no shutdown
vlan 1212
    no shutdown
vlan 33
    no shutdown
vlan 2
   no shutdown
interface bridge_normal
  no routing
```
```
switch# show vlan summary
Number of existing VLANs: 5
```

2. Viewing VLAN detailed information.
The `show vlan` shows detailed VLAN configurations.
The `show vlan ID` shows a detailed configuration of a specific VLAN for the following configurations:
```
switch#show running-config
Current configuration:
!
vlan 3003
vlan 1
    no shutdown
vlan 1212
    no shutdown
vlan 33
    no shutdown
vlan 2
   no shutdown
interface bridge_normal
  no routing
interface 2
    no routing
    vlan trunk native 1
    vlan trunk allowed 33
interface 1
    no routing
    vlan access 1
```
```
switch#show vlan
...................................................................................
VLAN  Name         Status    Reason        Reserved       Ports
...................................................................................
3003  vlan3003     down     admin_down     (null)
1     vlan1        up       ok             (null)         2, 1
1212  vlan1212     up       ok             (null)
33    vlan33       up       ok             (null)         2
2     vlan2        up       ok             (null)
```
```
switch#show vlan 33
...................................................................................
VLAN  Name         Status    Reason        Reserved       Ports
...................................................................................
33    vlan33       up       ok             (null)         2
```

## Configuring internal VLAN range
The `vlan internal range start-vlan-id end-vlan-id [ ascending | decsending ]` command sets the range for internal VLANs in ascending or descending order. For every L3 interfaces, there should be one internal VLAN. Whenever a user configures interfaces, one of the VLAN from this range is assigned to the interface.
```
switch(config)# vlan internal range 4093 4094 ascending
switch(config)# interface 1
switch(config-if)# no shutdown
switch(config-if)# interface 2
switch(config-if)# no shutdown
switch(config-if)# do show vlan internal

Internal VLAN range  : 4093-4094
Internal VLAN policy : ascending
------------------------
Assigned Interfaces:
        VLAN            Interface
        ----            ---------
        4093            1
        4094            2
```
## Troubleshooting
### Troubleshooting an internal VLAN
Every L3 interface must have one internal VLAN. When an interface does not have an internal VLAN because of it running short of internal VLANs that can be checked in the "show vrf" output, the interface that does not have an internal VLAN will have a status of `error: no_internal_vlan`.

```
switch# configure terminal
switch(config)# vlan internal range 4093 4094 ascending
switch(config)# interface 1
switch(config-if)# no shutdown
switch(config-if)# interface 2
switch(config-if)# no shutdown
switch(config-if)# do show vlan internal

Internal VLAN range  : 4093-4094
Internal VLAN policy : ascending
------------------------
Assigned Interfaces:
        VLAN            Interface
        ----            ---------
        4093            1
        4094            2
switch(config-if)# interface 3
switch(config-if)# no shutdown
switch(config-if)# do show vlan internal

Internal VLAN range  : 4093-4094
Internal VLAN policy : ascending
------------------------
Assigned Interfaces:
        VLAN            Interface
        ----            ---------
        4093            1
        4094            2
switch(config-if)# do show vrf
VRF Configuration:
------------------
VRF Name : vrf_default

        Interfaces :     Status :
        -------------------------
        3                error: no_internal_vlan
        2                up
        1                up
switch(config-if)#

```
## CLI
Click [here](/documents/user/VLAN_cli) for the CLI commands related to the VLAN.


## Related features
When configuring the switch for VLAN, it might also be necessary to configure the [Physical Interface](/documents/user/interface_cli) and [LACP](/documents/user/lacp_cli).
