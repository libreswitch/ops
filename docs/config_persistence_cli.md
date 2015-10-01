#CLI support for Config Persistence
## Contents##
- [Copy commands](#copy-commands)
    - [Copy startup configuration to running configuration](#copy-startup-configuration-
to-running-configuration)
    - [Copy running configuration to startup configuration](#copy-running-configuration-
to-startup-configuration)
- [Show commands](#show-commands)
    - [Show startup configuration](#show-startup-configuration)

## Copy commands ##
### Copy startup configuration to running configuration
#### Syntax ####
copy startup-config running-config

#### Description ####
The `copy startup-config running-config` command is used to save the configuration in the persistent database to the current configuration of the switch. This can be used as a rollback to the original configuration, if the modified configurations have to be discarded.

#### Authority ####
Admin
#### Parameters ####
None

#### Examples ####
```bash
switch # copy startup-config running-config
```

### Copy running configuration to startup configuration
#### Syntax ####
copy running-config startup-config

#### Description ####
The `copy running-config startup-config` command is used to save the current configuration of the switch to the persistent configuration database. The saved configuration is used as the startup configuration on the next boot up.
#### Authority ####
Admin
#### Parameters ####
None

#### Examples ####
```bash
switch # copy running-config startup-config
```

## Show Commands ##
### Show startup configuration
#### Syntax ####
show startup-config

#### Description ####
This command displays the saved startup configuration in CLI command format.

#### Authority ####
Admin
#### Parameters ####
None

#### Examples ####
```bash
switch # show startup-config
Startup configuration:
!
radius-server host 1.2.3.4 key testRadius
radius-server host 1.2.3.4 auth_port 2015
radius-server retries 5
radius-server timeout 10
!
```
