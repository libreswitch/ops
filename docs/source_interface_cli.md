# Source Interface Commands

## Contents

- [Source Interface configuration commands](#source-interface-configuration-commands)
    - [Setting a source-interface IP address to TFTP protocol](#setting-a-source-interafce-ip-address-to-tftp-protocol)
    - [Setting a source-interface IP address for all the specified protocols](#setting-a-source-interafce-IP-address-for-all-the-specified-protocols)
    - [Setting a source-interface to TFTP protocol](#setting-a-source-interafce-to-tftp-protocol)
    - [Setting a source-interface for all the specified protocols](#setting-a-source-interafce-for-all-the-specified-protocols)
    - [Unsetting a source-interface to TFTP protocol](#unsetting-a-source-interafce-to-tftp-protocol)
    - [Unsetting a source-interface for all the specified protocols](#unsetting-a-source-interafce-for-all-the-specified-protocols)
- [Using source-interface show commands](#using-source-interface-show-commands)
    - [Showing source-interface selection configuration to TFTP protocol](#showing-source-interface-selection-configuration-to-tftp-protocol)
    - [Showing source-interface selection configuration for all the specified protocols](#showing-source-interface-selection-configuration-for-all-the-specified-protocols)


## Source Interface Configuration Commands

### Setting a source-interface IP address to the TFTP protocol
##### Syntax
`ip source-interface tftp address <A.B.C.D>`
#### Description
This command works in the configuration context and sets a source-interface IP address to the TFTP protocol.
Note: As of now the CLI infra is ready, end to end functionality of source interface selection to the TFTP protocol is not implemented.
#### Authority
All users.
#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *address* | Sets the IP address defined on any interface to the TFTP protocol.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# ip source-interface tftp address 1.1.1.1
```
### Setting a source-interface IP address for all the specified protocols
##### Syntax
`ip source-interface all address <A.B.C.D>`
#### Description
This command works in the configuration context and sets a source-interface IP address for all the specified protocols.
Note: As of now the CLI infra is ready, end to end functionality of source interface selection for all the specicied protocols is not implemented.
#### Authority
All users.
#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *address* | Sets the IP address defined on any interface for all the specified protocols.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# ip source-interface all address 1.1.1.1
```
### Setting a source-interface to TFTP protocol
##### Syntax
`ip source-interface tftp interface <IFNAME>`
#### Description
This command works in the configuration context and sets a source-interface to the TFTP protocol.
Note: As of now the CLI infra is ready, end to end functionality of source interface selection to the TFTP protocol is not implemented.
#### Authority
All users.
#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *interface* | Sets an IP address-defined interface to the TFTP protocol.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# ip source-interface tftp interface 1
```
### Setting a source-interface for all the specified protocols
##### Syntax
`ip source-interface all interface <IFNAME>`
#### Description
This command works in the configuration context and sets a source-interface for all the specified protocols.
Note: As of now the CLI infra is ready, end to end functionality of source interface selection for all the specicied protocols is not implemented.
#### Authority
All users.
#### Parameters
| Parameter | Description |
|:-----------|:---------------------------------------|
| *interface* | Sets an IP address-defined interface for all the specified protocols.|
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# ip source-interface all interface 1
```
### Unsetting a source-interface to TFTP protocol
##### Syntax
`no ip source-interface tftp`
#### Description
This command works in the configuration context and removes the TFTP protocol from the source-interface.
Note: As of now the CLI infra is ready, end to end functionality of source interface selection to the TFTP protocol is not implemented.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no ip source-interface tftp
```
### Unsetting a source-interface for all the specified protocols
##### Syntax
`no ip source-interface tftp`
#### Description
This command works in the configuration context and removes all the specified protocols from a source-interface.
Note: As of now the CLI infra is ready, end to end functionality of source interface selection for all the specicied protocols is not implemented.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
ops-as5712# configure terminal
ops-as5712(config)# no ip source-interface all
```
## Using source-interface show commands
### Showing source-interface selection configuration  assigned to the TFTP protocol.
##### Syntax
`show ip source-interface tftp`
#### Description
This command displays source-interface selection configuration assigned to the TFTP protocol.
Note: As of now the CLI infra is ready, end to end functionality of source interface selection to the TFTP protocol is not implemented.
#### Authority
All users.
#### Parameters
No parameters.
#### Example
```
ops-as5712# show ip source-interface tftp


Source-interface Information

Protocol        Source Interface
--------        ----------------
tftp            1
```

### Showing source-interface selection configuration for all the specified protocols.
##### Syntax
`show ip source-interface`
#### Description
This command displays the source-interface selection configuration for all the specified protocols.
Note: As of now the CLI infra is ready, end to end functionality of source interface selection for all the specicied protocols is not implemented.
#### Authority
All users.
#### Parameters
No parameters.
#### Example
```
ops-as5712# show ip source-interface


Source-interface Information

Protocol        Source Interface
--------        ----------------
tftp            1
```