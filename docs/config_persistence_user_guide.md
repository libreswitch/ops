# Config Persistence

## Table of contents
- [Table of contents](#table-of-contents)
- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
	- [Configuration types](#configuration-types)
	- [Startup configuration persistence](#startup-configuration-persistence)
	- [Configuration format](#configuration-format)
	- [Action taken during configuration save](#action-taken-during-configuration-save)
	- [System action taken during system boot](#system-action-taken-during-system-boot)
	- [User actions](#user-actions)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
 <!--Provide an overview here. This overview should give the reader an introduction of when, where and why they would use the feature. -->
There are two types of configurations: the current running configuration and the startup configuration. The running configuration is not persistent across reboots but the startup configuration is persistent across reboots. While there are currently no provisions to facilitate rollbacks or local preservation of old configurations, these functions are being investigated as further enhancements.

## How to use the feature
### Configuration types
1) Running: The running configuration is dynamic and is the current state of all config type elements in the OVSDB.

2) Startup: If present, the startup configuration will be used on the next boot.

### Startup configuration persistence
When a configuration is saved as a startup configuration, it is stored in the **configtbl** table in OVSDB. The **confgtbl** can have from zero to multiple rows.

The content of each row includes:

- type: Only supported type is startup.
- name: Unique name, specified either by the system or by the user (Currently not populated).
- writer: Identifies who requested this configuration to be saved (Currently not populated).
- date: Date/Time when this row was last modified (Currently not populated).
- config: Configuration data.
- hardware: JSON formatted list of dictionaries containing the following information for all subsystems configured by the configuration data (Currently not populated).

### Configuration format
The configuration data is stored as a JSON string. The schema used is the same schema used by the REST API.
### Action taken during configuration save
When the user requests that the running configuration be saved as a startup-config, the following actions are taken:

-  All **config** type OVSDB elements are extracted from the database and formatted into the configuration format as noted below.
-  If a startup row is not found in the **configdb**, create a new row with type=**startup** or overwrite the existing row and save the configuration to config row.
- Configtbl is updated with all required information.

### System action taken during system boot
Except for the configurations table, the OVSDB is not persisted across reboots, so that it is initially empty. After the platform daemons discover all present hardware and populate the OVSDV with relevant hardware information, the configuration daemon (cfgd) checks to see if any saved configuration exists by checking for a startup type entry. If a startup configuration is found, it is applied to the remaining tables. If a startup configuration is not found, cfgd notes the startup configuration was not found.

### User actions

The REST and CLI APIs provide rich commands for managing the configuration of the system, allowing the user to:

- Request that the current running configuration be saved as a startup configuration.
- Request that a startup configuration be written to the running configuration.
- Request a read/show of a startup configuration.
- Request a read/show of a running configuration.

## CLI
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](/documents/user/config_persistence_cli) for the CLI commands related to the configuration persistence feature.
## Related features
None.
