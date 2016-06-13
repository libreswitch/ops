# Feature Test Cases for Daemon Coredump

## Contents
- [Feature Test Cases for Daemon Coredump](#feature-test-cases-for-daemon-coredump)
	- [Contents](#contents)
	- [Objective](#objective)
	- [Requirements](#requirements)
	- [Setup](#setup)
		- [Topology diagram](#topology-diagram)
	- [Standalone switch test setup](#standalone-switch-test-setup)
		- [Description](#description)
		- [Test result criteria](#test-result-criteria)
			- [Test pass criteria](#test-pass-criteria)
			- [Test fail criteria](#test-fail-criteria)
	- [Supported platforms](#supported-platforms)
	- [References](#references)

## Objective
The purpose of this test is to verify the daemon coredump feature.

## Requirements
Switch running OpenSwitch.

## Setup
### Topology diagram
```ditaa
+---------+
|         |
|  dut01  |
|         |
+---------+
```

## Standalone switch test setup

### Description
1. Log in as root user.
2. Check pid of a running daemon.
3. Run `kill -11 <pid of daemon>` on bash shell.
4. Check generated corefile at `/var/diagnostics/coredump/`.
5. You can see same core file in vtysh cli `show core-dump`.

### Test result criteria
#### Test pass criteria
- System creates coredump for the daemon.

#### Test fail criteria
- System don't create coredump for the daemon.

## Supported platforms
The following platforms are supported for this feature:
- as5712
- as6712

## References
* [ Daemon core dump design document ] ( daemon_coredump_design.md )
* [ Daemon core dump user guide ] ( daemon_coredump_user_guide.md )
