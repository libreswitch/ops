#Platform user guide

## Contents

- [Overview](#overview)
- [RS232/USB Serial Interface](#rs232usb-serial-interface)
- [ONIE for forwarding box OS installation](#onie-for-forwarding-box-os-installation)
- [40G default interfaces](#40g-default-interfaces)
- [10G speed support via splitter cable](#10g-speed-support-via-splitter-cable)
- [Redundant hot-swappable AC power supply](#redundant-hot-swappable-ac-power-supply)

## Overview
This guide provides details for using platform related features.

## RS232/USB Serial Interface
Default baud rate: 115200
Connect to the console port of the switch with a USB to serial adapter. Ensure you have the correct COM port associated with your adapter, for example COM5.
On return key a command prompt should appear in the CLI:

```
root@ops-as6712:~#
```

## ONIE for forwarding box OS installation
The user guide for this is documented [here] (http://www.openswitch.net/documents/dev/deploy-to-physical-switch#installing-using-onie-provisioning-mechanisms).


### 40G default interfaces
All 32 ports of AS6712 are 40G by default.
To enable a 40G port, use the following commands:
```
switch# configure
switch(config)# interface 1
switch(config-if)# no shutdown
```
To verify link speed and admin state of an interface:
```
switch# show interface 1

Interface 1 is down
 Admin state is up
 State information: admin_down
 Hardware: Ethernet, MAC Address: 48:0f:cf:ad:33:cd
 MTU 9192
 Full-duplex
 Speed 40000 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is on, output flow-control is on
 RX
            0 input packets              0 bytes
            0 input error                0 dropped
            0 CRC/FCS
 TX
            0 output packets             0 bytes
            0 input error                0 dropped
            0 collision
```
### 10G speed support via splitter cable
Currently the AS6712 supports only ports 5 to 28 being split. Each of these ports is capable of splitting into four 10G ports.
Split ports are represented with a hyphen with respect to the parent interface: <<parent_interface>parent_interface>-<<child_interface>child_interface>. For example, 5-1.
To split a port, use the following commands:
```
switch# configure
switch(config)# int 5
switch(config-if)# split
Warning: This will remove all L2/L3 configuration on parent interface.
Do you want to continue [y/n]? y
```
To verify the port has split lanes:
```
switch# show interface 5

Interface 19 is down (Administratively down)
 Admin state is down
 State information: lanes_split
 Hardware: Ethernet, MAC Address: 48:0f:cf:ad:33:cd
 MTU 9192
 Half-duplex
 Speed 0 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is on, output flow-control is on
 RX
           18 input packets           2136 bytes
            0 input error                0 dropped
            0 CRC/FCS
 TX
           21 output packets          2446 bytes
            0 input error                1 dropped
            0 collision
```
To enable the split ports:
```
switch(config-if)# int 5-1
switch(config-if)# no shutdown
switch(config-if)# int 5-2
switch(config-if)# no shutdown
switch(config-if)# int 5-3
switch(config-if)# no shutdown
switch(config-if)# int 5-4
switch(config-if)# no shutdown
```
To verify link speed and admin state of the split port:
```
switch# show interface 5-1

Interface 5-1 is down
 Admin state is up
 Hardware: Ethernet, MAC Address: 48:0f:cf:ad:33:cd
 IPv4 address 42.0.0.191/8
 MTU 1500
 Full-duplex
 Speed 10000 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RX
           18 input packets           2136 bytes
            0 input error                0 dropped
            0 CRC/FCS
 TX
           21 output packets          2446 bytes
            0 input error                1 dropped
            0 collision
```

To switch from a split port back to the default 40G port:
```
switch# configure
switch(config)# int 5
switch(config-if)# no split
Warning: This will remove all L2/L3 configuration on parent interface.
Do you want to continue [y/n]? y
```

## Redundant hot-swappable AC power supply
This feature is enabled by default. The user guide for this is documented [here] (http://openswitch.net/documents/user/system_user_guide).
