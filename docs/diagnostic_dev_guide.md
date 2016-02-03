#Developer Guide for Diagnostic Dump

## Contents

- [Overview](#overview)
- [How to define the mapping between this feature and the daemon which implements this feature](#how-to-define-the-mapping-between-this-feature-and-the-daemon-which-implements-this-feature))
	- [Sample code](#sample-code)
		- [BB script](#bb-script)
		- [Header file](#header-file)
		- [Init function](#init-function)
		- [Example of a callback function definition](#example-of-a-callback-function-definition)
		- [Example for lldpd daemon](#example-for-lldpd-daemon)
- [YAML configuration](#yaml-configuration)
- [Testing](#testing)
	- [diag-dump  list](#diag-dump-list)
	- [diag-dump  <feature> basic](#diag-dump-feature-basic)
	- [diag-dump  <feature> basic  <file name>](#diag-dump-feature-basic-file-name)
		- [CT script](#ct-script)
- [References](#references)

## Overview
Diagnostic module captures internal diagnostic information about the requested features from the respective daemons.

## How to define the mapping between this feature and the daemon which implements this feature
Define a callback function which will collect the necessary diagnostics information from the daemon for the given feature.  This callback function needs to allocate sufficient memory(buf) to hold the diagnostics information.  This memory will be later deallocated by the diagnostic framework.

The syntax of the callback function should be as below

```
static void cb_func_name (const char *feature , char **buf)
```

Initialize the Basic Diagnostic Framework in the Daemon init routine by calling INIT_DIAG_DUMP_BASIC passing the callback function name.

Example:
```
INIT_DIAG_DUMP_BASIC(basic_diag_handler_cb)
```

In summary the following steps needs to be followed

 1. Define Callback Function for Basic Diagnostic Information Collection
 2. This Callback function should perform the following activities
	 1. Allocate Character Buffer to hold Diagnostics Information.
	 2. Copies the Diagnostics Information(text format) into this buffer
	 3. Null Terminate the Buffer
 3. Initialize the Basic Diagnostic Framework in the daemon init routine.

*Please note that the Diagnostics Framework is responsible to free the allocated buffer once used*


### Sample code
#### BB script
Add dependancy ```"DEPENDS = ops-supportability" in bbscript of respective daemon.```

#### Header file
include diag_dump.h in .c file.
```ditaa
#include  <diag_dump.h>
```
#### Init function
Inside daemon init routine invoke this macro with callback function.
eg., ```INIT_DIAG_DUMP_BASIC(lldpd_diag_dump_basic_cb);```

#### Example of a callback function definition

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
#### Example for lldpd daemon

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


## YAML configuration
Add a new enty for daemon on switch or add this entry in ops-supportability repo.
/etc/openswitch/supportability/ops_diagdump.yaml
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

## Testing
### diag-dump  list
This command displays list of features supported by the diag-dump CLI.
### diag-dump  <feature> basic
This command displays basic diagnostic information of the feature. Check supported features by command "diag-dump list".
### diag-dump  <feature> basic  <file name>
This command captures diagnostic information to given file .


#### CT script
Please run the following ct test to verify diag-dump working fine with your configuration changes.
make devenv_ct_test src/ops-supportability/test/diag_dump_test.py


## References

* [Reference 1] 'diagnostic_dev_guide.md'
* [Reference 2] 'diagnostic_design.md'
* [Reference 3] 'diagnostic_cli.md'
* [Reference 4] 'diagnostic_test.md'
* [Reference 5] 'diagnostic_user_guide.md'
