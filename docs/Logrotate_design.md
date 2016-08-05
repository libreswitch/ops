#Log-rotate design

- [High level design](#high-level-design)
- [Responsibilities](#responsibilities)
- [Design choices](#design-choices)
- [Relationships to external OpenSwitch entities](#relationships-to-external-openswitch-entities)
- [OVSDB-Schema](#ovsdb-schema)
- [Internal structure](#internal-structure)
   - [CLI](#cli)
   - [REST](#rest)
- [References](#references)

##High level design
The CLI and REST API allows you to configure log-rotate parameters on the Open vSwitch Database (OVSDB). A Python script reads the log-rotate configuration and populates the respective log-rotate configuration file (`/etc/logrotate.ovs`). The Python script then runs the `logrotate` command `logrotate /etc/logrotate.ovs`.


##Responsibilities



  - Rotates the log files based either on period or on size or based on both period and size (whichever condition occurs first).
  - Compresses the rotated log files.
  - Rotated log files stored locally or transferred to the remote destination.


##Design choices

Log-rotate works as follows:

- The script for running the log-rotate feature runs hourly as a cron job.
- The log-rotate script uses the Linux logrotate utility for log rotation.
- Post rotation,log-rotate script compresses the rotated log file in gunzip format.
-  All module logs are stored in `var/log/messages`, all authentication logs are stored in `/var/log/auth.log', all audit logs are stored in '/var/log/audit/audit.log' and all event logs are stored in '/var/log/event.log'. Only logs stored in these paths are rotated.
- Management of rotated log files:
  - Rotated log files are compressed and stored locally in the path '/var/log/', regardless of the remote host configuration 
  - Rotated log files are stored with respective time extension to the granularity of hour and switch name in the format "file1- YYYYMMDDHH_${switchname}.gz" (e.g., messages-2015080715_access1.gz)
  - Rotated log files are replaced when the number of old rotated log files exceeds three. The newly rotated log file replaces the oldest rotated log file.
- Remote transfer of rotated log files:
  -  Only TFTP protocol is supported.
  -  Both IPv4 and IPv6 addresses are supported. But broadcast, multicast and loopback addresses are not supported.
  -  Only newly rotated log files are transferred to the remote host during the log rotation. Previously rotated log files are not transferred.
  -  Packet level failures with TFTP are handled in the protocol itself. With each TFTP session failure, TFTP retries the file transfer three times. Retries have a  timeout of five seconds.


##Relationships to external OpenSwitch entities

The following diagram provides a detailed description of the relationships and interactions.
```ditaa

	+---------------+              +---------------+
	|               |              |               |
	|   CLI         |              |    REST       |
	|               |              |               |
	+--------+------+              +------+--------+
	         |                            |
	         |                            |
	         |                            |
	    +------------------------------------------------------------------------------------+
	    |  +----------------------------------------+                          OVSDB         |
	    |  |                             System     |                                        |
	    |  | logrotate_config_col                   |                                        |
	    |  |                                        |                                        |
	    |  |                                        |                                        |
	    |  +----------------------------------------+                                        |
	    +------------------------------------------------------------------------------------+
	                          |
	                          |
	                          |
	                          |
	        +-----------------+--------------------+
	        |                                      |
	        |  Logrotate script scheduled as       |
	        |   an hourly cron job                 |
	        |                                      |
	        |                                      |
	        +--------------------------------------+
```

##OVSDB-Schema
System is the top level configuration table in the Open Halon configuration database.
The log-rotate configuration parameters are specified as logrotate\_config column in System table.

	+------------------------------------------------------------------------------------+
	|  +----------------------------------------+                          OVSDB         |
	|  |                             System     |                                        |
	|  | logrotate_config_col                   |                                        |
	|  |                                        |                                        |
	|  |                                        |                                        |
	|  +----------------------------------------+                                        |
	+------------------------------------------------------------------------------------+


##Internal structure

####CLI and REST sub-modules####

The CLI and REST sub-modules both perform the following functions:
  - Configures the various log-rotate parameters such as period, maxsize, and target.
  - The CLI provides a basic sanity check of the entered parameters, such as verifying the IP entered or validating the range of the maximum file size.
  - Updates the “logrotate_config” column.
  -Displays the configuration parameters for the log-rotation feature using the `show logrotate` CLI command.

####Log-rotate script####
Log-rotate script (scheduled as a hourly cron job) performs the following functions:

- Retrieves the configurations from OVSDB and populates the respective logrotate config file (/etc/logrotate.ovs)
- Executes the logrotate command using the updated config 'logrotate /etc/logrotate.ovs'
- Performs post rotate operations, such as compression and remote transfer.

##References

* [Logrotate CLI](http://www.openswitch.net/documents/user/Logrotate_cli)


<!-- Include references to any other modules that interact with this module directly or through the database model. For example, CLI, REST, etc.
ops-fand might provide reference to ops-sensord, etc. -->
