LLDP Test Cases
===============


## Contents

- [CLI](#cli)
  - [LLDP enable disable](#lldp-enable-disable)
  - [LLDP interface transmit and receive](#lldp-interface-transmit-and-receive)
  - [LLDP wait and hold timers](#lldp-wait-and-hold-timers)
- [SNMP](#snmp)
  - [snmpget](#snmpget)
  - [snmpgetNext](#snmpgetnext)
  - [snmpgetBulk](#snmpgetBulk)
  - [snmpwalk](#snmpwalk)

##CLI
### LLDP enable disable
#### Objective
The test case checks if LLDP has been enabled or disabled on a switch port by checking the neighbor port ID for the connected neighboring switch.
#### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_enable_disable.py`(LLDP enable/disable)

#### Setup
##### Topology diagram
```ditaa
    +--------+               +--------+
    |        |               |        |
    |   S1   | <-----------> |   S2   |
    |        |               |        |
    +--------+               +--------+
```

#### Description
1. Create a topology with a single link between two switches, switch 1 and switch 2.
2. Configure **lldp** on switch 1 and switch 2 and enable the connected interfaces on both switches.
3. Wait for 30 seconds for the neighbors to advertise and check if we see the neighbors on the connected ports.
4. Disable **lldp** on both switches.
5. Check if neighbor entries have cleared on both switches.

###  LLDP interface transmit and receive
#### Objective
The test case checks if LLDP transmit and receive can be configured successfully for individual interfaces.
#### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_interface_txrx.py`(LLDP transmit/receive)

#### Setup
##### Topology diagram
```ditaa
    +--------+               +--------+
    |        | <-----------> |        |
    |   S1   | <-----------> |   S2   |
    |        | <-----------> |        |
    |        | <-----------> |        |
    +--------+               +--------+
```

#### Description
1. Create a topology with a four links between two switches, switch 1 and switch 2.
2. Disable transmission on link 2 of switch 1(rx only), disable reception on link 3 of switch 1(tx only), disable both transmission and reception on link 4 of switch 1.
3. Configure **lldp** on switch 1 and switch 2 and enable the connected interfaces on both switches.
4. Wait for 30 seconds for the neighbors to advertise.
5. Check each of the cases for neighbor entries.
6. The link 1 on switch 1 and switch 2 is default case, so neighbors should be present on both.
7. The link 2 of switch 1 must have neighbor entry but link 2 of switch 2 must not.
8. The link 3 of switch 1 must not have neighbor entry but switch 2 link 3 must have.
9. The link 4 of switch 1 and switch 2 must not have neighbor entries.

###  LLDP wait and hold timers
#### Objective
The test case checks if LLDP wait and hold timers can be set.
#### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_wait_hold.py`(LLDP wait/hold)

#### Setup
##### Topology diagram
```ditaa
    +--------+               +--------+
    |        |               |        |
    |   S1   | <-----------> |   S2   |
    |        |               |        |
    +--------+               +--------+
```

#### Description
1. Create a topology with a single link between two switches, switch 1 and switch 2.
2. Configure transmit time of 5 seconds and hold time of 2 seconds on both the switches.
3. Enable **lldp** on both switches.
4. Wait for 15 seconds and check to see if neighbor entries are present.
5. Disable **lldp** on both the switches.
6. Wait for 15 seconds and check if neighbor entries have been deleted.

##SNMP

### Snmpget
#### Test case 1
##### Objective
- The test case to verify if snmpget(v1/v2/v3) query for a lldp object is processed by snmp agent to get the data from OVSDB.

##### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_snmp_get.py`

##### Setup

###### Topology diagram
```ditaa
    +--------+
    |        |
    |   S1   |
    |        |
    +--------+
```


##### Description
1. Create a topology with a single switch, switch 1.
2. Query for a OID which has a schema equivalent object.
3. Configure the schema equivalent of the above OID through CLI. Query again.


##### Pass/Fail criteria
- The test case is passed if
  - first query gets the default value of lldp tx interval.
  - second query gets the configured value of lldp tx interval.
- The test case is failed if
  - Get query fails to read from OVSDB.
  - Second query does not get the configured value.

#### Test case 2
##### Objective
- The test case to verify if snmpget(v1/v2/v3) query for a lldp object which does not have a schema equivalent.

##### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_snmp_get.py`

##### Setup

###### Topology diagram
```ditaa
    +--------+
    |        |
    |   S1   |
    |        |
    +--------+
```


##### Description
1. Create a topology with a single switch, switch 1.
2. Query for a OID which does not have a schema equivalent object.


##### Pass/Fail criteria
- The test case is passed if
  - The query returns default value specified in convert function.
- The test case is failed if
  - The query does not return default value specified in convert function.


### SnmpgetNext
#### Test case 1
##### Objective
- The test case to verify if snmpgetNext(v1/v2/v3) query for a lldp object is processed by snmp agent to get the data from OVSDB.

##### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_snmp_get_next.py`

##### Setup

###### Topology diagram
```ditaa
    +--------+
    |        |
    |   S1   |
    |        |
    +--------+
```


##### Description
1. Create a topology with a single switch, switch 1.
2. Query for next OID.
3. Configure the schema equivalent of the above OID through CLI. Query again.

##### Pass/Fail criteria
- The test case is passed if
  - first query gets the default value of a next OID in a lexicographical order.
  - second query gets the configured value for OID.
- The test case is failed if
  - Get query fails to read from OVSDB.
  - Second query does not get the configured value.

#### Test case 2
##### Objective
- The test case to verify if snmpgetNext(v1/v2/v3) query for a lldp object which does not have a schema equivalent.

##### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_snmp_get.py`

##### Setup

###### Topology diagram
```ditaa
    +--------+
    |        |
    |   S1   |
    |        |
    +--------+
```


##### Description
1. Create a topology with a single switch, switch 1.
2. Query for a OID whose next OID does not have a schema equivalent object.


##### Pass/Fail criteria
- The test case is passed if
  - The query returns default value specified in convert function.
- The test case is failed if
  - The query does not return default value specified in convert function.


### SnmpgetBulk
#### Test case 1
##### Objective
- The test case to verify if snmpgetBulk(v1/v2/v3) query for a set of lldp objects is processed by snmp agent to get the data from OVSDB.

##### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_snmp_get_next.py`

##### Setup

###### Topology diagram
```ditaa
    +--------+
    |        |
    |   S1   |
    |        |
    +--------+
```


##### Description
1. Create a topology with a single switch, switch 1.
2. Query for OID.
3. Configure the schema equivalent of the above OID through CLI. Query again.

##### Pass/Fail criteria
- The test case is passed if
  - The first query gets the default values.
  - The second query gets the configured value for OID.
- The test case is failed if
  - The query fails to read from OVSDB.
  - The second query does not get the configured value.

### Snmpwalk
#### Objective
- The test case is to verify if snmpwalk(v1/v2/v3) to walk the complete LLDP-MIB.

#### Requirements
- Physical Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_snmp_walk.py`

#### Setup

##### Topology diagram
```ditaa
    +--------+
    |        |
    |   S1   |
    |        |
    +--------+
```


#### Description
1. Create a topology with a single switch, switch 1.
2. Walk the table using snmpwalk.

##### Pass/Fail criteria
- The test case is passed if
   - The query walks through all the OIDs.
- The test case is failed if
   - The query fails to walk through all the OIDs.