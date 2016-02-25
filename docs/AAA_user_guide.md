# AAA feature
## Contents

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
    - [Scenario 1](#scenario-1)
        - [Setting up scenario 1 basic configuration](#setting-up-scenario-1-basic-configuration)
        - [Setting up scenario 1 optional configuration](#setting-up-scenario-1-optional-configuration)
        - [Verifying scenario 1 configuration](#verifying-scenario-1-configuration)
    - [Troubleshooting scenario 1 configuration](#troubleshooting-scenario-1-configuration)
    - [Scenario 2](#scenario-2)
        - [Setting up scenario 2 basic configuration](#setting-up-scenario-2-basic-configuration)
        - [Setting up scenario 2 optional configuration](#setting-up-scenario-2-optional-configuration)
        - [Verifying scenario 2 configuration](#verifying-scenario-2-configuration)
    - [Troubleshooting scenario 2 configuration](#troubleshooting-scenario-2-configuration)
    - [Scenario 3](#scenario-3)
        - [Setting up scenario 3 basic configuration](#setting-up-scenario-3-basic-configuration)
        - [Setting up scenario 3 optional configuration](#setting-up-scenario-3-optional-configuration)
        - [Verifying scenario 3 configuration](#verifying-scenario-3-configuration)
    - [Troubleshooting scenario 3 configuration](#troubleshooting-scenario-3-configuration)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The AAA feature is used for authenticating users who access the switch management interface using console, SSH, or REST. The AAA feature supports the following:

- Local or RADIUS authentication.
- Configuring the RADIUS authentication type.
- Configuring RADIUS servers (maximum of 64 RADIUS servers).
- Configuring the SSH authentication method.

This feature currently supports user authentication based on user name and password.

## How to use the feature
### Scenario 1
#### Setting up scenario 1 basic configuration
 1. Create a user on the switch, and configure a password.
 2. Configure the authentication mode. Select one of the following options:
    - local
    - RADIUS
 3. Configure RADIUS servers.

#### Setting up scenario 1 optional configuration
 1. Change the default value of the shared secret used for communication between the switch and the RADIUS server.
 2. Change the default value of the port used for communication with the RADIUS server.
 3. Change the default value of the connection retries.
 4. Change the connection timeout default value.
 5. Change the RADIUS authentication type to CHAP or PAP (default is PAP).

#### Verifying scenario 1 configuration
 1. Verify the configuration using the `show` command.
 2. Verify the configuration using the `show running-config` command for non default values.

### Troubleshooting scenario 1 configuration
#### Case 1
##### Condition
The local authentication is configured, but the user is unable to log in with local password.

##### Possible causes
- The AAA daemon is not active. Check the AAA status with the following command: ``` ps -ef | grep ops_aaautilspamcfg ```.
- The PAM configuration files are not present. Check for the presence of the common-****-access files located at `/etc/pam.d/`.
- The wrong password has been entered.

##### Remedies
- If the daemon is not running, restart it by entering `systemctl start aaautils.service`.
- If the PAM configuration files are removed, copy the PAM configuration files from another switch located at `etc/pam.d/`.
- Verify that the correct password has been entered.
- For more information, verify the `auth.log` file located at `/var/log/auth.log`.

#### Case 2
##### Condition
The RADIUS authentication is configured, but the user is unable to log in with the RADIUS server password.

##### Possible causes
- The AAA daemon is not active. Check the AAA status with the following command: ``` ps -ef | grep ops_aaautilspamcfgg ```.
- The RADIUS server is not active. Verify if the RADIUS server is stopped.
- There appears to be a difference in the configuration of the RADIUS servers on the switch and on the host. Enter the `show radius-server` command on the switch to verify the RADIUS servers' configuration.
- The wrong password has been entered.

##### Remedies
- If the daemon is not running, restart it by entering `systemctl start aaautils.service`.
- If the PAM configuration files are removed, copy the PAM configuration files from another switch located at `etc/pam.d/`.
- Restart the RADIUS server.
- Verify that the correct password has been entered.
- For more information, verify the `auth.log` file located at `/var/log/auth.log`.

### Scenario 2
#### Setting up scenario 2 basic configuration
 1. Enable RADIUS authentication.
 2. Enable fallback to local authentication.
 3. Configure the RADIUS server.

#### Setting up scenario 2 optional configuration
 1. Change the default value of the shared secret used for communication between the switch and the RADIUS server.
 2. Change the default value of the port used for communication with the RADIUS server.
 3. Change the default value of the connection retries.
 4. Change the connection timeout default value.
 5. Change the RADIUS authentication type to CHAP or PAP (default is PAP).

#### Verifying scenario 2 configuration
 1. Verify the configuration using the `show` command.
 2. Verify the configuration using the `show running-config` command for non-default values.

### Troubleshooting scenario 2 configuration
#### Condition
The RADIUS server is unreachable, and the user cannot log in with local credentials even though fallback to local is enabled.

#### Possible causes
- The AAA daemon is not active. Check the AAA status with the following command: ``` ps -ef | grep ops_aaautilspamcfg ```.
- The PAM configuration files are not present. Check for the presence of the *common-****-access* files located at `/etc/pam.d/`.
- The wrong password has been entered.

#### Remedies
- If the daemon is not running, restart it by entering `systemctl start aaautils.service`.
- If the PAM configuration files are removed, copy the PAM configuration files from another switch located at `etc/pam.d/`.
- Verify that the correct password has been entered.
- For more information, verify the `auth.log` file located at `/var/log/auth.log`.

### Scenario 3
#### Setting up scenario 3 basic configuration
 1. Create a user on the switch.
 2. Enable a SSH password or a public key authentication method.

#### Setting up scenario 3 optional configuration
N/A

#### Verifying scenario 3 configuration
 1. Verify the configuration using the `show` command.
 2. Verify the configuration using the `show running-config` command for non-default values.

### Troubleshooting scenario 3 configuration
#### Case 1
##### Condition
The SSH password authentication is enabled, but the user is not able to log in with the password.

##### Possible causes
- The AAA daemon is not active. Check the AAA status with the following command: ``` ps -ef | grep ops_aaautilspamcfg ```.
- The SSH configuration file is not present. Check for the presence of the *sshd_config* file located at `/etc/ssh/`.
- The wrong password has been entered.

##### Remedies
- If the daemon is not running, restart it by entering `systemctl start aaautils.service`.
- If the SSH configuration files is removed, copy the SSH configuration file *sshd_config* from another switch.
- Verify that the correct password has been entered.
- For more information, verify the `auth.log` file located at `/var/log/auth.log`.

#### Case 2
##### Condition
SSH public key authentication is enabled, but the user is not able to login.

##### Possible causes
- The AAA daemon is not active. Check the AAA status with the following command: ``` ps -ef | grep ops_aaautilspamcfg ```.
- The SSH configuration file is not present. Check for the presence of the *sshd_config* file located at `/etc/ssh/`.
- The user's public key is not present on the switch. Check for the presence of the public key by entering something similar to the following with the user's information:
`/home/<user>/.ssh/id_rsa.pub`

##### Remedies
- If the daemon is not running, restart it by entering `systemctl start aaautils.service`.
- If the SSH configuration files is removed, copy the SSH configuration file *sshd_config* from another switch.
- Copy the public key manually to the switch by entering something similar with the user's information as follows: `/home/<user>/.ssh/id_rsa.pub`
- For more information, verify the `auth.log` file located at `/var/log/auth.log`.

## CLI
Click [here](/documents/user/AAA_cli) for the CLI commands related to the AAA feature.

## Related features
The auto provisioning script is used to get SSH public keys. For more information on auto provisioning see [Auto Provisioning](/documents/user/autoprovision_user_guide).
