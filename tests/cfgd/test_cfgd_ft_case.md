# Config persistent component test cases

## Contents##
- [Test cases to verify Configuration Persistence](#test-cases-to-verify-configuration-persistence)
    - [Test to verify startup config push during boot](#test-to-verify-startup-config-push-during-boot)


##Test cases to verify Configuration Persistence ##
### Objective ###
Test cases to verify that the configdb and the cfgd daemon work.
### Requirements ###
The requirements for this test case are:

 - AS5712 switch

### Setup ###
#### Topology diagram ####
```ditaa
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+
```

### Test to verify startup config push during boot ###
#### Description ####
Test to verify that the config persistence daemon copies the startup config saved in the configdb to the running db during boot up time, then saves a startup config with hostname configured to "CT-TEST" and the system is rebooted.

### Test result criteria ###
#### Test pass criteria ####
Test case result is a success if the hostname in the System table is "CT-TEST"
#### Test fail criteria ####
Test case result is a fail if the hostname in the System table is not "CT-TEST".
