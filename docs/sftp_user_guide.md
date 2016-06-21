# SFTP

## Contents
   - [Overview](#overview)
   - [SFTP Server](#sftp-server)
   - [How to use SFTP server](#how-to-use-sftp-server)
   - [SFTP Client](#sftp-client)
   - [How to use SFTP client](#how-to-use-sftp-client)

## Overview
The SFTP (Secure File Transfer Protocol) command is a very common method for transferring a file or executing a command in a secure mode. SFTP makes use of encrypted SSH session for it's operation. It provides an alternative to TFTP (Trivial File Transfer Protocol) for transferring sensitive information to and from the switch.
Files transferred using SFTP are encryted and require authentication, thus providing greater security to the switch.
Both SFTP server and client functionality is supported in OpenSwitch. If switch acts as an SFTP server, it listens on a default SSH port (default SSH port is 22) for any incoming connections. As an SFTP client, it can initiate a file transfer or enter remote device. SFTP client commands can be accessed only by an admin user. The SFTP service is supported only in management interface.

## SFTP server
Syntax:
`[no] sftp server enable`
*Enables/Disables SFTP server. By default, it is disabled.*

`show sftp server`
*Display the SFTP server status.*

## How to use SFTP server

### Example

```
switch(config)#sftp server enable

switch#show sftp server

SFTP server configuration
........................................
SFTP server : Enabled

switch#show running-config
Current configuration:
!
!
!
sftp server enable

switch(config)#no sftp server enable

switch#show sftp server

SFTP server configuration
........................................
SFTP server : Disabled
```

## SFTP client
Syntax:
`copy sftp WORD (ipv4-address | hostname | ipv6-address) WORD [WORD]`
- get operation

`copy sftp WORD (ipv4-address | hostname | ipv6-address)`
- get operation
- put operation

## How to use SFTP client

```
switch# copy sftp user hostname srcpath
*Provide the username, hostname and the source file path of
the remote device.
Default destination is '/var/local/'*

switch# copy sftp abc hostmachine source-file
abc@hostmachine's password:
Connected to 10.1.1.1.
Fetching source-file to source-file
source-file                   100%   25     0.0KB/s   00:00
switch#
```

```
switch# copy sftp user IPv4-address srcpath
*Provide the username, IPv4 address and the source file path of
the remote device.
Default destination is '/var/local/'*

switch# copy sftp abc 10.1.1.1 source-file
abc@10.1.1.1's password:
Connected to 10.1.1.1.
Fetching source-file to source-file
source-file                   100%   25     0.0KB/s   00:00
switch#
```

```
switch# copy sftp user IPv6-address srcpath
*Provide the username, IPv6 address and the source file path of
the remote device.
Default destination is '/var/local/'*

switch# copy sftp abc a::1 source-file
abc@a::1's password:
Connected to a::1.
Fetching source-file to source-file
source-file                   100%   25     0.0KB/s   00:00
switch#
```

```
switch# copy sftp user hostname srcpath dstpath
*Provide the username, hostname, source path of
the remote device and the destination path where
the file is to be stored on the local device.*

switch# copy sftp abc hostmachine source-file destination-file
abc@hostmachine's password:
Connected to hostmachine.
Fetching source-file to destination-file
source-file                   100%   25     0.0KB/s   00:00
switch#
```

```
switch# copy sftp user IPv4-address srcpath dstpath
*Provide the username, IPv4 address, source path of
the remote device and the destination path where
the file is to be stored on the local device.*

switch# copy sftp abc 10.1.1.1 source-file destination-file
abc@10.1.1.1's password:
Connected to 10.1.1.1.
Fetching source-file to destination-file
source-file                   100%   25     0.0KB/s   00:00
switch#
```

```
switch# copy sftp user IPv6-address srcpath dstpath
*Provide the username, IPv6 address, source path of
the remote device and the destination path where
the file is to be stored on the local device.*

switch# copy sftp abc a::1 source-file destination-file
abc@a::1's password:
Connected to a::1.
Fetching source-file to destination-file
source-file                   100%   25     0.0KB/s   00:00
switch#
```

```
switch# copy sftp user hostname
*Provide the username and hostname of the remote device.*

switch# copy sftp abc hostmachine
abc@hostmachine's password:
Connected to hostmachine.
sftp>
sftp> get /users/abc/test_file
Fetching /users/abc/test_file to test_file
/users/abc/test_file                                                                                                                            100%  212     0.2KB/s   00:00
sftp> put test_file /users/abc/
Uploading test_file to /users/abc/test_file
test_file                                                                                                                                      100%  212     0.2KB/s   00:00
```

```
switch# copy sftp user IPv4-address
*Provide the username and IPv4 address of the remote device*

switch# copy sftp abc 10.1.1.1
The authenticity of host '10.1.1.1 (10.1.1.1)' can't be established.
ECDSA key fingerprint is SHA256:uWeyXm2j6VkDfCitlyz/P+xGgZW9YYw5GnDOsEgVHeU.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.1.1.1' (ECDSA) to the list of known hosts.
abc@10.1.1.1's password:
Connected to 10.1.1.1.
sftp>
sftp> get /users/abc/test_file
Fetching /users/abc/test_file to test_file
/users/abc/test_file                                                                                                                            100%  212     0.2KB/s   00:00
sftp> put test_file /users/abc/
Uploading test_file to /users/abc/test_file
test_file                                                                                                                                      100%  212     0.2KB/s   00:00
```
```
switch# copy sftp user IPv6-address
*Provide the username and IPv6 address of the remote device*

switch# copy sftp abc a::1
The authenticity of host 'a::1 (a::1)' can't be established.
ECDSA key fingerprint is SHA256:uWeyXm2j6VkDfCitlyz/P+xGgZW9YYw5GnDOsEgVHeU.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'a::1' (ECDSA) to the list of known hosts.
abc@a::1's password:
Connected to a::1.
sftp>
sftp> get /users/abc/test_file
Fetching /users/abc/test_file to test_file
/users/abc/test_file                                                                                                                            100%  212     0.2KB/s   00:00
sftp> put test_file /users/abc/
Uploading test_file to /users/abc/test_file
test_file                                                                                                                                      100%  212     0.2KB/s   00:00
```
