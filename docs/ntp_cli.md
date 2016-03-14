
# NTP Commands Reference

## Contents
- [NTP configuration commands](#ntp-configuration-commands)
	- [ntp server](#ntp-server)
	- [ntp authentication enable](#ntp-authentication-enable)
	- [ntp authentication key](#ntp-authentication-key)
	- [ntp trusted key](#ntp-trusted-key)
- [Display commands](#display-commands)
	- [show ntp associations](#show-ntp-associations)
	- [show ntp status](#show-ntp-status)
	- [show ntp trusted-keys](#show-ntp-trusted-keys)
	- [show ntp authentication-keys](#show-ntp-authentication-keys)
	- [show ntp statistics](#show-ntp-statistics)

## NTP configuration commands

### ntp server

#### Syntax
```
ntp server <name|ipv4-address> [key key-id] [prefer] [version version-number]
[no] ntp server <name|ipv4-address>
```

#### Description
Forms an association with an NTP server.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *name* | Required | Name-string of maximum length 57 characters or A.B.C.D. | The name or IPV4 address of the server. |
| *key-id* | Optional | 1-65534 | The key used while communicating with the server. |
| *prefer* | Optional | Literal | Request to make this the preferred NTP server. |
| *version-no* | Optional | 3-4 | NTP version 3 or 4. |
| **no** | Optional | Literal | Destroys a previously configured server. |

#### Examples
```
s1(config)#ntp server time.apple.com key 10 version 4
s1(config)#no ntp server 192.0.1.1
```

### ntp authentication

#### Syntax
```
[no] ntp authentication enable
```

#### Description
Enables/disables the NTP authentication feature.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| **no** | Optional | Literal | Disables the NTP authentication feature. |

#### Examples
```
s1(config)#ntp authentication enable
s1(config)#no ntp authentication enable
```

### ntp authentication-key

#### Syntax
```
ntp authentication-key <key-id> md5 <password>
[no] ntp authentication-key <key-id>
```

#### Description
Defines the authentication key.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *key-id* | Required | 1-65534 | The key used while communicating with the server. |
| password | Required | 8-16 chars | The MD5 password. |
| **no** | Optional | Literal | Destroys the previously created NTP authentication key. |

#### Examples
```
s1(config)#ntp authentication-key 10 md5 myPassword
s1(config)#no ntp authentication-key 10
```

### ntp trusted-key

#### Syntax
```
[no] ntp trusted-key <key-id>
```

#### Description
Marks a previously defined authentication key as trusted.
If NTP authentication is enabled, the device synchronizes with a time source only if the server carries one of the authentication keys specified as a trusted key.

#### Authority
Admin user.

#### Parameters
| Parameter | Status   | Syntax |	Description          |
|-----------|----------|----------------------|
| *key-id* | Required | 1-65534 | The key used while communicating with the server. |
| **no** | Optional | Literal | Destroys the perviously created NTP authentication key. |

#### Examples
```
s1(config)#ntp trusted-key 10
s1(config)#no ntp trusted-key 10
```

## Display commands

### show ntp associations

#### Syntax
```
show ntp associations
```

#### Description
Displays the status of connections to NTP servers.

#### Authority
Admin user.

#### Parameters
No parameters.

#### Examples
```
s1(config)#show ntp associations
--------------------------------------------------------------------------------------------------------------------
  ID             NAME           REMOTE  VER  KEYID           REF-ID  ST  T  LAST  POLL  REACH  DELAY  OFFSET  JITTER
--------------------------------------------------------------------------------------------------------------------
   1        192.0.1.1        192.0.1.1    3      -           .INIT.   -  -     -     -      -      -       -       -
*  2   time.apple.com     17.253.2.253    4     10           .GPSs.   2  U    10    64      0  0.121   0.994   0.001
--------------------------------------------------------------------------------------------------------------------
```

#### Key
```
code         : Tally code (Explained later)
ID           : Server number
NAME         : NTP server FQDN/IPV4 address (only the first 15 characters of the name are displayed)
REMOTE       : Remote server IP address
VER          : NTP version (3 or 4)
KEYID        : Key used to communicate with this server
REF_ID       : Reference ID for the remote server (Can be an IP address)
Stratum (ST) : Number of hops between the client and the reference clock.
TYPE (T)     : Transmission Type - U Unicast/manycast; B Broadcast; M Multicast; L Local; b bcast/mcast; S Symm_peer; m manycast
LAST         : Poll interval since the last packet was received (seconds unless unit is provided).
POLL         : Interval (in seconds) between NTP poll packets. Maximum (1024) reached as server and client syncs.
REACH        : Octal number that displays status of last eight NTP messages (377 - all messages received).
DELAY        : Round trip delay (in milliseconds) of packets to the selected reference clock.
OFFSET       : Provides Root Mean Square time (in milliseconds) between this local host and the remote peer or server.
JITTER       : Maximum error (in milliseconds) of local clock relative to the reference clock.
```

#### Key for the Tally code
This field displays the current selection status.
```
  : Discarded as not valid
x : Discarded by intersection algorithm
. : Discarded by table overflow (not used)
- : Discarded by the cluster algorithm
+ : Included by the combine algorithm
# : Backup (more than tos maxclock sources)
* : System peer
o : PPS peer (when the prefer peer is valid)
```

### show ntp status

#### Syntax
```
show ntp status
```

#### Description
Displays the status of NTP on the switch; whether NTP is enabled/disabled and if it has been syncronized with a server.

#### Authority
Admin user.

#### Parameters
No parameters.

#### Examples
When the system has not been synced:
```
s1(config)#show ntp status
NTP is enabled.
NTP authentication is enabled.
```
When the system has been synced to a NTP server:
```
s1(config)#show ntp status
NTP is enabled.
NTP authentication is enabled.
Uptime: 200 seconds
Synchronized to NTP Server 17.253.2.253 at stratum 2.
Poll interval = 1024 seconds.
Time accuracy is within 0.994 seconds
Reference time: Thu Jan 28 2016 0:57:06.647 (UTC)
```

### show ntp authentication-keys

#### Syntax
```
show ntp authentication-keys
```

#### Description
Displays the NTP authentication keys.

#### Authority
Admin user.

#### Parameters
No parameters.

#### Examples
```
s1(config)#show ntp authentication-keys
--------------------------------
Auth key            MD5 password
--------------------------------
 10                 MyPassword
```

### show ntp trusted-keys

#### Syntax
```
show ntp trusted-keys
```

#### Description
Displays the NTP trusted keys.

#### Authority
Admin user.

#### Parameters
No parameters.

#### Examples
```
s1(config)#show ntp trusted-keys
-------------
Trusted keys
-------------
 10
 50
-------------
```

### show ntp statistics

#### Syntax
```
show ntp statistics
```

#### Description
Displays the global NTP statistics.

#### Authority
Admin user.

#### Parameters
No parameters.

#### Examples
```
s1(config)#show ntp statistics
Rx-pkts              100
Rx cur ver           80
Rx old ver           20
Err-pkts             2
Auth-failed-pkts     1
Declined-pkts        0
Restricted-pkts      0
Rate-limited-pkts    0
KoD-pkts             0
```
Legend:
```
Rx-pkts: Total NTP packets received.
Cur Ver Rx-pkts: Number of NTP packets that match the current NTP version.
Old Ver Rx-pkts: Number of NTP packets that match the previous NTP version.
Error pkts: Packets dropped due to all other error reasons.
Auth-failed pkts: Packets dropped due to authentication failure.
Declined pkts: Packets denied access for any reason.
Restricted pkts: Packets dropped due to NTP access control.
Rate-limited pkts: Number of packets discarded due to rate limitation.
KOD pkts: Number of Kiss of Death packets.
```
Note: Because ntpq sends query messages to ntpd for fetching status information.
`Rx-pkts` field may show a non-zero packet count, even when ntp association is not
configured on the switch.
