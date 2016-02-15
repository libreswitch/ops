# High-Level Design of Diagnostic Dump
The primary goal of the diagnostic module is to capture internal diagnostic information about features from related daemons.

## Contents

- [Responsibilities](#responsibilities)
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [OVSDB-schema](#ovsdb-schema)
- [Diagnostic dump configuration YAML file](#diagnostic-dump-configuration-yaml-file)
- [Internal structure](#internal-structure)
	- [Source modules](#source-modules)
	- [Data structures](#data-structures)
- [C API detail](#c-api-detail)
- [Python API detail](#python-api-detail)
- [References](#references)


## Responsibilities

The diagnostic infrastructure is responsible for capturing information from one or more daemons for a feature.

## Design choices
- One feature can be mapped with multiple daemons, and one daemon can be mapped with multiple features.
- The user can change the mapping of a feature to a daemon at runtime.
- Basic diagnostics are dumped to a console or to a file by using the CLI.
- The CLI cannot be blocked for more than 30 seconds. If the daemon does not reply to vtysh, then the timer handler in vtysh releases vtysh for the next command.
- The diagnostic dump command creates the dump file at `/tmp/ops-diag/<file name>`.

## Participating modules

``` ditaa
  +---------------+                   +-----------------------+
  |               |                   |                       |
  | Config Parser |  ---------------> |        diag-dump      |
  |               |                   |(vtysh unixctl client) |
  +---------------+                   |                       |
          ^                           +-----------------------+
          |                                       | ^
          |                                unixctl| |unixctl reply
          |                     diag-dump request | |
          |                                       v |
  +-------+--------+                   +-----------------------+
  | Diag dump      |                   |                       |
  | Configuration  |                   |    daemon             |
  | File (YAML)    |                   |                       |
  +----------------+                   +-----------------------+


```


## OVSDB-schema
The OVSDB-schema is not used for this feature.

## Diagnostic dump configuration YAML file
Diag-dump uses a feature to a daemon mapping file whose absolute path is the following: `/etc/openswitch/supportability/ops_diagdump.yaml`

This YAML file is structured with the following elements:


  -
    feature_name: "feature1"
    feature_desc: "Description1"
    daemon:
      - "daemon1"
      - "daemon2"
      - "daemon3"

  -
    feature_name: "feature2"
    feature_desc: "Description2"
    daemon:
      - "daemon4"
      - "daemon5"
      - "daemon6"



A sample YAML file with two features defined:
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
      - "ops-lacpd"

```


## Internal structure


### Source modules
```ditaa
    diag_dump_vty.c
    diag_dump_vty.h
```

### Data structures

The diagnostic dump CLI parses information from the configuration file (`ops_diagdump.yaml`) and stores it in the following data structures.

```ditaa


struct daemon {
   char* name;
   struct daemon* next;
};

struct feature {
   char* name;
   char* desc;
   struct daemon*   p_daemon;
   struct feature*   next;
};



+------------------+
| +------------------+
| | +------------------+
+-+ |  Features(1..N)  |
  +-+     +            |
    +------------------+
          |
          |
          |
          |      +---------------------+
          |      | +---------------------+
          +----> | | +---------------------+
                 +-+ |  Daemons(0..N)      |
                   +-+                     |
                     +--------+------------+


```
## C API description
The daemon initialization function is required to register the diagnostic dump basic handler function.
The "INIT_DIAG_DUMP_BASIC" macro takes a function name as an argument, and this function is the callback handler for the basic diag-dump.

### API description

This macro registers its argument callback handler.
The callback function arguments are a double pointer to the buffer and a character pointer to the feature name.
The callback handler dynamically allocates memory as per requirement and populates required data in the buffer.
This macro checks and sends data inside the buffer as a reply to vtysh and free dynamically allocated memory.

```ditaa
Syntax:
INIT_DIAG_DUMP_BASIC(cb_func_name)
static void cb_func_name (const char *feature , char **buf)
```

In summary, complete these steps:
1. Define the callback function for the basic diagnostic information collection. This callback function should perform the following activities:
    a. Allocate the character buffer to hold the diagnostics information.
    b. Copy the diagnostics information(text format) into this buffer.
    c. Null terminate the buffer.
2. Initialize the basic diagnostic framework in the daemon init routine.
Note: The diagnostic framework is responsible to free the allocated buffer once used.


### Sample code
#### BBscript
Add dependency "DEPENDS = ops-supportability" in the BBScript of the respective daemon.
#### Header file
include diag_dump.h in .c file.
```ditaa
#include  <diag_dump.h>
```
#### Init function
Inside the initialization function invoke this macro with the handler function.
INIT_DIAG_DUMP_BASIC(cb_func_name);

#### Handler function definition

```ditaa
static void cb_func_name(const char *feature , char **buf)
{
    if (!buf)
        return;
    *buf =  xcalloc(1,BUF_LEN);
    if (*buf) {
        /* populate data in buffer */
        lldpd_dump(*buf,BUF_LEN);
        VLOG_DBG("basic diag-dump data populated for feature %s",feature);
    } else{
        VLOG_ERR("Memory allocation failed for feature %s",feature);
    }
    return ;
}

```
#### Example for lldpd daemon

```ditaa
yocto/openswitch/meta-distro-openswitch/recipes-ops/l2/ops-lldpd.bb
DEPENDS = "ops-utils ops-config-yaml ops-ovsdb libevent openssl ops-supportability"



src/ops-lldpd/src/daemon/lldpd_ovsdb_if.c

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
        VLOG_DBG("basic diag-dump data populated for feature %s",feature);
    } else{
        VLOG_ERR("Memory allocation failed for feature %s",feature);
    }
    return ;
}


```

## Python API description
The daemon initialization function is required to register the handler for a basic diagnostics dump by calling `init_diag_dump_basic()`.
The function `init_diag_dump_basic()` takes the diagnostic dump handler function name as an argument.

### Python API description

This function registers its argument as a callback handler. The callback handler
function contains the feature name in the argument `argv`. The callback handler collects all the diagnostic information and copies it to a buffer and returns the buffer.


```ditaa
Syntax:
ops_diagdump.init_diag_dump_basic(cb_func_name)
cb_func_name (argv)
```

In summary, complete these steps:
1. Define a callback function for collecting basic diagnostic information. The callback function must perform the following activities:
	 a. Copy the diagnostics information (text format) into the buffer.
	 b. Return the buffer.
2. Initialize the basic diagnostic framework in the daemon init routine.

### Sample code
#### BBScript
Add dependency "DEPENDS = ops-supportability" in the BBScript of the respective daemon.

#### Import Python module
import ops_diag_dump in Python file.
```ditaa
import ops_diagdump
```

#### Init function
Inside the initialization function invoke this function with the handler function.
init_diag_dump_basic(cb_func_name)

```ditaa
ops_diagdump.init_diag_dump_basic(diag_basic_handler)
```

#### Handler function definition

```ditaa

def diag_basic_handler( argv ):
    # argv[0] is set to the string "basic"
    # argv[1] is set to the feature name, e.g. lldp
    feature = argv.pop()
    buff = 'Diagnostic dump response for feature ' + feature + '.\n'
    buff = buff + 'diag-dump feature for AAA is not implemented'
    return buff

```

#### Example for the AAA daemon

```ditaa

BB Script: yocto/openswitch/meta-distro-openswitch/recipes-ops/utils/ops-aaa-utils.bb
DEPENDS = "ops-ovsdb ops-supportability"

file: src/ops-aaa-utils/ops_aaautilspamcfg.py

...
import ops_diagdump
...

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


## References

* [Diagnostic Dump Commands](http://www.openswitch.net/documents/user/diagnostic_cli)
* [Component Test Cases for Diagnostic](http://www.openswitch.net/documents/user/diagnostic_test)
* [Diagnostic Dump User Guide ](http://www.openswitch.net/documents/user/diagnostic_user_guide)
* [Developer Guide for Diagnostic Dump](http://www.openswitch.net/documents/dev/ops-diag/diagnostic_dev_guide)
