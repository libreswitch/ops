# Loopback interface

## Contents

- [Overview ##](#overview-)
- [How to use the feature ##](#how-to-use-the-feature-)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Verifying the configuration](#verifying-the-configuration)
	- [Troubleshooting the configuration](#troubleshooting-the-configuration)
		- [Condition](#condition)
		- [Cause](#cause)
		- [Remedy](#remedy)
- [CLI ##](#cli-)

## Overview
A loopback interface is a virtual interface that supports IPv4 and IPv6 address configurations and remains running until you disable it. Unlike subinterfaces, loopback interfaces are independent of the state of any physical interface. For example, Router IDs are for routing protocols like OSPF.

The loopback interface can be considered stable because once enabled, it will remain running until you shut it down. This makes loopback interfaces ideal for assigning Layer 3 addresses such as IP addresses when you want a single address as a reference that is independent of the status of any physical interfaces in the networking device.

The maximum limit of loopback interfaces is 1024.

## How to use the feature

###Setting up the basic configuration

 1. Create a loopback interface.
 2. Set up the IPv4 or IPv6 addresses.
 3. Enable the loopback interface.

###Verifying the configuration

Display the configured loopback interfaces.

###Troubleshooting the configuration

#### Condition
Unable to ping the loopback interface from an external entity.
#### Cause
An overlapping IP address is set on the loopback interface.
#### Remedy
Check for solutions in the `/var/log/messages` file.
## CLI ##

Click [CLI-TBL](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the loopback interfaces feature.
