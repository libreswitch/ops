Ping Utility
======
## Contents

- [Ping options](##ping-options)
- [Ping6 options](##ping6-options)

##Ping options
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
switch# ping 10.0.3.1
PING 10.0.3.1 (10.0.3.1): 100 data bytes
 108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.063 ms
 108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.023 ms
 108 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.050 ms
 108 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.044 ms
 108 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.056 ms
 --- 10.0.3.1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.023/0.047/0.063/0.000 ms
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
PING localhost.localdomain (127.0.0.1): 100 data bytes
 108 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.058 ms
 108 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.049 ms
 108 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.048 ms
 108 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.043 ms
 108 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.048 ms
 --- localhost.localdomain ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.043/0.049/0.058/0.000 ms
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
| *pattern* | Optional | String | Set the hexadecimal pattern to be filled in the packet. Pattern length should be less than 16 hexadecimal characters.|
#### Examples
```
switch# ping 10.0.3.1 data-fill ab
PING 10.0.3.1 (10.0.3.1): 100 data bytes
 108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.053 ms
 108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.049 ms
 108 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.049 ms
 108 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.048 ms
 108 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.046 ms
 --- 10.0.3.1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.046/0.049/0.053/0.000 ms
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
switch# ping 10.0.3.1 datagram-size 200
PING 10.0.3.1 (10.0.3.1): 200 data bytes
 208 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.053 ms
 208 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.047 ms
 208 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.049 ms
 208 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.045 ms
 208 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.048 ms
 --- 10.0.3.1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.045/0.048/0.053/0.000 ms
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
switch# ping 10.0.3.1 interval 2
PING 10.0.3.1 (10.0.3.1): 100 data bytes
 108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.055 ms
 108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.048 ms
 108 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.049 ms
 108 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.049 ms
 108 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.049 ms
 --- 10.0.3.1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.048/0.050/0.055/0.000 ms
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
switch# ping 10.0.3.1 repetitions 2
PING 10.0.3.1 (10.0.3.1): 100 data bytes
 108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.054 ms
 108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.048 ms
 --- 10.0.3.1 ping statistics ---
 2 packets transmitted, 2 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.048/0.051/0.054/0.000 ms
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
switch# ping 10.0.3.1 timeout 3
PING 10.0.3.1 (10.0.3.1): 100 data bytes
 108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.052 ms
 108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.047 ms
 108 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.049 ms
 108 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.032 ms
 108 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.051 ms
 --- 10.0.3.1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.032/0.046/0.052/0.000 ms
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
switch# ping 10.0.3.1 tos 0
PING 10.0.3.1 (10.0.3.1): 100 data bytes
 108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.056 ms
 108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.053 ms
 108 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.045 ms
 108 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.052 ms
 108 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.026 ms
 --- 10.0.3.1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.026/0.046/0.056/0.000 ms
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
switch# ping 10.0.3.1 ip-option include-timestamp
PING 10.0.3.1 (10.0.3.1): 100 data bytes
 108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.056 ms
 TS:    46747881 ms
        46747881 ms
        46747881 ms
        46747881 ms

 108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.049 ms
 TS:    46748882 ms
        46748882 ms
        46748882 ms
        46748883 ms

 108 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.053 ms
 TS:    46749884 ms
        46749884 ms
        46749884 ms
        46749884 ms

 108 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.051 ms
 TS:    46750885 ms
        46750885 ms
        46750885 ms
        46750885 ms

 108 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.045 ms
 TS:    46751886 ms
        46751886 ms
        46751886 ms
        46751886 ms

 --- 10.0.3.1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.045/0.051/0.056/0.000 ms

switch# ping 10.0.3.1 ip-option include-timestamp-and-address
PING 10.0.3.1 (10.0.3.1): 100 data bytes
 108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.054 ms
 TS:    switch (10.0.3.1)       46815087 ms
        switch (10.0.3.1)       46815087 ms
        switch (10.0.3.1)       46815087 ms
        switch (10.0.3.1)       46815087 ms

 108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.050 ms
 TS:    switch (10.0.3.1)       46816088 ms
        switch (10.0.3.1)       46816088 ms
        switch (10.0.3.1)       46816088 ms
        switch (10.0.3.1)       46816088 ms

 108 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.053 ms
 TS:    switch (10.0.3.1)       46817090 ms
        switch (10.0.3.1)       46817090 ms
        switch (10.0.3.1)       46817090 ms
        switch (10.0.3.1)       46817090 ms

 108 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.049 ms
 TS:    switch (10.0.3.1)       46818091 ms
        switch (10.0.3.1)       46818091 ms
        switch (10.0.3.1)       46818091 ms
        switch (10.0.3.1)       46818091 ms

 108 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.052 ms
 TS:    switch (10.0.3.1)       46819092 ms
        switch (10.0.3.1)       46819092 ms
        switch (10.0.3.1)       46819092 ms
        switch (10.0.3.1)       46819092 ms

 --- 10.0.3.1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.049/0.052/0.054/0.000 ms

switch# ping 10.0.3.1 ip-option record-route
PING 10.0.3.1 (10.0.3.1): 100 data bytes
 108 bytes from 10.0.3.1: icmp_seq=0 ttl=64 time=0.055 ms
 RR:    switch (10.0.3.1)
        switch (10.0.3.1)
        switch (10.0.3.1)
        switch (10.0.3.1)
 108 bytes from 10.0.3.1: icmp_seq=1 ttl=64 time=0.054 ms        (same route)
 108 bytes from 10.0.3.1: icmp_seq=2 ttl=64 time=0.054 ms        (same route)
 108 bytes from 10.0.3.1: icmp_seq=3 ttl=64 time=0.053 ms        (same route)
 108 bytes from 10.0.3.1: icmp_seq=4 ttl=64 time=0.054 ms        (same route)
 --- 10.0.3.1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.053/0.054/0.055/0.000 ms
```

##Ping6 options

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
switch# ping6 2000::1
PING 2000::1 (2000::1): 100 data bytes
 108 bytes from 2000::1: icmp_seq=0 ttl=64 time=0.092 ms
 108 bytes from 2000::1: icmp_seq=1 ttl=64 time=0.085 ms
 108 bytes from 2000::1: icmp_seq=2 ttl=64 time=0.054 ms
 108 bytes from 2000::1: icmp_seq=3 ttl=64 time=0.084 ms
 108 bytes from 2000::1: icmp_seq=4 ttl=64 time=0.088 ms
 --- 2000::1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.054/0.081/0.092/0.000 ms
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
PING localhost (::1): 100 data bytes
 108 bytes from ::1: icmp_seq=0 ttl=64 time=0.062 ms
 108 bytes from ::1: icmp_seq=1 ttl=64 time=0.048 ms
 108 bytes from ::1: icmp_seq=2 ttl=64 time=0.057 ms
 108 bytes from ::1: icmp_seq=3 ttl=64 time=0.054 ms
 108 bytes from ::1: icmp_seq=4 ttl=64 time=0.047 ms
 --- localhost ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.047/0.054/0.062/0.000 ms
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
| *pattern* | Optional | String | Set the hexadecimal pattern to be filled in the packet. Pattern length should be less than 16 hexadecimal characters.|
#### Examples
```
switch# ping6 2000::1 data-fill ab
PING 2000::1 (2000::1): 100 data bytes
 108 bytes from 2000::1: icmp_seq=0 ttl=64 time=0.118 ms
 108 bytes from 2000::1: icmp_seq=1 ttl=64 time=0.078 ms
 108 bytes from 2000::1: icmp_seq=2 ttl=64 time=0.088 ms
 108 bytes from 2000::1: icmp_seq=3 ttl=64 time=0.087 ms
 108 bytes from 2000::1: icmp_seq=4 ttl=64 time=0.063 ms
 --- 2000::1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.063/0.087/0.118/0.000 ms
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
switch# ping6 2000::1 datagram-size 200
PING 2000::1 (2000::1): 200 data bytes
 208 bytes from 2000::1: icmp_seq=0 ttl=64 time=0.110 ms
 208 bytes from 2000::1: icmp_seq=1 ttl=64 time=0.061 ms
 208 bytes from 2000::1: icmp_seq=2 ttl=64 time=0.085 ms
 208 bytes from 2000::1: icmp_seq=3 ttl=64 time=0.077 ms
 208 bytes from 2000::1: icmp_seq=4 ttl=64 time=0.087 ms
 --- 2000::1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.061/0.084/0.110/0.000 ms
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
switch# ping6 2000::1 interval 2
PING 2000::1 (2000::1): 100 data bytes
 108 bytes from 2000::1: icmp_seq=0 ttl=64 time=0.109 ms
 108 bytes from 2000::1: icmp_seq=1 ttl=64 time=0.029 ms
 108 bytes from 2000::1: icmp_seq=2 ttl=64 time=0.028 ms
 108 bytes from 2000::1: icmp_seq=3 ttl=64 time=0.029 ms
 108 bytes from 2000::1: icmp_seq=4 ttl=64 time=0.029 ms
 --- 2000::1 ping statistics ---
 5 packets transmitted, 5 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.028/0.045/0.109/0.032 ms

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
switch# ping6 2000::1 repetitions 2
PING 2000::1 (2000::1): 100 data bytes
 108 bytes from 2000::1: icmp_seq=0 ttl=64 time=0.115 ms
 108 bytes from 2000::1: icmp_seq=1 ttl=64 time=0.075 ms
 --- 2000::1 ping statistics ---
 2 packets transmitted, 2 packets received, 0% packet loss
 round-trip min/avg/max/stddev = 0.075/0.095/0.115/0.000 ms
```
