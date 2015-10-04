# Management Interface
## Table of contents
- [Table of contents](#table-of-contents)
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [How to use the feature](#how-to-use-the-feature)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Setting up the optional configuration](#setting-up-the-optional-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
	- [Troubleshooting the configuration](#troubleshooting-the-configuration)
- [CLI](#cli)
- [Related features](#related-features)

## Overview
The primary goal of the management module is to facilitate the management of the device. It provides the following:

- Device access and configuration

- Event collection for monitoring, analysis, and correlation

- Device and user authentication, authorization, and accounting

- Device time synchronization

- Device image downloading

The device is configured or monitored through the management interface. All management traffic such as device ssh, tftp and so on, goes through the management interface.

## Prerequisites
- A physical interface of the switch designated as the management interface must be specified in the 'image.manifest' hardware description file.

## How to use the feature

### Setting up the basic configuration

 Configure the mode in which the management interface is going to operate. Select one of the following options:
- DHCP mode -- The DHCP Client automatically populates all the management interface parameters.
- Static mode -- The user manually configures the management interface parameters.

### Setting up the optional configuration

 1. Configure the IPv4 or the IPv6 configuration depending on the requirement.
 2. Configure the secondary nameserver if fallback is required.

### Verifying the configuration

 1. Verify the configured values using the `show interface mgmt` command.
 2. Verify the configuration using the `show running-config` command.

### Troubleshooting the configuration
Troubleshoot the device only through the management interface. if there is any problem with the management interface configuration, you may not be able to access the device over the network. Try accessing it over the serial console.
#### Scenario 1
##### Condition
The values configured are not displayed with the show command.
##### Cause
The configured values will not appear in the show command if the configuration fails at the management interface daemon.
##### Remedy
- Check the syslog for error message.
- Check for errors in the daemon using the command `systemctl status mgmt-intf -l`.
- Restart the management interface daemon using the command `systemctl restart mgmt-intf`.

#### Scenario 2
##### Condition
Values configured in the CLI are not configured in the interface.
##### Cause
The management interface daemon could have crashed.
##### Remedy
- Check the syslog for error message.
- Check for errors in the daemon using the command `systemctl status mgmt-intf -l`.
- Restart the management interface daemon using the command `systemctl restart mgmt-intf`.

#### Scenario 3
##### Condition
The mode is dhcp, but no DHCP attributes are populated.
##### Cause
The dhclient might be down.
##### Remedy
- Check the syslog for error message.
- Check for errors in the daemon using the command `systemctl status mgmt-intf -l`.
- Restart the management interface daemon using the command `systemctl restart mgmt-intf`.

#### Scenario 4
##### Condition
The mode is dhcp, but IPv6 attributes are not seen in the `show interface mgmt` command.
##### Cause
Currently IPv6 notifications are not available.
##### Remedy
- The user can start the shell using "start-shell" command and check the IPv6 attributes by running the command `ip addr show`.

## CLI
Click [here-TBL](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the named feature.

## Related features
None.
