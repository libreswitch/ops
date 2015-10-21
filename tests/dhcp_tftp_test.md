DHCP-TFTP Feature test cases
========

## Contents
   - [DHCP IPv4 dynamic address pool configuration](#dhcp-ipv4-dynamic-address-pool-configuration)
   - [DHCP IPV4 static address pool configuration](#dhcp-ipv4-static-address-pool-configuration)

## DHCP IPv4 dynamic address pool configuration

### Configure DHCP IPV4 address pool for dynamic address allocations and verify the address assignments on hosts acting as DHCP clients.

#### Objective
The test case checks if DHCP IPV4 pool can be successfully created with specified configuration range of IPV4 addresses. The test case validates address assignments on hosts acting as DHCP clients.

#### Requirements
- Virtual mininet test setup
- **FT file**: ops/tests/dhcp-tftp/test_dhcp_tftp_ft_dynamic_ipv4_commands.py

#### Setup
##### Topology diagram
```
+------------------------------+
|                              |
|           Switch             |
|                              |
|                              |
+------------------------------+
       1                2
       |                |
       |                |
     eth1             eth1
 +-----------+    +-----------+
 |           |    |           |
 |  Host 1   |    |  Host 2   |
 |           |    |           |
 +-----------+    +-----------+
```
#### Description
This creates a DHCP IPV4 address pool for the specified range of addresses and validates the address assignments on the hosts acting as DHCP clients.
#### Test setup
Configure IP addresses for interface 1 and 2 on the switch.
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# no shutdown
switch(config-if)# ip address 10.0.0.1/8
switch(config-if)# exit
switch(config)# interface 2
switch(config-if)# no shutdown
switch(config-if)# ip address 20.0.0.1/8
switch(config-if)# end
```
Configure the DHCP IPV4 address pool on the DHCP server.
```
switch# configure terminal
switch(config)# dhcp-server
switch(config-dhcp-server)# range host1 start-ip-address 10.0.0.1 end-ip-address 10.0.0.100
switch(config-dhcp-server)# range host2 start-ip-address 20.0.0.1 end-ip-address 20.0.0.100
switch(config-dhcp-server)# end
```
Configure the DHCP clients (hosts 1 and 2) for DHCP requests.
```
mininet> h1 ifconfig -a
mininet> h1 ip addr del 10.0.0.1/8 dev h1-eth0
mininet> h1 dhclient h1-eth0

mininet> h2 ifconfig -a
mininet> h2 ip addr del 10.0.0.2/8 dev h2-eth0
mininet> h2 dhclient h2-eth0
```
#### Test result criteria
##### Test pass criteria
The `show dhcp-server` command on the DHCP server gives the following output:
```
switch# show dhcp-server

DHCP dynamic IP allocation configuration
----------------------------------------
Name    Start IP Address  End IP Address
----------------------------------------
host1   10.0.0.1          10.0.0.100
host2   20.0.0.1          20.0.0.100


DHCP static IP allocation configuration
---------------------------------------
DHCP static host is not configured.



DHCP options configuration
--------------------------------
DHCP options are not configured.


DHCP Match configuration
-----------------------------
DHCP match is not configured.


DHCP BOOTP configuration
-----------------------------
DHCP BOOTP is not configured.
```

The `ifconfigc` command on the hosts (DHCP clients) gives the following output:
```
mininet> h2 ifconfig h2-eth0
h2-eth0   Link encap:Ethernet  HWaddr 8a:07:f7:92:69:30
inet addr:20.0.0.90  Bcast:20.255.255.255  Mask:255.0.0.0
inet6 addr: fe80::8807:f7ff:fe92:6930/64 Scope:Link
UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
RX packets:54 errors:0 dropped:0 overruns:0 frame:0
TX packets:22 errors:0 dropped:1 overruns:0 carrier:0
collisions:0 txqueuelen:1000
RX bytes:5558 (5.5 KB)  TX bytes:2680 (2.6 KB)

mininet> h1 ifconfig h1-eth0
h1-eth0   Link encap:Ethernet  HWaddr 32:0b:09:b9:f6:54
inet addr:10.0.0.65  Bcast:20.255.255.255  Mask:255.0.0.0
inet6 addr: fe80::8807:f7ff:fe92:6930/64 Scope:Link
UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
RX packets:54 errors:0 dropped:0 overruns:0 frame:0
TX packets:22 errors:0 dropped:1 overruns:0 carrier:0
collisions:0 txqueuelen:1000
RX bytes:5558 (5.5 KB)  TX bytes:2680 (2.6 KB)
```
The `show dhcp-server leases` command on the switch gives the following output:
```
switch# show dhcp-server leases

Expiry Time                MAC Address         IP Address Hostname and Client-id
-----------------------------------------------------------------------------
Tue Sep 22 00:16:10 2015   8a:07:f7:92:69:30   20.0.0.90  53_h2       *
Tue Sep 22 00:13:36 2015   32:0b:09:b9:f6:54   10.0.0.65  53_h1       *
```
##### Test fail criteria

## DHCP IPV4 static address pool configuration

### Configure DHCP IPV4 address pool for static address allocations and verify address assignments on hosts acting as DHCP clients

#### Objective
The test case checks if the DHCP IPV4 pool can be successfully created with specified static allocations of IPV4 addresses. The test case also validates address assignments on hosts acting as DHCP clients.

#### Requirements
- Virtual mininet test setup
- **FT file**: ops/tests/dhcp-tftp/test_dhcp_tftp_ft_static_ipv4_commands.py

#### Setup
##### Topology diagram
```
+------------------------------+
|                              |
|           Switch             |
|                              |
|                              |
+------------------------------+
       1                2
       |                |
       |                |
     eth1             eth1
 +-----------+    +-----------+
 |           |    |           |
 |  Host 1   |    |  Host 2   |
 |           |    |           |
 +-----------+    +-----------+
```

#### Description
This creates a DHCP IPV4 address pool for the specified static allocations and validates address assignments on the hosts acting as DHCP clients.
#### Test setup
Configure IP addresses for interface 1 and 2 on the switch.
```
switch# configure terminal
switch(config)# interface 1
switch(config-if)# no shutdown
switch(config-if)# ip address 10.0.0.1/8
switch(config-if)# exit
switch(config)# interface 2
switch(config-if)# no shutdown
switch(config-if)# ip address 20.0.0.1/8
switch(config-if)# end
```
Configure a DHCP IPV4 address pool on the DHCP server.
```
switch# configure terminal
switch(config)# dhcp-server
switch(config-dhcp-server)# static 10.0.0.65 match-mac-address 32:0b:09:b9:f6:54
switch(config-dhcp-server)# static 20.0.0.90 match-mac-address  8a:07:f7:92:69:30
switch(config-dhcp-server)# end
```
Configure DHCP clients (hosts 1 and 2) for the DHCP requests.
```
mininet> h1 ifconfig -a
mininet> h1 ip addr del 10.0.0.1/8 dev h1-eth0
mininet> h1 dhclient h1-eth0

mininet> h2 ifconfig -a
mininet> h2 ip addr del 10.0.0.2/8 dev h2-eth0
mininet> h2 dhclient h2-eth0
```
#### Test result criteria
##### Test pass criteria
The `show dhcp-server` command on a DHCP server gives the following output:
```
switch# show dhcp-server

DHCP dynamic IP allocation configuration
-----------------------------------------
Name   Start IP Address  End IP Address
-----------------------------------------
host1  10.0.0.1          10.0.0.100
host2  20.0.0.1          20.0.0.100


DHCP static IP allocation configuration
---------------------------------------
IP Address Hostname Client-id   Lease time  MAC-Address        Set tags
-----------------------------------------------------------------------
10.0.0.65   53_h1      *            60      32:0b:09:b9:f6:54      *
20.0.0.90   53_h2      *            60      8a:07:f7:92:69:30      *


DHCP options configuration
--------------------------
DHCP options are not configured.


DHCP Match configuration
------------------------
DHCP match is not configured.


DHCP BOOTP configuration
------------------------
DHCP BOOTP is not configured.
```

The `ifconfig` command on the hosts (DHCP clients) gives the following output:
```
mininet> h2 ifconfig h2-eth0
h2-eth0   Link encap:Ethernet  HWaddr 8a:07:f7:92:69:30
inet addr:20.0.0.90  Bcast:20.255.255.255  Mask:255.0.0.0
inet6 addr: fe80::8807:f7ff:fe92:6930/64 Scope:Link
UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
RX packets:54 errors:0 dropped:0 overruns:0 frame:0
TX packets:22 errors:0 dropped:1 overruns:0 carrier:0
collisions:0 txqueuelen:1000
RX bytes:5558 (5.5 KB)  TX bytes:2680 (2.6 KB)

mininet> h1 ifconfig h1-eth0
h1-eth0   Link encap:Ethernet  HWaddr 32:0b:09:b9:f6:54
inet addr:10.0.0.65  Bcast:20.255.255.255  Mask:255.0.0.0
inet6 addr: fe80::8807:f7ff:fe92:6930/64 Scope:Link
UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
RX packets:54 errors:0 dropped:0 overruns:0 frame:0
TX packets:22 errors:0 dropped:1 overruns:0 carrier:0
collisions:0 txqueuelen:1000
RX bytes:5558 (5.5 KB)  TX bytes:2680 (2.6 KB)
```

The `show dhcp-server leases` command on the switch (DHCP server) gives the following outpu:.
```
switch# show dhcp-server leases

Expiry Time               MAC Address       IP Address  Hostname and Client-id
------------------------------------------------------------------------------
Tue Sep 22 00:16:10 2015  8a:07:f7:92:69:30 20.0.0.90   53_h2       *
Tue Sep 22 00:13:36 2015  32:0b:09:b9:f6:54 10.0.0.65   53_h1       *
```
##### Test fail criteria
