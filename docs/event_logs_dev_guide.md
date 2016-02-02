# Event Log Infrastructure Developer Guide

## Contents

- [Overview](#overview)
- [How to define an event in YAML file](#how-to-define-an-event-in-yaml-file)
- [Sample yaml File](#sample-yaml-file)
- [API usage](#api-usage)
- [show events CLI](#show-events-cli)

## Overview
Event log framework is designed to facilitate generation and processing of high level events which are related to the functionality and components of the switch. Examples are - Port state change event, LLDP neighbor discovered, Management Interface IP address updated etc.

Events can be generated from various sources in the system: Protocol daemons, Hardware daemons, Linux System, System health monitoring daemons, Configuration daemons etc. 

Events may be generated  as a result of state change in a daemon, hardware behavior, system health monitoring, user initiated configuration changes etc.

Events are different from debug logs which can be logged using the logging APIs. 
Unlike debug logs whose severity can be changed at run time to control what messages are logged, events cannot be filtered at the time of generation.

- An event has a unique ID. Other attributes are severity and timestamp when event is generated and optional list of key-value pairs.
- Events are stored in a format so that further processing can be done efficiently such as filtering, sorting etc.

To ensure the events are meaningful, events should be predefined by feature developers during the feature development. Events should be categorized by specifying an event category to enable easier filtering of events. Information elements which are part of the event must be defined.

Generated events are stored in a file on the persistent storage area of switch.

## How to define an event in YAML file
Event Log infrastructure makes use of a YAML file to define events and their corresponding categories.

The event yaml file is placed in ops-supportability repo under the path "ops-supportability/conf/ops_events.yaml"

The structure of this file is as shown below


Categories:
     - event_category:
       description:
       category_rank:

event_definitions:
      - event_name:
        event_category:
        event_ID :
        severity:
        keys:
        event_description:

## Sample yaml File

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

Every daemon which defined their event category of interest and events in YAML file are supposed to call event_log_init(category_name) during initialization. This will enable that daemon to log all the events in that category using log_events(event_name, key-values,...) API.

The following are the syntax of the API's:

int event_log_init("event_category");

- Initialize feature or event category specific events for the daemon.

- returns 0 on success , -1 on failure.

- an argument of event_log_init API is event_category.The category of events which needs to be initialized for the daemon.

Example:
 (a) event_log_init("LLDP")
 (b) event_log_init("FAN")
 (c) event_log_init("OSPF")


Events can be logged using:
```
int log_event(char *event_name, char *key-value1, char *key-value2,...)
```
- arguments are passed in log_event API are event_name- unique event name as defined in YAML
file,
 Key, Value - This should be specified as EV_KV("Key", format-specifier, Value)

Example:EV_KV("lldp_neighbour", "%d", test)

(a)log_event("LLDP_A", EV_KV("X", "%d", value_of_X), EV_KV("Y", "%s", "testing" ))
(b)log_event("FAN_EVENT", NULL)


## show events CLI

The logged events could be viewed from the vtysh shell by invoking the command "show events".
