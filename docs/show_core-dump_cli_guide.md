# Show Core Dump CLI Guide

## Contents

- [show core dump](#show-core-dump)
	- [Syntax](#syntax)
	- [Description](#description)
	- [Authority](#authority)
	- [Parameters](#parameters)
	- [Examples](#examples)

### show core dump

#### Syntax
```
show core-dump
```

#### Description
This command lists all the core dumps in the switch. Each entry in the listing displays the daemon name that crashed and the timestamp of the crash event.

#### Authority
All users.

#### Parameters
No Parameters

#### Examples

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

If there are no core dumps to present, the following information appears:

```
switch# show core-dump
No core dumps are present
```
