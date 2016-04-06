# Component Test Cases for Show VLOG

## Contents
- [1.Positive Test Cases](#1-positive-test-cases)
    - [1.0 Running show vlog config](#running-show-vlog-config)
    - [1.1 Show vlog daemon](#show-vlog-daemon)
    - [1.2 Show vlog severity](#show-vlog-severity)
    - [1.3 Basic vlog Configuration for daemon](#basic-vlog-configuration
        -for-daemon)
    - [1.4 Basic vlog Configuration for feature](#basic-vlog
        -configuration-for-feature)
    - [1.5 List the supported features for show vlog config](#list-the
        -supported-features-for-show-vlog-config)
    - [1.6 Show vlog daemon with severity](#show-vlog-daemon-with-severity)
    - [1.7 Show vlog severity with daemon](#show-vlog-severity-with-daemon)
- [2.Negative Test Cases](#2-negative-test-cases)
    - [2.0 Show vlog for invalid daemon](#show-vlog-for-invalid-daemon)
    - [2.1 Show vlog for invalid severity](#show-vlog-config-for-invalid-feature)
    - [2.2 Show vlog for invalid subcommand](#show-vlog-for-invalid-subcommand)

# 1.Positive Test Cases
## 1.0  Running show vlog config
### Objective
`show vlog config` command to display the list of features with their log levels of file and syslog destinations.

## Requirements.
Ensure that features related daemons are running. Features related daemons are available in ops_featuremapping.yaml file

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```
#### Test setup
### Description
Caapture the log levels of supported features.

### Test result criteria
#### Test pass criteria
'show vlog config' command displays the features corresponding daemons log levels
of file and syslog destinations on the console.
#### Test fail criteria
 vtysh crash or show vlog failed.

#1.1 show vlog daemon test
### Objective
`show vlog daemon <daemon_name>` command is able to display vlog messages for specific ops-daemon.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```
#### Test Setup
Standalone Switch
### Description
step:
- Run `show vlog daemon ops-ledd` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
`show vlog daemon ops-ledd` command display "show vlog daemon test passed".
#### Test fail criteria
 "show vlog daemon test failed".

#1.2 show vlog severity test
### Objective
`show vlog severity <severity_level>` command is able to display vlog messages for specific severity and above log level.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```
#### Test Setup
Standalone Switch
### Description
step:
- Run `show vlog severity warn` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
"show vlog severity warn" command display "show vlog severity test passed".
#### Test fail criteria
 "show vlog severity test failed".

## 1.3 Basic vlog Configuration for daemon
### Objective
Configure the log level of syslog and file destinations for daemon.

### Requirement
Ensure that daemon running on switch.
### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```
#### Test setup
### Description
Using `vlog daemon <daemon_name> file info` on configuration mode to configure the
log level of syslog or file destination for daemon .

### Test result criteria
#### Test pass criteria
User cant see configuration changes on configuration node .using `show vlog config daemon <daemon_name>`
to obtain configuration changes on Enable mode.
#### Test fail criteria
vtysh crash or vlog configuration failed.

##1.4 Basic vlog Configuration for feature
### Objective
Configure the log level and destination for feature.

### Requirements
Ensure that feature related daemon are running .Feature related daemon are available
in ops_featuremapping.yaml

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```
#### Test setup
### Description
Configure the basic log level for feature using command `vlog feature <feature_name> syslog dbg`
on console.

### Test result criteria
#### Test pass criteria
User cant see configuration changes on configuration node .using `show vlog config feature <feature_name>`
to obtain configuration changes on Enable mode.
#### Test fail criteria
vtysh crash or vlog configuration failed.

## 1.5 List the supported features for show vlog config
### Objective
`show vlog config list` command is able to display list of supported features and descriptions.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```

#### Test Setup
Standalone Switch
### Description
step:
- Run `show vlog config list` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
"show vlog config list" command gives list of supported features with their description.
#### Test fail criteria
"show vlog config list failed".

##1.6 Show vlog daemon with severity.
### Objective
This test verifies the behaviour of 'show vlog daemon <daemon_name> severity <severity_level>'CLI command.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```

#### Test Setup
Standalone Switch
### Description
step:
- Run `show vlog daemon ops-portd severity info` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
This CLI command Displays "show vlog daemon with severity test passed".
#### Test fail criteria
"show vlog daemon with severity failed".

## 1.7 Show vlog severity with daemon.
### Objective
This test verifies the behaviour of `show vlog severity <severity_level> daemon <daemon_name>` CLI command.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```

#### Test Setup
Standalone Switch
### Description
step:
- Run `show vlog severity info daemon ops-portd` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
This CLI command Displays "show vlog severity with daemon test passed".

#### Test fail criteria
"show vlog severity with daemon failed".

# 2.Negative Test Cases
## 2.0 Show vlog for invalid daemon.
### Objective
This test case verifies the behaviour of `show vlog daemon <daemon_name>` CLI command.
when we pass Invalid daemon_name as parameter to CLI.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```
#### Test setup
### Description
Passing Invalid daemon_name as argument to `show vlog daemon <daemon_name>` CLI command.

### Test result criteria
#### Test pass criteria
`show vlog daemon daemon_name` CLI Command results "show vlog for invalid daemon passed".
#### Test fail criteria
vtysh crash or Improper message.

## 2.1 Show vlog for invalid severity
### Objective
This test case verifies the behaviour of `show vlog severity <severity_level>` CLI command.
when we pass Invalid severity level as paramter to CLI.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```
#### Test setup
### Description
Passing Invalid severity level as argument to `show vlog severity <severity_level> CLI command.

### Test result criteria
#### Test pass criteria
`show vlog severity <severity_level>` CLI Command results show vlog for invalid severity passed.
#### Test fail criteria
vtysh crash or Improper message.

## 2.3 Show vlog for invalid subcommand
### Objective
This test case verifies the behviour of `show vlog <name>` CLI command.
when we pass Invalid subcommand as parameter to CLI.

### Requirements
The requirements for this test case are:
  - Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|   ops1  |
|         |
+---------+
```
#### Test setup
### Description
Passing Invalid subcommand as argument to `show vlog <name>` CLI command.

### Test result criteria
#### Test pass criteria
`show vlog <name>` CLI command results show vlog for invalid subcommand passed.
#### Test fail criteria
vtysh crash or Improper message.
