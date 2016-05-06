# Custom login banners
## Contents
- [Responsibilities](#responsibilities)
- [Design choices](#design-choices)
- [User roles](#user-roles)
- [Participating modules](#participating-modules)
- [OVSDB-schema](#ovsdb-schema)
- [References](#references)

## Responsibilities
The banner feature displays messages to a user authenticating themselves to a
management interface of a switch. One message is displayed before the user
enters their login and the other is displayed upon successful authentication.
These messages are customizable.

## Design choices
- The banner feature leverages the existing banner functionality in the OpenSSH
server for SSH connections.
- RESTD and ops-cli publish banner changes to the OVSDB.
- OpenSSH server reads the pre-authentication banner from `/etc/issue.net` and the
post authentication banner from `/etc/motd`.
- The AAA daemon subscribes to the System table and updates these files on disk
 whenever either banner has changed.

## User roles
There are currently two user roles in OpenSwitch, admin and netop.
The roles of these users are:
- admin: management of the actual switch hardware, admins are only allowed to
upgrade the firmware
- netop: management of virtual switch instances
Users in group ops\_netop are able to change the banner through the command line
interface. No other users are permitted to change the banner. This design is
based partly on the fact that the admin user in OpenSwitch should not have
access to vtysh. The design philosophy in OpenSwitch is that only ops\_netop
users are capable of making changes to the OVSDB.

## Participating modules

``` ditaa
     +---------------------+   +---------------------+
     |                     |   |                     |
     |       ops-cli       |   |       RESTD         |
     |                     |   |                     |
     |                     |   |                     |
     +----+----------------+   +-----+-----------+---+
          |                          |           |
          |                          +           |
publishes |                  subscribes          | publishes
          |                          +           |
          |        +-----------------v---+       |
          |        |                     |       |
          |        |       OVSDB         |       |
          +-------->                     <-------+
                   |                     |
                   +---------^-----------+
                             |
                             | subscribes
                             |
                   +---------+-----------+
                   |                     |
                   |        AAA          |
                   |                     |
                   |                     |
                   +---------+-----------+
                             | updates
                             |
                   +---------v------------+
                   |                      |
                   |     filesystem       |
                   |                      |
                   |                      |
                   +---------^------------+
                             | reads
                             |
                   +---------+------------+
                   |                      |
                   |        SSHD          |
                   |                      |
                   |                      |
                   +----------------------+

```
At the top of the diagram, the banner can be configured by a user through either the
ops-cli or RESTD. To set the banner is to alter the banner and banner\_exec KV
pairs referred to in the [OVSDB-schema](#ovsdb-schema) section below. The CLI
does not display the banner by subscribing to OVSDB because we need a method to
display a banner before the password prompt (when vtysh has not yet been loaded)
and after the password prompt. To accomplish this we simply leverage the built
in capability in the SSHD to display the contents of the files `/etc/issue.net`
and `/etc/motd` (these files are represented by the filesystem block in the above
diagram). For this to work, the files on disk must be updated whenever a change
is made to the related other\_configs in the schema. Ops-aaa subscribes to OVSDB
and modifies the files on disk whenever changes to the corresponding
other\_configs occur. RESTD simply reads the banner values from the OVSDB when it is
needed.

## OVSDB-schema
System:other\_config
Keys:
banner
banner\_exec

## References
* [Banner Commands](http://www.openswitch.net/documents/user/banner_cli)
* [Feature Test Cases for Banner](http://www.openswitch.net/documents/user/banner_test)
