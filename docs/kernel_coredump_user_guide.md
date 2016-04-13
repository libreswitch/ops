# Kernel Coredump  User Guide

## Contents

- [Overview](#overview)
- [How to use this feature](#how-to-use-this-feature)
	- [Troubleshooting](#troubleshooting)
	- [Configuration](#configuration)
	- [How to debug vmcore](#how-to-debug-vmcore)
- [Supported platforms](#supported-platforms)
- [CLI](#cli)
- [References](#references)


## Overview
This feature enables the switch to recover itself in case of kernel panic, as well as store the kernel core dump to debug the root cause.

## How to use this feature
In case of kernel panic it will capture vmcore and reboot the switch . You can see existing vmcore file present in switch by vtysh cli command "show croe-dump". You can copy out this core file by using "copy core-dump" cli command to external tftp/sftp server.

### Troubleshooting
Ensure that the /var/diagnostic partition has enough memory (at least 100 MB free space) to store the kernel vmcore.

### Configuration
No need to configure.

### How to debug vmcore
- Check the `show core-dump` command to see the kernel core dump file.
- Use the `copy core-dump` command to take out the kernel core to the build machine where the image was built.
- Uncompress the tar.gz file and extract vmcore.
- Check the file format of vmcore using the `head -1 <path of vmcore>` command.
- For ELF format, launch gdb or crash. (ELF format is supported by gdb and crash.)
     Syntax: `gdb <path of vmlinux> <vmcorepath>`
     Syntax: `crash <path of vmlinux> <vmcorepath>`
     For example (ELF format):
     ```
  gdb  build/tmp/work/as5712-openswitch-linux/linux-ops/3.9.11-r1_as5712/package/boot/vmlinux-3.9.11 <vmcorepath>
  ```
- For KDUMP format, launch crash.
     Syntax: `crash <path of vmlinux> <vmcorepath>`
     For example (KDUMP format):
     ```
  crash build/tmp/work/as5712-openswitch-linux/linux-ops/3.9.11-r1_as5712/package/boot/vmlinux-3.9.11 <vmcorepath>
     ```

## Supported platforms
The following platforms are supported for this feature
- as5712
- as6712

## CLI
You can use the `show core-dump` command to check the last kernel vmcore file.
You can take out the core file using the `copy core-dump` command to the external tftp/sftp server.

## References
* [Kernel coredump design document](kernel_coredump_design.md)
* [Kernel coredump test document](kernel_coredump_test.md)
* [Kernel coredump user guide](kernel_coredump_user_guide.md)
* [Reference Crash tool white paper](https://people.redhat.com/anderson/crash_whitepaper/)
