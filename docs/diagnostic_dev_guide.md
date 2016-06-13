# Diagnostic Dump Developer Guide

## Contents



- [Overview](#overview)
- [Mapping a feature to its daemons](#mapping-a-feature-to-its-daemons)
	- [Configuration file](#configuration-file)
- [Diagnostics dump C API](#diagnostics-dump-c-api)
	- [Header file](#header-file)
- [Diagnostics dump Python API](#diagnostics-dump-python-api)
	- [BBScript changes](#bbscript-changes)
	- [Import Python module](#import-python-module)
	- [Daemon init function](#daemon-init-function)
	- [Example of a callback function definition](#example-of-a-callback-function-definition)
	- [Example for AAA daemon](#example-for-aaa-daemon)
- [Testing](#testing)
	- [diag-dump list](#diag-dump-list)
	- [diag-dump for a feature (basic) on CLI session](#diag-dump-for-a-feature-basic-on-cli-session)
	- [diag-dump for a feature (basic) to a file](#diag-dump-for-a-feature-basic-to-a-file)
		- [CT script](#ct-script)
- [Frequently asked question](#frequently-asked-question)
- [References](#references)



## Overview
The diagnostic dump CLI command captures internal diagnostic information about features from their associated  daemons. Internally, it uses the unixctl mechanism to communicate with the daemons.

## Mapping a feature to its daemons

### Configuration file
Feature owners are required to map each feature to the daemons that implement the feature. This enables the  diagnostic dump module to determine the daemon with which to communicate when retrieving dumps. Mappings must be defined in the configuration file, which is: **ops-supportability/conf/ops_featuremapping.yaml**.


The file has the following structure (defined using YAML):
```ditaa
  -
    feature_name: "feature1"
    feature_desc: "Description1"
    daemon:
      - [name: "daemon1", 'diag_dump': "y"]
      - [name: "daemon2", 'diag_dump': "n"]
      - [name: "daemon3", 'diag_dump': "y"]
  -
    feature_name: "feature2"
    feature_desc: "Description2"
    daemon:
      - [name: "daemon4", 'diag_dump': "y"]
      - [name: "daemon5", 'diag_dump': "y"]
      - [name: "daemon6", 'diag_dump': "y"]

```


A sample file with two features defined would look like this:
```ditaa
  -
    feature_name: "lldp"
    feature_desc: "Link Layer Discovery Protocol"
    daemon:
      - [name: "ops-lldpd", 'diag_dump': "y"]

  -
    feature_name: "lacp"
    feature_desc: "Link Aggregation Control Protocol"
    daemon:
      - [name: "ops-lacpd", 'diag_dump': "y"]

```

## Diagnostics dump C API
Define a callback function that collects the necessary diagnostics information from the daemon for the given feature. This callback function needs to allocate sufficient memory (buf) to hold the diagnostics information. This memory is later deallocated by the diagnostic framework.

Syntax of the callback function:

```
static void cb_func_name(const char *feature, char **buf)
```

Initialize the basic diagnostic framework in the daemon init routine by calling **INIT_DIAG_DUMP_BASIC** and passing the callback function name. For example:

```
INIT_DIAG_DUMP_BASIC(basic_diag_handler_cb)
```

In summary, complete these steps:
1. Define the callback function for basic diagnostic information collection. The  function should perform the following:
    - Allocate a character buffer to hold the diagnostics information.
    - Copy diagnostics information(text format) into the buffer.
    - Null-terminate the buffer.
2. Initialize the basic diagnostic framework in the daemon init routine.
3. Enable diag-dump attribute for daemon in feature mapping yaml file.

**Note:** The diagnostic framework must free the buffer once it has been used.

#### BBscript
Add the dependency **DEPENDS = ops-supportability** to the BBScript for the associated daemon.

### Header file
Include diag_dump.h in the .c file.

```ditaa
#include  <diag_dump.h>
```
### Daemon init function
The daemon initialization routine should invoke this macro with the callback function. For example:
```
INIT_DIAG_DUMP_BASIC(lldpd_diag_dump_basic_cb)
```

### Example of a callback function definition

```ditaa
static void lldpd_diag_dump_basic_cb(const char *feature , char **buf)
{
    if (!buf)
        return;
    *buf =  xcalloc(1, BUF_LEN);
    if (*buf) {
        /* populate data in buffer */
        lldpd_dump(*buf, BUF_LEN);
        VLOG_INFO("basic diag-dump data populated for feature %s",feature);
    } else{
        VLOG_INFO("Memory allocation failed for feature %s",feature);
    }
    return ;
}

```

### Example of enabling diag-dump  attribute
Enable diag-dump attribute in the file ops_featuremapping.yaml.
```ditaa
  -
    feature_name: "lldp"
    feature_desc: "Link Layer Discovery Protocol"
    daemon:
        - [name: "ops-lldpd", 'diag_dump': "y"]
```

### Example for lldpd daemon

```ditaa
BB Script: yocto/openswitch/meta-distro-openswitch/recipes-ops/l2/ops-lldpd.bb
DEPENDS = "ops-utils ops-config-yaml ops-ovsdb libevent openssl ops-supportability"

file: src/ops-lldpd/src/daemon/lldpd_ovsdb_if.c

#include  <diag_dump.h>

ovsdb_init(){
...
INIT_DIAG_DUMP_BASIC(lldpd_diag_dump_basic_cb);
...
}

/*
 * Function       : lldpd_diag_dump_basic_cb
 * Responsibility : callback handler function for diagnostic dump basic
 *                  it allocates memory as per requirement and populates data.
 *                  INIT_DIAG_DUMP_BASIC will free allocated memory.
 * Parameters     : feature name string,buffer pointer
 * Returns        : void
 */

/* Determin buffer length for diag-dump and allocate required memory */
#define  BUF_LEN  300

static void lldpd_diag_dump_basic_cb(const char *feature , char **buf)
{
    if (!buf)
        return;
    *buf =  xcalloc(1,BUF_LEN);
    if (*buf) {
        /* populate basic diagnostic data to buffer  */
        lldpd_dump(*buf,BUF_LEN);
        VLOG_INFO("basic diag-dump data populated for feature %s",feature);
    } else{
        VLOG_INFO("Memory allocation failed for feature %s",feature);
    }
    return ;
}


file: ops_featuremapping.yaml
  -
    feature_name: "lldp"
    feature_desc: "Link Layer Discovery Protocol"
    daemon:
        - [name: "ops-lldpd", 'diag_dump': "y"]

```

## Diagnostics dump Python API
Define a callback function that collects the necessary diagnostics information from the daemon for the given feature. This callback function needs to fill a buffer to hold the diagnostic information. The callback function should return this buffer.

Syntax of the callback function:

```ditaa
cb_func_name(argv)
```

Initialize the basic diagnostic framework in the daemon init routine by calling **init_diag_dump_basic** and passing the callback function name. For example:

```ditaa
ops_diagdump.init_diag_dump_basic(basic_diag_handler_cb)
```

In summary, completed these steps:
1. Add the dependency **ops-supportability** in the BBScript.
2. Import Python module **ops_diagdump**.
3. Define a callback function for collecting basic diagnostic information. The callback function should perform the following activities:
	 - Copy the diagnostics information (text format) into the buffer.
	 - Return the buffer.
5. Initialize the basic diagnostic framework in the daemon init routine.


### BBScript changes
Add a dependency in bbscript for the respective daemon.
```ditaa
DEPENDS = "ops-supportability"
```

### Import Python module
import ops_diag_dump in Python file.

```ditaa
import ops_diagdump
```
### Daemon init function
The daemon initialization routine should invoke this macro with the callback function. For example:
```ditaa
ops_diagdump.init_diag_dump_basic(diag_basic_handler)
```



### Example of a callback function definition

```ditaa
def diag_basic_handler( argv ):
    # argv[0] is basic
    # argv[1] is feature name
    feature = argv.pop()
    buff = 'Diagnostic dump response for feature ' + feature + '.\n'
    buff = buff + 'diag-dump feature for AAA is not implemented'
    return buff
```
### Example for AAA daemon

```ditaa
BB Script: yocto/openswitch/meta-distro-openswitch/recipes-ops/utils/ops-aaa-utils.bb
DEPENDS = "ops-ovsdb ops-supportability"

file: src/ops-aaa-utils/ops_aaautilspamcfg.py

import ops_diagdump
.....

def diag_basic_handler( argv ):
    # argv[0] is basic
    # argv[1] is feature name
    feature = argv.pop()
    buff = 'Diagnostic dump response for feature ' + feature + '.\n'
    buff = buff + 'diag-dump feature for AAA is not implemented'
    return buff

...
ops_diagdump.init_diag_dump_basic(diag_basic_handler)
...
```

## Testing
### diag-dump list
The **diag-dump list** command displays the list of features supported by the diag-dump CLI.
### diag-dump for a feature (basic) on CLI session
The **diag-dump <feature> basic** command displays basic diagnostic information of the specified feature.
### diag-dump for a feature (basic) to a file
The **diag-dump <feature> basic <filename>** command captures diagnostic information to the specified file.
#### CT script
Run the following CT test to verify that the diag-dump command is properly working with the configuration changes:
`make devenv_ct_test src/ops-supportability/test/diag_dump_test.py`

## Frequently asked question
1) How to handle requests for different features implemented by the same daemon ?
   diag-dump api passes feature name in callback function argument as char* . Use this
   argument to understand the requested feature and populate feature related information .

2) What is size of diag-dump buffer ?
   Developer will decide the diag-dump buffer length.

## References

* [High-Level Design of Diagnostic Dump](http://www.openswitch.net/documents/dev/ops-diag/diagnostic_design)
* [Diagnostic Dump Commands](http://www.openswitch.net/documents/user/diagnostic_cli)
* [Component Test Cases for Diagnostic](http://www.openswitch.net/documents/user/diagnostic_test)
* [Diagnostic Dump User Guide ](http://www.openswitch.net/documents/user/diagnostic_user_guide)
