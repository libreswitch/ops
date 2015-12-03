# AAA Feature Test Cases

The following test cases verify AAA configuration :

- [Test Cases](#test-cases)
	- [Verify login with local authentication](#verify-login-with-local-authentication)
		- [Test case 1.01 : Verify local authentication](#test-case-1.01-:-verify-local-authentication)
		- [Test case 1.02 : Verify local authentication with wrong password](#test-case-1.02-:-verify-local-authentication-with-wrong-password)
	- [Verify login with RADIUS server authentication](#verify-login-with-radius-server-authentication)
		- [Test case 2.01 : Verify RADIUS authentication with RADIUS credentials](#test-case-2.01-:-verify-radius-authentication-with-radius-credentials)
		- [Test case 2.02 : Verify RADIUS authentication with wrong RADIUS credentials](#test-case-2.02-:-verify-radius-authentication-with-wrong-radius-credentials)
	- [Verify fallback to local authentication](#verify-fallback-to-local-authentication)
		- [Test case 3.01 : Verify fallback to local authentication](#test-case-3.01-:-verify-fallback-to-local-authentication)
	- [Verify secondary RADIUS server authentication](#verify-secondary-radius-server-authentication)
		- [Test case 4.01 : Verify authentication with secondary RADIUS server](#test-case-4.01-:-verify-authentication-with-secondary-radius-server)
	- [Verify SSH authentication method](#verify-ssh-authentication-method)
		- [Test case 5.01 : Verify SSH public key authentication](#test-case-5.01-:-verify-ssh-public-key-authentication)
		- [Test case 5.02 : Verify SSH password authentication](#test-case-5.02-:-verify-ssh-password-authentication)

#Test Cases #
##  Verify login with local authentication ##
### Objective ###
To configure local authentication and log in with local credentials.
### Requirements ###
The requirements for this test case are:
 - Docker version 1.7 or above.
 - Accton AS5712 switch docker instance.

### Setup ###
#### Topology Diagram ####
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

#### Test Setup ####
AS5712 switch instance.

### Test case 1.01 : Verify local authentication ###
### Description ###
Verify whether authentication is successful with local credentials.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to log in with local credentials.
#### Test Fail Criteria ####
User is not able to log in with local credentials.

### Test case 1.02 : Verify local authentication with wrong password ###
### Description ###
Verify whether authentication is a failure with wrong local credentials.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is not able to log in with wrong credentials.
#### Test Fail Criteria ####
User is able to log in with wrong credentials.

##  Verify login with RADIUS server authentication ##
### Objective ###
Verify whether authentication is successful with RADIUS server credentials.
### Requirements ###
The requirements for this test case are:
- Configure RADIUS server details on the switch and make RADIUS server reachable.
- Docker version 1.7 or above.
- Accton 5712 switch docker instance.
- Host instance with RADIUS server installed. (This test took freeradius server as reference)

### Setup ###
#### Topology Diagram ####

     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  Host with         |
     |                |eth0                               eth1 |  RADIUS server     |
     |                |                                        |                    |
     +----------------+                                        +--------------------+

#### Test Setup ####
AS5712 switch instance and host with RADIUS server.

### Test case 2.01 : Verify RADIUS authentication with RADIUS credentials ###
### Description ###
Verify whether RADIUS authentication is success with credentials configured on RADIUS server.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is able to login with RADIUS server credentials.
#### Test Fail Criteria ####
User is not able to login with RADIUS server credentials.

### Test case 2.02 : Verify RADIUS authentication with wrong RADIUS credentials ###
### Description ###
Verify whether RADIUS authentication is failure with wrong credentials.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is not able to login with wrong RADIUS credentials.
#### Test Fail Criteria ####
User is able to login with wrong RADIUS credentials.

##  Verify fallback to local authentication##
### Objective ###
Configure RADIUS server and make it un reachable, then authentication falls back to local.
### Requirements ###
The requirements for this test case are:
- Configure RADIUS server details on the switch and make RADIUS server un reachable.
- Docker version 1.7 or above.
- Accton 5712 switch docker instance.
- Host instance with RADIUS server installed. (This test took freeradius server as reference)
### Setup ###
#### Topology Diagram ####


     +----------------+                                        +--------------------+
     |                |                                        |                    |
     | AS5712 switch  |<-------------------------------------->|  Host with         |
     |                |eth0                               eth1 |  RADIUS server     |
     |                |                                        |                    |
     +----------------+                                        +--------------------+


#### Test Setup ####
AS5712 switch instance and host with RADIUS server.

### Test case 3.01 : Verify fallback to local authentication###
### Description ###
Verify whether authentication is success with local credentials when RADIUS server is not reachable.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is be able to login with local credentials.
#### Test Fail Criteria ####
User is not able to login with local credentials.

##  Verify secondary RADIUS server authentication##
### Objective ###
Configure two RADIUS servers and make first RADIUS server un reachable. Then authentication should happen through secondary RADIUS server.
### Requirements ###
The requirements for this test case are:
- Configure RADIUS server detailson the switch and make RADIUS server un reachable.
- Docker version 1.7 or above.
- Accton 5712 switch docker instance.
- Two host instance with RADIUS server installed. (This test took freeradius server as reference)
### Setup ###
#### Topology Diagram ####


     +---------------------+           +----------------------+        +-----------------------+
     |   HOST              |           |                      |eth0    |       HOST            |
     |primary RADIUS server|<----+---->|     AS5712           |<--+--->|Secondary RADIUS server|
     |                    h1-eth0  eth0|                      |    h2-eth0                     |
     |                     |           |                      |        |                       |
     +--------------------->           +----------------------+        +-----------------------+

#### Test Setup ####
AS5712 switch instance and two host with RADIUS server.

### Test case 4.01 : Verify authentication with secondary RADIUS server ###
### Description ###
Verify whether authentication is success with secondary RADIUS server credentials when first RADIUS server is not reachable.
### Test Result Criteria ###
#### Test Pass Criteria ####
User is be able to login with secondary RADIUS server credentials.
#### Test Fail Criteria ####
User is not able to login with secondary RADIUS server credentials.

##  Verify SSH authentication method##
### Objective ###
Configure SSH authentication method to be either password authentication or public key authentication. Then verify if user authentication is successful.
### Requirements ###
The requirements for this test case are:
- Accton 5712 switch docker instance.

### Setup ###
#### Topology Diagram ####

     +----------------+
     |                |
     | AS5712 switch  |
     |                |
     +----------------+

#### Test Setup ####
AS5712 switch instance.

### Test case 5.01 : Verify SSH public key authentication###
### Description ###
Verify whether ssh public key authentication method is successful or not.
### Test Result Criteria ###
#### Test Pass Criteria ####
SSH public key authentication is enabled and respective SSH config files are modified accordingly. User whose public key is copied to `/home/<user>/.ssh/` by auto provisioning feature can login automatically.
#### Test Fail Criteria ####
SSH public key authentication is not enabled and respective SSH config files are not modified accordingly and login fails.

### Test case 5.02 : Verify SSH password authentication###
### Description ###
Verify whether ssh password authentication method is successful or not. Password is prompted and user need to authenticate with valid passowrd.
### Test Result Criteria ###
#### Test Pass Criteria ####
SSH password authentication is enabled and respective SSH config files are modified accordingly. Login is successful with the password given by the user.
#### Test Fail Criteria ####
SSH password authentication is not enabled and respective SSH config files are not modified accordingly and login fails.
