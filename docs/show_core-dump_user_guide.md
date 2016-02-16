# Show Core Dump User Guide

## Contents

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
   - [Example](#example)


## Overview
This command lists all the core dumps in the switch. Each entry in the listing displays the daemon name that crashed and the timestamp of the crash event.

## How to use the feature
Execute the cli command "show core-dump".

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
