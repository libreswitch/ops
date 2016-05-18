# SFTP Design

## Contents
   - [High level design of SFTP](#high-level-design-of-sftp)
   - [Design choices](#design-choices)
   - [Internal structure](#internal-structure)
   - [OVSDB Schema](#ovsdb-schema)

## High level design of SFTP
The SFTP (Secure File Transfer Protocol) command is a very common method for transferring a file or executing a command in a secure mode. SFTP makes use of encrypted SSH sessions for its operation. It provides an alternative to TFTP (Trivial File Transfer Protocol) for transferring sensitive information to and from the switch. Files transferred using SFTP are encrypted and require authentication, thus providing greater security to the switch.

SFTP server:
The SFTP server can be enabled or disabled only by a netop user who has CLI as well as OVSDB access. The CLI daemon updates the modified configuration status of the SFTP server in the OVSDB. The ops-aaa-utils daemon which configures the SSH daemon picks up the modified status from the OVSDB and updates the `/etc/ssh/sshd_config` file. The SSH daemon reads the changes done in the `sshd_config` file and enables or disables the SFTP server accordingly.

SFTP client:
The SFTP client parameters are obtained from the user through the CLI. Information entered by the user is passed on to a SFTP CLI handler which maps this information to the open source SFTP client options and invokes the openSSH SFTP utility. The handler sends the response obtained from the openSSH back to the user. The end to end operation is performed in a single thread context as part of CLI daemon.
No OVSDB or any other module interaction is involved.
Only a netop user who has both CLI as well as OVSDB access can use SFTP client commands.

## Design choices

The open source `SFTP` application used is taken from the openSSH 6.8p1 package. SFTP runs on top of the SSH daemon and as openSSH 6.8 is the package currently used by the SSH daemon, we are leveraging the same.
The SFTP service is supported only in a management interface.
The SFTP client default destination location is `/var/local/`.

## Internal structure

```ditaa
SFTP client

+--------+           +-------------------+             +-----------------+
|        +----------->                   +------------->                 |
|  CLI   |           |  SFTP cli handler |             |   openSSH 6.8   |
|        <-----------+                   <-------------+    (client)     |
+--------+           +-------------------+             +-----------------+

```

```ditaa
SFTP server

+----------------+           +----------------------+             +-----------------+
|   CLI          +----------->                      |             |                 |
|  daemon        |           |       OVSDB          +------------->   AAA Daemon    |
|                <-----------+                      |             |                 |
+----------------+           +----------------------+             +-------+---------+
                                                                          |
                                                                          |
                                                                    +-----V----+     +----------+
                                                                    |   SSHd   |     |   open   |
                                                                    |   Config +----->  SSH 6.8 |
                                                                    |   file   |     | (server) |
                                                                    +----------+     +----------+

```

## OVSDB Schema
### System table
```
System:other_config
Key:
sftp_server_enable
Value:
true, false
```
