# Daemon Coredump  User Guide

## Contents

- [Overview](#overview)
- [How to use this feature](#how-to-use-this-feature)
    - [genericx86-64 Docker platform](#genericx86-64-docker-platform)
    - [Other platforms](#other-platforms)
- [Troubleshooting](#troubleshooting)
- [Configuration](#configuration)
    - [Configuring a genericx86-64 Docker platform](#configuring-a-genericx86-64-docker-platform)
    - [Configuring other platforms](#configuring-other-platforms)
- [CLI](#cli)
- [References](#references)


## Overview
Enable OpenSwitch to generate a core dump file and store sufficient information of the crashed daemon for debugging purposes.

## How to use this feature
When a daemon is crashed it generates a core dump file.

### genericx86-64 Docker platform
Core file generation is controlled by the host machine's sysctl kernel.core_pattern parameter. The
`show cored-dump` and `copy core-dump` commands are not supported for this platform.

### Other platforms
The `show core-dump` command is used to display the core dumps present in the system.

The `copy core-dump` command is used to copy the core dump file to an external tftp/sftp server. Refer to the copy core dump cli document.

## Troubleshooting
Ensure at least 50MB free space for the /var/diagnostic partition .

## Configuration
### Configuring a genericx86-64 Docker platform
In order to get core dump on a genericx86-64 (Docker) platform, setup and configure a core dump handler in the host machine. An example configuration is given below.

#### Example
Configuration
```
sysctl kernel.core_pattern="|/tmp/cdm.sh %e %p %t"
sysctl kernel.core_uses_pid=0
sysctl kernel.core_pipe_limit=4
```

Install the following script in the /tmp/cdm.sh location. Ensure that the root user can execute this script.

```
#!/bin/sh

LIMIT=5    #default maximum limt
ARCHIVED_CORE="/tmp/core"

PROCESS_NAME=$1
PROCESS_PID=$2
TIME_STAMP=$3
CORE_NO=0

TIME_STAMP_FMT=$(date -d @${TIME_STAMP} "+%Y%m%d.%H%M%S")
if [ ! -d "${ARCHIVED_CORE}/${PROCESS_NAME}" ]; then
    mkdir -p $ARCHIVED_CORE/${PROCESS_NAME} 2> /dev/null
fi

COUNT=$(ls ${ARCHIVED_CORE}/${PROCESS_NAME}/${PROCESS_NAME}*core.tar.gz  2> /dev/null | wc -l)
((COUNT++))

if  (( COUNT >= LIMIT )) ; then
    CORE_NO=$LIMIT
else
    CORE_NO=$COUNT
fi

CORE_DIR=${ARCHIVED_CORE}/${PROCESS_NAME}
CORE_FILE=${CORE_DIR}/${PROCESS_NAME}.${CORE_NO}.${TIME_STAMP_FMT}.core

rm -f  ${CORE_DIR}/${PROCESS_NAME}.${CORE_NO}.*
cat >  ${CORE_FILE}
tar -czvf  ${CORE_FILE}.tar.gz ${CORE_FILE}
if [ $? -eq 0 ] ; then
    rm -f  ${CORE_FILE}
fi

```

#### Configuring other platforms
Core dump works by default; no configuration is required.

## CLI
Use the `show core-dump` command to check daemon core file lists.

Take out a core file to an external tftp/sftp server by using the `copy core-dump` command.

## References
* [Daemon coredump design document](daemon_coredump_design.md)
* [Daemon coredump user guide](daemon_coredump_user_guide.md)
