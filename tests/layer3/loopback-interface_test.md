# Loopback Interface Feature Test Cases

## Contents
- [Verify the L3 reachability of the loopback interface](#verify-the-l3-reachability-of-the-loopback-interface)
- [Verify the L3 non-reachability of the loopback interface](#verify-the-l3-non-reachability-of-the-loopback-interface)

##  Verify the L3 reachability of the loopback interface

### Objective
Verify the reachability of the IP address set on the loopback interface.

### Requirements
The requirements for this test case are:
 - OpenSwitch
 - host

### Setup
Connect OpenSwitch interface 1 to eth0 on the host.

#### Test setup
### Description
1. Assign IP 192.168.1.2/24 to eth0 on the host.
2. Create a loopback interface.
3. Assign IP 192.168.1.1/24 to loopback interface 1.
4. Ping 192.168.1.1 from the host.

### Test result criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### Test fail criteria
Ping fails.

##  Verify the L3 non-reachability of the loopback interface

### Objective
Verify the non-reachability of the IP address set on the loopback interface.

### Requirements
The requirements for this test case are:
 - OpenSwitch
 - host

### Setup
Connect OpenSwitch interface 1 to eth0 on the host.

#### Test setup
### Description
1. Assign IP 192.168.1.2/24 to eth0 on the host.
2. Create loopback interface 1.
3. Assign IP 192.168.1.1/24 to loopback interface 1.
4. Ping 192.168.1.1 from the host.
5. Remove loopback interface 1.
6. Ping 192.168.1.1 from the host.

### Test result criteria
Ping result.

#### Test pass criteria
Ping fails.

#### Test fail criteria
Ping succeeds.
