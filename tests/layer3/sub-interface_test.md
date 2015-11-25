# Subinterfaces Feature Test Cases

## Contents
- [Verify the L3 reachability of the subinterface](#verify-the-l3-reachability-of-the-subinterface)
- [Verify the subinterface admin state](#verify-the-subinterface-admin-state)
- [Verify the L3 subinterfaces with the L2 VLAN](#verify-the-l3-subinterfaces-with-the-l2-vlan)
- [Verify the L2 VLANs with the L3 subinterface](#verify-the-l2-vlans-with-the-l3-subinterface)
- [Verify the routing on the L3 subinterfaces](#verify-the-routing-on-the-l3-subinterfaces)

##  Verify the L3 reachability of the subinterface

### Objective
Verify the reachability of the IP address set on the subinterface.

### Requirements
The requirements for this test case are:
 - OpenSwitch
 - VLAN aware host

### Setup
Connect OpenSwitch interface 1 to eth0 on the host.

#### Test setup
### Description
1. Create VLAN interface eth0.100 on the host.
2. Assign IP 192.168.1.2/24 to eth0.100.
3. Create subinterface 1.1 on interface 1.
4. Run `no shutdown` on 1.1.
5. Set Dot1Q encapsulation to 100 on 1.1.
6. Assign IP 192.168.1.1/24 to 1.1.
7. Ping 192.168.1.1 from the host.

### Test Result Criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### Test fail criteria
Ping fails.

##  Verify the subinterface admin state

### Objective
Verify the subinterface admin state.

### Requirements
The requirements for this test case are:
 - OpenSwitch
 - VLAN aware host

### Setup
Connect OpenSwitch interface 1 to eth0 on the host.

#### Test setup

### Description
1. Create VLAN interface eth0.100 on the host.
2. Assign IP 192.168.1.2/24 to eth0.100.
3. Run routing command on interface 1 on OpenSwitch.
4. Create subinterface 1.1 on interface 1.
5. Run `no shutdown` on 1.1.
6. Set Dot1Q encapsulation to 100 on 1.1.
7. Assign IP 192.168.1.1/24 to 1.1.
8. Ping 192.168.1.1 from the host.
9. Run `shutdown` on 1.1.
10. Ping 192.168.1.1 from the host.

### Test Result Criteria
Ping result.

#### Test pass criteria
Ping succeeds when the subinterface is enabled.
Ping fails when the subinterface is disabled.

#### Test fail criteria
Ping fails when the subinterface is enabled.

##  Verify the L3 subinterfaces with the L2 VLAN

### Objective

Verify the L3 subinterfaces with the L2 VLAN.

### Requirements
The requirements for this test case are:

 - ops 1
 - VLAN aware host 1
 - VLAN aware host 2
 - VLAN aware host 3

### Setup
1. Connect host 1 to ops 1 interface 1.
2. Connect host 2 to ops 1 interface 2.
3. Connect host 3 to ops 1 interface 3.

#### Test setup

### Description
1. Create VLAN 100 on ops 1 with interface 2 and interface 3.
2. Create VLAN interface eth0.100 on host.
3. Assign IP 192.168.1.2/24 to eth0.100.
4. Run routing command on interface 1 on OpenSwitch.
5. Create sub-interface 1.1 on interface 1.
6. Run `no shutdown` on 1.1.
7. Set dot1q encapsulation to 100 on 1.1.
8. Assign IP 192.168.1.1/24 to 1.1.
9. Ping 192.168.1.1 from the host.
10. Delete VLAN 100 on ops 1 with interface 2 and interface 3.
11. Ping 192.168.1.1 from the host.

### Test result criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### test fail criteria
Ping fails.

##  Verify the L2 VLANs with the L3 subinterface

### Objective

Verify the L2 VLANs with the L3 subinterface.

### Requirements
The requirements for this test case are:

 - OpenSwitch 1
 - VLAN aware host 1
 - VLAN aware host 2
 - VLAN aware host 3

### Setup
1. Connect host 1 to ops 1 interface 1.
2. Connect host 2 to ops 1 interface 2.
3. Connect host 3 to ops 1 interface 3.


#### Test setup

### Description
1. Create VLAN 100 on ops 1 with interface 2 and interface 3.
2. Create VLAN interface eth0.100 on the host.
3. Assign IP 192.168.1.2/24 to eth0.100.
4. Run routing command on interface 1 on OpenSwitch.
5. Create subinterface 1.1 on interface 1.
6. Run no shutdown on 1.1.
7. Set Dot1Q encapsulation to 100 on 1.1.
8. Assign IP 192.168.1.1/24 to 1.1.
9. Ping 192.168.1.1 from the host.
10. Put host 2 and host in the same subnet.
11. Ping host 2 from host 3 and vice-versa.

### Test result criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### Test fail criteria
Ping fails.

### Description
1.change the Dot1Q encapsulation to 200 on 1.1

### Test result criteria
ping result.

### Test pass criteria
ping  fails.

### Test fail criteria
ping pass.

##  Verify the routing on the L3 subinterfaces

### Objective

Verify the inter-VLAN routing on the L3 subinterfaces.

### Requirements

The requirements for this test case are:
 - OpenSwitch 1
 - OpenSwitch 2
 - VLAN aware host 1
 - VLAN aware host 2

### Setup
1. Connect OpenSwitch 1 interface 1 to ops 2 interface 3.
2. Connect host 1 to ops 2 interface 1.
3. Connect host 2 to ops 2 interface 2.


#### Test setp

### Description
1. On OpenSwitch 1, configure subinterface 1.100 (Set Dot1Q encapsulation to 100) with IP address 192.168.1.2/4.
2. On OpenSwitch 1, configure subinterface 1.200 (Set Dot1Q encapsulation to 200) with IP address 182.168.1.2/4.
3. On OpenSwitch 2, configure interface 3 as the trunk.
4. On ops 2, configure VLAN 100 and VLAN 200 on the trunk.
5. Add host 1 in VLAN 100 on OpenSwitch 2.
6. Configure subnet 192.168.1.1/24 on host 1 with 192.168.1.2 as default gateway.
7. Add host 2 in vlan 200 on OpenSwitch 2.
8. Configure subnet 182.168.1.1/24 on host 2 with 182.168.1.2 as default gateway.
9. Ping host 2 from host 1.

### Test result criteria
Ping result.

#### Test pass criteria
Ping succeeds.

#### Test fail criteria
Ping fails.

##  Verify the L3 reachability of the subinterface

### Objective
Verify the reachability of the IP address set on the subinterface.

### Requirements
The requirements for this test case are:
 - OpenSwitch
 - VLAN aware host

### Setup
Connect OpenSwitch interface 1 to eth0 on the host.


#### Test setup

### Description
1. Create VLAN interface eth0.100 on the host.
2. Assign IP 192.168.1.2/24 to eth0.100.
3. Create subinterface 1.1 on interface 1.
4. Run `no shutdown` on 1.1.
5. Set Dot1Q encapsulation to 100 on 1.1.
6. Assign IP 192.168.1.1/24 to 1.1.
7. Ping 192.168.1.1 from the host.
8. Remove Dot1Q encapsulation on 1.1.
9. Ping 192.168.1.1 from the host.

### Test Result Criteria
Ping result.

#### Test pass criteria
The ping succeeds when Dot1Q encapsulation is set.

#### Test fail criteria
The ping fails when there is no Dot1Q encapsulation.
