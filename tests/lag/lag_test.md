
LAG Test Cases
=======

## Contents

* [Create dynamic LAGs with different names](#create-dynamic-lags-with-different-names)
* [Create static LAGs with different names](#create-static-lags-with-different-names)
* [Verify interface can be moved from a static LAG to another](#verify-interface-can-be-moved-from-a-static-lag-to-another)
* [Verify interface can be moved from a dynamic LAG to another](#verify-interface-can-be-moved-from-a-dynamic-lag-to-another)
* [Create static LAG with nonconsecutive interfaces](#create-static-lag-with-nonconsecutive-interfaces)
* [Create dynamic LAG with nonconsecutive interfaces](#create-dynamic-lag-with-nonconsecutive-interfaces)
* [Convert dynamic LAG to static LAG](#convert-dynamic-lag-to-static-lag)
* [Delete dynamic LAG with minimum number of members](#delete-dynamic-lag-with-minimum-number-of-members)
* [Delete dynamic LAG with max number of members](#delete-dynamic-lag-with-max-number-of-members)
* [Delete nonexistent dynamic LAGs](#delete-nonexistent-dynamic-lags)
* [Modify number of dynamic LAG members lower limits](#modify-number-of-dynamic-lag-members-lower-limits)
* [Modify number of dynamic LAG members upper limits](#modify-number-of-dynamic-lag-members-upper-limits)
* [Convert static LAG to dynamic LAG](#convert-static-lag-to-dynamic-lag)
* [Delete static LAG with minimum number of members](#delete-static-lag-with-minimum-number-of-members)
* [Delete static LAG with max number of members](#delete-static-lag-with-max-number-of-members)
* [Delete nonexistent static LAGs](#delete-nonexistent-static-lags)
* [Modify number of static LAG members upper limits](#modify-number-of-static-lag-members-upper-limits)
* [Modify dynamic LAG without changing any setting](#modify-dynamic-lag-without-changing-any-setting)
* [Modify static LAG without changing any setting](#modify-static-lag-without-changing-any-setting)
* [Verify communication between 2 switches connected by L3 dynamic LAGs](#verify-communication-between-2-switches-connected-by-l3-dynamic-lags)
* [Verify communication between 2 switches connected by L3 static LAGs](#verify-communication-between-2-switches-connected-by-l3-static-lags)
* [Verify LAG interface functionality when using command shutdown for LAG](#verify-lag-interface-functionality-when-using-command-shutdown-for-lag)
* [Verify communication between 2 switches connected by L2 dynamic LAGs](#verify-communication-between-2-switches-connected-by-l2-dynamic-lags)
* [Verify communication between 2 switches connected by L2 static LAGs](#verify-communication-between-2-switches-connected-by-l2-static-lags)
* [Change static LAG from L2 to L3 and viceversa](#change-static-lag-from-l2-to-l3-and-viceversa)
* [Change interface from L2 LAG to L3 LAG and viceversa](#change-interface-from-l2-lag-to-l3-lag-and-viceversa)
* [Static LAG statistics basic summary](#static-lag-statistics-basic-summary)
* [Dynamic LAG statistics basic summary](#dynamic-lag-statistics-basic-summary)
* [Static LAG statistics when aggregation members change](#static-lag-statistics-when-aggregation-members-change)
* [Dynamic LAG statistics when aggregation members change](#dynamic-lag-statistics-when-aggregation-members-change)
* [LAG statistics cleanup on aggregation recreation](#lag-statistics-cleanup-on-aggregation-recreation)

## Create dynamic LAGs with different names
### Objective
To verify a dynamic LAG cannot be created if the name is too long or if it has unsupported characters.
### Requirements
The requirements for this test case are:

 - 1 Switch running OpenSwitch
 - **FT file**: `ops/tests/lag/lagDynamicSupportedAndUnsupportedNames.py`

### Setup
#### Topology diagram
```ditaa
                        +----------+
                        |          |
                        |  dut01   |
                        +----------+
```

#### Test setup
Standalone switch
### Description
This test passes if the dynamic LAG can be configured using valid names and cannot be configured using names longer than permitted or names containing invalid characters.

To test that a LAG can be configured:
-Configure a LAG with a LAG name that has a value of 1.
-Configure a LAG with a LAG name that has a value of 2000.
To test that a LAG cannot be configured:
-Configure a LAG with a LAG name that contains special characters or letters.
-Configure a LAG with a LAG name that has a value of 0, -1 or 2001.

### Test result criteria
#### Test pass criteria
Test will pass if dynamic LAG can be configured using valid name and cannot be configured using name longer than permitted or containing invalid characters.

#### Test fail criteria
This test fails if the dynamic LAG cannot be configured using valid names or can be configured using an invalid name.


## Create static LAGs with different names
### Objective
To verify that a static LAG cannot be created if the name is too long or if it has unsupported characters
### Requirements
The requirements for this test case are:

 - 1 Switch running OpenSwitch
 - **FT file**: `ops/tests/lag/lagStaticSupportedAndUnsupportedNames.py`

### Setup
#### Topology diagram
```ditaa
                        +----------+
                        |          |
                        |  dut01   |
                        +----------+
```

#### Test setup
Standalone switch
### Description
This test verifies that a static LAG can be configured using correct names and cannot be configured if it uses a name longer than permitted or if if the name contains unsupported characters.

To test that a LAG can be configured:
-Configure a LAG with a LAG name that has a value of 1.
-Configure a LAG with a LAG name that has a value of 2000.
To test that a LAG cannot be configured:
-Configure a LAG with a LAG name that contains special characters or letters.
-Configure a LAG with a LAG name that has a value of 0, -1 or 2001

### Test result criteria
#### Test pass criteria
This test passes if the static LAG can be configured using valid names and cannot be configured using names that are longer than permitted or using names that contain invalid characters.

#### Test fail criteria
This test fails if the dynamic LAG cannot be configured using a valid name or if it can be configured using an invalid name.



## Verify interface can be moved from a static LAG to another

### Objective
To move an interface associated with an static LAG to another static LAG.

### Requirements
The requirements for this test case are:

 - 1 Switch running OpenSwitch
 - **FT file**: `ops/tests/lag/lagStaticInterfacesOnOtherLAG.py`

### Setup

#### Topology diagram
```ditaa
                        +----------+
                        |          |
                        |  dut01   |
                        +----------+
```
#### Test setup
### Description
This test verifies that an interface can be moved from one static LAG to another static LAG.

To move an interface from one static LAG to another static LAG:
1. Configure LAG 1
2. Add an interface to LAG 1
3. Configure LAG 2
4. Add the same interface to LAG 2 to move it

### Test result criteria
#### Test pass criteria
This test passes if the interface is on LAG 1 after step 2 and it is moved to LAG 2 after step 4.

#### Test fail criteria
This test fails if the interface is not on LAG 1 after step 2, nor is it on LAG 2 after step 4.



## Verify interface can be moved from a dynamic LAG to another

### Objective
To move an interface associated with a dynamic LAG to another dynamic LAG.

### Requirements
The requirements for this test case are:

 - 1 Switch running OpenSwitch
 - **FT file**: `ops/tests/lag/lagDynamicInterfacesOnOtherLAG.py`

### Setup

#### Topology diagram
```ditaa
                        +----------+
                        |          |
                        |  dut01   |
                        +----------+
```
#### Test setup
### Description
This test verifies that an interface can be moved from one dynamic LAG to another dynamic LAG.

To move an interface from one dynamic LAG to another dynamic LAG:
1. Configure LAG 1
2. Add an interface to LAG 1
3. Configure LAG 2
4. Add the same interface to LAG 2 to move it

### Test result criteria
#### Test pass criteria
This test passes if the interface is on LAG 1 after step 2 and it is moved to LAG 2 after step 4.

#### Test fail criteria
This test fails if the interface is not on LAG 1 after step 2, nor is it on LAG 2 after step 4.



## Create static LAG with nonconsecutive interfaces

### Objective
To move an interface associated with a static LAG to another static LAG.

### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations
 - **FT file**: `ops/tests/lag/lagStaticNonConsecutiveInterfaces.py`
 
### Setup

#### Topology diagram
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
#### Test setup
### Description
This test verifies that a static LAG can be configured using non-consecutive interfaces.

To configure a static LAG using non-consecutive interfaces:
1. Configure LAG 1.
2. Add non-consecutive interfaces to LAG 1. For example: add interface 1 and interface 3.
3. Configure the workstations.
4. Ping between the workstations.

### Test result criteria
#### Test pass criteria
This test is effective if pinging between the workstations is successful.

#### Test fail criteria
This test fails if the ping does not reach the other side.


## Create dynamic LAG with nonconsecutive interfaces

### Objective
To move an interface associated with a dynamic LAG to another dynamic LAG.

### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations
 - **FT file**: `ops/tests/lag/lagDynamicNonConsecutiveInterfaces.py`

### Setup

#### Topology diagram
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
#### Test setup
### Description
This test verifies that a dynamic LAG can be configured using non-consecutive interfaces.

To configure a dynamic LAG using non-consecutive interfaces:
1. Configure LAG 1.
2. Add non-consecutive interfaces to LAG 1. For example: add interface 1 and interface 3.
3. Configure the workstations.  
4. Ping between the workstations.

### Test result criteria
#### Test pass criteria
This test is effective if pinging between the workstations is successful.

#### Test fail criteria
This test fails if the ping does not reach the other side.

## Convert dynamic LAG to static LAG
### Objective
To verify that a dynamic LAG can be converted to a dynamic LAG and pass traffic.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations
 - **FT file**: `ops/tests/lacp/DynamicLagConvertToStatic.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |
       |   |     LAG 1
       |   |
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
This test verifies that a dynamic LAG formed between an active and a passive member can be transitioned to a static LAG while retaining the connectivity of clients that are employing the LAG to communicate.

To configure a dynamic LAG to transition to a static LAG:
1. Configure the active LAG on switch 1 and add the 2 interfaces connected to switch 2.
2. Configure the passive LAG on switch 2 and add the 2 interfaces connected to switch 1.
3. Configure the LAG and the workstation's interfaces with the same VLAN.
4. Test the workstation's connectivity.
5. Change the LAGs on both switches to static.
6. Test the workstation's connectivity.

### Test result criteria
#### Test pass criteria

 * The LAGs cannot be converted from dynamic to static.
 * The workstations cannot communicate.

#### Test fail criteria

 * LAGs cannot be converted from dynamic to static.
 * Workstations cannot communicate.

## Delete dynamic LAG with minimum number of members
### Objective
To verify that a dynamic LAG of 2 members or less can be deleted.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations
 - **FT file**: `ops/tests/lacp/DynamicLagDeleteLowNumberOfMembers.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |
       |   |     LAG 1
       |   |
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
This test verifies that a dynamic LAG formed between an active and a passive member can be deleted when it has 2, 1 or 0 members.

To delete a dynamic LAG when it has two, one, or zero members:
 1. Configure the active LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure the passive LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure the LAG and the interfaces of the workstations with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Delete the LAGS and test to check if the connectivity is broken.
 6. Recreate the LAGs with one interface and test to ensure that the connectivity is reestablished.
 7. Delete the LAGS and test to check if the connectivity is broken.
 8. Recreate the LAGs with no interfaces and delete them again.

### Test result criteria
#### Test pass criteria

 * LAGs can be recreated and deleted without errors.
 * Workstations can communicate when a LAG is created with at least one interface.
 * Workstations cannot communicate when LAGs are deleted or the LAG has no interfaces associated.

#### Test fail criteria

 * LAGs cannot be created or deleted or there are errors when doing so.
 * Workstations cannot communicate when a LAG is created with at least 1 interface.
 * Workstations can communicate after deleting a LAG or when the LAG has no associated interfaces.

## Delete dynamic LAG with max number of members
### Objective
To verify that a dynamic LAG that contains 8 members can be deleted.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations
 - **FT file**: `ops/tests/lacp/DynamicLagDeleteMaxNumberOfMembers.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
+--------+--------+
|                 |
|    Switch 1     |
|                 |
+-+-+-+-+-+-+-+-+-+
  | | | | | | | |
  | | | | | | | |    LAG 1
  | | | | | | | |
+-+-+-+-+-+-+-+-+-+
|                 |
|    Switch 2     |
|                 |
+-------+---------+
        |
        |
+-------+---------+
|                 |
|  Workstation 2  |
|                 |
+-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
This test verifies that a dynamic LAG formed between an active and a passive member can be deleted when it has 8 members.

To delete a dynamic LAG when it has 8 members:
 1. Configure the active LAG on switch 1 and add eight interfaces connected to switch 2.
 2. Configure the passive LAG on switch 2 and add the eight interfaces connected to switch 1.
 3. Configure the LAGs and the interfaces of the workstations with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Delete the LAGS and test to check if the connectivity is broken.

### Test result criteria
#### Test pass criteria

 * LAGs can be created and deleted without errors.
 * Workstations can communicate when LAGs are created.
 * Workstations cannot communicate when LAGs are deleted.

#### Test fail criteria

 * LAGs cannot be created or deleted or there are errors when doing so.
 * Workstations cannot communicate when the LAGs are created.
 * Workstations can communicate after deleting the LAGs.

## Delete nonexistent dynamic LAGs
### Objective
To verify attempting to delete nonexistent LAGs will not affect created LAGs.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations
 - **FT file**: `ops/tests/lacp/DynamicLagDeleteNonExistingLags.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |
       |   |     LAG 1
       |   |
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
Tests that a previously configured dynamic link aggregation does not stop forwarding traffic when attempting to delete several nonexistent link aggregations with different names that might not be supported.

To ensure that attempting to delete a nonexistent LAG does not affect the created LAGs:
1. Configure the active LAG on switch 1 and add 2 interfaces connected to switch 2.
2. Configure the passive LAG on switch 2 and add the 2 interfaces connected to switch 1.
3. Configure the LAG and the workstation's interfaces with the same VLAN.
4. Test the workstations' connectivity.
5. Attempt to delete LAGs named XX, 0, -1, 2000, 2001, @%&$#(), 60000, 600,  and 2 on each switch.  At the same time, verify that the created LAG on each switch has not changed.
6. Test the workstations' connectivity.

### Test result criteria
#### Test pass criteria

 * Non-existent LAGs cannot be deleted (an error is displayed).
 * Workstations can communicate.
 * Existing LAGs do not see their configuration altered after attempting to delete the nonexistent LAGs.

#### Test fail criteria

 * Deleting a non-existent LAG is not met with an error.
 * The workstations cannot communicate.
 * Existing LAGs have their configurations modified after attempting to delete the nonexistent LAGs.

## Modify number of dynamic LAG members lower limits
### Objective
To verify that it is possible to modify the lower limits of a LAG.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations`
 - **FT file**: `ops/tests/lacp/DynamicLagModifyLowNumberOfMembers.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +-+---+---+--+
     |   |   |
     |   |   |      LAG 1
     |   |   |
   +-+---+---+--+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup

Workstations have a static IP address each in the same range.

### Description
Tests that a previously configured dynamic link aggregation can be modified to have between zero and two members.

to modify a dynamice link aggregation to have between zero and two members:
 1. Configure the active LAG on switch 1 and add the 3 interfaces connected to switch 2.
 2. Configure the passive LAG on switch 2 and add the 3 interfaces connected to switch 1.
 3. Configure the LAG and interfaces of the workstations with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Remove one interface from each LAG and test the connectivity between workstations.
 6. Add back the interface and test connectivity between workstations.
 7. Remove all the interfaces from the LAGs and test that the connectivity does not work.
 8. Add all the interfaces back into the LAGs and test that the connectivity is restored.
 9. Remove two interfaces from each LAG and test that the connectivity still works.
 10. Move the two interfaces back and test the connectivity.

### Test result criteria
#### Test pass criteria

 * Number of interfaces on the LAGs are modified
 * Workstations cannot communicate with at least one LAG interface still active.

#### Test fail criteria

 * Number of interfaces on the LAGs cannot be modified.
 * Workstations cannot communicate with at least 1 interface on each LAG or they can communicate when there are no interfaces on the LAGs.

## Modify number of dynamic LAG members upper limits
### Objective
To verify it is possible to modify the upper limits of a LAG member.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations`
 - **FT file**: `ops/tests/lacp/DynamicLagModifyMaxNumberOfMembers.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
+--------+--------+
|                 |
|    Switch 1     |
|                 |
+-+-+-+-+-+-+-+-+-+
  | | | | | | | |
  | | | | | | | |    LAG 1
  | | | | | | | |
+-+-+-+-+-+-+-+-+-+
|                 |
|    Switch 2     |
|                 |
+-------+---------+
        |
        |
+-------+---------+
|                 |
|  Workstation 2  |
|                 |
+-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
Tests that a previously configured dynamic link aggregation can be modified to have between seven and eight members.

To modify dynamic link aggregation:
 1. Configure the active LAG on switch 1 and add eight interfaces connected to switch 2.
 2. Configure the passive LAG on switch 2 and add the eight interfaces connected to switch 1.
 3. Configure the LAG and the interfaces of the workstations with the same VLAN.
 4. Test the connectivity of the workstations.   
 5. Remove one interface from each LAG and test the connectivity between the workstations.
 6. Add the interface back in and test the connectivity between the workstations.

### Test result criteria
#### Test pass criteria

 * The number of interfaces on the LAGs are modified.
 * The Workstations can communicate.

#### Test fail criteria

 * The number of interfaces on the LAGs cannot be modified.
 * The workstations cannot communicate.

## Convert static LAG to dynamic LAG
### Objective
To verify that a dynamic LAG can be converted to a static LAG and pass traffic.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations`
 - **FT file**: `ops-lacpd/ops-tests/feature/test_ft_lag_convert_to_lacp.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |
       |   |     LAG 1
       |   |
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
This test verifies that a static LAG formed between two switches can be transitioned to a dynamic LAG with one active member and one passive member while retaining the connectivity of clients employing the LAG to communicate.

To transition a dynamic LAG with one active member and one passive member to static:
 1. Configure the static LAG on switch 1 and add the two interfaces connected to switch 2.
 2. Configure the static LAG on switch 2 and add the two interfaces connected to switch 1.
 3. Configure the LAG and the interfaces of the workstations with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Change the LAGs on both switches to dynamic (one active, the other passive).
 6. Test the connectivity of the workstations.

### Test result criteria
#### Test pass criteria

 * The LAGs are converted from static to dynamic.
 * The workstations can communicate after the change in LAGs.

#### Test fail criteria

 * The LAGs cannot be converted from static to dynamic.
 * The workstations cannot communicate.

## Delete static LAG with minimum number of members
### Objective ###
To verify that a static LAG with two members or less can be deleted.
### Requirements ###
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations`
 - **FT file**: `ops/tests/lacp/StaticLagDeleteLowNumberOfMembers.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |
       |   |     LAG 1
       |   |
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
Tests that a previously configured static link aggregation of two, one, or zero members can be deleted.

To delete a previously configured static link aggregaton with two, one, or zero members:
 1. Configure the static LAG on switch 1 and add the two interfaces connected to switch 2.
 2. Configure the static LAG on switch 2 and add the two interfaces connected to switch 1.
 3. Configure the LAG and the workstation's interfaces with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Delete the LAGs and test if the connectivity is broken.
 6. Recreate the LAGs with one interface and test to ensure that the connectivity is reestablished.
 7. Delete the LAGs and test to check if the connectivity is broken.
 8. Recreate the LAGs without interfaces and delete them again.

### Test result criteria
#### Test pass criteria

 * The LAGs can be recreated and deleted without errors.
 * The workstations can communicate when a LAG is created with at least one interface.
 * The workstations cannot communicate when the LAGs are deleted or if the LAG has no interfaces associated with it.

#### Test fail criteria

 * The LAGs cannot be created or deleted or there are errors when doing so.
 * The Workstations cannot communicate when a LAG is created with at least one interface.
 * The workstations can communicate after deleting the LAG or when the LAG has no interfaces associated with it.

## Delete static LAG with max number of members
### Objective
To verify that a static LAG with eight members can be deleted.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations`
 - **FT file**: `ops/tests/lacp/StaticLagDeleteMaxNumberOfMembers.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
+--------+--------+
|                 |
|    Switch 1     |
|                 |
+-+-+-+-+-+-+-+-+-+
  | | | | | | | |
  | | | | | | | |    LAG 1
  | | | | | | | |
+-+-+-+-+-+-+-+-+-+
|                 |
|    Switch 2     |
|                 |
+-------+---------+
        |
        |
+-------+---------+
|                 |
|  Workstation 2  |
|                 |
+-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
Tests that a previously configured static link aggregation with eight members can be deleted.

To delete a previously configured static link aggregaton with eight members:
 1. Configure the active LAG on switch 1 and add eight interfaces connected to switch 2.
 2. Configure the passive LAG on switch 2 and add eight interfaces connected to switch 1.
 3. Configure the LAG and the interfaces of the workstations with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Delete the LAGS and test if the connectivity is broken.

### Test result criteria
#### Test pass criteria

 * The LAGs can be created and deleted without errors.
 * The workstations can communicate when the LAGs are created.
 * The workstations cannot communicate when the LAGs are deleted.

#### Test fail criteria

 * The LAGs cannot be created or deleted or there are errors when doing so.
 * The workstations cannot communicate when the LAGs are created.
 * The workstations can communicate after deleting the LAGs.

## Delete nonexistent static LAGs
### Objective
To verify that attempting to delete a non-existent LAG will not affect LAGs already created.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations`
 - **FT file**: `ops/tests/lacp/StaticLagDeleteNonExistingLags.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |
       |   |     LAG 1
       |   |
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
Tests to check that a previously configured static link aggregation does not stop forwarding traffic when attempting to delete several nonexistent link aggregations with different names that may not be supported.

To test that a previously configured static link aggregation does not stop forwarding traffic:
 1. Configure the static LAG on switch 1 and add two interfaces connected to switch 2.
 2. Configure static LAG on switch 2 and add two interfaces connected to switch 1.
 3. Configure the LAG and the interfaces of the workstations with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Attempt to delete LAGs named XX, 0, -1, 2000, 2001, @%&$#(), 60000, 600,  and 2 on each switch.  At the same time, verify that the created LAG on each switch has not changed.
 6. Test the connectivity of the workstations.

### Test result criteria
#### Test pass criteria

 * The Nonexistent LAGs cannot be deleted (an error is displayed).
 * The workstations can communicate.
 * The existing LAGs do not see their configuration altered after attempting to delete the nonexistent LAGs.

#### Test fail criteria

 * Deleting a nonexistent LAG is not met with an error.
 * The workstations cannot communicate.
 * The existing LAGs have their configuration modified after attempting to delete the nonexistent LAGs.

## Modify number of static LAG members upper limits
### Objective ###
To verify it is possible to modify the upper limits of a LAG.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations
 - **FT file**: `ops/tests/lacp/StaticLagModifyMaxNumberOfMembers.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
+--------+--------+
|                 |
|    Switch 1     |
|                 |
+-+-+-+-+-+-+-+-+-+
  | | | | | | | |
  | | | | | | | |    LAG 1
  | | | | | | | |
+-+-+-+-+-+-+-+-+-+
|                 |
|    Switch 2     |
|                 |
+-------+---------+
        |
        |
+-------+---------+
|                 |
|  Workstation 2  |
|                 |
+-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
This test verifies that a previously configured static link aggregation can be modified to have between seven and eight members.

To test that a previously configured static link aggregation can be modified to have between seven and eight members:
 1. Configure the static LAG on switch 1 and add eight interfaces connected to switch 2.
 2. Configure the static LAG on switch 2 and add eight interfaces connected to switch 1.
 3. Configure the LAG and the interfaces of the workstations with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Remove one interface from each LAG and test the connectivity between the  workstations.
 6. Add the interface back in and test the connectivity between the workstations.

### Test result criteria
#### Test pass criteria

 * The number of interfaces on the LAGs are modified.
 * The workstations can communicate.

#### Test fail criteria ####

 * The number of interfaces on the LAGs cannot be modified.
 * The workstations cannot communicate.

## Modify dynamic LAG without changing any setting
### Objective
To verify that when reapplying a dynamic LAG configuration, the LAG does not change and continues to pass traffic.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations
 - **FT file**: `ops/tests/lacp/dynamicLinkAggregation_modSet.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +-+---+---+--+
     |   |   |
     |   |   |      LAG 1
     |   |   |
   +-+---+---+--+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
Tests that a previously configured dynamic link aggregation does not stop forwarding traffic when the link is reconfigured with the same initial settings.

To test that a previously configured dynamic link does not stop forwarding traffic with the link is reconfigured with the same initial settings:
 1. Configure the dynamic LAG on switch 1 and add the three interfaces connected to switch 2.
 2. Configure the dynamic LAG on switch 2 and add the three interfaces connected to switch 1.
 3. Configure the LAG and workstations interfaces with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Reapply the LAG configuration and test the connectivity again.

### Test result criteria
#### Test pass criteria

The traffic flow between hosts is not stopped after applying the dynamic LAG configuration and the current configuration is not modified.

#### Test fail criteria

This test fails in the following scenarios:
 - The traffic between hosts stops crossing the dynamic LAG link.
 - The configuration changes.
 - The interfaces reset.
 - Other unexpected behavior.

## Modify static LAG without changing any setting
### Objective
To verify that when reapplying a static LAG configuration, the LAG does not change and continues to pass traffic.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations
 - **FT file**: `ops/tests/lacp/staticLinkAggregation_modSet.py`

### Setup

#### Topology diagram
```ditaa
+-----------------+
|                 |
|  Workstation 1  |
|                 |
+--------+--------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +-+---+---+--+
     |   |   |
     |   |   |      LAG 1
     |   |   |
   +-+---+---+--+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup

Workstations have one static IP address each in the same range.

### Description
Tests that a previously configured static link aggregation does not stop forwarding traffic when the link is reconfigured with the same initial settings.

To test that a previously configured static link aggregation does not stop forwarding traffic when the link is reconfigured with the same initial settings:
 1. Configure the static LAG on switch 1 and add the three interfaces connected to switch 2.
 2. Configure the dynamic LAG on switch 2 and add the three interfaces connected to switch 1.
 3. Configure the LAG and the interfaces of the workstations with the same VLAN.
 4. Test the connectivity of the workstations.
 5. Reapply the LAG configuration and test the connectivity again.

### Test result criteria
#### Test pass criteria

The traffic flow between the hosts is not stopped after applying the static LAG configuration and the current configuration is not modified.

#### Test fail criteria

This test fails in the following scenarios:
 - The traffic flow between the hosts stops crossing the static LAG link.
 - The configuration changes.
 - The interfaces reset.
 - Other unexpected behavior.

## Verify communication between 2 switches connected by L3 dynamic LAGs
### Objective
Verify a ping between 2 switches configured with L3 dynamic LAGs works properly.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - **FT file**: `ops/tests/lag/test_ft_lacp_l3_ping.py`

### Setup

#### Topology diagram
```ditaa

   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +-+---+---+--+
     |   |   |
     |   |   |      LAG 1
     |   |   |
   +-+---+---+--+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
```
#### Test setup
### Description

This test verifies that after configuring a L3 dynamic LAG between two switches
a ping works properly from one switch to the other.

  1. Create a dynamic LAG in both switches.
  2. Add 3 interfaces to each LAG.
  3. Assign IP address on the same range to each LAG.
  4. Ping from switch1 to switch2 and viceversa.

### Test result criteria
#### Test pass criteria
The number of packets transmitted in the ping is equal to the number of packets
received.

#### Test fail criteria
The number of packets transmitted in the ping is not equal to the number of
packets received.


## Verify communication between 2 switches connected by L3 static LAGs
### Objective
Verify a ping between 2 switches configured with L3 static LAGs works properly.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - **FT file**: `ops/tests/lag/test_ft_static_lag_l3_ping.py`

### Setup

#### Topology diagram
```ditaa
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +-+---+---+--+
     |   |   |
     |   |   |      LAG 1
     |   |   |
   +-+---+---+--+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
```
#### Test setup
### Description

This test verifies that after configuring a L3 static LAG between two switches
a ping works properly from one switch to the other.

  1. Create a static LAG in both switches.
  2. Add 3 interfaces to each LAG.
  3. Assign IP address on the same range to each LAG.
  4. Ping from switch1 to switch2 and viceversa.

### Test result criteria
#### Test pass criteria
The number of packets transmitted in the ping is equal to the number of packets
received.

#### Test fail criteria
The number of packets transmitted in the ping is not equal to the number of
packets received.

## Verify LAG interface functionality when using command shutdown for LAG

### Objective
To verify that LAG interfaces are not passing traffic when the command shutdown is
used in the LAG context, or to verify that LAG interfaces are passing traffic when
the command no shutdown is used in the LAG context.

### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations
 - **FT file**: `ops/tests/lag/test_lag_ft_shutdown_no_shutdown.py`

### Setup

#### Topology diagram
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
#### Test setup
### Description
This test verifies functionality of the commands shutdown and no shutdown in a LAG context

To configure a LAG:
1. Configure LAG 1.
2. Add interfaces to LAG 1.
3. Configure the workstations.
4. Ping between the workstations.
5. Use command **no shutdown** in LAG 1 in both switches. Ping between the workstations.
6. Use command **shutdown** in LAG 1 in both switches.
7. Ping between the workstations.
8. Use command **no shutdown** in LAG 1 in both switches.
9. Ping between the workstations.

### Test result criteria
#### Test pass criteria
Ping between the workstations fails when the command **shutdonw** is used.
Ping between the workstations is successful when the command **no shutdonw** is used.

#### Test fail criteria
Ping reach the other side when the command **shutdonw** is used.
Ping does not reach the other side when the command **no shutdonw** is used.


## Verify communication between 2 switches connected by L2 dynamic LAGs
### Objective
Verify a ping between 2 workstations connected by 2 switches configured with L2
dynamic LAGs works properly.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations
 - **FT file**: `ops/tests/lag/test_ft_lacp_l2_ping.py`

### Setup

#### Topology diagram
```ditaa
 +-----------------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-------+---------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |
       |   |     LAG 1
       |   |
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup
### Description

This test verifies that after configuring a L2 dynamic lag between two switches
a ping between 2 workstations connected by those switches works properly.

  1. Assign an IP address on the same range to each workstation.
  2. Configure dynamic L2 LAG on switch 1 and add the 2 interfaces connected to
     switch 2.
  3. Configure dynamic L2 LAG on switch 2 and add the 2 interfaces connected to
     switch 1.
  4. Configure LAGs and workstations interfaces with same VLAN.
  5. Ping from workstation 1 to workstation 2 and viceversa.

### Test result criteria
#### Test pass criteria
Ping is successful.

#### Test fail criteria
Ping is not successful.


## Verify communication between 2 switches connected by L2 static LAGs
### Objective
Verify a ping between 2 workstations connected by 2 switches configured with L2
static LAGs works properly.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations
 - **FT file**: `ops/tests/lag/test_ft_static_lag_l2_ping.py`

### Setup

#### Topology diagram
```ditaa

 +-----------------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-------+---------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |
       |   |     LAG 1
       |   |
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup
### Description

This test verifies that after configuring a L2 static lag between two switches
a ping between 2 workstations connected by those switches works properly.

  1. Assign an IP address on the same range to each workstation.
  2. Configure static L2 LAG on switch 1 and add the 2 interfaces connected to
     switch 2.
  3. Configure static L2 LAG on switch 2 and add the 2 interfaces connected to
     switch 1.
  4. Configure LAGs and workstations interfaces with same VLAN.
  5. Ping from workstation 1 to workstation 2 and viceversa.

### Test result criteria
#### Test pass criteria
Ping is successful.

#### Test fail criteria
Ping is not successful.


## Change static LAG from L2 to L3 and viceversa
### Objective
Verify a static LAG switches properly from L2 to L3 and viceversa.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations
 - **FT file**: `ops/tests/lag/test_ft_static_lag_l2_l3_change.py`

### Setup

#### Topology diagram
```ditaa
 +-----------------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-------+---------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |            |
   +---+---+----+
       |   |
       |   |     LAG 1
       |   |
   +---+---+----+
   |            |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup
### Description

This test verifies the communication of 2 switches connected first by a L2 LAG,
then by a L3 LAG and finally connected by a L2 LAG again.

  1. Assign an IP address on the same range to each workstation.
  2. Configure static L2 LAG on switch 1 and add the 2 interfaces connected to
     switch 2.
  3. Configure static L2 LAG on switch 2 and add the 2 interfaces connected to
     switch 1.
  4. Configure LAGs and workstations interfaces with same VLAN.
  5. Ping from workstation 1 to workstation 2 and viceversa.
  6. Configure LAGs as L3 and assign an IP address on the same range to
     each LAG, but different range than the one of the workstations.
  7. Ping from switch 1 to switch 2 and viceversa and
     from workstation 1 to workstation 2 and viceversa.
  8. Configure LAGs as L2 and configure LAGs and workstations
     interfaces with same VLAN.
  9. Ping from switch 1 to switch 2 and viceversa and
     from workstation 1 to workstation 2 and viceversa.

### Test result criteria
#### Test pass criteria
 * The ping between the workstations succeeds when the L2 LAG is configured and
   fails when the L3 LAG is configured.
 * The ping between the switches succeeds when the L3 LAG is configured and
   fails when the L2 LAG is configured.

#### Test fail criteria
 * The ping between the workstations fails when the L2 LAG is configured or
   succeeds when the L3 LAG is configured.
 * The ping between the switches fails when the L3 LAG is configured or
   succeeds when the L2 LAG is configured.


## Change interface from L2 LAG to L3 LAG and viceversa
### Objective
Verify an interface switches correctly from L2 LAG to L3 LAG and viceversa.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations
 - **FT file**: `ops/tests/lag/test_ft_static_lag_interface_l2_l3_change.py`

### Setup

#### Topology diagram
```ditaa
 +-----------------+
 |                 |
 |  Workstation 1  |
 |                 |
 +-------+---------+
         |
         |
   +-----+------+
   |            |
   |  Switch 1  |
   |  1  2  3   |
   +--+--+--+---+
      |  |  |
 L2   |  |  |  L3
 LAG  |  |  |  LAG
   +--+--+--+---+
   |  1  2  3   |
   |  Switch 2  |
   |            |
   +-----+------+
         |
         |
 +-------+---------+
 |                 |
 |  Workstation 2  |
 |                 |
 +-----------------+
```
#### Test setup
### Description

This test verifies the functionality of 2 LAGs when an interface is changed
from a L2 LAG to a L3 LAG and viceversa.

  1. Assign an IP address on the same range to each workstation.
  2. Configure a L2 LAG on switches 1 and 2 with fallback false and add interfaces 1 and 2.
  3. Configure a L3 LAG on switches 1 and 2 with fallback false and add interface 3.
  4. Configure L2 LAGs and workstations interfaces with same VLAN.
  5. Assign an IP address on the same range to each L3 LAG, but different than
     the range of the workstations.
  6. Ping from switch 1 to switch 2 (using IPs of step 5) and
     from workstation 1 to workstation 2 (using IPs of step 1).
  7. Configure interface 2 in both switches to be part of L3 LAG.
  8. Ping from switch 1 to switch 2 (using IPs of step 5) and
     from workstation 1 to workstation 2 (using IPs of step 1).
  9. Configure interface 2 in both switches to be part of L2 LAG.
  10. Ping from switch 1 to switch 2 (using IPs of step 5) and
      from workstation 1 to workstation 2 (using IPs of step 1).
  11. Remove interface 2 in both switches from L2 LAG.
  12. Add interface 2 in both switches to L3 LAG.
  13. Ping from switch 1 to switch 2 (using IPs of step 5) and
      from workstation 1 to workstation 2 (using IPs of step 1).
  14. Remove interface 2 in both switches from L3 LAG.
  15. Add interface 2 in both switches to L2 LAG.
  16. Ping from switch 1 to switch 2 (using IPs of step 5) and
      from workstation 1 to workstation 2 (using IPs of step 1).


### Test result criteria
#### Test pass criteria
 * The ping between the workstations succeeds.
 * The ping between the switches succeeds.

#### Test fail criteria
 * The ping between the workstations fails.
 * The ping between the switches fails.


## Static LAG statistics basic summary
### Objective
To verify LAG statistics reflect LAG configuration and individual ports statistics
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations with IP addresses on the same range and capable of using iperf
 - **FT file**: `ops-lacpd/ops-tests/feature/test_ft_lag_statistics.py`

### Setup

#### Topology diagram
```ditaa
           +-----------------+
           |                 |
           |      Host 1     |
           |                 |
           +-----------------+
                    |
                    |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 1           |
    |                               |
    +-------------------------------+
         |         |        |
         |         |        |
         |         |        |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 2           |
    |                               |
    +-------------------------------+
                    |
                    |
           +-----------------+
           |                 |
           |     Host 2      |
           |                 |
           +-----------------+
```
#### Test setup
### Description

Tests that a configured static Link Aggregation can summarize accurate individual interfaces statistics as they change.

To test LAG statistics do the following:
- Create a static LAG on both switches with members being the interfaces that interconnect them
- Configure an access VLAN and set it on the switches host interface and the LAG
- Validate the hosts can reach each other using ping
- For each LAG on each switch, obtain its statistics and verify all counters are the sum of all individual interfaces and its other information (LAG id, mode, aggregated interfaces) matches the expected settings
- On each host initiate iperf UDP servers
- On each host start iperf as client and send traffic for 30 seconds to the other one
- Gather the stats from the LAG interfaces and verify they still compare with the current values reported on each interface


### Test result criteria
#### Test pass criteria
 * The ping between the workstations succeeds.
 * The values reported by LAG statistics correspond with the LAG configuration and the counters with the sum of individual interfaces' counters.

#### Test fail criteria
 * The ping between the workstations fails.
 * The values reported by LAG statistics do not correspond with the LAG configuration and/or the counters with the sum of individual interfaces' counters.


## Dynamic LAG statistics basic summary
### Objective
To verify dynamic LAG statistics reflect LAG configuration and individual ports statistics.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations with IP addresses on the same range and capable of using iperf
 - **FT file**: `ops-lacpd/ops-tests/feature/test_ft_lacp_statistics.py`

### Setup

#### Topology diagram
```ditaa
           +-----------------+
           |                 |
           |      Host 1     |
           |                 |
           +-----------------+
                    |
                    |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 1           |
    |                               |
    +-------------------------------+
         |         |        |
         |         |        |
         |         |        |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 2           |
    |                               |
    +-------------------------------+
                    |
                    |
           +-----------------+
           |                 |
           |     Host 2      |
           |                 |
           +-----------------+
```
#### Test setup
### Description

Tests that a configured dynamic Link Aggregation can summarize accurate individual interfaces statistics as they change.

To test LAG statistics do the following:
- Create a dynamic LAG on both switches with members being the interfaces that interconnect them
- Configure an access VLAN and set it on the switches host interface and the LAG
- Validate the hosts can reach each other using ping
- For each LAG on each switch, obtain its statistics and verify all counters are the sum of all individual interfaces and its other information (LAG id, mode, aggregated interfaces) matches the expected settings
- On each host initiate iperf UDP servers
- On each host start iperf as client and send traffic for 30 seconds to the other one
- Gather the stats from the LAG interfaces and verify they still compare with the current values reported on each interface


### Test result criteria
#### Test pass criteria
 * The ping between the workstations succeeds.
 * The values reported by LAG statistics correspond with the LAG configuration and the counters with the sum of individual interfaces' counters.

#### Test fail criteria
 * The ping between the workstations fails.
 * The values reported by LAG statistics do not correspond with the LAG configuration and/or the counters with the sum of individual interfaces' counters.


## Static LAG statistics when aggregation members change
### Objective
To verify LAG statistics reflect the sum of individual members statistics when they change.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations with IP addresses on the same range and capable of using iperf
 - **FT file**: `ops-lacpd/ops-tests/feature/test_ft_lag_statistics_change_members.py`

### Setup

#### Topology diagram
```ditaa
           +-----------------+
           |                 |
           |      Host 1     |
           |                 |
           +-----------------+
                    |
                    |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 1           |
    |                               |
    +-------------------------------+
         |         |        |
         |         |        |
         |         |        |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 2           |
    |                               |
    +-------------------------------+
                    |
                    |
           +-----------------+
           |                 |
           |     Host 2      |
           |                 |
           +-----------------+
```
#### Test setup
### Description

Tests that a configured static Link Aggregation statistics change when its members are removed or added to match the current set of interfaces in the aggregation.

To test LAG statistics do the following:
- Configure an access VLAN on the switches host interfaces and one of the links interconnecting the switches
- Validate connectivity using ping
- On each host, initiate an iperf UDP server and then transmit UDP traffic with iperf between each other for 10 seconds
- Repeat first three steps using a different VLAN, a different link between switches, changing the IP addresses of the hosts and transmitting traffic for 15 seconds
- Repeat the previous step with yet another VLAN, different link between switches, hosts' IP address and transmitting traffic for 20 seconds
- Form a static LAG on one of the switches with no members and verify the statistics align with the LAG configuration and all counters are 0
- Repeat as before for every possible combination of ports while checking that the counters are the sum of the statistics from individual interfaces


### Test result criteria
#### Test pass criteria
 * The ping between the workstations succeeds always.
 * The values reported by LAG statistics correspond with the LAG configuration and the counters with the sum of individual interfaces' counters.

#### Test fail criteria
 * The ping between the workstations fails.
 * The values reported by LAG statistics do not correspond with the LAG configuration and/or the counters with the sum of individual interfaces' counters.


## Dynamic LAG statistics when aggregation members change
### Objective
To verify dynamic LAG statistics reflect the sum of individual members statistics when they change.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations with IP addresses on the same range and capable of using iperf
 - **FT file**: `ops-lacpd/ops-tests/feature/test_ft_lacp_statistics_change_members.py`

### Setup

#### Topology diagram
```ditaa
           +-----------------+
           |                 |
           |      Host 1     |
           |                 |
           +-----------------+
                    |
                    |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 1           |
    |                               |
    +-------------------------------+
         |         |        |
         |         |        |
         |         |        |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 2           |
    |                               |
    +-------------------------------+
                    |
                    |
           +-----------------+
           |                 |
           |     Host 2      |
           |                 |
           +-----------------+
```
#### Test setup
### Description

Tests that a configured static Link Aggregation statistics change when its members are removed or added to match the current set of interfaces in the aggregation.

To test LAG statistics do the following:
- Configure an access VLAN on the switches host interfaces and one of the links interconnecting the switches
- Validate connectivity using ping
- On each host, initiate an iperf UDP server and then transmit UDP traffic with iperf between each other for 10 seconds
- Repeat first three steps using a different VLAN, a different link between switches, changing the IP addresses of the hosts and transmitting traffic for 15 seconds
- Repeat the previous step with yet another VLAN, different link between switches, hosts' IP address and transmitting traffic for 20 seconds
- Form a dynamic LAG on one of the switches with no members and verify the statistics align with the LAG configuration and all counters are 0
- Repeat as before for every possible combination of ports while checking that the counters are the sum of the statistics from individual interfaces


### Test result criteria
#### Test pass criteria
 * The ping between the workstations succeeds always.
 * The values reported by LAG statistics correspond with the LAG configuration and the counters with the sum of individual interfaces' counters.

#### Test fail criteria
 * The ping between the workstations fails.
 * The values reported by LAG statistics do not correspond with the LAG configuration and/or the counters with the sum of individual interfaces' counters.


## LAG statistics cleanup on aggregation recreation
### Objective
To verify LAG statistics reflect the sum of current individual members statistics when deleted and recreated.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 Workstations with IP addresses on the same range and capable of using iperf
 - **FT file**: `ops-lacpd/ops-tests/feature/test_ft_lag_statistics_recreate_lag_interface.py`

### Setup

#### Topology diagram
```ditaa
           +-----------------+
           |                 |
           |      Host 1     |
           |                 |
           +-----------------+
                    |
                    |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 1           |
    |                               |
    +-------------------------------+
         |         |        |
         |         |        |
         |         |        |
    +-------------------------------+
    |                               |
    |                               |
    |            Switch 2           |
    |                               |
    +-------------------------------+
                    |
                    |
           +-----------------+
           |                 |
           |     Host 2      |
           |                 |
           +-----------------+
```
#### Test setup
### Description

Tests that a recreating a static Link Aggregation will have its statistics cleaned and replaced with the sum of the current number of member interfaces.

To test LAG statistics cleanup do the following:
- Configure an access VLAN on the switches host interfaces and one of the links interconnecting the switches
- Validate connectivity using ping
- On each host, initiate an iperf UDP server and then transmit UDP traffic with iperf between each other for 10 seconds
- Repeat first three steps using a different VLAN, a different link between switches, changing the IP addresses of the hosts and transmitting traffic for 15 seconds
- Repeat the previous step with yet another VLAN, different link between switches, hosts' IP address and transmitting traffic for 20 seconds
- Form a static LAG on one of the switches with one interface and verify the statistics align with the LAG configuration and all counters are equal to that of the member
- Delete and recreate the LAG and verify all counters are now in 0, then add a different combination of members and check the statistics counters match the sum of members' values
- Repeat the last step with all possible combination of three interfaces


### Test result criteria
#### Test pass criteria
 * The ping between the workstations succeeds always.
 * The values reported by LAG statistics correspond with the LAG configuration and the counters with the sum of individual interfaces' counters.

#### Test fail criteria
 * The ping between the workstations fails.
 * The values reported by LAG statistics do not correspond with the LAG configuration and/or the counters with the sum of individual interfaces' counters.
