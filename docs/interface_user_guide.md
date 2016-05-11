# Physical Interface

## Contents

- [Contents](#contents)
- [Overview](#overview)
- [Configuring the physical interface](#configuring-the-physical-interface)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Setting up optional configurations](#setting-up-optional-configurations)
- [Verifying the configuration](#verifying-the-configuration)
	- [Viewing interface information](#viewing-interface-information)
	- [Viewing snapshot of active configurations](#viewing-snapshot-of-active-configurations)
- [Troubleshooting the configuration](#troubleshooting-the-configuration)
	- [Condition](#condition)
	- [Cause](#cause)
	- [Remedy](#remedy)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
This guide provides detail for managing and monitoring the physical interface present in the switch. All configurations work in interface context. When the interface is running, all the default configurations take effect. To change the default configuration, see [Setting up the basic configuration](#intfconfopt).

## Configuring the physical interface
### Setting up the basic configuration
1. Change to the interface context.
The `interface` *`interface`* command changes the vtysh context to interface. The *`interface`* variable in the command depicts the name of the interface, such as interface "1" in the following example.
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)#
```

2. Enable the interface.
The `no shutdown` command enables a particular interface on the switch. Once the interface is enabled, all other configurations take effect.
```
ops-as5712(config-if)# no shutdown
ops-as5712(config-if)#
```

3. Set the interface speed.
The `speed` command sets the interface speed. Supported speeds are 1Gbps, 10 Gbps and 40 Gbps. Depending upon the interface type, these configurations may or may not take effect.
```
ops-as5712(config-if)# speed 1000
ops-as5712(config-if)#
```
The `no speed` command reverts the interface speed to auto mode.
```
ops-as5712(config-if)# no speed
ops-as5712(config-if)#
```

4. Set the interface duplexity.
The `duplex` command sets the interface duplexity to either half or full duplex.
```
ops-as5712(config-if)# duplex half
ops-as5712(config-if)#
```
The `no duplex` commands reverts the interface duplexity to default to `full`.
```
ops-as5712(config-if)# no duplex
ops-as5712(config-if)#
```

5. Set the interface MTU.
The MTU of a communications protocol refers to the size in bytes of the largest frame (Ethernet) or packet (IP) that can be sent on the network. Different protocols support a variety of MTU sizes. Most IP over Ethernet implementations uses the Ethernet V2 frame format, which specifies an MTU of 1500 bytes. Jumbo frames are Ethernet frames containing more than 1500 bytes.
```
ops-as5712(config)# mtu 2000
ops-as5712(config)#
```
Note: Maximum configurable MTU value for jumbo frame is 9192 which allows inbound jumbo packets up to 9216(9192+padding bytes(6+6+4+4+2+2 i.e DA + SA + STAG + CTAG + LEN + FCS) byte, while tagged packets of MTU + 4 bytes are permitted.

 The `no mtu` commands reverts the mtu of the interface to default auto mode.
 The 'mtu auto' command sets MTU to system default.
```
ops-as5712(config-if)# no mtu
ops-as5712(config-if)#
```


6. Select the interface autonegotiation state.
The `autonegotiation` command turns the autonegotiation state on or off. The `no autonegotiation` command sets the autonegotiation state to default.
```
ops-as5712(config-if)# autonegotiation on
ops-as5712(config-if)#
ops-as5712(config-if)# no autonegotiation
ops-as5712(config-if)#
```

7. Set the flowcontrol.
The `flowcontrol` command enables the flow control mechanism (pause frame technique). The ‘no flowcontrol’ command disables the flow control mechanism. This command is executed to receive and send pause frames individually.
```
ops-as5712(config-if)# flowcontrol receive on
ops-as5712(config-if)# flowcontrol send on
ops-as5712(config-if)#
ops-as5712(config-if)# no flowcontrol receive
ops-as5712(config-if)# no flowcontrol send on
```

### Setting up optional configurations
1. Set up interface description.
The `description` command associates a description with an interface.
```
ops-as5712(config-if)# description This is interface 1
ops-as5712(config-if)#
```

2. Configure the interface as L2 or L3.
By default all interfaces are configured as L3. If an interface is not configured as L3, the `routing` command can be used to set the interface to L3.
```
ops-as5712(config-if)# routing
ops-as5712(config-if)#
```
To configure the interface as L2, the `no routing` command is used.
```
ops-as5712(config-if)# no routing
ops-as5712(config-if)#
```

3. Set the IP address of the interface.
The `ip address` and `ipv6 address` commands set the ip address of the interface. These two commands work only if the interface is configured as L3.
```
ops-as5712(config-if)# ip address 10.10.10.2/24
ops-as5712(config-if)#
ops-as5712(config-if)#  ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334/24
```
To set a secondary ip address, append the ‘secondary’ keyword at the end as shown below:
```
ops-as5712(config-if)# ip address 10.10.10.2/24 secondary
ops-as5712(config-if)#
ops-as5712(config-if)#  ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334/24 secondary
```
To remove the ipv4/ipv6 interface address, use the `no ip address` and the `no ipv6 address` commands.
```
ops-as5712(config-if)# no ip address 10.10.10.2/24
ops-as5712(config-if)# no ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334/24
ops-as5712(config-if)# no ip address 10.10.10.2/24 secondary
ops-as5712(config-if)#  no ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334/24 secondary
```

## Verifying the configuration
### Viewing interface information
The `show interface` and `show interface brief` commands display information about the state and configuration of all the interfaces. The information includes details on speed, mtu, packet counts, and so on.
```
ops-as5712# show interface

Interface 45 is down (Administratively down)
 Admin state is down
 Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
 MTU 1500
 Half-duplex
 Speed 0 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is on, output flow-control is on
 RX
      0 input packets   0 bytes
      0 input error     0 dropped
      0 short frame     0 overrun
      0 CRC/FCS
 TX
      0 output packets   0 bytes
      0 input error      4 dropped
      0 collision

Interface 36 is down (Administratively down)
 Admin state is down
 Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
 MTU 1500
 Half-duplex
 Speed 0 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is on, output flow-control is on
 RX
      0 input packets   0 bytes
      0 input error     0 dropped
      0 short frame     0 overrun
      0 CRC/FCS
 TX
      0 output packets   0 bytes
      0 input error      4 dropped
      0 collision
.........
.........
ops-as5712# show interface brief
....................................................................................................
Ethernet    VLAN   Type   Mode    Status   Reason                   Speed     Port
Interface                                                           (Mb/s)    Ch#
....................................................................................................
 45          ..   eth     ..       down    Administratively down    auto      ..
 36          ..   eth     ..       down    Administratively down    auto      ..
 9           ..   eth     ..       down    Administratively down    auto      ..
...............
...............
```

To view information for a particular interface use the `show interface` *`interface`* or `show interface` *`interface`* `brief` commands, where the *`interface`* variable is the name of the interface, such as interface "1" in the following example.
```
ops-as5712# show interface 1

Interface 1 is up
 Admin state is up
 Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
 MTU 1500
 Full-duplex
 Speed 1000 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RXc
      50 input packets     14462 bytes
      0 input error        7 dropped
      0 short frame        0 overrun
      0 CRC/FCS
 TX
      213 output packets  34506 bytes
      0 input error       4 dropped
      0 collision
ops-as5712# show interface 1 brief
....................................................................................................
Ethernet    VLAN   Type   Mode    Status     Reason                Speed     Port
Interface                                                          (Mb/s)    Ch#
....................................................................................................
  1          ..    eth     ..      down    Administratively down    auto     ..
```
### Viewing snapshot of active configurations
The `show running-config interface` and `show running-config interface` *`interface`* commands are used to see a snapshot of active configurations for all interfaces and if used with the interface name (*`interface`*), active configurations for a particular interface are displayed.
```
ops-as5712# show running-config interface
Interface 2
   no shutdown
   speed 40000
   autonegotiation on
   exit
Interface 1
   no shutdown
   exit
.............
.............
ops-as5712# show running-config interface 2
Interface 2
   no shutdown
   speed 40000
   autonegotiation on
   exit
```

## Troubleshooting the configuration
### Condition
Unable to set the ipv4/ipv6 address even after enabling the interface.
### Cause
The interface may be configured as an L2.
### Remedy
Configure the interface as an L3 using the `routing` command. See the Command Reference for more information.

## CLI
Click [here](/documents/user/interface_cli) to access the CLI commands related to the Physical interface.

## Related features
No related features.
