# ARP

## Contents
- [Display commands](#display-commands)
	- [show arp](#show-arp)
	- [show ipv6 neighbors](#show-ipv6-neighbors)

## Display commands

### show arp

##### Syntax
Under privileged mode.

`show arp`

#### Description
Displays the IPv4 addresses from the Address Resolution Protocol (ARP) table.

#### Authority
Operator.

##### Parameters

None.

##### Example
```
hostname# show arp
ARP IPv4 Entries:
------------------
IPv4 Address MAC Port Status
172.16.1.1 48:0F:CF:AF:D1:C7 1 --
172.16.1.2 48:0F:CF:AF:D1:C8 2 --

```

### show ipv6 neighbors

##### Syntax
Under privileged mode.

`show ipv6 neighbors`

#### Description
Displays IPv6 addresses from the neighbor table.

#### Authority
Operator.

##### Parameters

None.

##### Example
```
hostname# show ipv6 neighbors
IPv6 Entries:
------------------
IPv6 Address MAC Port Status
FE80:0000:0000:0000:0202:B3FF:FE1E:8329 00:01:02:03:04:08 4 --
FE80:0000:0000:0000:0202:B3FF:FE1E:8328 00:01:02:03:04:07 3 --
```
