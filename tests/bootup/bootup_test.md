# Boot Up Test Case

## Contents

- [Boot up verification](#boot-up-verification)
	- [Objective](#objective)
	- [Requirements](#requirements)
	- [Setup](#setup)
		- [Topology diagram](#topology-diagram)
		- [Test Setup](#test-setup)
	- [Description](#description)
	- [Test result criteria](#test-result-criteria)
		- [Test pass criteria](#test-pass-criteria)
		- [Test fail criteria](#test-fail-criteria)

## Boot up verification
### Objective
The test case verifies that all platform daemons are up and running. It also parses the log files to detect any errors logged by the platform daemons.

### Requirements
 - Two Switches
 - One Host

### Setup
#### Topology diagram

```ditaa
+--------+      +---------+    +----------+
|        |      |         |    |          |
| Host 1 +------+  SW 1   +----+   SW 2   |
|        |      |         |    |          |
+--------+      +---------+    +----------+
```

#### Test setup
**Switch 1** is configured with:

  ```
  !
  vlan 1
      no shutdown
  interface 1
      no shutdown
      ip address 10.0.30.2/24
  interface 2
      no shutdown
      ip address 10.0.10.2/24
  !
  ```

**Switch 2** is confiured with:

  ```
  !
  vlan 1
      no shutdown
  interface 1
      no shutdown
      ip address 10.0.30.3/24
  !
  ```

### Description
1. Configure Switch 1 and Switch 2 in **vtysh** with the following commands:

    ***Switch 1***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 10.0.30.2/24
    interface 2
    no shutdown
    ip address 10.0.10.2/24
    ```

    ***Switch 2***

    ```
    configure terminal
    interface 1
    no shutdown
    ip address 10.0.30.3/24
    ```

2. The host IP address is configured as **10.0.10.1/24**.
3. Verify that the platform processes are running on the switches by confirming that a non-null value is displayed after executing `ps -e`.
4. Verify that there are no platform error messages in the log file at **/var/log/messages**. After boot-up copy the log file  into another file and parse it for error messages using the `cat /messages | grep segfault` command.
5. Verify that the switch is reachable over the network by doing ping test from **Switch 2** to **Host 1**. Execute `ping 10.0.10.1/24` in the Switch 2 - **vtysh** command prompt.

### Test result criteria
#### Test pass criteria

 - All the platform daemons are up and running.
 - No error message is logged by platform daemons in the log file during boot-up.
 - The switch is reachable over a network. Verified by doing an IPv4-address ping test.

#### Test fail criteria

- Any of the platform daemons are not running. This is verified by not finding the daemon in the **ps -e** output.
- A platform specific error message is logged in the system log file.
- The ping test between **Host 1** and **Switch 1** fails.
