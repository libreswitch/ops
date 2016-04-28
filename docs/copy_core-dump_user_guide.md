# Copy Core Dump User Guide

## Contents

- [Copy Core Dump User Guide](#copy-core-dump-user-guide)
	- [Contents](#contents)
	- [Overview](#overview)
	- [How to use the feature](#how-to-use-the-feature)
	- [Examples](#examples)
	- [References](#references)


## Overview
This command copies a daemon or a kernel corefile to the tftp or sftp server.

## How to use the feature
Use the following procedure to copy the daemon core to a TFTP server:
1. Execute the command sequence `copy core-dump  <DAEMONNAME> instance-id <INSTANCE ID>  tftp  <TFTP SERVER IPV4 ADDRESS /HOST NAME> [FILENAME]`
2. Execute the command sequence `copy core-dump <DAEMONNAME>  tftp <TFTP SERVER IPV4 ADDRESS / HOSTNAME >`

Use the following procedure to copy the daemon core to a sftp server:
1. Execute the command sequence `copy core-dump <DAEMONNAME> instance-id <INSTANCE ID> sftp <USERNAME> <SFTP SERVER IPV4/HOST NAME> [FILENAME ]`.
2. Execute the command sequence `copy core-dump < DAEMON NAME>  sftp <USERNAME> <SFTP SERVER ADDRESS>  [DESTINATION FILE NAME]`.

Use the following procedure to copy the kernel core:
1. Execute the command sequence `copy core-dump kernel tftp  <TFTP SERVER IPV4 ADDRESS / HOST NAME > [ DESTINATION FILE NAME]`.
2. Execute the command sequence `copy core-dump kernel sftp <USERNAME>  <SFTP SERVER IP>  [ DESTINATION FILE NAME]`.



## Examples
```
switch# show  core-dump
======================================================================================
Daemon Name         | Instance ID | Crash Reason                  | Timestamp
======================================================================================
ops-vland             439           Aborted                        2016-04-26 18:05:28
ops-vland             410           Aborted                        2016-04-26 18:08:59
======================================================================================
Total number of core dumps : 2
======================================================================================
switch#

switch# copy core-dump ops-vland instance-id 439 tftp 10.0.12.161 ops-vland.xz
copying ...
Sent 109188 bytes in 0.1 seconds
switch#

switch# copy core-dump ops-vland tftp 10.0.12.161
copying ...
Sent 109188 bytes in 0.1 seconds
copying ...
Sent 109044 bytes in 0.0 seconds
switch#

switch# copy core-dump kernel tftp   10.0.12.161
copying ...
Sent 30955484 bytes in 19.6 seconds
switch#

switch#copy core-dump ops-vland instance-id 410 sftp naiksat 10.0.12.161 ops-vland.xz
copying ...
naiksat@10.0.12.161's password:
Connected to 10.0.12.161.
sftp> put /var/diagnostics/coredump/core.ops-vland.0.a6f6c4b58aa5467ba57d7f9492afa10f.410.1461694139000000.xz ops-vland.xz
Uploading /var/diagnostics/coredump/core.ops-vland.0.a6f6c4b58aa5467ba57d7f9492afa10f.410.1461694139000000.xz to /users/naiksat/ops-vland.xz
/var/diagnostics/coredump/core.ops-vland.0.a6 100%  106KB 106.5KB/s   00:00
switch#

switch# copy core-dump ops-switchd sftp naiksat 10.0.12.161
copying ...
The authenticity of host '10.0.12.161 (10.0.12.161)' can't be established.
ECDSA key fingerprint is SHA256:uWeyXm2j6VkDfCitlyz/P+xGgZW9YYw5GnDOsEgVHeU.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.0.12.161' (ECDSA) to the list of known hosts.
naiksat@10.0.12.161's password:
Connected to 10.0.12.161.
sftp> put /var/diagnostics/coredump/core.ops-switchd.0.1bddabce7ee5468884cc012b1d7c2ab0.361.1461694266000000.xz core.ops-switchd.0.1bddabce7ee5468884cc012b1d7c2ab0.361.1461694266000000.xz
Uploading /var/diagnostics/coredump/core.ops-switchd.0.1bddabce7ee5468884cc012b1d7c2ab0.361.1461694266000000.xz to /users/naiksat/core.ops-switchd.0.1bddabce7ee5468884cc012b1d7c2ab0.361.1461694266000000.xz
/var/diagnostics/coredump/core.ops-switchd.0. 100% 4531KB   4.4MB/s   00:00
switch#

switch# copy core-dump kernel sftp naiksat 10.0.12.161 kernelcore.tar.gz
copying ...
naiksat@10.0.12.161's password:
Connected to 10.0.12.161.
sftp> put /var/diagnostics/coredump/kernel-core/vmcore.20160426.180420.tar.gz
kernelcore.tar.gz
Uploading /var/diagnostics/coredump/kernel-core/vmcore.20160426.180420.tar.gz to
/users/naiksat/kernelcore.tar.gz
/var/diagnostics/coredump/kernel-core/vmcore. 100%   44MB  43.5MB/s   00:01
switch#
```

## References
* [ Copy core-dump commands ]  copy_core-dump_cli_guide.md
* [ Copy core-dump userguide ] copy_core-dump_user_guide.md
* [ Copy core-dump design  ]  copy_core-dump_design_doc.md
