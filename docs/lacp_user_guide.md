# LACP

## Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuring LACP](#configuring-lacp)
	- [Creating and adding interfaces to LAG](#creating-and-adding-interfaces-to-lag)
	- [Removing interfaces and deleting LAG](#removing-interfaces-and-deleting-lag)
	- [Setting up LACP global parameters](#setting-up-lacp-global-parameters)
	- [Setting up LAG parameters](#setting-up-lag-parameters)
	- [Setting up interface LACP parameters](#setting-up-interface-lacp-parameters)
	- [Verifying the configuration](#verifying-the-configuration)
		- [Viewing LACP global information](#viewing-lacp-global-information)
		- [Viewing LACP aggregate information](#viewing-lacp-aggregate-information)
		- [Viewing LACP interface details](#viewing-lacp-interface-details)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The Link Aggregation Control Protocol (LACP) is one method of bundling several physical interfaces to form one logical interface. LACP exchanges are made between **actors** and **partners**. An **actor** is the local interface in an LACP exchange. A **partner** is the remote interface in an LACP exchange. LACP is defined in IEEE 802.3ad, Aggregation of Multiple Link Segments.

- In **dynamic mode**, local Link Aggregation Groups (LAGs) are aware of partner switch LAGs. Interfaces configured as dynamic LAGs are designated as active or passive.
— **Active** interfaces initiate LACP negotiations by sending LACP PDUs when forming a channel with an interface on the remote switch.
— **Passive** interfaces participate in LACP negotiations initiated by remote switch, but are not allowed to initiate such negotiations.

- In **static** mode, switch LAGs are created without the awareness of their partner switch LAGs. Packets may drop when  LAG static aggregate configurations differ between switches. The switch aggregates static links without LACP negotiation.

## Prerequisites
All the switch interfaces (at least the interfaces that are connected to other devices) must be administratively up.

## Configuring LACP
### Creating and adding interfaces to LAG
1. Configure the terminal to change the vtysh context to config context with the following commands:
```
ops-xxxx# configure terminal
ops-xxxx(config)#
```

2. Create a LAG with the following command:
```
ops-xxxx(config)# interface lag 100
ops-xxxx(config-lag-if)#
```
After creating the LAG, the CLI drops into LAG interface context and allows you to configure specific LAG parameters.

3. Add interfaces to LAG.
A maximum of eight physical interfaces can be added to a LAG. Configure the terminal to change the context to interface context and then add the interface to LAG.
```
ops-xxxx(config)# interface 1
ops-xxxx(config-if)# lag 100
ops-xxxx(config-if)#
```

### Removing interfaces and deleting LAG
1. Configure the terminal to change the vtysh context to config context with the following commands:
```
ops-xxxx# configure terminal
ops-xxxx(config)#
```

2. Delete the LAG with the following command:
```
ops-xxxx(config)# no interface lag 100
```
After deleting the LAG, the interfaces associated with the LAG behave as L3 interfaces.

3. Remove interfaces from the LAG.
```
ops-xxxx(config)# interface 1
ops-xxxx(config-if)# no lag 100
ops-xxxx(config-if)#
```

### Setting up LACP global parameters

1. Setting the LACP **system priority**.
```
ops-xxxx(config)# lacp system-priority 100
ops-xxxx(config)#
```
The `no lacp system-priority` commands reverts the LACP system-priority to its default value of 65534.
```
ops-xxxx(config)# no lacp system-priority
ops-xxxx(config)#
```
In LACP negotiations, link status decisions are made by the system with the numerically lower priority.

### Setting up LAG parameters

1. Setting the LACP **mode**.
LACP mode allows values such as **active**, **passive** and **off**.  The default value is **off**.
The following example displays how to set the LACP mode commands to active, passive, or off.
```
ops-xxxx(config-lag-if)# lacp mode active
ops-xxxx(config-lag-if)# lacp mode passive
ops-xxxx(config-lag-if)# no lacp mode {active / passive}
```
2. Setting the **hash type**.
The Hash type takes the value of **l2-src-dst**, **l3-src-dst** or **l4-src-dst** to control the selection of a interface in a group of aggregate interfaces. This Hash type value helps transmit a frame.
The default hash type is **l3-src-dst**.
```
ops-xxxx(config-lag-if)# hash l2-src-dst
```

3.  Setting the LACP **rate**.
LACP rate takes values **slow** and **fast**. By default **slow**.
When configured to be fast, LACP heartbeats are requested at a rate of once per second causing connectivity issues to be detected quickly. In slow mode, heartbeats are requested at a rate of once every 30 seconds.
```
ops-xxxx(config-lag-if)# lacp rate fast
no form of 'lacp rate fast' sets the rate to slow.
ops-xxxx(config-lag-if)# no lacp rate fast
```

### Setting up interface LACP parameters

1. Setting the LACP **port-id**.
The LACP port-id is used in LACP negotiations to identify individual ports participating in aggregation.
The LACP port-id takes values in the range of 1 to 65535.
```
ops-xxxx(config-if)# lacp port-id 100
```

2. Setting the LACP **port-priority**.
The LACP port-priority is used in LACP negotiations. In LACP negotiations interfaces with numerically lower priorities are preferred for aggregation.
The LACP port-priority takes values in the range of 1 to 65535.
```
ops-xxxx(config-if)# lacp port-priority 100
```

### Verifying the configuration
##### Viewing LACP global information
The `show lacp configuration` command displays global LACP configuration information.
```
ops-xxxx# show lacp configuration
System-id       : 70:72:cf:ef:fc:d9
System-priority : 65534
```

##### Viewing LACP aggregate information
The `show lacp aggregates` command displays information about all LACP aggregates.

```
ops-xxxx# show lacp aggregates
Aggregate-name          : lag100
Aggregated-interfaces   :
Heartbeat rate          : slow
Fallback                : false
Hash                    : l3-src-dst
Aggregate mode          : off

>Aggregate-name         : lag200
Aggregated-interfaces   :
Heartbeat rate          : slow
Fallback                : false
Hash                    : l3-src-dst
Aggregate mode          : off
```
The `show lacp aggregates [lag-name]` command displays information about specified LAG.

```
ops-xxxx# show lacp aggregates lag100
Aggregate-name          : lag100
Aggregated-interfaces   :
Heartbeat rate          : slow
Fallback                : false
Hash                    : l3-src-dst
Aggregate mode          : off
```

##### Viewing LACP interface details
The `show lacp interfaces` command displays LACP interface configuration.

```
ops-xxxx# show lacp interfaces
State abbreviations :
A - Active        P - Passive      F - Aggregable I - Individual
S - Short-timeout L - Long-timeout N - InSync     O - OutofSync
C - Collecting    D - Distributing
X - State m/c expired              E - Default neighbor state

Actor details of all interfaces:
------------------------------------------------------------------------------
Intf Aggregate Port    Port     Key  State   System-id         System   Aggr
     name      id      Priority                                Priority Key
------------------------------------------------------------------------------
3    lag200    69      1        200  ALFNCD  70:72:cf:37:a3:5c 20       200
2    lag200    14      1        200  ALFNCD  70:72:cf:37:a3:5c 20       200
4    lag200    26      1        200  ALFNCD  70:72:cf:37:a3:5c 20       200
1    lag500    17      1        500  ALFNCD  70:72:cf:37:a3:5c 20       500


Partner details of all interfaces:
------------------------------------------------------------------------------
Intf Aggregate Partner Port     Key  State   System-id         System   Aggr
     name      Port-id Priority                                Priority Key
------------------------------------------------------------------------------
3    lag200    69      1        200  PLFNC   70:72:cf:8c:60:a7 65534    200
2    lag200    14      1        200  PLFNC   70:72:cf:8c:60:a7 65534    200
4    lag200    26      1        200  PLFNCD  70:72:cf:8c:60:a7 65534    200
1    lag500    18      1        500  PLFNCD  70:72:cf:8c:60:a7 65534    500
```

## CLI
Click [here](/documents/user/lacp_cli) for the CLI commands related to the LACP feature.
## Related features
When configuring the switch for LACP, it might also be necessary to configure the physical interface. [Physical Interface](/documents/user/interface_user_guide).
