# UDP Broadcast Forwarder

## Contents

- [UDP broadcast forwarding](#udp-broadcast-forwarding)
    - [Global enable/disable UDP broadcast forwarding](#global-enable/disable-udp-broadcast-forwarding)
    - [Configure UDP forward-protocol on an interface](#configure-udp-forward-protocol-on-an-interface)
    - [Show UDP forward-protocol](#show-udp-forward-protocol)

## UDP broadcast forwarding
### Global enable/disable UDP broadcast forwarding
#### Syntax
`[no] ip udp-bcast-forward`
#### Description
This command enables/disables the UDP broadcast forwarding.
#### Authority
Root and Admin users.
#### Parameters
No parameters.
#### Examples
```
switch(config)#ip udp-bcast-forward

switch(config)#no ip udp-bcast-forward
```

### Configure UDP forward-protocol on an interface
#### Syntax
`[no] ip forward-protocol udp <IPv4-address> <port-number | protocol-name>`
#### Description
This command configures a UDP broadcast server on the interface for a particular UDP port.
#### Authority
Root and Admin users.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *IPv4-address* | Required | A.B.C.D | The IPv4 address of the protocol server. This can be either be a unicast address of a destination server on another subnet, or the broadcast address of the subnet on which a destination server operates.
| *port-number* | Required | Integer | Any UDP port number corresponding to a UDP application supported on a device.
| *protocol-name* | Required | String |  Any common names for certain well-known UDP port numbers. Supported protocol names are: dns: Domain Name Service (53), ntp: Network Time Protocol (123), netbios-ns: NetBIOS Name Service (137), netbios-dgm: NetBIOS Datagram Service (138), radius: Remote Authentication Dial-In User Service (1812), radius-old: Remote Authentication Dial-In User Service (1645), rip: Routing Information Protocol (520), snmp: Simple Network Management Protocol (161), snmp-trap: Simple Network Management Protocol (162), tftp: Trivial File Transfer Protocol (69), timep: Time Protocol (37).
#### Examples
```
switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 53

switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 dns

```

### Show UDP forward-protocol
#### Syntax
`show ip forward-protocol [interface <WORD>]`
#### Description
This command shows the server addresses where broadcast requests received by the switch are to be forwarded.
#### Authority
Root and Admin users.
#### Parameters
| Parameter | Status | Syntax | Description |
|:-----------|:----------|:----------------:|:------------------------|
| *interface <WORD>* | Optional | String | Select the interface on which UDP broadcast forwarding information needs to be displayed.
#### Examples
```
switch(config)#ip udp-bcast-forward
switch(config)#interface 1
switch(config-if)#ip forward-protocol udp 1.1.1.1 53
switch(config-if)#ip forward-protocol udp 8.1.1.1 161
switch(config-if)#ip forward-protocol udp 4.4.4.4 137
switch(config)#interface 2
switch(config-if)#ip forward-protocol udp 2.2.2.2 161


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
  2.2.2.2                161

switch#show ip forward-protocol interface 1

UDP Broadcast Forwarder : enabled

Interface: 1
  IP Forward Address    UDP Port
  -------------------------------
  4.4.4.4                137
  1.1.1.1                53
  8.1.1.1                161

```
