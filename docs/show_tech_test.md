# Show Tech Test Cases

## Contents

- [1. Positive Test Cases](#1-positive-test-cases)
    - [1.1 Verify Show tech List Runs Successfully](#11-vefify-show-tech-list-runs-successfully)
    - [1.2 Verify Show tech Running Successfully](#12-verify-show-tech-running-successfully)
    - [1.3 Show tech Feature Running Successfully](#13-show-tech-feature-running-successfully)
    - [1.4 Show tech to local file](#14-show-tech-to-local-file)
    - [1.5 Show tech to local file with force](#15-show-tech-to-local-file-with-force)
    - [1.7 Show tech LAG Feature Running Successfully](#17-show-tech-lag-feature-running-successfull
y)
- [2. Negative Tests](#2-negative-tests)
    - [2.1 Show tech Individual Command Failure](#21-show-tech-individual-command-failure)
    - [2.2 Show tech Command with extra Parameter](#22-show-tech-command-with-extra-parameter)
    - [2.3 Show tech feature with invalid feature name](#23-show-tech-feature-with-invalid-feature-name)

## 1. Positive Test Cases

##  1.1 Verify Show tech List Runs Successfully

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
1. Run `show tech list` on vtysh shell.
2. Pick one of the Features listed there.
3. Run `show tech <feature>`, substitute *feature* with the feature name you picked.

### Test Result Criteria
#### Test Pass Criteria
Show tech feature runs successfully and prints `Show Tech Commands Executed Successfully`.

#### Test Fail Criteria
Show tech feature completes with failure and prints `Show Tech Commands Executed with N Failures`.

## 1.4 Show tech to local file
### Objective
This test case verifies whether the show tech output can be successfully written to a local file.

### Requirements
The requirements for this test case are:
 - Switch running OpenSwitch

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
1. Run `show tech localfile showtech.sta` on vtysh shell.
2. Verify that the output of show tech is written successfully to the file **/tmp/showtech.sta**.

### Test Result Criteria
#### Test Pass Criteria
Show tech output written successfully to the given file.

#### Test Fail Criteria
Show tech failed to execute or the output is not stored in the file properly.

## 1.5 Show tech to local file with force
### Objective
User should be able to overwrite an existing file using the **force** option.

### Requirements
The requirements for this test case are:
 - Switch running OpenSwitch

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
1. Run `show tech localfile showtech.sta` on vtysh shell.
2. Run again `show tech localfile showtech.sta` on vtysh shell. Now you should get error indicating that the file already exists.
3. Run the command with the `force` option: `show tech localfile showtech.sta force`.
3. The file should be overwritten. Check the timestamp of show tech output and it should the latest one.

### Test Result Criteria
#### Test Pass Criteria
Show tech file successfully overwritten using `force` option.

#### Test Fail Criteria
Show tech failed or the `force` option failed to overwrite the existing file.


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
When a show command specified in the configuration file fails to execute, the show tech command should report the failure.

### Requirements
The requirements for this test case are:
 - Switch running OpenSwitch

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
1. Add a invalid show command to the show tech configuration file (`/etc/openswitch/supportability/ops_showtech.yaml`). For example, add `show xyklasdflj` and `show opopuhjkhjhflj` under the *system* feature section.
3. Run `show tech system`

### Test Result Criteria
#### Test Pass Criteria
 Show tech completes with failure and prints `Show Tech Commands Executed with N Failures`, with N indicating the number of failures.

#### Test Fail Criteria
 Show tech did not report a failure.


## 2.2 Show tech Command with extra Parameter
### Objective
When unnecessary extra parameters are passed to the show tech commands, we have to error out. This test verifies that behaviour

### Requirements
The requirements for this test case are:
 - Switch running OpenSwitch

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
1. Run `show tech system xyklasdflj` on vtysh shell.

### Test Result Criteria
#### Test Pass Criteria
Show tech reports the following error.
 `% Unknown command.`
#### Test Fail Criteria
No errors are reported.


## 2.3 Show tech feature with invalid feature name
### Objective
Run Show tech with an invalid feature name. It should error out that the feature is not found.

### Requirements
The requirements for this test case are:
 - Switch running OpenSwitch

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
1. Run `show tech !@#$%^&*((QWERTYUIOPLFDSAZXCVBNM<>)(&^%$#!` on the vtysh shell.

### Test Result Criteria
#### Test Pass Criteria
`Feature !@#$%^&*((QWERTYUIOPLFDSAZXCVBNM<>)(&^%$#! is not supported`  is reported.

#### Test Fail Criteria
No error is reported.
