# Show Core Dump Test Case

##Contents

- [1. Negative test cases](#1-negative-test-cases)
	- [1.1 Daemon core dump configuration file missing](#11-daemon-core-dump-configuration-file-missing)
	- [1.2 Empty daemon core dump configuration file](#12-empty-daemon-core-dump-configuration-file)
	- [1.3 Corrupted daemon core dump configuration file](#13-corrupted-daemon-core-dump-configuration-file)
	- [1.4 No kernel core dump configuration file](#14-no-kernel-core-dump-configuration-file)
	- [1.5 Empty kernel core dump configuration file](#15-empty-kernel-core-dump-configuration-file)
	- [1.7 Invalid input parameter to CLI](#17-invalid-input-parameter-to-cli)
- [2. Positive test cases](#2-positive-test-cases)
	- [2.1 No core dumps present](#21-no-core-dumps-present)
	- [2.2 Daemon core dumps displayed.](#22-daemon-core-dumps-displayed)
	- [2.3 Kernel core dumps present](#23-kernel-core-dumps-present)
	- [2.4 Display both kernel and daemon core dumps.](#24-display-both-kernel-and-daemon-core-dumps)
- [3. Destructive tests](#3-destructive-tests)
	- [3.1 Core Dump with Corrupted Core File Names](#31-core-dump-with-corrupted-core-file-names)

# 1. Negative test cases
##  1.1 Daemon core dump configuration file missing

### Objective
This test case verifies the behavior of the `show core-dump` command in the absence of the daemon core dump configuration file.

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
*Steps*
1. Remove the daemon core dump configuration file (`/etc/ops_corefile.conf`).
2. Execute the `show core-dump` command.

### Test result criteria
#### Test pass criteria
This test passes if the `show core-dump` command displays the error `Unable to read daemon core dump config file`.

#### Test fail criteria
This test fails if an improper error message is returned or if there is a system crash.

## 1.2 Empty daemon core dump configuration file

### Objective
This test case verifies the behavior of the `show core-dump` command when there is no information present in the configuration file.

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
*Steps*
1. Empty the core dump configuration file located at `/etc/ops_corefile.conf`.
2. Run the `show core-dump` command on the vtysh shell.

### Test result criteria
#### Test pass criteria
This test passes if the `show core-dump` command displays the error `Invalid daemon core dump config file`.

#### Test fail criteria
This test fails if an improper error message is returned or if there is a system crash.


## 1.3 Corrupted daemon core dump configuration file

### Objective
This test case verifies the behavior of the `show core-dump` command when the daemon core dump configuration file is corrupted.

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
*Steps*
1. Remove the corepath entry from core dump configuration file located at `/etc/ops_corefile.conf`.
2. Add some junk characters around the configuration file.
3. Run the `show core-dump` command on vtysh shell.

### Test result criteria
#### Test pass criteria
This test passes if the show core-dump command displays the error `Invalid daemon core dump config file`.

#### Test fail criteria
This test fails if an improper error message is returned or if there is a system crash.


## 1.4 No kernel core dump configuration file

### Objective
This test case verifies the behavior of the `show core-dump` command when the kernel core dump configuration file is missing.

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
*Steps*
1. Remove the kernel core dump configuration file located at `/etc/kdump.conf`.
2. Run the `show core-dump` command on the vtysh shell.

### Test result criteria
#### Test pass criteria
This test passes if the show core-dump command displays the error `Unable to read kernel core dump config file`.

#### Test fail criteria
This test fails if an improper error message is returned or if there is a system crash.


## 1.5 Empty kernel core dump configuration file

### Objective
This test case verifies the behavior of the show core-dump command when the kernel core dump configuration file is empty.

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
*Steps*
1.  Remove the contents of the kernel core dump configuration file located at `/etc/kdump.conf`.
2. Run the `show core-dump` command on the vtysh shell.

### Test result criteria
#### Test pass criteria
This test passes if the `show core-dump` displays the error `Invalid kernel core dump config file`.

#### Test fail criteria
This test fails if an improper error message is returned or if there is a system crash.


## 1.6 Corrupted kernel core dump configuration file

### Objective
This test case verifies the behavior of the `show core-dump` when the kernel core dump configuration file is corrupted.

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
*Steps*
1.  Remove the configuration named 'path' from core dump configuration file located at `/etc/kdump.conf`.
2. Add junk entries across the configuration file.
3. Run the `show core-dump` command on the vtysh shell.

### Test result criteria
#### Test pass criteria
This test passes if the `show core-dump` command displays the error `Invalid kernel core dump config file`.

#### Test fail criteria
This test fails if an improper error message is returned or if there is a system crash.


## 1.7 Invalid input parameter to CLI

### Objective
This test case verifies the behavior of the `show core-dump` command when invalid parameters are passed to it.

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

Run the `show core-dump` command with invalid characters on the vtysh shell. For example:

`show core-dump 2314!@#$!@#$jkj`

### Test result criteria
#### Test pass criteria
This test passes if the `show core-dump` command displays the error `Unknown command`.

#### Test fail criteria
This test fails if an improper error message is returned or if there is a system crash.


# 2. Positive test cases
## 2.1 No core dumps present
### Objective
Verify the behavior of the `show core-dump` command when no core dump is present in the system.

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

*Steps*
1. Delete all the core dump files (daemon as well as kernel) from the system.
2. Run the "show core-dump" command on the vtysh shell.

### Test result criteria
#### Test pass criteria
This test passes if the `show core-dump`command displays the message `No core dumps are present`.

#### Test fail criteria
This test fails if an improper error message is returned or if there is a system crash.


## 2.2 Daemon core dumps displayed
### Objective
This test verifies that the `show core-dump` command displays daemon core dumps correctly.

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
*Steps*
1. Generate the core dumps if no core dump is already present. To generate a core dump,  kill any process with a PID, For example, execute `kill -11 <PID>`.  Otherwise, just create a file under the core dump folder with the following format to simulate a core dump. `<DaemonName>/<DaemonName>.1.YYYYMMDD.HHMMSS.core.tar.gz`
2. Execute the `show core-dump` command.

### Test result criteria
#### Test pass criteria
This test passes if the newly added core dump is displayed.

#### Test fail criteria
This test fails if the newly added core dump is not displayed or there is a system crash.


## 2.3 Kernel core dumps present
### Objective
This test verifies that the `show core-dump` command displays the kernel core dump.

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
*Steps*
1. Generate the kernel core dumps if no core dump is already present. To generate a kernel core dump, run `echo c > /proc/sysrq-trigger`.  Otherwise, create a dummy core dump file in the location mentioned in the kernel core dump configuration file.  This dummy core dump file should be named similar to the following:

`vmcore.YYYYMMDD.HHMMSS.tar.gz`.
2. Execute the `show core-dump` command.

### Test result criteria
#### Test pass criteria

This test passes if the `show core-dump` command displays the kernel core dump along with the timestamp specified.

#### Test fail criteria
This test fails if the `show core-dump` command does not display the kernel core dump or displays an error.


## 2.4 Display both kernel and daemon core dumps
### Objective
This test verifies that the `show core-dump` command displays both kernel and daemon core dumps.

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
*Steps*
1. Generate the core dumps if no core dump is already present. To generate a core dump, kill any process with a PID.  For example, execute "kill -11 <PID>".  Otherwise, just create a file under the core dump folder with the following format to simulate a core dump:
`<DaemonName>/<DaemonName>.1.YYYYMMDD.HHMMSS.core.tar.gz`
2. Generate the kernel core dumps if no core dump is already present. To generate a kernel core dump, run `echo c > /proc/sysrq-trigger`.  Otherwise create a dummy core dump file in the location mentioned in the kernel core dump configuration file.  This dummy core dump file should be named `vmcore.YYYYMMDD.HHMMSS.tar.gz`.
3. Execute the `show core-dump` command.


### Test result criteria
#### Test pass criteria
This test passes if both the kernel and daemon core dumps are displayed.

#### Test fail criteria
This test fails if either the kernel or the daemon core dump is missing from the display.

# 3. Destructive tests
## 3.1 Core Dump with Corrupted Core File Names
### Objective
This test verifies that the `show core-dump` command handles corrupted core dump files without crashing.


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
*Steps*
1. Generate the daemon core dump and change the name of core file to a random string.
2. Run the "show core-dump" command on the vtysh shell.

### Test result criteria
#### Test pass criteria
This test passes if the `show core-dump` command does not display those core dumps.

#### Test fail criteria
 This test fails if the `show core-dump` command displays junk information or if the system crashes or junk information is displayed.
