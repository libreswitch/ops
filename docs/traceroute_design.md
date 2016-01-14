# Traceroute Design

## Contents
   - [High level design of traceroute](#high-level-design-of-traceroute)
   - [Design choices](#design-choices)
   - [Internal structure](#internal-structure)
       - [CLI Daemon](#cli-daemon)
   - [References](#references)

## High level design of traceroute

Traceroute is a computer network diagnostic tool for displaying the route (path), and measuring transit delays of packets
across an Internet Protocol (IP) network.
OpenSwitch uses open source `traceroute` from the inetutils package for implementing traceroute functionality.
OpenSwitch uses open source `traceroute6` from the iputils package for implementing traceroute6 functionality.
Traceroute parameters are obtained from the user through CLI.
Obtained information is stored in a structure and passed to the handler as an argument.
The handler maps traceroute parameters entered by the user to the open source traceroute options and invokes the Linux traceroute utility.
The handler sends the response obtained from the open source traceroute back to the user through CLI.
The end to end operation is performed in a single thread context as part of the CLI Daemon.
No OVSDB interaction or any other module interaction is involved.

## Design choices

There are multiple open source packages available for the traceroute application.
The open source `Traceroute` application used is taken from the Linux inetutils package.
The open source `Traceroute6` application used is taken from the Linux iputils package.

## Internal structure

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
                    |             Traceroute Handler      |
                    |                                     |
                    +-------------------------------------+

```

### CLI Daemon
All information needed by the traceroute application is obtained from the user through CLI.
The information below is stored in a structure and maintained in the CLI Daemon.

* IPv4-Address
* IPv6-Address
* Hostname
* Maximum TTL
* Minimum TTL
* Timeout value
* Destination port
* Probes
* Ip-option loose source route



## References
Inetutils Package (http://www.gnu.org/software/inetutils/)

Iputils Package   (http://www.skbuff.net/iputils/iputils-current.tar.bz2)

Linux Traceroute Man page (http://linux.die.net/man/8/traceroute)
