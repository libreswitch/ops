#PING Design

## Contents
   - [High level design of ping](#high-level-design-of-ping)
   - [Design choices](#design-choices)
   - [Internal structure](#internal-structure)
       - [CLI Daemon](#cli-daemon)
   - [References](#references)

## High level design of ping

The Ping application is most commonly used for troubleshooting the accessibility of devices.
It is mostly used to verify connectivity between your switch and a host or port.
OpenSwitch uses open source `ping` and `ping6` from the iputils package for implementing ping functionality.
Ping parameters are obtained from the user through CLI.
Obtained information is stored in a structure and passed to the handler as an argument.
The handler maps the ping parameters entered by the user to the open source ping options and invokes the Linux ping utility.
The handler sends the response obtained from the open source ping to the user through CLI.
The end to end operation is performed in a single thread context as part of CLI Daemon.
No OVSDB interaction or any other module interaction is involved.

## Design choices

There are multiple open source packages available for the ping application.
The open source `Ping` application used is taken from the Linux iputils package.

##Internal structure

```

                     +------------------------------------+
                     |                                    |
                     |                CLI                 |
                     |                                    |
                     +-----------------+------------------+
                                       |
                                       |
                                       |
                                       |
                    +------------------+------------------+
                    |                                     |
                    |             Ping Handler            |
                    |                                     |
                    +-------------------------------------+

```

### CLI Daemon
All information needed by the ping application is obtained from the user through CLI.
The information below is stored in a structure and maintained in the CLI Daemon.

* IPv4-Address
* IPv6-Address
* Hostname
* Datagram-size
* Data-fill pattern
* Timeout value
* Interval value
* Ip-options
* Repetitions value
* Type of Service value


## References
Iputils Package (http://www.skbuff.net/iputils/)

Linux Ping Man page (http://linux.die.net/man/8/ping)
