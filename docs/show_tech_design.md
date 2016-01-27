# Show Tech Infrastructure

## Contents
- [High level design of show tech infra](#high-level-design-of-show-tech-infra)
    - [Responsibilities](#responsibilities)
    - [Design choices](#design-choices)
    - [Block Diagram](#block-diagram)
    - [OVSDB-Schema](#ovsdb-schema)
    - [Show Tech Configuration Yaml File](#show-tech-configuration-yaml-file)
    - [Internal structure](#internal-structure)
        - [Source modules](#source-modules)
        - [Data structures](#data-structures)
        - [Failure Handling](#failure-handling)

# High level design of show tech infrastructure
   Show Tech Infrastructure helps to execute multiple show commands grouped under various feature and produce the output of those commands.  This helps the support and development engineers to analysis the system behaviour.  This infrastructure is based on a description file in readable (yaml) format, containing mapping of feature names to the corresponding cli commands which provides the show tech information for that feature.  This allows the feature team to introduce new feature and cli commands per feature as new features are added or modified.

   In future the description file may also contain information of the tables in the OVSDB which contains show tech related informations.  This information allows development of tools to extract and perform analysis of show tech data.

## Responsibilities
The Show tech Infrastructure is responsible to execute multiple show commands grouped under different features and thus provide the overview of system or feature behaviour. This Infra consist of show tech configuration parser and cli component. Show Tech configuration parser is built as a library component, hence it could be imported by various daemon to get access to the show tech infra.

## Design choices
show tech infra could have been merged with the ops-cli. However, keeping these separate will help us to export the show tech infra as a module to other daemons and python scrips to perform more show tech analysis.


## Block Diagram
```ditaa
+-------------------+  Imports as     +-----------------------+
|                   |  library        |        ops-cli        |
|  Show Tech Infra  +---------------> |     (vtysh Daemon)    |
|     (Library)     |                 |                       |
|                   |                 |                       |
| +---------------+ |                 |    cli_showtech       |
| | Config Parser | |                 |          +            |
| +---------------+ |                 |          |            |
+-------------------+                 |          v            |
          ^                           |    show commands      |
          |                           |                       |
          |                           |                       |
          |                           +-----------------------+
          |
          |
  +-------+--------+
  | Show Tech      |
  | Configuration  |
  | File ( YAML)   |
  +----------------+

```

## OVSDB-Schema
ovsdb schema is not used for this feature.


##  Show Tech Configuration Yaml File

List of Show Tech Features and the corresponding commands to be executed under various features are specified in /etc/openswitch/supportability/ops_showtech.yaml configuration file.

The Yaml file is structured with the following elements

- feature
  * feature_name
  * feature_desc
  * cli_cmds
   * "command1"
   * "command2"
   * ...

Sample Yaml File with Two Feature Definition is shown below

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


## Internal structure


### Source modules
```ditaa
  showtech.c
  showtech.h
```

### Data structures

Show tech Configuration Information from the configuration file (ops_showtech.yaml) is parsed and stored in linked list datastructure.
We mainly perform two operation on this datastructure.

1. Addition of New element O(1)
2. Search for a Element O(N)

We also have to preserve the order of the elements as they are defined in yaml configuration file.  Hence we are using simple linked list.

```ditaa
 struct clicmds
 {
  char* command;
  struct clicmds* next;
};

struct ovscolm
{
  char* name;
  struct ovscolm* next;
};

struct ovstable
{
  char* tablename;
  struct ovscolm* p_colmname;
  struct ovstable* next;
};

struct feature
{
  char* name;
  char* desc;
  struct clicmds* p_clicmds;
  struct ovstable* p_ovstable;
  struct feature* next;
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
          |                             +---------------------+
          |                             | +---------------------+
          +-----------------------------> | +---------------------+
                                        +-+ |  CliCommands(1..N)  |
                                          +-+                     |
                                            +---------------------+

```

### Failure Handling

Show Tech Infra has external dependencies on the description (yaml) file and feature specific cli commands.  We could have the following failures due to external dependencies, handling of these failures as designed as below



|Failure |Handling|
|:-------|:-------|
|Description File missing or corrupted | 1) Parser flags error
|| 2) allocated datastructures are destroyed
|| 3) Error Logged in Logging Infra
|| 4) Error Displayed on CLI|
|Feature specific CLI Commands Hangs | Each CLI command will be executed with a timeout. On timeout
|| 1) Error Logged in Logging Infra
|| 2) Skip this CLI and move to the next CLI command execution.
|| 3) Error Displayed on summary|
