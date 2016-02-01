# Infrastructure for the show events command

## Contents

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
    - [Setting up the basic configuration](#setting-up-the-basic-configuration)
    - [Verifying the configuration](#verifying-the-configuration)
    - [Troubleshooting the configuration](#troubleshooting-the-configuration)
        - [Configuration file is missing in its path](#Configuration file is missing in its path)
        - [File is not properly configured](#File is not properly configured)


## Overview

The `show events` command is used to display events for all of the supported features. This CLI is useful to generate switch event logs for administrators, developers, support, and lab staff. Problem events and solutions are also easily obtainable using the CLI.

## How to use the CLI

	To access events for supported features or daemons in the switch, run the CLI `show events`command.

### Setting up the basic configuration

The `show events` command infrastructure loads its configuration from the "showevent configuration yaml" file located in (/etc/openswitch/supportability/ops_events.yaml). This file contains the default configuration for the `show events` command.

### Verifying the configuration

 Execute the CLI `show events` command and verify that the features are configured.

### Troubleshooting the configuration

#### Configuration file is missing in its path.

If the error `ops_events.yaml configuration file is missing in its path` appears, ensure that the `ops_events.yaml` file is present in the (/etc/openswitch/supportability/ops_events.yaml) path.

#### File is not properly configured

If the error `ops_events.yaml configuration file is wrongly configured` appears, use the yaml tools to confirm that the configuration file (ops_events.yaml) is valid.
