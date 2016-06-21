# SFTP Feature Test Cases

## Contents
- [Verify SFTP server configuration](#verify-sftp-server-configuration)
	- [Verify SFTP copy without SFTP server service](#verify-sftp-copy-without-sftp-server-service)
	- [Verify SFTP server enable](#verify-sftp-server-enable)
	- [Verify SFTP server status](#verify-sftp-server-status)
- [Verify SFTP client](#verify-sftp-client)
	- [Verify SFTP client in an interactive mode](#verify-sftp-client-in-an-interactive-mode)
	- [Verify SFTP client in a non-interactive mode](#verify-sftp-client-in-a-non-interactive-mode)
    - [Verify SFTP client in an interactive mode for netop user](#verify-sftp-client-in-an-interactive-mode-for-netop-user)
    - [Verify SFTP client in a non-interactive mode for netop user](#verify-sftp-client-in-a-non-interactive-mode-for-netop-user)
	- [Verify SFTP copy on a non mgmt interface](#verify-sftp-copy-on-a-non-mgmt-interface)
	- [Verify SFTP copy from multiple vty sessions](#verify-sftp-copy-from-multiple-vty-sessions)

## Verify SFTP server configuration
### Objective
To verify enablement/disablement of the SFTP server.
### Requirements
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton switch docker instance/physical hardware switch.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with IPv4 addresses/IPv6 addresses.

### Setup
#### Topology Diagram
```ditaa

     +----------------+                                        +--------------------+
     |                |                                        |                    |
     |    DUT01       |<-------------------------------------->|  Switch01          |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+
```

### Verify SFTP copy without SFTP server service
### Description
Verify SFTP copy is not working when SFTP server service is disabled.
### Test Result Criteria
#### Test Pass Criteria
User is unable to perform the SFTP copy.
#### Test Fail Criteria
User is able to perform the SFTP copy.

### Verify SFTP server enable
### Description
Enable the SFTP server on switch1 using appropriate CLI.
### Test Result Criteria
#### Test Pass Criteria
User is able to initiate an SFTP server.
#### Test Fail Criteria
User is unable to initiate a SFTP server.

### Verify SFTP server status
### Description
Verify the SFTP server status using the show command.
### Test Result Criteria
#### Test Pass Criteria
User is able to check for the current SFTP server status as either enable/disable.
#### Test Fail Criteria
User is unable to execute the show command.

## Verify SFTP client
### Objective
To verify Interactive/Non-Interactive mode of the SFTP client.
### Requirements
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton switch docker instance/physical hardware switch.
 - A topology with a single link between two switches, switch 1 and switch 2 are configured with IPv4 addresses/IPv6 addresses.

### Setup
#### Topology Diagram
```ditaa

     +----------------+                                        +--------------------+
     |                |                                        |                    |
     |    DUT01       |<-------------------------------------->|  Switch01          |
     |                |int1                                int1|                    |
     |                |                                        |                    |
     +----------------+                                        +--------------------+
```

### Verify SFTP client in an interactive mode
### Description
Verify SFTP client is working in the interactive mode.
### Test Result Criteria
#### Test Pass Criteria
User is able to enter the interactive mode and perform get/put.
#### Test Fail Criteria
User is unable to enter the interactive mode.

### Verify SFTP client in a non-interactive mode
### Description
Verify switch1, working as an SFTP client, is able to perform a secure copy
from switch2, which is providing SFTP server service.
### Test Result Criteria
#### Test Pass Criteria
User is able to perform secure copy from switch2.
#### Test Fail Criteria
User is unable to perform secure copy from switch2.

### Verify SFTP client in an interactive mode for netop user
### Description
Verify SFTP client copy is not allowed for netop users.
### Test Result Criteria
#### Test Pass Criteria
Netop user is unable to perform the SFTP client copy.
#### Test Fail Criteria
Netop user is able to perform the SFTP client copy.

### Verify SFTP client in a non-interactive mode for netop user
### Description
Verify SFTP client copy is not allowed for netop users.
### Test Result Criteria
#### Test Pass Criteria
Netop user is unable to perform the SFTP client copy.
#### Test Fail Criteria
Netop user is able to perform the SFTP client copy.

### Verify SFTP copy on a non mgmt interface
### Description
Verify SFTP copy is not working on a non mgmt interface.
### Test Result Criteria
#### Test Pass Criteria
User is unable to perform the SFTP copy.
#### Test Fail Criteria
User is able to perform the SFTP copy.

### Verify SFTP copy from multiple vty sessions
### Description
Verify SFTP copy from a number of vty sessions.
### Test Result Criteria
#### Test Pass Criteria
User is able to perform the SFTP copy from different vty sessions.
#### Test Fail Criteria
User is unable to perform the SFTP copy from different vty sessions.
