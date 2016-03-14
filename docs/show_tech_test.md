# Show Tech Test Cases

## Contents

- [1. Positive Test Cases](#1-positive-test-cases)
    - [1.1 Vefify Show tech List Runs Successfully](#11-vefify-show-tech-list-runs-successfully)
    - [1.2 Verify Show tech Running Successfully](#12-verify-show-tech-running-successfully)
    - [1.3 Show tech Feature Running Successfully](#13-show-tech-feature-running-successfully)
    - [1.7 Show tech LAG Feature Running Successfully](#17-show-tech-lag-feature-running-successfully)

- [2. Negative Tests](#2-negative-tests)
    - [2.1 Show tech Individual Command Failure](#21-show-tech-individual-command-failure)
    - [2.2 Show tech Command with extra Parameter](#22-show-tech-command-with-extra-parameter)
    - [2.3 Show tech feature with invalid feature name](#23-show-tech-feature-with-invalid-feature-name)

## 1. Positive Test Cases

##  1.1 Vefify Show tech List Runs Successfully

### Objective
This test case verifies that the show tech infra is up and running, also it is able to list the supported featues.

### Requirements
The requirements for this test case are:
 - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+

```

#### Test Setup
Standalone Switch
### Description
Step:
 - Run `show tech list` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
Test Passes if the show tech list displays the list of supported show tech features successfully

#### Test Fail Criteria
Test fails if the show tech configuration is not successful.  show tech list displays the following error in this Case
`Failed to obtain Show Tech Configuration`




## 1.2 Verify Show tech Running Successfully

### Objective
This test case verifies that the show tech infra is up and running, show tech (all) runs successfully.

### Requirements
The requirements for this test case are:
 - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+

```

#### Test Setup
Standalone Switch

### Description
This test case verifies that the show tech infra is up and running, show tech (all) runs successfully.

### Test Result Criteria
#### Test Pass Criteria
 Show tech runs successfully and prints `Show Tech Commands Executed Successfully`

#### Test Fail Criteria
 Show tech completes with failure and prints `Show Tech Commands Executed with N Failures`




## 1.3 Show tech Feature Running Successfully
### Objective
This test case verifies that the show tech infra is up and running, show tech feature runs successfully.

### Requirements
The requirements for this test case are:
 - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+

```

#### Test Setup
Standalone Switch

### Description
*Steps*
1. Run `show tech list` on vtysh shell
2. Pick one of the Feature listed there
3. Run `show tech FEATURE`, substitute *FEATURE* with the feature name you have picked

### Test Result Criteria
#### Test Pass Criteria
Show tech feature runs successfully and prints `Show Tech Commands Executed Successfully`

#### Test Fail Criteria
Show tech feature completes with failure and prints `Show Tech Commands Executed with N Failures`


## 1.7 Show tech LAG Feature Running Successfully
### Objective
This test case verifies that the show tech LAG is up and running successfully.

### Requirements
The requirements for this test case are:
 - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+

```

#### Test Setup
Standalone Switch

### Description
*Steps*
1. Run `show tech LAG` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
Show tech feature runs successfully and prints `Show Tech Commands Executed Successfully`

#### Test Fail Criteria
Show tech feature completes with failure and prints `Show Tech Commands Executed with N Failures`


## 2. Negative Tests
## 2.1 Show tech Individual Command Failure
### Objective
When a command execute failed, the show tech infra should report the failure.  This test case verifies that part

### Requirements
The requirements for this test case are:
 - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+

```

#### Test Setup
Standalone Switch

### Description

*Steps*
1. Add a non existing show command to the show tech configuration file (/etc/openswitch/supportability/ops_showtech.yaml)
2. For eg., add `show xyklasdflj` and `show opopuhjkhjhflj` under *system* feature configuration
3. Run `show tech system`

### Test Result Criteria
#### Test Pass Criteria
 Show tech completes with failure and prints `Show Tech Commands Executed with N Failures`, N being variable here.

#### Test Fail Criteria
 Show tech didn't report failure


## 2.2 Show tech Command with extra Parameter
### Objective
When unnecessary extra parameters are passed to the show tech commands, we have to error out. This test verifies that behaviour

### Requirements
The requirements for this test case are:
 - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+

```

#### Test Setup
Standalone Switch

### Description
*Steps*
1. Run `show tech system xyklasdflj` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
Show Tech reports the following error
 `% Unknown command.`
#### Test Fail Criteria
no errors printed in the cli


## 2.3 Show tech feature with invalid feature name
### Objective
Run Show tech with invalid feature name. It should error out that the feature is not found

### Requirements
The requirements for this test case are:
 - Switch running openswitch

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+

```

#### Test Setup
Standalone Switch

### Description
*Steps*
1. Run `show tech !@#$%^&*((QWERTYUIOPLFDSAZXCVBNM<>)(&^%$#!` on the vtysh shell

### Test Result Criteria
#### Test Pass Criteria
`Feature !@#$%^&*((QWERTYUIOPLFDSAZXCVBNM<>)(&^%$#! is not supported`  error is printed on console.

#### Test Fail Criteria
No Error Reported
