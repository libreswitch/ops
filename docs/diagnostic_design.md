# High level design of Diagnostic Dump
Primary goal of diagnostic module is to capture internal diagnostic information about features from related daemons.


## Contents

- [High level design of Diagnostic Dump](#high-level-design-of-diagnostic-dump)
    - [Contents](#contents)
    - [Responsibilities](#responsibilities)
    - [Design choices](#design-choices)
    - [Participating modules](#participating-modules)
    - [OVSDB-schema](#ovsdb-schema)
    - [Diagnostic dump configuration yaml file](#diagnostic-dump-configuration-yaml-file)
    - [Internal structure](#internal-structure)
        - [Source modules](#source-modules)
        - [Data structures](#data-structures)
    - [API detail](#api-detail)
        - [API description](#api-description)
        - [Sample code](#sample-code)
            - [BB script](#bb-script)
            - [Header file](#header-file)
            - [Init function](#init-function)
            - [Handler function definition](#handler-function-definition)
            - [Example for lldpd daemon](#example-for-lldpd-daemon)
    - [References](#references)

##Responsibilities

Diagnostic infrastructure is responsible for capturing information from one or more daemon for a feature.

## Design choices
-One feature can be mapped with multiple daemon and one daemon can be mapped with multiple feature.
-User can change mapping of feature to daemon at runtime .
-Basic diagnostic is dumped to console or file using CLI .
-CLI can't be blocked for more than 30 sec . If daemon doesn't reply to vtysh then timer handler in vtysh will release vtysh for next command.

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
  | File ( YAML)   |                   |                       |
  +----------------+                   +-----------------------+


```


## OVSDB-schema
ovsdb schema is not used for this feature.


##  Diagnostic dump configuration yaml file
Diag-dump uses a feature to daemon mapping file whose absolute path is /etc/openswitch/supportability/ops_diagdump.yaml

This Yaml file is structured with the following elements


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



Sample Yaml File with Two Feature Definition is shown below
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

Diagnostic dump cli parses information from the configuration file (ops_diagdump.yaml) and stores in following data structures.

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
## API detail
Daemon initialisation function is required to register diagnostic dump basic handler function.
"INIT_DIAG_DUMP_BASIC" macro takes function name as argument and this function is callback handler for basic diag-dump.

###API description

This macro registers it argument callback handler .
Callback function arguments are double pointer to buffer and character pointer to feature name.
Callback handler dynamically allocates memory as per requirement and populates required data in buffer.
This macro checks and send data inside buffer as reply to vtysh and free dynamically allocated memory.

```ditaa
Syntax:
INIT_DIAG_DUMP_BASIC(cb_func_name)
static void cb_func_name (const char *feature , char **buf)
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
Add dependancy "DEPENDS = ops-supportability" in bbscript of respective daemon.
#### Header file
include diag_dump.h in .c file.
```ditaa
#include  <diag_dump.h>
```
#### Init function
Inside initialisation function invoke this macro with handler function.
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

## References

* [Reference 1] 'diagnostic_design.md'
* [Reference 2] 'diagnostic_cli.md' 167
* [Reference 3] 'diagnostic_test.md'    168
* [Reference 4] 'diagnostic_user_guide.md'
* [Reference 5] 'diagnostic_dev_guide.md'   165
