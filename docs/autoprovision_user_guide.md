# Autoprovisioning

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
    - [Setting up the basic configuration](#setting-up-the-basic-configuration)
    - [Verifying the configuration](#verifying-the-configuration)
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

###Troubleshooting the configuration

#### Condition
Autoprovisioning is not performed.
#### Cause
- The DHCP option 239 not configured on the DHCP server.

Verify whether DHCP server is correctly configured.

- Provisioning script does not contain the line `OPS-PROVISIONING`.

Please verify the provisioning script.
## CLI ##
Click [ here](/documents/user/autoprovision_CLI) for the CLI commands related to the named feature.

## Related features ##
None.
