# Layer3 User Guide

## Overview
This document provides a step-by-step reference for configuration of basic layer3 functionality and features.

* [Layer 3 Interfaces](#layer3-interfaces)
* [Static routes](#static-routes)
* [ECMP](#ecmp)
* [Internal VLAN Management](#internal-vlan-management)
* [References](#references)

## Layer3 Interfaces
OpenSwitch supports configuring IPv4 and IPv6 addresses to layer3 interfaces. Every layer3 interfaces is associated with one VRF. In the first version, only one VRF is supported and hence the association with the VRF is not necessary.

To configure an interface:
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no shutdown
ops-as5712(config-if)# ip address 192.168.1.1/24
ops-as5712(config-if)# ipv6 address 2000::1/120
ops-as5712(config-if)# end
ops-as5712#
```
### VLAN Interfaces
To achieve interVLAN routing, VLAN interfaces are created. VLAN interfaces are configured similar to physical interfaces. In addition to configuring IPv4 or IPv6 addresses, these interfaces are associated with a VLAN. The VLAN ID is part of the name of the VLAN interface being configured.

To configure a VLAN interface for VLAN ID 100:

```
ops-as5712# configure terminal
ops-as5712(config)# interface vlan100
ops-as5712(config-if)# no shutdown
ops-as5712(config-if)# ip address 192.168.1.1/24
ops-as5712(config-if)# ipv6 address 2000::1/120
ops-as5712(config-if)# end
ops-as5712#
```


To view the list of interfaces configured:
```
ops-as5712# show interface

Interface 1 is up
 Admin state is up
 Hardware: Ethernet, MAC Address: 70:72:cf:77:06:df
 IPv4 address 192.168.1.1/24
 MTU 0
 Full-duplex
 Speed 1000 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RX
            0 input packets              0 bytes
            0 input error                0 dropped
            0 CRC/FCS
 TX
            0 output packets             0 bytes
            0 input error                0 dropped
            0 collision

ops-as5712# show ip interface

Interface 1 is up
 Admin state is up
 Hardware: Ethernet, MAC Address: 70:72:cf:77:06:df
 IPv4 address: 192.168.1.1/24
 MTU 0
 RX
          ucast: 10 packets, 750 bytes
          mcast: 0 packets, 0 bytes
 TX
          ucast: 10 packets, 750 bytes
          mcast: 0 packets, 0 bytes

ops-as5712# show interface brief

--------------------------------------------------------------------------------
Ethernet      VLAN    Type Mode   Status  Reason                   Speed     Port
Interface                                                          (Mb/s)    Ch#
--------------------------------------------------------------------------------
 1            --      eth  --     up                               1000     --

```

## Static routes
OpenSwitch supports the configuration of IPv4 and IPv6 static routes.

To add static routes:
```
ops-as5712# configure terminal
ops-as5712(config)# ip route 192.168.2.0/24 192.168.1.2
ops-as5712(config)# ipv6 route 2002::0/120 2000::1
```

To see the active routes in the system, including static routes:
```
ops-as5712# show ip route

Displaying ipv4 routes selected for forwarding

'[x/y]' denotes [distance/metric]

10.0.30.0/24,  1 unicast next-hops
        via  3,  [0/0],  connected
10.0.20.0/24,  1 unicast next-hops
        via  2,  [0/0],  connected
10.0.10.0/24,  1 unicast next-hops
        via  1,  [0/0],  connected
10.0.40.0/24,  1 unicast next-hops
        via  4,  [0/0],  connected
10.0.70.0/24,  2 unicast next-hops
        via  10.0.40.2,  [1/0],  static
        via  10.0.30.2,  [1/0],  static

ops-as5712#

```
To see all the routes in the system:
```
ops-as5712# show rib

Displaying ipv4 rib entries

'*' denotes selected
'[x/y]' denotes [distance/metric]

*10.0.30.0/24,  1 unicast next-hops
        *via  3,  [0/0],  connected
*10.0.20.0/24,  1 unicast next-hops
        *via  2,  [0/0],  connected
*10.0.10.0/24,  1 unicast next-hops
        *via  1,  [0/0],  connected
*10.0.40.0/24,  1 unicast next-hops
        *via  4,  [0/0],  connected
*10.0.70.0/24,  2 unicast next-hops
        *via  10.0.40.2,  [1/0],  static
        *via  10.0.30.2,  [1/0],  static

No ipv6 rib entries

ops-as5712#

```

## ECMP
ECMP capability in OpenSwitch is currently available for IPv4 and IPv6 routes. ECMP can be enabled/disabled at the system level. By default ECMP is enabled.

To disable ECMP on OpenSwitch:
```
ops-as5712# configure terminal
ops-as5712(config)# ip ecmp disable
```
To re-enable ECMP:
```
ops-as5712# configure terminal
ops-as5712(config)# no ip ecmp disable
```

By default, ECMP uses four tuple in the hash calculation:
 - SrcIP
 - DstIP
 - SrcPort
 - DstPort

Each of these fields can be explicitly disabled from the hash calculations.
For example, to disable the dst-ip field from the ECMP hash calculation use the following commands:
```
ops-as5712# configure terminal
ops-as5712(config)# ip ecmp load-balance dst-ip disable
```
To add back dst-ip in the hash calculation:
```
ops-as5712# configure terminal
ops-as5712(config)# no ip ecmp load-balance dst-ip disable
```
To see all the tuples that can be added/removed from the ECMP hash:
```
ops-as5712# configure terminal
ops-as5712(config)# ip ecmp load-balance ?
  dst-ip    Load balancing by destination IP
  dst-port  Load balancing by destination port
  src-ip    Load balancing by source IP
  src-port  Load balancing by source port
```

If the platform supports it, OpenSwitch will enable "resilient ECMP" by default to preserve in-flight traffic flows when ECMP group membership changes.
To disable resilient ECMP, use the following commands:
```
ops-as5712# configure terminal
ops-as5712(config)# ip ecmp load-balance resilient disable
```
To re-enable resilient ECMP:
```
ops-as5712# configure terminal
ops-as5712(config)# no ip ecmp load-balance resilient disable
```

To see the complete ECMP configuration:
```
ops-as5712# show ip ecmp

ECMP Configuration
---------------------

ECMP Status        : Enabled
Resilient Hashing  : Enabled

ECMP Load Balancing by
------------------------
Source IP          : Enabled
Destination IP     : Enabled
Source Port        : Enabled
Destination Port   : Enabled
```

## Internal VLAN Management
Every layer3 interface is associated with a unique VLAN ID. By default, OpenSwitch uses VLAN IDs from the range 1024-4094 for this purpose. However, this range is configurable. The order in which the VLAN IDs are used in this range is also be specified using "ascending" or "descending" in the CLI.
To configure the VLAN range for internal use:
```
ops-as5712# configure terminal
ops-as5712(config)# vlan internal range 400 500 ascending
```
To show the configured VLAN range
```
ops-as5712# sh vlan internal

Internal VLAN range  : 400-500
Internal VLAN policy : ascending
------------------------
Assigned Interfaces:
        VLAN            Interface
        ----            ---------
        401             2
        400             1

ops-as5712#
```

## References
* [Layer 3 Design](layer3_design)
* [Layer 3 Interfaces](layer3_interface_cli)
* [ECMP](layer3_ecmp_cli)
* [Internal VLAN Management](vlan_user_guide)