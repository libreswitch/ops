# BroadView Commands

## Contents

- [BroadView configuration commands](#broadview-configuration-commands)
    - [broadview client ip port](#broadview-client-ip-port)
    - [broadview agent-port](#broadview-agent-port)
- [Display Commands](#display-commands)
    - [show broadview](#show-broadview)


## BroadView configuration commands


### broadview client ip port

#### Syntax
```
broadview client ip <ipv4-address> port <port-num>
```
#### Description
Sets the IP address of the remote device on which the application that retrieves BroadView statistics is located.

#### Command mode
Configuration mode (config).

#### Authority
Admin

#### Parameters

| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------|---------------------------------------|
| *ipv4-address* | Required | A.B.C.D | IPv4 adddress of the remote device. |
| *port-num* | Required | Integer | Port number the application is using on the remote device. |

#### Example

###### Setting up communications with a application on device 10.10.47.50 on port 8080
```
switch(config)# broadview client ip 10.10.47.50 port 8080
```


### broadview agent-port

#### Syntax
```
broadview agent-port <port-num>
```
#### Description
Sets the port number the BroadView agent on the switch will use to communicate with the application on the remote device

#### Authority
Admin.

#### Parameters
| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------|---------------------------------------|
| *port-num* | Required | Integer | Port number the BroadView agent will use to communicate. |

#### Examples

###### Setting the agent port to 8080
```
switch(config)# broadview agent-port 8080
```


## Display commands

### show broadview

#### Syntax
```
show broadview
```
#### Description
Display configuration settings.

#### Command mode
Enable mode.

#### Authority
Admin.

#### Parameters
None.

#### Example
```
switch# show broadview
BroadView client IP is 10.130.168.30
BroadView client port is 9054
BroadView agent port is 8080

```
