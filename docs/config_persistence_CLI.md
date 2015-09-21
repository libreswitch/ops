#CLI support for Config Persistence
## Contents##
- [1. Copy commands](#1.-copy-commands)
    - [1.1 Copy startup configuration to running configuration](#1.1-copy-startup-configuration-
to-running-configuration)
    - [1.2 Copy running configuration to startup configuration](#1.2-copy-running-configuration-
to-startup-configuration)
- [2. Show commands](#2.-show-commands)
    - [2.1 Show startup configuration](#2.1-show-startup-configuration)

## 1. Copy commands ##
###1.1 Copy startup configuration to running configuration
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

###1.2 Copy running configuration to startup configuration
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

##2. Show Commands ##
###2.1 Show startup configuration
#### Syntax ####
show startup-config

#### Description ####
To display the saved startup configuration in JSON format.

#### Authority ####
Admin
#### Parameters ####
None

#### Examples ####
```bash
switch # show startup-config
```
