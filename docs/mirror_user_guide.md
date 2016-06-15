# Port Mirroring User Guide


## Contents
	- [Overview](#overview)
		- [Mirror sessions](#mirror-sessions)
		- [Mirror rules](#mirror-rules)
		- [Creating a new mirror session](#creating-a-new-mirror-session)
		- [Editing an existing mirror session](#editing-an-existing-mirror-session)
			- [Removing the destination interface](#removing-the-destination-interface)
			- [Modifying the destination interface](#modifying-the-destination-interface)
			- [Modifying a source interface](#modifying-a-source-interface)
			- [Removing a source interface](#removing-a-source-interface)
			- [Deactivating a mirror session](#deactivating-a-mirror-session)
			- [Removing a mirror session](#removing-a-mirror-session)
		- [Displaying mirror session status](#displaying-mirror-session-status)
			- [Displaying a list of all configured mirror sessions](#displaying-a-list-of-all-configured-mirror-sessions)
			- [Displaying detailed mirror session information](#displaying-detailed-mirror-session-information)
		- [Troubleshooting](#troubleshooting)
			- [No data is being mirrored](#no-data-is-being-mirrored)
			- [Too much or not enough data is seen on the destination interface](#too-much-or-not-enough-data-is-seen-on-the-destination-interface)

## Overview
The port mirroring feature enables traffic on one or more switch interfaces to
be replicated on another interface for purposes such as monitoring.

### Mirror sessions
A mirror session defines the settings for the replication of data between one
or more source interfaces and a destination interface.

A maximum of four mirror sessions can be active at the same time on the switch.
There is no limit on the number of inactive sessions that can be defined in the
configuration.

Each mirror session has a single output, or *destination* interface, and zero
or more input, or *source* interfaces. The destination interface is the
recipient of all mirrored traffic, and must able to support  the combined data
rate of all source interfaces. Source interfaces can be configured to mirror
received traffic, transmitted traffic, or all traffic. Source and destination
interfaces do not need to reside in the same subnet, VLAN or VRF.

A LAG can be specified as either a source or destination interface. The switch
internally handles the mirroring of the traffic appropriately across all the
LAG member interfaces.

Mirroring is VRF agnostic. That is, a network administrator may choose to
specify source interfaces from different VRFs in the same mirror session and
have a single destination for the mirrored traffic.

### Mirror rules

The following rules apply when creating a mirror session:

1. An interface cannot be both a source and destination in the same mirror session.
2. The destination interface in an **active** mirror session cannot be the source
or destination in another **active** mirror session.
3. The source interface in an **active** mirror session cannot be the destination
in another **active** mirror session.
4. The destination interface cannot be a member of a VLAN nor have an IP address
configured.
5. The destination interface cannot have the spanning tree protocol enabled on it.

Note:
- If you try to activate a mirror session that violates rules 2 or 3 it will remain
shutdown.
- The same interface can be the source in more than one mirror session as long as it
does not violate rule 1 or 3.
- You can configure multiple session that violate rules 3 or 4 as long as they are
not active at the same time.


### Creating a new mirror session

1. Change to configuration mode.
```
switch# configure terminal
```

2. Create a new mirror session. In the following example, the session is called
**mirror_3**.
```
switch# (config)# mirror session mirror_3
```

3. Set interface 1 as the destination. Interface 1 must be a valid configured
switch interface.
```
switch# (config-mirror)# destination interface 1
```

4. Add source interface. In the following example, interface 2 will only mirror
incoming traffic.  Interface 2 must be a valid configured switch interface.
```
switch# (config-mirror)# source interface 2 rx
```

5. Add source interface. In the following example, interface 3 will only mirror
outgoing traffic.  Interface 3 must be a valid configured switch interface.
```
switch# (config-mirror)# source interface 3 tx
```

6. Add source interface. In the following example, interface 4 will mirror all
traffic.  Interface 4 must be a valid configured switch interface.
```
switch# (config-mirror)# source interface 4 both
```

7. Activate the mirror.  Prior to mirror activation ensure that all configured
interfaces are also actived or results may not be as expected.
```
switch# (config-mirror)# no shutdown
```

8. View mirror status to verify activation.
```
  switch# (config-mirror)# do show mirror

  name                                                            status
  --------------------------------------------------------------- --------------
  mirror_3                                                        active
```

9. View detailed mirror status to verify all interfaces.
```
switch# (config-mirror)# do show mirror mirror_3
 Mirror Session: mirror_3
 Status: active
 Source: interface 4 both
 Source: interface 2 rx
 Source: interface 3 tx
 Destination: interface 1
 Output Packets: 143658
 Output Bytes: 1207498
```


### Editing an existing mirror session

Mirror sessions can be modified while active.

#### Removing the destination interface
Removing the destination interface from an active mirror results in immediate
shutdown. For example:
```
switch# (config)# mirror session mirror_3
switch# (config-mirror)# no destination interface
switch# (config-mirror)# do show mirror

name                                                            status
--------------------------------------------------------------- --------------
mirror_3                                                        shutdown
```

#### Modifying the destination interface
A destination interface can be modified without removing the existing
definition. The mirror session remains active and traffic is immediately
sent to the new interface.
```
switch# (config)# mirror session mirror_3
switch# (config-mirror)# destination interface 5
switch# (config-mirror)# do show mirror mirror_3
 Mirror Session: mirror_3
 Status: active
 Source: interface 4 both
 Source: interface 2 rx
 Source: interface 3 tx
 Destination: interface 5
 Output Packets: 143658
 Output Bytes: 1207498
```

#### Modifying a source interface
To change the settings for a source port, re-issue the source command with the
new settings. For example, if interface 3 is set to mirror both types of
traffic, the following command changes it to only mirror transmitted traffic.
```
switch# (config)# mirror session mirror_3
switch# (config-mirror)# source interface 3 tx
```

#### Removing a source interface
The following example removes source interface 2 from the mirror_3 session.
```
switch# (config)# mirror session mirror_3
switch# (config-mirror)# no source interface 2
```

#### Deactivating a mirror session
```
(config)# mirror session mirror_3
(config-mirror)# shutdown
```

#### Removing a mirror session
This can be performed on both active and shutdown sessions.  If the session is
active, mirroring of traffic stops immediately.
```
switch(config)# no mirror session mirror_3
```


### Displaying mirror session status

#### Displaying a list of all configured mirror sessions
```
swtich (config)# show mirror

name                                                            status
--------------------------------------------------------------- --------------
mirror_1                                                        active
mirror_2                                                        shutdown
mirror_3                                                        active
```


#### Displaying detailed mirror session information
```
switch(config)# show mirror mirror_3

 Mirror Session: xyz
 Status: active
 Source: interface 4 both
 Source: interface 2 rx
 Source: interface 3 tx
 Destination: interface 1
 Output Packets: 143658
 Output Bytes: 1207498
```

### Troubleshooting

#### Unable to add interface to mirror
When attempting to add a source or destination interface to a mirror session,
if the message 'Invalid interface <interface_name>' is seen, make sure the
interface has been added to the switch configuration via the
'interface <interface_name>' command.  Note that the interface must also be
activated via the 'no shutdown' command for an active mirror session to
function properly.


#### No data is being mirrored
- Verify physical connectivity of the source and destination interfaces.
- Verify that all member interfaces have been activated via the 'no shutdown'
command
- Display details of the mirror session to ensure the desired ports are added
and the session status is **active**.
- Since session activation, if any source/destination LAG interface membership
changes have occurred, or if any interface routing changes have occured, these
interfaces will need re-adding to the mirror.  If one such interface was the
session destination, the session will also need to be reactivated.


#### Too much or not enough data is seen on the destination interface
Ensure that the source port you added is configured for the correct direction:
receive, transmit, or both.

#### Many to many condition
It is best that a source interface is in only one active mirror session.
It is permissible for the same source interface to be in difference sessions.
When the same source interface(s) are in multiple mirror sessions, there is
additional restriction that any one mirror session cannot have sources that are
also sources in different sessions.  This is called a ‘many-to-many’ situation.

An example of a many-to-many situation:
	Three mirror sessions A, B, & C.
	Interface 1 is a source in session A
	Interface 2 is a source in sessions A and B
	Interface 3 is a source in sessions B and C
	Interface 4 is a source in session C

Mirror session B will not work because its sources (2 & 3) are in a many-to-many
relationship with other mirror sessions.
