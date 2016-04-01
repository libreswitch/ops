# DHCP Relay

## Contents
   - [Overview](#overview)
   - [Configure DHCP relay](#configure-dhcp-relay)
   - [How to use DHCP relay](#how-to-use-dhcp-relay)
   - [Configure DHCP relay option 82](#configure-dhcp-relay-option-82)
   - [How to use DHCP relay option 82](#how-to-use-dhcp-relay-option-82)
   - [Configure DHCP relay bootp gateway](#configure-dhcp-relay-bootp-gateway)
   - [How to use DHCP relay bootp gateway](#how-to-use-dhcp-relay-bootp-gateway)
   - [Configure DHCP relay hop count increment](#configure-dhcp-relay-hop-count-increment)
   - [How to use DHCP relay hop count increment](#how-to-use-dhcp-relay-hop-count-increment)

## Overview
The Dynamic Host Configuration Protocol (DHCP) is used for configuring hosts with IP addresses and other configuration parameters, without human intervention. The protocol is composed of
three components: the DHCP client, the DHCP server, and the DHCP relay agent. The DHCP client sends broadcast request packets to the network. DHCP servers respond with broadcast
packets that offer IP parameters, such as an IP address for the client. After the client chooses the IP parameters, communication between the client and the server is by unicast packets.
The function of the DHCP relay agent is to forward the DHCP messages to other subnets so that the DHCP server does not have to be on the same subnet as the DHCP clients. The DHCP relay agent
transfers DHCP messages from the DHCP clients located on a subnet without a DHCP server, to other subnets. It also relays answers from DHCP servers to DHCP clients. The DHCP relay agent on
the routing switch forwards DHCP client packets to all DHCP servers (helper IP addresses) that are configured in the table administered for each interface. The helper address
configuration is allowed only on data plane interfaces. The helper address should not be multicast or loopback address.

### DHCP relay option 82
Option 82 is called the relay agent information option. The option 82 field is inserted/replaced or the packet with this option is dropped by the DHCP relay agent, when forwarding client-originated DHCP packets to a DHCP server. Servers recognizing the relay agent information option may use the information to implement an IP address or other parameter assignment policies. The relay agent relays the server-to-client replies to the client.

### Hop count in DHCP requests
When a DHCP client broadcasts requests, the DHCP relay agent in the routing switch receives the packets and forwards them to the DHCP server (on a different subnet, if necessary.) During this
process, the DHCP relay agent increments the hop count before forwarding DHCP packets to the server. The DHCP server, in turn, includes the hop count in DHCP header from the received DHCP request in the
response sent back to a DHCP client. This is enabled by default.

### Configuring a BOOTP/DHCP relay gateway
The DHCP relay agent selects the lowest-numbered IP address on the interface to use for DHCP messages. The DHCP server then uses this IP address when it assigns client addresses. However,
this IP address may not be the same subnet as the one on which the client needs the DHCP service. This feature provides a way to configure a gateway address for the DHCP relay agent to use for
relayed DHCP requests, rather than the DHCP relay agent automatically assigning the lowest-numbered IP address.

## Configure DHCP relay
Helper address configuration on an interface is allowed even if routing is disabled on the interface, but DHCP relay functionality will be inactive on that interface. In case a client has
received an IP address, and no routing is configured, the IP address is valid on the client until the lease time expires.

### Syntax
`[no] dhcp-relay`
*Enable/Disable dhcp-relay. By default, it is enabled.*

`[no] ip helper-address <IPv4-address>`
*Configure the IP helper-address needed by DHCP relay on a particular interface.*

### Explanation of parameters
•   IPv4-address - The IPv4 address of the protocol server. This is a unicast address of a destination server on another subnet. The maximum number of helper addresses that can be configured per interface is eight. DHCP relay functions on L3 interfaces that include split-interfaces and sub-interfaces.

### Syntax
`show ip helper-address [interface <interface-name>]`
*Displays the configured IP helper-address(es).*

### Explanation of parameters
•   interface `<interface-name>` - The interface on which server addresses are configured.

## How to use DHCP relay

### Example 1

```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-relay

ops-as5712# show dhcp-relay

 DHCP Relay Agent                 : Enabled
 DHCP Request Hop Count Increment : Enabled
 Option 82                        : Disabled
 Response Validation              : Disabled
 Option 82 Handle Policy          : replace
 Remote ID                        : mac

 DHCP Relay Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  60         10         60         10

  DHCP Relay Option 82 Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  50         8          50         8
```

### Example 2

```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip helper-address 192.168.10.1
ops-as5712(config-if)# ip helper-address 192.168.20.1
ops-as5712(config-if)# ip helper-address 192.168.30.1

ops-as5712# show ip helper-address

IP Helper Addresses

 Interface: 1
  IP Helper Address
  -----------------
  192.168.10.1
  192.168.20.1
  192.168.30.1
```
### Example 3

```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no ip helper-address 192.168.10.1
ops-as5712(config-if)# no ip helper-address 192.168.20.1
ops-as5712(config-if)# no ip helper-address 192.168.30.1
ops-as5712# show ip helper-address
No helper-address configuration found.
```

### Example 4

```
ops-as5712# configure terminal
ops-as5712(config)# no dhcp-relay

ops-as5712# show dhcp-relay

 DHCP Relay Agent                 : Disabled
 DHCP Request Hop Count Increment : Enabled
 Option 82                        : Disabled
 Response Validation              : Disabled
 Option 82 Handle Policy          : replace
 Remote ID                        : mac

 DHCP Relay Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  60         10         60         10

  DHCP Relay Option 82 Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  50         8          50         8
```
```

## Configure DHCP relay option 82

### Syntax
Configure dhcp-relay option 82 globally:
`dhcp-relay option 82 < replace [validate] | drop [validate] | keep | validate [replace | drop  ] >  [ ip | mac ]`

Disable option 82 completely:
`no dhcp-relay option 82`

Disable response validation only for drop/replace policy. Not applicable if keep policy was selected.
`no dhcp-relay option 82 [validate]`

Display the dhcp-relay option 82 configurations:
`show dhcp-relay`



### Explanation of parameters

• drop - Configures the router to unconditionally drop any client DHCP packet received with existing option 82 fields. This means that such packets are not forwarded. Use this option where access to the router by untrusted clients is possible.
• keep - For any client DHCP packet received with existing option 82 fields, configures the router to forward the packet as-is, without replacing or adding to the existing option 82 fields.
• replace - Configures the switch to replace existing option 82 fields in an inbound client DHCP packet with an Option 82 field for the switch.
• validate - Operates when the routing switch is configured with append, replace, or drop as a forwarding policy. With validate enabled, the routing switch applies stricter rules to an incoming Option 82 server response to determine whether to forward or drop the response.
• ip - Specifies the IP address of the interface on which the client DHCP packet enters the switch.
• mac - Specifies the MAC address of the router. (The MAC address used is the same MAC address that is assigned to all interfaces configured on the router.) This is the default setting.



## How to use DHCP relay option 82

### Example 1

```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-relay option 82 replace validate mac

switch# show dhcp-relay

 DHCP Relay Agent                 : Enabled
 DHCP Request Hop Count Increment : Enabled
 Option 82                        : Enabled
 Response Validation              : Enabled
 Option 82 Handle Policy          : replace
 Remote ID                        : mac

 DHCP Relay Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  60         10         60         10

  DHCP Relay Option 82 Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  50         8          50         8
```

### Example 2

```
ops-as5712# configure terminal
ops-as5712(config)# no dhcp-relay option 82

ops-as5712# show dhcp-relay

 DHCP Relay Agent                 : Enabled
 DHCP Request Hop Count Increment : Enabled
 Option 82                        : Disabled
 Response Validation              : Enabled
 Option 82 Handle policy          : replace
 Remote ID                        : mac

 DHCP Relay Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  60         10         60         10

  DHCP Relay Option 82 Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  50         8          50         8
```

## Configure DHCP relay BOOTP gateway

### Syntax
`[no] ip bootp-gateway <IPv4-address>`
*Configure the IP bootp-gateway needed by DHCP relay on a particular interface.*

### Explanation of parameters
• IPv4-address - The IPv4 address of the gateway. Provides a way to configure a gateway address for the DHCP relay agent to use for DHCP requests, rather than the DHCP relay agent automatically assigning the lowest-numbered IP address.

`show dhcp-relay bootp-gateway [interface <interface-name>]`
*Displays the bootp-gateway configuration.*

Explanation of parameters
• interface `<interface-name>` - Interface on which gateway address is configured.


## How to use DHCP relay BOOTP gateway

### Example 1
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip bootp-gateway 1.1.1.1

ops-as5712# show dhcp-relay bootp-gateway

 BOOTP Gateway Entries

 Interface            BOOTP Gateway
 -------------------- ---------------
 1                    1.1.1.1
```
### Example 2

```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no ip bootp-gateway 1.1.1.1
ops-as5712# show dhcp-relay bootp-gateway
No bootp-gateway configuration found.
```

## Configure DHCP relay hop count increment
### Syntax
`[no] dhcp-relay hop-count-increment`
* Enable/Disable the dhcp-relay hop-count-increment command. By default, it is enabled.*

`show dhcp-relay`
* Displays the dhcp-relay hop-count-increment configurations.*

## How to use DHCP relay hop count increment

### Example 1

```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-relay hop-count-increment

ops-as5712# show dhcp-relay

 DHCP Relay Agent                 : Enabled
 DHCP Request Hop Count Increment : Enabled
 Option 82                        : Disabled
 Response Validation              : Disabled
 Option 82 Handle Policy          : replace
 Remote ID                        : mac

 DHCP Relay Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  60         10         60         10

  DHCP Relay Option 82 Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  50         8          50         8
```

### Example 2

```
ops-as5712# configure terminal
ops-as5712(config)# no dhcp-relay hop-count-increment

ops-as5712# show dhcp-relay

 DHCP Relay Agent                 : Enabled
 DHCP Request Hop Count Increment : Disabled
 Option 82                        : Disabled
 Response Validation              : Disabled
 Option 82 Handle Policy          : replace
 Remote ID                        : mac

 DHCP Relay Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  60         10         60         10

  DHCP Relay Option 82 Statistics:

  Client Requests       Server Responses

  Valid      Dropped    Valid      Dropped
  ---------- ---------- ---------- ----------
  50         8          50         8
```
