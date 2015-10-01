
VLAN Test Cases
=

 [TOC]

## VLAN_Id_Validation ##
### **Objective**  ##
Verify that a VID out of the 802.1Q range, in the Rerserved VID range or prexisting VID can not be created.
### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
### Setup ###

#### Topology Diagram ####
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test Setup ####
- 1 DUT in standalone

### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context.
### Test Result Criteria ###

#### Test Pass Criteria ####
VLANs described in the objective should not be set.
#### Test Fail Criteria ####
User is able to create an invalid VLAN.

##  VLAN_state_transition ##
### Objective ###
Verify the status of the VLAN change from up to down correctly. The status of a VLAN is changed from down to up when a port is added to the VLAN and the VLAN has been brought up with the respective command.
### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
### Setup ###

#### Topology Diagram ####
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test Setup ####
- 1 DUT in standalone

### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context.
### Test Result Criteria ###
#### Test Pass Criteria ####
VLANs status is correctly verifyed and validated in every scenario of configuration
#### Test Fail Criteria ####
If VLAN status is wrong showed in one of the scenarios

##  VLAN_state_reason_transition ##
### Objective ###
With several VLANs configured, bring one VLAN up and confirm its state, witch one port assigned to it verify its the VLAN Reason state for that VLAN transitions from no_member_port  ok.  Then administratively disable the VLAN and note the VLAN Status state transition from up to down. State changes should only occur on the VLAN being modified.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS

### Setup ###

#### Topology Diagram ####
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test Setup ####
- 1 DUT in standalone
### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context.
### Test Result Criteria ###
#### Test Pass Criteria ####
The reason and status state should only change for the VLAN being modified
#### Test Fail Criteria ####
If more than one VLAN was configured with same options or the VLAN being modified changes to an incorrect state.

##  VLAN_removed_from_end_of_table ##
### Objective ###
Verify the functionality of deleting a VLAN and reasigned port to another VLAN. The VLAN will be deleted from the end of the VLAN list table. Traffic on unmodified VLANs should continue to forward traffic without any loss.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
 - Ubuntu or CentOS for workStations with nmap installed

### Setup ###

#### Topology Diagram ####
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+
                       |
                       |
                  +---+ --+
                  |       |
                  |wrkSton|
                  |       |
                  +-------+

```
#### Test Setup ####
- 1 DUT
- 3 workStations
### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context. In the other hand workStations must have nmap installed.
### Test Result Criteria ###
#### Test Pass Criteria ####
VLAN is correctly deleted without affecting the other ones, and traffic is correctly sent.
#### Test Fail Criteria ####
Other VLAN were affected with traffic sent and or target VLAN was not correctly deleted.

##  VLAN_removed_from_middle_of_table ##
### Objective ###
Verify the functionality of deleting a VLAN and reasigned port to another VLAN. The VLAN will be deleted from middle of the VLAN list or the VLAN not with the highest or lowest VID. No traffic should pass through other VLANs.

### Requirements ###
The requirements for this test case are:

 - OpenSwitch OS
 - Ubuntu or CentOS for workStations with nmap installed

### Setup ###

#### Topology Diagram ####
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+
                       |
                       |
                  +---+ --+
                  |       |
                  |wrkSton|
                  |       |
                  +-------+

```
#### Test Setup ####
- 1 DUT in standalone
- 3 workStations
### Description ###
DUT must be running OpenSwitch OS to execute this test, should be by default configured and in the login or bash-shell context. In the other hand workStations must have nmap installed.
### Test Result Criteria ###
#### Test Pass Criteria ####
VLAN is correctly deleted without affecting the other ones, and traffic is correctly sent.
#### Test Fail Criteria ####
Other VLAN were affected with traffic sent and or target VLAN was not correctly deleted.

##  VLAN_initial_state##
### Objective ###
Verify the initial state of VLANs when they are created.
### Requirements ###
The requirements for this test case are:

 - Single switch with OpenSwitch OS
### Setup ###
DUT must be running OpenSwitch OS and started from a clean setup.
#### Topology Diagram ####
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test Setup ####
Standalone switch
### Description ###
When VLANs are created they initially show a status of down.
### Test Result Criteria ###
#### Test Pass Criteria ####
VLAN 30 is created and shows up with a status of down in the 'show vlan' output
#### Test Fail Criteria ####
VLAN status is other than down

##  VLAN_admin_down ##
### Objective ###
 Verify state of a VLAN with ports ports assigned and  administratively shut down.
### Requirements ###
The requirements for this test case are:

 - Single switch with OpenSwitch OS
### Setup ###
DUT must be running OpenSwitch OS and started from a clean setup.
#### Topology Diagram ####
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test Setup ####
Standalone switch
### Description ###
The state and reason values of a VLAN is down and admin_down if ports have been assigned to the respective VLAN but VLAN has not been set to up.
### Test Result Criteria ###
#### Test Pass Criteria ####
VLAN 30 is created with ports assigned to it and shows up with a status of down and reason of admin_down in the 'show vlan' output.
#### Test Fail Criteria ####
VLAN status or reason value is other than down and admin_down.

##  VLAN_description##
### Objective ###
Verify that a VLAN description can be added to the switch and it can be modified correctly.
### Requirements ###
The requirements for this test case are:

 - Single switch with OpenSwitch OS
### Setup ###
DUT must be running OpenSwitch OS and started from a clean setup.
#### Topology Diagram ####
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test Setup ####
Standalone switch
### Description ###
a. Add new VLANs to the switch and add a description.
b. Rename the new VLAN with another description.

### Test Result Criteria ###

#### Test Pass Criteria ####
Vlan description is added and changed successfully.
#### Test Fail Criteria ####
Unable to add or modify vlan description.

##  VLAN_no_port_member ##
### Objective ###
 Create three different VLANs and set admin state 'up' for one of them. Verify the state is down and no_member_port in the reason value for one of them.
### Requirements ###
The requirements for this test case are:

 - Single switch with OpenSwitch OS
### Setup ###
DUT must be running OpenSwitch OS and started from a clean setup.
#### Topology Diagram ####
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test Setup ####
Standalone switch
### Description ###
The state and reason value of a VLAN with no ports and "no shutdown" should be down and no_member_port .
### Test Result Criteria ###
#### Test Pass Criteria ####
VLAN 30,40 and 50 are created. Only one VLAN shows up with a status and reason of down and no_member_port as per the 'show vlan' output.
#### Test Fail Criteria ####
VLAN status or reason is other than down and no_member_port.