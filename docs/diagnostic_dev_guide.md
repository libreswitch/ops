# Developer Guide for Diagnostic Dump

## Contents

- [Overview](#overview)
- [How to define the mapping between a feature and the daemon which implements that feature](#how-to-define-the-mapping-between-a-feature-and-the-daemon-which-implements-that-feature)
	- [YAML configuration](#yaml-configuration)
- [Diagnostics dump C API](#diagnostics-dump-c-api)
- [Diagnostics dump Python API](#diagnostics-dump-python-api)
- [Testing](#testing)
	- [diag-dump list](#diag-dump-list)
	- [diag-dump for a feature (basic) on CLI session](#diag-dump-for-a-feature-basic-on-cli-session)
	- [diag-dump for a feature (basic) to a file](#diag-dump-for-a-feature-basic-to-a-file)
		- [CT script](#ct-script)
- [References](#references)


## Overview
The Diagnostic CLI captures internal diagnostic information about the requested features from the respective daemons. Internally it uses the unixctl mechanism to communicate with the daemons.

## Defining the mapping between a feature and its daemons

### YAML configuration
Feature owners are required to define the mapping between the feature and the daemons that implement the feature, so that the diagnostic module can understand which daemons it has to communicate to. This mapping should be defined in the configuration file in the ops-supportability repo under the path `ops-supportability/conf/ops_diagdump.yaml`.

Example mappings:

```ditaa
  -
    feature_name: "lldp"
    feature_desc: "Link Layer Discovery Protocol"
    daemon:
      - "ops-lldpd"

  -
    feature_name: "lacp"
    feature_desc: "Link Aggregation Control Protocol"
    daemon:
      - "ops-lldpd"
      - "ops-fand"
      - "ops-lacp"

```

## Diagnostics dump C API
Define a callback function that collects the necessary diagnostics information from the daemon for the given feature. This callback function needs to allocate sufficient memory (buf) to hold the diagnostics information. This memory is later deallocated by the diagnostic framework.

Syntax of the callback function:

```
static void cb_func_name(const char *feature, char **buf)
```

Initialize the basic diagnostic framework in the daemon init routine by calling `INIT_DIAG_DUMP_BASIC` and passing the callback function name.

Example:
```
INIT_DIAG_DUMP_BASIC(basic_diag_handler_cb)
```

In summary, complete the following steps:

1. Define a callback function for collecting basic diagnostic information. The callback function should perform the following activities:
	 a. Allocate character buffer to hold the diagnostics information.
	 b. Copy the diagnostics information (text format) into the buffer.
	 c. Null terminate the buffer.
3. Initialize the basic diagnostic framework in the daemon init routine.

*Note: The diagnostics framework is responsible for freeing the allocated buffer once it is used.*


### BBScript changes
Add a dependency in BBScript for the respective daemon.
```
DEPENDS = "ops-supportability"
```

### Header file
Include diag_dump.h in the .c file.

```ditaa
#include  <diag_dump.h>
```
### Daemon init function
The daemon initialization routine should invoke this macro with the callback function.
For example:
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



```

## Diagnostics dump Python API
Define a callback function that collects the necessary diagnostics information from the daemon for the given feature. This callback function needs to fill a buffer to hold the diagnostic information. The callback function should return this buffer.

Syntax of the callback function:

```ditaa
cb_func_name(argv)
```

Initialize the basic diagnostic framework in the daemon init routine by calling `init_diag_dump_basic` and passing the callback function name.

Example:
```ditaa
ops_diagdump.init_diag_dump_basic(basic_diag_handler_cb)
```

In summary, completed these steps:
1. Add dependency "ops-supportability" in the BBScript.
2. Import Python module ops_diagdump.
3. Define a callback function for collecting basic diagnostic information. The callback function should perform the following activities:
	 a. Copy the diagnostics information (text format) into the buffer.
	 b. Return the buffer.
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
The `diag-dump list` command displays the list of features supported by the diag-dump CLI.
### diag-dump for a feature (basic) on CLI session
The `diag-dump <feature> basic` command displays basic diagnostic information of the specified feature.
### diag-dump for a feature (basic) to a file
The `diag-dump <feature> basic <file name>` command captures diagnostic information to the specified file.
#### CT script
Run the following CT test to verify that the diag-dump command is properly working with the configuration changes:
`make devenv_ct_test src/ops-supportability/test/diag_dump_test.py`

## References

* [High-Level Design of Diagnostic Dump](http://www.openswitch.net/documents/dev/ops-diag/diagnostic_design)
* [Diagnostic Dump Commands](http://www.openswitch.net/documents/user/diagnostic_cli)
* [Component Test Cases for Diagnostic](http://www.openswitch.net/documents/user/diagnostic_test)
* [Diagnostic Dump User Guide ](http://www.openswitch.net/documents/user/diagnostic_user_guide)
