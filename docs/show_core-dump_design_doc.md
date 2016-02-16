#Show Core Dump Design Document

##Contents
- [High level design of show core dump](#high-level-design-of-show-core-dump)
- [Design choices](#design-choices)
	- [Get crash information from the event log and display the coredumps](#get-crash-information-from-the-event-log-and-display-the-coredumps)
	- [Iterate through the core dump storage location and list all the coredump present there.](#iterate-through-the-core-dump-storage-location-and-list-all-the-coredump-present-there)
	- [Final choice](#final-choice)
- [Limitations](#limitations)
- [Block diagram](#block-diagram)
- [Example](#example)

### High level design of show core dump
The show core dump command lists all of the core dumps present in the switch including the kernel core dump. This helps the user support team to find out what crashes happened in the system. It displays the name of crashed daemon along with time of the crash.

### Design choices
We had the following two design choices for displaying the core dumps:


#### Get crash information from the event log and display the core dumps

When `show core-dump` is executed, the system looks into the sd-journal log for crash events.  It then verifies whether or not the file exists in the given file location. If it exists, then it will display the same in the output.  Since the core dumps could have been removed by the user, you need to verify whether or not it is present in the system.

####  Iterate through the core dump storage location and list all the core dumps present there

Locate the core dump by reading the core dump configuration file. Iterate though the core dump storage location and list only those files present in that location.  The core dump daemon name and timestamp is obtained by parsing the name of the core dump file.

#### Final choice
Iterate through the core dump storage location and list all the core dumps present there.  We finalized on this choice based on the following reasons:
  1. Going through all the entries in the journal is an expensive process.
  2. Some entries might refer to core dumps that are already removed.

### Limitations
The core dump files are stored with a specific name format.  The name includes the daemon that crashed and the crash event timestamp.  If the name of the core file is changed, then the information will be based on the new file name.  If the new file name does not follow the core dump file naming format, then that core dump is not displayed.

### Block diagram

```ditaa

  CLI Command
 +---------------+        +-------+------+
 |show core-dump | Read   |  Core Dump   |
 |               |------->+  Location    |
 +---------------+        +-------+------+
```

### Example

```

switch# show core-dump
===========================================================
TimeStamp           | Daemon Name
===========================================================
2016-10-09 09:08:22   ops-lldpd
2015-09-12 10:34:56   kernel
===========================================================
Total number of core dumps : 1
===========================================================

```

If there are no core dumps present, the following information appears:

```
switch# show core-dump
No core dumps are present
```
