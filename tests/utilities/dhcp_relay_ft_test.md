# DHCP Relay Feature Test Cases

## Contents

- [DHCP relay functionality](#dhcp-relay-functionality)
    - [Verify basic DHCP relay functionality with one server](#verify-basic-dhcp-relay-functionality-with-one-server)
    - [Verify basic DHCP relay functionality with two servers](#verify-basic-dhcp-relay-functionality-with-two-servers)
    - [Verify basic DHCP relay functionality with two servers and make one server unreachable](#verify-basic-dhcp-relay-functionality-with-two-servers-and-make-one-server-unreachable)
    - [Verify that DHCP relay functionality is inactive when DHCP relay is disabled](#verify-that-dhcp-relay-functionality-is-inactive-when-dhcp-relay-is-disabled)
    - [Verify DHCP client requests with and without helper address configuration](#verify-dhcp-client-requests-with-and-without-helper-address-configuration)
    - [Verify helper address configuration in the same subnet as relay interface](#verify-helper-address-configuration-in-the-same-subnet-as-relay-interface)
    - [Verify the DHCP relay functionality when IP routing is enabled or disabled](#verify-the-dhcp-relay-functionality-when-ip-routing-is-enabled-or-disabled)
    - [Verify the DHCP relay functionality when packet is received with hop count set to maximum value](#verify-the-dhcp-relay-functionality-when-packet-is-received-with-hop-count-set-to-maximum-value)
- [DHCP relay option 82 test cases](#dhcp-relay-option-82-test-cases)
    - [Verify that proper remote id is added when interface on which client request is received is configured with multiple IP addresses](#verify-that-proper-remote-id-is-added-when-interface-on-which-client-request-is-received-is-configured-with-multiple-ip-addresses)
    - [Verify the DHCP relay agent behavior on DHCP client request packets when DROP policy is enabled](#verify-the-dhcp-relay-agent-behavior-on-dhcp-client-request-packets-when-drop-policy-is-enabled)
    - [Verify the DHCP relay agent behavior on DHCP server response packets when DROP policy is enabled](#verify-the-dhcp-relay-agent-behavior-on-dhcp-server-response-packets-when-drop-policy-is-enabled)
    - [Verify the DHCP relay agent behavior on DHCP client request packets when KEEP policy is enabled](#verify-the-dhcp-relay-agent-behavior-on-dhcp-client-request-packets-when-keep-policy-is-enabled)
    - [Verify the DHCP relay agent behavior on DHCP server response packets when KEEP policy is enabled](#verify-the-dhcp-relay-agent-behavior-on-dhcp-server-response-packets-when-keep-policy-is-enabled)
    - [Verify the DHCP relay agent behavior on DHCP client request packets when REPLACE policy is enabled](#verify-the-dhcp-relay-agent-behavior-on-dhcp-client-request-packets-when-replace-policy-is-enabled)
    - [Verify the DHCP relay agent behavior on DHCP server response packets when REPLACE policy is enabled](#verify-the-dhcp-relay-agent-behavior-on-dhcp-server-response-packets-when-replace-policy-is-enabled)
    - [Verify the DHCP relay agent behavior on server response when server responses are not being validated by switch policy](#verify-the-dhcp-relay-agent-behavior-on-server-response-when-server-responses-are-not-being-validated-by-switch-policy)
    - [Verify the DHCP relay drops the packets unconditionally based on the IP address if option 82 field already exists in the client DHCP packet](#verify-the-dhcp-relay-drops-the-packets-unconditionally-based-on-the-ip-address-if-option-82-field-already-exists-in-the-client-dhcp-packet)
    - [Verify that the DHCP packet will be dropped uncondtionally if option 82 fields already exists in the client DHCP packet](#verify-that-the-dhcp-packet-will-be-dropped-uncondtionally-if-option-82-fields-already-exists-in-the-client-dhcp-packet)
    - [Verify the DHCP relay does not add or replace the option 82 field with ip address if option fields already exists in the client DHCP packet](#verify-the-dhcp-relay-does-not-add-or-replace-the-option-82-field-with-ip-address-if-option-fields-already-exists-in-the-client-dhcp-packet)
    - [Verify the DHCP relay does not add or replace the option 82 field if option fields already exists in the client DHCP packet](#verify-the-dhcp-relay-does-not-add-or-replace-the-option-82-field-if-option-fields-already-exists-in-the-client-dhcp-packet)
    - [Verify the DHCP relay functionality with option 82 enabled when the relay receives huge amount of DHCP request from the client](#verify-the-dhcp-relay-functionality-with-option-82-enabled-when-the-relay-receives-huge-amount-of-dhcp-request-from-the-client)
- [DHCP relay bootp gateway test cases](#dhcp-relay-bootp-gateway-test-cases)
    - [Verify that default gateway works when no gateway is specified](#verify-that-default-gateway-works-when-no-gateway-is-specified)
    - [Verify that set gateway is the interface that gets DHCP addresses](#verify-that-set-gateway-is-the-interface-that-gets-dhcp-addresses)
    - [Verify that removal of set gateway IP address on a multinetted interface will cause the lowest address to become the default gateway](#verify-that-removal-of-set-gateway-ip-address-on-a-multinetted-interface-will-cause-the-lowest-address-to-become-the-default-gateway)


## DHCP relay functionality
### Objective
The purpose of this test is to validate DHCP relay functionality when client and server are connected.

### Requirements
The requirements for this test case are:
 - Three (3) switches
 - One (1) workstation

### Setup
#### Topology diagram

```ditaa
                                    +-------------+
                                    |             |
                                    |             |
                                    |  Server2    |
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
|              |                    |    DHCP      |                   |             |
|   DHCP       |                    |    Relay     |                   |  Server1    |
|   Client     +--------------------+    Agent     +-------------------+             |
|              |                    |              |                   |             |
+--------------+                    +--------------+                   +-------------+

```
#### Test setup

### Verify basic DHCP relay functionality with one server
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Configure the DHCP Server to assign IP address to the client.
4. Request DHCP address on client and verify that the DHCP relay agent relays DHCP packets to client/server.
5. Verify that the DHCP client has received an IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if the DHCP client recieves an IP address.
#### Test fail criteria
This test fails if a the DHCP client does not recieve an IP address.

### Verify basic DHCP relay functionality with two servers
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP addresses as helper addresses on the DHCP relay agent.
3. Assign secondary ip address to the interface connecting relay and server1.
4. Configure the DHCP Servers to assign IP address to the client.
5. Request DHCP address on client and verify that the DHCP relay agent receives response from server1 via secondary ip.
6. Verify that the DHCP client has received an IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if the DHCP client recieves an IP address.
#### Test fail criteria
This test fails if a the DHCP client does not recieve an IP address.

### Verify basic DHCP relay functionality with two servers and make one server unreachable
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP addresses as helper addresses on the DHCP relay agent.
3. delete the static route from server2 to dhcp client.
4. Configure the DHCP Servers to assign IP address to the client.
5. Request DHCP address on client and verify that the DHCP relay agent receives response from server1.
6. Verify that the DHCP client has received an IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if the DHCP client recieves an IP address.
#### Test fail criteria
This test fails if a the DHCP client does not recieve an IP address.

### Verify that DHCP relay functionality is inactive when DHCP relay is disabled
### Description
This is a manual test. Configuration is below:
1. Configure an IP address on DHCP client, DHCP relay agent, DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on DHCP relay agent.
3. Disable DHCP relay globally on DHCP relay using the`no dhcp-relay` command.
4. Configure the DHCP server to assign IP address to the Client.
5. Request DHCP address on client.
6. Verify that the DHCP Client has not received an IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if the DHCP client does not recieve an IP address.
#### Test fail criteria
This test fails if the DHCP client recieves an IP address.

### Verify DHCP client requests with and without helper address configuration
### Description
This is a manual test. Configuration is below:
1. Configure an IP address on DHCP client, DHCP relay agent, DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on DHCP relay agent.
3. Configure the DHCP server to assign IP address to the Client.
4. Request DHCP address on client.
5. Verify that the DHCP Client has received an IP address.
6. Remove server IP address as helper addresses on DHCP relay agent.
7. Request DHCP address on client.
8. Verify that the DHCP Client has not received an IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify helper address configuration in the same subnet as relay interface
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on DHCP relay agent. Helper address is in the same subnet as relay interface.
3. Configure the DHCP server to assign IP address to the Client.
4. Request DHCP address on client.
5. Verify that the DHCP Client has received an IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if the DHCP client recieves an IP address.
#### Test fail criteria
This test fails if a the DHCP client does not recieve an IP address.

## Verify the DHCP relay functionality when IP routing is enabled or disabled
### Description
This is a manual test. Configuration is below:
1. Configure an IP address on DHCP client, DHCP relay agent, DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on DHCP relay agent.
3. Disable IP routing on relay interface using the`no routing` command.
4. Configure the DHCP server to assign IP address to the Client.
5. Request DHCP address on client.
6. Verify that the DHCP Client has not received an IP address.
7. Enable Ip routing on relay interface using `routing` command.
8. Configure IP address on relay and configure server IP address as helper addresses on DHCP relay agent.
9. Request DHCP address on client
10. Verify that the DHCP Client has received an IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

## Verify the DHCP relay functionality when packet is received with hop count set to maximum value
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Configure the DHCP Server to assign IP address to the client.
4. Request DHCP address on client (send packet with hop count set to maximum value).
5. Verify that the DHCP relay agent drops the packet.
6. Verify that the DHCP client has not received an IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if the DHCP client does not recieve an IP address.
#### Test fail criteria
This test fails if the DHCP client recieves an IP address.

## DHCP relay option 82 test cases

### Objective
The purpose of this test is to validate DHCP relay option 82 functionality when client and server are connected.
All test cases are manual test cases.

### Requirements
The requirements for this test case are:
 - two (2) switches
 - One (1) workstation

### Setup
#### Topology diagram

```ditaa

+--------------+                    +--------------+                   +-------------+
|              |                    |              |                   |             |
|              |                    |    DHCP      |                   |             |
|   DHCP       |                    |    Relay     |                   |  Server1    |
|   Client     +--------------------+    Agent     +-------------------+             |
|              |                    |              |                   |             |
+--------------+                    +--------------+                   +-------------+

```
#### Test setup

### Verify that proper remote id is added when interface on which client request is received is configured with multiple IP addresses
This test will test the DHCP relay agent to add the proper remote ID to the DHCP option 82 when interface on which client request is received is configured with multiple IP addresses.
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Create an interface on DHCP relay with two IP addresses
interface 100
(int-100)ip address 10.10.10.1/24
(int-100)ip address 10.10.20.1/24
2. Enable dhcp-relay option 82 to replace interface ip, with no server responses validation using `dhcp-relay option 82 replace ip` command.
3. On DHCP client , request a DHCP ip address (10.10.10.x) subnet, by setting the giaddr(relay agent IP address)
to the address of the DHCP relay in the client interface for the desired subnet. ex: 10.10.10.1
4. Do not add option 82 information on original request.
5. Using Sniffer validate ethernet packets going/coming from DHCP server. DHCP relay should add Option 82 to DHCP request to server appending remote ID the IP address of the multinetted interface.
6. Verify Client recieves IP address.
7. Delete the configured IP address and configure a new IP.
8. Verify in the successive request the new IP is used as remote ID.

### Test results criteria
#### Test pass criteria
This test succeeds if the DHCP client recieves an IP address.
#### Test fail criteria
This test fails if a the DHCP client does not recieve an IP address.

### Verify the DHCP relay agent behavior on DHCP client request packets when DROP policy is enabled
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable dhcp-relay option 82 with drop policy using `dhcp-relay option 82 drop ip` command.
4. Request DHCP address from client in a configuration with single dhcp relay agent to DHCP server. DHCP request packet has:
    - giaddr = NULL
    - option 82 = NULL
5. Use sniffer to verify that Option 82 is added with interface IP as remote ID field to DHCP client request (single option 82) and then forwarded to DHCP server.
DHCP relay should process the client request and server response. DHCP client should receive an IP.
6. Use ixia or other means to send DHCP request packets to DHCP relay with:
    - giaddr != NULL
    - option 82 = NULL
7. Use sniffer to verify that Option 82 is added as per configuration without changing the giaddr field by the DHCP relay and then forwarded to DHCP server.
8. With DROP policy enabled, use ixia or other means to send DHCP request packets to DHCP relay with:
    - giaddr = NULL
    - Option 82 != NULL
9. Verify using sniffer that relay agent drops the packet.
10. With DROP policy enabled, use ixia or other means to send DHCP request packets to DHCP relay with:
    - giaddr != NULL
    - option 82 != NULL
10. Verify using sniffer that dhcp relay agent drops the packet.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay agent behavior on DHCP server response packets when DROP policy is enabled
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Configure DHCP relay agent to NO validation on server responses using `no dhcp-relay option 82 validate` command.
4. Enable dhcp-relay option 82 to DROP packets and validate server responses using `dhcp-relay option 82 drop ip validate` command.
5. Request DHCP address from client in a standard DHCP server setup/configuration.
6. Verify Client recieves IP address.
7. Use ixia or other means to send DHCP packets to DHCP relay that would trigger a drop policy on validation of server responses.
8. Verify using sniffer that server response packets are received on DHCP relay and not forwarded to DHCP client.
DHCP relay agent is dropping them (drop counter should reflect this).
9. Repeat above 4-8 using Option 82 configured with - MAC ADDRESS, same behavior should be observed.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay agent behavior on DHCP client request packets when KEEP policy is enabled
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable dhcp-relay option 82 with KEEP policy using `dhcp-relay option 82 keep ip` command.
4. Request DHCP address from client in a configuration with single dhcp relay agent to DHCP server. DHCP request packet has:
    - giaddr = NULL
    - option 82 = NULL
5. Use sniffer to verify that Option 82 is added with interface IP as remote ID field to DHCP client request(single option 82) and then forwarded to DHCP server.
DHCP relay should process the client request and server response. DHCP client should receive an IP.
6. Use ixia or other means to send DHCP request packets to dhcp relay agent with:
    - giaddr != NULL and
    - option 82 = NULL
7. Verify using sniffer that DHCP relay agent is adding option 82 fields as per configuration, without changing 'giaddr' and forward to DHCP server.
8. Use ixia or other means to send DHCP request packets to DHCP relay agent with:
    - giaddr = NULL
    - Option 82 != NULL
7. Verify using sniffer that DHCP relay drops the packet.
8. Use ixia or other means to send DHCP request packets to DHCP relay agent with:
    - giaddr != NULL
    - Option 82 != NULL
9. Verify using sniffer that client request packets are forwarded unchanged to DHCP server.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay agent behavior on DHCP server response packets when KEEP policy is enabled
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Configure DHCP relay agent to NO validation on server responses using `no dhcp-relay option 82 validate` command.
4. Enable dhcp-relay option 82 to append interface IP, with no server responses validation using `dhcp-relay option 82 keep ip` command.
5. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP
    - Circuit ID = DHCP relay agent's circuit IP
6. Verify using sniffer that server response packets are received on DHCP relay agent and forwarded to interface after removing Option 82 field.
7. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP and
    - No option 82
9. Verify using sniffer that server response packets are received on DHCP relay agent and forwarded to interface unchanged.
10. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP and
    - multiple option 82 field and at least one matches DHCP relay agent circuit ID AND remote ID
11. Verify using sniffer that server response packets are received on DHCP relay agent and forwarded to port after removing all option 82 fields.
12. Use ixia or other means to send DHCP server response packets to DHCP relay agent with:
    - giaddr ! = DHCP relay agent's IP and (giaddr NOT = DHCP relay agent's IP)
    - single/multiple option 82 field and at least one matches DHCP relay agent's circuit ID AND remote ID
13. Verify using sniffer that DHCP relay agent will not relay server response packets and DHCP relay counters will remain unaffected.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay agent behavior on DHCP client request packets when REPLACE policy is enabled
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable dhcp-relay option 82 to append interface IP, with no server responses validation using `dhcp-relay option 82 replace ip` command.
4. Request DHCP address from client in a configuration with single dhcp relay agent to DHCP server. DHCP request packet has:
    - giaddr = NULL
    - option 82 = NULL
5. Use sniffer to verify that Option 82 is added with interface IP as remote ID field to DHCP client request (single option 82) and then forwarded to DHCP server.
DHCP relay agent should process the client request and server response. DHCP client should receive an IP.
6. Use ixia or other means to send DHCP request packets to DHCP relay agent with:
    - giaddr != NULL and
    - Option 82 = NULL
7. Verify using sniffer that DHCP relay agent is adding option 82 filds as per configuration, without changing 'giaddr' and forward to DHCP server.
8. With REPLACE policy enabled, use ixia or other means to send DHCP request packets to DHCP relay agent with:
    - giaddr = NULL
    - Option 82 != NULL
9. Verify using sniffer that DHCP relay agent drops the packet.
10. With REPLACE policy enabled, use ixia or other means to send DHCP request packets to DHCP relay agent with:
    - giaddr != NULL and
    - Option 82 != NULL
11. Verify using sniffer that DHCP relay agent replaces option 82 fields as per configuration without changing 'giaddr' and forwarded to DHCP-server.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay agent behavior on DHCP server response packets when REPLACE policy is enabled
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Configure DHCP relay agent to NO validation on server responses using `no dhcp-relay option 82 validate` command.
4. Enable dhcp-relay option 82 to append interface IP, with no server responses validation using `dhcp-relay option 82 replace ip` command.
5. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP and
    - Circuit ID = DHCP relay agent circuit IP
6. Verify using sniffer that server response packets are received on DHCP relay agent and forwarded to interface after removing Option 82 field.
7. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP and
    - No option 82
8. Verify using sniffer that server response packets are received on DHCP relay agent and forwarded to interface unchanged.
9. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP and
    - multiple option 82 field and at least one matches DHCP relay agent circuit ID AND remote ID
10. Verify using sniffer that server response packets are received on DHCP relay agent and forwarded to port after removing all option 82 fields.
11. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr ! = DHCP relay agent's IP and
    - single/multiple option 82 field and at least one matches DHCP relay agent circuit ID AND remote ID
12. Verify using sniffer that DHCP relay agent will not relay server response packets and DHCP relay counters will remain unaffected.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay agent behavior when validation on DHCP server responses is enabled
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable dhcp-relay option 82 to validate server responses using `dhcp-relay option 82 validate` command.
4. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = NULL and
    - No option 82
5. Verify using sniffer that server response packets are dropped on DHCP relay agent. DHCP relay agent is dropping them (drop counter should reflect this = no counter increment).
6. Clear the value of counters.
7. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent IP and
    - No option 82
8. Verify using sniffer that server response packets are dropped on DHCP relay agent. DHCP relay agent is dropping them (drop counter should reflect this).
9. Clear the value of counters.
10. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agentS IP address and
    - Circuit ID != DHCP relay agent curcuit ID
    - Remote ID != DHCP relay agent remote ID
11. Verify using sniffer that server response packets are dropped on DHCP relay agent. DHCP relay agent is dropping them (drop counter should reflect this).
12. Clear the value of counters.
13. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP address and
    - Circuit ID = DHCP relay agent curcuit ID
    - Remote ID != DHCP relay agent remote ID
14. Verify using sniffer that server response packets are dropped on DHCP relay agent. DHCP relay agent is dropping them (drop counter should reflect this).
15. Clear the value of counters.
16. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP address and
    - Circuit ID = DHCP relay agent curcuit ID
    - Remote ID = DHCP relay agent remote ID
17. Verify using sniffer that server response packets are forwarded to interface. DHCP relay agent counter should reflect this.
18. Clear the value of counters.
19. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr != DHCP relay agent's IP address (NOT equal) and
    - Circuit ID = DHCP relay agent curcuit ID
    - Remote ID = DHCP relay agent remote ID
20. Verify using sniffer that DHCP relay server response packets. No counters are incremented. Packet goes to host stack.
21. Clear the value of counters.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay agent behavior on server response when server responses are not being validated by switch policy
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable dhcp-relay option 82 to validate server responses `dhcp-relay option 82 validate` command.
4. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = NULL and
    - No option 82
5. Verify using sniffer that server response packets are dropped on DHCP relay agent. DHCP relay agent is dropping them (drop counter should reflect this = no counter increment).
6. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP and
    - No option 82
7. Verify using sniffer that server response packets are forwarded to interface. DHCP relay agent counter should reflect this (valid server responses).
8. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP address and
    - Circuit ID != DHCP relay agent curcuit ID
    - Remote ID != DHCP relay agent remote ID
9. Verify using sniffer that server response packets are forwarded to interface. DHCP relay agent counter should reflect this (valid server responses).
10. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP address and
    - Circuit ID = DHCP relay agent curcuit ID
    - Remote ID != DHCP relay agent remote ID
11. Verify using sniffer that server response packets are forwarded to interface. DHCP relay agent counter should reflect this (valid server responses).
12. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr = DHCP relay agent's IP address and
    - Circuit ID = DHCP relay agent curcuit ID
    - Remote ID = DHCP relay agent remote ID
13. Verify using sniffer that server response packets are forwarded to interface. DHCP relay agent counter should reflect this (valid server responses).
14. Use ixia or other means to send DHCP server responses packets to DHCP relay agent with:
    - giaddr != DHCP relay agent's IP address and
    - Circuit ID = DHCP relay agent curcuit ID
    - Remote ID = DHCP relay agent remote ID
15. Verify using sniffer that DHCP relay server response packets. No counters are incremented. Packet goes to host stack.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay drops the packets unconditionally based on the IP address if option 82 field already exists in the client DHCP packet
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable option 82 to drop unconditionally using `dhcp-relay option 82 drop ip` command.
4. Request DHCP address on client.
5. Using sniffer verify that DHCP relay agent drops the packet from the DHCP client, if the client has the option 82 within the DHCP packet and IP address as Sub Option 2.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify that the DHCP packet will be dropped uncondtionally if option 82 fields already exists in the client DHCP packet
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable option 82 to drop mac using `dhcp-relay option 82 drop mac` command.
4. Request DHCP address on client.
5. Using sniffer verify that DHCP relay agent will drop the packet from the client, if the client has the option 82 within the DHCP packet and MAC address as Sub Option 2.
6. DHCP relay agent keeps DHCP packet with option 82 intact and adds DHCP relay agent's IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay does not add or replace the option 82 field with ip address if option fields already exists in the client DHCP packet
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable option 82 to keep ip using `dhcp-relay option 82 keep ip` command.
4. Request DHCP address on client.
5. Using sniffer verify DHCP relay agent will not change any DHCP packets with option 82, and IP Address as Sub Option 2.
6. DHCP relay agent keeps DHCP packet with option 82 intact and adds DHCP relay agent's IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay does not add or replace the option 82 field if option fields already exists in the client DHCP packet
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable option 82 to keep using `dhcp-relay option 82 keep` command.
4. Request DHCP address on client.
5. Using sniffer verify DHCP relay agent will not change any DHCP packets with option 82.
6. Verify DHCP relay agent keeps DHCP packet with option 82 intact.

### Test results criteria
#### Test pass criteria
This test succeeds if all the above steps are successful.
#### Test fail criteria
This test fails if any of the above steps fail.

### Verify the DHCP relay functionality with option 82 enabled when the relay receives huge amount of DHCP request from the client
### Description
1. Configure an IP address on DHCP client, DHCP relay agent, and the DHCP Server. Add static routes and check connectivity from DHCP client to DHCP server.
2. Configure server IP address as helper addresses on the DHCP relay agent.
3. Enable option 82 on the DHCP relay agent.
4. Configure the DHCP Server to assign IP address to the client.
5. Request DHCP address on client and verify that the DHCP relay agent relays DHCP packets to client/server.
6. Verify that the DHCP client has received an IP address.

### Test results criteria
#### Test pass criteria
This test succeeds if the DHCP client recieves an IP address.
#### Test fail criteria
This test fails if a the DHCP client does not recieve an IP address.

## DHCP relay bootp gateway test cases
### Objective
The purpose of this test is to validate DHCP relay bootp gateway functionality.

### Requirements
The requirements for this test case are:
 - one (1) switch
 - One (1) workstation

### Setup
#### Topology diagram

```ditaa

+--------------+                    +--------------+
|              |                    |              |
|              |                    |    DHCP      |
|   DHCP       |                    |    Relay     |
|   Client     +--------------------+    Agent     |
|              |                    |              |
+--------------+                    +--------------+

```
#### Test setup

### Verify that default gateway works when no gateway is specified
This test will verify that the lowest IP address on a multinetted interface will be used for the default gateway.
### Description
1. Create a multinetted interface on relay and make sure the lowest IP subnet is used for DHCP addresses.
2. Request DHCP address on client.
2. Use ethereal to capture packets and make sure lowest address is the relay gateway.
3. Verify in the DHCP packets which address is the gateway.

### Test results criteria
#### Test pass criteria
This test succeeds if lowest address on an interface is the relay gateway.
#### Test fail criteria
This test fails if lowest address on an interface is not the relay gateway.

### Verify that set gateway is the interface that gets DHCP addresses
This test will verify that the set gateway IP address on a multinetted interface will be used for the relay gateway.
### Description
1. Create a multinetted interface and make sure the set gateway IP subnet is used for DHCP addresses.
2. Set the gateway for the multinetted interface using `interface 3 ip bootp-gateway <IPaddress>` command.
Choose an address from the ones configured on interface 3 that is not the lowest.
3. Request DHCP address on client.
4. Use "Wireshark" to capture packets and make sure set gateway address is the relay gateway.
5. Verify in the DHCP packets which address is the gateway.(check within the DHCP portion of the packet, NOT the relay address used to forward the packet).

### Test results criteria
#### Test pass criteria
This test succeeds if set address on an interface is the relay gateway.
#### Test fail criteria
This test fails if set address on an interface is not the relay gateway.

### Verify that removal of set gateway IP address on a multinetted interface will cause the lowest address to become the default gateway
### Description
1. Create a multinetted interface and make sure the set gateway IP subnet is used for DHCP addresses.
2. Set the gateway for the multinetted interface using `interface 3 ip bootp-gateway <IPaddress>` command.
Choose an address from the ones configured on interface 3 that is not the lowest.
3. Request DHCP address on client.
4. Use "Wireshark" to capture packets and make sure set gateway address is the relay gateway.
5. Verify in the DHCP packets which address is the gateway.
6. Disconnect DHCP Relay and remove gateway from multinetted interface using `no interface 3 ip bootp-gateway <IP address>` command.
7. Use Ethereal to capture packets and make sure lowest IP address is the relay gateway.
8. Re-add the removed gateway on interface using `interface 3 ip bootp-gateway <ip address>` command.
9. Now physically remove the GW address from the interface using `no interface 3 ip address <ip address>` command.
10. Verify that next time client refreashes lease it should obtain address from lowest remaining IP address on interface.

### Test results criteria
#### Test pass criteria
This test succeeds if lowest address on an interface is the relay gateway.
#### Test fail criteria
This test fails if lowest address on an interface is not the relay gateway.
