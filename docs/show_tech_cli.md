# Show Tech Commands
## Contents

- [Display commands](#display-commands)
    - [Command summary](#commands-summary)
    - [Show tech](#show-tech)
    - [Show tech list](#show-tech-list)
    - [Show tech feature](#show-tech-feature)
    - [Help text](#help-text)
 
## Display commands
### Command summary
| Command | Usage |
|:--------|:----------|
| **show tech** | Runs show tech for all supported features |
| **show tech list**| Lists all the supported show tech features |
| **show tech FEATURE**| Runs show tech for the feature specified |


### Show tech
#### Syntax
`show tech`
#### Description
Runs the `show tech` command for all the supported features.
#### Authority
All users
#### Examples

```
====================================================
[Begin] Feature system
====================================================


---------------------------------
Command : show version
---------------------------------
OpenSwitch 0.3.0 (Build: developer_image)

---------------------------------
Command : show system
---------------------------------
OpenSwitch Version  : 0.3.0 (Build: developer_image)
Product Name        : OpenSwitch

Vendor              : OpenSwitch
Platform            : Generic-x86-64
Manufacturer        : OpenSwitch
Manufacturer Date   : 09/01/2015 00:00:01

Serial Number       : X8664001            Label Revision      : L01

ONIE Version        : 2014.08.00.05       DIAG Version        : 1.0.0.0
Base MAC Address    : 70:72:cf:d0:bc:e0   Number of MACs      : 74
Interface Count     : 78                  Max Interface Speed : 40000 Mbps

Fan details:

Name           Speed     Status
--------------------------------

LED details:

Name      State     Status
-------------------------

Power supply details:

Name      Status
-----------------------

Temperature Sensors:

Location  Name      Reading(celsius)
------------------------------------

---------------------------------
Command : show vlan
---------------------------------
No vlan is configured
====================================================
[End] Feature system
====================================================

====================================================
[Begin] Feature lldp
====================================================

---------------------------------
Command : show lldp configuration
---------------------------------
LLDP Global Configuration:

LLDP Enabled :No
LLDP Transmit Interval :30
LLDP Hold time Multiplier :4

```

The output is truncated for readability.

### Show tech list
#### Syntax
`show tech list`
#### Description
This command lists all the supported show tech features.
#### Authority
All users
#### Parameters
None
#### Examples

```
ops-as5712# show tech list
Show Tech Supported Features List
-----------------------------------------------------------
Feature                    Desc
------------------------------------------------------------
system                     Show Tech System
lldp                       Link Layer Discovery Protocol

```

### Show tech feature
#### Syntax
`show tech FEATURE`
#### Description
This command runs the show tech for the feature specified.
#### Authority
All users
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **FEATURE** | Required | Feature Name (String) | Feature name as displayed in the show tech list |
#### Examples

```
====================================================
[Begin] Feature system
====================================================

---------------------------------
Command : show version
---------------------------------
OpenSwitch 0.3.0 (Build: developer_image)

---------------------------------
Command : show system
---------------------------------
OpenSwitch Version  : 0.3.0 (Build: developer_image)
Product Name        : OpenSwitch

Vendor              : OpenSwitch
Platform            : Generic-x86-64
Manufacturer        : OpenSwitch
Manufacturer Date   : 09/01/2015 00:00:01

Serial Number       : X8664001            Label Revision      : L01

ONIE Version        : 2014.08.00.05       DIAG Version        : 1.0.0.0
Base MAC Address    : 70:72:cf:d0:bc:e0   Number of MACs      : 74
Interface Count     : 78                  Max Interface Speed : 40000 Mbps

Fan details:

Name           Speed     Status
--------------------------------

LED details:

Name      State     Status
-------------------------

Power supply details:

Name      Status
-----------------------

Temperature Sensors:

Location  Name      Reading(celsius)
------------------------------------

---------------------------------
Command : show vlan
---------------------------------
No vlan is configured
====================================================
[End] Feature system
====================================================

====================================================
Show Tech commands executed successfully
====================================================

```

### Help text
| Command | Help text |
|:--------|:----------|
| **show tech** | Runs show tech for all supported features |
| **show tech list**| Lists all the supported show tech features |
| **show tech FEATURE**| Runs show tech for the feature specified |

#### Example

```
switch# show tech ?
  <cr>
  FEATURE  Run show tech for the feature specified
  list     List all the supported show tech features

switch# show ?
  (other commands are omitted for simplicity)
  tech              Run show tech for all supported features
```
