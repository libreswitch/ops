Web User Interface
==================
OpenSwitch Web User Interface (UI)

# Overview
The OpenSwitch web UI provides an easy-to-see visual representation displaying the state of the switch.  Easy to use view and configuration screens help the user understand and configure complex features.

# Accesing Web UI
To access the web UI, bring up a browser (Chrome preferred) and enter the IP address of the switch management interface.

# Screens


##Login
When accessing the switch web UI, the first screen that appears is the login screen.  The login is tied to a user account that has been added to the switch via the CLI `useradd` command.

##General

###Overview
The Overview screen displays important information and statistics about the switch.

####Information
The information panel includes the product name, vendor, version, ONIE version, and base MAC address.   Also listed in the information panel are status indicators for fans (including the total number of fans in parentheses).  The power supplies status shows different states:
- OK
- Input Fault (power supply present but not plugged in)
- Output Fault (power supply present and plugged in, but there is a voltage issue)
- Absent (power supply not present).

####Temperatures
The temperature sensors displays the various sensors.  On initial release, the AS5712 has 3 sensors - front, back, and side.

####CPU Load
The CPU Load gauge displays the current load average on the switch.  This is similar to the `uptime` command in Linux.  Clicking the graph icon at the top of the gauge takes you to the System Monitor screen, displaying details about that gauge.

####Memory
The Memory gauge displays the amount of memory being used by the switch.  Clicking the graph icon at the top of the gauge takes you to the System Monitor screen, displaying details about that gauge.

####Storage
The Storage gauge displays the amount of disk space used by the switch.

####Top Interface Utilization
The Top Interface Utilization panel displays the ports with the top utilization (transmite or receive).  The list automatically sorts, moving the port with the top utliization percentage to the top.  Clicking the graph icon at the top of the gauge takes you to the Interfaces Monitor screen, displaying details for the top interface.

###System Monitor
The System Monitor screen displays live, updating graphs for CPU Load, Memory, and Temperature.

###Management Interface
The Management Interface screen displays the current settings for the Management Interface.  This includes the name, typically `eth0` and Mode `dhcp` or `static`.  If the mode is `static`, the remaining IPv4/IPv6 information displays (address, subnet mask, and gateway).

##Interfaces

###Management
The Interface Management screen displays a graphical view of the switch, along with the list of interfaces.  The box graphic displays the status of the interface for each port.  A green checkmark means the interface is enabled and there is a link.  A red X means that Admin is disabled, and a yellow X means there is no link.  The interface list includes the following:
- Name
- Admin State
- Link State
- Duplex
- Speed
- Connector
- Vendor (of the connector).

###Monitor
The Interface Monitor screen displays a live graph of Rx utilization, Tx utilization, Dropped bytes and Error bytes.  The port being viewed can be changed by clicking the **Select Port** dropdown.  The live graph can be paused and resumed, and the various items being graphed can be turned on or off by clicking the area chart icon next to the statistic type at the top of the graph.

Clicking the line chart icon for each of these statistics changes the graph to a bar chart of just the selected statistic type.

###LAG
The LAG screen displays Link Aggregate Group (i.e. trunk) information configured on the switch.  The top list shows the list of configured LAGs. Clicking one of the LAGs displays the interface information for that LAG in the lower list.

##VLANs

###Management
The VLAN Management screen displays all VLANs configured on the switch, as well as the ports that are part of the VLANs. Clicking the checkbox for a VLAN displays the port membership for that VLAN on the box graphic. Up to 4 VLANs can be selected at the same time.

##Links

###Swagger UI
The Swagger UI link opens a new window/tab in the browser and displays the Swagger UI:  http://api.openswitch.net/rest/dist/index.html

###OpenSwitch.net
The OpenSwitch.net link opens a new window/tab in the browser and displays the OpenSwitch web site:  http://openswitch.net
