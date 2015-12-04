
# VLAN Test Cases

##Contents


[Validating the fault tolerant VLAN ID](#validating-the-fault-tolerant-vlan-id)
[Verifying the fault tolerant VLAN state transition](#verifying-the-fault-tolerant-vlan-state-transition)
[Verifying the fault tolerant VLAN state reason](#verifying-the-fault-tolerant-vlan-state-reason)
[Deleting a VLAN and reassigning the port](#deleting-a-vlan-and-reassigning-the-port)
[Deleting VLANs from the middle of the VLAN list and reassigning the port](#deleting-vlans-from-the-middle-of-the-vlan-list-and-reassigning-the-port)
[Handling tagged frames received on an access port](#handling-tagged-frames-received-on-an-access-port)
[Verifying switch ports with untagged frames on trunk ports](#verifying-switch-ports-with-untagged-frames-on-trunk-ports)
[Verifying the functionality of deleting an existing and nonexistent VLAN with various port configurations](#verifying-the-functionality-of-deleting-an-existing-and-nonexistent-vlan-with-various-port-configurations)
[Verifying the initial state of created VLANs](#verifying-the-initial-state-of-created-vlans)
[Confirming the VLAN state or reason values if ports have been assigned](#confirming-the-vlan-state-or-reason-values-if-ports-have-been-assigned)
[Verify trunk link with multiple VLAN traffic](#verify-trunk-link-with-multiple-vlan-traffic)
[Testing the VLAN admin state reason value](#testing-the-vlan-admin-state-reason-value)


## Validating the fault tolerant VLAN ID
### Objective
Verify that a VID out of the 802.1Q range or reserved VID cannot be set. Also, confirm that a VID that already exists cannot not be set again.
### Requirements
The OpenSwitch OS is required for this test.
### Setup

#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
The test setup consists of one DUT in standalone mode.

### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default, and be in the login or bash-shell context.
### Test result criteria

#### Test pass criteria
A VID out of the 802.1Q range or a VID already in use, was not applied to the configuration.
#### Test fail criteria
A VID out of the 802.1Q range or a VID already in use, was applied to the configuration.

## Verifying the fault tolerant VLAN state transition
### Objective
Verify that the status of the VLAN changes from up to down correctly. The status of a VLAN is changed from down to up when a port is added to the VLAN, and the VLAN has been brought up with the 'no shutdown' command.
### Requirements
The OpenSwitch OS is required for this test.
### Setup

#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
The test setup consists of one DUT in standalone mode.

### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default, and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
The VLAN status is correct in every scenario.
#### Test fail criteria
If the VLAN status displayed in one of the scenarios is wrong.

## Verifying the fault tolerant VLAN state reason
### Objective
With several VLANs configured, bring up one VLAN and confirm its state, assign one port to that VLAN, and verify its reason value is 'ok'. Then issue the command to set the VLAN to 'down' and confirm its state. Only one VLAN should see a change in its state.

### Requirements
The OpenSwitch OS is required for this test.

### Setup

#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
The test setup consists of one DUT in standalone mode.
### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default, and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
Only one of the VLANs has the configuration performed.
#### Test fail criteria
More than one VLAN is configured with the same options.

## Deleting a VLAN and reassigning the port
### Objective
To verify the functionality of deleting a VLAN and reassigning the port to another VLAN.

### Requirements
The requirements for this test case are:

 - OpenSwitch OS
 - WorkStations must have nmap installed

### Setup

#### Topology diagram
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
#### Test setup
- 1 DUT
- 3 workStations

### Description
The DUT must be:

- Running the OpenSwitch OS.
- Configured by default.
- Using the login or bash-shell context.
- Running with workstations that have 'nmap' installed.

### Test result criteria
#### Test pass criteria
The VLAN is deleted from the end of the VLAN table, and no traffic passes through other VLANs.
#### Test fail criteria
This test fails if other VLANs are affected by the deletion.

## Deleting VLANs from the middle of the VLAN list and reassigning the port
### Objective
To verify the functionality of deleting a VLAN from the middle of the VLAN list, and reassigning the port to another VLAN. The VLAN is deleted from the middle of the VLAN list, or is the VLAN that does not have the highest or the lowest VID. No traffic passes through the other VLANs.

### Requirements
The requirements for this test case are:

 - OpenSwitch OS
 - Ubuntu workStations with nmap installed

### Setup

#### Topology diagram
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
#### Test setup
- 1 DUT in standalone mode
- 3 workStations

### Description
The DUT must be:

- Running the OpenSwitch OS.
- Configured by default.
- Using the login or bash-shell context.
- Running with workstations that have 'nmap' installed.

### Test result criteria
#### Test pass criteria
The VLAN is deleted without affecting the other VLANS and the traffic is sent correctly.
#### Test fail criteria
This test fails if other VLANs are affected by the deletion.

## Handling tagged frames received on an access port
### Objective
To confirm that a switch port has the ability to handle tagged frames received on an access port.

### Requirements
The OpenSwitch OS is required for this test.

### Setup

#### Topology diagram
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+

```
#### Test setup
- 1 DUT in standalone mode
- 2 workStations

### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default, and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
The VLAN forwards traffic correctly, or drops it if necessary.
#### Test fail criteria
Tagged frames are not discarded on an access port.

## Verifying switch ports with untagged frames on trunk ports
### Objective
To confirm a switch port's ability to handle untagged frames that are received on trunk ports.

### Requirements
The OpenSwitch OS is required for this test.

### Setup

#### Topology diagram
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+

```
#### Test setup
- 1 DUT in standalone mode
- 2 workStations

### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default, and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
The VLAN forwards traffic correctly, or drops it if necessary.
#### Test fail criteria
Untagged frames are not dropped on the trunk port.

## Verifying the functionality of deleting an existing and nonexistent VLAN with various port configurations
### Objective
Verify the functionality of deleting an existing and nonexistent VLAN with or without ports configured within it.

### Requirements
The requirements for this test case are:

 - OpenSwitch OS
 - WorkStations must have nmap installed

### Setup

#### Topology diagram
```ditaa

    +-------+     +---------+     +-------+
    |       |     |         |     |       |
    |wrkSton+----->   DUT   <-----+wrkSton|
    |       |     |         |     |       |
    +-------+     +----^----+     +-------+

```
#### Test setup
- 1 DUT in standalone mode
- 2 workStations

### Description
The DUT must be running the OpenSwitch OS to execute this test. The DUT must also be configured by default, and be in the login or bash-shell context.
### Test result criteria
#### Test pass criteria
The VLAN is correctly deleted with ports and without ports.
#### Test fail criteria
The VLAN is not deleted from the configuration.

## Verifying the initial state of created VLANS
### Objective
Verify that the initially created VLANs are in a down state.
### Requirements
A single switch with the OpenSwitch OS is required for this test.
### Setup
The DUT must be running the OpenSwitch OS and started from a clean setup.
#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
This test setup requires a standalone switch.
### Description
When VLANs are created they initially show a status of "down".
### Test result criteria
#### Test pass criteria
A VLAN is created and displays a status of "down" in the 'show vlan' output.
#### Test fail criteria
A VLAN is created and displays a status other than "down" in the 'show vlan' output.

## Confirming the VLAN state or reason values if ports have been assigned
### Objective
Confirm the state of a VLAN that has assigned ports but is administratively shut down.
### Requirements
A single switch with the OpenSwitch OS is required for this test.
### Setup
The DUT must be running the OpenSwitch OS and started from a clean setup.
#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
This test setup requires a standalone switch.
### Description
The VLAN state value is "down" and the reason value is "admin_down" if the ports have been assigned to the respective VLAN, but the VLAN has not been set to "up".
### Test result criteria
#### Test pass criteria
A VLAN is created with ports assigned to it, and displays a status value of "up" and a reason value of "admin_down" in the 'show vlan' output.
#### Test fail criteria
This test fails with a status other than "down" or a reason other than "admin_down".

## Verify trunk link with multiple VLAN traffic
### Objective
Verify that a trunk link can carry traffic from multiple VLANs.
### Requirements
The requirements for this test case are:

 - 2 Switches with OpenSwitch OS
 - 4 Workstations

### Setup
The DUT must be running the OpenSwitch OS and started from a clean setup.
#### Topology diagram
```ditaa

 +-----------+     +----------+
 |  DUT1     |     |   DUT2   |
 |           +-----+          |
 +-----------+     +----------+
    |     |           |      |
    |     |           |      |
 +----+ +-----+     +----+ +----+
 |Wrks| |Wrks |     |Wrks| |Wrks|
 +----+ +-----+     +----+ +----+

```
#### Test setup
1. Configure the trunking between two DUTs.
2. Assign the ports to VLANs on both DUTs.

### Description
A trunk link is used to connect switches, and is able to carry traffic from multiple VLANs.

### Test result criteria

#### Test pass criteria
This test is successful if connectivity exists for all VLANs in the system.
#### Test fail criteria
This test is unsuccessful if the connectivity fails.

## Testing the VLAN admin state reason value
### Objective
To create three different VLANs and set the admin state to "up" for one of them. Verify the the state is "down" and "no_member_port" is the reason value for one of the VLANs.
### Requirements
A single switch with the OpenSwitch OS is required for this test.
### Setup
The DUT must be running the OpenSwitch OS and started from a clean setup.
#### Topology diagram
```ditaa

    +-------+
    |       |
    |  DUT  |
    |       |
    +-------+

```
#### Test setup
This test setup requires a standalone switch.
### Description
A VLAN with no ports and "no shutdown" must report a state value of "down" and a reason value of "no_member_port".
### Test result criteria
#### Test pass criteria
Three VLANs are created. Only one VLAN displays the state value as "down" and the reason value as "no_member_port" in the 'show vlan' output.
#### Test fail criteria
The VLAN state is other than "down" or the reason value is other than "no_member_port".