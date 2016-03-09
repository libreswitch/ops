# Proxy ARP

## Contents
   - [Overview](#overview)
   - [Configuring Proxy ARP](#configuring-proxy-arp)
   - [Examples](#examples)
       - [Enabling Proxy ARP on an interface](#enabling-proxy-arp-on-an-interface)
       - [Disabling Proxy ARP on an interface](#disabling-proxy-arp-on-an-interface)
       - [Viewing status of Proxy ARP on an interface](#viewing-status-of-proxy-arp-on-an-interface)

## Overview
Proxy ARP is a technique by which a device on a given network answers the ARP queries for a network address that is not on that network. The ARP proxy is aware of the location of the traffic's destination, and offers its own MAC address as the final destination.

## Configuring Proxy ARP
Proxy ARP is available only if routing is enabled on an interface.

Syntax:
`[no] ip proxy-arp`

*The above syntax enables or disables proxy ARP on an L3 interface. By default, it is disabled.*

##Examples
####Enabling proxy ARP on an interface
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# ip proxy-arp

```
####Disabling proxy ARP on an interface
```
ops-as5712# configure terminal
ops-as5712(config)# interface 1
ops-as5712(config-if)# no ip proxy-arp

```

####Viewing status of proxy ARP on an interface
```
ops-as5712# show interface 1

Interface 1 is down (Administratively down)
 Admin state is down
 State information: admin_down
 Proxy ARP: Enabled
 Hardware: Ethernet, MAC Address: 70:72:cf:67:e0:87
 MTU 0
 Half-duplex
 Speed 0 Mb/s
 Auto-Negotiation is turned on
 Input flow-control is off, output flow-control is off
 RX
            0 input packets              0 bytes
            0 input error                0 dropped
            0 CRC/FCS
 TX
            0 output packets             0 bytes
            0 input error                0 dropped
            0 collision


```
```
ops-as5712# show running-config
Current configuration:
!
!
!
vlan 1
    no shutdown
interface 1
    ip proxy-arp

```
