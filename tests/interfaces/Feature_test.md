Feature Test Cases
==================

Physical Interfaces

 [TOC]

##  Enable/Disable Interface ##
### Objective ###
Verify that enable and disabling interfaces behaves as expected.
### Requirements ###
The requirements for this test case are:
 - RTL
 - 1 switch
 - 3 workstations
### Setup ###

#### Topology Diagram ####

```ditaa
                 switch                ws1
          +------------------+        +------+
          |                  |        |      |
          |             eth0 +--------+eth1  |
          |                  |        |      |
          |   1         2    |        +------+
          +---+---------+----+
              |         |
              |         |
          +---+---+  +--+----+
          | eth1  |  | eth1  |
          |       |  |       |
          |       |  |       |
          +-------+  +-------+
           ws2         ws3
```

#### Test Setup ####

### Description ###
  Enable/Disable Interface

  ```
  Create two interfaces, one up and one down.
  Verify that status is correct and pings fail.
  Bring up the other interface.
  Verify that status is correct and pings succeed.
  Shutdown the interface.
  Verify that status is correct and pings fail.

  dut01: vtysh cmd:     configure terminal
  dut01: vtysh cmd:     vlan 10
  dut01: vtysh cmd:     name v10
  dut01: vtysh cmd:     no shutdown
  dut01: vtysh cmd:     exit
  dut01: vtysh cmd:     interface 2
  dut01: vtysh cmd:     no routing
  dut01: vtysh cmd:     vlan access 10
  dut01: vtysh cmd:     no shutdown
  dut01: vtysh cmd:     interface 1
  dut01: vtysh cmd:     no routing
  dut01: vtysh cmd:     vlan access 10
  dut01: shell cmd:     ovs-vsctl show interface 1
       : verify   :     admin_state="down"
  wrkston02: shell cmd: ping <to wrkston03 ip addr>
       : verify   :     ping fails
  dut01: vtysh cmd:     no shutdown
  dut01: shell cmd:     ovs-vsctl show interface 1
       : verify   :     admin_state="up"
  wrkston01: shell cmd: ping <to wrkston02 ip addr>
       : verify   :     ping succeeds
  dut01: vtysh cmd:     shutdown
  dut01: shell cmd:     ovs-vsctl show interface 1
       : verify   :     admin_state="down"
  wrkston02: shell cmd: ping <to wrkston03 ip addr>
       : verify   :     ping fails
  ```

### Test Result Criteria ###
```
interface:admin_state is used, either "down" or "up"
ping is used to determine link is up and working.
```
#### Test Pass Criteria ####
```
interface:admin_state = "up" or "down" when appropriate
pings succeed or fail when appropriate
```
#### Test Fail Criteria ####

##  Autonegotiation ##
### Objective ###
Verify autonegotiation config changes behave as expected.
### Requirements ###
The requirements for this test case are:
 - RTL
 - 1 switch
 - 3 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
                 switch                ws1
          +------------------+        +------+
          |                  |        |      |
          |             eth0 +--------+eth1  |
          |                  |        |      |
          |   1         2    |        +------+
          +---+---------+----+
              |         |
              |         |
          +---+---+  +--+----+
          | eth1  |  | eth1  |
          |       |  |       |
          |       |  |       |
          +-------+  +-------+
           ws2         ws3
```

#### Test Setup ####

### Description ###
  Autonegotiation

  ```
  Bring up two intefaces, with default autoneg (not configured)
  Verify autoneg set to "on" and pings succeed
  Disable autoneg
  Verify admin_state is donw, error=autoneg_required, and pings fails
  Enable autoneg
  Verify autoneg set to "on" and pings succeed
  Remove autoneg (no autoneg), it goes back to default (on)
  Verify autoneg set to "on" and pings succeed

  dut01: vtysh cmd:     configure terminal
  dut01: vtysh cmd:     vlan 10
  dut01: vtysh cmd:     name v10
  dut01: vtysh cmd:     no shutdown
  dut01: vtysh cmd:     exit
  dut01: vtysh cmd:     interface 2
  dut01: vtysh cmd:     no routing
  dut01: vtysh cmd:     vlan access 10
  dut01: vtysh cmd:     no shutdown
  dut01: vtysh cmd:     interface 1
  dut01: vtysh cmd:     no routing
  dut01: vtysh cmd:     vlan access 10
  dut01: vtysh cmd:     no shutdown
  dut01: shell cmd:     ovs-vsctl show interface 1
       : verify   :     hw_intf_config:autoneg="on"
  wrkston02: shell cmd: ping <to wrkston03 ip addr>
       : verify   :     ping succeeds
  dut01: vtysh cmd:     autonegotiation off
  dut01: shell cmd:     ovs-vsctl show interface 1
       : verify   :     admin_state="down"
       : verify   :     error="autoneg_required"
  wrkston01: shell cmd: ping <to wrkston02 ip addr>
       : verify   :     ping fails
  dut01: vtysh cmd:     autonegotiation on
  dut01: shell cmd:     ovs-vsctl show interface 1
       : verify   :     admin_state="up"
       : verify   :     hw_intf_config:autoneg="on"
  wrkston02: shell cmd: ping <to wrkston03 ip addr>
       : verify   :     ping succeeds
  dut01: vtysh cmd:     no autonegotiation
  dut01: shell cmd:     ovs-vsctl show interface 1
       : verify   :     admin_state="up"
       : verify   :     hw_intf_config:autoneg="on"
  wrkston02: shell cmd: ping <to wrkston03 ip addr>
       : verify   :     ping succeeds
  ```

### Test Result Criteria ###
```
interface:admin_state is used, either "down" or "up"
interface:error is used, should be "autoneg_required" when autoneg=no
ping is used to determine link is up and working.
```
#### Test Pass Criteria ####
```
interface:admin_state = "up" or "down" when appropriate
interface:error = "autoneg_required" when autoneg=no
pings succeed or fail when appropriate
```
#### Test Fail Criteria ####

##  Statistics ##
### Objective ###
Verify interface statistics change as expected.
### Requirements ###
The requirements for this test case are:
 - RTL
 - 1 switch
 - 3 workstations
### Setup ###

#### Topology Diagram ####
```ditaa
                 switch                ws1
          +------------------+        +------+
          |                  |        |      |
          |             eth0 +--------+eth1  |
          |                  |        |      |
          |   1         2    |        +------+
          +---+---------+----+
              |         |
              |         |
          +---+---+  +--+----+
          | eth1  |  | eth1  |
          |       |  |       |
          |       |  |       |
          +-------+  +-------+
           ws2         ws3
```

#### Test Setup ####
### Description ###
  ```
  Verify Interface Statistics

  Bring up two interfaces
  Collect baseline stats
  Send pings from ws2 to ws3
  Verify stats are as expected
  Send pings from ws3 to ws2
  Verify stats are as expected

  dut01: vtysh cmd:     configure terminal
  dut01: vtysh cmd:     vlan 10
  dut01: vtysh cmd:     name v10
  dut01: vtysh cmd:     no shutdown
  dut01: vtysh cmd:     exit
  dut01: vtysh cmd:     interface 2
  dut01: vtysh cmd:     no routing
  dut01: vtysh cmd:     vlan access 10
  dut01: vtysh cmd:     no shutdown
  dut01: vtysh cmd:     interface 1
  dut01: vtysh cmd:     no routing
  dut01: vtysh cmd:     vlan access 10
  dut01: vtysh cmd:     no shutdown
  dut01: vtysh cmd:     exit
  dut01: vtysh cmd:     exit
  dut01: vtysh cmd:     show interface 1
  dut01: vtysh cmd:     show interface 2
       : verify   :     <collect baseline for stats>
  wrkston02: shell cmd: ping <to wrkston03 ip addr>
       : action   :     sleep(5)
  dut01: vtysh cmd:     show interface 1
  dut01: vtysh cmd:     show interface 2
       : verify   :     stats updated correctly
  wrkston03: shell cmd: ping <to wrkston02 ip addr>
       : action   :     sleep(5)
  dut01: vtysh cmd:     show interface 1
  dut01: vtysh cmd:     show interface 2
       : verify   :     stats updated correctly
       : action   :     sleep(10)
  dut01: vtysh cmd:     show interface 1
  dut01: vtysh cmd:     show interface 2
       : verify   :     stats not updated
  ```

### Test Result Criteria ###
```
Use vtysh output for "show interface x"
Expect stats to increase appropriate due to pings
```
#### Test Pass Criteria ####
```
counters increase for rx/tx packets, bytes
counters do not change for rx/tx input errors, drops; rx crc; tx collisions
```
#### Test Fail Criteria ####
