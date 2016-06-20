# Traceroute

## Contents
   - [Overview](#overview)
   - [How to use the feature](#how-to-use-the-feature)
   - [Related features](#related-features)

## Overview

Traceroute is a computer network diagnostic tool for displaying the route (path), and measuring transit delays of packets
across an Internet Protocol (IP) network.
It sends a sequence of User Datagram Protocol (UDP) packets addressed to a destination host.
The time-to-live (TTL) value, also known as hop limit, is used in determining the intermediate routers being traversed towards the destination.


### Syntax
`traceroute <IP-ADDR | hostname > [dstport <1-34000> ] [maxttl <1-255>] [minttl <1-255>] [probes <1-5>] [timeout <1-60>] [ip-option loosesourceroute <IP-ADDR>]`

`traceroute6 <IP-ADDR | hostname > [dstport <1-34000> ] [maxttl <1-255>] [probes <1-5>] [timeout <1-60>]`

#### Explanation of parameters

*   IP-ADDR - Network IP address of the device to which to send traceroute.

*   Hostname - Domain name of the device to which to send traceroute.

*   Dstport <1-34000> -Destination port For UDP tracing. The default value is 33434.

*   Maxttl <1-255> - Maximum number of hops used in outgoing probe packets. The default value is 30.

*   Minttl <1-255> - Minimum number of hops used in outgoing probe packets. The default value is 1.

*   Probes <1-5> - Number of probe queries to send out for each hop. The default value is 3.

*   Timeout <1-60> - Time (in seconds) to wait for a response to a probe. The default value is 3 seconds.

*   Ip-option - Tells traceroute to add an IP source routing option to the outgoing packet.

*   Loosesourceroute <IP-ADDR> - Tells the network to route the packet through the specified gateway.

## How to use the feature

### Traceroute examples

#### Traceroute IP-address
    Send IP traceroute UDP packets to the device that has IP address 10.168.1.146:
```
    switch# traceroute 10.168.1.146
    traceroute to 10.168.1.146 (10.168.1.146) , 1 hops min, 30 hops max, 3 sec. timeout, 3 probes
      1 10.57.191.129 2 ms 3 ms 3 ms
      2 10.57.232.1 4 ms 2 ms 3 ms
      3 10.168.1.146 4 ms 3 ms 3 ms
```
Send IP traceroute UDP packets to the device that has IP address 0.0.0.0:
```
    switch# traceroute 0.0.0.0
    traceroute to 0.0.0.0 (0.0.0.0), 1 hops min, 30 hops max, 3 sec. timeout, 3 probes
      1   127.0.0.1  0.015ms  0.003ms  0.002ms
```
##### Failure case

Network unreachable
```
   switch# traceroute 10.0.0.1
   traceroute to 10.0.0.1 (10.0.0.1), 1 hops min, 30 hops max, 3 sec. timeout, 3 probes
     1  traceroute: sendto: Network is unreachable
```
Destination host unreachable
```
   switch# traceroute 9.0.0.6
   traceroute to 9.0.0.6 (9.0.0.6), 1 hops min, 30 hops max, 3 sec. timeout, 3 probes
     1 9.0.0.2  2 ms !H  3 ms !H  2 ms !H

```

#### Hostname
    traceroute hostname
    Domain name of the host to traceroute.

#### Destination port
    traceroute  <IP | Hostname> dstport <1-34000>.
    Destination port number.
    Range: <1 to 34000>

#### Maximum TTL
    traceroute  <IP | Hostname> maxttl <1-255>
    Maximum number of hops used in outgoing probe packets.
    Range: <1 to 255>

#### Minimum TTL
    traceroute <IP | Hostname> minttl <1-255>
    Minimum number of hops used in outgoing probe packets.
    Range: <1 to 255>

#### Probes
    traceroute  <IP | Hostname> probes <1-5>
    Number of probe queries to send out for each hop <1-5>.
    Range: < 1 to 5 >

#### Timeout
    traceroute  <IP | Hostname> timeout <1-60>
    Time (in seconds) to wait for a response to a probe <1-60>.
    Range: < 1 to 60 >

#### Ip-option loose source route
    traceroute <IP | Hostname> ip-option loosesourceroute <IP-ADDR>
    Loose source route defines the default gateway to the destination.

### Traceroute6 examples

#### Traceroute6 IPv6-address
    Send IPv6 traceroute UDP packets to the device that has IPv6 address 0:0::0:1 :
```
    switch# traceroute6 0:0::0:1
    traceroute to 0:0::0:1 (::1) from ::1, 30 hops max, 3 sec. timeout, 3 probes, 24 byte packets
     1  localhost (::1)  0.117 ms  0.032 ms  0.021 ms
```
    Send IP traceroute UDP packets to the device that has IP address ::0:
```
    switch# traceroute6 ::0
    traceroute to ::0 (::) from ::1, 30 hops max, 3 sec. timeout, 3 probes, 24 byte packets
     1  localhost (::1)  0.144 ms  0.03 ms  0.016 ms
```
 ##### Failure case

Network unreachable
```
   switch# traceroute6 2004::2
   connect: Network is unreachable
```
Destination host unreachable
```
   switch# traceroute6 2001::2
   traceroute to 2001::2 (2001::2) from 2001::1, 30 hops max, 3 sec. timeout, 3 probes, 24 byte packets
    1  switch (2001::1)  2998.93 ms !H  2999.14 ms !H  2999.79 ms !H


```

#### Hostname
    traceroute6 hostname
    Domain name of the host to traceroute6.

#### Destination port
    traceroute6 <IPv6 | Hostname> dstport <1-34000>
    Destination port number.
    Range: <1 to 34000>

#### Maximum TTL
    traceroute6 <IPv6 | Hostname> maxttl <1-255>
    Maximum number of hops used in outgoing probe packets.
    Range: <1 to 255>

#### Probes
    traceroute6 <IPv6 | Hostname> probes <1-5>
    Number of probe queries to send out for each hop <1-5>.
    Range: < 1 to 5 >

#### Timeout
    traceroute6 <IPv6 | Hostname> timeout <1-60>
    Time (in seconds) to wait for a response to a probe <1-60>.
    Range: < 1 to 60 >


## Related features
None.
