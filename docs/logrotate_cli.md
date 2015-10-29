# logrotate Commands #

## Contents ##

- [Configuration commands](#configuration-commands)
	- [logrotate period](#logrotate-period)
	- [logrotate maxsize](#logrotate-maxsize)
	- [logrotate target](#logrotate-target)
- [Display Commands](#display-commands)
	- [show logrotate](#show-logrotate)

# Configuration commands #
###  logrotate period ###
#### Syntax ####
```
    [no] logrotate period ( hourly | weekly | monthly )
```
#### Description ####

This command configures the rotation of log files based on time. The possible values are hourly, weekly or  monthly. When the time difference between the last rotation of a log file and current time exceeds the configured value, the log rotation is triggered for that particular file. To reset the log rotation to the default value of `daily`, use the `no` form of the command (`no logrotate period ( hourly | weekly | monthly)`).
#### Authority ####

All users

#### Parameters ####

| Parameter | Status   | Syntax | Description          |
|-----------|----------|--------|------------------------|
|   period_value |  Required    |  'hourly'   | Rotates log files every hour.   |
|                |              |  'monthly'  | Rotates log files every month.  |
|                |              |  'weekly'   | Rotates log files every week.   |

If no parameter is specified, the default value of `daily` is used.
#### Examples ####
```
    switch(config)# logrotate period weekly
```

### logrotate maxsize ###

#### Syntax ####
```
   [no] logrotate maxsize <filesize>
```
#### Description ####

This command configures the log rotation based on log file size. The log file size is checked hourly. When the size of the log file exceeds the configured value, the rotation is triggered for that particular log file.
To reset the default value of 10 MB, use the `no` form of the command (`no logrotate maxsize *filesize*`).

#### Authority ####
   All users

#### Parameters ####
  *filesize*

Specify the maximum file size in megabytes (MB) for the log rotation. The range is from 1 to 200 MB. If a value is not specified, the default value is 10 MB.

| Parameter | Status   | Syntax | Description          |
|-----------|----------|--------|------------------------|
|  *filesize*    |  Required    |  <1-200>    | File size in Mega Bytes (MB).  Default value is 10MB    |


#### Examples ####
```
   switch(config)# logrotate maxsize 20
```


### logrotate target ###

#### Syntax ####

```
   [no] logrotate target <URI>
```
#### Description ####
This command sends the rotated log files to a specified remote host Universal Resource Identifier (URI) by using the `tftp` protocol. If no URI is specified, the rotated and compressed log files are stored locally in the `/var/log/` path. To prevent rotated logs from being sent to a remote host, use the `no` form of the command (`no logrotate target *URI*`).
#### Authority ####
   All users
#### Parameters ####

This parameter specifies the URI of the remote host. The possible values are `tftp://A.B.C.D' or 'tftp://X:X::X:X`. Both IPv4 and IPv6 addresses are supported.

| Parameter | Status   | Syntax | Description          |
|-----------|----------|--------|------------------------|
|  URI           |  Required    |  String     | URI of the remote host.         |
|                |              |             | Supported values :              |
|                |              |             | 'tftp://A.B.C.D' or             |
|                |              |             | 'tftp://X:X::X:X'               |


#### Examples ####
```
    switch(config)# logrotate target tftp://192.168.1.132
    switch(config)# logrotate target tftp://2001:db8:0:1::128
```

## Display commands ##
### show logrotate ###
#### Syntax ####
```
    show logrotate
```

#### Description ####
This command displays configuration parameters for the `logrotate` commands.
#### Authority ####
     All users
#### Parameters ####
#### Examples ####
```
    h1# show logrotate
    Logrotate configurations :
    Period            : weekly
    Maxsize           : 20MB
    Target            : tftp://2001:db8:0:1::128
```
