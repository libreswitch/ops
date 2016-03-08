# Infrastructure for the Show Events Command

## Contents

- [Overview](#overview)
- [How to use the CLI](#how-to-use-the-cli)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
		- [Log filter options](#log-filter-options)
		- [Reverse list option](#reverse-list-option)
	- [Troubleshooting the configuration](#troubleshooting-the-configuration)
		- [Configuration file is missing in its path](#configuration-file-is-missing-in-its-path)
		- [File is not properly configured](#file-is-not-properly-configured)

## Overview

The `show events` command is used to display events for all of the supported features. This command is useful to generate switch event logs for administrators, developers, support staff, and lab staff. Problem events and solutions are also easily obtainable using the CLI.

## How to use the CLI

To access events for supported features or daemons in the switch, run the CLI `show events`command.
`
### Setting up the basic configuration

The `show events` command infrastructure loads its configuration from the "showevent configuration yaml" file located in (/etc/openswitch/supportability/ops_events.yaml). This file contains the default configuration for the `show events` command.

### Verifying the configuration

Execute the CLI `show events` command and verify that the features are configured.

#### Log filter options

The `show events` command provides log filter options to show only the logs of interest. The following filters are supported:

 * event-id
 * severity
 * category

These filter keywords can be used along with the `show events` command to filter logs accordingly.

#### Examples

To filter according to event ID 1002:
`show events event-id 1002`

To filter according to severity level of emergency:
`show events severity emer`

The following are the severity keywords supported in the CLI:
 * emer
 * alert
 * crit
 * error
 * warn
 * notice
 * info
 * debug

To filter according to interested log category:
`show events category LLDP`

A combination of all of these filters can also be used:
`show events event-id 1003 category LLDP severity emer`

#### Reverse list option

The show events output usually displays from oldest to latest in order.
You can make use of the `reverse` keyword to list logs from most recent to oldest.
This option can be used along with any of the log filters as well.

For example:
`show events reverse`
`show events event-id 1003 category LLDP severity emer reverse`

### Troubleshooting the configuration

#### Configuration file is missing in its path

If the error `ops_events.yaml configuration file is missing in its path` appears, ensure that the `ops_events.yaml` file is present in the (/etc/openswitch/supportability/ops_events.yaml) path.

#### File is not properly configured

If the error `ops_events.yaml configuration file is wrongly configured` appears, use the yaml tools to confirm that the configuration file (ops_events.yaml) is valid.
