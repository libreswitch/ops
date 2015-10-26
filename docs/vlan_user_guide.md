VLANs
======

## Contents
- [Contents](#contents)
- [Overview](#Overview)
- [Configuring a VLAN](#configuring-VLAN)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Setting up optional configurations](#setting-up-optional-configurations)
	- [Verifying the configuration](#verifying-the-configuration)
- [CLI](#cli)
- [Related features](#related-features)


## Overview
This guide provides detail for managing and monitoring VLANs on the switch. All the VLAN configuratio ns work in VLAN context. For a VLAN to have a physical existance, it has to be associated with one of the interfaces.
All such configurations work in interface context. VLAN mandates the associated in terface to be non-routing interface. By default when the VLAN is created it is not associated with a ny interface. To configure this feature, see the basic configuration.

The main use of VLANs is to ***provide network segmentation***.VLANs also address issues such as *scalability*,*security* and *network management*.

## Configuring a VLAN
### Setting up the basic configuration
1. ++Create a VLAN++
The 'vlan *vlanid*' command creates a VLAN with a given ID and changes the vtysh context to VLAN. If the VLAN already exists then it changes the context to VLAN. The '*vlanid*' in the command depicts the name of the VLAN, which is replaced with VLAN '12' in the following example.
```
switch# configure terminal
switch(config)# vlan 12
switch(config-vlan)#
```
The 'no vlan ID' command deletes the VLAN.
```
switch(config)# no vlan 12
switch(config)
```
2. ++ Enable the VLAN++
The 'no shutdown' command enables a particular VLAN. Once the VLAN is enabled all the configurations take effect.
```
switch(config-vlan)#no shutdown
switch(config-vlan)#
```
The 'shutdown' command disables a particular VLAN.
```
switch(config-vlan)#shutdown
switch(config-vlan)#
```

3. ++ Add VLAN access to the interface or LAG interface++
The 'vlan access ID' command adds an access VLAN to the interface. If the interface is already associated with an access VLAN then this command overrides the previous configuration. There can only be one access VLAN associated with the interface.
```
switch# config terminal
switch(config)# interface 2
switch(config-if)#no routing
switch(config-if)#vlan access 20
```
The 'no vlan access' command removes the access VLAN from the interface.
```
switch(config-if)#no vlan access
```

4. ++ Adding trunk native VLAN++
The 'vlan trunk native ID' command adds a trunk native VLAN to the interface or LAG interface. With this configuration on the interface, all the untagged packets are allowed in the native VLAN.
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

5. ++Adding trunk VLAN++
'vlan trunk allowed ID' command lets the user specify the VLAN allowed in the trunk. Multiple VLANs can be allowed on a trunk.
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
The 'no vlan trunk native' command removes the trunk native VLAN specified by ID from the trunk allowed list.
```
switch(config-if)#no vlan trunk allowed 1
```
```
switch(config-lag-if)#no vlan trunk allowed 1
```

6. ++Add tagging on a native VLAN++
The 'vlan trunk allowed ID' command specifies the VLAN allowed in the trunk. Multiple VLANs can be allowed in a trunk
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
The 'no vlan trunk native tag' command disables tagging on native VLANs.
```
switch(config-if)#vlan trunk native tag
```
```
switch(config-lag-if)#vlan trunk native tag
```
### Setting up an optional configuration
1. ++ Set the description to the VLAN  ++
The optional 'description' command lets the user give a description to the VLAN.
```
switch# config terminal
switch(config)# vlan 12
switch(config-vlan)#description testvlan
```
###Verifying the configuration
1. ++ Viewing a VLAN summary ++
The 'show vlan summary' displays a VLAN summary. The following summary displays a list of configured VLANs:
```
switch# show running-config
Current configuration:
!
vlan 3003
vlan 1
    no shutdown
    description test1\
vlan 1212
    no shutdown
    description test1212
vlan 33
    no shutdown
    description test33
vlan 2
   no shutdown
    description test2
interface bridge_normal
  no routing
```
```
switch# show vlan summary
Number of existing VLANs: 5
```

2. ++ Viewing VLAN detailed information++
The 'show vlan' shows detailed VLAN configurations.
The 'show vlan ID' shows a detailed configuration of a specific VLAN for the following configurations:
```
switch#show running-config
Current configuration:
!
vlan 3003
vlan 1
    no shutdown
    description test1
vlan 1212
    no shutdown
    description test1212
vlan 33
    no shutdown
    description test33
vlan 2
   no shutdown
    description test2
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







## CLI
Click [here](https://openswitch.net/cli_feat.html#cli_command_anchor) for the CLI commands related to the VLAN.


## Related features
When configuring the switch for VLAN, it might also be necessary to configure the [Physical Interface](https://openswitch.net./tbd/other_filefeatures/related_feature1.html#first_anchor) and [LACP](https://openswitch.net./tbd/other_filefeatures/related_feature1.html#first_anchor).
