# VRF

## Contents
- [Configuration commands](#configuration-commands)
	- [vrf](#vrf)
- [Display commands](#display-commands)
	- [show vrf](#show-vrf)

## Configuration commands

###  vrf

##### Syntax
Under the config context.

`[no] vrf <vrf-name>`

##### Description
Add or remove a VRF.

##### Authority
Admin.

##### Parameters
| Parameter | Status   | Syntax| Description          |
|-----------|----------|-| ---------------------|
| *vrf-name*  | Required. | String. | The name of the VRF. |

##### Example
No examples to display.

## Display commands

### show vrf

##### Syntax
Under privileged mode.

`show vrf`

#### Description
Display the details of the configured VRFs.

#### Authority
Operator.

##### Parameters

None.

##### Example
```
hostname# show vrf
VRF Configuration:
------------------
VRF Name : vrf_default

        Interfaces :
        ------------
		1
        30
```
