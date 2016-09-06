# sFlow Commands

## Contents

- [sFlow configuration commands](#sflow-configuration-commands)
	- [Global context commands](#global-context-commands)
		- [Enable sFlow globally](#enable-sflow-globally)
		- [Disable sFlow globally](#disable-sflow-globally)
		- [Set sFlow sampling rate](#set-sflow-sampling-rate)
		- [Remove sFlow sampling rate](#remove-sflow-sampling-rate)
		- [Set sFlow polling interval](#set-sflow-polling-interval)
		- [Remove sFlow polling interval](#remove-sflow-polling-interval)
		- [Set sFlow collector IP address](#set-sflow-collector-ip-address)
		- [Remove sFlow collector ip address](#remove-sflow-collector-ip-address)
		- [Set sFlow agent interface name and family](#set-sflow-agent-interface-name-and-family)
		- [Remove sFlow agent interface name and family](#remove-sflow-agent-interface-name-and-family)
		- [Set sFlow header size](#set-sflow-header-size)
		- [Remove sFlow header size](#remove-sflow-header-size)
		- [Set sFlow max datagram size](#set-sflow-max-datagram-size)
		- [Remove sFlow max datagram size](#remove-sflow-max-datagram-size)
	- [Interface context commands](#interface-context-commands)
		- [Enable sFlow on the interface](#enable-sflow-on-the-interface)
		- [Disable sFlow on the interface](#disable-sflow-on-the-interface)
- [sFlow display commands](#sflow-display-commands)
	- [Show sFlow configuration](#show-sflow-configuration)
	- [Show sFlow configuration interface](#show-sflow-configuration-interface)

## sFlow configuration commands

### Global context commands
#### Enable sFlow globally
##### Syntax
`sflow enable`
##### Description
This command enables sFlow globally. By default sFlow is disabled.
##### Authority
All users.
##### Parameters
No parameters.
##### Example
```
switch# configure terminal
switch(config)# sflow enable
```
#### Disable sFlow globally
##### Syntax
`no sflow enable`
##### Description
This command disables sFlow globally. By default sFlow is disabled.
##### Authority
All users.
##### Parameters
No parameters.
##### Example
```
switch# configure terminal
switch(config)# no sflow enable
```
#### Set sFlow sampling rate
##### Syntax
`sflow sampling <rate>`
##### Description
This command sets the global sampling rate for sFlow. The default sampling rate is 4096, which means that one in every 4096 packets is sampled.
##### Authority
All users.
##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *rate* | Required | 1-1000000000 | Sets the global sampling rate. |
##### Example
```
switch# configure terminal
switch(config)# sflow sampling 1000
```
#### Remove sFlow sampling rate
##### Syntax
`no sflow sampling`
##### Description
This command sets the global sampling rate back to the default of 4096, which means that one in every 4096 packets is sampled.
##### Authority
All users.
##### Parameters
No parameters.
##### Example
```
switch# configure terminal
switch(config)# no sflow sampling
```
#### Set sFlow polling interval
##### Syntax
`sflow polling <interval>`
##### Description
This command sets the global polling interval, which by default is 30 seconds. Set the polling interval to 0 to disable polling.
##### Authority
All users.
##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interval* | Required | 0-3600 | Sets the global polling interval. |
##### Example
```
switch# configure terminal
switch(config)# sflow polling 10
```
#### Remove sFlow polling interval
##### Syntax
`no sflow polling`
##### Description
This command resets the global polling interval to 30 seconds.
##### Authority
All users.
##### Parameters
No parameters.
##### Example
```
switch# configure terminal
switch(config)# no sflow polling
```
#### Set sFlow collector IP address
##### Syntax
`sflow collector <IP> [port <port-number>] [vrf <vrf-name>]`
##### Description
This command sets a collector IP address (IPv4 or IPv6), with optional port and VRF (virtual routing and forwarding). The default port is 6343. VRF is the vrf on which the collector can be reached. By default, this is the data vrf. A maximum of three collectors can be configured.
##### Authority
All users.
##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *IP* | Required | A.B.C.D or X:X::X:X | Collector IPv4 or IPv6 address. |
| *port-number* | Optional | 0-65535 | Port on which to reach a collector. |
| *vrf-name* | Optional | String | Name of VRF on which to reach a collector. |
##### Example
```
switch# configure terminal
switch(config)# sflow collector 10.0.0.1 port 6343 vrf vrf1
```
#### Remove sFlow collector ip address
##### Syntax
`no sflow collector <IP> [port <port-number>] [vrf <vrf-name>]`
##### Description
This command removes a collector IP address (if present).
##### Authority
All users.
##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *IP* | Required | A.B.C.D or X:X::X:X | Collector IPv4 or IPv6 address. |
| *port-number* | Optional | 0-65535 | Port on which to reach a collector. |
| *vrf-name* | Optional | String | Name of VRF on which to reach a collector. |
##### Example
```
switch# configure terminal
switch(config)# no sFlow collector 10.0.0.1 port 6343 vrf vrf2
```
#### Set sFlow agent interface name and family
##### Syntax
`sflow agent-interface <interface-name> [ipv4 | ipv6]`
##### Description
This command sets the name of the interface that is used for the agent IP in sFlow datagrams.
If not specified, the system picks the IP address from one of the interfaces in a priority order (to be determined). It also optionally sets the family type (IPv4 or IPv6) for the agent interface, which is set to IPv4 by default.
##### Authority
All users.
##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface-name* | Required | System defined | Name of the interface to use for agent IP address. |
| *ipv4* | Optional | Literal | IPv4 address family. |
| *ipv6* | Optional | Literal | IPv6 address family. |
##### Example
```
switch# configure terminal
switch(config)# sflow agent-interface 1 ipv4
```
#### Remove sFlow agent interface name and family
##### Syntax
`no sflow agent-interface`
##### Description
This command removes an agent interface and family if set.
##### Authority
All users.
##### Parameters
No parameters.
##### Example
```
switch# configure terminal
switch(config)# no sflow agent-interface
```

#### Set sFlow header size
##### Syntax
`sflow header-size <size>`
##### Description
This command sets the sFlow header size in bytes. The default value is 128.
##### Authority
All users.
##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *size* | Required | 64-256 | Sets size of the header in bytes. |
##### Example
```
switch# configure terminal
switch(config)# sflow header-size 64
```
#### Remove sFlow header size
##### Syntax
`no sflow header-size`
##### Description
This command resets the sFlow header size to the default value of 128 bytes.
##### Authority
All users.
##### Parameters
No parameters.
##### Example
```
switch# configure terminal
switch(config)# no sflow header-size
```
#### Set sFlow max datagram size
##### Syntax
`sflow max-datagram-size <size>`
##### Description
This command sets the maximum number of bytes that are sent in one sFlow datagram. The default value is 1400 bytes.
##### Authority
All users.
##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *size* | Required | 200-9000 | Sets the maximum size of an sFlow datagram. |
##### Example
```
switch# configure terminal
switch(config)# sflow max-datagram-size 1000
```
#### Remove sFlow max datagram size
##### Syntax
`no sflow max-datagram-size`
##### Description
This command resets the number of bytes that are sent in one sFlow datagram to the default of 1400.
##### Authority
All users.
##### Parameters
No parameters.
##### Example
```
switch# configure terminal
switch(config)# no sflow max-datagram-size
```
### Interface context commands
#### Enable sFlow on the interface
##### Syntax
`sflow enable`
##### Description
This command enables sFlow on the interface. It is used in the **interface** context.
##### Authority
All users.
##### Parameters
No parameters.
##### Example
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# sflow enable
```
#### Disable sFlow on the interface
##### Syntax
`no sflow enable`
##### Description
This command disables sFlow on the interface. It is used in the **interface** context.
##### Authority
All users.
##### Parameters
No parameters.
##### Example
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# no sflow enable
```

## sFlow display commands
### Show sFlow configuration
#### Syntax
`show sflow`
#### Description
This command displays global sFlow configuration settings and statistics.
#### Authority
All users.
#### Parameters
No parameters.
#### Example
```
switch# show sflow
 sFlow Configuration
 -----------------------------------------
 sFlow                         enabled
 Collector IP/Port/Vrf         10.0.0.1/6343/vrf_default
                               10.0.0.2/6343/vrf_default
 Agent Interface               1
 Agent Address Family          ipv4
 Sampling Rate                 1024
 Polling Interval              30
 Header Size                   128
 Max Datagram Size             1400
 Number of Samples             0
 ```

### Show sFlow configuration interface
#### Syntax
`show sflow <interface>`
#### Description
This command displays sFlow configuration settings and  statistics for an specific interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *interface* | Required | String | Name of the interface. System defined. |
#### Example
```
switch# show sflow 1
 sFlow configuration - Interface 1
 -----------------------------------------
 sFlow                         enabled
 Sampling Rate                 1024
 Number of Samples             0

```
