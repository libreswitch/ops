# Show Events Command

## Contents

- [Configuration commands](#configuration-commands)
- [Display commands](#display-commands)
	- [Commands summary](#commands-summary)
		- [Log filters](#log-filters)
	- [Show events](#show-events)
		- [Syntax](#syntax)
		- [Description](#description)
		- [Authority](#authority)
		- [Examples](#examples)
	- [events log](#events-log)
	- [show event logs](#show-event-logs)

## Configuration commands

`switch# configure terminal`

For example:

`switch(config)# lldp enable`

`switch(config)# no lldp enable`

`switch(config)# lldp timer 125`

## Display commands
### Commands summary
| Command | Usage|
|:--------|:--------|
| **show events**| Displays events for all supported features|
#### Log filters
| Command | Usage|
|:--------|:--------|
| **show events event-id <<filler>ev-id>**| Displays events with supplied event ID
| **show events severity <<filler>severity-level>**| Displays events with supplied severity|
| **show events category <<filler>category>**| Displays events of supplied category|
| **show events reverse**| Displays events in reverse order|

### Show events
#### Syntax
#### Description
```
show events
show events event-id <event-id>
show events severity <severity-level>
show events category <category>
show events reverse
```

#### Description
Runs the `show events` command for all the supported features.
#### Authority
All users
#### Examples
```
switch# configure t
switch(config)# lldp enable
switch(config)# no lldp enable
switch(config)# lldp timer 100
switch(config)# lldp management-address 10.0.0.1
switch(config)# end
switch# show events
```

### events log
```
2016-01-20:14:17:15.041851|ops-lldpd|1002|LOG_INFO|LLDP Disabled
2016-01-20:14:17:54.562838|ops-lldpd|1001|LOG_INFO|LLDP Enabled
2016-01-20:14:18:55.397152|ops-lldpd|1003|LOG_INFO|Configured LLDP tx-timer with 100
2016-01-20:14:20:16.715133|ops-lldpd|1007|LOG_INFO|Configured LLDP Management pattern 10.0.0.1

switch# show events event-id 1002
```

### show event logs
```
2016-02-19:03:55:05.391372|ops-lldpd|1002|LOG_INFO|LLDP Disabled

switch# show events category LLDP
```

### show event logs
```
2016-02-19:03:55:05.391372|ops-lldpd|1002|LOG_INFO|LLDP Disabled
2016-02-19:03:57:50.249296|ops-lldpd|1003|LOG_INFO|Configured LLDP tx-timer with 9
2016-02-19:03:57:57.342332|ops-lldpd|1007|LOG_INFO|Configured LLDP Management pattern 10.1.1.1

switch# show events severity emer
```

### show event logs
```
No event match the filter provided

switch# show events reverse
```
### show event logs
```
2016-02-19:03:57:57.342332|ops-lldpd|1007|LOG_INFO|Configured LLDP Management pattern 10.1.1.1
2016-02-19:03:57:50.249296|ops-lldpd|1003|LOG_INFO|Configured LLDP tx-timer with 9
2016-02-19:03:55:05.391372|ops-lldpd|1002|LOG_INFO|LLDP Disabled
```
