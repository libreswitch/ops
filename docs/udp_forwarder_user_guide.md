# UDP Broadcast Forwarder

## Contents
   - [Overview](#overview)
   - [Configure the UDP broadcast forwarder](#configure-the-udp-broadcast-forwarder)
   - [How to use the UDP broadcast forwarder](#how-to-use-the-udp-broadcast-forwarder)

## Overview
The routers by default do not forward broadcast packets. This is to avoid packet flooding on the network. However, there are situations where it is desirable to forward certain broadcast packets.
The UDP (User Datagram Protocol) broadcast forwarder takes up the client's UDP broadcast packet and forwards it to the configured server(s) in a different subnet. By default, a router's UDP broadcast forwarding is disabled. A client's UDP broadcast requests cannot reach a target server on a different subnet unless explicitly configured on the router to forward client UDP broadcasts to that server.
UDP forward-protocol addresses can be configured on an interface regardless of whether UDP broadcast forwarding is globally enabled on the device. However, the feature does not operate unless globally enabled.
A UDP forwarding entry includes the application UDP port number, and either an IP unicast address or an IP subnet broadcast address on which the server operates. Thus, an incoming UDP packet carrying the configured port number will be:
1. Forwarded to a specific host if a unicast server address is configured for that port number.
2. Broadcast on the appropriate destination subnet if a subnet address is configured for that port number.

UDP broadcast forwarder allows multiple unicast server IPs to be configured for a single UDP port.
UDP broadcast forwarding is supported only for IPv4 addresses. UDP forward-protocol configuration is allowed on the interface with routing disabled, but UDP broadcast forwarding will not take effect on that interface until routing is enabled.

## Configure the UDP broadcast forwarder
Syntax:
`[no] ip udp-bcast-forward`
*Enable/disable UDP broadcast forwarding. By default, it is disabled.*

`[no] ip forward-protocol udp <IPv4-address> <port-number | protocol-name>`
*Configure UDP broadcast server(s) on the interface for a particular udp port.*
UDP forward-protocol configuration is supported on data-plane interfaces.

Explanation of parameters
• IPv4-address - The IPv4 address of the protocol server. This can be either be a unicast address of a destination server on another subnet or a broadcast address of the subnet on which a destination server operates.
• port-number - Any UDP port number corresponding to a UDP application supported on a device.
• protocol-name - Allows the use of common names for certain well-known UDP port numbers.
Supported UDP protocols:
• dns: Domain Name Service (53)
• ntp: Network Time Protocol (123)
• netbios-ns: NetBIOS Name Service (137)
• netbios-dgm: NetBIOS Datagram Service (138)
• radius: Remote Authentication Dial-In User Service (1812)
• radius-old: Remote Authentication Dial-In User Service (1645)
• rip: Routing Information Protocol (520)
• snmp: Simple Network Management Protocol (161)
• snmp-trap: Simple Network Management Protocol (162)
• tftp: Trivial File Transfer Protocol (69)
• timep: Time Protocol (37)

`show ip forward-protocol [interface <WORD>]`
*Display the server addresses where broadcast requests received by the device are to be forwarded based on configured port.*

Explanation of parameters
•   interface <WORD> - The interface on which server addresses are configured.

## How to use the UDP broadcast forwarder

### Example

```
switch(config)#ip udp-bcast-forward

switch#show ip forward-protocol

UDP Broadcast Forwarder : enabled

switch#show running-config
Current configuration:
!
!
!
ip udp-bcast-forward

switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 53

switch#show ip forward-protocol

UDP Broadcast Forwarder : enabled

Interface: 1
  IP Forward Address    UDP Port
  -----------------------------
  1.1.1.1                53

switch#show ip forward-protocol interface 1

UDP Broadcast Forwarder : enabled

Interface: 1
  IP Forward Address    UDP Port
  -------------------------------
  1.1.1.1                53

switch#show running-config
Current configuration:
!
!
!
interface 1
    ip forward-protocol udp 1.1.1.1 53
ip udp-bcast-forward

switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 8.1.1.1 161
switch(config-if)#ip forward-protocol udp 4.4.4.4 137
switch(config)#interface 2
switch(config-if)#ip forward-protocol udp 3.3.3.3 137

switch#show ip forward-protocol

UDP Broadcast Forwarder : enabled

Interface: 1
  IP Forward Address    UDP Port
  -----------------------------
  4.4.4.4                137
  1.1.1.1                53
  8.1.1.1                161
Interface: 2
  IP Forward Address    UDP Port
  -----------------------------
  3.3.3.3                137

switch#show ip forward-protocol interface 1

UDP Broadcast Forwarder : enabled

Interface: 1
  IP Forward Address    UDP Port
  -------------------------------
  4.4.4.4                137
  8.1.1.1                161
  1.1.1.1                53

switch#show running-config
Current configuration:
!
!
!
!
interface 1
    ip forward-protocol udp 1.1.1.1 53
    ip forward-protocol udp 8.1.1.1 161
    ip forward-protocol udp 4.4.4.4 137
interface 2
    ip forward-protocol udp 3.3.3.3 137
ip udp-bcast-forward

switch(config)#no ip udp-bcast-forward
switch#show ip forward-protocol

UDP Broadcast Forwarder : disabled

Interface: 1
  IP Forward Address    UDP Port
  -----------------------------
  4.4.4.4                137
  1.1.1.1                53
  8.1.1.1                161
Interface: 2
  IP Forward Address    UDP Port
  -----------------------------
  3.3.3.3                137

switch#show ip forward-protocol interface 1

UDP Broadcast Forwarder : disabled

Interface: 1
  IP Forward Address    UDP Port
  -------------------------------
  4.4.4.4                137
  1.1.1.1                53
  8.1.1.1                161

switch#show running-config
Current configuration:
!
!
!
interface 1
    ip forward-protocol udp 1.1.1.1 53
    ip forward-protocol udp 8.1.1.1 161
    ip forward-protocol udp 4.4.4.4 137
interface 2
    ip forward-protocol udp 3.3.3.3 137

switch(config)#interface 1
switch(config-if)#no ip forward-protocol udp 1.1.1.1 53
switch#show ip forward-protocol

UDP Broadcast Forwarder : disabled

Interface: 1
  IP Forward Address    UDP Port
  -----------------------------
  4.4.4.4                137
  8.1.1.1                161
Interface: 2
  IP Forward Address    UDP Port
  -----------------------------
  3.3.3.3                161

switch#show ip forward-protocol interface 1

UDP Broadcast Forwarder : disabled

Interface: 1
  IP Forward Address    UDP Port
  -------------------------------
  4.4.4.4                137
  8.1.1.1                161

switch#show running-config
Current configuration:
!
!
!
interface 1
    ip forward-protocol udp 8.1.1.1 161
    ip forward-protocol udp 4.4.4.4 137
interface 2
    ip forward-protocol udp 3.3.3.3 137
```
