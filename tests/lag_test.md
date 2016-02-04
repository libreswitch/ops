
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
This test verify a dynamic LAG can be configured using correct names and can not be configured using a name longer than permited or if it contains unsupported characters.

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
This test verifies that a static LAG can be configured using correct names and cannot be configured if it uses a name longer than permited or if it containis unsupported characters.

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
2. Add interface to LAG 1
3. Configure LAG 2
4. Add interface to LAG 2 to move it

### Test result criteria
#### Test pass criteria
Interface is on LAG 1 after step 2, and moved to LAG 2 after step 4.

#### Test fail criteria ####
If the interface is not on LAG 1 after step 2, and is not on LAG 2 after step 4.



## Verify interface can be moved from a dynamic LAG to another

### Objective
To move an interface associated with an dynamic LAG to another dynamic LAG.

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
2. Add interface to LAG 1
3. Configure LAG 2
4. Add interface to LAG 2 to move it

### Test result criteria
#### Test pass criteria
Interface is on LAG 1 after step 2, and moved to LAG 2 after step 4.

#### Test fail criteria
If the interface is not on LAG 1 after step 2, and is not on LAG 2 after step 4.



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
 1. Configure active LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations' interfaces with same VLAN.
 4. Test the workstations' connectivity.
 5. Delete LAGS and test connectivity is broken.
 6. Recreate the LAGs with 1 interface and test connectivity is reestablished.
 8. Delete LAGS and test connectivity is broken.
 9. Recreate the LAGs with no interfaces and delete them again.

### Test result criteria
#### Test pass criteria

 * LAGs can be recreated and deleted without errors.
 * Workstations can communicate when a LAG is created with at least 1 interface.
 * Workstations cannot communicate when LAGs are deleted or the LAG has no interfaces associated.

#### Test fail criteria

 * LAGs cannot be created or deleted or there are errors when doing so.
 * Workstations cannot communicate when a LAG is created with at least 1 interface.
 * Workstations can communicate after deleting a LAG or when the LAG has no associated interfaces.

## Delete dynamic LAG with max number of members
### Objective
To verify a dynamic LAG that contains 8 members can be deleted.
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
 1. Configure active LAG on switch 1 and add the 8 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 8 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations' connectivity.
 5. Delete LAGS and test if the connectivity is broken.

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

Workstations have a static IP address each on the same range.

### Description
Tests that a previously configured dynamic link aggregation can be modified to have between zero and two members.

to modify a dynamice link aggregation to have between zero and two members:
 1. Configure active LAG on switch 1 and add the 3 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 3 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations' connectivity.
 5. Remove one interface of each LAG and test connectivity between workstations.
 6. Add back the interface and test connectivity between workstations.
 7. Remove all interfaces from LAGs and test that the connectivity doesn't work.
 8. Add all interfaces back to LAGs and test that the connectivity is restored.
 9. Remove 2 interfaces from each LAG and test that the connectivity still works.
 10. Remove the 2 interfaces back and test the connectivity.

### Test result criteria
#### Test pass criteria

 * Number of interfaces on the LAGs are modified
 * Workstations can communicate as long as LAGs have at least 1 interface.

#### Test fail criteria

 * Number of interfaces on the LAGs cannot be modified.
 * Workstations cannot communicate with at least 1 interface on each LAG or they can communicate when there are no interfaces on the LAGs.

## Modify number of dynamic LAG members upper limits
### Objective
To verify it is possible to modify a LAG’s upper limits.
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

Workstations have a static IP address each on the same range.

### Description
Tests that a previously configured dynamic link aggregation can be modified to have between seven and eight members.

To modify dynamic link aggregation:
 1. Configure active LAG on switch 1 and add the 8 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 8 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations' connectivity.
 5. Remove 1 interface of each LAG and test connectivity between the workstations.
 6. Add back the interface and test connectivity between workstations.

### Test result criteria
#### Test pass criteria

 * The number of interfaces on the LAGs are modified
 * The Workstations can communicate.

#### Test fail criteria

 * The number of interfaces on the LAGs cannot be modified.
 * The workstations cannot communicate.

## Convert static LAG to dynamic LAG
### Objective
To verify a dynamic LAG can be converted to a static LAG and pass traffic.
### Requirements
The requirements for this test case are:

 - 2 Switches running OpenSwitch
 - 2 workstations`
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

Workstations have a static IP address each on the same range.

### Description
This test verifies that a static LAG formed between two switches can be transitioned to a dynamic LAG with one active member and one passive member while retaining the connectivity of clients employing the LAG to communicate.

To transition a dynamic LAG with one active member and one passive member to static:
 1. Configure static LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure static LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test the workstations' connectivity.
 5. Change LAGs on both switches to dynamic (1 active, the other passive).
 6. Test the workstations' connectivity.

### Test result criteria
#### Test pass criteria

 * The LAGs are converted from static to dynamic.
 * The workstations can communicate after change in LAGs.

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

Workstations have a static IP address each on the same range.

### Description
Tests that a previously configured static link aggregation of two, one, or zero members can be deleted.

To delete a previously configured static link aggregaton with two, one, or zero members:
 1. Configure static LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure static LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test workstations' connectivity.
 5. Delete the LAGs and test if the connectivity is broken.
 6. Re-create the LAGs with 1 interface and test connectivity is re-established.
 8. Delete LAGS and test connectivity is broken.
 9. Re-create the LAGs with no interfaces and re-delete them.

### Test result criteria
#### Test pass criteria

 * The LAGs can be recreated and deleted without errors.
 * The workstations can communicate when a LAG is created with at least one interface.
 * The workstations cannot communicate when LAGs are deleted or if the LAG has no interfaces associated.

#### Test fail criteria

 * LAGs cannot be created or deleted or there are errors when doing so.
 * The Workstations cannot communicate when a LAG is created with at least one interface.
 * The workstations can communicate after deleting the LAG or when the LAG has no interfaces associated.

## Delete static LAG with max number of members
### Objective
To verify a static LAG with eight members can be deleted.
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

Workstations have a static IP address each on the same range.

### Description
Tests that a previously configured static link aggregation with eight members can be deleted.

To delete a previously configured static link aggregaton with eight members:
 1. Configure active LAG on switch 1 and add the 8 interfaces connected to switch 2.
 2. Configure passive LAG on switch 2 and add the 8 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test the workstations' connectivity.
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

Workstations have a static IP address each on the same range.

### Description
Tests that a previously configured static link aggregation does not stop forwarding traffic when attempting to delete several nonexistent Link Aggregations with different names that may not be supported.

To test that a previously configured static link aggregation does not stop forwarding traffic:
 1. Configure static LAG on switch 1 and add the 2 interfaces connected to switch 2.
 2. Configure static LAG on switch 2 and add the 2 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test the workstations' connectivity.
 5. Attempt to delete LAGs named XX, 0, -1, 2000, 2001, @%&$#(), 60000, 600,  and 2 on each switch.  At the same time, verify that the created LAG on each switch has not changed.
 6. Test the workstations' connectivity.

### Test result criteria
#### Test pass criteria

 * The Nonexistent LAGs cannot be deleted (an error is displayed).
 * The workstations can communicate.
 * The Existing LAGs don't see their configuration altered after attempting to delete the nonexistent LAGs.

#### Test fail criteria

 * Deleting a nonexistent LAG is not met with an error.
 * The workstations cannot communicate.
 * The existing LAGs have their configuration modified after attempting to delete the nonexistent LAGs.

## Modify number of static LAG members upper limits
### Objective ###
To verify it is possible to modify a LAG's upper limits.
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

Workstations have a static IP address each on the same range.

### Description
Tests that a previously configured static Link Aggregation can be modified to have between 7 and 8 members.

Steps:
 1. Configure static LAG on switch 1 and add the 8 interfaces connected to switch 2.
 2. Configure static LAG on switch 2 and add the 8 interfaces connected to switch 1.
 3. Configure LAG and workstations interfaces with same VLAN.
 4. Test the workstations' connectivity.
 5. Remove one interface of each LAG and test connectivity between the workstations.
 6. Add the interface back in and test connectivity between the workstations.

### Test result criteria
#### Test pass criteria

 * The number of interfaces on the LAGs are modified
 * The workstations can communicate.

#### Test fail criteria ####

 * The number of interfaces on the LAGs cannot be modified.
 * The workstations cannot communicate.

## Modify dynamic LAG without changing any setting
### Objective
To verify when reapplying a dynamic LAG configuration, the LAG does not change and continues to pass traffic.
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

Workstations have a static IP address each on the same range.

### Description
Tests that a previously configured dynamic link aggregation does not stop forwarding traffic when the link is reconfigured with the same initial settings.

To test that a previously configured dynamic link does not stop forwarding traffic with the link is reconfigured with the same initial settings:
 1. Configure the dynamic LAG on switch 1 and add the three interfaces connected to switch 2.
 2. Configure the dynamic LAG on switch 2 and add the three interfaces connected to switch 1.
 3. Configure the LAG and workstations interfaces with the same VLAN.
 4. Test the workstations' connectivity.
 5. Reapply the LAG configuration and test connectivity again.

### Test result criteria
#### Test pass criteria

The traffic flow between hosts is not stopped after applying dynamic LAG configuration and current configuration is not modified.

#### Test fail criteria

The traffic between hosts stops crossing the dynamic LAG link, or the configuration changes, or the interfaces reset, or for any other unexpected behavior.

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

Workstations have a static IP address each on the same range.

### Description
Tests that a previously configured static link aggregation does not stop forwarding traffic when the link is reconfigured with the same initial settings.

To test that a previously configured static link aggregation does not stop forwarding traffic when the link is reconfigured with the same initial settings:
 1. Configure static LAG on switch 1 and add the three interfaces connected to switch 2.
 2. Configure dynamic LAG on switch 2 and add the three interfaces connected to switch 1.
 3. Configure the LAG and workstations' interfaces with same VLAN.
 4. Test the workstations' connectivity.
 5. Reapply LAG configuration and test connectivity again.

### Test result criteria
#### Test pass criteria

The traffic flow between hosts is not stopped after applying static LAG configuration and current configuration is not modified.

#### Test fail criteria

The traffic between hosts stops crossing the static LAG link, or the configuration changes, or the interfaces reset, or for any other unexpected behavior.

