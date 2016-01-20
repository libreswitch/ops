Ping Feature Test Cases
========

## Contents

- [Verify the basic Ping utility](#verify-the-basic-ping-utility)
- [Verify the Ping utility with optional parameters](#verify-the-ping-utility-with-optional-parameters)
- [Verify the Ping utility with the extended option parameters](#verify-the-ping-utility-with-the-extended-option-parameters)
- [Verify the basic Ping6 utility](#verify-the-basic-ping6-utility)
- [Verify the Ping6 utility with the optional parameters](#verify-the-ping6-utility-with-the-optional-parameters)
- [Verify the Ping utility failure cases](#verify-the-ping-utility-failure-cases)
- [Verify the Ping6 utility failure cases](#verify-the-ping6-utility-failure-cases)

## Verify the basic Ping utility
### Objective
Verify that the basic ping from Switch2 to Host1 works. Host1 is configured with an IPv4 address.

### Requirements
The requirements for this test case are:
 - Two (2) switches
 - One (1) workstation

### Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 1.01
This test checks that when using the Ping utility, pinging from switch2 to Host1 with the Host1 IPv4 address is successful.
### Description
From Switch2 CLI, execute the `ping <destinationIP>` command where the destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from Switch2 to Host1 is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`

## Verify the Ping utility with optional parameters
### Objective
Verify that when using the Ping utility, pinging with optional parameters from Switch2 to Host1 works. Host1 is configured with an IPv4 address.
### Requirements
The requirements for this test case are:
 - Two (2) switches
 - One (1) workstation

### Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 2.01
This test checks that when using the Ping utility, pinging from Switch2 to Host1 is successful with the data-fill parameter.
### Description
From Switch2 CLI, execute the `ping <destinationIP> data-fill <character>`command where the destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from Switch2 to Host1 with the data-fill parameter is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`

### Test case 2.02
This test checks that when using the Ping utility, pinging from Switch2 to Host1 is successful with the datagram-size parameter.
### Description
From the Switch2 CLI, execute the `ping <destinationIP> datagram-size <size>`command where the destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from Switch2 to Host1 with the datagram-size parameter is successful and the CLI output shows a zero packet loss.
Also, verify that the packet with the appropriate byte size `<size>` is sent to the destination.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`

### Test case 2.03
This test case checks that when using the Ping utility, pinging from Switch2 to Host1 with the interval parameter is successful.
### Description
From the Switch2 CLI, execute the `ping <destinationIP> interval <time>` command where destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from Switch2 to Host1 with the interval parameter is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`


### Test case 2.04
This test case checks that when using the Ping utility, pinging from Switch2 to Host1 with the repetition parameter is successful.
### Description
From the Switch2 CLI, execute the `ping <destinationIP> repetition <count>`command where the destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from Switch2 to Host1 with the repetition parameter is successful and the CLI output shows a zero packet loss.
Also, verify that the `<count>` number of packets are sent to the destination.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`


### Test case 2.05
This test case checks that the ping is successful from Switch2 to Host1 with the timeout parameter.
### Description
From the Switch2 CLI, execute the `ping <destinationIP> timeout <time_out>` command where the destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from Switch2 to Host1 with the timeout parameter is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`

### Test case 2.06
This test case checks that pinging from Switch2 to Host1 with the TOS parameter is successful.
### Description
From the Switch2 CLI, execute the `ping <destinationIP> tos <number>` command where destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from Switch2 to Host1 with the TOS parameter is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`

## Verify the Ping utility with the extended option parameters
### Objective
Verify that when using the Ping utility, ping with extended option parameters from Switch2 to Host1 works. Host1 is configured with an IPv4 address.
### Requirements
The requirements for this test case are:
 - Two (2) switches
 - One (1) workstation

## Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 3.01
This test case checks that when using the Ping utility, pinging from Switch2 to Host1 is successful with the ip-option record-route parameter.
### Description
From the Switch2 CLI, execute the `ping <destinationIP> ip-option record-route` command where the destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from Switch2 to Host1 with the ip-option record-route parameter is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `network is unreachable`
- `packet loss is more than 0%`

### Test case 3.02
This test case checks that the ping is successful from Switch2 to Host1 with the ip-option include-timestamp parameter.
### Description
From the Switch2 CLI, execute the `ping <destinationIP> ip-option include-timestamp` command where destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, ping from Switch2 to Host1 with the ip-option include-timestamp parameter is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `network is unreachable`
- `packet loss is more than 0%`

### Test case 3.03
This test case checks that pinging from Switch2 to Host1 is successful with the ip-option include-timestamp-and-address parameter.
### Description
From the Switch2 CLI, execute the `ping <destinationIP> ip-option include-timestamp-and-address` command where the destination IP is an IPv4 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping utility, pinging from Switch2 to Host1 with the `ip-option include-timestamp-and-address` parameter is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `network is unreachable`
- `packet loss is more than 0%`

## Verify the basic Ping6 utility
### Objective
Verify that the basic ping6 from Switch2 to Host1 works. Host1 is configured with an IPv6 address.

### Requirements
The requirements for this test case are:
 - Two (2) switches
 - One (1) workstation
### Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 4.01
This test case checks using the Ping6 utility, pinging from Switch2 to Host1 with the Host1 IPv6 address is successful.
### Description
From the Switch2 CLI, execute the `ping6 <destinationIP>` command where the destination IP is an IPv6 address configured on Host1.
### Test result criteria
#### Test pass criteria
Using the Ping6 utility, pinging from Switch2 to Host1 is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `network is unreachable`
- `packet loss is more than 0%`

## Verify the Ping6 utility with the optional parameters
### Objective
Using the Ping6 utility, verify that pinging from Switch2 to Host1 with optional parameters works. Host1 is configured with an IPv6 address.
### Requirements
The requirements for this test case are:
 - Two (2) switches
 - One (1) workstation
### Setup
#### Topology diagram
    ```ditaa
                +---------+            +----------+          +-----------+
                |         |            |          |          |           |
                |         |            |          |          |           |
                | Host1   +------------+ Switch1  +----------+ Switch2   |
                |         |            |          |          |           |
                |         |            |          |          |           |
                +---------+            +----------+          +-----------+
    ```
#### Test setup

### Test case 5.01
This test case checks that when using the Ping6 utility, pinging from Switch2 to Host1 is successful with the data-fill parameter is successful.
### Description
From the Switch2 CLI, execute the `ping6 <destinationIP> data-fill <character>`command where destination IP is an IPv6 address configured on Host1.
### Test result criteria
#### Test pass criteria
Using the Ping6 utility, pinging from Switch2 to Host1 with the data-fill parameter is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`

### Test case 5.02
This test case checks that when using the Ping6 utility, pinging from Switch2 to Host1 with the datagram-size parameter is successful.
### Description
From the Switch2 CLI, execute the `ping6 <destinationIP> datagram-size <size>`command where the destination IP is an IPv6 address configured on Host1.
### Test result criteria
#### Test pass criteria
Using the Ping6 utility, pinging from Switch2 to Host1 with the datagram-size parameter is successful and the CLI output shows a zero packet loss.
Also, verify that the packet with the appropriate byte size `<size>` is sent to the destination.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`

### Test case 5.03
The test case checks that when using the Ping6 utility, pinging from Switch2 to Host1 with the interval parameter is successful.
### Description
From Switch2 CLI, execute the `ping6 <destinationIP> interval <time>`command where the destination IP is an IPv6 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping6 utility, pinging from Switch2 to Host1 with the interval parameter is successful and the CLI output shows a zero packet loss.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`

### Test case 5.04
This test case checks that when using the Ping6 utility, pinging from Switch2 to Host1 with the repetition parameter is successful.
### Description
From the Switch2 CLI, execute the `ping6 <destinationIP> repetition <count>` command where the destination IP is an IPv6 address configured on Host1.
### Test result criteria
#### Test pass criteria
When using the Ping6 utility, pinging from Switch2 to Host1 with the repetition parameter is successful and the CLI output shows a zero packet loss.
Also, verify that the number of packets `<count>` are sent to the destination.
#### Test fail criteria
This test fails if the Switch2 CLI output shows one of the following messages:

- `host is unreachable`
- `packet loss is more than 0%`

## Verify the Ping utility failure cases
### Objective
Verify the different ping failure cases
### Requirements
One switch is required for this test.

### Setup
#### Topology diagram
     ```ditaa
                +-------+
                |       |
                |Switch2|
                |       |
                +-------+
     ```
#### Test setup

### Test case 6.01
This test case checks that when using the Ping utility,  pinging from Switch2 to an unreachable IPv4 address fails.
### Description
From the switch2 CLI, execute the `ping <destinationIP>` command where the destination IP is an unreachable IPv4 address.
Where destination IP is an unreachable IPv4 address.
### Test result criteria
#### Test pass criteria
The Switch2 CLI output displays the following:

`Network is unreachable.`
#### Test fail criteria
The ping is successful and the packet loss is 0%.

### Test case 6.02
This test case checks that when using the Ping utility, pinging from switch2 to a wrong IPv4 address that has the same subnet mask as configured on switch2 fails.
### Description
From the switch1 CLI, execute the `ping <destinationIP>` command where the destination IP is the wrong IPv4 address that has the same subnet mask as configured on Switch2.
### Test result criteria
#### Test pass criteria
The Switch2 CLI output displays the following:

`Destination Host Unreachable.`
#### Test fail criteria
The ping is successful and the packet loss is 0%.

### Test case 6.03
This test case checks that when using the Ping utility, pinging from Switch2 to an unknown host fails.
### Description
From the switch2 CLI, execute the `ping <hostname>` command where `hostname` is an unknown host name.
### Test result criteria
#### Test pass criteria
The Switch2 CLI output displays the following:
`unknown host`
#### Test fail criteria
The ping is successful and the packet loss is 0%.

## Verify the Ping6 utility failure cases
### Objective
Using the Ping6 utility, verify the different ping6 failure cases.
### Requirements
One switch is required for this test.


### Setup
#### Topology diagram
     ```ditaa
                +-------+
                |       |
                |Switch2|
                |       |
                +-------+
     ```
#### Test setup

### Test case 7.01
This test case checks that when using the Ping6 utility, pinging from switch2 to an unreachable IPv6 address fails.
### Description
From the switch2 CLI, execute the`ping6 <destinationIP>`command where the destination IP is an unreachable IPv6 address.
### Test result criteria
#### Test pass criteria
The switch2 CLI output displays the following:

`Network is unreachable.`
#### Test fail criteria
Using the Ping6 utility, pinging is successful and the packet loss is 0%.

### Test case 7.02
This test case checks that when using the Ping6 utility, pinging from switch1 to an unknown host fails.
### Description
From the DUT CLI, execute the `ping6 <hostname>` command where `<hostname>`is an unknown host name.
### Test result criteria
#### Test pass criteria
The Switch2 CLI output displays the following:
`unknown host`
#### Test fail criteria
The ping6 is successful and the packet loss is 0%.
