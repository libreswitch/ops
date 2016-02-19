# Mirror Commands
<!-- Version 3 -->

## Contents

- [Mirror session configuration commands](#mirror-session-configuration-commands)
  - [destination](#destination)
  - [shutdown](#shutdown)
  - [source](#source)
- [Mirror session show commands](#mirror-session-show-commands)
  - [show mirror](#show-mirror)

Mirroring is the ability of a switch to transmit a copy of a packet out another
port.  This allows network administrators to seamlessly inspect traffic flowing
through the switch.

Mirroring is configured and controlled from a Mirror Session in the
configuration context.

**NOTE:**  OpenSwitch 0.4 only supports mirroring traffic from one or more ports
out another port.


## Mirror session configuration commands

#### Syntax
```
mirror session <NAME>
no mirror session <NAME>
```

To create or edit an existing the Mirror Session context, enter **mirror session
<NAME>**.

The following commands are available in the Mirror Session context:
- [destination](#destination)
- [shutdown](#shutdown)
- [source](#source)

#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *NAME* |  Up to 64 letters, numbers, underscores, dashes, or periods


#### Examples
```
switch# configure terminal
switch(config)# mirror session Port_1_Mirror
switch(config-mirror)#
```


## destination

#### Syntax
```
destination interface <INTERFACE>
no destination interface
```

#### Description
The **destination interface** command assigns the specified Ethernet interface
or LAG where all mirror traffic for this session will be transmitted.  Only one
destination interface is allowed per session.

Entering another destination interface will cause all mirror traffic to use the
interface.  This may cause a temporary suspension of mirror traffic from the
source(s) during the reconfiguration.

The **no destination interface** command will cease the use of the interface and
deactivate (shutdown) the session.

##### Special requirements for destination interfaces

To be qualified as a mirror session destination, the interface:
- Must not already be a source or destination in any other active mirror session
- Must not be participating in any form of Spanning Tree protocol
- Must not have routing enabled
- Must not have any IP addresses configured on the destination


**NOTE**: When the destination is an Ethernet LAG and members are added or
removed while the mirror session is active, the session must be restarted for
the change to be recognized

To clearly distinguish mirror traffic, it is best if the interface is either the
sole member of a vlan or VRF.

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
switch(config-mirror)# destination interface 10
```

## shutdown

#### Syntax
```
shutdown
no shutdown
```

#### Description
By default a newly created mirror session is inactive.  To activate mirroring of
traffic from the source(s) to the destination enter the **no shutdown** command.

The **shutdown** command will stop mirroring of traffic from the source to the
destination.

**NOTE**:  Please refer to product documentation for the allowed number of
simultaneous active mirror sessions.

#### Authority
All configuration users.

#### Examples
```
switch# configure terminal
switch(config)# mirror session Mirror_3
switch(config-mirror)# destination interface 10
switch(config-mirror)# source interface 20
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
interface or LAG as a mirror source.  When adding or modifing a source port, the
direction where traffic to be mirror must be specified:
- **both** - traffic received and transmitted
- **rx** only received traffic
- **tx** only transmitted traffic

More than one source interface can be configured in a mirror session, each with
their own direction.

To change the direction of a source interface, reenter the **source interface**
command again with the new direction.

A temporary suspension mirroring traffic from all source(s) may occur when
adding sources or changing source directions.

The **no source <INTERFACE>** command will cease mirroring traffic from the
source interface.

##### Special requirements for mirror source interfaces

To be qualified as a mirror session source, the interface must:
- Not already be a destination in any mirror session

**NOTE** When the source is an Ethernet LAG and members are added or removed
while the mirror session is active, the session must be restarted for the change
to be recognized

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
