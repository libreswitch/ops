# Diagnostic Dump Design

## Contents

- [High level design of diagnostic dump](#high-level-design-of-diagnostic-dump)
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [OVSDB-schema](#ovsdb-schema)
- [Configuration file](#configuration-file)
- [Internal structure](#internal-structure)
	- [Source modules](#source-modules)
	- [Data structures](#data-structures)
- [C API description](#c-api-description)
	- [API description](#api-description)
		- [Syntax](#syntax)
	- [Sample code](#sample-code)
		- [BBscript](#bbscript)
		- [Header file](#header-file)
- [Python API description](#python-api-description)
	- [Python API description](#python-api-description)
		- [Syntax](#syntax)
	- [Sample code](#sample-code)
		- [BBScript](#bbscript)
		- [Import Python module](#import-python-module)
		- [Init function](#init-function)
		- [Handler function definition](#handler-function-definition)
		- [Example for the AAA daemon](#example-for-the-aaa-daemon)
- [References](#references)


## High level design of diagnostic dump

The primary goal of the diagnostic dump module is to capture internal diagnostic information about features from their related daemons.

## Design choices
- The relationship between features and daemons is many-to-many. A feature may have multiple daemons, and a daemon may be used by several different features.
- Users can change the mapping of a feature to a daemon at runtime.
- Basic diagnostics are dumped to the console or to a file  using the CLI.
- The CLI cannot be blocked for more than 30 seconds. If the daemon does not reply to vtysh, then the timer handler in vtysh releases vtysh for the next command.
- The diagnostic dump command creates a dump file at `/tmp/ops-diag/<file name>`.

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

## Configuration file
Diagnostic dump uses a configuration file to associate features and daemons. The file is located here: **/etc/openswitch/supportability/ops_featuremapping.yaml**

The configuration file has the following structure (defined using YAML):
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


A sample configuration file with two features defined would look like this:
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


## Internal structure


### Source modules
```ditaa
diag_dump_vty.c
diag_dump_vty.h
```

### Data structures

The diagnostic dump CLI command parses information from the configuration file (ops_featuremapping.yaml) and stores it in the following data structures:

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
The daemon initialization function is required to register the diagnostic dump basic handler function. The **INIT_DIAG_DUMP_BASIC** macro takes a function name as an argument, and this function is the callback handler for the basic diag-dump.

### API description

This macro registers its argument callback handler. The callback function arguments are a double pointer to the buffer and a character pointer to the feature name. The callback handler dynamically allocates memory as required and populates the buffer with data as needed. This macro checks and sends data inside the buffer as a reply to vtysh and frees dynamically allocated memory.

####Syntax
The callback function has the following syntax:

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
    - Copy diagnostics information (text format) into the buffer.
    - Null-terminate the buffer.
2. Initialize the basic diagnostic framework in the daemon init routine.

**Note:** The diagnostic framework must free the buffer once it has been used.


### Sample code
#### BBscript
Add the dependency **DEPENDS = ops-supportability** to the BBScript of the associated daemon.

#### Header file
Include **diag_dump.h** in the .c file.
```ditaa
#include  <diag_dump.h>
```
#### Init function
Inside the initialization function, invoke the following macro with the handler function:
```
INIT_DIAG_DUMP_BASIC(cb_func_name);
```
#### Handler function definition

```ditaa
#define  BUF_LEN  300
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
#### Example for the lldpd daemon

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
        VLOG_DBG("basic diag-dump data populated for feature %s",feature);
    } else{
        VLOG_ERR("Memory allocation failed for feature %s",feature);
    }
    return ;
}
```

## Python API description
The daemon initialization function is required to register the handler for a basic diagnostics dump by calling **init_diag_dump_basic()**. This function takes the diagnostic dump handler function name as an argument.

### Python API description

This function registers its argument as a callback handler. The callback handler function contains the feature name in the argument **argv**. The callback handler collects all the diagnostic information and copies it to a buffer and returns the buffer.

#### Syntax
```ditaa
ops_diagdump.init_diag_dump_basic(cb_func_name)
cb_func_name (argv)
```

In summary, complete these steps:
1. Define a callback function for collecting basic diagnostic information. The callback function must perform the following activities:
 - Copy diagnostics information (text format) into the buffer.
 - Return the buffer.
2. Initialize the basic diagnostic framework in the daemon init routine.

### Sample code
#### BBScript
Add the dependency **DEPENDS = ops-supportability** to the BBScript of the associated daemon.

#### Import Python module
Import ops_diag_dump in the Python file.
```ditaa
import ops_diagdump
```

#### Init function
Inside the initialization function, invoke the following function with the handler function:
```
init_diag_dump_basic(cb_func_name)
```
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
