Platform Capabilities and Capacities Design

## Contents
  * [High level design of platform capabilties and capacities](#high-level-design-of-platform-capabilities-and-capacities)
    * [Design choices](#design-choices)
    * [Participating modules](#participating-modules)
  * [OVSDB-Schema](#ovsdb-schema)
  * [References](#references)

# High level design of platform capabilties and capacities
Porting OpenSwitch to a new hardware platform requires communicating hardware-specific capabilities and limititations from the platform-dependent modules to the platform-independent modules. The modules in switchd and sysd determine the properties of the switching ASIC and of the platform and those modules then populate subsystem and system tables in OVSDB. User interfaces, daemons, and applications query the system table and act accordingly to determine which features are enabled and their limitations.

## Design choices

### Location of data
Other design considerations include putting capabilities and capacities in tables appropriate to the respective features and modules. The risk in doing so is that information of this type is spread across the OVSDB and could be overlooked, which could lead to duplicate or inconsistent feature capability or capacity data. Consolidating the data into the system table provides a single source of truth in the database, with a well-known location and well-known keys.


### Allowable values
Several ideas were discussed in the [IRC Discussions](#references)
* Lists for capabilities allow consolidation of multiple related capabilities under a single key. For example: acls_capable: in_ipv4, out_ipv4, in_mac, and so on. This would require an extra level of parsing, but allow a more compact representation in the database.
* Enums for capabilities - Allows for fine-grained communication of capabilities but allows more values than just true or false.
* Bitmaps for capabilities - Use an integer bitmap to represent related capabilities.

## Participating modules
```ditaa
+---------+   +---------+  +------+
|         |   | {s}     |  |      |
| daemons <--->         <--> apps |
+---------+   |         |  +------+
              |  OVSDB  <------+
              +----^----+      |
                   |           |
          +--------+----+   +--v-----------+
          | ops-switchd |   |   ops-sysd   |
          +--------^----+   +--+-----------+
                   |           |
          +--------v----+   +--v-----------+
          |   ASIC      |   |   Hardware   |
          +-------------+   +--------------+
```

During module initialization, switchd populates the capabilities and capacities columns in the OVSDB Subsystem table. The sysd module acts as an arbiter to summarize the data from multiple subsystems into the System table capacities and capabilities columns. Applications and daemons read the system-wide values from the System table.

## OVSDB-Schema
The specific keys and their meanings are documented in vswitch.xml.

### Capabilities
Capabilities can have a key that is present or not present. If a key is present, the value can be true or false.

Key Status     | Value   |  Meaning
---------------|---------|-----------------
Not present    | n/a     | feature is not supported
present        | true    | feature is supported and enabled
present        | false   | feature is supported but not enabled

### Capacities
Capacities can have a key that is present or not present. If a key is present, the value can be zero or greater than zero.

Key Status     | Value   |  Meaning
---------------|---------|-----------------
Not present    | n/a     | feature is not supported
present        | >0      | feature is supported and enabled, with limit specified by value
present        | 0       | feature is supported but not enabled

### Subsystem table
```
Subsystem:capabilities
Keys: string
Values: boolean

Subsystem:capacities
Keys: string
Values: integer
```
### System table
```
System:capabilities
Keys: string
Values: boolean

System:capacities
Keys: string
Values: integer
```

# References
[IRC Discussions] (http://eavesdrop.openswitch.net/meetings/platform_capabilities_and_capacities/2015/)
