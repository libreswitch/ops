# sFlow

## Contents
- [Overview](#overview)
- [Configuring the OpenSwitch sFlow agent](#configuring-the-openswitch-sflow-agent)
	- [Default settings](#default-settings)
	- [Enabling sFlow globally](#enabling-sflow-globally)
	- [Disabling sFlow globally](#disabling-sflow-globally)
	- [Configuring collectors](#configuring-collectors)
	- [Configuring the sampling rate](#configuring-the-sampling-rate)
	- [Configuring the polling interval](#configuring-the-polling-interval)
	- [Configuring agent interface name and address family](#configuring-agent-interface-name-and-address-family)
	- [Configuring header size](#configuring-header-size)
	- [Configuring max datagram size](#configuring-max-datagram-size)
	- [Enableing/disabling sFlow per interface](#enableingdisabling-sflow-per-interface)
- [Viewing sFlow configuration](#viewing-sflow-configuration)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
sFlow is a technology for monitoring traffic in high-speed switched or routed
networks. The sFlow monitoring system is comprised of:

- **An sFlow Agent** that runs on a network device, such as a switch. The agent
  uses sampling techniques to capture information about the data traffic
flowing through the device and forwards this information to an sFlow collector.
The OpenSwitch sFlow agent can sample traffic from all physical and bonded
interfaces in the system.

- **An sFlow Collector** that receives monitoring information from sFlow
  agents. The collector stores this information so that a network administrator
can analyze it to understand network data flow patterns.

**Important: sFlow datagrams sent to the collector are not encrypted, therefore
any sensitive information contained in an sFlow sample is exposed.**

## Configuring the OpenSwitch sFlow agent

- The agent can communicate with up to three sFlow collectors at the same time.
- Only the default VRF is supported.
- Only in-band collectors are supported.
- Support is provided for the SNMP MIB-2 ifTable.
- Although the CLI allows high sampling rates, the switch may drop samples if
  it cannot handle the rate of sampled packets.


### Default settings
- sFlow is disabled on all interfaces.
- Collector port = 6343.
- Agent interface address type = IPv4.
- Sampling rate = 4096.
- Polling interval = 30 seconds.
- Header size = 128 bytes.
- Max datagram size = 1400 bytes.


### Enabling sFlow globally
To enable sFlow on all interfaces on the switch:
```
switch#
switch# configure terminal
switch(config)# sflow enable
```

### Disabling sFlow globally
To disable sFlow on all interfaces on the switch:
```
switch#
switch# configure terminal
switch(config)# no sflow enable
```

### Configuring collectors
To configure an sFlow collector:
```
switch(config)# sflow collector <ip> [port <port>] [vrf <vrf-name>]
```
- **ip** is the IPv4 or IPv6 address of the collector.
- **port** is any valid UDP port that the collector is listening on. Default is 6343.
- **vrf-name** is the name of a VRFs on the switch. Default is vrf_default.

To remove an sFlow collector:
```
switch(config)# no sflow collector <IP> [port <port>] [vrf <vrf-name>]
```

### Configuring the sampling rate
To configure the global sampling rate:
```
switch(config)# sflow sampling <rate>
```
- **rate** is the approximate number of packets between samples. Default is
  4096, which means that approximately every 4096 packet will be sampled.
(There is some jitter introduced purposefully into the sample collection.)

To reset the global sampling rate to default:
```
switch(config)# no sflow sampling
```

### Configuring the polling interval
To configure the interval at which statistics are send to the collector:
```
switch(config)# sflow polling <interval>
```
- **interval** is in seconds and the default is 30.

To set the polling interval back to default:
```
switch(config)# no sflow polling
```

### Configuring agent interface name and address family
To define sFlow agent interface settings:
```
switch(config)# sflow agent-interface <ifname> [ipv4|ipv6]
```
- **ifname** is the name of the interface whose IP address will be used as the
  agent IP in sFlow datagrams. If not specified, system will pick the IP
address from one of the interfaces in the switch.

- **ipv4 | ipv6** optionally set the address type for the agent interface. By
  default the address type is IPv4.

### Configuring header size
To set the sFlow header size:
```
switch(config)# sflow header-size <size>
```
- **size** is the the maximum number of bytes to copy and forward from the
  header of the sampled
packet. Default is 128 bytes.

To set the sFlow header size back to default:
```
switch(config)# no sflow header-size
```

### Configuring max datagram size
To set the sFlow max datagram size:
```
switch(config)# sflow max-datagram-size <size>
```
- **size** is the maximum number of bytes that will be sent in one sFlow UDP
  datagram.  Default is 1400 bytes.

To set the sFlow max datagram size back to default:
```
switch(config)# no sflow max-datagram-size
```

### Enableing/disabling sFlow per interface
sFlow can be enbled/disabled individually on each interface.

To enable sFlow on a specific interface:
```
switch(config)# interface <interface-name>
switch(config-if)# sflow enable
```

To enable sFlow on a specific interface:
```
switch(config)# interface <interface-name>
switch(config-if)# no sflow enable
```

## Viewing sFlow configuration
To view global sFlow configuration settings:
```
switch# show sflow
```
To view sFlow settings for a specific interface:

```
switch# show sflow <interface-name>
```


## CLI

Click [here](/documents/user/sflow_cli) for the CLI commands related to the
sFlow feature.

## Related features
None
