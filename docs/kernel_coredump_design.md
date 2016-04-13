# High Level Design of Kernel Core Dump

## Contents

- [Overview](#overview)
- [Responsibilities](#responsibilities)
- [Design choices](#design-choices)
- [Internal structure](#internal-structure)
- [Configuration](#configuration)
- [How kernel vmcore is generated](#how-kernel-vmcore-is-generated)
- [Supported platforms](#supported-platforms)
- [References](#references)

## Overview

An available kernel core dump is benefitial for analysing and identifying root cause issues related to kernel configuration, kernel code, kernel exceptions, and device driver code and exceptions.

When the running kernel crashes, it is not in a stable state to store and process its own core dump. Because of this, a utility like makedumpfile is used to dump the core dump of the crashed kernel.

Kdump is a standard Linux mechanism to dump machine memory content when a kernel crash occurs. Kdump internally uses a collection of tools, like kexec and makedumpfile, to perform the core dump.  In order to perform this task, kdump needs a stable running kernel.  Kdump utilizes two kernels: a primary kernel and a secondary kernel. The primary kernel is the kernel that is booted with special kdump-specific flags. The secondary kernel is the kernel that takes control if the primary kernel crashes. The secondary kernel's main objective is to dump the kernel core dump and reboot the system as early as possible. In the boot option of the system kernel, an amount of physical memory is specified/reserved where the dump-capture kernel is loaded. The boot script of the system kernel is configured to load the secondary kernel in advance because at the moment a crash happens there is no way to read any data from the disk to load the dump capture kernel.

Once a kernel crash happens, the kernel crash handler uses the kexec mechanism to boot the dump capture kernel. Note that primary kernel memory is untouched and is accessible from the dump capture kernel, as seen at the moment of the crash. Once a dump capture kernel is booted, the kdump script makes use of a tool like makedumpfile, and dumps the kernel core dump.

## Responsibilities

The primary goal of the kernel core dump module is to generate and store sufficient information of the crashed kernel for debugging purposes.

## Design choices

The design choices made for the kernel core dump module are:
- The core file is compressed and archived with the build/release information file(/etc/os-release ).
- The core file is stored in the /var/diagnostics/coredump/ directory.
- The default format to capture vmcore is ELF. The kernel core dump module supports ELF and KDUMP formats to capture vmcore. Format changes are done by changing the kdump config file (/etc/kdump.conf).
- The primary and secondary requirements for compression are time and memory. If the system kernel crashes, the goal is to dump the core dump and bring the system back to a stable state as soon as possible. GZ compression is used to compress the core dump since it provides compression in the least amount of time and with the best compression ratio.

## Internal structure

```ditaa

+-------------------+
|Primary Kernel     | <----------------------------------------------------+
+-------+-----------+                                                      |
        |                          +----------------------------------+    |
        |                 +------> |                                  |    |
        |                 |        |makedumpfile                      |    |
+-------v-----------+     |        |copy from  /proc/vmcore(RAM)      |    |
|Kernel Panic       |     |        |to <flash>/vmcore (FLASH)         |    |
+-------+-----------+     |        |                                  |    |
        |                 |        +---------------+------------------+    |
        |                 |                        |                       |
        |                 |        +---------------v------------------+    |
+-------v-----------+     |        |/etc/systemd/kdump                |    |
|Panic Handler      |     |        |tar archive vmcore                |    |
+-------+-----------+     |        |   vmcore-dmesg                   |    |
        |                 |        |tar.gz compress all               |    |
        |                 |        |                                  |    |
        |                 |        +---------------+------------------+    |
+-------v-----------+     |                        |                       |
|kexec              |     |                        |                       |
+-------+-----------+     |                        |                       |
        |                 |        +---------------v------------------+    |
        |                 |        | Reboot                           +----+
        |                 |        +----------------------------------+
+-------v-----------+     |
|Secondary Kernel   +-----+
+-------------------+

```

## Configuration

Enabling this feature on OpenSwitch requires the following recommended configuration changes in multiple config files, which are given below.

1.  Build the kernel with enabling debug flags.
         make menuconfig=>
         CONFIG_LOCALVERSION=""
         CONFIG_PHYSICAL_START=0x1000000
         CONFIG_SYSFS=y
         CONFIG_RELOCATABLE=y
         CONFIG_INITRAMFS_SOURCE=""
         CONFIG_KEXEC=y
         CONFIG_DEBUG_INFO=y
         CONFIG_CRASH_DUMP=y

2.  Configure kdump parameters.
        /etc/kdump.conf
        path /var/core
        for ELF format:
        core_collector makedumpfile -E -f --message-level 1 -d 31
        for KDUMP format:
        core_collector makedumpfile -c --message-level 1 -d 31

3.  Configure the boot loader.
        boot kernel with parameter  "crashkernel=128M@0M"


## How kernel vmcore is generated
When OpenSwitch starts, the boot loader specifies the crashkernel parameter and systemd starts the kdump service. The crashkernel parameter is used to reserve memory for the secondary kernel. The kdump service launches kexec with the required parameters. When an exception or NULL dereference occurs, kernel panic is invoked.  The panic handler launches the secondary kernel using kexec with isolated and reserved memory space. The secondary kernel launches the kdump service.  The primary kernel RAM is accessible by reading /proc/vmcore. The kdump service checks for /proc/vmcore.

Create vmcore in ELF or KDUMP format using the makedumpfile utility. The vmcore-dmesg utility generates dmesg from vmcore. After makedumpfile finishes these jobs, the vmcore-dmesg secondary kernel reboots and the boot loader launches the primary kernel. The primary kernel launches the kdump service and compresses the vmcore core.

## Supported platforms
Following platforms are supported for this feature:
- as5712
- as6712

## References
* [Kernel coredump design document](kernel_coredump_design.md)
* [Kernel coredump test document](kernel_coredump_test.md)
* [Kernel coredump user guide](kernel_coredump_user_guide.md)
* [Reference Crash tool white paper](https://people.redhat.com/anderson/crash_whitepaper/)
