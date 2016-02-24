# NTP Feature Test Cases

## Contents

- [NTP configuration without authentication](#ntp-configuration-without-authentication)
- [NTP configuration with authentication](#ntp-configuration-with-authentication)


## NTP configuration without authentication

### Objective
The test case checks if the switch is configured as a Network Time Protocol (NTP) client and if the switch is successfully configured with the local NTP server.


#### Requirements
- Virtual Mininet test setup with a workstation that can host as a local NTP server
- **FT file**: `ops/tests/ntp/test_ntpd_ft_auth_noauth_restart.py`


#### Setup
##### Topology diagram
```
   +------------+   +------------+
   |            |   |            |
   |  Switch    |---|    Host1   |
   |            |   |    (auth)  |
   +------------+   +------------+
         |
         |
   +-----------+
   |           |
   |   Host    |
   |  (no auth)|
   +-----------+
```

#### Test setup

##### NTP server setup

1. The preferred NTP server should be configured with the following parameters in the `/etc/ntp.conf` file.

 ```
 keys /etc/ntp.keys
 trustedkey <key-id>
 server <server_ip> prefer
 ```

2. The `/etc/ntp.keys` file in the NTP server should have the appropriate key that can be used for authentication.
For example:

 ```
 55 MD5 MyNtpPassword

 ```

3. Start the NTPD service and verify that the service is running on the server.

 ```
 # ntpd -c /etc/ntp.conf

 ```

4. Verify that the non-NTP server provided in the `ntp.conf` file is configured properly.

Example output:

```

  ntpq -p


     remote           refid      st t when poll reach   delay   offset  jitter
  ==============================================================================
  *15.1.1.3           .GPS.       2 u    9   64    1   48.865  -51.213   0.000


```


##### NTP client setup

Configure the switch as an NTP client and add the NTP server's IP address as a preferred IP address.

  ```
  configure terminal
  ntp server <ntp_server_ip>
  ntp server 172.17.0.2 prefer
  ntp server 172.17.0.3 key-id 55
  ```


#### Restartabilty

Restart the ops-ntpd service on the switch, and check if the NTP associations and NTP status is verified.
Use the command below on the switch to restart the ops-ntpd service.

The following command is not a vtysh CLI command. Run it on the Linux shell.
To come out of the vtysh shell, use `exit` on the vtysh shell and then execute the following command.

 ```
 service restart ops-ntpd
 ```

After restarting an additional-ntpd service, make sure that the NTP association and NTP status is verified.


### Test result criteria

#### Test pass criteria

- The NTP server configured for the client has an appropriate REF-ID.

- Check the NTP status and verify if the clock is synchronized with the NTP server.

- Confirm that the local server can reach its configured public server. If the public server cannot be reached, the NTP client cannot be configured with the local NTP server.

- The nonauthenticating server has been added as the preferred server. Confirm that the IP address of the preferred server is synchronized with the client.

Example output:

 ```

 show ntp associations
 ----------------------------------------------------------------------------------------------------------------------
   ID             NAME           REMOTE  VER  KEYID           REF-ID  ST  T  LAST  POLL  REACH    DELAY  OFFSET  JITTER
 ----------------------------------------------------------------------------------------------------------------------
    1       172.17.0.2       172.17.0.2    3     55          15.1.1.4  2  U     4    64     17    0.109  -0.005   0.040
 *  2       172.17.0.3       172.17.0.3    3      -          15.1.1.3  2  U     4    64     17    0.133   0.023   0.032
 ----------------------------------------------------------------------------------------------------------------------

 switch# show ntp status

 NTP is enabled
 NTP authentication is enabled
 Synchronized to NTP Server 172.17.0.3 at stratum 3
 Poll interval = 64 seconds
 Time accuracy is within 0.016 seconds
 Reference time: Thu Jan 27 2016 20:32:55.639
 ```

#### Test fail criteria

If the REF-ID status is .NKEY., .INIT., .TIME.,.RATE. or .AUTH., an issue exists with connecting to the NTP server.



## NTP configuration with authentication

### Objective

The test case checks if the switch is configured as a Network Time Protocol (NTP) client and if the switch is successfully configured with NTP server with authentication.

#### Requirements
- Virtual Mininet test setup with a workstation that can host as a local NTP server
- **FT file**: `ops/tests/ntp/test_ntpd_ft_auth_noauth_restart.py`

#### Setup
##### Topology diagram
```
   +------------+   +------------+
   |            |   |            |
   |  Switch    |---|    Host1   |
   |            |   |    (auth)  |
   +------------+   +------------+
         |
         |
   +-----------+
   |           |
   |   Host    |
   |  (no auth)|
   +-----------+

```


#### Test setup

##### NTP server setup

We have set up two NTP servers using Host1 and Host2.

1. The preferred NTP server should be configured with the following parameters in the `/etc/ntp.conf` file.

 ```
authenticate yes
keys /etc/ntp.keys
trustedkey <key-id>
server <server_ip> prefer
 ```

2. The `/etc/ntp.keys` file in the NTP server should have the appropriate key that can be used for authentication.
For example:

 ```
55 MD5 MyNtpPassword
 ```

3. Start the NTPD service and verify the service is running on the server.

 ```
  # ntpd -c /etc/ntp.conf

 ```

4. Verify that the NTP server provided in the `ntp.conf` file is configured properly.

 ```
 ntpq -p

     remote         refid      st t when poll reach   delay   offset  jitter
 ===========================================================================
  *15.1.1.3         .GPS.      2  u   9   64    1   48.865  -51.213   0.000

 ```


##### NTP client setup

Configure the switch as an NTP client and add both the NTP servers' IP addresses as a preferred IP address.

  ```
  configure terminal
  ntp authentication-key 55 md5 MyNtpPassword
  ntp trusted-key 55
  ntp authentication enable
  ntp server 172.17.0.2
  ntp server 172.17.0.3 prefer key-id 55
  ```

#### Restartabilty

Restart the ops-ntpd service on the switch, and check if the NTP associations and NTP status is verified.
Use the command below on the switch to restart the ops-ntpd service.

The following command is not a vtysh CLI command, and run it on the Linux shell.
To come out of the vtysh shell, use `exit` on the vtysh shell and then run following command:

```
service restart ops-ntpd
```

After restarting the ops-ntpd service, confirm that the NTP association and NTP status is verified.


### Test result criteria

#### Test pass criteria

- The NTP server configured for the client has an appropriate REF-ID. Confirm that the preferred server is configured properly without errors in the REF-ID column.

- Check the NTP status, and verify that the clock is synchronized with the NTP server.

- Confirm that the local server can reach its configured public server. If the public server cannot be reached, the NTP client cannot be configured with the local NTP server.

- The nonauthenticating server has been added as the preferred server. Confirm that the IP address of the preferred server is synchronized with the client.

Example output:

```

switch# show ntp associations
----------------------------------------------------------------------------------------------------------------------
  ID             NAME           REMOTE  VER  KEYID           REF-ID  ST  T  LAST  POLL  REACH    DELAY  OFFSET  JITTER
----------------------------------------------------------------------------------------------------------------------
* 1       172.17.0.2       172.17.0.2    3     55           15.1.1.4 2  U    66    64      7    0.000   0.000   0.000
  2       172.17.0.3       172.17.0.3    3      -           15.1.1.3 2  U    66    64      7    0.126   0.029   0.016
----------------------------------------------------------------------------------------------------------------------

switch# show ntp status

NTP is enabled
NTP authentication is enabled
Synchronized to NTP Server 172.17.0.2 at stratum 3
Poll interval = 64 seconds
Time accuracy is within 0.016 seconds
Reference time: Thu Jan 28 2016 20:32:55.639

```

#### Test fail criteria

If the REF-ID status is .NKEY., .INIT., .TIME.,.RATE. or .AUTH., an issue exists with connecting to the NTP server.
