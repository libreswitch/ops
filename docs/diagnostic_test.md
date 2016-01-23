# Component Test Cases for Diagnostic

## Contents

- [Component Test Cases for Diagnostic](#component-test-cases-for-diagnostic)
    - [Contents](#contents)
    - [List supported feature for diag dump](#list-supported-feature-for-diag-dump)
        - [Objective](#objective)
        - [Requirements](#requirements)
        - [Setup](#setup)
            - [Topology diagram](#topology-diagram)
            - [Test setup](#test-setup)
        - [Description](#description)
        - [Test result criteria](#test-result-criteria)
            - [Test pass criteria](#test-pass-criteria)
            - [Test fail criteria](#test-fail-criteria)
    - [Basic diag dump on console](#basic-diag-dump-on-console)
        - [Objective](#objective)
        - [Requirements](#requirements)
        - [Setup](#setup)
            - [Topology diagram](#topology-diagram)
            - [Test setup](#test-setup)
        - [Description](#description)
        - [Test result criteria](#test-result-criteria)
            - [Test pass criteria](#test-pass-criteria)
            - [Test fail criteria](#test-fail-criteria)
    - [Basic diag dump to given file](#basic-diag-dump-to-given-file)
        - [Objective](#objective)
        - [Requirements](#requirements)
        - [Setup](#setup)
            - [Topology diagram](#topology-diagram)
            - [Test setup](#test-setup)
        - [Description](#description)
        - [Test result criteria](#test-result-criteria)
            - [Test pass criteria](#test-pass-criteria)
            - [Test fail criteria](#test-fail-criteria)
    - [References](#references)

## List supported feature for diag dump

### Objective
"diag-dump list" command is able to display list of supported featues on console.

### Requirements
Switch running openswitch

### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```

#### Test setup
Standalone Switch
### Description
Step:
- Run 'diag-dump list' on vtysh shell.

### Test result criteria


#### Test pass criteria
"diag-dump list" command gives list of supported features with their description.

#### Test fail criteria
"diag-dump list" command blocks for long time or vtysh crashing.

## Basic diag dump on console

### Objective
Capture basic diag dump on stdout of vtysh .

### Requirements
Switch running openswitch
### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
Standalone Switch
### Description
Capture basic diag dump on console  using command 'diag-dump <feature name> basic' .
### Test result criteria
#### Test pass criteria
User can see output with last line as "Diagnostic dump captured for feature" .

#### Test fail criteria
No output on console or exit of vtysh process or missing of
"Diagnostic dump captured for feature" confirms to failure of test case.

## Basic diag dump to given file
### Objective
Capture basic diag dump to given file .

### Requirements
Ensure that feature related daemon are running .Feature related daemon are available in ops_diagdump.yaml file.
### Setup
#### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```
#### Test setup
### Description
Capture basic diag dump into give file using command 'diag-dump <feature name> basic <filename>'.
### Test result criteria
#### Test pass criteria
User can't see output on vtysh and vtysh is free for next command.
Output file contains the diag dump output with string "Diagnostic dump captured for feature".
#### Test fail criteria
vtysh crash or showing output on console confirms failure of test case.

## References
* [Reference 1] 'diagnostic_test.md'
