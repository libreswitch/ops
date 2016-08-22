OpenSwitch Web User Interface (UI)
==================

# Contents
- [Overview](#overview)
- [Accessing web UI](#accessing-web-ui)
- [Screens](#screens)
	- [Login](#login)
	- [Overview](#overview)
		- [System](#system)
		- [General](#general)
		- [Hardware](#hardware)
		- [Top Interface Utilization panel](#top-interface-utilization-panel)
		- [Log](#log)
	- [Interfaces](#interfaces)
	- [Interface Details panel](#interface-details-panel)
		- [Edit icon (wrench)](#edit-icon-wrench)
		- [Edit panel](#edit-panel)
		- [Split/Unsplit option](#splitunsplit-option)
	- [LAGs](#lags)
		- [Adding LAGs](#adding-lags)
			- [ID & Interfaces](#id-interfaces)
			- [Adding an interface](#adding-an-interface)
			- [Removing an interface](#removing-an-interface)
			- [Attributes](#attributes)
		- [Remove LAG](#remove-lag)
		- [Edit LAG](#edit-lag)
	- [ECMP](#ecmp)
		- [Editing ECMP](#editing-ecmp)
	- [Log](#log)
	- [Quick Guides](#quick-guides)
	- [Links](#links)
		- [REST API](#rest-api)
		- [OpenSwitch.net](#openswitchnet)
	- [User](#user)
		- [Logout](#logout)
		- [Change Password](#change-password)


# Overview
The OpenSwitch web UI provides an easy-to-see visual representation displaying the state of the switch. Easy-to-use view and configuration screens help the user to understand and configure complex features.

# Accessing the web UI
To access the web UI, open a web browser (Google Chrome preferred) and enter the IP address of the switch management interface.

The web server (REST daemon) is disabled by default.  Refer to the REST API user guide for information on how to enable the REST daemon.

# Screens


## Login
When accessing the switch web UI, the user first sees the login screen. The login is tied to a user account that has been added to the switch via the CLI `useradd` command.

## Overview
The Overview screen displays important information and statistics about the switch.

### System
The system panel includes information about the switch, such as:
- the product name
- serial number
- vendor
- version
- ONIE Version
- base MAC address

### General
The features panel includes:
- a listing of the switch features and their current state (enabled or disabled)
- number of VLANs configured on the switch
- number of interfaces on the switch
- the maximum transmission unit (MTU)
- the maximum interface speed

### Hardware
The hardware panel shows the status of:
- the power supplies
- temperatures
- fans

### Top Interface Utilization panel
The Top Interface Utilization panel displays the ports with the top utilization (either through transmitting or receiving data). The list automatically sorts, moving the port with the top utilization percentage to the top. Clicking the graph icon at the top of the gauge takes you to the Interfaces Monitor screen, which displays details for the top interface.

### Log
The log panel displays the last system log messages.

## Interfaces
The Interfaces screen displays the box graphic of the switch, interface table with details, edit and search options. The Details option is selected by default. The total number of rows in the table is displayed in the top-left corner of the table. The total dynamically updates by showing the number of results found by the search.

If you select an interface in the table and the Details option is selected, additional details about the selected interface are displayed in the Interface Details panel on the right side of the screen.

## Interface Details panel
The Interface Details panel provides configuration and health information for an interface, in addition to providing troubleshooting information via the LLDP “map” of directly connected devices.

The Interface Details panel has three tabs:
- **General:** The General tab has information about the interface configuration.
- **Statistics:** All port statistics are present in the Statistics tab.
- **LLDP:** LLDP neighbor information and statistics are provided under the LLDP tab.

If an interface can be split, the split children and split parent details are displayed in the Interface Details panel.

To close the Interface Details panel, click the close (X) icon in the top-right corner.

### Edit icon (wrench)
The edit icon (wrench) on the Interfaces screen is enabled when you select a row on the table or click a port on the box graphic.

### Edit panel
When you click the edit icon, the Edit panel appears with the current:
* admin state
* auto negotiation
* duplex and flow control of the interface, which can be configured

Click the “OK” button in the bottom of the Edit panel. Click the Close (X) icon at the top-right corner of the Edit panel to close the panel.

### Split/Unsplit option
When editing a split parent interface, the Split/Unsplit option becomes available. If the split parent interface is configured split from here, the table updates to show all the split interfaces of that parent. The split parent cannot be configured until it is unsplit.

## LAGs
The Link Aggregation (LAG) screen displays the LAG table with details, edit, add, delete and search options. The Details panel is displayed by first selecting a LAG in the list number and then selecting the Details option. The number of LAGs are displayed in the top-left corner of the table. The total updates dynamically by showing the number of results found by the search.

### Adding LAGs
Click the plus sign (+) to add a LAG. The software displays the LAG add panel with 2 tabs:
* ID & Interfaces
* Attributes

#### ID & Interfaces
The ID & Interfaces tab has an input box for the LAG ID to be created. The list of available LAG ID ranges is shown. There are two icons plus (+) and minus (-) which increment and decrement the LAG ID.
The software provides two list for interfaces: available and those currently part of that LAG. The boxes next to "Available" and the LAG name select and deselect everything in the list.

#### Adding an interface
To add an interface:
1. Select the interface ID from the Available list.
2. Click the greater than sign (>).

#### Removing an interface
An interface can be removed from the LAG by selecting it and clicking the less than sign (<).

#### Attributes
LAG Attributes includes the following configuration options:
- **Aggregation Mode:** Aggregation Mode can be active, passive, or off (static LAG). The default setting is off.
- **Rate:** Rate at which LACP control packets are sent to an LACP-supported interface to detect status and fault in the LAG:
  - **Fast LACP:** LACP packets are sent every second.
  - **Slow LACP (default):** LACP packets are sent every 30 seconds.
- **Fallback:** Fallback is true or false (default).
- **Hash:** Hashing is used to determine how the LAG chooses which interface to forward traffic:
 - **L2 Src/Dst (source/destination):** Layer 2 hashing mode.
 - **L3 Src/Dst (default):** Layer 3 hashing mode.
 - **L4 Src/Dst:** Layer 4 hashing mode.

### Remove LAG
The currently selected LAG can be removed by clicking the minus sign (-).

### Edit LAG
To change the information of an existing LAG, select the LAG and click the edit icon (wrench). The same dialog as Add LAG is displayed.


## ECMP
The ECMP screen shows ECMP (Equal Cost Multi-Path) status and various load balancing configurations:

- **Status:** Determines whether ECMP is enabled in the system. Default is true

- **Source IP:** Determines whether the source IP participates in the ECMP hash calculation. Default is true.

- **Source Port:**  Determines whether the source TCP/UDP port participates in the ECMP hash calculation. Default is true.

- **Destination IP:** Determines whether the destination IP participates in the ECMP hash calculation. Default is true.

- **Destination Port:** Determines whether the destination TCP/UDP port participates in the ECMP hash calculation. Default is true.

- **Resilience Hashing:** Determines whether the ECMP hashing preserves traffic flows when the ECMP group membership changes. Default is true.

### Editing ECMP
To edit the ECMP configuration, click the wrench icon.


## Log
The Log screen displays a table of the switch logs. By default the only the critical logs from the last hour are displayed. The fields displayed are:
- Time
- Severity
- Identifier
- Category
- Message

The Log screen provides drop-down lists for severity (Critical Only, Critical & Warning, and All) and for time (Last Hour, Last 24 Hours, and Last 7 Days). When selecting an option in the drop-down list, the software requests the switch to pull the latest logs matching the selected criteria.

In the upper-right corner of the Log screen is a search box. The search feature filters the list of logs to those matching the search criteria. All fields are used when searching.

If the length of the message field is too big to fit, the entire message is displayed when you mouse over the message field.

## Quick Guides
Quick Guides provide online help for some of the web UI features.

## Links

### REST API
The Swagger UI link opens a new window/tab in the browser and displays the Swagger UI:  [http://api.openswitch.net/rest/dist/index.html](http://api.openswitch.net/rest/dist/index.html)

### OpenSwitch.net
The OpenSwitch.net link opens a new window/tab in the browser and displays the OpenSwitch website:
[http://openswitch.net](http://openswitch.net)

## User
The user name of the account currently logged in is displayed at the bottom-left corner of the screen. When you click the user name, a pop-up menu with two options is displayed:
- Logout
- Change Password

### Logout
It logs out the current user, and returns the user to the login page.

### Change Password
The Change Password feature prompts the user for the old password, the new password and the confirmed new password.
