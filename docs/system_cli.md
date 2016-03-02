System commands
======

## Contents

- [System configuration commands](#system-configuration-commands)
	- [Setting the fan speed](#setting-the-fan-speed)
	- [Unsetting the fan speed](#unsetting-the-fan-speed)
	- [Setting an LED state](#setting-an-led-state)
	- [Unsetting an LED state](#unsetting-an-led-state)
- [System Display Commands](#system-display-commands)
        - [Showing package information](#showing-package-information)
	- [Showing system information](#showing-system-information)
	- [System fan information](#system-fan-information)
	- [Showing system temperature information](#showing-system-temperature-information)
	- [Showing system LED information](#showing-system-led-information)
	- [Showing system power-supply information](#showing-system-power-supply-information)


## System configuration commands
### Setting the fan speed
#### Syntax
`fan-speed < normal | slow | medium | fast | maximum >`

#### Description
This command globally sets the fan speed to the value indicated by command parameter. This command overrides the fan speed set internally by platform. The fan speed value set by the user takes effect depending on platform cooling requirements.

#### Authority
All users.

#### Parameters
This command takes one of the following values:
- slow
- normal
- medium
- fast
By default fans operate at normal speed.

| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------------|
| *slow* | choose one| Literal | set fan speed to slow, which is 25% of maximum speed |
| *normal* | choose one| Literal | set fan speed to normal, which is 40% of maximum speed  |
| *medium* | choose one| Literal | set fan speed to medium, which is 65% of maximum speed|
| *fast* | choose one| Literal | set fan speed to fast, which is 80% of maximum speed|
| *max* | choose one| Literal | set fan speed to maximum |

#### Examples

```
switch(config)#fan-speed slow
```

### Unsetting the fan speed
#### Syntax
`no fan-speed [< normal | slow | medium | fast | maximum >]`

#### Description
This command removes the configured fan speed and sets it to the default speed.

#### Authority
All users.

#### Parameters

| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------------|
| *slow* | optional(choose one)| Literal | set fan speed to slow, which is 25% of maximum speed |
| *normal* |optional(choose one)| Literal | set fan speed to normal, which is 40% of maximum speed | 
| *medium* | optional(choose one)| Literal | set fan speed to medium, which is 65% of maximum speed|
| *fast* | optional(choose one)| Literal | set fan speed to fast, which is 80% of maximum speed|
| *max* | optional(choose one)| Literal | set fan speed to maximum |

#### Examples
```
switch(config)#no fan-speed
```

### Setting an LED state
#### Syntax
`led < led-name > < on | flashing | off >`

#### Description
This command sets the LED state to **on**, **off**, or **flashing**. By default, the LED state is off.

#### Authority
All users.

#### Parameters
| Parameter 1| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *led-name* | Required | Literal |LED name of whose state is to be set |


| Parameter 2| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *off* | choose one| Literal |Select this to switch off LED |
| *on* | choose one| Literal  | Select this to switch on LED |
| *flashing*| choose one|Literal | Select this to blink/flash the LED|

#### Examples
```
switch(config)#led base-loc on
```

### Unsetting an LED state
#### Syntax
`no led <led-name> [< on | flashing | off >]`

#### Description
This command turns off the LED.

#### Authority
All users.

#### Parameters
| Parameter 1| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *led-name* | Required | Literal | LED name of whose state is to be set |


| Parameter 2| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *off* | Optional(choose one)| Literal |Select this to switch the LED off |
| *on* | Optional (choose one)| Literal  | Select this to switch the LED on |
| *flashing*| Optional (choose one)|Literal | Select this to blink/flash the LED|


#### Examples
```
switch(config)#no led base-loc
```

## System display commands
### Showing package information
#### Syntax
`show version detail`

#### Description
This command lists every package present in the switch image under the PACKAGE
column. The VERSION column displays the git hash value if the SOURCE URL is a
git repository. If not, the VERSION column displays the version string of the
package. SOURCE TYPE displays the type of source pointed to by SOURCE URL.
SOURCE URL displays the download location for the source-code of the
corresponding package in the SOURCE URI column. If version information and/or
Source URL is not available during build-time, `show version detail` displays
'NA' (Not Available).

#### Authority
All users.

#### Parameters
This command does not require a parameter.

#### Examples
```
switch#show version detail
PACKAGE     : kernel-module-gspca-spca1528
VERSION     : 3.14.36+gitAUTOINC+a996d95104_dbe5b52e93
SOURCE TYPE : git
SOURCE URL  : https://git.yoctoproject.org/linux-yocto-3.14.git;bareclone=1;branch=standard/common-pc-64/base,meta;name=machine,meta

PACKAGE     : python-jsonpatch
VERSION     : 1.11
SOURCE TYPE : http
SOURCE URL  : http://pypi.python.org/packages/source/j/jsonpatch/jsonpatch-1.11.tar.gz

PACKAGE     : ops-cli
VERSION     : a70df32190755dabf3fb404c3cde04a03aa6be40~DIRTY
SOURCE TYPE : other
SOURCE URL  : NA

PACKAGE     : dbus-1
VERSION     : NA
SOURCE TYPE : other
SOURCE URL  : NA
```

### Showing system information
#### Syntax
`show system [ < fan | temperature [ detail ] | led | power-supply >]`

#### Description
Using no parameter, this command shows the overall system details including information about physical components such as the fan, temperature sensor, LED, power supply, etc. Using a parameter, this command gives detailed information of various physical components.

#### Authority
All users.

#### Parameters
| Parameter 1 | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *fan* | choose one| Literal | To display fan information |
| *temperature * | choose one| Literal | To display temperature-sensor information |
| *led* | choose one| Literal | To display LED information |
| *power-supply* | choose one| Literal | To display power-supply information |

| Parameter 2 | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *detail* | Optional | Literal | To display detailed temperature-sensor information |

#### Examples
```
switch#show system
OpenSwitch Version  :
Product Name        : 5712-54X-O-AC-F
Vendor              : Edgecore
Platform            : x86_64-accton_as5712_54x-r0
Manufacturer        : Accton
Manufacturer Date   : 03/24/2015 02:05:30
Serial Number       : 571254X1512035      Label Revision      : R01H
ONIE Version        : 2014.08.00.05       DIAG Version        : 2.0.1.0
Base MAC Address    : 70:72:cf:fd:e9:b9   Number of MACs      : 74
Interface Count     : 78                  Max Interface Speed : 40000 Mbps

Fan details:
Name           Speed     Status
--------------------------------
base-1L        normal    ok
base-1R        normal    ok
base-2L        normal    ok
base-2R        normal    ok
base-3L        normal    ok
base-3R        normal    ok
base-4L        normal    ok
base-4R        normal    ok
base-5L        normal    ok
base-5R        normal    ok

LED details:

Name      State     Status
-------------------------
base-loc  on        ok
Power supply details:
Name      Status
-----------------------

base-1    ok
base-2    Input Fault
Temperature Sensors:
Location                                          Name      Reading(celsius)
---------------------------------------------------------------------------
front                                             base-1    21.00
side                                              base-3    18.00
back                                              base-2    20.00
```

### System fan information
#### Syntax
`show system fan`
#### Description
This command displays detailed fan information.
#### Authority
All users
#### Parameters
This command does not require a parameter
#### Example
```
switch#show system fan

Fan information
------------------------------------------------------
Name         Speed  Direction      Status        RPM
------------------------------------------------------
base-2L      normal front-to-back  ok            9600
base-5R      normal front-to-back  ok            8100
base-3R      normal front-to-back  ok            8100
base-4R      normal front-to-back  ok            8100
base-3L      normal front-to-back  ok            9600
base-5L      normal front-to-back  ok            9600
base-1R      normal front-to-back  ok            8100
base-1L      normal front-to-back  ok            9600
base-2R      normal front-to-back  ok            7950
base-4L      normal front-to-back  ok            9600
------------------------------------------------------
Fan speed override is not configured
------------------------------------------------------
```
### Showing system temperature information
#### Syntax
`
show system temperature { detail }
`
#### Description
This command displays detailed temperature sensor information. If a parameter is not used, the command displays brief temperature information.

#### Authority
All users.

#### Parameters
| Parameter  | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *detail* | Optional | Literal | To display detailed temperature-sensor information |

#### Example
```
switch#show system temperature

Temperature information
---------------------------------------------------
            Current
Name      temperature    Status         Fan state
            (in C)
---------------------------------------------------
base-1    21.50          normal         normal
base-3    18.50          normal         normal
base-2    20.50          normal         normal
```
```
switch#show system temperature detail

Detailed temperature information
---------------------------------------------------
Name                      :base-1
Location                  :front
Status                    :normal
Fan-state                 :normal
Current temperature(in C) :21.50
Minimum temperature(in C) :19.50
Maximum temperature(in C) :22.00

Name                      :base-3
Location                  :side
Status                    :normal
Fan-state                 :normal
Current temperature(in C) :18.50
Minimum temperature(in C) :17.50
Maximum temperature(in C) :19.50

Name                      :base-2
Location                  :back
Status                    :normal
Fan-state                 :normal
Current temperature(in C) :20.50
Minimum temperature(in C) :18.50
Maximum temperature(in C) :21.00

```

### Showing system LED information
#### Syntax
`show system led`

#### Description
This command displays detailed LED information.

#### Authority
All users

#### Parameters
This command does not require a parameter.

#### Example
```
switch#show system led

Name           State     Status
-----------------------------------
base-loc       on        ok
```

### Showing system power-supply information

#### Syntax
`show system power-supply`

#### Description
This command displays detailed power-supply information.

#### Authority
All users.

#### Parameters
This command does not require a parameter.

#### Examples
```
switch#show system power-supply
Name           Status
-----------------------------
base-1         ok
base-2         Input Fault
```
