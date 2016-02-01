# Show Events Command
## Contents

- [Configuration commands](#configuration-commands)
- [Display commands](#display-commands)
  - [Commands summary](#commands-summary)
  - [Show events](#show events)
     - [Syntax](#syntax)
     - [Description](#description)
     - [Authority](#authority)
     - [Examples](#examples)

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

### Show events
#### Syntax
`show events`
#### Description
Runs the `show events` command for all the supported features.
#### Authority
All users
#### Examples
switch# configure t
switch(config)# lldp enable
switch(config)# no lldp enable
switch(config)# lldp timer 100
switch(config)# lldp management-address 10.0.0.1
switch(config)# end
switch# show events

---------------------------------------------------
events log
---------------------------------------------------
2016-01-20:14:17:15.041851|ops-lldpd|1002|LOG_INFO|LLDP Disabled
2016-01-20:14:17:54.562838|ops-lldpd|1001|LOG_INFO|LLDP Enabled
2016-01-20:14:18:55.397152|ops-lldpd|1003|LOG_INFO|Configured LLDP tx-timer with 100
2016-01-20:14:20:16.715133|ops-lldpd|1007|LOG_INFO|Configured LLDP Management pattern 10.0.0.1
