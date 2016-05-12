#Show Vlog Commands

## Contents

- [Display commands](#display-commands)
	- [Commands summary](#commands-summary)
	- [Show vlog](#show-vlog)
	- [Show vlog daemon](#show-vlog-daemon)
	- [Show vlog severity](#show-vlog-severity)
	- [Show vlog config list](#show-vlog-config-list)
	- [Show vlog config feature](#show-vlog-config-feature)
	- [Show vlog config daemon](#show-vlog-config-daemon)
	- [Show vlog config](#show-vlog-config)
	- [Show vlog daemon (daemon_name) severity (severity_level)](#show-vlog-daemon-daemonname-severity-severitylevel)
	- [Examples](#examples)
- [References](#references)

## Display commands
### Commands summary
| Command | Usage |
|:------- |:------|
| **show vlog** | Displays vlog messages of ops daemons. |
| **show vlog daemon (daemon_name)** | Displays the vlog messages of the corresponding ops-daemon only. |
| **show vlog severity (severity_level)** | Displays the vlog messages of the corresponding severity level and above. |
| **show vlog config list** | Displays a list of supported features and descriptions. |
| **show vlog config feature (feature_Name)** | Displays the feature configuration log level of syslog and file destinations. |
| **show vlog config daemon (daemon_Name)**| Displays the daemon configuration log level of syslog and file destinations. |
| **show vlog config** | Displays a list of supported features' corresponding daemons logging levels of file and console destinations. |
| **show vlog daemon (daemon_name) severity (severity_level)** | Displays vlogs for the specified ops-daemon with the specified severity level and above. |
| **show vlog severity (severity_level) daemon (daemon_name)** | Displays vlogs for the specified severity level and above with ops-daemon only. |


### Show vlog
#### Syntax
`show vlog`
#### Description
Displays vlog messages of ops daemons.
#### Authority
All users.
#### Parameters
No parameters.

### Show vlog daemon
#### Syntax
`show vlog daemon <daemon_name>`
#### Description
Displays only the corresponding ops daemon vlog messages.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *daemon_name* | Required | String | Name of the ops daemon. |

### Show vlog severity
#### Syntax
`show vlog severity <emer/err/warn/info/debug>`
#### Description
Displays corresponding severity level and above vlog messages.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *emer* | Required | Keyword  | Emergency logs only.  |
| *err* | Required | Keyword | Error and above severity logs. |
| *warn* | Required | Keyword | Warning and above severity logs. |
| *info* | Required | Keyword | Information and above severity logs. |
| *debug* | Required | Keyword | All logs. |

### Show vlog config list
#### Syntax
`show vlog config list`
#### Description
Lists all vlog supported features and descriptions.
#### Authority
All users.
#### Parameters
No parameters.

### Show vlog config feature
#### Syntax
`show vlog config feature <feature_name>`
#### Description
Displays the feature configuration log levels of file and syslog destinations.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *feature_name* | Required | String | Name of the feature. |

### Show vlog config daemon
#### Syntax
`show vlog config daemon <daemon_name>`
#### Description
Displays the ops-daemon configuration log levels of file and syslog destinations.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *daemon_name* | Required | String | Name of the ops daemon. |

### Show vlog config
#### Syntax
`show vlog config`
#### Description
Lists all supported features and coresponding daemons logging levels of file and syslog destinations.
#### Authority
All users.
#### Parameters
No parameters.

### Show vlog daemon (daemon_name) severity (severity_level)
#### Syntax
`show vlog daemon <daemon_name> severity <severity_level>`
#### Description
Displays vlogs for the specified ops-daemon only with specified severity level and above.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------|:---------------------------------------|
| *daemon_name* | Required | String | Name of the ops daemon. |
| *severity_level* | Required | Keyword (emer/err/warn/info/dbg)| Severity log level.  |

### Examples
```
switch# show vlog

-----------------------------------------------------
show vlog
-----------------------------------------------------
ovsdb-server            |ovs|00001|ovsdb_server|INFO|ovsdb-server (Open vSwitch) 2.5.0
ops-arpmgrd             |ovs|00001|arpmgrd|INFO|ops-arpmgrd (OpenSwitch arpmgrd) 2.5.0
ops-arpmgrd             |ovs|00002|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connecting...
ops-arpmgrd             |ovs|00003|reconnect|INFO|unix:/var/run/openvswitch/db.sock: connected
ops-arpmgrd             |ovs|00004|ovsdb_idl|INFO|DEBUG first row is missing from table class System
ops-intfd               |ovs|00001|ops_intfd|INFO|ops-intfd (OpenSwitch Interface Daemon) started
.......


switch# show vlog daemon ops-lldpd

---------------------------------------------------
show vlog
----------------------------------------------------
ovs|00001|lldpd_ovsdb_if|INFO|ops-lldpd (OPENSWITCH LLDPD Daemon) started

switch# show vlog severity warn

---------------------------------------------------
show vlog
-----------------------------------------------------
ops-sysd            |ovs|00005|ovsdb_if|ERR|Failed to commit the transaction. rc = 7
ops-pmd             |ovs|00007|timeval|WARN|Unreasonably long 2802ms poll interval (168ms user, 29ms system)
ops-pmd             |ovs|00008|timeval|WARN|faults: 590 minor, 0 major
ops-pmd             |ovs|00009|timeval|WARN|context switches: 637 voluntary, 70 involuntary
ops-sysd            |ovs|00006|ovsdb_if|ERR|Failed to commit the transaction. rc = 7
ops-intfd           |ovs|00007|intfd_ovsdb_if|WARN|value for speeds not set in h/w description file
......

switch# show vlog config list

================================================
Features          Description
================================================
lldp              Link Layer Discovery Protocol
lacp              Link Aggregation Control Protocol
fan               System Fan

switch# show vlog config feature lldp
========================================
Feature               Syslog     File
========================================
lldp                   DBG       WARN

switch# show vlog config daemon ops-fand

======================================
Daemon              Syslog     File
======================================
ops-fand             DBG       WARN

switch# show vlog config

=================================================
Feature         Daemon          Syslog     File
=================================================
lldp            ops-lldpd        DBG        DBG

                ops-portd       INFO       INFO

lacp            ops-lacpd        OFF        OFF

                ops-ledd         DBG       EMER

fan             ops-fand        INFO       INFO


switch# configure t
switch(config)# vlog feature lacp syslog dbg
switch(config)# vlog daemon ops-lldpd file warn
switch(config)# end
switch# show vlog feature lacp

========================================
Feature               Syslog     File
========================================
lacp                   DBG       INFO

switch# show vlog daemon ops-lldpd

======================================
Daemon              Syslog     File
======================================
ops-lldpd            DBG       WARN

switch# configure t
switch(config)# vlog feature lacp file dbg
switch(config)# vlog daemon ops-lldpd syslog info
switch(config)# vlog feature fand all dbg
switch(config)# end

switch# show vlog config feature lacp

========================================
Feature               Syslog     File
========================================
lacp                   OFF        DBG

switch# show vlog config daemon ops-lldpd

======================================
Daemon              Syslog     File
======================================
ops-lldpd           INFO        DBG

switch# show vlog config feature fan

========================================
Feature               Syslog     File
========================================
fan                   DBG        DBG


switch# show vlog severity debug daemon ops-pmd

---------------------------------------------------
show vlog
-----------------------------------------------------
ovs|00006|ops_pmd|INFO|ops-pmd (OpenSwitch pmd) 0.02
```

## References
- [Show Vlog User Guide](showvlog_user_guide)
