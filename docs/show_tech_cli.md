# Show Tech Commands
## Contents
- [Display commands](#display-commands)
    - [show tech](#show-tech)
    - [show tech list](#show-tech-list)
    - [show tech feature](#show-tech-feature)
    - [Show tech to file](#show-tech-to-file)

## Display commands

### show tech
#### Syntax
`show tech`
#### Description
Displays detailed information about the switch by automatically running the collection of `show` commands associated with switch features. The show commands associated with a feature are defined in the show tech configuration file (`ops-supportability/conf/ops_showtech.yaml`).

#### Authority
All users.

#### Parameters
None.

#### Example
This example shows a truncated version of the information returned by the `show tech` command. The *system* feature results in the running of three show commands: `show version`, `show system`, and `show vlan`.

```
switch# show tech
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

Serial Number       : X0000000            Label Revision      : L01

ONIE Version        : 2014.08.00.05       DIAG Version        : 1.0.0.0
Base MAC Address    : xx:xx:xx:xx:xx:xx   Number of MACs      : 74
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


### show tech list
#### Syntax
`show tech list`
#### Description
Lists all features that are supported by the show tech command.

#### Authority
All users.
#### Parameters
None.
#### Example

```
switch# show tech list
Show Tech Supported Features List
-----------------------------------------------------------
Feature                    Desc
------------------------------------------------------------
system                     Show Tech System
lldp                       Link Layer Discovery Protocol

```

### show tech feature
#### Syntax
`show tech <feature>`
#### Description
Runs all `show` commands that are defined for the specified feature.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *feature* | Required | String | Feature name as displayed by the `show tech list` command. |
#### Example

```
swtich# show tech system
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

Serial Number       : X0000000            Label Revision      : L01

ONIE Version        : 2014.08.00.05       DIAG Version        : 1.0.0.0
Base MAC Address    : xx:xx:xx:xx:xx:xx   Number of MACs      : 74
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
### Show tech to file
#### Syntax
`show tech [<feature>] localfile <filename> [force]`

#### Description
Saves the output of the show tech command to a file.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *feature* | Optional | String | Feature name as displayed by the `show tech list` command. |
| *filename* | Required | String | Name of the file where output of the command  is saved. If the specified file already exisits, it is not overwritten.|
| *force* | Optional | Literal | If the specified output file exists, it is overwritten. |

#### Examples
```
switch# show tech basic localfile stbasic.sta
Show Tech output stored in file /tmp/stbasic.sta

switch# show tech basic localfile stbasic.sta
/tmp/stbasic.sta already exists, please give different name or use force option to overwrite existing file

switch# show tech basic localfile stbasic.sta force
Show Tech output stored in file /tmp/stbasic.sta

```
