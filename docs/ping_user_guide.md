# Ping

## Contents
- [Overview](#overview)
    - [Syntax](#syntax)
    - [Explanation of parameters](#explanation-of-parameters)
- [How to use the feature](#how-to-use-the-feature)
    - [Ping examples for IPv4 addresses](#ping-examples-for-ipv4-addresses)
    - [Ping6 examples for IPv6 addresses](#ping6-examples-for-ipv6-addresses)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The ping (Packet InterNet Groper) command is a very common method for troubleshooting the accessibility of devices.
It uses Internet Control Message Protocol (ICMP) echo requests and ICMP echo replies to determine if another device is alive.
It also measures the amount of time it takes to receive a reply from the specified destination.
The ping command is mostly used to verify connectivity between your switch and a host or port. The reply packet tells you if the host received the ping and the amount of time it took to return the packet.

### Syntax
`ping <ipv4-address | hostname> [repetitions <1-10000>] [timeout <1-60>] [interval <1-60>] [datagram-size <100-65399>] [data-fill <WORD>][ip-option (include-timestamp |include-timestamp-and-address |record-route)][tos <0-255>]`

`ping6 <ipv6-address | hostname> [repetitions <1-10000>] [interval <1-60>] [datagram-size <100-65468>] [data-fill <WORD>]`

### Explanation of parameters

* Ipv4-address - Target IPv4 address of the destination node being pinged.

* Hostname - Hostname of the destination node being pinged.

* Repetitions <1-10000> - Number of ping packets sent to the destination address. The default value is 5.

* Timeout <1-60> - Timeout interval in seconds, the ECHO REPLY must be received before this time interval expires for the Ping to be successful. The default value is 2 seconds.

* Interval <1-60> - Interval seconds between sending each packet. The default value is 1 second.

* Datagram-size - Size of packet sent to the destination. The default value is 100 bytes.

* Data-fill -  Hexadecimal pattern to be filled in the packet. A Maximum of 16 'pad' bytes can be specified to fill out the icmp packet.

* Ip-options - This prompt offers more selection of any one option from the list below.

 *   Include-timestamp - Timestamp option is used to measure roundtrip time to particular hosts.
 *   Include-timestamp-and-address - Displays roundtrip time to particular hosts as well as address.
 *   Record-route - Displays the addresses of the hops the packet goes through.

*   TOS <0-255> - Specifies the Type of Service (TOS). The requested TOS is placed in each probe. It is the Internet service quality selection.

Note: Ping 0.0.0.0 and ping6 0::0 issues ping and ping6 to localhost. This is default Linux behavior.

## How to use the feature

### Ping examples for IPv4 addresses
#### Ping IPv4-address
##### Success case
Send an IP ping request to the device that has IP address 9.0.0.1.
```
    switch# ping 9.0.0.1
    PING 9.0.0.1 (9.0.0.1) 100(128) bytes of data.
    108 bytes from 9.0.0.1: icmp_seq=1 ttl=64 time=0.035 ms
    108 bytes from 9.0.0.1: icmp_seq=2 ttl=64 time=0.034 ms
    108 bytes from 9.0.0.1: icmp_seq=3 ttl=64 time=0.034 ms
    108 bytes from 9.0.0.1: icmp_seq=4 ttl=64 time=0.034 ms
    108 bytes from 9.0.0.1: icmp_seq=5 ttl=64 time=0.033 ms

    --- 9.0.0.1 ping statistics ---
    5 packets transmitted, 5 received, 0% packet loss, time 3999ms
    rtt min/avg/max/mdev = 0.033/0.034/0.035/0.000 ms
```

Send an IP ping request to IP address 0.0.0.0.
```
    switch# ping 0.0.0.0
    PING 0.0.0.0 (127.0.0.1) 100(128) bytes of data.
    108 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.061 ms
    108 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.065 ms
    108 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.061 ms
    108 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.041 ms
    108 bytes from 127.0.0.1: icmp_seq=5 ttl=64 time=0.036 ms

    --- 0.0.0.0 ping statistics ---
    5 packets transmitted, 5 received, 0% packet loss, time 4002ms
    rtt min/avg/max/mdev = 0.036/0.052/0.065/0.015 ms
```

##### Failure case

Network unreachable
```
    switch# ping 1.1.1.1
    connect: Network is unreachable

```

Destination host unreachable
```
    switch# ping 9.0.0.1
    PING 9.0.0.1 (9.0.0.1) 100(128) bytes of data.
    From 9.0.0.2 icmp_seq=1 Destination Host Unreachable
    From 9.0.0.2 icmp_seq=2 Destination Host Unreachable
    From 9.0.0.2 icmp_seq=3 Destination Host Unreachable
    From 9.0.0.2 icmp_seq=4 Destination Host Unreachable

    --- 9.0.0.1 ping statistics ---
    5 packets transmitted, 0 received, +4 errors, 100% packet loss, time 4002ms
    pipe 4
```

#### Hostname
`ping hostname`
 Domain name of the host to ping.

#### Repetitions
`ping <ipv4-address | hostname> repetitions <1-10000>`
Number of packets to send <1-10000>.
Range: < 1 to 10000 >

#### Timeout
`ping <ipv4-address | hostname> timeout <1-60>`
Ping timeout in seconds <1-60>.
Range: <1 to 60>

#### Interval
`ping <ipv4-address | hostname> interval <1-60>`
Seconds between sending each packet <1-60>.
Range: <1 to 60>

#### Data-fill
`ping <ipv4-address | hostname> data-fill WORD`
Ping data fill string, example 'ab'
A Maximum of 16 'pad' bytes can be specified to fill out in the icmp packet.

#### Datagram-size
`ping <ipv4-address | hostname> datagram-size <100-65399>`
 Range: <100 to 65399>

### Ping6 examples for IPv6 addresses
#### Ping IPv6-address
##### Success case
Send an IPv6 Ping request to the device that has IPv6 address 2020::2
```
    switch# ping6 2020::2
    PING 2020::2(2020::2) 100 data bytes
    108 bytes from 2020::2: icmp_seq=1 ttl=64 time=0.386 ms
    108 bytes from 2020::2: icmp_seq=2 ttl=64 time=0.235 ms
    108 bytes from 2020::2: icmp_seq=3 ttl=64 time=0.249 ms
    108 bytes from 2020::2: icmp_seq=4 ttl=64 time=0.240 ms
    108 bytes from 2020::2: icmp_seq=5 ttl=64 time=0.252 ms

    --- 2020::2 ping statistics ---
    5 packets transmitted, 5 received, 0% packet loss, time 4000ms
    rtt min/avg/max/mdev = 0.235/0.272/0.386/0.059 ms
    ```

Send an IPv6 Ping request to IPv6 address 0::0
```
    switch# ping6 0::0
    PING 0::0(::) 100 data bytes
    108 bytes from ::1: icmp_seq=1 ttl=64 time=0.036 ms
    108 bytes from ::1: icmp_seq=2 ttl=64 time=0.064 ms
    108 bytes from ::1: icmp_seq=3 ttl=64 time=0.065 ms
    108 bytes from ::1: icmp_seq=4 ttl=64 time=0.060 ms
    108 bytes from ::1: icmp_seq=5 ttl=64 time=0.061 ms

    --- 0::0 ping statistics ---
    5 packets transmitted, 5 received, 0% packet loss, time 4000ms
    rtt min/avg/max/mdev = 0.036/0.057/0.065/0.011 ms
```

##### Failure case

Network unreachable
```
    switch# ping6 3030::1
    connect: Network is unreachable

```

Destination host unreachable
```
    switch# ping6 2020::1
    PING 2020::1(2020::1) 100 data bytes
    From 2020::2 icmp_seq=1 Destination unreachable: Address unreachable
    From 2020::2 icmp_seq=2 Destination unreachable: Address unreachable
    From 2020::2 icmp_seq=3 Destination unreachable: Address unreachable
    From 2020::2 icmp_seq=4 Destination unreachable: Address unreachable
    From 2020::2 icmp_seq=5 Destination unreachable: Address unreachable

    --- 2020::1 ping statistics ---
    5 packets transmitted, 0 received, +5 errors, 100% packet loss, time 4000ms
```

#### Hostname
`ping6 hostname`
Domain name of the host to ping.

#### Repetitions
`ping6 <ipv6-address | hostname> repetitions <1-10000>`
Number of packets to send <1-10000>.
Range: <1 to 10000>

#### Interval
`ping6 <ipv6-address | hostname> interval <1-60>`
Seconds between sending each packet <1-60>.
Range: <1 to 60>

#### Data-fill
`ping6 <ipv6-address | hostname> data-fill WORD`
Ping data fill string, example 'ab'
A Maximum of 16 'pad' bytes can be specified to fill out in the icmp packet.

#### Datagram-size
`ping6 <ipv6-address | hostname> datagram-size <100-65468>`
    Range: <100 to 65468>

## CLI
Click [here](http://www.openswitch.net/documents/user/ping_cli) for more information about the CLI commands related to the ping feature.

## Related features
* [Traceroute User Guide](http://www.openswitch.net/documents/user/traceroute_user_guide)
* [Traceroute CLI Guide](http://www.openswitch.net/documents/user/traceroute_cli)
