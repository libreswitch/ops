# General CLI commands

## Contents

- [Configuration commands](#configuration-commands)
- [Setting the session timeout](#setting-the-session-timeout)
	- [Setting a command alias](#setting-a-command-alias)
		- [Syntax](#syntax)
		- [Description](#description)
		- [Authority](#authority)
			- [Parameters](#parameters)
		- [Examples](#examples)
- [Display commands](#display-commands)
	- [Displaying the session-timeout value](#displaying-the-session-timeout-value)
		- [Syntax](#syntax)
		- [Description](#description)
		- [Authority](#authority)
		- [Parameters](#parameters)
		- [Examples](#examples)
	- [Displaying the aliases](#displaying-the-aliases)
		- [Syntax](#syntax)
		- [Description](#description)
		- [Authority](#authority)
		- [Parameters](#parameters)
		- [Examples](#examples)
- [Audit framwork](#audit-framwork)


## Configuration commands

### Setting the session timeout

#### Syntax
```
session-timeout <time>
no session-timeout
```
#### Description
Use this commmand to set the amount of time a CLI session can be idle before it is automatically logged out.

#### Authority
All users.

##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *time* | Required | 0-4320 | Idle timeout in minutes. A value of 0 means no timeout.|
| *no* | Required | Literal | Resets the session timeout to the default value of 30 minutes. |


#### Examples
```
switch(config)# session-timeout 2
switch(config)#
```
After being idle for 2 minutes ...
```
Idle session timeout reached, logging out.

Halon 0.3.0 switch ttyS1

switch login:
```

```
switch(config)# no session-timeout
switch(config)# do show session-timeout
session-timeout: 30 minutes (Default)

switch(config)#

```
### Setting a command alias

#### Syntax

```
alias <command> [ $1 $2 $3 ... $9 ${10} … ${N} ]
no alias <command>
```

#### Description
Use this command to define an alias for a CLI command.

#### Authority
All users.

##### Parameters
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *command* | Required | String | Command for which to create an alias. |
| *$1 $2 $3 ... $9 ${10} … ${N} * | Optional | String | These parameters are replaced by the corresponding arguments from the command line. Maximum length is 400 characters.|

Note: Alias commands available only in the configuration context.

#### Examples
```
switch(config)# alias hst hostname $1
switch(config)# hst myhost
myhost(config)#
myhost(config)# do show alias
 Alias Name                     Alias Definition
 -------------------------------------------------------------------------------
 hst                            hostname $1
myhost(config)#

myhost(config)# no alias hst
myhost(config)# do show hst
 Alias Name                     Alias Definition
 -------------------------------------------------------------------------------
myhost(config)#
```

## Display commands

### Displaying the session-timeout value

#### Syntax

`show session-timeout  `

#### Description
This command shows the idle timeout in minutes.

#### Authority
All users.

#### Parameters
None.

#### Examples
```
switch# show session-timeout
session-timeout: 2 minutes

switch#

```
### Displaying the aliases
#### Syntax
`show alias  `
#### Description
This command shows all aliases that are defined.
#### Authority
All users.
#### Parameters
No Parameters.
#### Examples
```
switch# show alias
 Alias Name                     Alias Definition
 -------------------------------------------------------------------------------
 abc                            hostname $1
```

##Audit framwork

The audit framework is used to create audit events for tracking configuaration changes made by users to switch. When users execute CLI configuration commands, the audit events are logged in the file: **/var/log/audit/audit.log**.

####Example
```
switch(config)# session-timeout 100
```

######Log format
```
type = USYS_CONFIG msg=audit(1456270989.650:31): pid=1507 uid=0 auid=4294967295 ses=4425671256  msg = 'op=CLI:command data=73657373696F6E2D74696D656F757420313030 exec="/usr/bin/vtysh" hostname=switch add=fe80::40af:cfff:feaf:d17c terminal=ttyS1 res=success'
```
The **data** field has an encoded version of the command that was executed. To decode the encoded data use the Linux **ausearch -i** command.

```
$ausearch -i -a 31
type = USYS_CONFIG msg=audit(03/22/16 08:29:57.452:10) : pid=604 uid=netop auid=unset ses=unset msg='op=CLI:command  data="session-timeout 100 " exe=/usr/bin/vtysh hostname=switch addr=fe80::4a0f:cfff:feaf:81dc terminal=ttyS1 res=success'
```
Where:
    "-a" or "--event"                :   Display events based on given event ID.
    "-i" or "--interpret"            :   Converts numeric values to text. Decodes uid/gid to the actual user/group name and displays encoded strings as their original ASCII values.
