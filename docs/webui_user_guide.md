OpenSwitch Web User Interface (UI)
==================

#Contents
- [Overview](#overview)
- [Accesing Web UI](#accesing-web-ui)
- [Screens](#screens)
	- [Login](#login)
	- [Overview](#overview)
		- [System](#system)
		- [Hardware](#hardware)
		- [Features](#features)
		- [Traffic](#traffic)
		- [Logs](#logs)
	- [Interfaces](#interfaces)
	- [VLANs](#vlans)
	- [LAGs](#lags)
	- [ECMP](#ecmp)
	- [Logs](#logs)
	- [Quick Guides](#quick-guides)
	- [Links](#links)
		- [REST API](#rest-api)
		- [OpenSwitch.net](#openswitchnet)


# Overview
The OpenSwitch web UI provides an easy-to-see visual representation displaying the state of the switch. Easy to use view and configuration screens help the user to understand and configure complex features.

# Accesing Web UI
To access the web UI, bring up a web browser (Google Chrome preferred) and enter the IP address of the switch management interface.

# Screens


## Login
When accessing the switch web UI, the first screen that appears is the login screen. The login is tied to a user account that has been added to the switch via the CLI `useradd` command.

## Overview
The Overview screen displays important information and statistics about the switch.

### System
The system panel includes information about the switch, such as:
- the product name
- serial number
- vendor
- version
- base MAC address

### Hardware
The hardware panel shows the status of:
- the power supplies
- temperatures
- fans

### Features
The features panel includes:
- a listing of the switch features and their current state (enabled or disabled)
- number of VLANs configured on the switch
- number of interfaces on the switch
- the maximum transmission unit (MTU)

### Traffic
The traffic panel displays the ports with the top utilization (transmit or receive). The list automatically sorts, moving the port with the top utliization percentage to the top. Clicking the graph icon at the top of the gauge takes you to the Interfaces Monitor screen, displaying details for the top interface.

### Logs
The logs panel displays the last system log messages.

## Interfaces
The interface screen displays the box graphic of the switch, interface table with search option.
On clicking any row in the interface table/click on any port on the box graphic should shoot out interface details panel. This interface details panel has information about that interface, LLDP Port and Statistics.

This interface details panel has general information about the interface configuration and statistics. In addition, LLDP neighbor information and statistics are provided. The information in the interface details panel can be used to help understand the interface configuration and health as well as provide troubleshooting information via the LLDP "map" of directly connected devices.

There are two options on the top-right corner of the interface details panel, a pencil icon (edit) and close (X). On clicking the edit/ pencil icon on the top-right corner of the interface details panel, a window slides out from the right where you can change the Admin State “up” and “down” for that particular interface. The X icon is used to close the interface details panel.

## VLANs

## LAGs

## ECMP
The ECMP screen shows ECMP (Equal Cost Multi-Path) status and various load balancing configurations:

- **Status:** Determines whether ECMP is enabled in the system. Default is true

- **Source IP:** Determines whether the source IP participates in the ECMP hash calculation. Default is true.

- **Source Port:**  Determines whether the source TCP/UDP port participates in the ECMP hash calculation. Default is true.

- **Destination IP:** Determines whether the destination IP participates in the ECMP hash calculation. Default is true.

- **Destination Port:** Determines whether the destination TCP/UDP port participates in the ECMP hash calculation. Default is true.

- **Resilience Hashing:** Determines whether the ECMP hashing preserves traffic flows when the ECMP group membership changes. Default is true.



## Logs

## Quick Guides

## Links

### REST API
The Swagger UI link opens a new window/tab in the browser and displays the Swagger UI:  [http://api.openswitch.net/rest/dist/index.html](http://api.openswitch.net/rest/dist/index.html)

### OpenSwitch.net
The OpenSwitch.net link opens a new window/tab in the browser and displays the OpenSwitch website:
[http://openswitch.net](http://openswitch.net)
