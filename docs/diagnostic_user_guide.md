# Diagnostic Dump User Guide

## Contents

- [Overview](#overview)
- [Using the diag-dump command to access feature information](#using-the-diag-dump-command-to-access-feature-information)
	- [List diagnostic supported features](#list-diagnostic-supported-features)
	- [Basic diagnostic on console](#basic-diagnostic-on-console)
	- [Basic diagnostic to file](#basic-diagnostic-to-file)
	- [Troubleshooting the configuration](#troubleshooting-the-configuration)
		- [Condition](#condition)
		- [Cause](#cause)
		- [Remedy](#remedy)
	- [Feature to daemon mapping](#feature-to-daemon-mapping)
- [References](#references)


## Overview
The diagnostic dump command is used to collect internal diagnostic information from single or multiple daemons mapped to a single feature.

## Using the diag-dump command to access feature information

There are various ways to get access to supported feature information using the `diag-dump` command as shown in the following sections.

### List diagnostic supported features
Execute the CLI "diag-dump list" command to get the list of supported features with descriptions on the console.

### Basic diagnostic on console
Execute the CLI "diag-dump <feature> basic" command to get basic diagnostic information on the console.

### Basic diagnostic to file
Execute the CLI "diag-dump <feature> basic <filename>" command to get basic diagnostic information into a file.

### Troubleshooting the configuration

#### Condition
The 'diag-dump' command results in the following error
'Failed to capture diagnostic information'


#### Cause
1. The ops_diagdump.yaml file is not present in the `/etc/openswitch/supportability/ops_diagdump.yaml` path.
2. The user may not have read permission.
3. The content of the yaml file is incorrect.


#### Remedy
1. Ensure that the yaml file is present in its `/etc/openswitch/supportability/ops_diagdump.yaml` path.
2. Ensure that the user has read permission for the yaml file.
3. Verify that the content of the yaml file is correct using the yaml lint tool.
4. Verify that the structure of the configuration is valid.

### Feature to daemon mapping
The `/etc/openswitch/supportability/ops_diagdump.yaml` file contains "feature to daemon mapping" configurations.

## References
* [Reference 1] 'diagnostic_user_guide.md'
