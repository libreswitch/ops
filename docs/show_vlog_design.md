# Design Document of VLOG Infrastructure Configuration

VLOG is used as the logging infra in most of the ops daemons.  Hence we design vtysh commands in order to display and configure the vlog settings for various features.


## Contents
- [Responsibilities](#responsibilities)
- [Design](#design)
- [Limitations](#limitations)
- [Block Diagram](#block-diagram)
- [Vlog Configuration Yaml File](#vlog-configuration-yaml-file)
- [Data Structures](#Data-structures)
- [References](#references)

## Responsibilities
Vlog commands will enable the user to configure vlog settings (syslog and file settings) for various daemons.  It provides the following cli commands for this purpose.

```show vlog config feature/daemon <NAME>```

List the current Configuration of various features

```config> vlog feature/daemon <NAME> [syslog | file] [emer |err |warn | info |dbg]```

Configure vlog of the daemons corresponding to the given feature.

## Design
### show vlog config design

When the user gives show vlog config for a feature, all the daemons corresponding to that feature will be queried for the current configuration of vlog (syslog and file settings) using unixctl command vlog/list.  The information returned by the daemon will be displayed on the console.

### vlog configuration design

When the user sets the vlog configuration (syslog and file - severity level), we send ''' vlog/set any ''' unixctl command to all the daemons corresponding to that feature.

## Limitations

1. ### Configuration of One Feature might affect another related Feature
Vlog configuration and show command works at feature level.  A Feature could be implemented by a single daemon or a group of daemons, it is also possible that a single daemon implements multiple feature.  In this case when we set the vlog configuration for a feature it would affect all the daemons corresponding to it which might after features which are also implemented by those daemons.
For eg., ops-mgmt daemon implements multiple management features.  When vlog configuration for one of those features is changed, the corresponding configuration for all the features implemented by ops-mgmt would be affected.

2. ### All modules in the daemon would be set to same configuration
with this vlog command we could control the vlog configuration only at the daemon level, ie., the changes are applied to all the modules, controlling individual modules of a daemon is not possible.  As per this design, when the show vlog is running, it would fetch only the configuration of the first module and display it as the configuration of the feature/daemon.

## Unixctl Command

By using unixctl command `vlog/list`will get the vlog Configuration of the modules corresponding to the daemon.  Since all the modules for the daemon will have the same configuration, it is sufficient to get only the first modules setttings.

## Block Diagram

```ditaa
  +---------------+                   +-----------------------+
  |               |                   |                       |
  | Config Parser |  ---------------> |                       |
  |               |                   |(vtysh unixctl client) |
  +---------------+                   |                       |
          ^                           +-----------------------+
          |              unixctl_command_register | ^
          |                                       | |unixctl reply
          |                                       | |
          |                                       v |
  +-------+--------+                   +-----------------------+
  |     vlog       |                   |                       |
  | Configuration  |                   |      daemon           |
  | File ( YAML)   |                   |                       |
  +----------------+                   +-----------------------+
```

## Vlog Configuration Yaml File

The Yaml file is structured with the following elements
```
-
   feature_name: "feature1"
   feature_desc: "Description1"
   daemon:
     - "daemon1"
     - "daemon2"
     - "daemon3"
```
Sample Yaml File is shown below

```ditaa
---
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

## Data Structures

show vlog cli parses information from the configuration file(ops_featuremapping.yaml) and stores in to following data Structures.

```ditaa

struct daemon {
   char* name;
   struct daemon* next;
};

struct feature {
   char* name;
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
## References

* [Reference 1 ] `show_vlog_design.md`
* [Reference 2 ] `show_vlog_cli.md`
* [Reference 3 ] `show_vlog_test.md`
* [Reference 4 ] `show_vlog_user_guide.md`
* [Reference 5 ] `show_vlog_dev_guide.md`