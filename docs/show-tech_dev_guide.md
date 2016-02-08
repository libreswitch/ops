# Show Tech Infrastructure Developer Guide

## Contents
- [Overview](#overview)
- [Support for JSON output](#support-for-json-output)
- [How to add new features in show tech](#how-to-add-new-features-in-show-tech)
	- [Sample YAML files](#sample-yaml-files)
		- [Simple configuration supporting only text output](#simple-configuration-supporting-only-text-output)
		- [Supporting both text and JSON output](#supporting-both-text-and-json-output)
		- [YAML file with two feature definitions](#yaml-file-with-two-feature-definitions)
- [Testing](#testing)
	- [Running CT test for show tech](#running-ct-test-for-show-tech)

## Overview
The show tech infrastructure is used to collect the summary of switch or feature specific information.  This infrastructure runs a collection of show commands and produces the output in text format.  The collection of show commands per feature are present in the show tech configuration file, and accordingly show tech uses those commands for the given feature.  The output of the show tech command is useful to analyze the system/feature behavior.

## Support for JSON output
Currently the show tech infrastructure is designed to produce output in plain text format. Because parsing and gathering information from the text data is difficult, show tech output is provided in JSON format in addition to the text format. In order to achieve this functionality, the show tech infrastructure directly reads the specified tables and columns from the OVSDB server and produces JSON output. In the future, tools will be developed to parse the JSON output and provide inferences.

## How to add new features in show tech
The show tech infrastructure uses the show tech configuration (YAML) file to understand the list of supported features, as well as the corresponding CLI commands used for each of those features.

The configuration YAML file is placed in the ops-supportability repo under the path `ops-supportability/conf/ops_showtech.yaml`.

Following is the structure of the file:

```
- feature:
   feature_desc:
   feature_name:
   cli_cmds:
	   - "command1"
	   - "command2"
	   - ...
   ovsdb:
	   table:
		   table_name:
		   col_names:
			  - "column1"
			  - "column2"
			  - ....
```

### Sample YAML files
#### Simple configuration supporting only text output

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

#### Supporting both text and JSON output
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

For example, to add support for the lldp feature, add the corresponding feature name, feature description, CLI commands, and OVSDB table details to the configuration file as shown below.


#### YAML file with two feature definitions

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
Once the configuration file is modified, test the following three CLI commands and verify the output.

| Command | Expectation|
|:--------|:----------|
| **show tech** | Runs show tech for all supported features.  Ensure that your newly added feature commands run successfully as part of the show tech output. |
| **show tech list**| Lists all the supported show tech features. Ensure that it lists your newly added feature name and description. |
| **show tech FEATURE**| Runs show tech for the newly added feature and verifies the output. |


*Note that the show tech output in JSON format is currently not supported. It is recommended that the corresponding OVSDB configuration is added to the YAML file for future reference.*


### Running CT test for show tech
Run the following CT test to verify that the show tech infrastructure is properly working with the configuration changes.

`make devenv_ct_test src/ops-supportability/test/show-tech_test.py`
