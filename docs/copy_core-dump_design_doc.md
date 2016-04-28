# Copy Core Dump Design Document

##Contents
- [Copy Core Dump Design Document](#copy-core-dump-design-document)
	- [Contents](#contents)
	- [High level design of show core dump](#high-level-design-of-show-core-dump)
	- [Design choices](#design-choices)
	- [Block diagram](#block-diagram)
	- [Example  copy daemon coredump](#example-copy-daemon-coredump)
	- [References](#references)


## High level design of show core dump
Use the `copy core dump` command to copy the daemon or the kernel core file to the tftp or sftp server.

## Design choices
- The core files can be copied with or without specifying the destination file name.
- Maximum length of User name, destination file, or daemon name is limited to 50 characters and host name is up to 256 characters.
- Acceptable characters for the usernames are "a-zA-Z0-9_-"  .
- Acceptable characters for the host names are "A-Za-z0-9_.:-" .
- Acceptable characters for the file names are "A-Za-z0-9_.-" .
- Acceptable characters for daemon names are "A-Za-z0-9_.-" .
- Usernames or host names cannot use the "@" character. It is used as a separator between the user and the host while running ssh.


## Block diagram

```ditaa

  CLI Command
 +---------------+        +--------------+
 |copy core-dump | Read   |  Core Dump   |
 |               | -----> |  Location    |
 +---------------+        +--------------+
        |
        | copy
        v
 +---------------+
 | tftp          |
 | sftp server   |
 +---------------+

```

## Example copy daemon coredump

```
switch# show core-dump
======================================================================================
Daemon Name         | Instance ID | Crash Reason                  | Timestamp
======================================================================================
ops-snmpd             370           Segmentation fault             2016-04-26 18:17:56
ops-switchd           361           Segmentation fault             2016-04-26 18:07:36
ops-switchd           356           Segmentation fault             2016-04-26 18:06:32
======================================================================================
Total number of core dumps : 3
======================================================================================
switch#
switch#
switch# copy core-dump ops-switchd tftp 10.0.12.161
copying ...
Sent 4694776 bytes in 3.0 seconds
copying ...
Sent 4707280 bytes in 4.0 seconds
switch#
switch#
```

If there are no core dumps present, the following information appears:

```
No coredump found for daemon <daemon name>
```
```
switch#
switch# copy  core-dump ops-fand tftp 10.0.12.161
No coredump found for daemon ops-fand
switch#

```

## References
* [ Copy core-dump commands ]  copy_core-dump_cli_guide.md
* [ Copy core-dump userguide ] copy_core-dump_user_guide.md
* [ Copy core-dump design  ]  copy_core-dump_design_doc.md
