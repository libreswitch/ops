
<!--  See the https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet for additional information about markdown text.
Here are a few suggestions in regards to style and grammar:
* Use active voice. With active voice, the subject is the doer of the action. Tell the reader what
to do by using the imperative mood, for example, Press Enter to view the next screen. See https://en.wikipedia.org/wiki/Active_voice for more information about the active voice. 
* Use present tense. See https://en.wikipedia.org/wiki/Present_tense for more information about using the present tense.
* The subject is the test case. Explain the actions as if the "test case" is doing them. For example, "Test case configures the IPv4 address on one of the switch interfaces". Avoid the use of first (I) or second person. Explain the instructions in context of the test case doing them. 
* See https://en.wikipedia.org/wiki/Wikipedia%3aManual_of_Style for an online style guide.
 -->

#Log-rotate Test Cases


<!--Provide the name of the grouping of commands, for example, LLDP commands-->

 - [1.0 Test cases to verify log-rotate configuration](#1.0-test-cases-to-verify-log-rotate-configuration)
     - [1.01 To verify default configuration of log-rotate](#1.01-to-verify-default-configuration-of-log-rotate)
     - [1.02 Verify that the OVSDB is updated properly for the period configuration](#1.02-verify-that-the-ovsdb-is-updated-properly-for-the-period-configuration)
     - [1.03 Verify that the period configuration CLI is updated in the running config](#1.03-verify-that-the-period-configuration-cli-is-updated-in-the-running-config)
     - [1.04 Verify if the OVSDB is updated properly for a maxsize configuration](#1.04-verify-if-the-ovsdb-is-updated-properly-for-a-maxsize-configuration)
     - [1.05 Verify that the maxsize configuration CLI is updated in the running config](#1.05-verify-that-the-maxsize-configuration-cli-is-updated-in-the-running-config)
     - [1.06 Verify logrotate maxsize CLI for the wrong values](#1.06-verify-logrotate-maxsize-cli-for-the-wrong-values)
     - [1.07 Verify if the OVSDB is updated properly for the target configuration](#1.07-verify-if-the-ovsdb-is-updated-properly-for-the-target-configuration)
     - [1.08 Verify the logrotate target CLI for an invalid or unsupported protocol](#1.08-verify-the-logrotate-target-cli-for-an-invalid-or-unsupported-protocol)
     - [1.09 Verify the logrotate target CLI for an invalid IPv4 address](#1.09-verify-the-logrotate-target-cli-for-an-invalid-ipv4-address)
     - [1.10 Verify the logrotate target CLI for the broadcast IPv4 address](#1.10-verify-the-logrotate-target-cli-for-the-broadcast-ipv4-address)
     - [1.11 Verify the logrotate target CLI for a multicast IPv4 address](#1.11-verify-the-logrotate-target-cli-for-a-multicast-ipv4-address)
     - [1.12 Verify the logrotate target CLI for the loopback IPv4 address](#1.12-verify-the-logrotate-target-cli-for-the-loopback-ipv4-address)
     - [1.13 Verify the logrotate target CLI for an invalid IPv6 address](#1.13-verify-the-logrotate-target-cli-for-an-invalid-ipv6-address)
     - [1.14 Verify the logrotate target CLI for a multicast IPv6 address](#1.14-verify-the-logrotate-target-cli-for-a-multicast-ipv6-address)
     - [1.15 Verify the logrotate target CLI for the loopback IPv6 address](#1.15-verify-the-logrotate-target-cli-for-the-loopback-ipv6-address)
 - [2.0 Test cases to verify log-rotation and remote transfer](#2.0-test-case-to-verify-log-rotation-and-remote-transfer)
     - [2.01 Verify the log-rotate period with the default configuration](#2.01-verify-the-log-rotate-period-with-the-default-configuration)
     - [2.02 Verify the log-rotate period with a non-default configuration](#2.02-verify-the-log-rotate-period-with-a-non-default-configuration)
     - [2.03 Verify the log-rotate period with a remote host](#2.03-verify-the-log-rotate-period-with-a-remote-host)
     - [2.04 Verify the log-rotate maxsize with the default configuration](#2.04-verify-the-log-rotate-maxsize-with-the-default-configuration)
     - [2.05 Verify the log-rotate maxsize with a non-default configuration](#2.05-verify-the-log-rotate-maxsize-with-a-non-default-configuration)
     - [2.06 Verify the log-rotate maxsize with a remote host](#2.06-verify-the-log-rotate-maxsize-with-a-remote-host)
     - [2.07 Verify the log-rotate remote transfer with a non-reachable IPv4 address](#2.07-verify-the-log-rotate-remote-transfer-with-a-non-reachable-ipv4-address)
     - [2.08 Verify the-log-rotate remote transfer with an IPv6 address](#2.08-verify-the-log-rotate-remote-transfer-with-an-ipv6-address)
     - [2.09 Verify the log-rotate remote transfer with a non-reachable IPv6 address](#2.09-verify-the-log-rotate-remote-transfer-with-a-non-reachable-ipv6-address)

##  1.0 Test cases to verify log-rotate configuration ##

### Objective ###
The objective of these test cases is to configure various log-rotate parameters and to verify the expected behavior for valid scenarios and behavior for scenarios that have errors.

### Requirements ###

 A  TFTP server (tftpd-hpa) is required for these test cases.

### Setup ###
#### Topology Diagram ####

```ditaa

                                                           +-------------------+
              +------------------+                         | Linux workstation |
              |                  |eth0                eth0 |+-----------------+|
              |  AS5712 switch   |<----+         +-------->||TFTP Server      ||
              |                  |     |         |         |+-----------------+|
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 |                     |
                                 +---------------------+

```

###1.01 To verify default configuration of log-rotate ###

#### Description ####
Display the log-rotate configuration with the `show` command without a log-rotate configuration in the database.

Command : `root# show logrotate`

#### Test result criteria ####
#### Test pass criteria ####
The default values should be displayed.
```bash
    Logrotate configurations :
    Period            : daily
    Maxsize           : 10MB
```

#### Test fail criteria ####
If default values are not displayed or if the values are different, then the test case fails.


###1.02 Verify that the OVSDB is updated properly for the period configuration ###

#### Description ####
Configure the logrotate period and check that the database is updated properly with the correct period value.

Command: `root# logrotate period hourly`

The values in the OVSDB are verified with the following command:
```bash
Show logrotate
Ovs-vsctl list Open-vSwitch
```

#### Test result criteria ####
#### Test pass criteria ####
Configured period value should be updated in OVSDB.

#### Test fail criteria ####
Test case fails if the configured value is not found in the OVSDB or the OVSDB is updated with the incorrect value.

### 1.03 Verify that the  period configuration CLI is updated in running config ###
#### Description ####
Configure the logrotate period with a value different from the default value.

Command:

`root# logrotate period hourly`

Command to verify:

`show running-config`

#### Test result criteria ####
#### Test pass criteria ####
Configured period value is updated in the OVDDB and command is updated in the running config.
#### Test fail criteria ####
The test case fails, if the configured CLI is not displayed as part of the  `show running config` output.

### 1.04 Verify if the OVSDB is updated properly for a maxsize configuration ###
#### Description ####
Configure the logrotate maxsize and check if the OVSDB is updated properly.

Command:

`root# logrotate maxsize 20`

The values in the OVSDB shall be verified with the following command:

```bash
Show logrotate
Ovs-vsctl list Open-vSwitch
```

#### Test result criteria ####
#### Test pass criteria ####
The configured maxsize value is updated in the OVSDB.

#### Test fail criteria ####
The test case fails if the configured value is not found in the OVSDB or the OVSDB is updated with the incorrect value.

### 1.05 Verify that the maxsize configuration CLI is updated in the running config ###
#### Description ####
Configure the logrotate maxsize with a value different from the default value.

Command:

`root# logrotate period maxsize 20'

Command to verify:

`show running-config`

#### Test result criteria ####
#### Test pass criteria ####
The configured maxsize value is updated in the OVSDB and the command is updated in the running config.
#### Test fail criteria ####
The test case fails, if  the configured CLI is not displayed as part of the output of the 'show running config' command.

### 1.06 Verify logrotate maxsize CLI for the wrong values ###
#### Description ####
Enter the wrong values for logrotate maxsize.

Command:

`root# logrotate maxsize 250`

#### Test result criteria ####
#### Test pass criteria ####
The test case is successful if the proper error messages are displayed.

#### Test fail criteria ####
The test fails if  the logrotate maxsize can be configured.


### 1.07 Verify if the OVSDB is updated properly for the target configuration ###
#### Description ####
Configure the logrotate target and check if the OVSDB is updated properly.

Command:

`root# logrotate target tftp://1.1.1.1`

The values in OVSDB shall be verified with the following command:

```bash
Show logrotate
Ovs-vsctl list Open-vSwitch
Show running-config
```
#### Test result criteria ####
#### Test pass criteria ####
The configured target value is updated in the OVSDB and the command is updated in the show running config output.

#### Test fail criteria ####
The test fails if the configured value is not found in the OVSDB or if the OVSDB is updated with the incorrect value. The test also fails if the CLI is not part of show running config command output.

### 1.08 Verify the logrotate target CLI for an invalid or unsupported protocol ###
#### Description ####
Configure the logrotate target with an invalid or unsupported protocol.

Command:

`root# logrotate target scp://1.1.1.1`

#### Test result riteria ####
#### Test pass criteria ####
The test is successful  if the configuration fails with the following message:
"Only TFTP protocol is supported".
#### Test fail criteria ####
The test fails if the logrotate target can be configured.


### 1.09 Verify the logrotate target CLI for an invalid IPv4 address ###
#### Description ####
Configure the logrotate target with an invalid IPv4 address.

Command:

`root# logrotate target tftp://1.1`

#### Test result criteria ####
#### Test pass criteria ####
The test  is successful if the configuration fails and displays the following message:
"Invalid IPv4 or IPv6 address".
#### Test fail criteria ####
The test fails if the logrotate target can be configured with an invalid IPv4 address.


### 1.10 Verify the logrotate target CLI for the broadcast IPv4 address ###
#### Description ####
Configure the logrotate target with the broadcast IPv4 address.

Command:

`root# logrotate target tftp://255.255.255.255`

#### Test result criteria ####
#### Test pass criteria ####
The test is successful if the configuration fails with the message:
"IPv4: broadcast, multicast and loopback addresses are not allowed".
#### Test fail criteria  ####
The test fails if the logrotate target can be configured with an IPv4 broadcast address.


### 1.11 Verify the logrotate target CLI for a multicast IPv4 address ###
#### Description ####
Configure the logrotate target with a multicast IPv4 address.

Command:

`root# logrotate target tftp://224.10.0.1`

#### Test result criteria ####
#### Test pass criteria ####
The test  is successful if the configuration fails with the message:
"IPv4: broadcast, multicast and loopback addresses are not allowed".
#### Test fail criteria ####
The test fails if the logrotate target can be configured with a multicast IPv4 address.


### 1.12 Verify the logrotate target CLI for the loopback IPv4 address ###
#### Description ####
Configure the logrotate target with the loopback IPv4 address.

Command:

`root# logrotate target tftp://127.0.0.1`

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if the configuration fails with the message:
"IPv4: broadcast, multicast and loopback addresses are not allowed".
#### Test fail criteria  ####
The test fails if the logrotate target can be configured with the loopback IPv4 address.


### 1.13 Verify the logrotate target CLI for an invalid IPv6 address ###
#### Description ####
Configure the logrotate target with an invalid IPv6 address.

Command:

`root# logrotate target tftp://22:22`

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if the configuration fails with the message:
"Invalid IPv4 or IPv6 address".
#### Test fail criteria ####
The test fails if the logrotate target can be configured with an invalid IPv6 address.


### 1.14 Verify the logrotate target CLI for a multicast IPv6 address ###
#### Description ####
Configure the logrotate target with a multicast IPv6 address.

Command:

`root# logrotate target tftp://ff02::1:3`

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if the configuration fails with the message:
"IPv6: Multicast and loopback addresses are not allowed".
#### Test fail criteria  ####
The test fails if the logrotate target can be configured with a multicast IPv6 address.


### 1.15 Verify the logrotate target CLI for the loopback IPv6 address ###
#### Description ####
Configure the logrotate target with the loopback IPv6 address.

Command:

`root# logrotate target tftp://::1`

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if the configuration fails with the message:
"IPv6: Multicast and loopback addresses are not allowed".
#### Test fail criteria ####
The test fails if the logrotate target can be configured with the loopback IPv6 address.

##  2.0 Test cases to verify log-rotation and remote transfer ##

### Objective ###
The objective is to verify log-rotation in the local host and to verify the transfer of the rotated logs to the remote host.

### Requirements ###
A TFTP server (tftpd-hpa) is required for these test cases.

### Setup ###
#### Topology Diagram ####
```ditaa
                                                           +-------------------+
              +------------------+                         | Linux workstation |
              |                  |eth0                eth0 |+-----------------+|
              |  AS5712 switch   |<----+         +-------->||TFTP Server      ||
              |                  |     |         |         |+-----------------+|
              +------------------+     |         |         +-------------------+
                                       |         |
                                       v         v
                                 +---------------------+
                                 | port 1      port 2  |
                                 |                     |
                                 |      Switch         |
                                 |                     |
                                 +---------------------+

```

#### Test Setup ####
### 2.01 Verify the log-rotate period with the default configuration  ###
#### Description ####
Using the  default configuration, change the date to simulate the daily log-rotation on the local host.

Command:

`date --set='2015-06-26 12:21:42'`

Command to verify:

`ls –lhrt /var/log/`


#### Test result criteria ####
#### Test pass criteria ####
The test is successful, if the log files are rotated, compressed,  and stored locally in  the /var/log/ file with the appropriate time extension timestamped hourly.
#### Test fail criteria  ####
The test fails, if the rotation, compression, and file timestamped with the appropriate time extension is not met.

### 2.02 Verify the log-rotate period with a non-default configuration ###
#### Description ####
Change the period configuration to 'hourly' and change the date to simulate hourly log-rotate on the local host.

Command:

`date --set='2015-06-26 12:21:42'`

Command to verify:

`ls –lhrt /var/log/`

#### Test result criteria ####

#### Test pass criteria  ####
The test is successful if the log files are rotated, compressed, and stored locally in the /var/log/ file with the appropriate time extension timestamped hourly.
#### Test fail criteria ####
The test fails, if the rotation, compression, and file timestamped with the appropriate time extension is not met.

### 2.03 Verify the log-rotate period with a remote host  ###
#### Description ####
Repeat test 2.02 for remote transfer by configuring a logrotate target.

Command:
```bash
root# logrotate target tftp://172.17.42.1
date --set='2015-06-26 12:21:42
```
Command to verify:
```bash
ls –lhrt /var/log/ (in local host)
ls (in remote host tftp path)
```

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if the log files are rotated, compressed, and stored locally in the /var/log/ file with the appropriate time extension timestamped hourly and if the files are also transferred to the remote host.
#### Test fail criteria ####
The test fails if the rotation, compression, and file timestamped with the appropriate time extension is not met.

### 2.04 Verify the log-rotate maxsize with the default configuration ###
#### Description ####
With the default configuration, copy a file of a size greater than 10 MB to /var/log/messages and change the date to simulate the hourly logrotate on the local host.

Command:

`date --set='2015-06-26 12:21:42'`

Command to verify:

`ls –lhrt /var/log/`

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if the log files are rotated, compressed, and stored locally in the /var/log/ file with the appropriate time extension timestamped hourly.
#### Test fail criteria  ####
The test fails if the rotation, compression, and file timestamped with the appropriate time extension is not met.

### 2.05 Verify the log-rotate maxsize with a  non-default configuration ###
#### Description ####
Change the logrotate maxsize to 20 MB, copy a file of size greater than 20MB to /var/log/messages and change the date to simulate hourly logrotate on the local host.

Command:

`date --set='2015-06-26 12:21:42'`

Command to verify:

`ls –lhrt /var/log/`

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if the log files are rotated, compressed, and stored locally in the /var/log/ file with the appropriate time extension timestamped hourly.
#### Test fail criteria  ####
The test fails if the rotation, compression, and file timestamped with the appropriate time extension is not met.


### 2.06 Verify the log-rotate maxsize with a remote host ###
#### Description ####
Repeat test 2.05 for remote transfer by configuring the logrotate target.

Command:
```bash
root# logrotate target tftp://172.17.42.1
date --set='2015-06-26 12:21:42'
```
Command to verify:
```bash
ls –lhrt /var/log/ (in local host)
ls (in remote host tftp path)
```

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if the log files are rotated, compressed, and stored locally in the /var/log/ file with the appropriate time extension timestamped hourly, and if the files are also transferred to the remote host.
#### Test fail criteria ####
The test fails if the rotation, compression, and file timestamped with the appropriate time extension and remote transfer is not met.

### 2.07 Verify the log-rotate remote transfer with a non-reachable IPv4 address ###
#### Description ####
Enter a non-reachable IP in the logrotate target.

Command:

`root# logrotate target tftp://1.1.1.1`

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if log_rotate script times out after some time without waiting indefinitely.
#### Test fail criteria ####
The test fails if the log_rotate script waits indefinitely.

### 2.08 Verify the log-rotate remote transfer with an IPv6 address ###
#### Description ####
Repeat test 2.05 for remote transfer with a valid IPv6 address in the logrotate target.

Command:

`root# logrotate target tftp://2001:db8:0:1::128`

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful if the log files are rotated, compressed, and stored locally in the /var/log/ file with the appropriate time extension timestamped hourly and the files are also transferred to the remote host.
#### Test fail criteria ####
The test fails if the rotation, compression, and file timestamped with the appropriate time extension and remote transfer is not met.


### 2.09 Verify the log-rotate remote transfer with a non-reachable IPv6 address ###
#### Description ####
Enter a non-reachable IPv6 in the logrotate target.

Command:

`root# logrotate target tftp://2001:db8:0:1::fe`

#### Test result criteria ####
#### Test pass criteria  ####
The test is successful  if  the log_rotate script times out after a small amount of time without waiting indefinitely.
#### Test fail criteria ####
The test fails if the log_rotate script waits indefinitely.