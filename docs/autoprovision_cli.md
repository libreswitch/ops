# CLI support for Autoprovision

- [Autoprovision show command](#autoprovision-show-command)
	- [show autoprovisioning](#show-autoprovisioning)

## Autoprovision show command
### show autoprovisioning
Display the status of autoprovision.
#### Syntax
show autoprovisioning

#### Description
This command displays the autoprovision status. If autoprovision has been performed, the script URL is displayed. See the following examples for expected output.

#### Authority
Admin

#### Parameters
None

#### Examples
If autoprovision is performed
```bash
switch # show autoprovisioning
Performed : Yes
URL : http://192.168.1.1/autoprovision.sh
```
If autoprovision is not performed
```bash
switch # show autoprovisioning
Performed : No
```
