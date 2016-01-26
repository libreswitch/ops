# High Level Design of Event logging Infra

Event Logging provides system administrators/support/lab with information useful for diagnostics and auditing. This facilities localization and allows system administrators/support/lab to more easily obtain information on problem that occur and provide an appropriate solution to problem.

## Contents
- [Responsibilities](#responsibilities)
- [Design choice](#design-choice)
- [Block Diagram](#block-diagram)
- [OVSDB-Schema](#ovsdb-schema)
- [Event logging Configuration Yaml File](#event-logging-configuration-yaml-file)
- [Event Initialization](#event-initialization)
- [Event Logging](#event-logging)
- [Configure rsyslog](#configure-rsyslog)
- [Data structures](#data-structures)


## Responsibilities
The Event logging Infrastructure is responsible to generate and capture Event logs from different Features/Daemons.

## Design choice

Event logging framework is a part of supportability infrastructure.All feature/module owners need to use this framework as a library for generating their specific event logs.

ops_events.yaml is a global file.Information about the events of the corresponding modules are read from this yaml file and kept in the datastructure.  Later this information is referred while logging the events.

Systemd journal provides a centralized management solution for logging all kernel and userland process.The system that collects and manages these logs by journal.By using journalctl utility able to access and manipulate the data held with in the journal.journald daemons collects data from all available sources and stores them in a binary format.

journal events can be transferred to different looging ways.
- messages are immediately forwarded to socket (/run/systemd/journal/syslog),where traditional syslog can read them.This can be controlled by **ForwardToSyslog=**option.

For Event Logging we are using `sd_journal_send` api and log it directly to the systemd journal.  Later the event logs are copied from journal to a seperate eventlog file for easy access.


## Block Diagram

```ditaa
event_log_init(event_category)

 +--------------+      +-------------+
 | (libyaml)    |store |  evt_table  |
 | parsing yaml +----->|             |
 +------+-------+table +------^---+--+
        ^                     |   |
        |                     |   |
        |                     |   |
 +------+-------+             |   |
 | ops_events.  |             |   |log_event(event_name,key-value)
 |    yaml      |         +---+---v--------+
 +--------------+         | sd_journal_send|
                          |                |
                          +------+---------+
                                 |
  CLI command                    v
 +--------------+        +-------+------+
 | show events  |        |   journal    |
 |              | <------+              |
 +--------------+        +-------+------+
                                 | forwarded
                                 |   to
                          +------v-------+
                          |    rsyslog   |
                          |              |
                          +-------+------+
                                  | rsyslog.conf
                                  |
                           +------v-------+
                           |   event.log  |
                           |              |
                           +--------------+

```

## OVSDB-Schema
ovsdb schema is not used for this feature.


## Event logging Configuration Yaml File

List of Event log Categories are defined in yaml file.

eg: Event_Groups:
   event_category: LLDP
   event category: FAN
   event category: OSPF
   event category: BGP

Event_Definition:

event_name: A unique name for the event.
event_category: event_category is already added into event category list.
evt_ID: first 2 digits belongs to event category and last 3 for its events.
severity: LOG_EMER, LOG_ALER, LOG_CRIT, LOG_ERR, LOG_WARN, LOG_NOTICE, LOG_INFO
Keys: The variables that need to be populated during run time.
event_description: The event description string.

Define your feature specific events as per the below format in ops_event.yaml file.

Yaml file should be under /etc/supportability/ops_event.yaml

Sample Yaml File with Two daemon events Definition is shown below.

---

   categories:
   -
      event_category: LLDP_EVENTS
      description: 'Events related to LLDP_A'
   -
      event category: LLDP_A
      description: 'Events related to LLDP_A'
   -
      event category: LLDP_B
      description: 'Events related to LLDP_B'
   -
      event category: FAN_EVENT
      description: 'Events related to FAN'

event_definitions:
   -
      event_name: LLDP_A
      event_category: LLDP
      event_ID : 01001
      severity: LOG_INFO
      keys: X, Y
      event_description: 'LLDP {X} ADDED ON {Y}'
   -
      event_name: LLDP_B
      event_category: LLDP
      event_ID : 01002
      severity: LOG_INFO
      keys: x,y
      event_description: 'LLDP neighbor added on {x} with {y}'
   -
      event_name: FAN_EVENT
      event_category: FAN
      event_ID : 02001
      severity: LOG_EMER
      keys: key1,key2
      event_description: 'High temperature detected'

## Event Initialization
      API Prototype: int event_log_init("event_category")

Each Feature should call event_log_init() API during its init or just before logging an event.
- an argument of event_log_init API is event_category.The category of events which needs to be initialized for the daemon.
- Initialize feature or event category specific events for the daemon.
- returns 0 on sucess.
- returns -1 on failure for
   - if category name is NULL
   - failed to create event_table for daemons.
   - check whether event_log_init () on this category already done.
      if that is the case daemon will be present in event table.

Example:
   (a) event_log_init("LLDP")
   (b) event_log_init("FAN")
   (c) event_log_init("OSPF")


## Event Logging
   API Prototype: int log_event(char *event_name, char *key-value1, char *key-value2,...)

Log an event using log_event () API.
-  Log the specified feature event.
-  arguments are passed in log_event API are event_name- unique event name as defined in YAML file
   Key, Value - This should be specified as EV_KV("Key", format-specifier, Value)
   Example:EV_KV("lldp_neighbour", "%d", test)
-  returns 0 on success.
-  returns -1 on failure for
   - if event_name is NULL
   - not able to find the given event_name in the event table.

Example:
   (a)log_event("LLDP_A", EV_KV("X", "%d", value_of_X), EV_KV("Y", "%s", "testing" ))
   (b)log_event("FAN_EVENT", NULL)

## Configure rsyslog

    rsyslog.conf is configured file to store logs in separate file event.log.


## Data structures

Event log Configuration file event.yaml is parsed and stored in the following data structure.
```
typedef struct{
    int event_id;
    char event_name[64];
    char severity[24];
    int num_of_keys;
    char event_description[240];
    }event;

event ev_table[1024];
```
Some important fields in the journal entry for an event are shown below:

```
eg:
- "__REALTIME_TIMESTAMP" : "1453705711129950",
- "PRIORITY" : "6",
- "_PID" : "20",
- "_COMM" : "systemd-journal",
- "_SYSTEMD_UNIT" : "systemd-journald.service",
- "MESSAGE" : "Journal started",
- "MESSAGE_ID" : "f77379a8490b408bbe5f6940505a777b"
```
