Ping Feature Test Cases
========

## Contents
   - [Verify the Connectivity between 2 switches configured with an IPv4 address](#verify-the-connectivity-between-2-switches-configured-with-an-IPv4-address)
   - [Verify the Connectivity between 2 switches configured with an IPv6 address](#verify-the-connectivity-between-2-switches-configured-with-an-IPv6-address)

## Verify the Connectivity between 2 switches configured with an IPv4 address
### Objective
To verify that the connectivity between 2 switches is successfully established and that the ping is also successful.
### Requirements
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton AS5712 switch docker instance.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with an IPv4 address.

### Setup
#### Topology diagram

```ditaa
     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  AS5712 switch     |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+
```

#### Test setup

### Test case 1.01
Ping from switch1 to switch2.
### Description
Verify that the ping from switch1 to switch2 is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.02
Ping from switch2 to switch1.
### Description
Verify that the ping from switch2 to switch1 is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch2 to switch1 is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.03
Ping from switch1 to switch2 with the data-fill parameter.
### Description
Verify that the ping from switch1 to switch2 with the data-fill parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the data-fill parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.04
Ping from switch1 to switch2 with the datagram-size parameter.
### Description
Verify that the ping from switch1 to switch2 with the datagram-size parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the datagram-size parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.05
Ping from switch1 to switch2 with the interval parameter.
### Description
Verify that the ping from switch1 to switch2 with the interval parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the interval parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.06
Ping from switch1 to switch2 with the repetitions parameter.
### Description
Verify that the ping from switch1 to switch2 with the repetitions parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the repetitions parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.07
Ping from switch1 to switch2 with the timeout parameter.
### Description
Verify that the ping from switch1 to switch2 with the timeout parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the timeout parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.08
Ping from switch1 to switch2 with the TOS parameter.
### Description
Verify that the ping from switch1 to switch2 with the TOS parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the TOS parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.09
Ping from switch1 to switch2 with the ip-option record-route parameter.
### Description
Verify that the ping from switch1 to switch2 with the ip-option record-route parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the ip-option record-route parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.10
Ping from switch1 to switch2 with the ip-option include-timestamp parameter.
### Description
Verify that the ping from switch1 to switch2 with the ip-option include-timestamp parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the ip-option include-timestamp parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 1.11
Ping from switch1 to switch2 with the ip-option include-timestamp-and-address parameter.
### Description
Verify that the ping from switch1 to switch2 with the ip-option include-timestamp-and-address parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the ip-option include-timestamp-and-address parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

## Verify the Connectivity between 2 switches configured with an IPv6 address
### Objective
To verify that the connectivity between 2 switches is successfully established and that ping6 is also successful.
### Requirements
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton AS5712 switch docker instance.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with an IPv6 address.

### Setup
#### Topology diagram

```ditaa
     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  AS5712 switch     |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+
```

#### Test setup

### Test case 2.01
Ping6 from switch1 to switch2.
### Description
Verify that the ping6 from switch1 to switch2 is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 2.02
Ping6 from switch2 to switch1.
### Description
Verify that the ping6 from switch2 to switch1 is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch2 to switch1 is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 2.03
Ping6 from switch1 to switch2 with the data-fill parameter.
### Description
Verify that the ping6 from switch1 to switch2 with the data-fill parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the data-fill parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 2.04
Ping6 from switch1 to switch2 with the datagram-size parameter.
### Description
Verify that the ping6 from switch1 to switch2 with the datagram-size parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the datagram-size parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 2.05
Ping6 from switch1 to switch2 with the interval parameter.
### Description
Verify that the ping6 from switch1 to switch2 with the interval parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the interval parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.

### Test case 2.06
Ping6 from switch1 to switch2 with the repetitions parameter.
### Description
Verify that the ping6 from switch1 to switch2 with the repetitions parameter is successful.
### Test result criteria
#### Test pass criteria
This test is effective if pinging from switch1 to switch2 with the repetitions parameter is successful and a zero packet loss is observed.
#### Test fail criteria
The ping does not reach the other side and a 100% packet loss is observed.