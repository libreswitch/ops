# Intervlan Routing Feature Test Cases

## Contents

- [Verify the Intervlan ping utility](#verify-the-intervlan-ping-utility)

## Verify the Intervlan ping utility
### Objective
Verify that the basic ping between hosts connected via switch works for both IPv4/IPv6. Hosts adn switch are configured with an IPv4/IPv6 address.

### Requirements
The requirements for this test case are:
 - One (1) switch
 - Four (4) workstations

### Setup
#### Topology diagram


                                       +----------+
                                       |          |
                                       |  Host2   |
                                       |          |
                                       +----+-----+
                                            |
                                            |
                +---------+            +----+-----+          +-----------+
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+  Host3    |
                |         |            |          |          |           |
                +---------+            +-----+----+          +-----------+
                                             |
                                             |
                                       +-----+----+
                                       |          |
                                       |  Host4   |
                                       |          |
                                       +----------+


#### Test setup
### Test case 1.01
This test verifies the basic ping between hosts connected via switch works for both IPv4/IPv6. Hosts and switch are configured with an IPv4/IPv6 address.
### Description
- Switch is connnected to 4 hosts via 4 interfaces (interface1, interface2, interface3, interface4) which are enabled. Interface vlans are enabled & configured on this 4 interfaces. Ipv4 & IPv6 addresses are configured for these interface vlans.
- Each host is configured with IPv4 & IPv6 address, and ip routes.
- Verify IPv4 and IPv6 ping test from host1 to host3.
- Verify IPv4 and IPv6 ping test from host1 to host4.
- Verify IPv4 and IPv6 ping test from host1 to host2.
- Verify ping test to host3 and host4 from host1.
- Verify L3 statistics on L3 interface.
- Unconfigure VLANs.
- Test ping from Host1 to Host2 and Host1 to Host3


### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from one host to another is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the any host shows below messages:

- `host is unreachable`
- `packet loss is more than 0%`
