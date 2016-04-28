# Copy Core Dump CLI Guide

 ## Contents

- [Copy an instance of daemon coredump to tftp](#copy-an-instance-of-daemon-coredump-to-tftp)
- [Copy all instances of a corefile for a daemon](#copy-all-instances-of-a-corefile-for-a-daemon)
- [Copy kernel corefile to tftp server](#copy-kernel-corefile-to-tftp-server)
- [Copy one instance of daemon corefile to sftp server](#copy-one-instance-of-daemon-corefile-to-sftp-server)
- [Copy all corefile instances for a daemon to a sftp server](#copy-all-corefile-instances-for-a-daemon-to-a-sftp-server)
- [Copy kernel corefile to sftp srver](#copy-kernel-corefile-to-sftp-srver)
- [Copy coredump help string](#copy-coredump-help-string)
- [References](#references)

### Copy an instance of daemon coredump to tftp

#### Syntax
```
copy core-dump  <DAEMONNAME> instance-id <INSTANCE ID>  tftp  <TFTP SERVER IPIV4 ADDRESS /HOST NAME> [FILENAME]
```

#### Description
This command copies only one instance of the coredump daemon file to the destination tftp server. The destination filename is an optional parameter. If the destination file name (optional) is not provided, the source file name is used as the destination file name.

#### Authority
The root and netop users can copy corefiles to any external tftp or sftp server from the switch.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------|---------------------------------------|
| **daemon name** | Required | string |  Daemon name |
| **instance id** | Required | <1-65535> | Instance id of core file |
| **tftp server address** | Required | string | Host name of TFTP server |
| **file name** | Optional | string  | Destination file name |



#### Examples
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
switch# copy core-dump ops-vland instance-id 439  tftp 10.0.12.161 ops-vland.xz
copying ...
Sent 109188 bytes in 0.1 seconds
switch#
```

If there are no core dumps present with a given instance, then the following information appears:
`No coredump found for daemon <daemon name>`
```
switch# copy core-dump ops-vland instance-id 567  tftp 10.0.12.161 ops-vland.xz
No coredump found for daemon ops-vland with instance 567
switch#
```

### Copy all instances of a corefile for a daemon

#### Syntax
```
copy core-dump <DAEMONNAME>  tftp <TFTP SERVER IPV4 ADDRESS / HOSTNAME >
```

#### Description
This command copies all of the corefile instances for a daemon to the destination tftp server.

#### Authority
The root and netop users can copy corefiles to any external tftp or sftp server from the switch.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------|---------------------------------------|
| **daemon name** | Required | string |  Daemon name |
| **tftp server address** | Required | string | Host name of TFTP server |


#### Examples

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
switch# copy core-dump ops-vland tftp 10.0.12.161
copying ...
Sent 109188 bytes in 0.1 seconds
copying ...
Sent 109044 bytes in 0.0 seconds
switch#
```

If there are no core dumps files present, then the following information appears:

```
switch# copy core-dump ops-lldpd  tftp 10.0.12.161
No coredump found for daemon ops-lldpd
switch#
```


### Copy kernel corefile to tftp server

#### Syntax
```
copy core-dump kernel tftp  <TFTP SERVER IPV4 ADDRESS / HOST NAME > [FILENAME]

```

#### Description
This command copies the daemon coredump to the destination sftp server. You can specify the destination filename by specifying in the command.

#### Authority
The root and netop users can copy corefiles to any external tftp or sftp server from the switch.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------|---------------------------------------|
| **tftp server address** | Required | string | Host name of TFTP server |
| **file name** | Optional | string  | Destination file name |




#### Examples

```
switch# show core-dump
======================================================================================
Daemon Name         | Instance ID | Crash Reason                  | Timestamp
======================================================================================
ops-vland             439           Aborted                        2016-04-26 18:05:28
ops-vland             410           Aborted                        2016-04-26 18:08:59
kernel                                                             2016-04-26 18:04:20
======================================================================================
Total number of core dumps : 3
======================================================================================
switch#
switch#
switch# copy core-dump kernel
sftp  tftp
switch# copy core-dump kernel
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump kernel tftp
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump kernel tftp 10.0.12.161
  <cr>
  [FILENAME]  Specify destination file name

switch# copy core-dump kernel tftp   10.0.12.161
copying ...
Sent 30955484 bytes in 19.6 seconds
switch#

```

If there are no kernel corefiles, then the following information appears:
`No coredump found for kernel`

```
switch#  copy core-dump kernel tftp 10.0.12.161
No coredump found for kernel
switch#
```

### Copy one instance of daemon corefile to sftp server

#### Syntax
```
copy core-dump <DAEMONNAME> instance-id <INSTANCE ID> sftp <USERNAME> <SFTP SERVER IPV4/HOST NAME> [FILENAME]
```

#### Description
This command copies the daemon coredump to the destination sftp server. You can specify the destination filename. The destination filename is optional parameter. If you have not specified the file name, then it saves as a source file name.

#### Authority
The root and netop users can copy corefiles to any external tftp or sftp server from the switch.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------|---------------------------------------|
| **daemon name** | Required | string |  Daemon name |
| **instance id** | Required | <1-65535> | Instance id of core file |
| **sftp server address** | Required | string | Host name of SFTP server |
| **user name** | Required | string |  User name |
| **file name** | Optional | string  | Destination file name |


#### Examples

```
switch#copy core-dump ops-vland instance-id 410 sftp naiksat 10.0.12.161 ops-vland.xz
copying ...
naiksat@10.0.12.161's password:
Connected to 10.0.12.161.
sftp> put /var/diagnostics/coredump/core.ops-vland.0.a6f6c4b58aa5467ba57d7f9492afa10f.410.1461694139000000.xz ops-vland.xz
Uploading /var/diagnostics/coredump/core.ops-vland.0.a6f6c4b58aa5467ba57d7f9492afa10f.410.1461694139000000.xz to /users/naiksat/ops-vland.xz
/var/diagnostics/coredump/core.ops-vland.0.a6 100%  106KB 106.5KB/s   00:00
switch#
```

If there are no core dumps to present, the following information appears:

```
copy core-dump ops-vland instance-id 410 sftp naiksat 10.0.12.161 ops-vland.xz
No coredump found for daemon ops-vland with instance 410
```

### Copy all corefile instances for a daemon to a sftp server

#### Syntax
```
copy core-dump < DAEMON NAME>  sftp <USERNAME> <SFTP SERVER ADDRESS>  [DESTINATION FILE NAME]
```

#### Description
This command copies all instance of a daemon coredump to the destination sftp server. You can specify the destination file name.
If you have not specified the file name then it saves as a source file name.

#### Authority
The root and netop users can copy corefiles to any external tftp or sftp server from the switch.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------|---------------------------------------|
| **daemon name** | Required | string |  Daemon name |
| **instance id** | Required | <1-65535> | Instance id of core file |
| **sftp server address** | Required | string | Host name of SFTP server |
| **file name** | Optional | string  | Destination file name |

#### Examples

```
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

```

If there are no core dumps to present, the following information appears:

```
switch# copy core-dump ops-fand  sftp naiksat 10.0.12.161
No coredump found for daemon ops-fand
switch#

```

### Copy kernel corefile to sftp srver

#### Syntax
```
copy core-dump kernel sftp <USERNAME>  <SFTP SERVER IP>  [ DESTINATION FILE NAME ]
```
#### Description
This command copies the kernel corefile to the destination sftp server. You can specify the destination file name. If you have not specified a file name then it saves as a source file name.

#### Authority
The root and netop users can copy corefiles to any external tftp or sftp server from the switch.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------|---------------------------------------|
| **sftp server address** | Required | string | Host name of SFTP server |
| **user name** | Required | string |  User name |
| **file name** | Optional | string  | Destination file name |


#### Examples

```
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

If there are no core dumps to present, the following information appears:
`No coredump found for kernel`
```
switch# copy core-dump kernel sftp naiksat 10.0.12.161 kernelcore.tar.gz
No coredump found for kernel
switch#
```

### Copy coredump help string
```
switch# copy
  core-dump       Copy daemon or kernel coredump
  running-config  Copy from current system running configuration
  sftp            Copy data from an SFTP server
  startup-config  Copy from startup configuration
switch# copy core-dump
  DAEMON_NAME  Specify daemon-name
  kernel       Copy kernel coredump
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand instance-id
  INSTANCE_ID  Specify coredump instance ID
switch# copy core-dump ops-fand instance-id 123
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump ops-fand instance-id 123 tftp
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump ops-fand instance-id 123 tftp 1.2.3.4
  <cr>
  [FILE_NAME]  Specify destination file name
switch# copy core-dump ops-fand instance-id 123 tftp 1.2.3.4 abc.xz
  <cr>
switch# copy core-dump ops-fand instance-id 123 tftp 1.2.3.4 ops-fand.xz
  <cr>
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand tftp
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump ops-fand tftp 1.2.3.4
  <cr>
switch# copy core-dump kernel
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump kernel tftp
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump kernel tftp 1.2.3.4
  <cr>
  [FILENAME]  Specify destination file name
switch# copy core-dump kernel tftp 1.2.3.4 kernel.tar.gz
  <cr>
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand instance-id 123
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump ops-fand instance-id 123 sftp
  USERNAME  Specify user name of sshd server
switch# copy core-dump ops-fand instance-id 123 sftp naiksat
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch#
switch# copy core-dump ops-fand instance-id 123 sftp naiksat 1.2.3.4
  <cr>
  [FILE_NAME]  Specify destination file name
switch# copy core-dump ops-fand instance-id 123 sftp naiksat 1.2.3.4 ops-fand.tar.gz

switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand
  instance-id  Coredump instance ID
  sftp         Copy coredump to sftp server
  tftp         Copy coredump to tftp server
switch# copy core-dump ops-fand sftp
  USERNAME  Specify user name of sshd server
switch# copy core-dump ops-fand sftp naiksat
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump ops-fand sftp naiksat 1.2.3.4
  <cr>
switch# copy core-dump
  DAEMON_NAME  Specify daemon-name
  kernel       Copy kernel coredump
switch# copy core-dump kernel
  sftp  Copy coredump to sftp server
  tftp  Copy coredump to tftp server
switch# copy core-dump kernel sftp
  USERNAME  Specify user name of sshd server
switch# copy core-dump kernel sftp naiksat
  A.B.C.D  Specify server IP
  WORD     Specify server name
switch# copy core-dump kernel sftp naiksat 1.2.3.4
  <cr>
  [FILENAME]  Specify destination file name
switch# copy core-dump kernel sftp naiksat 1.2.3.4 kernel.tar.gz
  <cr>

```

## References
* [ Copy core-dump commands ]  copy_core-dump_cli_guide.md
* [ Copy core-dump user guide ] copy_core-dump_user_guide.md
* [ Copy core-dump design  ]  copy_core-dump_design_doc.md
