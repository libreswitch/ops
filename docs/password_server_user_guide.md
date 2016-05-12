# Password Server

## Contents

- [Overview](#overview)
- [How to use a password server to update a user password](#how-to-use-a-password-server-to-update-a-user-password)
- [Setting up the basic configuration](#setting-up-the-basic-configuration)
- [Troubleshooting the configuration](#troubleshooting-the-configuration)
- [CLI](#cli)
- [Related features](#related-features)


## Overview
The password server provides a password service to other subsystems (clients) in
OpenSwitch.

This feature provides two functionalities:

- Updates the user password upon request.
  **Note:** The user must be in the `ovsdb-client` group.

- Adds or removes the user.
  **Note:** The requester must be in `ops-admin` group

## How to use a password server to update a user password

To update a user password, access the client program to open
the UNIX socket connection to the password and then send a request via a socket.

A message must be encrypted using the public key provided by the password server.
Upon execution of the request, the password server sends the status
of the operation back to the client program regardless of whether the operation is
successfully completed or not.

### Setting up the basic configuration

This feature is included in the switch image build and is enabled by default.
Since the password server uses a UNIX socket for the communication, the client
program must open a UNIX socket to communicate with the password server.

To communicate with the password server, the information below is needed:
- Location of the socket descriptor created by the password server
- Location of the public key file to encrypt the message
- Operation codes
- Status codes

Above information can be found in the design document.  The design document is
located at https://git.openswitch.net/cgit/openswitch/ops-passwd-srv/tree/DESIGN.md

### Troubleshooting the configuration

#### Condition
Error in updating the user password.
#### Cause
- Client program cannot connect to the password server (UNIX socket open fails)
- User password is not updated properly. For example the user did not provide a valid old and new password.

#### Remedy
- Make sure that the password server is running (`/usr/bin/ops-passwd-srv`)
- Run the command to list the password server daemon displayed as follows:
  ```bash
  ps aux | grep ops-passwd-srv
 ````
- Verify that `/usr/bin/ops-passwd-srv` is a running process.
- Make sure the user provided a valid old and new password to update the password
- Make sure the client program has the proper permissions such as
  - Only users from the `ovsdb-client` group are allowed to change their own passwords.
  - Only users from the `ovs-admin` group are allowed to add or remove users.

## CLI
The password server is a service module, it has no CLIs of its own.

## Related features
- The password server uses a crypto library to generate private or public keys.  A public
key is stored in the filesystem.
- The password server uses the `yaml-cpp` library to parse configurations.
- The password server uses a UNIX socket to listen for the request.