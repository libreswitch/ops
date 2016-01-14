# SFTP Feature Test Cases

## Contents
   - [Verify SFTP server](#verify-sftp-server)
   - [Verify SFTP client](#verify-sftp-client)

## Verify SFTP server
### Objective
Verify SFTP server functionality.
### Requirements
The requirements for this test case are:
 - 2 switches

### Setup
#### Topology Diagram
    ```ditaa

                    +---+----+        +--------+
                    |        |        |        |
                    + dut1   +--------| dut2   |
                    |        |        |        |
                    +--------+        +--------+
    ```
#### Test setup
Set up an IP connectivity between dut1 and dut2.
dut1 is used as SFTP client and dut2 as SFTP server.

### Test case 1.01
Test case checks if dut1 can download a file from dut2 when SFTP server is disabled by default.
### Description
On dut1, perform a SFTP get from dut2.
### Test result criteria
#### Test pass criteria
On dut1, SFTP get failed.
#### Test fail criteria
On dut1, SFTP get succeeded.

### Test case 1.02
Test case enables SFTP server service on dut2 and then dut1 copies a file.
### Description
On dut2 CLI, in configure terminal and execute, `sftp server enable`.
On dut1, perform a SFTP get from dut2.
### Test result criteria
#### Test pass criteria
On dut1, SFTP get succeeded.
#### Test fail criteria
On dut1, SFTP get failed.

### Test case 1.03
Test case performs SFTP put from dut1 to dut2 when SFTP server is enabled.
### Description
On dut1, perform a SFTP put to dut2.
### Test result criteria
#### Test pass criteria
On dut1, SFTP put succeeded.
#### Test fail criteria
On dut1, SFTP put failed.

### Test case 1.04
Test case disables SFTP service on dut2 and then dut1 copies a file.
### Description
On dut2 CLI, in configure terminal and execute, `no sftp server enable`.
On dut1, perform a SFTP get from dut1.
### Test result criteria
#### Test pass criteria
On dut1, SFTP get failed.
#### Test fail criteria
On dut1, SFTP get succeeded.

### Test case 1.05
Test case performs SFTP put from dut1 to dut2 when SFTP server is disabled.
### Description
On dut1, perform a SFTP put to dut2.
### Test result criteria
#### Test pass criteria
On dut1, SFTP put failed.
#### Test fail criteria
On dut1, SFTP put succeeded.

### Test case 1.06
Test case to verify the SFTP server status after reboot.
### Description
On dut2, enable SFTP server.
Save the configurations using command `copy running-config startup-config`.
Reboot.
### Test result criteria
#### Test pass criteria
After reboot, from dut1 SFTP get succeeded.
#### Test fail criteria
After reboot, from dut1 SFTP get failed.

## Verify SFTP client
### Objective
Verify SFTP client functionality.
### Requirements
The requirements for this test case are:
 - 2 switches

### Setup
#### Topology Diagram
    ```ditaa

                    +---+----+        +--------+
                    |        |        |        |
                    + dut1   +--------| dut2   |
                    |        |        |        |
                    +--------+        +--------+
    ```
#### Test setup
On dut2, enable SFTP server.
Set up an IP connectivity between dut1 and dut2.

### Test case 2.01
Test case to verify SFTP client get operation to a specific destination.
### Description
On dut1 CLI, enter the command `copy sftp <user-name> <hostIP> <source-path> <destination-path>`.
### Test result criteria
#### Test pass criteria
On dut1, SFTP get succeeded.
#### Test fail criteria
On dut1, SFTP get failed.

### Test case 2.02
Test case to verify SFTP get operation to default destination.
### Description
On dut1 CLI, enter the command `copy sftp <user-name> <hostIP> <source-path>`.
### Test result criteria
#### Test pass criteria
On dut1, SFTP get succeeded.
#### Test fail criteria
On dut1, SFTP get failed.

### Test case 2.03
Test case to verify SFTP client get.
### Description
On dut1 CLI, enter the command `copy sftp <user-name> <hostIP>`.
On dut1, perform `get <source-path> <destination-path>`.
### Test result criteria
#### Test pass criteria
On dut1, SFTP get succeeded.
#### Test fail criteria
On dut1, SFTP get failed.

### Test case 2.04
Test case to verify SFTP client put.
### Description
On dut1 CLI, enter the command `copy sftp <user-name> <hostIP>`.
On dut1, perform `put <source-path> <destination-path>`.
### Test result criteria
#### Test pass criteria
On dut1, SFTP put succeeded.
#### Test fail criteria
On dut1, SFTP put failed.
