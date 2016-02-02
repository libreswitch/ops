# Show Tech Infrastructure Developer Guide

## Contents


	- [Overview](#overview)
	- [Support for JSON output](#support-for-json-output)
	- [How to add new feature into show tech](#how-to-add-new-feature-into-show-tech)
		- [Sample yaml file (simple configuration supporting only text output)](#sample-yaml-file-simple-configuration-supporting-only-text-output)
		- [Sample yaml file (supporting both text and JSON output)](#sample-yaml-file-supporting-both-text-and-json-output)
		- [Sample yaml file with two feature definition is shown below](#sample-yaml-file-with-two-feature-definition-is-shown-below)
- [Show tech System Feature](#show-tech-system-feature)
- [Show Tech LLDP Feature](#show-tech-lldp-feature)
	- [Testing](#testing)
		- [Running CT test for Show Tech](#running-ct-test-for-show-tech)

## Overview
Show Tech Infrastructure is used to collect the summary of switch or feature specific information.  This Infrastructure will run a collection of show commands and produces the output in text format.  The collection of show commands per feature are present in the show tech configuration file, accordingly show tech will use those commands for the given feature.  The output of the show tech command is mainly useful to analyze the system/feature behavior.

## Support for JSON output
Currently show tech infra produces output in plain text form.  It is the collection of cli show command outputs for each feature specified.   Parsing and gathering information from this text data is difficult, hence it is desired to provide show tech output in JSON format in addition to the text format.  In order to achieve this functionality, the show tech infra will directly read the configured tables and columns from the ovsdb and produces them as JSON output.

## How to add new feature into show tech
Show Tech infra uses the show tech configuration (yaml ) file to understand the list of supported features as well as the corresponding cli commands to be used for each of those features.

The configuration yaml file is placed in ops-supportability repo under the path "ops-supportability/conf/ops_showtech.yaml"

The structure of this file is as shown below


- feature
  * feature_name
  * feature_desc
  * cli_cmds
	   * "command1"
	   * "command2"
	   * ...
  * ovsdb
	  * table:
		  * table_name
		  * col_names
			  * "column1"
			  * "column2"
			  * ....


### Sample yaml file (simple configuration supporting only text output)

```ditaa

---
  feature:
  -
    feature_desc: "Show Tech System"
    feature_name: system
    cli_cmds:
      - "show version"
      - "show system"
      - "show vlan"
```

### Sample yaml file (supporting both text and JSON output)
```ditaa
---
  feature:
  -
    feature_desc: "Link Layer Discovery Protocol"
    feature_name: lldp
    cli_cmds:
      - "show lldp configuration"
      - "show lldp statistics"
      - "show lldp counters"
    ovsdb:
      -
        table:
          -
            table_name: system
            col_names:
              - other_config
              - lldp_statistics
      -
        table:
          -
            table_name: interface
            col_names:
              - other_config
              - lldp_statistics
      -
        table:
          -
            table_name: subsystem
            col_names:
              - other_config
              - lldp
              - lldp_subsys
```

For eg., to add support for lldp feature, add the corresponding feature name, feature description, cli commands and ovsdb table details to the configuration file as shown in the eg., below.


### Sample yaml file with two feature definition is shown below

```ditaa

---
# Show tech System Feature
  feature:
  -
    feature_desc: "Show Tech System"
    feature_name: system
    cli_cmds:
      - "show version"
      - "show system"
      - "show vlan"
# Show Tech LLDP Feature
  feature:
  -
    feature_desc: "Link Layer Discovery Protocol (LLDP)"
    feature_name: lldp
    cli_cmds:
      - "show lldp statistics"
      - "show lldp configuration"
      - "show lldp neighbor-info"
    ovsdb:
      -
        table:
          -
            table_name: system
            col_names:
              - other_config
              - lldp_statistics
      -
        table:
          -
            table_name: interface
            col_names:
              - other_config
              - lldp_statistics
      -
        table:
          -
            table_name: subsystem
            col_names:
              - other_config
              - lldp
              - lldp_subsys

```


## Testing
Once the configuration file is modified, test the following three cli commands and verify the output

| Command | Expectation|
|:--------|:----------|
| **show tech** | Runs show tech for all supported features.  Please make sure that your newly added feature commands run successfully as part of the show tech |
| **show tech list**| Lists all the supported show tech features.  Please make sure it list your newly added feature name and desc. |
| **show tech FEATURE**| Runs show tech for the feature newly added and verifyt the output |


*Please note that the show tech output in json format is currently not supported.   But we request you to add the corresponding ovsdb configuration in the yaml file so that we don't need to revisit it later.*


### Running CT test for Show Tech
Please run the following ct test to verify that the show tech infra is working fine with your configuration changes.

`make devenv_ct_test src/ops-supportability/test/show-tech_test.py`
