# High Level Design of Daemon Core Dump

## Contents

- [Overview](#overview)
- [Design choices](#design-choices)
- [How core dumps are generated](#how-core-dumps-are-generated)
- [Core dump handling in Docker](#core-dump-handling-in-docker)
    - [Piping core dumps to a program](#piping-core-dumps-to-a-program)
    - [Revert back to original configuration stored in host machine](#revert-back-to-original-configuration-stored-in-host-machine)
- [References](#references)

## Overview
The primary goal of the daemon coredump module is to generate and store sufficient information of the crashed daemon for debugging purpose.

## Design choices


- Uses the systemd core dump feature to capture and generate the core dump file.
- Generated core dump files are stored in the /var/lib/systemd/coredump folder.
- The /var/lib/systemd/coredump folder is created as a symbolic link to a persistant location in order to store the core dumps persistantly.
- Core dumps are stored in compressed format.

## How core dumps are generated

Whenever a process misbehaves, the kernel generates the appropriate signal and sends it to the process. The process's signal handler mechanism determines whether to core dump or not.  Accordingly, the kernel calls the core dump utility as specified by kernel.core_pattern. This kernel.core_pattern is set to use the systemd helper binary called *systemd-coredump*. This core dump helper utility receives the crashing process's core file, along with additional information such as the process PID, timestamp of the crash, and signal number leading to the core dump. The  systemd core dump utility then compresses and saves the core dump file in the path /var/lib/systemd/coredump. It also adds the following metadata information to the file's extended attributes.

|Key|Value|Example|
|----------------------|
|user.coredump.comm | Process name  | vtysh |
|user.coredump.exe | Program location  | /usr/bin/vtysh |
|user.coredump.pid | Process PID | 4166 |
|user.coredump.signal | Signal number leading to the core dump. | 11 |
|user.coredump.timerstamp | Timestamp of the core dump event. | 1459354952 |

The `show core dump` command uses these extended attributes to extract information about the core dump and displays that information.

```ditaa
                 corefile,           +-----------------------+
     +--------+  crash info    (3)   |                       |
     | Kernel +-------------------------> Systemd coredump   |
     +-+----^-+                      |           +           |
       |    |                        |           |           |
       |    |                        |           v           |
       |    |(2)                     |        compress       |
       |    |                        |           +           |
       |    |                        |           |           |
signal |    | Core file              |           v           |
       |    |                        |     save metadata     |
       |    |                        |                       |
    (1)|    |                        |                       |
       |    |                        +-----------------------+
       |    |
     +-v----+-+
     | Daemon |
     +--------+
```

## Core dump handling in Docker

Where the core dump of a process is running inside the Docker, core dump handling is done by the kernel of the host machine. Core dump handling using systemd mandates that the host machine has systemd installed. The kernel.core_pattern of the host machine might not be configured to use the systemd core dump utility, or the host machine might not have systemd installed. In order to generate core dumps for a switch image running in Docker, use the host machine's core dump handler.

The following step helps configure the host machine to generate a core dump.

### Piping core dumps to a program
Update the kernel.core_pattern variable to reflect the core dump handler of choice.

Example :

```
sysctl kernel.core_pattern="|/tmp/ops_cdm.sh %e %p %t"
```

### Revert back to original configuration stored in host machine
Use the `sysctl --system` command to revert back to the original configuration in the host machine.

## References
* [Daemon core dump design document](daemon_coredump_design.md)
* [Daemon core dump user guide](daemon_coredump_user_guide.md)
