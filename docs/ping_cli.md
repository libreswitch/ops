Ping Utility
======
## Contents

- [Ping options](#ping-options)
- [Ping6 options](#ping6-options)

## Ping options
### IPv4 address
#### Syntax
`ping <IPv4-address>`
#### Description
This command is used to ping a specific IPv4 address.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *IPv4-address* | Required | A.B.C.D | IPv4 address to ping.|
#### Examples
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

### Hostname
#### Syntax
`ping <hostname>`
#### Description
This command is used to ping a specific Hostname.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *hostname* | Required | String | Hostname to ping. Length must be less than 256 characters.|
#### Examples
```
switch# ping localhost
PING localhost (127.0.0.1) 100(128) bytes of data.
108 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.060 ms
108 bytes from localhost (127.0.0.1): icmp_seq=2 ttl=64 time=0.035 ms
108 bytes from localhost (127.0.0.1): icmp_seq=3 ttl=64 time=0.043 ms
108 bytes from localhost (127.0.0.1): icmp_seq=4 ttl=64 time=0.041 ms
108 bytes from localhost (127.0.0.1): icmp_seq=5 ttl=64 time=0.034 ms

--- localhost ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3998ms
rtt min/avg/max/mdev = 0.034/0.042/0.060/0.011 ms
```

### Set data-fill pattern
#### Syntax
`ping ( <IPv4-address> | <hostname> ) data-fill <pattern>`
#### Description
This command sets the hexadecimal pattern to be filled in the packet.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *pattern* | Optional | String | Set the hexadecimal pattern to be filled in the packet. A Maximum of 16 'pad' bytes can be specified to fill out the icmp packet.|
#### Examples
```
switch# ping 10.0.0.2 data-fill 1234123412341234acde123456789012
PATTERN: 0x1234123412341234acde123456789012
PING 10.0.0.2 (10.0.0.2) 100(128) bytes of data.
108 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=0.207 ms
108 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.187 ms
108 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.225 ms
108 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.197 ms
108 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=0.210 ms

--- 10.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3999ms
rtt min/avg/max/mdev = 0.187/0.205/0.225/0.015 ms
```

### Set datagram-size
#### Syntax
`ping ( <IPv4-address> | <hostname> ) datagram-size <size>`
#### Description
This command sets the size of the packet to be sent. The default value is 100 bytes.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *size* | Optional | <100-65399> | Select the datagram-size between 100 and 65399.|
#### Examples
```
switch# ping 9.0.0.2 datagram-size 200
PING 9.0.0.2 (9.0.0.2) 200(228) bytes of data.
208 bytes from 9.0.0.2: icmp_seq=1 ttl=64 time=0.202 ms
208 bytes from 9.0.0.2: icmp_seq=2 ttl=64 time=0.194 ms
208 bytes from 9.0.0.2: icmp_seq=3 ttl=64 time=0.201 ms
208 bytes from 9.0.0.2: icmp_seq=4 ttl=64 time=0.200 ms
208 bytes from 9.0.0.2: icmp_seq=5 ttl=64 time=0.186 ms

--- 9.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4000ms
rtt min/avg/max/mdev = 0.186/0.196/0.202/0.016 ms
```

### Set interval
#### Syntax
`ping ( <IPv4-address> | <hostname> ) interval <time>`
#### Description
This command sets the interval seconds between sending each packet. The default value is 1 second.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *time* | Optional | <1-60> | Select an interval in seconds between 1 and 60.|
#### Examples
```
switch# ping 9.0.0.2 interval 2
PING 9.0.0.2 (9.0.0.2) 100(128) bytes of data.
108 bytes from 9.0.0.2: icmp_seq=1 ttl=64 time=0.199 ms
108 bytes from 9.0.0.2: icmp_seq=2 ttl=64 time=0.192 ms
108 bytes from 9.0.0.2: icmp_seq=3 ttl=64 time=0.208 ms
108 bytes from 9.0.0.2: icmp_seq=4 ttl=64 time=0.182 ms
108 bytes from 9.0.0.2: icmp_seq=5 ttl=64 time=0.194 ms

--- 9.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 7999ms
rtt min/avg/max/mdev = 0.182/0.195/0.208/0.008 ms
```

### Set repetitions
#### Syntax
`ping ( <IPv4-address> | <hostname> ) repetitions <number>`
#### Description
This command sets the number of packets to be sent to the destination address. The default value is 5.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *number* | Optional | <1-10000> | Select the number of packets to send between 1 and 10000.|
#### Examples
```
switch# ping 9.0.0.2 repetitions 10
PING 9.0.0.2 (9.0.0.2) 100(128) bytes of data.
108 bytes from 9.0.0.2: icmp_seq=1 ttl=64 time=0.213 ms
108 bytes from 9.0.0.2: icmp_seq=2 ttl=64 time=0.204 ms
108 bytes from 9.0.0.2: icmp_seq=3 ttl=64 time=0.201 ms
108 bytes from 9.0.0.2: icmp_seq=4 ttl=64 time=0.184 ms
108 bytes from 9.0.0.2: icmp_seq=5 ttl=64 time=0.202 ms
108 bytes from 9.0.0.2: icmp_seq=6 ttl=64 time=0.184 ms
108 bytes from 9.0.0.2: icmp_seq=7 ttl=64 time=0.193 ms
108 bytes from 9.0.0.2: icmp_seq=8 ttl=64 time=0.196 ms
108 bytes from 9.0.0.2: icmp_seq=9 ttl=64 time=0.193 ms
108 bytes from 9.0.0.2: icmp_seq=10 ttl=64 time=0.200 ms

--- 9.0.0.2 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 8999ms
rtt min/avg/max/mdev = 0.184/0.197/0.213/0.008 ms
```

### Set timeout
#### Syntax
`ping ( <IPv4-address> | <hostname> ) timeout <time>`
#### Description
This command sets the time to wait for a response in seconds from the receiver. The default value is 2 seconds.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *time* | Optional | <1-60> | Select timeout in seconds between 1 and 60.|
#### Examples
```
switch# ping 9.0.0.2 timeout 3
PING 9.0.0.2 (9.0.0.2) 100(128) bytes of data.
108 bytes from 9.0.0.2: icmp_seq=1 ttl=64 time=0.175 ms
108 bytes from 9.0.0.2: icmp_seq=2 ttl=64 time=0.192 ms
108 bytes from 9.0.0.2: icmp_seq=3 ttl=64 time=0.190 ms
108 bytes from 9.0.0.2: icmp_seq=4 ttl=64 time=0.181 ms
108 bytes from 9.0.0.2: icmp_seq=5 ttl=64 time=0.197 ms

--- 9.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4000ms
rtt min/avg/max/mdev = 0.175/0.187/0.197/0.007 ms
```

### Set TOS
#### Syntax
`ping ( <IPv4-address> | <hostname> ) tos <number>`
#### Description
This command sets Type of Service (TOS) related bits in ICMP datagrams.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *number* | Optional | <0-255> | Select the TOS value between 0 and 255.|
#### Examples
```
switch# ping 9.0.0.2 tos 2
PING 9.0.0.2 (9.0.0.2) 100(128) bytes of data.
108 bytes from 9.0.0.2: icmp_seq=1 ttl=64 time=0.033 ms
108 bytes from 9.0.0.2: icmp_seq=2 ttl=64 time=0.034 ms
108 bytes from 9.0.0.2: icmp_seq=3 ttl=64 time=0.031 ms
108 bytes from 9.0.0.2: icmp_seq=4 ttl=64 time=0.034 ms
108 bytes from 9.0.0.2: icmp_seq=5 ttl=64 time=0.031 ms

--- 9.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3999ms
rtt min/avg/max/mdev = 0.031/0.032/0.034/0.006 ms
```

### Set ip-option
#### Syntax
`ping ( <IPv4-address> | <hostname> ) ip-option (include-timestamp |include-timestamp-and-address |record-route ) `
#### Description
This command is used to record either the intermediate router timestamp, the intermediate router timestamp and IP address, or the intermediate router addresses.
#### Authority
Root user.
#### Parameters
No parameters.
#### Examples
```
switch# ping 9.0.0.2 ip-option include-timestamp
PING 9.0.0.2 (9.0.0.2) 100(168) bytes of data.
108 bytes from 9.0.0.2: icmp_seq=1 ttl=64 time=0.031 ms
TS:     59909005 absolute
        0
        0
        0

108 bytes from 9.0.0.2: icmp_seq=2 ttl=64 time=0.034 ms
TS:     59910005 absolute
        0
        0
        0

108 bytes from 9.0.0.2: icmp_seq=3 ttl=64 time=0.038 ms
TS:     59911005 absolute
        0
        0
        0

108 bytes from 9.0.0.2: icmp_seq=4 ttl=64 time=0.035 ms
TS:     59912005 absolute
        0
        0
        0

108 bytes from 9.0.0.2: icmp_seq=5 ttl=64 time=0.037 ms
TS:     59913005 absolute
        0
        0
        0


--- 9.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3999ms
rtt min/avg/max/mdev = 0.031/0.035/0.038/0.002 ms

switch# ping 9.0.0.2 ip-option include-timestamp-and-address
PING 9.0.0.2 (9.0.0.2) 100(168) bytes of data.
108 bytes from 9.0.0.2: icmp_seq=1 ttl=64 time=0.030 ms
TS:     9.0.0.2 60007355 absolute
        9.0.0.2 0
        9.0.0.2 0
        9.0.0.2 0

108 bytes from 9.0.0.2: icmp_seq=2 ttl=64 time=0.037 ms
TS:     9.0.0.2 60008355 absolute
        9.0.0.2 0
        9.0.0.2 0
        9.0.0.2 0

108 bytes from 9.0.0.2: icmp_seq=3 ttl=64 time=0.037 ms
TS:     9.0.0.2 60009355 absolute
        9.0.0.2 0
        9.0.0.2 0
        9.0.0.2 0

108 bytes from 9.0.0.2: icmp_seq=4 ttl=64 time=0.038 ms
TS:     9.0.0.2 60010355 absolute
        9.0.0.2 0
        9.0.0.2 0
        9.0.0.2 0

108 bytes from 9.0.0.2: icmp_seq=5 ttl=64 time=0.039 ms
TS:     9.0.0.2 60011355 absolute
        9.0.0.2 0
        9.0.0.2 0
        9.0.0.2 0


--- 9.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3999ms
rtt min/avg/max/mdev = 0.030/0.036/0.039/0.005 ms

switch# ping 9.0.0.2 ip-option record-route
PING 9.0.0.2 (9.0.0.2) 100(168) bytes of data.
108 bytes from 9.0.0.2: icmp_seq=1 ttl=64 time=0.034 ms
RR:     9.0.0.2
        9.0.0.2
        9.0.0.2
        9.0.0.2

108 bytes from 9.0.0.2: icmp_seq=2 ttl=64 time=0.038 ms (same route)
108 bytes from 9.0.0.2: icmp_seq=3 ttl=64 time=0.036 ms (same route)
108 bytes from 9.0.0.2: icmp_seq=4 ttl=64 time=0.037 ms (same route)
108 bytes from 9.0.0.2: icmp_seq=5 ttl=64 time=0.035 ms (same route)

--- 9.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3999ms
rtt min/avg/max/mdev = 0.034/0.036/0.038/0.001 ms

```

## Ping6 options

### IPv6 address
#### Syntax
`ping6 <IPv6-address>`
#### Description
This command is used to ping the specified IPv6 address.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *IPv6-address* | Required | X:X::X:X | IPv6 address to ping.|
#### Examples
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

### Hostname
#### Syntax
`ping6 <hostname>`
#### Description
This command is used to ping the specified Hostname.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *hostname* | Required | String | Hostname to ping. Length must be less than 256 characters.|
#### Examples
```
switch# ping6 localhost
PING localhost(localhost) 100 data bytes
108 bytes from localhost: icmp_seq=1 ttl=64 time=0.093 ms
108 bytes from localhost: icmp_seq=2 ttl=64 time=0.051 ms
108 bytes from localhost: icmp_seq=3 ttl=64 time=0.055 ms
108 bytes from localhost: icmp_seq=4 ttl=64 time=0.046 ms
108 bytes from localhost: icmp_seq=5 ttl=64 time=0.048 ms

--- localhost ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3998ms
rtt min/avg/max/mdev = 0.046/0.058/0.093/0.019 ms

```

### Set data-fill pattern
#### Syntax
`ping6 ( <IPv6-address> | <hostname> ) data-fill <pattern>`
#### Description
This command sets the hexadecimal pattern to be filled in the packet.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *pattern* | Optional | String | Set the hexadecimal pattern to be filled in the packet. A Maximum of 16 'pad' bytes can be specified to fill out the icmp packet.|
#### Examples
```
switch# ping6 2020::2 data-fill ab
PATTERN: 0xab
PING 2020::2(2020::2) 100 data bytes
108 bytes from 2020::2: icmp_seq=1 ttl=64 time=0.038 ms
108 bytes from 2020::2: icmp_seq=2 ttl=64 time=0.074 ms
108 bytes from 2020::2: icmp_seq=3 ttl=64 time=0.076 ms
108 bytes from 2020::2: icmp_seq=4 ttl=64 time=0.075 ms
108 bytes from 2020::2: icmp_seq=5 ttl=64 time=0.077 ms

--- 2020::2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3999ms
rtt min/avg/max/mdev = 0.038/0.068/0.077/0.015 ms

```

### Set datagram-size
#### Syntax
`ping6 ( <IPv6-address> | <hostname> ) datagram-size <size>`
#### Description
This command sets the size of the packet to be sent. The default value is 100 bytes.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *size* | Optional | <100-65468> | Select datagram-size between 100 and 65468.|
#### Examples
```
switch# ping6 2020::2 datagram-size 200
PING 2020::2(2020::2) 200 data bytes
208 bytes from 2020::2: icmp_seq=1 ttl=64 time=0.037 ms
208 bytes from 2020::2: icmp_seq=2 ttl=64 time=0.076 ms
208 bytes from 2020::2: icmp_seq=3 ttl=64 time=0.076 ms
208 bytes from 2020::2: icmp_seq=4 ttl=64 time=0.077 ms
208 bytes from 2020::2: icmp_seq=5 ttl=64 time=0.066 ms

--- 2020::2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3999ms
rtt min/avg/max/mdev = 0.037/0.066/0.077/0.016 ms

```

### Set interval
#### Syntax
`ping6 ( <IPv6-address> | <hostname> ) interval <time>`
#### Description
This command sets the interval seconds between sending each packet. The default value is 1 second.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *time* | Optional | <1-60> | Select interval in seconds between 1 and 60.|
#### Examples
```
switch# ping6 2020::2 interval 5
PING 2020::2(2020::2) 100 data bytes
108 bytes from 2020::2: icmp_seq=1 ttl=64 time=0.043 ms
108 bytes from 2020::2: icmp_seq=2 ttl=64 time=0.075 ms
108 bytes from 2020::2: icmp_seq=3 ttl=64 time=0.074 ms
108 bytes from 2020::2: icmp_seq=4 ttl=64 time=0.075 ms
108 bytes from 2020::2: icmp_seq=5 ttl=64 time=0.075 ms

--- 2020::2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 19999ms
rtt min/avg/max/mdev = 0.043/0.068/0.075/0.014 ms
```

### Set repetitions
#### Syntax
`ping6 ( <IPv6-address> | <hostname> ) repetitions <number>`
#### Description
This command sets the number of packets to be sent to the destination address. The default value is 5.
#### Authority
Root user.
#### Parameters
| Parameter | Status | Syntax | Description |
|-----------|--------|--------|-------------|
| *number* | Optional | <1-10000> | Select the number of packets to send between 1 and 10000.|
#### Examples
```
switch# ping6 2020::2 repetitions 6
PING 2020::2(2020::2) 100 data bytes
108 bytes from 2020::2: icmp_seq=1 ttl=64 time=0.039 ms
108 bytes from 2020::2: icmp_seq=2 ttl=64 time=0.070 ms
108 bytes from 2020::2: icmp_seq=3 ttl=64 time=0.076 ms
108 bytes from 2020::2: icmp_seq=4 ttl=64 time=0.076 ms
108 bytes from 2020::2: icmp_seq=5 ttl=64 time=0.071 ms
108 bytes from 2020::2: icmp_seq=6 ttl=64 time=0.078 ms

--- 2020::2 ping statistics ---
6 packets transmitted, 6 received, 0% packet loss, time 4999ms
rtt min/avg/max/mdev = 0.039/0.068/0.078/0.015 ms
```
