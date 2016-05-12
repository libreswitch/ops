# Show Vlog User Guide

## Contents

- [Overview](#overview)
- [Show vlog command to display vlogs](#show-vlog-command-to-display-vlogs)
	- [Filter vlogs based on daemon name](#filter-vlogs-based-on-daemon-name)
	- [Filter vlogs based on severity](#filter-vlogs-based-on-severity)
- [Using the show vlog config command to access feature/daemon information](#using-the-show-vlog-command-to-access-feature-daemon-information)
    - [List the vlog supported features](#list-vlog-supported-features)
    - [Severity log level of a feature](#severity-log-level-of-a-feature)
    - [Severity log levels of supported features](#severit-log-levels-of-supported-features)
    - [Severity log level of a daemon](#severity-log-level-of-a-daemon)
    - [Configure the logging level of features and daemons](#configure-the-logging-level-of-features-and-daemons)
- [Troubleshooting the configuration](#troubleshooting-the-configuration)
	- [Condition](#condition)
	- [Configuration file is missing](#configuration-file-is-missing)
	- [Configuration file is not properly configured](#configuration-file-is-not-properly-configured)
- [Feature to daemon mapping](#feature-to-daemon-mapping)
- [References](#references)

## Overview
The `show vlog` command is used to display vlog messages of ops daemons.

The `show vlog config` command is used to display a list of features and corresponding daemons log levels of syslog and file destinations. The `show vlog config` command is useful to generate switch feature vlog configuration log levels for administrators, developers, support, and lab staff.

## Show vlog command to display vlogs
The `show vlog` command is used to display vlog messages of ops daemons. There are various ways to filter the vlog messages.

### Filter vlogs based on daemon name

The `show vlog daemon <daemon_name>` command is used to filter the vlog messages based on a daemon-name/word. This command displays only vlog messages for the specified daemon-name/word.

### Filter vlogs based on severity
The `show vlog severity <emer/err/warn/info/debug>` command is used to filter and display the vlog messages of a specified severity level and above.

## Using the show vlog command to access feature/daemon information

There are various ways to access supported feature information using the `show vlog config` command.

### List vlog supported features
Use the `show vlog config list` command to get the list of supported features on the console with descriptions.

### Severity log level of a feature
Use the `show vlog config feature <feature_name>` command to capture log levels of file and syslog destinations on the console for a specific feature.

### Severity log levels of supported features
Use the `show vlog config` command to get the list of supported features, and corresponding daemons' log levels of file and syslog destinations, on the console.

### Severity log level of a daemon
Use the `show vlog config daemon <daemon_name>` command to capture log levels of file and syslog destinations on the console for the specified daemon.

### Configure feature logging level and destination
Configure the switch using the
`vlog (feature|daemon) <name> <syslog/file/all> <emer/err/warn/info/dbg>` command in configuration mode.
Use the `show vlog config feature <feature_name>` and `show vlog config daemon <daemon_name>`command to obtain the corresponding feature/daemon log level changes of file and syslog destinations on the console.

## Troubleshooting the configuration

### Condition
The `show vlog config` command results in the following error
'Failed to capture vlog information <feature/daemon>'

### Configuration file is missing
If the error `ops_featuremapping.yaml configuration file is missing in its path` message appears, ensure that the `ops_featuremapping.yaml` file is present in the `/etc/openswitch/supportability/ops_featuremapping.yaml` path.

### Configuration file is not properly configured
If the error `ops_featuremapping.yaml configuration file is wrongly configured` message appears,
use the yaml tools to confirm that the configuration file (ops_featuremapping.yaml) is valid.

## Feature to daemon mapping
The `/etc/openswitch/supportability/ops_featuremapping.yaml` file contains feature to daemon mapping configurations.

## References
* [Show Vlog Commands](show_vlog_cli)
