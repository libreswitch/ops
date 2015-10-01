# ECMP

## Contents
- [Configuration commands](#configuration-commands)
	- [ip ecmp disable](#ip-ecmp-disable)
	- [ip ecmp load-balance](#ip-ecmp-load-balance)
- [Display commands](#display-commands)
	- [show ip ecmp](#show-ip-ecmp)

## Configuration commands

### ip ecmp disable
##### Syntax
Under the config context.

`[no] ip ecmp disable`

##### Description
Completely disable Equal Cost Multi Path (ECMP).

##### Authority
Admin.

##### Parameters
None.

##### Example
```
hostname(config)# ip ecmp disable
hostname(config)#
```

###  ip ecmp load-balance dst-ip disable

##### Syntax
Under the config context.

`[no] ip ecmp load-balance dst-ip disable`

##### Description
Disable destination IP based load balancing. Use the 'no' variant to enable.

##### Authority
Admin.

##### Parameters
None.

##### Example
```
hostname(config)# ip ecmp load-balance dst-ip disable
hostname(config)#
```

###  ip ecmp load-balance src-ip disable

##### Syntax
Under the config context.

`[no] ip ecmp load-balance src-ip disable`

##### Description
Disable source IP based load balancing. Use the 'no' variant to enable.

##### Authority
Admin.

##### Parameters
None.

##### Example
```
hostname(config)# ip ecmp load-balance src-ip disable
hostname(config)#
```

###  ip ecmp load-balance dst-port disable

##### Syntax
Under the config context.

`[no] ip ecmp load-balance dst-port disable`

##### Description
Disable destination port based load balancing. Use the 'no' variant to enable.

##### Authority
Admin.

##### Parameters
None.

##### Example
```
hostname(config)# ip ecmp load-balance dst-port disable
hostname(config)#
```

###  ip ecmp load-balance src-port disable

##### Syntax
Under the config context.

`[no] ip ecmp load-balance src-port disable`

##### Description
Disable source port based load balancing. Use the 'no' variant to enable.

##### Authority
Admin.

##### Parameters
None.

##### Example
```
hostname(config)# ip ecmp load-balance src-port disable
hostname(config)#
```

## Display commands

### show ip ecmp

##### Syntax
Under privileged mode.

`show ip ecmp`

#### Description
Displays the ECMP configuration.

#### Authority
Operator.

##### Parameters
None.

##### Example
```
hostname# show ip ecmp

ECMP Configuration
---------------------

ECMP Status        : Enabled

ECMP Load Balancing by
------------------------
Source IP          : Enabled
Destination IP     : Enabled
Source Port        : Enabled
Destination Port   : Enabled

```
