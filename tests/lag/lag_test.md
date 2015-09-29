
[LAG] Test Cases
=======

 [TOC]

##  [Dynamic LAG: Create LAGs with different names] ##
### Objective ###
To verify a dynamic LAG cannot be created if the name is too long or has unsupported characters.
### Requirements ###
The requirements for this test case are:
 - 1 Switch running Open Switch
### Setup ###
#### Topology Diagram ####
```ditaa

						+----------+
						|          |
						|  dut01   |
						+----------+

```

#### Test Setup ####
Standalone Switch
### Description ###
This test verify a dynamic LAG can be configured using correct names and can not be configured using a name longer than permited or containing unsupported characters.

Steps:
1)      LAG name with value of 1.
2)      LAG name with value of 2000.
3)      Negative: LAG name with special characters or letters.
4)      Negative: LAG name with value 0,-1, 2001.

### Test Result Criteria ###
#### Test Pass Criteria ####
Test will pass if dynamic LAG can be configured using valid name and cannot be configured using name longer than permitted or containing invalid characters.
Steps that should succeed: 1 and 2
Steps that should fail: 3 and 4

#### Test Fail Criteria ####
Test will fail if dynamic LAG can not be configured using valid name or can be configured using invalid name.


##  [Static LAG: Create LAGs with different names] ##
### Objective ###
To verify a static LAG cannot be created if the name is too long or has unsupported characters.
### Requirements ###
The requirements for this test case are:
 - 1 Switch running Open Switch
### Setup ###
#### Topology Diagram ####
```ditaa

						+----------+
						|          |
						|  dut01   |
						+----------+

```

#### Test Setup ####
Standalone Switch
### Description ###
This test verify a static LAG can be configured using correct names and can not be configured using a name longer than permited or containing unsupported characters.

Steps:
1)      LAG name with value of 1.
2)      LAG name with value of 2000.
3)      Negative: LAG name with special characters or letters.
4)      Negative: LAG name with value 0,-1, 2001.

### Test Result Criteria ###
#### Test Pass Criteria ####
Test will pass if static LAG can be configured using valid name and cannot be configured using name longer than permitted or containing invalid characters.
Steps that should succeed: 1 and 2
Steps that should fail: 3 and 4

#### Test Fail Criteria ####
Test will fail if dynamic LAG can not be configured using valid name or can be configured using invalid name.



##  [Static LAG: Verify interface can be moved to a different LAG] 

### Objective ###
To move an interface associated with an static LAG to another static LAG

### Requirements ###
The requirements for this test case are:

 - 1 Switch running Open Switch
 
### Setup ###

#### Topology Diagram ####
```ditaa

						+----------+
						|          |
						|  dut01   |
						+----------+

```
#### Test Setup ####
### Description ###
This test verifies that an interface can be moved from one static LAG to another static LAG

Steps:
1- Configure LAG 1
2- Add interface to LAG 1
3- Configure LAG 2
4- Add interface to LAG 2

### Test Result Criteria ###
#### Test Pass Criteria ####
Interface is on LAG 1 after step 2, and is on LAG 2 after step 4

#### Test Fail Criteria ####
Interface is not on LAG 1 after step 2, or is not on LAG 2 after step 4



##  [Dynamic LAG: Verify interface can be moved to a different LAG] 

### Objective ###
To move an interface associated with an dynamic LAG to another dynamic LAG

### Requirements ###
The requirements for this test case are:

 - 1 Switch running Open Switch
 
### Setup ###

#### Topology Diagram ####
```ditaa

						+----------+
						|          |
						|  dut01   |
						+----------+

```
#### Test Setup ####
### Description ###
This test verifies that an interface can be moved from one dynamic LAG to another dynamic LAG

Steps:
1- Configure LAG 1
2- Add interface to LAG 1
3- Configure LAG 2
4- Add interface to LAG 2

### Test Result Criteria ###
#### Test Pass Criteria ####
Interface is on LAG 1 after step 2, and is on LAG 2 after step 4

#### Test Fail Criteria ####
Interface is not on LAG 1 after step 2, or is not on LAG 2 after step 4



##  [Static LAG: Create LAG with non-consecutive interfaces] 

### Objective ###
To move an interface associated with a static LAG to another static LAG

### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 Workstations
 
### Setup ###

#### Topology Diagram ####
```ditaa

						+-----------+
						|workstation|
						|    01     |
						+-----------+
						      |
						+----------+
						|          |
						|  dut01   |
						+----------+
						    ||         LAG 1
						+----------+
						|          |
						|  dut02   |
						+----------+
						     |
						+-----------+
						|workstation|
						|    02     |
						+-----------+
```
#### Test Setup ####
### Description ###
This test verifies that a static LAG can be configured using non consecutive interfaces

Steps:
1- Configure LAG 1
2- Add non consecutive interfaces to LAG 1 (example: 1 and 3)
3- Configure workstations
4- Ping between workstations

### Test Result Criteria ###
#### Test Pass Criteria ####
Ping between workstation is successful

#### Test Fail Criteria ####
Ping doesn't reach the other side


##  [Dynamic LAG: Create LAG with non-consecutive interfaces] 

### Objective ###
To move an interface associated with a dynamic LAG to another dynamic LAG

### Requirements ###
The requirements for this test case are:

 - 2 Switches running Open Switch
 - 2 Workstations
 
### Setup ###

#### Topology Diagram ####
```ditaa

						+-----------+
						|workstation|
						|    01     |
						+-----------+
						      |
						+----------+
						|          |
						|  dut01   |
						+----------+
						    ||         LAG 1
						+----------+
						|          |
						|  dut02   |
						+----------+
						     |
						+-----------+
						|workstation|
						|    02     |
						+-----------+
```
#### Test Setup ####
### Description ###
This test verifies that a dynamic LAG can be configured using non consecutive interfaces

Steps:
1- Configure LAG 1
2- Add non consecutive interfaces to LAG 1 (example: 1 and 3)
3- Configure workstations
4- Ping between workstations

### Test Result Criteria ###
#### Test Pass Criteria ####
Ping between workstation is successful

#### Test Fail Criteria ####
Ping doesn't reach the other side
