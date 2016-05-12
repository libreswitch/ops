# LACP commands

## Contents

- [LACP configuration commands](#lacp-configuration-commands)
	- [Global context commands](#global-context-commands)
		- [Creation of LAG interface](#creation-of-lag-interface)
		- [Deletion of LAG interface](#deletion-of-lag-interface)
		- [Configuring LACP system priority](#configuring-lacp-system-priority)
		- [Configuring default LACP system priority](#configuring-default-lacp-system-priority)
	- [Interface context commands](#interface-context-commands)
		- [Assigning interface to LAG](#assigning-interface-to-lag)
		- [Removing interface from LAG](#removing-interface-from-lag)
		- [Configuring LACP port-id](#configuring-lacp-port-id)
		- [Configuring LACP port-priority](#configuring-lacp-port-priority)
	- [LAG context commands](#lag-context-commands)
		- [Entering into LAG context](#entering-into-lag-context)
		- [Configuring LACP mode](#configuring-lacp-mode)
		- [Configuring hash type](#configuring-hash-type)
		- [Configuring LACP fallback mode](#configuring-lacp-fallback-mode)
		- [Configuring LACP rate](#configuring-lacp-rate)
		- [Configuring shutdown](#configuring-shutdown)
- [LAG display commands](#lag-display-commands)
	- [Display global LACP configuration](#display-global-lacp-configuration)
	- [Display LACP aggregates](#display-lacp-aggregates)
	- [Display LACP interface configuration](#display-lacp-interface-configuration)
	- [LAG show running-config](#lag-show-running-config)
- [LAG diagnostic dump commands](#lag-diagnostic-dump-commands)
	- [LAG diag-dump basic](#lag-diag-dump-basic)

## LACP configuration commands
### Global context commands
#### Creation of LAG interface
##### Syntax

```
    interface lag ID
```

##### Description
This command creates a Link Aggregation Group (LAG) interface represented by an ID.

##### Authority
all users

##### Parameters
This command takes an ID as a parameter which represents a LAG interface. The LAG interface ID can be in the range of 1 to 2000.

##### Examples

```
switch(config)# interface lag 100

switch(config-lag-if)#
```

#### Deletion of LAG interface
##### Syntax

```
 no interface lag ID
```

##### Description
This command deletes a LAG interface represented by an ID.

##### Authority
all users

##### Parameters
This command takes an ID as a parameter which represents a LAG interface. The LAG interface ID can be in the range of 1 to 2000.

##### Examples

```
switch(config)# no interface lag 100
```

#### Configuring LACP system priority
##### Syntax

```
    lacp system-priority <0-65535>
```

##### Description
This command sets a Link Aggregation Control Protocol (LACP) system priority.

##### Authority
all users

##### Parameters
This command takes a system priority value in the of range 0 to 65535.

##### Examples

```
switch(config)# lacp system-priority 100
```

#### Configuring default LACP system priority
##### Syntax

```
    no lacp system-priority
```

##### Description
This command sets an LACP system priority to a default(65534).

##### Authority
all users

##### Parameters
no parameters

##### Examples

```
switch(config)# lacp system-priority 100
```

### Interface context commands
#### Assigning interface to LAG
##### Syntax

```
    lag ID
```

##### Description
This command adds an interface to a LAG interface specified by an ID.

##### Authority
all users

##### Parameters
This command takes an ID as a parameter which represents a LAG interface. The LAG interface ID can be in the range of 1 to 2000.

##### Examples

```
switch(config)# interface 1
switch(config-if)# lag 100
```

#### Removing interface from LAG
##### Syntax

```
    no lag ID
```

##### Description
This command removes an interface from a LAG interface specified by an ID.

##### Authority
all users

##### Parameters
This command takes an ID as a parameter which represents a LAG interface. The LAG interface ID can be in the range of 1 to 2000.

##### Examples

```
switch(config)# interface 1
switch(config-if)# no lag 100
```

#### Configuring LACP port-id
##### Syntax

```
    lacp port-id <1-65535>
```

##### Description
This command sets an LACP port-id value of the interface.

##### Authority
all users

##### Parameters
This command takes a port-id value in the range of 1 to 65535.

##### Examples

```
switch(config-if)# lacp port-id 10
```

#### Configuring LACP port-priority
##### Syntax

```
    lacp port-priority <1-65535>
```

##### Description
This command sets an LACP port-priority value for the interface.

##### Authority
all users

##### Parameters
This command takes a port-priority value in the range of 1 to 65535.

##### Examples

```
switch(config-if)# lacp port-priority 10
```

### LAG context commands
#### Entering into LAG context
##### Syntax

```
    interface lag ID
```

##### Description
This command enters into the LAG context of the specified LAG ID. If the specified LAG interface is not present, this command creates a LAG interface and enters it into the LAG context.

##### Authority
all users

##### Parameters
This command takes an ID as a parameter which represents a LAG interface. The LAG interface ID can be in the range of 1 to 2000.

##### Examples

```
switch(config)# interface 1
switch(config-if)# lag 100
```

#### Configuring LACP mode
##### Syntax

```
    [no] lacp mode {active/passive}
```

##### Description
This command sets an LACP mode to active or passive.
The **no** form of the command sets the LACP mode to **off**.

##### Authority
all users

##### Parameters
This command takes an **active** or **passive** keyword as an argument to set an LACP mode.

##### Examples

```
switch(config)# interface lag 1
switch(config-lag-if)# lacp mode active
switch(config-lag-if)# no lacp mode active
```

#### Configuring hash type
##### Syntax

```
    hash {l2-src-dst/l3-src-dst/l4-src-dst}
```

##### Description
This command sets an LACP hash type to l2-src-dst, l3-src-dst or l4-src-dst. The default is l3-src-dst.

##### Authority
all users

##### Parameters
no parameters.

##### Examples

```
switch(config)# interface lag 1
switch(config-lag-if)# hash l2-src-dst
```

#### Configuring LACP fallback mode
##### Syntax

```
    lacp fallback
```

##### Description
This command enables an LACP fallback mode.
The **no** form of the command disables the an LACP fallback mode.

##### Authority
all users

##### Parameters
no parameters.

##### Examples

```
switch(config)# interface lag 1
switch(config-lag-if)# lacp fallback
switch(config-lag-if)# no lacp fallback
```

##### Configuring LACP rate
##### Syntax

```
    lacp rate fast
```

##### Description
This command sets an LACP heartbeat request time to **fast**. The default is **slow**, which is once every 30 seconds. The **no** form of the command sets an LACP rate to **slow**.

##### Authority
all users

##### Parameters
no parameters.

##### Examples

```
switch(config)# interface lag 1
switch(config-lag-if)# lacp rate fast
```

##### Configuring no shutdown
##### Syntax

```
    no shutdown
```

##### Description
This command sets every interface in LAG to no shutdown.

##### Authority
all users

##### Parameters
no parameters.

##### Examples

```
switch(config)# interface lag 1
switch(config-lag-if)# no shutdown
```

##### Configuring shutdown
##### Syntax

```
    shutdown
```

##### Description
This command sets every interface in LAG to shutdown.

##### Authority
all users

##### Parameters
no parameters.

##### Examples

```
switch(config)# interface lag 1
switch(config-lag-if)# shutdown
```

## LAG display commands
### Display global LACP configuration
#### Syntax

```
    show lacp configuration
```

#### Description
This command displays global a LACP configuration.

#### Authority
all users

#### Parameters
no parameters

#### Examples

```
switch# show lacp configuration
System-id       : 70:72:cf:ef:fc:d9
System-priority : 65534
```

### Display LACP aggregates
#### Syntax

```
    show lacp aggregates [lag-name]
```

#### Description
This command displays all LACP aggregate information if no parameter is passed. If a LAG name is passed as an argument, it shows information of the specified LAG.

#### Authority
all users

#### Parameters
This command takes a LAG name as an optional parameter.

#### Examples

```
switch# show lacp aggregates lag100

Aggregate-name        : lag100
Aggregated-interfaces : 1
Heartbeat rate        : slow
Fallback              : false
Hash                  : l3-src-dst
Aggregate mode        : active

switch# show lacp aggregates

Aggregate-name        : lag100
Aggregated-interfaces : 1
Heartbeat rate        : slow
Fallback              : false
Hash                  : l3-src-dst
Aggregate mode        : active

Aggregate-name        : lag200
Aggregated-interfaces : 3 2
Heartbeat rate        : slow
Fallback              : false
Hash                  : l3-src-dst
Aggregate mode        : active

switch#
```

### Display LACP interface configuration
#### Syntax

```
    show lacp interfaces [IFNAME]
```

#### Description
This command displays an LACP configuration of the physical interfaces. If an interface name is passed as argument, it only displays an LACP configuration of a specified interface.

#### Authority
all users

#### Parameters
This command takes an interface name as an optional parameter.

#### Examples

```
switch# show lacp interfaces
State abbreviations
A - Active        P - Passive      F - Aggregable I - Individual
S - Short-timeout L - Long-timeout N - InSync     O - OutofSync
C - Collecting    D - Distributing
X - State m/c expired              E - Default neighbor state

Actor details of all interfaces
\------------------------------------------------------------------------------
Intf Aggregate Port    Port     Key  State   System-id         System   Aggr
     name      id      Priority                                Priority Key
\------------------------------------------------------------------------------
1    lag100    16      1        1    ALFNCDE 70:72:cf:59:97:06 65534    100
3    lag200    70      1        2    ALFOCX  70:72:cf:59:97:06 65534    200
2    lag200    13      1        2    ALFNCDE 70:72:cf:59:97:06 65534    200
.
Partner details of all interfaces
\------------------------------------------------------------------------------
Intf Aggregate Partner Port     Key  State   System-id         System   Aggr
     name      Port-id Priority                                Priority Key
\------------------------------------------------------------------------------
1    lag100    0       0        0    PLFNCD  00:00:00:00:00:00 0        100
3    lag200    0       0        0    PSFO    00:00:00:00:00:00 0        200
2    lag200    0       0        0    PLFNCD  00:00:00:00:00:00 0        200


switch# show lacp interfaces lag100

State abbreviations
A - Active        P - Passive      F - Aggregable I - Individual
S - Short-timeout L - Long-timeout N - InSync     O - OutofSync
C - Collecting    D - Distributing
X - State m/c expired              E - Default neighbor state

Aggregate-name :
\-------------------------------------------------
                       Actor             Partner
\-------------------------------------------------
Port-id            |                    |
Port-priority      |                    |
Key                |                    |
State              |                    |
System-id          |                    |
System-priority    |                    |

switch#
```

### LAG show running-config
#### Syntax

```
    show running-config
```

#### Description
This command displays the complete switch configuration, when the switch has
LAGs configured it should display all the configuration specific to those interfaces.

#### Authority
all users

#### Parameters
No parameters

#### Examples
```
switch# show running-config
Current configuration:
!
!
!
!
!
vlan 1
    no shutdown
interface lag 2
    no shutdown
    ip address 10.2.2.2/24
    ipv6 address 2001::1/64
interface lag 3
    no shutdown
    lacp mode passive
interface lag 1
    no shutdown
    lacp mode active
    ip address 10.1.1.1/24
    ipv6 address 2001:db8:a0b:12f0::1/64
```

## LAG diagnostic dump commands
### LAG diag-dump basic
#### Syntax

```
    diag-dump lacp basic [file]
```

#### Description
This command displays diagnostic information about the system LAGs. If a file is
specified, it captures the information to it.
The information includes the configured, eligible and participant interface
members of all the LAGs in the system. It also includes the amount of PDUs and
marker PDUs sent and received by each interface configured as member of one
dynamic LAG, and the LACP state machine state for each dyanmic LAG in the system.
It also includes the configuration files for the Linux bonding driver for each
LAG in the system.

#### Authority
All users

#### Parameters
| Parameter | Status  | Syntax |   Description  |
|-----------|---------|--------|----------------|
| **file**  | Optional | String | File to capture the command output.|

#### Examples
```
switch# diag-dump lacp basic
=========================================================================
[Start] Feature lacp Time : Wed Apr  6 01:54:44 2016

=========================================================================
-------------------------------------------------------------------------
[Start] Daemon ops-lacpd
-------------------------------------------------------------------------
System Ports:
================ Ports ================
Port lag2:
    lacp                 : active
    lag_member_speed     : 1000
    configured_members   : 5 4
    eligible_members     : 5 4
    participant_members  : 5 4
    interface_count      : 2
Port 1:
    lacp                 : off
    lag_member_speed     : 1000
    configured_members   : 1
    eligible_members     : 1
    participant_members  :
    interface_count      : 0
Port bridge_normal:
    lacp                 : off
    lag_member_speed     : 0
    configured_members   : bridge_normal
    eligible_members     :
    participant_members  :
    interface_count      : 0

LAG interfaces:
Port lag2:
    configured_members   : 5 4
    eligible_members     : 5 4
    participant_members  : 5 4

LACP PDUs counters:
LAG lag2:
 Configured interfaces:
  Interface: 5
    lacp_pdus_sent: 10
    marker_response_pdus_sent: 0
    lacp_pdus_received: 7
    marker_pdus_received: 0
  Interface: 4
    lacp_pdus_sent: 10
    marker_response_pdus_sent: 0
    lacp_pdus_received: 8
    marker_pdus_received: 0

LACP state:
LAG lag2:
 Configured interfaces:
  Interface: 5
    actor_oper_port_state
       lacp_activity:1 time_out:0 aggregation:1 sync:1 collecting:1 distributing:1 defaulted:0 expired:0
    partner_oper_port_state
       lacp_activity:1 time_out:0 aggregation:1 sync:1 collecting:1 distributing:1 defaulted:0 expired:0
    lacp_control
       begin:0 actor_churn:0 partner_churn:0 ready_n:1 selected:1 port_moved:0 ntt:0 port_enabled:1
  Interface: 4
    actor_oper_port_state
       lacp_activity:1 time_out:0 aggregation:1 sync:1 collecting:1 distributing:1 defaulted:0 expired:0
    partner_oper_port_state
       lacp_activity:1 time_out:0 aggregation:1 sync:1 collecting:1 distributing:1 defaulted:0 expired:0
    lacp_control
       begin:0 actor_churn:0 partner_churn:0 ready_n:1 selected:1 port_moved:0 ntt:0 port_enabled:1

-------------------------------------------------------------------------
[End] Daemon ops-lacpd
-------------------------------------------------------------------------
-------------------------------------------------------------------------
[Start] Daemon ops-portd
-------------------------------------------------------------------------
Configuration file for lag2:
Ethernet Channel Bonding Driver: v3.7.1 (April 27, 2011)

Bonding Mode: load balancing (xor)
Transmit Hash Policy: layer2 (0)
MII Status: up
MII Polling Interval (ms): 0
Up Delay (ms): 0
Down Delay (ms): 0

Slave Interface: 5
MII Status: up
Speed: 10000 Mbps
Duplex: full
Link Failure Count: 0
Permanent HW addr: 70:72:cf:3a:b6:b6
Slave queue ID: 0

Slave Interface: 4
MII Status: up
Speed: 10000 Mbps
Duplex: full
Link Failure Count: 0
Permanent HW addr: 70:72:cf:3a:b6:b6
Slave queue ID: 0

-------------------------------------------------------------------------
[End] Daemon ops-portd
-------------------------------------------------------------------------
=========================================================================
[End] Feature lacp
=========================================================================
Diagnostic dump captured for feature lacp
```
