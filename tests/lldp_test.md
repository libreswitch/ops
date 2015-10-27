LLDP Test Cases
===============


## Contents

- [LLDP enable disable](#LLDP-enable-disable)
- [LLDP interface transmit and receive](#LLDP-interface-transmit-recieve)
- [LLDP wait and hold timers](#LLDP-wait-hold-timer)

##  LLDP enable disable
### Objective
The test case checks if LLDP has been enabled or disabled on a switch port by checking the neighbor port ID for the connected neighboring switch.
### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_enable_disable.py`(LLDP enable/disable)

### Setup
#### Topology diagram
```ditaa
    +--------+               +--------+
    |        |               |        |
    |   S1   | <-----------> |   S2   |
    |        |               |        |
    +--------+               +--------+
```

### Description
1. Create a topology with a single link between two switches, switch 1 and switch 2.
2. Configure **lldp** on switch 1 and switch 2 and enable the connected interfaces on both switches.
3. Wait for 30 seconds for the neighbors to advertise and check if we see the neighbors on the connected ports.
4. Disable **lldp** on both switches.
5. Check if neighbor entries have cleared on both switches.

##  LLDP interface transmit and receive
### Objective
The test case checks if LLDP transmit and receive can be configured successfully for individual interfaces.
### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_interface_txrx.py`(LLDP transmit/receive)

### Setup
#### Topology diagram
```ditaa
    +--------+               +--------+
    |        | <-----------> |        |
    |   S1   | <-----------> |   S2   |
    |        | <-----------> |        |
    |        | <-----------> |        |
    +--------+               +--------+
```

### Description
1. Create a topology with a four links between two switches, switch 1 and switch 2.
2. Disable transmission on link 2 of switch 1(rx only), disable reception on link 3 of switch 1(tx only), disable both transmission and reception on link 4 of switch 1.
3. Configure **lldp** on switch 1 and switch 2 and enable the connected interfaces on both switches.
4. Wait for 30 seconds for the neighbors to advertise.
5. Check each of the cases for neighbor entries.
6. The link 1 on switch 1 and switch 2 is default case, so neighbors should be present on both.
7. The link 2 of switch 1 must have neighbor entry but link 2 of switch 2 must not.
8. The link 3 of switch 1 must not have neighbor entry but switch 2 link 3 must have.
9. The link 4 of switch 1 and switch 2 must not have neighbor entries.

##  LLDP wait and hold timers
### Objective
The test case checks if LLDP wait and hold timers can be set.
### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_wait_hold.py`(LLDP wait/hold)

### Setup
#### Topology diagram
```ditaa
    +--------+               +--------+
    |        |               |        |
    |   S1   | <-----------> |   S2   |
    |        |               |        |
    +--------+               +--------+
```

### Description
1. Create a topology with a single link between two switches, switch 1 and switch 2.
2. Configure transmit time of 5 seconds and hold time of 2 seconds on both the switches.
3. Enable **lldp** on both switches.
4. Wait for 15 seconds and check to see if neighbor entries are present.
5. Disable **lldp** on both the switches.
6. Wait for 15 seconds and check if neighbor entries have been deleted.
