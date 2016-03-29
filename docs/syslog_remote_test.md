# Syslog Remote Configuration Test Cases

## Contents
- [Logging CLI configurations](#logging-cli-configurations)
- [Logging configuration displayed in show running-config](#logging-configuration-displayed-in-show-running-config)
- [Syslog messages are received in remote syslog servers](#syslog-messages-are-received-in-remote-syslog-servers)

## Logging CLI configurations

### Objective
This test verifies that logging CLI configurations results in a proper update of the rsyslog remote configuration file.

### Requirements
A switch running OpenSwitch is required for this test case.

### Setup
#### Topology Diagram

```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+

```
#### Test setup
Standalone switch

### Description

1. Get into the configuration terminal of the switch.
2. Execute the command `logging 10.0.0.2 udp 514 severity info`.
3. Get into the bash shell.
4. Verify that the file `/etc/rsyslog.remote.conf` contains the line `info.* @10.0.0.2:514`.

### Test result criteria
#### Test pass criteria
Logging configuration is correctly stored in the `/etc/rsyslog.remote.conf` file.

#### Test fail criteria
This test fails if the logging configuration is not found in the `/etc/rsyslog.remote.conf` file.

## Logging configuration displayed in show running-config
### Objective
This test confirms that the logging cli configurations changes are displayed in the `show running-config` command.

### Requirements
A switch running OpenSwitch is required for this test case.

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
Standalone switch

### Description

1. Get into the configuration terminal of the switch
2. Execute the `logging 10.0.0.2 udp 514 severity info` command.
3. Execute `end` and go back to the vtysh shell.
4. Execute the `show running` command.
5. Verify that the changes are reflected in the `show running` command output.

### Test result criteria
#### Test pass criteria
This test passes if the logging configurations are visible in the `show running-config` command output.

#### Test fail criteria
This test fails if the logging configurations are not found in the `show running-config` command output.

## Syslog messages are received in remote syslog servers
### Objective
This test verifies that the syslog messages are received on the remote syslog server.

### Requirements
1. A switch running OpenSwitch is required for this test case.
2. A Host running syslog server.

### Setup
#### Topology diagram
```ditaa
 +----------+        +--------+
 |          |        |        |
 |  Switch  <-------->  Host  |
 |          |        |        |
 +----------+        +--------+

```
#### Test setup
Standalone switch

### Description

1. Get into the configuration terminal of the switch.
2. Execute the `logging 10.0.0.2 udp 514 severity info` command.
3. Verify that the "severity info and above" syslog messages are received on the host machine.

### Test result criteria
#### Test pass criteria
The "severity info and above" syslog messages are received on the host machine.

#### Test fail criteria
Syslog messages are not received on the host machine.
