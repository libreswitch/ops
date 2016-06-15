# Mirror Commands

## Contents
- [Overview](#overview)
	- [Mirror sessions](#mirror-sessions)
	- [Mirror rules](#mirror-rules)
- [Configuration commands](#configuration-commands)
	- [mirror session](#mirror-session)
	- [destination](#destination)
- [shutdown](#shutdown)
- [source](#source)
- [Mirror session show commands](#mirror-session-show-commands)
	- [show mirror](#show-mirror)

## Overview
The port mirroring feature enables traffic on one or more switch interfaces to
be replicated on another interface.

### Mirror sessions
A mirror session defines the settings for the replication of data between one
or more source interfaces and a destination interface.

A maximum of four mirror sessions can be active at the same time on the switch.
There is no limit on the number of inactive sessions that can be defined in the
configuration.

Each mirror session has a single output, or *destination* interface, and zero
or more input, or *source* interfaces. The destination interface is the
recipient of all mirrored traffic, and must able to support the combined data
rate of all source interfaces. Source interfaces can be configured to mirror
received traffic, transmitted traffic, or all traffic.

Source and destination interfaces do not need to reside in the same subnet,
VLAN or VRF.

A LAG can be specified as either a source or destination interface. The switch
internally handles the mirroring of the traffic appropriately across all the
LAG member interfaces.

Mirroring is VRF agnostic. That is, a network administrator may choose to
specify source interfaces from different VRFs in the same mirror session and
have a single destination for the mirrored traffic.

### Mirror rules

The following rules apply when creating a mirror session:

1. An interface cannot be both a source and destination in the same mirror
session.
2. The destination interface in an **active** mirror session cannot be the
source or destination in another **active** mirror session.
3. The source interface in an **active** mirror session cannot be the
destination in another **active** mirror session.
4. The destination interface cannot be a member of a VLAN nor have an IP address
configured.
5. The destination interface cannot have the spanning tree protocol enabled on
it.

Note:
- If you try to activate a mirror session that violates rules 2 or 3 it will
remain shutdown.
- The same interface can be the source in more than one mirror session as long
as it does not violate rule 1 or 3.


## Configuration commands

### mirror session

#### Syntax
```
mirror session <name>
no mirror session <name>
```

#### Description
Changes to mirror session mode for the specified session name. If the session
name does not exist, it is created.

Use the `no` form of this command to remove a mirror session.


#### Command mode
Configuration mode (config).

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:----------|:---------|:---------------|:--------------------------------------|
| *name* | Required | String | Name of a session. Up to 64 letters, numbers, underscores, dashes, or periods. |


#### Example

###### Creating a new mirror session named **Mirror_3**
```
switch(config)# mirror session Mirror_3
switch(config-mirror)#
```


### destination

#### Syntax
```
destination interface <interface>
no destination interface
```

#### Description
The **destination interface** command assigns the specified Ethernet interface
or LAG where all mirror traffic for this session will be transmitted.  Only one
destination interface is allowed per session.

The interface must already be an interface defined in the switch configuration.
Interface activation is not necessary for addition to a mirror session.

Entering another destination interface will cause all mirror traffic to use the
interface.  This may cause a temporary suspension of mirror traffic from the
source(s) during the reconfiguration.

The **no destination interface** command will cease the use of the interface and
deactivate (shutdown) the session.

##### Special requirements for destination interfaces

To be qualified as a mirror session destination, the interface:
- Must not already be a source or destination in any other active mirror session
- Must not be participating in any form of Spanning Tree protocol
- Must not be a member of a VLAN nor have an IP address configured.

**NOTE** An interface will be automatically removed from a mirror session in these
two circumstances:
- the interface becomes a member of a LAG
- the interface route mode is changed (i.e. ‘routing’ or ‘no routing’)

If the interface removed is a mirror destination, then the mirror session is
automatically de-activated (i.e. ‘no shutdown’).

The interface/LAG must then be re-added to the mirror session and the session
reactivated.


#### Command mode
Mirror session mode (config-mirror).

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:----------|:---------|:---------------|:--------------------------------------|
| *interface* | Required | String | Name of a an interface. |

#### Example

###### Setting interface **10** as the destination for the session **Mirror_3**
```
switch(config)# mirror session Mirror_3
switch(config-mirror)# destination interface 10
```

###### Removing interface **10** as the destination for the session **Mirror_3**
```
switch(config)# mirror session Mirror_3
switch(config-mirror)# no destination interface
```


## shutdown

#### Syntax
```
shutdown
no shutdown
```

#### Description
Deactivates a mirror session. By default, mirror sessions are inactive.

Use the `no` form of this command to activate a mirror session.

#### Command mode
Mirror session mode (config-mirror).

#### Authority
All users.

#### Examples

###### Activating mirror session Mirror_3
```
switch(config)# mirror session Mirror_3
switch(config-mirror)# no shutdown
```

## source

#### Syntax
```
source interface <INTERFACE> {both|rx|tx}
no source interface <INTERFACE>
```

#### Description
The **source interface** command adds, modifies, or removes the specified Ethernet
interface or LAG as a mirror source.  When adding or modifying a source port, the
mirror traffic direction must be specified:
- **both** - traffic received and transmitted
- **rx** only received traffic
- **tx** only transmitted traffic

A source interface must already be an interface defined in the switch configuration.
Interface activation is not necessary for addition to a mirror session.

More than one source interface can be configured in a mirror session, each with
their own direction.

To change the direction of a source interface, reenter the **source interface**
command again with the new direction.

There may be a temporary suspension of mirrored traffic when adding sources or
changing source directions.

The **no source <INTERFACE>** command will cease mirroring traffic from the
source interface.

##### Special requirements for mirror source interfaces

To be qualified as a mirror session source, the interface must:
- Not already be a destination in any mirror session

**NOTE** An interface will be automatically removed from a mirror session in these
two circumstances:
- the interface becomes a member of a LAG
- the interface route mode is changed (i.e. ‘routing’ or ‘no routing’)

The interface/LAG must then be re-added to the mirror session.

#### Command mode
Mirror session mode (config-mirror).

#### Authority
All configuration users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *INTERFACE* |  Ethernet interface or LAG

#### Examples
```
switch# configure terminal
switch(config)# mirror session Mirror_3
switch(config-mirror)# source interface 5 both
```


## Mirror session show commands
The following commands show configuration and status information of mirror
sessions.

### show mirror

#### Syntax
```
show mirror [<NAME>]
```

#### Description
The **show mirror** command will display the list of all configured mirror
sessions and their status.

With a **NAME** parameter, this command will display the details of the single
named mirror session.

#### Authority
All users.

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* |  Display the details of that mirror session

#### Examples
```
switch# show mirror
 name                                                            status
 --------------------------------------------------------------- --------------
 My_Session_1                                                    active
 Other-Session-2                                                 shutdown

switch# show mirror My_Session_1
 Mirror Session: My_Session_1
 Status: active
 Source: interface 2 both
 Source: interface 3 rx
 Destination: interface 1
 Output Packets: 123456789
 Output Bytes: 8912345678
```
