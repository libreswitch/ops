DHCP-TFTP Feature Test Cases
========

## Contents
   - [DHCP IPv4 dynamic address pool configuration](#dhcp-ipv4-dynamic-address-pool-configuration)
   - [DHCP IPV4 static address pool configuration](#dhcp-ipv4-static-address-pool-configuration)

## DHCP IPv4 dynamic address pool configuration

### Configure DHCP IPV4 address pool for dynamic address allocations and verify address assignments on hosts acting as DHCP clients

#### Objective
Test case checks if DHCP IPV4 pool can be successfully created with specified configuration range of IPV4 addresses. Test case validates address assignments on hosts acting as DHCP clients.

#### Requirements
- Virtual Mininet Test Setup
- **FT file**: ops/tests/dhcp-tftp/test_dhcp_tftp_ft_dynamic_ipv4_commands.py

#### Setup
##### Topology Diagram
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
Creates DHCP IPV4 address pool for specified range of addresses.Validates address assignments on hosts acting as DHCP clients.
#### Test Setup
Configure IP addresses for interface 1 and 2 on switch.
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
Configure DHCP IPV4 address pool on DHCP server.
```
switch# configure terminal
switch(config)# dhcp-server
switch(config-dhcp-server)# range host1 start-ip-address 10.0.0.1 end-ip-address 10.0.0.100
switch(config-dhcp-server)# range host2 start-ip-address 20.0.0.1 end-ip-address 20.0.0.100
switch(config-dhcp-server)# end
```
Configure DHCP clients (hosts 1 and 2) for DHCP requests.
```
mininet> h1 ifconfig -a
mininet> h1 ip addr del 10.0.0.1/8 dev h1-eth0
mininet> h1 dhclient h1-eth0

mininet> h2 ifconfig -a
mininet> h2 ip addr del 10.0.0.2/8 dev h2-eth0
mininet> h2 dhclient h2-eth0
```
#### Test Result Criteria
##### Test Pass Criteria
"show dhcp-server" command on DHCP server will give the following output.
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

"ifconfig" command on the hosts (DHCP clients) will give the following output.
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
"show dhcp-server leases" command on the switch will give the following output.
```
switch# show dhcp-server leases

Expiry Time                MAC Address         IP Address Hostname and Client-id
-----------------------------------------------------------------------------
Tue Sep 22 00:16:10 2015   8a:07:f7:92:69:30   20.0.0.90  53_h2       *
Tue Sep 22 00:13:36 2015   32:0b:09:b9:f6:54   10.0.0.65  53_h1       *
```
##### Test Fail Criteria

## DHCP IPV4 static address pool configuration

### Configure DHCP IPV4 address pool for static address allocations and verify address assignments on hosts acting as DHCP clients

#### Objective
Test case checks if DHCP IPV4 pool can be successfully created with specified static allocations of IPV4 addresses. Test case validates address assignments on hosts acting as DHCP clients.

#### Requirements
- Virtual Mininet Test Setup
- **FT file**: ops/tests/dhcp-tftp/test_dhcp_tftp_ft_static_ipv4_commands.py

#### Setup
##### Topology Diagram
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
Creates DHCP IPV4 address pool for specified static allocations.Validates address assignments on hosts acting as DHCP clients.
#### Test Setup
Configure IP addresses for interface 1 and 2 on switch.
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
Configure DHCP IPV4 address pool on DHCP server.
```
switch# configure terminal
switch(config)# dhcp-server
switch(config-dhcp-server)# static 10.0.0.65 match-mac-address 32:0b:09:b9:f6:54
switch(config-dhcp-server)# static 20.0.0.90 match-mac-address  8a:07:f7:92:69:30
switch(config-dhcp-server)# end
```
Configure DHCP clients (hosts 1 and 2) for DHCP requests.
```
mininet> h1 ifconfig -a
mininet> h1 ip addr del 10.0.0.1/8 dev h1-eth0
mininet> h1 dhclient h1-eth0

mininet> h2 ifconfig -a
mininet> h2 ip addr del 10.0.0.2/8 dev h2-eth0
mininet> h2 dhclient h2-eth0
```
#### Test Result Criteria
##### Test Pass Criteria
“show dhcp-server” command on DHCP server will give the following output.
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

"ifconfig" command on the hosts (DHCP clients) will give the following output.
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

“show dhcp-server leases” command on the switch (DHCP server) will give the following output.
```
switch# show dhcp-server leases

Expiry Time               MAC Address       IP Address  Hostname and Client-id
------------------------------------------------------------------------------
Tue Sep 22 00:16:10 2015  8a:07:f7:92:69:30 20.0.0.90   53_h2       *
Tue Sep 22 00:13:36 2015  32:0b:09:b9:f6:54 10.0.0.65   53_h1       *
```
##### Test Fail Criteria
