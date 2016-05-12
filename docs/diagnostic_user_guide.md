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
The diagnostic dump command lets you display or save diagnostic information about an OpenSwitch feature.

### Listing features that support diagnostic dump
Run following command to see all features that support diagnostic information:
```diag-dump list```

##### Example
```
switch# diag-dump list
Diagnostic Dump Supported Features List
-------------------------------------------------------------------------
Feature                                  Description
-------------------------------------------------------------------------
lldp                                     Link Layer Discovery
lacp                                     Link Aggregation Con
fand                                     System Fan
routing                                  Routing protocols
ospfv2                                   Open Shortest Path F
bgp                                      Border Gateway Proto
sub-interface                            sub-interface
loopback                                 Loopback interface
```

### Viewing basic diagnostic information for a feature
Run the command:
```diag-dump <feature-name> basic```

##### Example
```
switch# diag-dump lldp basic
=========================================================================
[Start] Feature lldp Time : Thu Apr 14 02:54:18 2016

=========================================================================
-------------------------------------------------------------------------
[Start] Daemon ops-lldpd
-------------------------------------------------------------------------

LLDP : DISABLED

    intf name   |   OVSDB interface     |   LLDPD Interface     |    LLDP Status        |  Link State
==============================================================================================
bridge_normal   |    Yes                |    Yes                |    rxtx               |    down
51-3            |    Yes                |No             |
53              |    Yes                |No             |
49-4            |    Yes                |No             |
51-1            |    Yes                |No             |
35              |    Yes                |No             |
6               |    Yes                |No             |
39              |    Yes                |No             |
4               |    Yes                |No             |
50-1            |    Yes                |No             |
53-3            |    Yes                |No             |
25              |    Yes                |No             |
50-4            |    Yes                |No             |
40              |    Yes                |No             |
51-4            |    Yes                |No             |
37              |    Yes                |No             |
48              |    Yes                |No             |
49              |    Yes                |No             |
50-2            |    Yes                |No             |
52              |    Yes                |No             |
11              |    Yes                |No             |
22              |    Yes                |No             |
5               |    Yes                |No             |
36              |    Yes                |No             |
34              |    Yes                |No             |
49-2            |    Yes                |No             |
54-3            |    Yes                |No             |
17              |    Yes                |No             |
20              |    Yes                |No             |
46              |    Yes                |No             |
9               |    Yes                |No             |
42              |    Yes                |No             |
49-3            |    Yes                |No             |
23              |    Yes                |No             |
47              |    Yes                |No             |
12              |    Yes                |No             |
30              |    Yes                |No             |
24              |    Yes                |No             |
27              |    Yes                |No             |
50              |    Yes                |No             |
13              |    Yes                |No             |
33              |    Yes                |No             |
51              |    Yes                |No             |
49-1            |    Yes                |No             |
43              |    Yes                |No             |
28              |    Yes                |No             |
45              |    Yes                |No             |
50-3            |    Yes                |No             |
16              |    Yes                |No             |
8               |    Yes                |No             |
3               |    Yes                |No             |
15              |    Yes                |No             |
51-2            |    Yes                |No             |
53-1            |    Yes                |No             |
29              |    Yes                |No             |
26              |    Yes                |No             |
18              |    Yes                |No             |
52-1            |    Yes                |No             |
53-4            |    Yes                |No             |
14              |    Yes                |No             |

-------------------------------------------------------------------------
[End] Daemon ops-lldpd
-------------------------------------------------------------------------
=========================================================================
[End] Feature lldp
=========================================================================
Diagnostic dump captured for feature lldp


```
### Saving basic diagnostic information to a file
Run the command:
```diag-dump <feature-name> basic <filename>```


### Troubleshooting

#### Condition
The **diag-dump** command displays the message: **Failed to capture diagnostic information**


#### Causes
1. The configuration file (**/etc/openswitch/supportability/ops_featuremapping.yaml**) is missing.
2. You may not have read permission for the configuration file.
3. The content of the configuration file is incorrect.


#### Remedy
1. Ensure that the configuration file (**/etc/openswitch/supportability/ops_featuremapping.yaml**) exists.
2. Ensure that the you have read permission for the configuration file.
3. Verify that the content of the configuration file is correct using the yaml lint tool.
4. Verify that the structure of the configuration file is valid.

## References

* [High-Level Design of Diagnostic Dump](http://www.openswitch.net/documents/dev/ops-diag/diagnostic_design)
* [Diagnostic Dump Commands](http://www.openswitch.net/documents/user/diagnostic_cli)
* [Component Test Cases for Diagnostic](http://www.openswitch.net/documents/user/diagnostic_test)
