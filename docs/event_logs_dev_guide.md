# Event Log Infrastructure Developer Guide

## Contents

- [Overview](#overview)
- [How to define an event in a YAML file](#how-to-define-an-event-in-a-yaml-file)
- [Sample YAML file](#sample-yaml-file)
- [API usage](#api-usage)
	- [C API usage](#c-api-usage)
	- [Python API usage](#python-api-usage)
- [show events CLI](#show-events-cli)

## Overview
The event log framework is designed to facilitate generation and processing of high level events that are related to the functionality and components of the switch. For example, a port state change event, an LLDP neighbor discovered, or a management interface IP address updated.

Events can be generated from various sources in the system, such as protocol daemons, hardware daemons, the Linux system, system health monitoring daemons, and configuration daemons.

Events may be generated as a result of a state change in a daemon, hardware behavior, system health monitoring, or user initiated configuration changes.

Events are different from debug logs, which can be logged by using a logging API.
Unlike debug logs whose severity can be changed at run time to control which messages are logged, events cannot be filtered at the time of generation.

- An event has a unique ID. Other attributes are severity and timestamp, when the event is generated, and an optional list of key-value pairs.
- Events are stored in a format so that further processing, such as filtering or sorting, can be done efficiently.

To ensure the events are meaningful, events should be predefined by feature developers during the feature's development. Events should be categorized by specifying an event category to enable easier filtering of events. Information elements which are part of the event must be defined.

Generated events are stored in a file in the persistent storage area of a switch.

## How to define an event in a YAML file
The event log infrastructure makes use of a YAML file to define events and their corresponding categories.

The event YAML file is placed in the ops-supportability repo under the path `ops-supportability/conf/ops_events.yaml`.

Following is the structure of the file:

```
categories:
     - event_category:
       description:
       category_rank:
```
```
event_definitions:
      - event_name:
        event_category:
        event_ID:
        severity:
        keys:
        event_description:
```

## Sample YAML file

```ditaa

categories:
      - event_category: LLDP_EVENTS
        description: 'Events related to LLDP_A'
	    category_rank: 001

      - event category: LLDP_A
        description: 'Events related to LLDP_A'
	    category_rank: 002

      - event category: LLDP_B
        description: 'Events related to LLDP_B'
	    category_rank: 003

      - event category: FAN_EVENT
        description: 'Events related to FAN'
	    category_rank: 004

event_definitions:

      - event_name: LLDP_A
        event_category: LLDP
        event_ID : 001001
        severity: LOG_INFO
        keys: X, Y
        event_description: 'LLDP {X} ADDED ON {Y}'

      - event_name: LLDP_B
        event_category: LLDP
        event_ID : 001002
        severity: LOG_INFO
        keys: x,y
        event_description: 'LLDP neighbor added on {x} with {y}'

      - event_name: FAN_EVENT
        event_category: FAN
        event_ID : 002001
        severity: LOG_EMER
        keys: key1,key2
        event_description: 'High temperature detected'
```

## API usage

### C API usage
Every daemon that defined its event category of interest and its events in a YAML file, calls event_log_init(category_name) during initialization. This enables the daemon to log all the events in that category by using the log_events(event_name, key-values,...) API.

Following is the syntax of the APIs:

`int event_log_init("event_category")`

- Initializes feature or event category specific events for the daemon.

- Returns 0 on success or -1 on failure.

- An argument of `event_log_init` API is `event_category`. This is the category of events that needs to be initialized for the daemon.

For example:
 (a) `event_log_init("LLDP")`
 (b) `event_log_init("FAN")`
 (c) `event_log_init("OSPF")`


Events can be logged using:
```
int log_event(char *event_name, char *key-value1, char *key-value2,...)
```
Arguments that are passed in the log_event API are:
- event_name - A unique event name that is defined in the YAML file.
- Key, Value - This should be specified as `EV_KV("Key", format-specifier, Value)`.

For example:
- With Key Value Pairs
   ```
   EV_KV("lldp_neighbour", "%d", test)
   log_event("LLDP_A", EV_KV("X", "%d", value_of_X), EV_KV("Y", "%s", "testing" ))
   ```
- Without Key Value Pairs
   ```
   log_event("FAN_EVENT", NULL)
   ```

### Python API usage
Python APIs can be used by Python daemons to log events.

Syntax of the Python APIs:

`event_log_init("event_category")`

Initializes feature or event category specific events for the daemon:

- Returns -1 on failure.

- An argument of `event_log_init` API is `event_category`. This is the category of events that needs to be initialized for the daemon.

For example:
 (a) `event_log_init("LLDP")`
 (b) `event_log_init("FAN")`
 (c) `event_log_init("OSPF")`

 Events can be logged by using:

 `log_event(event_name, [Key, Value],..)`

 Arguments that are passed in the log_event API are:
 - event_name - A unique event name that is defined in the YAML file.
 - Key, Value - This should be specified as `[Key, Value]`.

 For example:
  - With Key Value Pairs:

    `log_event("LLDP_A", ["X", value_of_X], ["Y", "testing"])`

  - Without Key Value Pairs:

    `log_event("FAN_EVENT")`

## show events CLI

The logged events can be viewed from the vtysh shell by invoking the command `show events`.
