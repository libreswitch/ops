VLAN commands
======

## Contents

- [VLAN configuration commands](#vlan-configuration-commands)
	- [Interface context commands](#interface-context-commands)
		- [Assigning an interface to access mode VLAN](#assigning-an-interface-to-access-mode-vlan)
		- [Removing an interface from access mode VLAN](#removing-an-interface-from-access-mode-vlan)
		- [Assigning a trunk native VLAN to an interface](#assigning-a-trunk-native-vlan-to-an-interface)
		- [Removing a trunk native VLAN from an interface](#removing-a-trunk-native-vlan-from-an-interface)
		- [Assigning tagging on a native VLAN to an interface](#assigning-tagging-on-a-native-vlan-to-an-interface)
		- [Removing tagging on a native VLAN from an interface](#removing-tagging-on-a-native-vlan-from-an-interface)
		- [Assigning a VLAN to a trunk on the interface](#assigning-a-vlan-to-a-trunk-on-the-interface)
		- [Removing a VLAN from a trunk on the interface](#removing-a-vlan-from-a-trunk-on-the-interface)
	- [VLAN context commands](#vlan-context-commands)
		- [Turning on a VLAN](#turning-on-a-vlan)
		- [Turning off a VLAN](#turning-off-a-vlan)
	- [Global context commands](#global-context-commands)
		- [Creating a VLAN](#creating-a-vlan)
		- [Deleting a VLAN](#deleting-a-vlan)
- [VLAN display commands](#vlan-display-commands)
	- [Displaying a VLAN summary](#displaying-a-vlan-summary)
	- [Displaying a VLAN detail](#displaying-a-vlan-detail)


## VLAN configuration commands
### Interface context commands
#### Assigning an interface to access mode VLAN
####Syntax
`vlan access <vlanid>`
#### Description
This command assigns the interface to an existing access VLAN represented by the ID in the command.
If the VLAN does not exist already, this command displays an error.
####Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlanid* | Required | 1 - 4094 | Represents VLAN and takes values from 1 to 4094 |

#### Examples
The following commands assign interface 2 to access mode VLAN 20.
```
switch(config)# interface 2
switch(config-if)#no routing
switch(config-if)#vlan access 20
```

#### Removing an interface from access mode VLAN
#### Syntax
`no vlan access [<vlanid>]`
#### Description
This command removes the interface from an access VLAN represented by an ID.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlanid* | Optional | 1 - 4094 | Represents VLAN and takes values from 1 to 4094 |

#### Examples
```
switch(config)#interface 2
switch(config-if)# no VLAN access
```
OR
```
switch(config-if)# no VLAN access 20
```

#### Assigning a trunk native VLAN to an interface
#### Syntax
`vlan trunk native <vlanid>`
#### Description
This command assigns a trunk native VLAN represented by an ID to an interface or a LAG interface. The interface or LAG interface should have routing disabled for this command to work correctly.
#### Authority
All users.
#### Parameters

| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlanid* | Required | 1 - 4094 | Represents VLAN and takes values from 1 to 4094 |
#### Examples
```
switch(config)# interface 2
switch(config-if)#no routing
switch(config-if)#vlan trunk native 20
```
```
switch(config)# interface lag 2
switch(config-lag-if)#no routing
switch(config-lag-if)#vlan trunk native 20
```

#### Removing a trunk native VLAN from an interface
#### Syntax
`no vlan trunk native [<vlanid>]`
#### Description
This command removes the trunk native VLAN from an interface/LAG interface.
#### Authority
All users.
#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlanid* | Optional | 1 - 4094 | Represents VLAN and takes values from 1 to 4094 |
#### Examples
```
switch(config)# interface 2
switch(config-if)#no vlan trunk native
```
```
switch(config)# interface lag 2
switch(config-lag-if)#no vlan trunk native
```

#### Assigning tagging on a native VLAN to an interface
#### Syntax
`vlan trunk native tag`
#### Description
This command enables tagging on a native VLAN to an interface or a LAG interface.
#### Authority
All users.
#### Parameters
This command does not require a parameter.
#### Examples
```
switch(config)# interface 2
switch(config-if)#no routing
switch(config-if)#vlan trunk native tag
```
```
switch(config)# interface lag 2
switch(config-if)#no routing
switch(config-lag-if)#vlan trunk native tag
```


####Removing tagging on a native VLAN from an interface
#### Syntax
`no vlan trunk native tag`

#### Description
This command disables tagging on a native VLAN on an interface/LAG interface.

#### Authority
All users.

#### Parameters
This command does not take a parameter.

#### Examples
The following commands remove interface 2 from tagged trunk native VLAN.

    switch(config)# interface 2
    switch(config-if)# no vlan trunk native tag

The following commands remove interface LAG 2 to trunk native VLAN 20 which is already created.

    switch(config)# interface lag 2
    switch(config-lag-if)# no vlan trunk native tag

#### Assigning a VLAN to a trunk on the interface
#### Syntax
`vlan trunk allowed <vlanid>`

**Note : vlanid can accept input in the form of range, comma and both.**

For example :

      i)  vlan trunk allowed 2
     ii)  vlan trunk allowed 2-6
    iii)  vlan trunk allowed 2,5,8,10
     iv)  vlan trunk allowed 2-5,6

#### Description
This command assigns the VLAN represented by an ID to a trunk on the interface / LAG interface. This command expects the interface / LAG interface to be already configured as part of the trunk VLAN.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlanid* | Required | 1 - 4094 | Represents VLAN and takes values from 1 to 4094 |

#### Examples
```
switch(config)# interface 2
switch(config-if)#no routing
switch(config-if)#vlan trunk native 1
switch(config-if)#vlan trunk allowed  2
```
```
switch(config)# interface lag 2
switch(config-if)#no routing
switch(config-lag-if)#vlan trunk native 1
switch(config-lag-if)#vlan trunk allowed 2
```
```
switch(config)# interface 3
switch(config-if)# no routing
switch(config-if)# vlan trunk native 1
switch(config-if)# vlan trunk allowed 2-5,10,17
```

#### Removing a VLAN from a trunk on the interface
#### Syntax
`no vlan trunk allowed [<vlanid>]`

#### Description
This command removes the VLAN represented by an ID from a trunk on the interface/LAG interface.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlanid* | Required | 1 - 4094 | Represents VLAN and takes values from 1 to 4094 |

#### Examples
```
switch(config)# interface 2
switch(config-if)#no vlan trunk allowed 2
```
```
switch(config)# interface lag 2
switch(config-lag-if)#no vlan trunk allowed 2
```


### VLAN context commands
#### Turning on a VLAN
#### Syntax
`no shutdown`

#### Description
This command powers the VLAN up.

#### Authority
All users.

#### Parameters
This command does not require a parameter.

#### Examples
```
switch(config)# vlan 3
switch(config-vlan)# no shutdown
```
#### Turning off a VLAN
#### Syntax
`shutdown`

#### Description
This command shuts the VLAN down.

#### Authority
All users.

#### Parameters
This command does not require a parameter.

#### Examples
```
switch(config)# vlan 3
switch(config-vlan)# shutdown
```
### Global context commands
#### Creating a VLAN
#### Syntax
`vlan <vlanid>`

#### Description
This command creates a VLAN with a given ID and sets the admin state of the VLAN to the default of **down**.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlanid* | Required | 1 - 4094 | Represents VLAN and takes values from 1 to 4094 |

#### Examples
```
switch(config)# vlan 3
switch(config-vlan)#
```

#### Deleting a VLAN
#### Syntax
`no vlan < vlanid >`

#### Description
This command deletes the VLAN with a given ID. The value ranges from 1 to 4094.

#### Authority
All users.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlanid* | Required | 1 - 4094 | Represents VLAN and takes values from 1 to 4094 |
#### Examples
```
switch(config-vlan)# no vlan 3
switch(config)#
```
## VLAN display commands
### Displaying a VLAN summary
#### Syntax
`show vlan summary`

#### Description
This command displays a summary of a VLAN configuration.

#### Authority
All users.

#### Parameters
This command does not require a parameter.

#### Examples
`
switch#show vlan summary
`
```
Number of existing VLANs : 2
```
### Displaying a VLAN detail
#### Syntax
`show vlan [< vlanid >]`

#### Description
This command displays VLAN configuration information of all existing VLANs in the switch.

#### Authority
All users

#### Parameters
Use of a command with this parameter is optional.

| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *vlanid* | Required | 1 - 4094 | Represents VLAN and takes values from 1 to 4094 |

#### Examples
`
switch#show vlan
`

```
|VLAN   |    Name    |     Status  |      Reason  |   Reserved  |  Ports  |
|-------|------------|-------------|--------------|-------------|---------|
| 1     |   default  |   active    |    ADMIN/UP  |   No        |  1,L2   |
| 33    |   asdf     |   active    |    ADMIN/UP  |   L3        |   1     |
```

`
switch#show vlan 33
`
```
|VLAN   |    Name    |     Status  |      Reason  |   Reserved  |  Ports  |
|-------|------------|-------------|--------------|-------------|---------|
| 33    |   asdf     |   active    |    ADMIN/UP  |   L3        |   1     |
```
