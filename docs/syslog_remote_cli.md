# Remote Syslog Logging Configuration Commands

## Contents

- [Logging configuration commands](#logging-configuration-commands)
	- [Syntax](#syntax)
	- [Description](#description)
	- [Authority](#authority)
	- [Parameters](#parameters)
	- [Examples](#examples)

## Logging configuration commands

#### Syntax
```
[no] logging <IPv4-address> | <IPv6-address> | <hostname> [udp [<port>] | tcp [<port>]] [severity <level>]
```

#### Description
This command is used to add or remove remote syslog server configurations.

#### Authority
All users.

#### Parameters
<!-- Provide for the parameters for the command. -->

| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------|---------------------------------------|
| **IPv4-address** | Required | A.B.C.D | IPv4 address of the remote syslog server |
| **IPv6-address** | Required | X:X::X:X | IPv6 address of the remote syslog server |
| **hostname** | Required | string | FQDN or hostname of the remote syslog server |
| *udp* | Optional | string | UDP transport protocol used to send syslog messages |
| *tcp* | Optional | string | TCP transport protocol used to send syslog messages|
| *port* | Optional | <1-65535> | Port Number on which the remote syslog server runs. Default for UDP is 514 and for TCP is 1470 |
| *severity* | Optional | string | Filter syslog messages using severity  |
| *level* | Optional | string | Filter messages with severity higher than or equal to the specified value |



#### Examples
<!--    myprogramstart -s process_xyz-->

```
switch(config)#logging 10.0.10.2

switch(config)#no logging

switch(config)#logging 10.0.10.6 severity info

switch(config)#no logging 10.0.10.6

switch(config)#logging 10.0.10.9 tcp 4242 severity err
```
