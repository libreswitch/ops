Traceroute Feature Test Cases
========

## Contents
   - [Verify the basic Traceroute](#verify-the-basic-traceroute)
   - [Verify the Traceroute with the option parameters](#verify-the-traceroute-with-the-option-parameters)
   - [Verify the Traceroute with the extended option parameters](#verify-the-traceroute-with-the-extended-option-parameters)
   - [Verify the basic Traceroute6](#verify-the-basic-traceroute6)
   - [Verify the Traceroute6 with the option parameters](#verify-the-traceroute6-with-the-option-parameters)

## Verify the basic Traceroute
### Objective
Verify the basic Traceroute from the switch3 configured with an IPv4 address to host1
### Requirements
The requirements for this test case are:
 - 3 switch
 - 1 workstation

### Setup
#### Topology Diagram
    ```ditaa

                    +---+----+        +--------+        +--------+
                    |        |        |        |        |        |
                    +switch1 +--------|switch2 |--------+switch3 +
                    |        |        |        |        |        |
                    +--------+        +--------+        +--------+
                         |
                         |
                         |
                    +----+---+
                    |        |
                    +  host1 +
                    |        |
                    +--------+
    ```
#### Test setup

### Test case 1.01
Test case checks the Traceroute diagnostic tool to trace the path from switch3 to host1 with the host1 IPv4 address.
### Description
From DUT CLI, execute command 'traceroute <destinationIP>'.
Where destination IP is a known responding IPv4 address on host1.
### Test result criteria
#### Test pass criteria
Traceroute from switch3 to host1 is successfull and CLI ouput shows the final hop as destination with a response time and NOT "*".
#### Test fail criteria
CLI ouput that shows the final hop as 'Host unreachable'.

### Test case 1.02
Test case checks the Traceroute diagnostic tool to trace the path from switch3 to host1 with host1's hostname as destination.
### Description
From DUT CLI, execute command 'traceroute <destination hostname>'.
Where destination is the known hostname of host1.
### Test result criteria
#### Test pass criteria
Traceroute from switch3 to host1 is successfull and CLI ouput that shows the final hop as destination with a response time and NOT "*".
#### Test fail criteria
CLI ouput that shows the final hop as 'Host unreachable'.


## Verify the Traceroute with the option parameters
### Objective
Verify the Traceroute with the option parameters from the switch3 configured with an IPv4 address to host1.
### Requirements
The requirements for this test case are:
 - 3 switch
 - 1 workstation

### Setup
#### Topology Diagram
    ```ditaa

                    +---+----+        +--------+        +--------+
                    |        |        |        |        |        |
                    +switch1 +--------|switch2 |--------+switch3 +
                    |        |        |        |        |        |
                    +--------+        +--------+        +--------+
                         |
                         |
                         |
                    +----+---+
                    |        |
                    +  host1 +
                    |        |
                    +--------+
    ```
#### Test setup

### Test case 2.01
Test case checks the Traceroute diagnostic tool to trace the path from switch3 to host1 with the maxttl parameter.
### Description
From DUT CLI, execute command `traceroute <destinationIP> maxttl <max_ttl>`.
Where destination IP is a known responding IPv4 address of host1 and max_ttl is greater than the number of hops required to reach the destination.
### Test result criteria
#### Test pass criteria
Traceroute from switch3 to host1 with the maxttl parameter is successfull and CLI ouput that shows the final hop as destination with a response time and NOT "*".
#### Test fail criteria
CLI ouput that shows the final hop as 'Host unreachable'.

### Test case 2.02
Test case checks the Traceroute diagnostic tool to trace the path from switch3 to host1 with the minttl parameter.
### Description
From DUT CLI, execute command 'traceroute <destinationIP> minttl <min_ttl>'.
Where destination IP is a known responding IPv4 address of host1 and min_ttl is less than the number of hops required to reach the destination.
### Test result criteria
#### Test pass criteria
Traceroute from switch3 to host1 with the minttl parameter is successfull and CLI ouput that shows the first hop is the target device and the destination is <minttl> hops away.
#### Test fail criteria
Device should display an invlaid input response as unknown command.

### Test case 2.03
Test case checks the Traceroute diagnostic tool to trace the path from switch3 to host1 with the dstport parameter.
### Description
From DUT CLI, execute command 'traceroute <destinationIP> dstport <dst_port>'.
Where destination IP is a known responding IPv4 address of host1 and for UDP tracing, specifies the destination port base traceroute will use (the dst_port number will be incremented by each probe).
### Test result criteria
#### Test pass criteria
Traceroute from switch3 to host1 with the dstport parameter is successfull and CLI ouput that shows the final hop as destination with a response time and NOT "*".
#### Test fail criteria
CLI ouput that shows the final hop as 'Host unreachable'.

### Test case 2.04
Test case checks the Traceroute diagnostic tool to trace the path from switch3 to host1 with the probes parameter.
### Description
From DUT CLI, execute command 'traceroute <destinationIP> probes <#probes>'.
Where destination IP is a known responding IPv4 address of host1 and #probes is less than the number of supported on the platform.
For this test it does not matter if the desntination device responds so long as there are intermediate hops that do respond.
### Test result criteria
#### Test pass criteria
Traceroute from switch3 to host1 with the probes parameter is successfull and CLI ouput that shows a response time for each probe packet.
Also, verify the "probes header in the results reflects the number submitted at the CLI".
#### Test fail criteria
Device should display an invlaid input response as unknown command.

### Test case 2.05
Test case checks the Traceroute diagnostic tool to trace the path from switch3 to host1 with the timeout parameter.
### Description
From DUT CLI, execute command 'traceroute <destinationIP> timeout <time_out>'.
Where destination IP is a known responding IPv4 address of host and Traceroute to destination should occur notifying timeout value.
### Test result criteria
#### Test pass criteria
Traceroute from switch3 to host1 with the timeout parameter is successfull and CLI ouput that shows a response time for each probe packet.
#### Test fail criteria
CLI ouput that shows the final hop as '*'.


## Verify the Traceroute with the extended option parameters
### Objective
Verify the Traceroute with the extended option parameters from the switch2 configured with an IPv4 address to host1.
### Requirements
The requirements for this test case are:
 - 3 switch
 - 1 workstation

### Setup
#### Topology Diagram
    ```ditaa

               +------------------------------------------------------+
               |                                                      |
               |    +---+----+        +--------+        +--------+    |
               |    |        |        |        |        |        |    |
               +----+switch1 +--------|switch2 |--------+switch3 +----+
                    |        |        |        |        |        |
                    +--------+        +--------+        +--------+
                         |
                         |
                         |
                    +----+---+
                    |        |
                    +  host1 +
                    |        |
                    +--------+
    ```
#### Test setup

### Test case 3.01
Test case checks the Traceroute diagnostic tool to trace the path from switch2 to host1  with the ip-option loose source route parameter.
### Description
From DUT CLI, execute command 'traceroute <destinationIP> ip-option loosesourceroute <loose_source_route_ip>'
Where destination IP is a known responding IPv4 address of host1 and loose_source_route_ip is the deafualt gateway to reach the destination.
### Test result criteria
#### Test pass criteria
Traceroute from switch2 to host1 with the ip-option loose source route parameter is successfull and CLI ouput that shows the default gateway as the loose source route hop.
#### Test fail criteria
CLI ouput that shows the default gateway as not the loose source route hop.


## Verify the basic Traceroute6
### Objective
Verify the basic Traceroute6 from the switch3 configured with an IPv6 address to host1.
### Requirements
The requirements for this test case are:
 - 3 switch
 - 1 workstation

### Setup
#### Topology Diagram
    ```ditaa

                    +---+----+        +--------+        +--------+
                    |        |        |        |        |        |
                    +switch1 +--------|switch2 |--------+switch3 +
                    |        |        |        |        |        |
                    +--------+        +--------+        +--------+
                         |
                         |
                         |
                    +----+---+
                    |        |
                    +  host1 +
                    |        |
                    +--------+
    ```
#### Test setup

### Test case 4.01
Test case checks the Traceroute6 diagnostic tool to trace the path from switch3 to host1 with the destination IPv6.
### Description
From DUT CLI, execute command 'traceroute6 <destinationIPv6>'.
Where destination IPv6 is a known responding IPv6 address of host1.
### Test result criteria
#### Test pass criteria
Traceroute6 from switch3 to host1 is successfull and CLI ouput that shows the final hop as destination with a response time and NOT "*".
#### Test fail criteria
CLI ouput that shows the final hop as 'Host unreachable'.

### Test case 4.02
Test case checks the Traceroute6 diagnostic tool to trace the path from switch3 to host1 with the destination hostname.
### Description
From DUT CLI, execute command 'traceroute6 <destination hostname>'.
Where destination host is a known responding hostname of host1.
### Test result criteria
#### Test pass criteria
Traceroute6 from switch3 to host1 is successfull and CLI ouput that shows the final hop as destination with a response time and NOT "*".
#### Test fail criteria
CLI ouput that shows the final hop as 'Host unreachable'.


## Verify the Traceroute6 with the option parameters
### Objective
Verify the Traceroute6 with the option parameters from the switch3 configured with an IPv6 address to host1.
### Requirements
The requirements for this test case are:
 - 3 switch
 - 1 workstation

### Setup
#### Topology Diagram
    ```ditaa

                    +---+----+        +--------+        +--------+
                    |        |        |        |        |        |
                    +switch1 +--------|switch2 |--------+switch3 +
                    |        |        |        |        |        |
                    +--------+        +--------+        +--------+
                         |
                         |
                         |
                    +----+---+
                    |        |
                    +  host1 +
                    |        |
                    +--------+
    ```
#### Test setup

### Test case 5.01
Test case checks the Traceroute6 diagnostic tool to trace the path from switch3 to host1 with the maxttl parameter.
### Description
From DUT CLI, execute command `traceroute6 <destinationIPv6> maxttl <max_ttl>`.
Where destination IPv6 is a known responding IPv6 address of host1 and max_ttl is greater than the number of hops required to reach the destination.
### Test result criteria
#### Test pass criteria
Traceroute6 from switch3 to host1 with the maxttl parameter is successfull and CLI ouput that shows the final hop as destination with a response time and NOT "*".
#### Test fail criteria
CLI ouput that shows the final hop as 'Host unreachable'

### Test case 5.02
Test case checks the Traceroute6 diagnostic tool to trace the path from switch3 to host1 with the dstport parameter.
### Description
From DUT CLI, execute command 'traceroute6 <destinationIPv6> dstport <dst_port>'.
Where destination IPv6 is a known responding IPv6 address of host1 and For UDP tracing, specifies the destination port base traceroute6 will use (the dst_port number will be incremented by each probe).
### Test result criteria
#### Test pass criteria
Traceroute6 from switch3 to host1 with the dstport parameter is successfull and CLI ouput that shows the final hop as destination with a response time and NOT "*".
#### Test fail criteria
CLI ouput that shows the final hop as 'Host unreachable'.

### Test case 5.03
Test case checks the Traceroute6 diagnostic tool to trace the path from switch3 to host1 with the probes parameter.
### Description
From DUT CLI, execute command 'traceroute6 <destinationIPv6> probes <#probes>'.
Where destination IPv6 is a known responding IPv6 address of host1 and #probes is less than the number supported on the platform.
For this test is does not matter if the desntination device responds so long as there are intermediate hops that do respond.
### Test result criteria
#### Test pass criteria
Traceroute6 from switch3 to host1 with the probes parameter is successfull and CLI ouput that shows a response time for each probe packet.
Also, verify the "probes header in the results reflects the number submitted at the CLI".
#### Test fail criteria
Device should display an invlaid input response as unknown command.

### Test case 5.04
Test case checks the Traceroute6 diagnostic tool to trace the path from switch3 to host1 with the timeout parameter.
### Description
From DUT CLI, execute command 'traceroute6 <destinationIPv6> timeout <time_out>'.
Where destination IPv6 is a known responding IPv6 address of host1 and Traceroute6 to destination should occur notifying timeout value.
### Test result criteria
#### Test pass criteria
Traceroute6 from switch3 to host1 with the timeout parameter is successfull and CLI ouput that shows a response time for each probe packet.
#### Test fail criteria
CLI ouput that shows the final hop as '*'.
