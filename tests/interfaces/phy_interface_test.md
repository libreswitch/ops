# Physical Interface Feature Test Cases

## Contents

- [Enable/Disable Interface](#enabledisable-interface)
   - [Verify through SNMP read operations](#verify-through-snmp-read-operations)
- [Autonegotiation](#autonegotiation)
- [Statistics](#statistics)
    - [Verify statistics through SNMP read operations](#verify-statistics-through-snmp-read-operations)
- [Verify interface statistics through SNMP](#verify-interface-statistics-through-snmp)

## Enable/Disable interface
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
#### Verify through SNMP read operations
Read the *ifAdminStatus* parameter of interface 1 through 'snmpget'. Verify the status of the interface.
```
wrkston01 : snmpget -v2c -cpublic <switch mgmt ip>:161 IF-MIB::ifAdminStatus.1
```
### Test result criteria
The interface `admin_state` is either "down" or "up" and pinging is used to determine if the link is active and working.

#### Test pass criteria
The interface `admin_state` is "up" or "down" when appropriate and pinging succeeds.

#### Test fail criteria
The interface `admin_state` is displayed as "up" or "down" when appropriate but pinging fails.

## Autonegotiation
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
Bring up two interfaces, with default autoneg (not configured). Verify autoneg is set to "on" and pings succeed.
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
#### Verify statistics through SNMP read operations
Execute the IF-MIB and then verify that the statistics are being incremented.
```
wrkston01 : snmpwalk -v1 -cpublic <switch mgmt ip>:161 1.3.6.1.2.1.2.1
```

### Test result criteria
Use the vtysh output for "show interface x". The statistics should increase appropriately due to pings.

#### Test pass criteria
Counters increase for `rx` or `tx` packets and bytes.

#### Test fail criteria
Counters do not change for `rx` or `tx` input errors, drops occur for `rx crc`, or drops occur for `tx`  collisions.


## Verify interface statistics through SNMP


### Objective
The test case confirms that SNMP is able to fetch the statistics update from the OVSDB.

Following are the statistics objects set by using the `ovs-vsctl` command.

### Interface statistics

| MIB-object  | OVSDB key|
|--------|--------|
| ifInUcastPkts,ifHCInUcastPkts | rx_packets |
| ifInOctets ,ifHCInOctets | rx_bytes |
| ifOutUcastPkts,ifHCOutUcastPkts |  tx_packets |
| ifOutOctets,ifHCOutOctets |tx_bytes |
| ifInDiscards | rx_dropped |
| ifInErrors | rx_crc_err |
| ifOutDiscards | tx_dropped |
| ifOutErrors    | tx_errors |


### IP statistics
| MIB-object  | OVSDB key|
|--------|--------|
|ipSystemStatsInReceives                       |             [sum over all interfaces]-- statistics[ip<v4/v6>_uc_rx_packets] + statistics[ip<v4/v6>_mc_rx_packets]|
|ipSystemStatsHCInReceives                      |             [sum over all interfaces]-- statistics[ip<v4/v6>_uc_rx_packets] + statistics[ip<v4/v6>_mc_rx_packets] |
|ipSystemStatsInOctets                          |             [sum over all interfaces]-- statistics[ip<v4/v6>_uc_rx_bytes] + statistics[ip<v4/v6>_mc_rx_bytes]|
|ipSystemStatsHCInOctets                        |             [sum over all interfaces]-- statistics[ip<v4/v6>_uc_rx_bytes] + statistics[ip<v4/v6>_mc_rx_bytes] |
|ipSystemStatsOutTransmits                      |             [sum over all interfaces]-- statistics[ip<v4/v6>_uc_tx_packets] + statistics[ip<v4/v6>_mc_tx_packets]|
|ipSystemStatsHCOutTransmits                    |             [sum over all interfaces]-- statistics[ip<v4/v6>_uc_tx_packets] + statistics[ip<v4/v6>_mc_tx_packets]|
|ipSystemStatsOutOctets                         |             [sum over all interfaces]-- statistics[ip<v4/v6>_uc_tx_bytes] + statistics[ip<v4/v6>_mc_tx_bytes]|
|ipSystemStatsHCOutOctets                       |             [sum over all interfaces]-- statistics[ip<v4/v6>_uc_tx_bytes] + statistics[ip<v4/v6>_mc_tx_bytes]|
|ipSystemStatsInMcastPkts                       |             [sum over all interfaces]-- statistics[ip<v4/v6>_mc_rx_packets]|
|ipSystemStatsHCInMcastPkts                     |             [sum over all interfaces]-- statistics[ip<v4/v6>_mc_rx_packets]|
|ipSystemStatsInMcastOctets                     |             [sum over all interfaces]-- statistics[ip<v4/v6>_mc_rx_bytes]|
|ipSystemStatsHCInMcastOctets                   |             [sum over all interfaces]-- statistics[ip<v4/v6>_mc_rx_bytes]|
|ipSystemStatsOutMcastPkts                      |             [sum over all interfaces]-- statistics[ip<v4/v6>_mc_tx_packets]|
|ipSystemStatsHCOutMcastPkts                    |             [sum over all interfaces]-- statistics[ip<v4/v6>_mc_tx_packets]|
|ipSystemStatsOutMcastOctets                    |             [sum over all interfaces]-- statistics[ip<v4/v6>_mc_tx_bytes]|
|ipSystemStatsHCOutMcastOctets                  |             [sum over all interfaces]-- statistics[ip<v4/v6>_mc_tx_bytes]     |


### Requirements
One switch is required for this test.

### Setup

#### Topology diagram
```ditaa
    +--------+               +--------+
    |        |               |        |
    |   S1   | <-----------> |   S2   |
    |        |               |        |
    +--------+               +--------+
```
## Case 1 : snmpwalk for version 1, 2c and 3

## Description
To test the scenario, the statistics values are manually added using the `ovs-vsctl set` command, followed by snmpwalk operations on an IF-MIB snd IP-MIB objects.
To test v3,
- Configure SNMPv3 authNoPriv user. and query with respective auth-key.
- Configure SNMPv3 authPriv user, and query with respective auth-key and priv-key.


### Test result criteria
Use the `snmpwalk` command to read all the IF-MIB and IP-MIB statistics.
For version 1 and verison 2c,
```
snmpwalk -<v1/v2c> -c<public/configured_community> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2
```
For version v3, authNoPriv user,
```
snmpwalk -v3 - u <user> -a <auth> -A <auth-key> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2
```
For version v3, authPriv user,
```
snmpwalk -v3 - u <user> -a <auth> -A <auth-key> -x <priv> -X <priv-key> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2
```

#### Test pass criteria
The `snmpwalk` command output result reflects the updated counters.

#### Test fail criteria
The `snmpwalk` command output result does not reflect the updated counters.

## Case 2 : snmpgetnext for version 1, 2c and 3

## Description
To test the scenario, the statistics values are manually added using the `ovs-vsctl set` command, followed by snmpgetnext operations on an IF-MIB snd IP-MIB objects.
To test v3,
- Configure SNMPv3 authNoPriv user. and query with respective auth-key.
- Configure SNMPv3 authPriv user, and query with respective auth-key and priv-key.


### Test result criteria
Use the `snmpgetnext` command to read all the IF-MIB and IP-MIB statistics.
For version 1 and verison 2c,
```
snmpgetnext -<v1/v2c> -c<public/configured_community> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2.1.10.1
```
For version v3, authNoPriv user,
```
snmpgetnext -v3 - u <user> -a <auth> -A <auth-key> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2.2.1.10.1
```
For version v3, authPriv user,
```
snmpgetnext -v3 - u <user> -a <auth> -A <auth-key> -x <priv> -X <priv-key> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2.2.1.10.1
```

#### Test pass criteria
The `snmpgetnext` command output result reflects the updated counters.

#### Test fail criteria
The `snmpgetnext` command output result does not reflect the updated counters.

## Case 3 : snmpget for version 1, 2c and 3

## Description
To test the scenario, the statistics values are manually added using the `ovs-vsctl set` command, followed by snmpget operations on an IF-MIB snd IP-MIB objects.
To test v3,
- Configure SNMPv3 authNoPriv user. and query with respective auth-key.
- Configure SNMPv3 authPriv user, and query with respective auth-key and priv-key.


### Test result criteria
Use the `snmpget` command to read all the IF-MIB and IP-MIB statistics.
For version 1 and verison 2c,
```
snmpget -<v1/v2c> -c<public/configured_community> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2.1.10.1
```
For version v3, authNoPriv user,
```
snmpget -v3 - u <user> -a <auth> -A <auth-key> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2.2.1.10.1
```
For version v3, authPriv user,
```
snmpget -v3 - u <user> -a <auth> -A <auth-key> -x <priv> -X <priv-key> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2.2.1.10.1
```

#### Test pass criteria
The `snmpget` command output result reflects the updated counters.

#### Test fail criteria
The `snmpget` command output result does not reflect the updated counters.

## Case 4 : snmpbulkget for version 2c and 3

## Description
To test the scenario, the statistics values are manually added using the `ovs-vsctl set` command, followed by snmpget operations on an IF-MIB snd IP-MIB objects.
To test v3,
- Configure SNMPv3 authNoPriv user. and query with respective auth-key.
- Configure SNMPv3 authPriv user, and query with respective auth-key and priv-key.


### Test result criteria
Use the `snmpbulkget` command to read all the IF-MIB and IP-MIB statistics.
For version 1 and verison 2c,
```
snmpbulkget -<v1/v2c> -c<public/configured_community> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2.1.10.1
```
For version v3, authNoPriv user,
```
snmpbulkget -v3 - u <user> -a <auth> -A <auth-key> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2.2.1.10.1
```
For version v3, authPriv user,
```
snmpbulkget -v3 - u <user> -a <auth> -A <auth-key> -x <priv> -X <priv-key> <localhost/remote IP:agent_port> 1.3.6.1.2.1.2.2.2.1.10.1
```

#### Test pass criteria
The `snmpbulkget` command output result reflects the updated counters for next 10 consecutive MIB objects.

#### Test fail criteria
The `snmpbulkget` command output result does not reflect the updated counters for next 10 consecutive MIB objects.