# Show Vlog Infrastructure Developer Guide

## Contents

- [Overview](#overview)
- [How to map feature to daemon in to show vlog ](#how-to-map-feature-to-daemon-in-to-show-vlog)
- [Testing](#testing)
	- [Running CT test for show vlog](#running-ct-test-for-show-vlog)
- [References](#references)


## Overview
The `show vlog` CLI is used to capture logging infrastructure in most of ops daemons.
This `show vlog config` CLI captures the log levels of file and syslog destinations for supported
features.

## How to map feature to daemon in to show vlog
Please add an entry for your daemon in the yaml file `/etc/openswitch/supportability/ops_featuremapping.yaml` as per format described below.

	```ditta
     -
       feature_name: "lldp"
       feature_desc: "Link Layer Discovery Protocol"
       daemon:
         - "ops-lldpd"

     -
       feature_name: "lacp"
       feature_desc: "Link Aggregation Control Protocol"
       daemon:
         - "ops-lacpd"
     -
       feature_name: "fand"
       feature_desc: "System Fan"
       daemon:
          - "ops-fand"
```

## Testing

Once the configuration file is modified, test the following CLI commands and verify the output.

| Command | Expectation|
|:--------|:-----------|
| **show vlog config** | Runs show vlog config for supported features.Ensure that your newly added feature commands run successfully as part of the show vlog config output |
| **show vlog config list** | List the supported features and description.Ensure that it lists your newly added feature name and description |
| **show vlog config feature <feature_name>** | Runs show vlog config for the newly added feature and verifies the ouput |
| **show vlog config daemon <daemon_name>** | Runs show vlog config for daemon directly |
| **show vlog daemon <daemon_name>** | Runs show vlog daemon to display vlogs for specified daemon|
| **show vlog severity <severity_level>** | Runs show vlog severity to display vlogs for specified severity level or above |
| **show vlog daemon  <daemon_name> severity <severity_level>** | This CLI displays vlogs for the specified ops-daemon only with specified severity level and above |

### Running CT test for show vlog
Run the following CT test to verify that the show vlog infrastructure is properly working with the configuration changes.

`make devenv_ct_test src/ops-supportability/test/show_vlog_test.py`

## References

* [Reference 1 ] `show_vlog_design.md`
* [Reference 2 ] `show_vlog_cli.md`
* [Reference 3 ] `show_vlog_test.md`
* [Reference 4 ] `show_vlog_user_guide.md`
* [Reference 5 ] `show_vlog_dev_guide.md`