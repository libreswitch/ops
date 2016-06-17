# Autoprovisioning

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
    - [Setting up the basic configuration](#setting-up-the-basic-configuration)
    - [Verifying the configuration](#verifying-the-configuration)
    - [Writing autoprovisioning script](#writing-autoprovisioning-script)
        - [Major Executables](#major-executables)
        - [Examples](#examples)
            - [VTYSH](#vtysh)
            - [WGET](#wget)
            - [LOGGER](#logger)
        - [Sample script file](#sample-script-file)
    - [Troubleshooting the configuration](#troubleshooting-the-configuration)
        - [Condition](#condition)
        - [Cause](#cause)
- [CLI](#cli)
- [Related features](#related-features)

## Overview ##
Autoprovisioning (a.k.a Zero Touch Provisioning - ZTP)  is a feature that enables automatic provisioning of switch when it is deployed. Using a DHCP option advertised by DHCP server in the setup, the switch downloads a provisioning script and executes it. The provisioning script can do many things, such as new management users, downloading `ssh` keys, installing a server certificate, etc. This feature is mainly used to download `ssh` keys and add user ids to the switch enabling key based authentication of management users.

## How to use the feature ##
###Setting up the basic configuration

The feature is enabled by default and cannot be turned off through CLI. To disable the autoprovisioning feature, configure the DHCP server to NOT send option 239 in the DHCP reply/ack messages.


###Verifying the configuration

Not applicable.

###Writing autoprovisioning script
- Shell, Perl and Python scripts are supported as auto-provisioning script.
- It is assumed that the first line of the script contains entries like `#!/bin/sh` to distinguish between a shell, perl and python scripts.
- The provisioning script must contain a line `OPS-PROVISIONING` as a comment. This is for a very rudimentary validation that we got a valid provisioning script.
- The script is executed on the Linux shell(Bourne shell) of the switch.

#### Major Executables
In the script the following executables can be used to configure CLI commands in the switch(VTYSH), to download other files from outside the switch(WGET) and to log the appropriate ZTP messages(LOGGER).
```
VTYSH=/usr/bin/vtysh
WGET=/usr/bin/wget
LOGGER=/usr/bin/logger
```
Other usual shell commands which are available in OpenSwitch can also be used in an autoprovisioning script.

#### Examples
Suppose we want to configure the below CLI commands and copy some SSH Public keys from outside on to the  switch:
```
vlan 2
    no shutdown
interface 3
    no shutdown
    no routing
    vlan trunk native 1
    vlan trunk allowed 2
```
##### VTYSH
- CLI commands can be configured with the executable `/usr/bin/vtysh`.
- The arguments to this executable are the exact CLI commands in a correct order with a tag of `-c` preceding each command.
- To configure the above CLI commands in switch, execute the below commands in switch's Linux shell:
```
root@switch:~# VTYSH=/usr/bin/vtysh
root@switch:~# $VTYSH -c "configure terminal" -c "vlan 2" -c "no shutdown"  -c "interface 3" -c "no shutdown" -c "no routing" -c "vlan trunk allowed 2" -c "exit"
```
- The above commands can also be incorportated in an autoprovisioning [shell script](#sample-script-file) the example of which is given below.
- Since autoprovisioning script will get executed on the Linux shell so automating a script to read the CLI configuration from a separately downloaded config file and run the CLI commands like above is fairly easy task.

##### WGET
- Use `/usr/bin/wget` to download config file/SSH keys.
- Shell commands like wget can be used to download any type of file into switch.
```
$WGET <Link to config/SSH key file> -O <File-name>
```

##### LOGGER
- Logging events with `/usr/bin/logger`:
```
$LOGGER -i "MESSAGE that needs to be documented"
```

#### Sample script file
```
#!/bin/sh

# OPS-PROVISIONING
# Sample auto-provisioning script for OpenSwitch.

# executable files used by this script
VTYSH=/usr/bin/vtysh
WGET=/usr/bin/wget
LOGGER=/usr/bin/logger

# Run vtysh command on switch Linux shell
$VTYSH -c "configure terminal" -c "vlan 2" -c "no shutdown"  -c "interface 3" -c "no shutdown" -c "no routing" -c "vlan trunk allowed 2" -c "exit"

# Log the events
$LOGGER -i "Configured vlan 2"
$LOGGER -i "Configured interface 3 with vlan trunk 2"

# Create a new user or copy SSH keys to an existing user home directory
# Download SSH keys from outside the switch and save it for username "netop"
$WGET http://192.168.1.1/sshkeys.txt -O /home/netop/.ssh/authorized_keys
[ $? -eq 0 ] && $LOGGER -i "Copied and saved authorized SSH keys for netop"

<---- Complete the script to read configuration file and apply any other commands on switch using VTYSH ---->
```

###Troubleshooting the configuration

#### Condition
Autoprovisioning is not performed.
#### Cause
- The DHCP option 239 not configured on the DHCP server.

Verify whether DHCP server is correctly configured.

- The URL in the DHCP option 239 is not valid.

The URL can be seen in the output of "show autoprovisioning" command. If this URL is incorrect, autoprovisioning does not happen.

- Provisioning script does not contain the line `OPS-PROVISIONING`.

Please verify the provisioning script.
## CLI ##
Click [ here](/documents/user/autoprovision_CLI) for the CLI commands related to the named feature.

## Related features ##
None.
