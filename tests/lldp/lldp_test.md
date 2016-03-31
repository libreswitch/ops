# LLDP Test Cases


## Contents



- [CLI](#cli)
	- [LLDP enable or disable](#lldp-enable-or-disable)
	- [LLDP interface transmit and receive](#lldp-interface-transmit-and-receive)
	- [LLDP wait and hold timers](#lldp-wait-and-hold-timers)
- [SNMP](#snmp)
	- [Snmpget](#snmpget)
	- [SnmpgetNext](#snmpgetnext)
	- [SnmpgetBulk](#snmpgetbulk)
	- [Snmpwalk](#snmpwalk)
	- [LLDP SNMP traps](#lldp-snmp-traps)
	- [Test to verify the SNMP master agent port operation](#test-to-verify-the-snmp-master-agent-port-operation)
    - [Test to verify the SNMP master communities operation](#test-to-verify-the-snmp-master-communities-operation)
    - [Test to verify the SNMP system MIB configurations](#test-to-verify-the-snmp-system-mib-configurations)
    - [Test to verify the SNMP version 3 configurations](#test-to-verify-the-snmp-version-3-configurations)


##CLI
### LLDP enable or disable
#### Objective
This test case validates that the LLDP has been enabled or disabled on a switch port by checking the neighbor port ID for the connected neighboring switch.
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
3. Wait for 30 seconds for the neighbors to advertise and check that the neighbors are on the connected ports.
4. Disable **lldp** on both switches.
5. Ensure that the neighbor entries have cleared on both switches.

### LLDP interface transmit and receive
#### Objective
This test case confirms that the LLDP transmit and receive can be configured successfully for individual interfaces.
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
2. Disable the transmission on link 2 of switch 1(rx only), disable the reception on link 3 of switch 1(tx only), and disable both transmission and reception on link 4 of switch 1.
3. Configure **lldp** on switch 1 and switch 2 and enable the connected interfaces on both switches.
4. Wait for 30 seconds for the neighbors to advertise.
5. Check each of the cases for neighbor entries.
6. The link 1 on switch 1 and switch 2 is default case, so neighbors should be present on both.
7. The link 2 of switch 1 must have neighbor entry but link 2 of switch 2 must not.
8. The link 3 of switch 1 must not have neighbor entry but switch 2 link 3 must have.
9. The link 4 of switch 1 and switch 2 must not have neighbor entries.

### LLDP wait and hold timers
#### Objective
This test case confirms that the LLDP wait and hold timers can be set.
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
1. Create a topology with a single link between switch 1 and switch 2 (two switches).
2. Configure the transmit time of 5 seconds and the hold time of 2 seconds on both the switches.
3. Enable **lldp** on both switches.
4. Wait for 15 seconds and check to see if the neighbor entries are present.
5. Disable **lldp** on both the switches.
6. Wait for 15 seconds and check if the neighbor entries have been deleted.

##SNMP

### Snmpget
#### Test case 1
##### Objective
This test case verifies if the snmpget(v1/v2/v3) query for an lldp object is processed by the snmp agent to get the data from the OVSDB.

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
1. Create a topology with switch 1 (single switch).
2. Query for an OID which has a schema equivalent object.
3. Configure the schema equivalent object of the above OID through the CLI. Query again.


##### Pass/Fail criteria
This test case passes if the:
  - First query gets the default value of lldp tx interval.
  - Second query gets the configured value of lldp tx interval.
This test cases fails if the:
  - Get query fails to read from OVSDB.
  - Second query does not get the configured value.

#### Test case 2
##### Objective
- This test case verifies that the snmpget(v1/v2/v3) query for an lldp object which does not have a schema equivalent, returns the default value specified in the convert function.

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
1. Create a topology with switch 1 (single switch).
2. Query for an OID which does not have a schema equivalent object.


##### Pass/Fail criteria
- This test case passes if the query returns the default value specified in convert function.
- This test case fails if the query does not return the default value specified in convert function.


### SnmpgetNext
#### Test case 1
##### Objective
- This test case verifies that the snmpgetNext(v1/v2/v3) query for an lldp object is processed by the snmp agent to get the data from the OVSDB.

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
1. Create a topology with switch 1 (single switch).
2. Query for the next OID.
3. Configure the schema equivalent of the above OID through the CLI. Query again.

##### Pass/Fail criteria
- This test case passes if the:
  - First query gets the default value of a next OID in a lexicographical order.
  - Second query gets the configured value for OID.
- This test case fails if the:
  - Get query fails to read from OVSDB.
  - Second query does not get the configured value.

#### Test case 2
##### Objective
This test case confirms that the snmpgetNext(v1/v2/v3) query for an lldp object which does not have a schema equivalent, returns the default value specified in the convert function.
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
1. Create a topology with switch 1 (single switch).
2. Query for an OID who's next OID does not have a schema equivalent object.


##### Pass/Fail criteria
- This test case passes if the query returns default value specified in the convert function.
- This test fails if the query does not return default value specified in the convert function.


### SnmpgetBulk
#### Test case 1
##### Objective
This test case verifies that the snmpgetBulk(v1/v2/v3) query for a set of lldp objects is processed by the snmp agent to get the data from the OVSDB.

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
1. Create a topology with switch 1 (single switch).
2. Query for OID.
3. Configure the schema equivalent of the above OID through the CLI. Query again.

##### Pass/Fail criteria
- This test case passes if the:
  - First query gets the default values.
  - Second query gets the configured value for OID.
- This test case fails if the:
  - Query fails to read from OVSDB.
  - Second query does not get the configured value.

### Snmpwalk
#### Objective
This test case verifies if the snmpwalk(v1/v2/v3) can walk through the complete LLDP-MIB.

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
1. Create a topology with switch 1 (a single switch).
2. Walk the table using snmpwalk.

##### Pass/Fail criteria
- This test case passes if the query walks through all of the OIDs.
- This test case fails if the query does not walk through all of the OIDs.

## LLDP SNMP traps
### Objective
This test case verifies that the LLDP daemon is sending the lldpRemTablesChange trap to the trap receiver.
### Requirements
- Physical Host/Switch/Switch Test setup
- **FT File**: `ops/tests/lldp/test_lldp_ft_enable_disable.py`(LLDP Traps)

### Setup
#### Topology diagram
```ditaa
     +--------+     +--------+               +--------+
     |        |     |        |               |        |
     |   H1   | <-->|   S1   | <-----------> |   S2   |
     |        |     |        |               |        |
     +--------+     +--------+               +--------+
```

### Description
1. Create a topology with a single link between two switches, switch 1 and switch 2, and a single link between host 1 and switch 1.
2. Configure the trap receiver daemon on host H1 and set it as the trap receiver in S1.
3. Configure **lldp** on switch 1 and switch 2 and enable the connected interfaces on both switches.
4. Check if a trap has been received on H1 with an increase in the lldpStatsRemTablesInserts value.
5. Disable **lldp** on switch 2.
6. Wait for 30 seconds and check if a trap has been received on H1.

##### Pass/Fail criteria
- This test case passes if the trap is received on the receiver.
- This test case fails if the trap is not seen on the receiver log.

### Test to verify the SNMP master agent port operation

#### Objective

- The test verifies that when a port on which a SNMP agent is listening on to for the user queries is modified, the agent will listen on the new port. Test case is validated using snmpwalk version 2 query.



#### Requirements

- Physical Switch/switch, workstation Test setup



#### Setup



##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.
2. Configure a SNMP agent port using CLI `snmp-server agent-port <1-65535>`.
3. Verify the configuration using `show snmp agent-port`
4.  Walk the MIB using `snmpwalk` on configured port



##### Pass/Fail criteria

- The test passes if the query walks through all the OIDs on the new port.

- This tests fails if the query does not walk through all the OIDs on the new port.

### Test to verify the SNMP master communities operation

#### Objective

- The test verifies that when a new community is configured using CLI, all the snmp queries will answer to that community. Test case is validated using snmpwalk version 2 query.



#### Requirements

- Physical Switch/switch, workstation Test setup



#### Setup



##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```





#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.
2. Configure a SNMP community using CLI `snmp-server community WORD`.
3. Verify the configration using `show snmp community`
3. Walk the MIB.



##### Pass/Fail criteria

- The test passes if the query walks through all the OIDs for a configured community.

- This tests fails if the query does not walk through all the OIDs for a configured community.

### Test to verify the SNMP system MIB configurations

#### Objective

- The test verifies that when a system MIB objects are configured through CLI, the new values are reflected when walked through system MIB. Test case is validated using snmpwalk version 2 query.

#### Requirements
- Physical Switch/switch, workstation Test setup

#### Setup
##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```

#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.
2. Configure a SNMP system description using `snmp-server system-description .LINE`.
3. Configure a SNMP system location using `snmp-server system-location .LINE`.
4. Configure a SNMP system contact using `snmp-server system-contact .LINE`.
5. Verify the configuration using `show anmp system`.
6. Configure hostname using `hostname WORD`
7. Walk the system MIB.

##### Pass/Fail criteria
- The test passes if the query walks through all the system MIB OIDs reflecting the configured values.
- This tests fails if the query does not walk through all the system MIB OIDs or does not reflect the configured values.


### Test to verify the SNMP version 3 configurations

#### Objective
- The test verifies that when snmpv3 user is configured, agent responds to the queries for the new user.

#### Requirements
- Physical Switch/switch, workstation Test setup

#### Setup
##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```


#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.
2. Configure a SNMPv3 user using CLI `snmpv3 user WORD [auth (md5|sha) auth-pass WORD [priv (aes | des) priv-pass WORD]]`
6. Verify the configuration using `show snmpv3 user`.
7. SNMP Walk on .1 for the configured user. (Walk on .1 walk through all the MIB OIDs registered.)

##### Pass/Fail criteria

- The test passes if the query walks through all the MIB OIDs.
- This tests fails if the query does not walk through  MIB OIDs.


### Test to verify the SNMP version 3 authnopriv configurations

#### Objective
- The test verifies that when authnopriv snmpv3 user is configured, agent responds to the queries for the new user only if authentication key is correct.

#### Requirements
- Physical Switch/switch, workstation Test setup

#### Setup
##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```


#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.
2. Configure a SNMPv3 user using CLI `snmpv3 user WORD [auth (md5|sha) auth-pass WORD [priv (aes | des) priv-pass WORD]]`
6. Verify the configuration using `show snmpv3 user`.
7. SNMP Walk on .1 for the configured user, providing the correct auth-key.(Walk on .1 walk through all the MIB OIDs registered.)

##### Pass/Fail criteria

- The test passes if the query walks through all the MIB OIDs.
- This tests fails if the query does not walk through  MIB OIDs.


### Test to verify the SNMP version 3 authpriv configurations

#### Objective
- The test verifies that when authpriv snmpv3 user is configured, agent responds to the queries for the new user only if authentication and privecy key are correct.

#### Requirements
- Physical Switch/switch, workstation Test setup

#### Setup
##### Topology diagram

```ditaa

    +--------+               +--------+

    |        | <-----------> |        |

    |   S1   | <-----------> |   WS   |

    |        | <-----------> |        |

    |        | <-----------> |        |

    +--------+               +--------+

```


#### Description

1. Create a topology with a single switch, switch 1 and a workstation WS.
2. Configure a SNMPv3 user using CLI `snmpv3 user WORD [auth (md5|sha) auth-pass WORD [priv (aes | des) priv-pass WORD]]`
6. Verify the configuration using `show snmpv3 user`.
7. SNMP Walk on .1 for the configured user providing correct auth-key and priv-key.(Walk on .1 walk through all the MIB OIDs registered.)

##### Pass/Fail criteria

- The test passes if the query walks through all the MIB OIDs.
- This tests fails if the query does not walk through  MIB OIDs.
