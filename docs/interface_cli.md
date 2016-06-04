# Interface Commands


## Contents

- [Interface configuration commands](#interface-configuration-commands)
	- [Change to interface context](#change-to-interface-context)
	- [Enable an interface](#enable-an-interface)
	- [Disable an interface](#disable-an-interface)
	- [Enable routing on an interface](#enable-routing-on-an-interface)
	- [Disable routing on an interface](#disable-routing-on-an-interface)
	- [Set interface speed](#set-interface-speed)
	- [Set interface speed to default](#set-interface-speed-to-default)
	- [Set interface MTU](#set-interface-mtu)
	- [Set interface MTU to default](#set-interface-mtu-to-default)
	- [Set interface duplexity](#set-interface-duplexity)
	- [Set interface duplexity to default](#set-interface-duplexity-to-default)
	- [Enable flow control](#enable-flow-control)
	- [Set flowcontrol to default](#set-flowcontrol-to-default)
	- [Set autonegotiation state](#set-autonegotiation-state)
	- [Set autonegotiation to default](#set-autonegotiation-to-default)
	- [Set an IPv4 address for an interface](#set-an-ipv4-address-for-interface)
	- [Remove the IPv4 address for an interface](#remove-the-ipv4-address-for-interface)
	- [Set an IPv6 address for an interface](#set-an-ipv6-address-for-interface)
	- [Remove the IPv6 address for an interface](#remove-the-ipv6-address-for-interface)
	- [Split a QSPF interface](#spilt-a-qspf-interface)
- [Interface show commands](#interface-show-commands)
	- [Show all interfaces](#show-all-interfaces)
	- [Show the interface configuration](#show-the-interface-configuration)
	- [Show transceiver information for all interfaces](#show-transceiver-information-for-all-interfaces)
	- [Show transceiver information for an interface](#show-transceiver-information-for-an-interface)
	- [Show the running configuration for all interfaces](#show-the-running-configuration-for-all-interfaces)
	- [Show the running configuration for an interface](#show-the-running-configuration-for-an-interface)
	- [Show transceiver DOM information for all interfaces](#show-transceiver-dom-information-for-all-interfaces)
	- [Show transceiver DOM information for an interface](#show-transceiver-dom-information-for-an-interface)

## Interface configuration commands
In vtysh every command belongs to a particular context. All interface configuration commands, except `interface`, work in the interface context.
### Change to interface context
#### Syntax
`interface <interface>`
#### Description
This command changes the vtysh context to interface. This command works in the config context.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)#
```
### Enable an interface
#### Syntax
`no shutdown`
#### Description
This command enables an interface.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no shutdown
```
### Disable an interface
#### Syntax
`shutdown`
#### Description
This command disables an interface.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# shutdown
```
### Enable routing on an interface
#### Syntax
`routing`
#### Description
This command enables routing on an interface.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# routing
```
### Disable routing on an interface
#### Syntax
`no routing`
#### Description
This command disables routing on an interface.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no routing
```
### Set interface speed
#### Syntax
`speed (auto|1000|10000|100000|40000)`
#### Description
This command sets the operating speed of an interface.
#### Authority
All users.
#### Parameters
Choose one of the following parameters as the speed:

| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **auto** | Required | Literal | Speed set to auto mode. |
| **1000** | Required | Literal | Speed set to 1 Gbps. |
| **10000** | Required | Literal | Speed set to 10 Gbps. |
| **100000** | Required | Literal | Speed set to 100 Gbps. |
| **40000** | Required | Literal | Speed set to 40 Gbps. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# speed 10000
```
### Set interface speed to default
#### Syntax
`no speed`
#### Description
This command sets the operating speed of an interface to default. The default setting is auto.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no speed
```
### Set interface MTU
#### Syntax
`mtu (auto|<value>)`
#### Description
This command sets the MTU (maximum transmission unit) of an interface.
#### Authority
All users.
#### Parameters
Choose one of the following parameters as the MTU:

| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **auto** | Required | Literal | MTU set to auto mode. |
| *value* | Required | 576-9192 | MTU value between 576 and 9192 bytes.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# mtu auto
ops-as5712(config-if)# mtu 580
```
### Set interface MTU to default
#### Syntax
`no mtu`
#### Description
This command sets the MTU (maximum transmission unit) of an interface to default. The default setting is auto.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no mtu
```
### Set interface duplexity

#### Syntax
`duplex (half|full)`
#### Description
This command sets the duplexity of an interface to either half duplex or full duplex.
#### Authority
All users.
#### Parameters
Choose one of the following parameters as duplexity:

| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **half** | Required | Literal | Set mode as half duplex. |
| **full** | Required | Literal | Set mode as full duplex. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# duplex half
```
### Set interface duplexity to default
#### Syntax
`no duplex`
#### Description
This command sets the duplexity of an interface to default. The default mode is full.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no duplex
```
### Enable flow control
#### Syntax
`flowcontrol (receive|send) (off|on)`
#### Description
This command enables flow control for sending and receiving pause frames.
#### Authority
All users.
#### Parameters
Choose one of the following parameters to set flow control to receive pause frames or send pause frames:

| Parameter 1 | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **receive** | Required | Literal | Select the status for receiving pause frames. |
| **send** | Required | Literal |Select the status for sending pause frames. |

Choose one of the following parameters to either switch flow control on or off:

| Parameter 2 | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **off** | Required | Literal | Switches flow control off for the above parameter. |
| **on** | Required | Literal | Switches flow control on for the above parameter. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# flowcontrol receive on
ops-as5712(config-if)# flowcontrol send on
```
### Set flowcontrol to default
#### Syntax
`no flowcontrol (receive|send)`
#### Description
This command sets the flow control to default. The default is off.
#### Authority
All users.
#### Parameters
Choose one of the following parameters to select whether to disable *receive* flow control or *send* flow control:

| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **receive** | Required | Literal | Select the status for receiving pause frames. |
| **send** | Required | Literal | Select the status for sending pause frames. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no flowcontrol receive
ops-as5712(config-if)# no flowcontrol send
```
### Set autonegotiation state
#### Syntax
`autonegotiation (on|off)`
#### Description
This command sets the autonegotiation state of the interface.
#### Authority
All users.
#### Parameters
Choose one of the following parameters to switch the autonegotiation state on or off:

| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------------------|
| **off** | Required | Literal | Switch off auto negotiation. |
| **on** | Required | Literal | Switch on auto negotiation. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# autonegotiation on
```
### Set autonegotiation to default
#### Syntax
`no autonegotiation`
#### Description
This command sets the autonegotiation state to default. The default is off.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no autonegotiation
```
### Set an IPv4 address for an interface
#### Syntax
`ip address <ipv4_address/mask> [secondary]`
#### Description
This command sets an IPv4 address for an interface. This command only works when the interface is configured as L3.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv4_address/mask* | Required | A.B.C.D/M | IPv4 address with mask for the interface. |
| **secondary** | Optional| Literal  | Select this if the IPv4 address is a secondary address. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip address 16.93.50.2/24
ops-as5712(config-if)# ip address 16.93.50.3/24 secondary
```
### Remove the IPv4 address for an interface
#### Syntax
`no ip address <ipv4_address/mask> [secondary]`
#### Description
This command removes the IPv4 address associated with an interface. This command works only when the interface is configured as L3.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv4_address/mask* | Required | A.B.C.D/M | IPv4 address with mask for the interface. |
| **secondary** | Optional| Literal  | Select this if the  IPV4 address is a secondary address. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no ip address 16.93.50.2/24
ops-as5712(config-if)# no ip address 16.93.50.3/24 secondary
```

### Set an IPv6 address for an interface
#### Syntax
`ipv6 address <ipv6_address/mask> [secondary]`
#### Description
This command sets an IPv6 address for an interface. This command only works when the interface is configured as L3.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv6_address/mask* | Required | X:X::X:X/M | IPv6 address with mask for the interface. |
| **secondary** | Optional| Literal  | Select this if the IPv6 address is a secondary address. |
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334/24
ops-as5712(config-if)# ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:733/24 secondary
```
### Remove the IPv6 address for an interface
#### Syntax
`no ipv6 address <ipv6_address/mask> [secondary]`
#### Description
This command removes the IPv6 address associated with an interface. This command only works when the interface is configured as L3.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *ipv6_address/mask* | Required | X:X::X:X/M | IPv6 address with mask for the interface. |
| **secondary** | Optional| Literal  | Select this if the IPv6 address is a secondary address.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334/24
ops-as5712(config-if)# no ipv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:733/24 secondary
```
### Split a QSPF interface
#### Syntax
`[no] split`
#### Description
The `split` command, splits a QSPF interface to work as four 10Gb interfaces. The QSPF interface must support splitter cables in order to split the interface.

The `no split` command combines the split QSPF interface to work as one 40Gb interface.

The split interface names are appended with '-1','-2','-3' and '-4'. For example, if the QSPF interface name is 54 then the split interface names are 54-1, 54-2, 54-3 and 54-4.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# interface 54
ops-as5712(config)# split

ops-as5712# configure terminal
ops-as5712(config)# interface 54
ops-as5712(config)# no split
```
## Interface show commands
### Show all interfaces
#### Syntax
`show interface [brief]`
#### Description
This command displays various switch interfaces with their configurations and statuses.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **brief** | Optional| Literal  | Select this to display the output in tabular format. |
#### Examples
```
ops-as5712# show interface

Interface 1 is down (Administratively down)
Admin state is down
State information: admin_down
Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
MTU 9192
Half-duplex
Speed 0 Mb/s
Auto-Negotiation is turned on
Input flow-control is on, output flow-control is on
RX
   0 input packets 0 bytes
   0 input error   0 dropped
   0 CRC/FCS
TX
   0 output packets 0 bytes
   0 input error    4 dropped
   0 collision

Interface 10 is down (Administratively down)
Admin state is down
State information: admin_down
Hardware: Ethernet, MAC Address: 70:72:cf:fd:e7:b4
MTU 9192
Half-duplex
Speed 0 Mb/s
Auto-Negotiation is turned on
Input flow-control is on, output flow-control is on
RX
   0 input packets 0 bytes
   0 input error   0 dropped
   0 CRC/FCS
TX
   0 output packets 0 bytes
   0 input error    4 dropped
   0 collision
.........
.........
ops-as5712# show interface brief
....................................................................................................
Ethernet      VLAN     Type    Mode    Status         Reason             Speed   Port
Interface                                                                (Mb/s)   Ch#
....................................................................................................
 1             ..       eth     ..      down     Administratively down    auto    ..
 10            ..       eth     ..      down     Administratively down    auto    ..
 11            ..       eth     ..      down     Administratively down    auto    ..
...............
...............
```
### Show the interface configuration

#### Syntax
`show interface <interface> [brief]`
#### Description
This command displays the configuration and status of an interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. |
| **brief** | Optional| Literal  | Select this to display the output in tabular format. |
#### Examples
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
 RX
      0 input packets     0 bytes
      0 input error       0 dropped
      0 CRC/FCS
 TX
      0 output packets  0 bytes
      0 input error     0 dropped
      0 collision
ops-as5712# show interface 1 brief
....................................................................................................
Ethernet    VLAN   Type   Mode    Status   Reason                    Speed     Port
Interface                                                            (Mb/s)    Ch#
....................................................................................................
  1          ..    eth     ..     down    Administratively down       auto     ..
```
### Show transceiver information for all interfaces
#### Syntax
`show interface transceiver [brief]`
#### Description
This command displays information about pluggable modules or fixed interfaces present in the switch.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **brief** | Optional| Literal  | Select this to display the output in tabular format. |
#### Examples
```
ops-as5712# show interface transceiver

Interface 1:
 Connector: SFP+
 Transceiver module: SFP_RJ45
 Connector status: supported
 Vendor name: AVAGO
 Part number: ABCU-5710RZ-HP8
 Part revision:
 Serial number: MY36G2C52D
 Supported speeds: 1000

Interface 10:
 Connector: SFP+
 Transceiver module: not present

Interface 11:
 Connector: SFP+
 Transceiver module: not present
 -------
 -------
ops-as5712# show interface transceiver brief

-----------------------------------------------
Ethernet      Connector    Module     Module
Interface                  Type       Status
-----------------------------------------------
 1              SFP+       SFP_RJ45   supported
 10             SFP+       --         --
 11             SFP+       --         --
 12             SFP+       --         --
 13             SFP+       --         --
 -------
 -------

```
### Show transceiver information for an interface
#### Syntax
`show interface <interface> transceiver [brief]`
#### Description
This command displays transceiver information about a particular switch interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. |
| **brief** | Optional| Literal  | Select this to display the output in tabular format. |
#### Examples
```
ops-as5712# show interface 1 transceiver

Interface 1:
 Connector: SFP+
 Transceiver module: SFP_RJ45
 Connector status: supported
 Vendor name: AVAGO
 Part number: ABCU-5710RZ-HP8
 Part revision:
 Serial number: MY36G2C52D
 Supported speeds: 1000

ops-as5712# show interface 1 transceiver brief

-----------------------------------------------
Ethernet      Connector    Module     Module
Interface                  Type       Status
-----------------------------------------------
 1              SFP+       SFP_RJ45   supported
```
### Show the running configuration for all interfaces
#### Syntax
`show running-config interface`
#### Description
This command displays active configurations of various switch interfaces.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
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
```

```
ops-as5712# show running-config interface
interface bridge_normal
   no shutdown
   no routing
   exit
interface 2
   no shutdown
   lag 100
   exit
interface lag 100
   no routing
   lacp mode active
```

### Show the running configuration for an interface
#### Syntax
`show running-config interface <interface>`
#### Description
This command displays active configurations of a particular switch interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. |
#### Examples
```
ops-as5712# show running-config interface 2
Interface 2
   no shutdown
   speed 40000
   autonegotiation on
   exit
```

```
ops-as5712# do show running-config interface lag100
interface lag 100
   no routing
   lacp mode active
```

### Show transceiver DOM information for all interfaces
#### Syntax
`show interface dom`
#### Description
This command displays diagnostics information, and alarm and warning flags of optical transceivers (SFP, SFP+, QSFP+), on all interfaces. This information is known as DOM (Digital Optical Monitoring).

DOM information also consists of vendor determined thresholds which trigger high/low alarm and warning flags.
#### Authority
All users.
#### Examples
```
switch# sh int 1 dom
Interface 1:
 Connector: SFP+
 Transceiver module: SFP_SR
  Temperature: 18.00C
  Temperature high alarm: Off
  Temperature low alarm: Off
  Temperature high warning: Off
  Temperature low warning: Off
  Temperature high alarm threshold: 73.00C
  Temperature low alarm threshold: -3.00C
  Temperature high warning threshold: 70.00C
  Temperature low warning threshold: 0.00C
  Voltage: 3.41V
  Voltage high alarm: Off
  Voltage high alarm: Off
  Voltage high alarm: Off
  Voltage low warning: Off
  Voltage high alarm threshold: 3.80V
  Voltage low alarm threshold: 2.81V
  Voltage high warning threshold: 3.46V
  Voltage low warning threshold: 3.13V
  Bias current: 0.16mA
  Bias current high alarm: Off
  Bias current low alarm: On
  Bias current high warning: Off
  Bias current low warning: On
  Bias current high alarm threshold: 13.20mA
  Bias current low alarm threshold: 1.00mA
  Bias current high warning threshold: 12.60mA
  Bias current low warning threshold: 1.00mA
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: On
  Rx power high warning: Off
  Rx power low warning: On
  Rx power high alarm threshold: 1.26mW
  Rx power low alarm threshold: 0.11mW
  Rx power high warning threshold: 0.79mW
  Rx power low warning threshold: 0.18mW
  Tx power: 0.01mW
  Tx power high alarm: Off
  Tx power low alarm: On
  Tx power high warning: Off
  Tx power low warning: On
  Tx power high alarm threshold: 1.00mW
  Tx power low alarm threshold: 0.09mW
  Tx power high warning threshold: 0.79mW
  Tx power low warning threshold: 0.19mW


Interface 3:
 Connector: SFP+
 Transceiver module: SFP_DAC
 % No DOM information available

Interface 4:
 Connector: SFP+
 Transceiver module: SFP_DAC
 % No DOM information available

Interface 5:
 Connector: SFP+
 Transceiver module: not present

Interface 6:
 Connector: SFP+
 Transceiver module: not present

switch# sh int 49 dom
Interface 49:
 Connector: QSFP (splittable)
 Transceiver module: QSFP_SR4
  Temperature: 24.00C
  Voltage: 3.37V

 Lane 1:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off

 Lane 2:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off

 Lane 3:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off

 Lane 4:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off


Interface 50:
 Connector: QSFP (splittable)
 Transceiver module: QSFP_CR4
 % No DOM information available

Interface 50-1:
 Connector: QSFP

Interface 50-2:
 Connector: QSFP

Interface 50-3:
 Connector: QSFP

Interface 50-4:
 Connector: QSFP

Interface 51:
 Connector: QSFP (splittable)
 Transceiver module: not present

```

### Show transceiver DOM information for an interface
#### Syntax
`show interface <interface> dom`
#### Description
This command displays diagnostics information, and alarm and warning flags of optical transceivers (SFP, SFP+, QSFP+), on a particular interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface* | Required | System defined | Name of the interface. |
|
#### Examples
```
switch# sh int 1 dom
Interface 1:
 Connector: SFP+
 Transceiver module: SFP_SR
  Temperature: 18.00C
  Temperature high alarm: Off
  Temperature low alarm: Off
  Temperature high warning: Off
  Temperature low warning: Off
  Temperature high alarm threshold: 73.00C
  Temperature low alarm threshold: -3.00C
  Temperature high warning threshold: 70.00C
  Temperature low warning threshold: 0.00C
  Voltage: 3.41V
  Voltage high alarm: Off
  Voltage high alarm: Off
  Voltage high alarm: Off
  Voltage low warning: Off
  Voltage high alarm threshold: 3.80V
  Voltage low alarm threshold: 2.81V
  Voltage high warning threshold: 3.46V
  Voltage low warning threshold: 3.13V
  Bias current: 0.16mA
  Bias current high alarm: Off
  Bias current low alarm: On
  Bias current high warning: Off
  Bias current low warning: On
  Bias current high alarm threshold: 13.20mA
  Bias current low alarm threshold: 1.00mA
  Bias current high warning threshold: 12.60mA
  Bias current low warning threshold: 1.00mA
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: On
  Rx power high warning: Off
  Rx power low warning: On
  Rx power high alarm threshold: 1.26mW
  Rx power low alarm threshold: 0.11mW
  Rx power high warning threshold: 0.79mW
  Rx power low warning threshold: 0.18mW
  Tx power: 0.01mW
  Tx power high alarm: Off
  Tx power low alarm: On
  Tx power high warning: Off
  Tx power low warning: On
  Tx power high alarm threshold: 1.00mW
  Tx power low alarm threshold: 0.09mW
  Tx power high warning threshold: 0.79mW
  Tx power low warning threshold: 0.19mW


switch# sh int 50 dom
Interface 50:
 Connector: QSFP (splittable)
 Transceiver module: QSFP_SR4
  Temperature: 24.00C
  Voltage: 3.37V

 Lane 1:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off

 Lane 2:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off

 Lane 3:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off

 Lane 4:
  Bias current: 0.00mA
  Bias current high alarm: Off
  Bias current low alarm: Off
  Bias current high warning: Off
  Bias current low warning: Off
  Rx power: 0.00mW
  Rx power high alarm: Off
  Rx power low alarm: Off
  Rx power high warning: Off
  Rx power low warning: Off

```
