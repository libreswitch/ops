# UDP Broadcast Forwarder Feature Test Cases

## Contents

- [Verify UDP Broadcast Forwarder functionality](#verify-udp-broadcast-forwarder-functionality)
	- [Verify the UDP Broadcast forward-protocol for all supported UDP protocols](#verify-the-udp-broadcast-forward-protocol-for-all-supported-udp-protocols)
	- [Verify that the UDP Forwarder functionality is inactive when no UDP forward-protocols are configured.](#verify-that-the-udp-forwarder-functionality-is-inactive-when-no-udp-forward-protocols-are-configured)
	- [Verify the UDP Broadcast forward-protocol for configuration and unconfiguration multiple times for the same UDP protocol](#verify-the-udp-broadcast-forward-protocol-for-configuration-and-unconfiguration-multiple-times-for-the-same-udp-protocol)
	- [Verify the UDP Broadcast forward protocol for configuration and unconfiguration multiple times for the same UDP protocol during continious packet transmission](#verify-the-udp-broadcast-forward-protocol-for-configuration-and-unconfiguration-multiple-times-for-the-same-udp-protocol-during-continious-packet-transmission)
	- [Verify UDP broadcast forwarding with multiple servers for single a protocol](#verify-udp-broadcast-forwarding-with-multiple-servers-for-single-a-protocol)
	- [Verify UDP broadcast forwarding with a single server for multiple protocols](#verify-udp-broadcast-forwarding-with-a-single-server-for-multiple-protocols)
	- [Verify UDP broadcast forwarding with subnet broadcasting server](#verify-udp-broadcast-forwarding-with-subnet-broadcasting-server)
	- [Verify the UDP broadcast forwarding post reboot](#verify-the-udp-broadcast-forwarding-post-reboot)
	- [Verify the UDP broadcast forwarding functionality with huge traffic](#verify-the-udp-broadcast-forwarding-functionality-with-huge-traffic)
- [Failure cases](#failure-cases)
	- [Verify that the UDP Forwarder functionality is inactive when UDP broadcast forwarding is disabled](#verify-that-the-udp-forwarder-functionality-is-inactive-when-udp-broadcast-forwarding-is-disabled)
	- [Verify the UDP Forwarder functionality is inactive when the server is unreachable](#verify-the-udp-forwarder-functionality-is-inactive-when-the-server-is-unreachable)
	- [Verify the UDP Forwarder functionality when the connection between server and forwarder is flapping](#verify-the-udp-forwarder-functionality-when-the-connection-between-server-and-forwarder-is-flapping)
	- [Verify that the UDP Forwarder functionality is inactive when the server is in same interface](#verify-that-the-udp-forwarder-functionality-is-inactive-when-the-server-is-in-same-interface)

## Verify UDP Broadcast Forwarder functionality
### Objective
The purpose of this test is to validate UDP broadcast forwarder functionality when application client and application server are connected.

### Requirements
The requirements for this test case are:
 - Four (4) switches

### Setup
#### Topology diagram

```ditaa
                                    +-------------+
                                    |             |
                                    | Application |
                                    |  Server2    |
                                    |             |
                                    |             |
                                    |             |
                                    +------+------+
                                           |
                                           |
                                           |
                                           |
                                           |
                                           |
+--------------+                    +------+-------+                   +-------------+
|              |                    |              |                   |             |
|              |                    |              |                   | Application |
| Application  |                    |   UDP        |                   |  Server1    |
|   Client     +--------------------+   Forwarder  +-------------------+             |
|              |                    |              |                   |             |
|              |                    |              |                   |             |
+--------------+                    +--------------+                   +-------------+

```

### Verify the UDP Broadcast forward protocol for all supported UDP protocols
### Description
This test case will cover testing of UDP broadcast forwarding to all supported protocols.
The application client is generic and transmit the supported UDP protocol broadcast packet.
The application server1 is generic and runs all the supported UDP protocol servers.
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Check the connectivity between UDP forwarder, application server1 and the application client.
3. Configure Server1 IPv4 address as UDP forward-protocol for an UDP protocol on the UDP Forwarder.
4. Enable UDP broadcast forwarding globally on UDP forwarder using the command `ip udp-bcast-forward`.
5. Verify that the application client has started and transmits a broadcast packet.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is recieved at the respective UDP protocol server running on application server1.
#### Test fail criteria
The user verifies that the broadcast packet is not recieved at the respective UDP protocol server running on application server1.

### Verify that the UDP Forwarder functionality is inactive when no UDP forward protocols are configured
### Description
This test case will cover testing of UDP broadcast forwarding being inactive to all supported protocols.
The application client is generic and transmit the supported UDP protocol broadcast packet.
The application server1 is generic and runs all the supported UDP protocol servers.
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Check the connectivity between UDP forwarder, application server1 and the application client.
3. Disable UDP broadcast forwarding globally on UDP forwarder using the command `no ip udp-bcast-forward`.
4. Verify that the application client has started and transmits a broadcast packet.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is not recieved at the respective UDP protocol server running on application server1.
#### Test fail criteria
The user verifies that the broadcast packet is recieved at the respective UDP protocol server running on application server1.

### Verify the UDP Broadcast forward protocol for configuration and unconfiguration multiple times for the same UDP protocol
### Description
This test case will verify if the broadcast packets are not recieved at the UDP protocol server before configuring the forward protocol, and check if the packet is recieved when the forward protocol is configured and again when the configuration is removed, verify the packet reception stops.
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Check the connectivity between UDP forwarder, application server1 and the application client.
3. Enable UDP broadcast forwarding globally on UDP forwarder using the command `ip udp-bcast-forward`.
4. Do not configure any UDP forward protocols.
5. Verify that the application client has started and transmits a broadcast packet but this should not be recieved at the resepective server, stop the transmission of broadcast packets.
6. Configure an UDP forward protocol on the UDP forwarder.
7. Verify that the application client has started and transmits a broadcast packet again and the packets are recieved at the resepective server, stop the transmission of broadcast packets.
8. Unconfigure the UDP forward protocol on the UDP forwarder.
9. Verify that the application client has started and transmits a broadcast packet but this should not be recieved at the resepective server.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is recieved at the respective UDP protocol server running on application server1 only when the UDP forward protocol is configured on the UDP forwarder.
#### Test fail criteria
The user verifies that the broadcast packet is recieved at the respective UDP protocol server running on application server1 even when the UDP forward protocol is not configured on the UDP forwarder.

### Verify the UDP Broadcast forward protocol for configuration and unconfiguration multiple times for the same UDP protocol during continious packet transmission
### Description
In this test case continuous broadcast packets are transmitted from the client, Initially there is no configuration on the forwarder, so verify if the packets are recieved at the server and then enable a forward protocol and verify the packet reception at the server, now disable the forward protocol and verify that the packets are not recieved anymore at the server.
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Check the connectivity between UDP forwarder, application server1 and the application client.
3. Enable UDP broadcast forwarding globally on UDP forwarder using the command `ip udp-bcast-forward`.
4. Do not configure any UDP forward protocols.
5. Verify that the application client has started and transmits broadcast packets continously but this should not be recieved at the resepective server.
6. Configure an UDP forward protocol on the UDP forwarder.
7. Verify that the broadcast packets are recieved at the resepective server.
8. Unconfigure the UDP forward protocol on the UDP forwarder.
9. Verify that the broadcast packet reception has stopped at the resepective server as soon as the unconfiguration is done.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is recieved at the respective UDP protocol server running on application server1 only when the UDP forward protocol is configured on the UDP forwarder.
#### Test fail criteria
The user verifies that the broadcast packet is recieved at the respective UDP protocol server running on application server1 even when the UDP forward protocol is not configured on the UDP forwarder.

### Verify UDP broadcast forwarding with multiple servers for single a protocol
### Description
1. Configure an IPv4 address on an application client, UDP forwarder, application Server1(used as dns server), and the application Server2(used as dns server).
2. Check the connectivity between UDP forwarder, application server1, application server2 and the application client.
3. Configure server1 IPv4 address as UDP forward protocol with dns UDP port on the UDP Forwarder.
4. Enable UDP broadcast forwarding globally on UDP forwarder using the command `ip udp-bcast-forward`.
5. Verify that the application client has started and transmits a dns request packet.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is recieved at the application serve1 and not recieved at the server2.
#### Test fail criteria
The user verifies that the broadcast packet is not recieved at the application server1.

### Verify UDP broadcast forwarding with a single server for multiple protocols
### Description
1. Configure an IPv4 address on an application client, UDP forwarder, application Server1. Make sure this application server1 internally runs multiple UDP protocol servers like dns and snmp.
2. Check the connectivity between UDP forwarder, application server1, and the application client.
3. Configure server1 IPv4 address as UDP forward protocol with dns and snmp UDP ports on the UDP Forwarder.
4. Enable UDP broadcast forwarding globally on UDP forwarder using the command `ip udp-bcast-forward`.
5. Verify that the application client has started and transmits a dns request packet.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is recieved at the dns server and not recieved at the snmp server.
#### Test fail criteria
The user verifies that the broadcast packet is not recieved at the dns server.

### Verify UDP broadcast forwarding with subnet broadcasting server
### Description
1. Configure an IPv4 address on an application client, UDP forwarder, application Server1.
2. Check the connectivity between UDP forwarder, application server1, application server2 and the application client.
3. Configure subnet broadcast IPv4 address of the interface on which the server is connected as UDP forward-protocol on the UDP Forwarder.
4. Enable UDP broadcast forwarding globally on UDP forwarder using the command `ip udp-bcast-forward`.
5. Verify that the application client has started and transmits a broadcast packet.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is recieved at the server which is part of different interface.
#### Test fail criteria
The user verifies that the broadcast packet is not recieved at the server.

### Verify the UDP broadcast forwarding post reboot
### Description
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Check the connectivity between UDP forwarder, application server1 and the application client.
3. Configure Server1 IPv4 address as UDP forward protocol for an UDP protocol on the UDP Forwarder.
4. Enable UDP broadcast forwarding globally on UDP forwarder using the command `ip udp-bcast-forward`.
5. Verify that the application client has started and transmits a packet.
6. Perform reboot of the UDP forwarder.
7. Verify that the application client transmit a broadcast packet.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is recieved at the respective UDP protocol server running on application server1 post reboot.
#### Test fail criteria
The user verifies that the broadcast packet is not recieved at the respective UDP protocol server running on application server1 post reboot.

## Verify the UDP broadcast forwarding functionality with huge traffic
### Description
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Check the connectivity between UDP forwarder, application server1 and the application client.
3. Configure server IPv4 address as UDP forward protocol on the UDP Forwarder.
4. Verify that the application client has started to transmit huge traffic of 500 broadcast packets.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is recieved at the server.
#### Test fail criteria
The user verifies that the broadcast packet is not recieved at the server.

## Failure cases
### Objective
The purpose of this test is to validate possible failure cases and corner cases when using UDP Forwarder.

### Requirements
The requirements for this test case are:
 - Four (4) switches

### Setup
#### Topology diagram

```ditaa

                                    +-------------+
                                    |             |
                                    |             |
                                    | Application |
                                    |   Server2   |
                                    |             |
                                    |             |
                                    +------+------+
                                           |
                                           |
                                           |
                                           |
                                           |
                                           |
+--------------+                    +------+-------+                   +-------------+
|              |                    |              |                   |             |
|              |                    |              |                   |             |
| Application  |                    |    UDP       |                   | Application |
|   Client     +--------------------+  Forwarder   +-------------------+  Server1    |
|              |                    |              |                   |             |
|              |                    |              |                   |             |
+--------------+                    +--------------+                   +-------------+

```

### Verify that the UDP Forwarder functionality is inactive when UDP broadcast forwarding is disabled
### Description
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Check the connectivity between UDP forwarder, application server1 and the application client.
3. Configure server IPv4 address as UDP forward protocol on the UDP Forwarder.
4. Disable UDP broadcast forwarding globally on UDP forwarder using the command `no ip udp-bcast-forward`.
5. Verify that the application client has started and transmits a broadcast packet.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is not recieved at the server.
#### Test fail criteria
The user verifies that the broadcast packet is recieved at the server.

### Verify the UDP Forwarder functionality is inactive when the server is unreachable
### Description
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Change the interface state of the server to down, and then connect the UDP Forwarder and the application client using the appropriate CLI commands.
3. Configure server IPv4 address as UDP forward protocol on the UDP Forwarder.
4. Verify that the application client has started and transmits a broadcast packet.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is not recieved at the server.
#### Test fail criteria
The user verifies that the broadcast packet is recieved at the server.

### Verify the UDP Forwarder functionality when the connection between server and forwarder is flapping
### Description
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Check the connectivity between UDP forwarder, application server1 and the application client.
3. Configure server IPv4 address as UDP forward protocol on the UDP Forwarder.
4. Verify that the application client has started and transmits a broadcast packet.
5. Toggle the forwarder and server interface to up and down multiple times.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is recieved at the server only during interface between server and forwarder is up.
#### Test fail criteria
The user verifies that the broadcast packet is not recieved at the server only during interface between server and forwarder is up.

## Verify that the UDP Forwarder functionality is inactive when the server is in same interface
### Description
1. Configure an IPv4 address on an application client, UDP forwarder, and the application Server1.
2. Check the connectivity between UDP forwarder, application server1 and the application client.
3. Configure server IPv4 address as UDP forward protocol on the UDP Forwarder in the same interface where the client is connected and recieves the broadcast packets.
4. Verify that the application client has started and transmits a broadcast packet.

### Test results criteria
#### Test pass criteria
The user verifies that the broadcast packet is not recieved at the server.
#### Test fail criteria
The user verifies that the broadcast packet is recieved at the server.
