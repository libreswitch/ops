Managing and monitoring switch platform components
======

## Contents
- [Contents](#contents)
- [Overview](#overview)
- [Configuring system](#configuring-system)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
- [CLI](#cli)

## Overview
This guide provides the detail for managing and monitoring platform components on the switch. All the configuration commands work in configure context.
Some of the following switch physical components are:
-Fans
-Temperature sensors
-Power supply modules
-LED
This feature allows you to configure fan speed or LED state.

##Configuring system

### Setting up the basic configuration

1. ++Setting the fan speed++
Fans can be configured to operate at a specified speed with the'fan-speed *(slow medium | fast | max )*' commands. By default all the fans operate at normal speed and change according to the system temperature.
```
switch# configure terminal
switch(config)# fan-speed slow
switch(config)#
```

2. ++Setting LED state++
'led *led-name* *(on | off | flashing)*' lets the user to set the state of the LED . By default all the LEDs will be in off state.
User should know the name of the LED of whose state is to be set.
In the example below *'base-loc'* LED is set to *on*.
```
switch# configure terminal
switch(config)# led base-loc on
switch(config)#
```

### Verifying the configuration
1. ++View the fan information.++
'show system fan' command displays the detailed information of fans in the system.
```
switch#show system fan
Fan information
...............................................................
Name     Speed  Direction      Status        RPM
...............................................................
base-2R  slow  front-to-back  ok            5700
base-5L  slow  front-to-back  ok            6600
base-3L  slow  front-to-back  ok            6600
base-4L  slow  front-to-back  ok            6600
base-5R  slow  front-to-back  ok            5700
base-2L  slow  front-to-back  ok            6650
base-3R  slow  front-to-back  ok            5700
base-1R  slow  front-to-back  ok            5750
base-1L  slow  front-to-back  ok            6700
base-4R  slow  front-to-back  ok            5700
..............................................................
Fan speed override is set to : slow
..............................................................
```
2. ++View the LED information++
The 'show system led' command displays LED information.
```
switch#sh system led
Name           State     Status
.....................................
base-loc       on       ok
```

3. ++View power-supply information++
The 'show system power-supply' command displays detailed power supply information.
```
switch#sh system power-supply
Name           Status
............................
base-1         ok
base-2         Input Fault
```

4. ++View temperature sensor information++
The 'show system temperature' command displays temperature sensor information.
```
switch#sh system temperature
Temperature information
....................................................
            Current
Name     temperature    Status         Fan state
            (in C)
....................................................
base-1    22.00          normal         normal
base-3    18.50          normal         normal
base-2    20.50          normal         normal
```

## CLI

Click [here](/documents/user/system_cli) for the CLI commands related to the system.
