# show events Test Case

## Contents

- [1. Positive Test Case](#positive-test-case)
   -  [Verify show events runs Successfully](#verify-show-events-runs-successfully)
- [2. Negative Test Case](#Negative-test-case)
   -  [show events command failure](#show-events-command-failure)


## 1.Positive Test case

##    Verify show events runs Successfully

###   Objective
This test case verifies that show events infra is up and running.

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
 - Run `show events` on vtysh shell

### Test Result Criteria
#### Test Pass Criteria
Test passes if the show events displays the events are triggered by `lldp enable` and `no lldp enable` on vtysh shell.

#### Test Fail Criteria
Test fails if the show events is not successfull.
