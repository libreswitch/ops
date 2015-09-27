
<!--  See the https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet for additional information about markdown text.
Here are a few suggestions in regards to style and grammar:
* Use active voice. With active voice, the subject is the doer of the action. Tell the reader what
to do by using the imperative mood, for example, Press Enter to view the next screen. See https://en.wikipedia.org/wiki/Active_voice for more information about the active voice. 
* Use present tense. See https://en.wikipedia.org/wiki/Present_tense for more information about using the present tense. 
* Avoid the use of I or third person. Address your instructions to the user. In text, refer to the reader as you (second person) rather than as the user (third person). The exception to not using the third-person is when the documentation is for an administrator. In that case, *the user* is someone the reader interacts with, for example, teach your users how to back up their laptop. 
* See https://en.wikipedia.org/wiki/Wikipedia%3aManual_of_Style for an online style guide.
Note regarding anchors:
--StackEdit automatically creates an anchor tag based off of each heading.  Spaces and other nonconforming characters are substituted by other characters in the anchor when the file is converted to HTML. 
 -->

# logrotate Commands #


<!--Provide the name of the grouping of commands, for example, LLDP commands-->


## Contents ##
[TOC]

#Configuration commands #
###  logrotate period ###
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
```
    [no] logrotate period ( hourly | weekly | monthly )
```
#### Description ####

This command configures the rotation of log files based on time. The possible values are hourly, weekly or  monthly. When the time difference between the last rotation of a log file and current time exceeds the configured value, the log rotation is triggered for that particular file. To reset the log rotation to the default value of `daily`, use the `no` form of the command (`no logrotate period ( hourly | weekly | monthly)`).
#### Authority ####

    All users
#### Parameters ####
```ditaa

+----------------+--------------+-------------+---------------------------------+
|                |              |             |                                 |
|  Parameter     |  Status      |  Syntax     | Description                     |
+-------------------------------------------------------------------------------+
|                |              |             |                                 |
|   period_value |  Required    |  'hourly'   | Rotates log files every hour.   |
|                |              |             |                                 |
|                |              |  'monthly'  | Rotates log files every month.  |
|                |              |             |                                 |
|                |              |  'weekly'   | Rotates log files every week.   |
|                |              |             |                                 |
+----------------+--------------+-------------+---------------------------------+
```

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
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
   All users
#### Parameters ####
<!--Provide for the parameters for the command.-->
  *filesize*

Specify the maximum file size in megabytes (MB) for the log rotation. The range is from 1 to 200 MB. If a value is not specified, the default value is 10 MB.
```ditaa
+----------------+--------------+-------------+---------------------------------+
|                |              |             |                                 |
|  Parameter     |  Status      |  Syntax     | Description                     |
+-------------------------------------------------------------------------------+
|                |              |             |                                 |
|  *filesize*    |  Required    |  <1-200>    | File size in Mega Bytes (MB).   |
|                |              |             | Default value is 10MB           |
|                |              |             |                                 |
+----------------+--------------+-------------+---------------------------------+

```

#### Examples ####
<!--    myprogramstart -s process_xyz-->
```
   switch(config)# logrotate maxsize 20
```


### logrotate target ###

#### Syntax ####

```
   [no] logrotate target <URI>
```
#### Description ####
<!--Provide a description of the command. -->
This command sends the rotated log files to a specified remote host Universal Resource Identifier (URI) by using the `tftp` protocol. If no URI is specified, the rotated and compressed log files are stored locally in the `/var/log/` path. To prevent rotated logs from being sent to a remote host, use the `no` form of the command (`no logrotate target *URI*`).
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
   All users
#### Parameters ####
<!--Provide for the parameters for the command.-->
    *URI*


This parameter specifies the URI of the remote host. The possible values are `tftp://A.B.C.D' or 'tftp://X:X::X:X`. Both IPv4 and IPv6 addresses are supported.

```ditaa

+----------------+--------------+-------------+---------------------------------+
|                |              |             |                                 |
|  Parameter     |  Status      |  Syntax     | Description                     |
+-------------------------------------------------------------------------------+
|                |              |             |                                 |
|  URI           |  Required    |  String     | URI of the remote host.         |
|                |              |             | Supported values :              |
|                |              |             | 'tftp://A.B.C.D' or             |
|                |              |             | 'tftp://X:X::X:X'               |
|                |              |             |                                 |
|                |              |             |                                 |
+----------------+--------------+-------------+---------------------------------+
```

#### Examples ####
<!--    myprogramstart -s process_xyz-->
```
    switch(config)# logrotate target tftp://192.168.1.132 93
    switch(config)# logrotate target tftp://2001:db8:0:1::128
```

##Display Commands ##
### show logrotate ###
<!--Change the value of the anchor tag above, so this command can be directly linked. -->
#### Syntax ####
<!--For example,    myprogramstart [option] <process_name> -->
```
    show logrotate
```

#### Description ####
<!--Provide a description of the command. -->
This command displays configuration parameters for the `logrotate` commands.
#### Authority ####
<!--Provide who is authorized to use this command, such as Super Admin or all users.-->
     All users
#### Parameters ####
<!--Provide for the parameters for the command.-->
#### Examples ####
<!--    myprogramstart -s process_xyz-->
```
    h1# show logrotate
    Logrotate configurations :
    Period            : weekly
    Maxsize           : 20MB
    Target            : tftp://2001:db8:0:1::128
```