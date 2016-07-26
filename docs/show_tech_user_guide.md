# Show Tech Infrastructure

## Contents


- [Show Tech Infrastructure](#show-tech-infrastructure)
	- [Contents](#contents)
	- [Overview](#overview)
	- [How to use the Show Tech feature](#how-to-use-the-show-tech-feature)
		- [Setting up the basic configuration](#setting-up-the-basic-configuration)
		- [Verifying the configuration](#verifying-the-configuration)
		- [Troubleshooting the configuration](#troubleshooting-the-configuration)
			- [Condition](#condition)
			- [Cause](#cause)
			- [Remedy](#remedy)
	- [CLI](#cli)



## Overview
The Show Tech Infrastructure is used to collect a summary of switch or feature specific information.  This Infrastructure runs a collection of show commands and produces the output in text format.  The collection of show commands per feature are present in the show tech configuration file, accordingly show tech displays those commands for the given feature.  The output of the show tech command is mainly useful to analyze system or feature behavior. Tools can be developed to parse show tech command output in order to arrive at a meaningful conclusion and aid in  troubleshooting.

## How to use the Show Tech feature

- To collect the switch wide show tech information, run the cli command `show tech`.
- To collect a feature specific show tech information, run the cli command `show tech FEATURE-NAME`.
- To display the list of features supported by show tech, run the cli command `show tech lis`.

### Setting up the basic configuration

The Show Tech infrastructure loads its configuration from the show tech configuration yaml file located in (/etc/openswitch/supportability/ops_showtech.yaml).
This file contains the default configuration for show tech.

### Verifying the configuration

 Execute the cli command `show tech list` and verify the features are listed as configured.

### Troubleshooting the configuration

#### Condition
1.  The `show tech` cli commands result in the following error:

`Failed to obtain Show Tech Configuration`

#### Cause
This "Failed to obtain Show Tech Configuration" error can appear in the following two cases:
- The ops_showtech.yaml configuration file is missing in its path
- The ops_showtech.yaml configuration file is wrongly configured.

#### Remedy
1. Ensure that the `ops_showtech.yaml file` is present in its path (/etc/openswitch/supportability/ops_showtech.yaml).
2. Verify that the ops_showtech.yaml configuration file is a valid yaml file, using the  yaml lint tools.
3. Verify that the structure of the configuration is valid.  Refer [here](/documents/user/show-tech_design#show-tech-configuration-yaml-file) for structure information and examples.

#### Condition
2. The `show event` command within `show tech` has timed out.

#### Cause
There is a time limit of 60 seconds for each command within show tech, on exceeding that, the command will time out.
When switch contains too many event logs and show tech is executed via a telnet connection, there is a chance for `show event` command to time out.

#### Remedy
1. Use a ssh connection to access CLI and execute `show tech`.
2. Use the command `show tech localfile <filename>`

## CLI

Click [here](/documents/user/show-tech_cli#commands-summary) for the CLI commands related to the named feature.
