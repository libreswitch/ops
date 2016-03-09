# Physical Interface Feature Test Cases

## Contents

- [Enable/Disable Interface](#enabledisable-interface)
- [Autonegotiation](#autonegotiation)
- [Statistics](#statistics)

##  Enable/Disable interface
### Objective
Verify that enable and disabling interfaces behave as expected.
### Requirements
The requirements for this test case are:
- RTL
- 1 switch
- 3 workstations

### Setup

#### Topology diagram

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

### Description
Create two interfaces, one up and one down. Verify that status is correct and pings fail. Bring up the other interface. Verify that status is correct and pings succeed. Shutdown the interface. Verify that status is correct and pings fail.

  ```
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

### Test result criteria
Interface: admin_state is either "down" or "up" and ping is used to determine if the link is up and working.

#### Test pass criteria
Interface: admin_state = "up" or "down" when appropriate and pings succeed.

#### Test fail criteria
Interface: admin_state = "up" or "down" when appropriate and pings fail.

##  Autonegotiation
### Objective
Verify autonegotiation configuration changes behave as expected.
### Requirements
The requirements for this test case are:
- RTL
- 1 switch
- 3 workstations

### Setup

#### Topology diagram
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

#### Test setup

### Description
Bring up two intefaces, with default autoneg (not configured). Verify autoneg is set to "on" and pings succeed.
Disable autoneg, verify admin_state is down, error=autoneg_required, and pings fail.
Enable autoneg, verify autoneg is set to "on", and pings succeed.
Remove autoneg (no autoneg) and it goes back to default (on). Verify autoneg is set to "on" and pings succeed.

```
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

### Test result criteria
Interface: admin_state is either "down" or "up".
Interface: error is used and should be "autoneg_required" when autoneg=no.
Ping is used to determine if the link is up and working.

#### Test pass criteria
Interface: admin_state = "up" or "down" when appropriate and pings succeed.
Interface: error = "autoneg_required" when autoneg=no and pings succeed.

#### Test fail criteria
Interface: admin_state = "up" or "down" when appropriate and pings fail.
Interface: error = "autoneg_required" when autoneg=no and pings fail.

## Statistics
### Objective
Verify interface statistics change as expected.
### Requirements
The requirements for this test case are:
- RTL
- 1 switch
- 3 workstations

### Setup

#### Topology diagram
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

### Description
Bring up two interfaces and collect baseline statistics. Send pings from ws2 to ws3 and verify that the statistics are as expected. Send pings from ws3 to ws2 and verify that the statistics are as expected.

```
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

### Test result criteria
Use vtysh output for "show interface x". Statistics should increase appropriately due to pings.

#### Test pass criteria
Counters increase for rx/tx packets and bytes.

#### Test fail criteria
Counters do not change for rx/tx input errors, drops, rx crc, or tx collisions.
