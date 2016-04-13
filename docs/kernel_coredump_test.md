# Feature Test Cases for Kernel Core

## Contents

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
The purpose of this test is to verify the kernel coredump feature.

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
1. Log in to root user.
2. Run the `echo c > /proc/sysrq-trigger` command in bash shell.
3. The system reboots and the core file is stored in /var/diagnostics/coredump/kernel-core.
4. After the reboot, wait for  2-3 minutes and login to vtysh and run the `show core-dump` command to see corefile.
5. Copy the kernel core dump using the `copy core-dump kernel` command.


### Test result criteria
#### Test pass criteria
- System recovers automatically within 60 seconds.
- A kernel core dump file is generated.

#### Test fail criteria
- System hangs.
- System did not generate a kernel core dump file.


## Supported platforms
The following platforms are supported for this feature:
- as5712
- as6712

## References
* [Kernel coredump design document](kernel_coredump_design.md)
* [Kernel coredump test document](kernel_coredump_test.md)
* [Kernel coredump user guide](kernel_coredump_user_guide.md)
* [Reference Crash tool white paper](https://people.redhat.com/anderson/crash_whitepaper/)
