# Access Control Lists (ACLs)

##  Contents
- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
    - [Setting up the basic configuration](#setting-up-the-basic-configuration)
    - [Verifying the configuration](#verifying-the-configuration)
    - [Active configuration versus user-specified configuration](#active-configuration-versus-user-specified-configuration)
    - [Displaying ACL hitcounts](#displaying-acl-hitcounts)
    - [ACL Logging](#acl-logging)
    - [Configure the ACL logging timer](#configure-the-acl-logging-timer)
    - [Displaying hardware resource usage](#displaying-hardware-resource-usage)
    - [Troubleshooting the configuration](#troubleshooting-the-configuration)
         - [IP traffic that was not explicitly denied is blocked](#ip-traffic-that-was-not-explicitly-denied-is-blocked)
         - [An empty ACL is applied to an interface and all IP traffic is blocked](#an-empty-acl-is-applied-to-an-interface-and-all-ip-traffic-is-blocked)
         - [An ACL is applied and is not blocking traffic](#an-acl-is-applied-and-is-not-blocking-traffic)
         - [Permitted traffic is denied or denied traffic is permitted](#permitted-traffic-is-denied-or-denied-traffic-is-permitted)
- [CLI](#cli)
- [REST](#rest)

## Overview
ACLs can be used to help improve network performance and restrict network usage
by creating policies to eliminate unwanted IP traffic by filtering packets where
they enter the switch on layer 2 and layer 3 interfaces.

An access control list (ACL) is an ordered list of one or more access control
list entries (ACEs) prioritized by sequence number. An incoming packet is
matched sequentially against each entry in an ACL.  When a match is made, the
action of that ACE is taken and the packet is not compared against any other
ACEs in the list.


For ACL filtering to take effect, configure an ACL and then assign it in the
inbound direction on either a layer 2 or layer 3 interface.

**Note:** Every ACL is configured with a `deny any any any` entry as the last
entry in the list.  This entry is known as the implicit deny entry, and applies
to all IP traffic that does not match any sequentially higher (numerically
lower) entry in the list.  The implicit deny entry will not filter traffic of a
type different from the ACL.  For example, an IP ACL applies to IPv4 traffic
only, it will not filter IPv6 traffic.  An ACL with no user configured entries
that is applied to an interface, is programmed in hardware with the implicit
deny entry.

**Note:** ACLs are supported on split interfaces.  ACLs are not supported on
sub-interfaces.


## How to use the feature

### Setting up the basic configuration
Prior to applying an ACL to an interface, verify that traffic is flowing as
expected through the device.


Create an ACL:

    switch(config)# access-list ip testACL


Add one or more entries to the list:

    switch(config-acl)# 10 permit udp any 172.16.1.0/24
    switch(config-acl)# 20 permit tcp 172.16.2.0/16 gt 1023 any
    switch(config-acl)# 30 deny any any any count
    switch(config-acl)# exit


Apply the ACL to an interface:

    switch(config)# interface 1
    switch(config-if)# apply access-list ip testACL in
    switch(config-if)# exit

Delete an ACL

    switch(config)# no access-list ip testACL

If an ACL is deleted while applied to any interfaces, the ACL automatically is
unapplied from all interfaces.

### Verifying the configuration

Use the following show commands to display the ACL configuration:

    show access-list [{interface} <id> [in]] [ip] [<acl-name>] [commands] [configuration]


The following refers to the above basic configuration example.

Show the ACL applied to interface 1:

    switch# show access-list interface 1 in
    Direction
    Type       Name
      Sequence Comment
           Action                          L3 Protocol
           Source IP Address               Source L4 Port(s)
           Destination IP Address          Destination L4 Port(s)
           Additional Parameters
    -------------------------------------------------------------------------------
    Inbound
    IPv4       testACL
        10 permit                          udp
           any
           172.16.1.0/255.255.255.0
        20 permit                          tcp
           172.16.2.0/255.255.0.0           >  1023
           any
        30 deny                            any
           any
           any
           Hit-counts: enabled
    -------------------------------------------------------------------------------

Show all active ACLs configured on the system:


    switch# show access-list
    Type       Name
      Sequence Comment
           Action                          L3 Protocol
           Source IP Address               Source L4 Port(s)
           Destination IP Address          Destination L4 Port(s)
           Additional Parameters
    -------------------------------------------------------------------------------
    IPv4       100
        10 permit                          tcp
           1.1.1.1/255.255.255.0
           2.2.2.2/255.255.255.0            >  1024
        20 permit                          udp
           1.1.1.1/255.255.255.0
           2.2.2.2/255.255.255.0            >  1024
    -------------------------------------------------------------------------------
    IPv4       testACL
        10 permit                          udp
           any
           172.16.1.0/255.255.255.0
        20 permit                          tcp
           172.16.2.0/255.255.0.0           >  1023
           any
        30 deny                            any
           any
           any
           Hit-counts: enabled
    -------------------------------------------------------------------------------

Show all ACLs configured by the user:

    switch# show access-list configuration
    Type       Name
      Sequence Comment
           Action                          L3 Protocol
           Source IP Address               Source L4 Port(s)
           Destination IP Address          Destination L4 Port(s)
           Additional Parameters
    -------------------------------------------------------------------------------
    IPv4       100
        10 permit                          tcp
           1.1.1.1/255.255.255.0
           2.2.2.2/255.255.255.0            >  1024
        20 permit                          udp
           1.1.1.1/255.255.255.0
           2.2.2.2/255.255.255.0            >  1024
    -------------------------------------------------------------------------------
    IPv4       testACL
        10 permit                          udp
           any
           172.16.1.0/255.255.255.0
        20 permit                          tcp
           172.16.2.0/255.255.0.0           >  1023
           any
        30 deny                            any
           any
           any
           Hit-counts: enabled
    -------------------------------------------------------------------------------

Show the ACLs in command line format:

    switch# show access-list commands
    access-list ip 100
        10 permit tcp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
        20 permit udp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
    access-list ip testACL
        10 permit udp any 172.16.1.0/255.255.255.0
        20 permit tcp 172.16.2.0/255.255.0.0 gt 1023 any
        30 deny any any any count
    interface 1
        apply access-list ip testACL in


### Active configuration versus user-specified configuration

The output from the `show access-list` command displays the active configuration
of the product.  The active configuration displays the ACLs that have been
configured and accepted by the system.  In the case of applied ACLs, the active
configuration displays the interfaces on which the ACLs have successfully been
programmed in hardware.

The output from the `show access-list` command with the `configuration` option,
displays the ACLs that have been configured by the user. The output of this
command may not be the same as what was programmed in hardware or what is active
on the product. Unsupported command parameters may have been configured,
unsupported applications may have been specified, or an application of an ACL
may have been unsuccessful due to a lack of hardware resources. To determine if
there is a discrepancy between what was configured and what is active, run
either the `show access-list commands` command or the `show access-list commands
configuration` command. If the active ACLs and configured ACLs are not the same,
a warning message is displayed.

```
Warning: user-specified access-list apply does not match active configuration
```

If the warning message is displayed, additional changes may be made until the
error message is no longer displayed when `show access-list commands` or `show
access-list commands configuration` is entered, or run the `reset access-list`
command. The `reset access-list` command changes the user-specified
configuration to match the active configuration.

    reset access-list {all | ip <acl-name>}

Example:

    switch(config)# access-list ip testACL
    switch# show access-list commands configuration

Change the source L4 port operator of entry 20 to be neq, which is unsupported
by hardware:

    switch(config-acl)# 20 permit tcp 172.16.2.0/16 neq 1023 any

Display the user-specified configuration:

    switch# show access-list commands configuration
    access-list ip 100
        10 permit tcp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
        20 permit udp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
    access-list ip testACL
        10 permit udp any 172.16.1.0/255.255.255.0
        20 permit tcp 172.16.2.0/255.255.0.0 neq 1023 any /* neq is an unsupported parameter in hw */
        30 deny any any any count
    interface 1
        apply access-list ip testACL in
    % Warning: user-specified access-list apply does not match active configuration

Reset the user-specified configuration to the active configuration:

    switch(config)# reset access-list all

Display the updated user-configuration:

    switch# show access-list commands configuration
    access-list ip 100
        10 permit tcp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
        20 permit udp 1.1.1.1/255.255.255.0 2.2.2.2/255.255.255.0 gt 1024
    access-list ip testACL
        10 permit udp any 172.16.1.0/255.255.255.0
        20 permit tcp 172.16.2.0/255.255.0.0 gt 1023 any
        30 deny any any any count
    interface 1
        apply access-list ip testACL in


### Displaying ACL hitcounts
Hitcounts are available for ACEs that are created with the `count` keyword
specified, as in entry 30 in the example ACL testACL.  The ACL must be applied
to an interface and actively configured for the hitcounts to be valid.

    switch# show access-list hitcounts ip testACL interface 1 in
    Statistics for ACL testACL (ipv4):
    Interface 1 (in):
               Hit Count  Configuration
                       -  10 permit udp any 172.16.1.0/255.255.255.0
                       -  20 permit tcp 172.16.2.0/255.255.0.0 gt 1023 any
                    2045  30 deny any any any count

**Note:** In the above output, only entry 30 displays a numerical hitcount.
Entry 30 is the only ACE that contains the `count` keyword.


### ACL Logging
ACL logging is a useful tool for troubleshooting ACLs. It can identify traffic
in the following scenarios:

1. Traffic is expected to be permitted and is blocked.
2. Unexpected traffic in the network.

When the `log` keyword is specified for an ACE, packets that match this entry
are copied to the switch CPU for processing by the ACL logging feature. The
first packet that matches any log-enabled ACE in an ACL are logged to the
configured system log. The reception of this packet also starts the ACL logging
timer. Subsequent packets that match log-enabled ACEs are not logged to the
system log for the duration of the ACL logging timer. When the ACL logging timer
expires, a list of all the ACLs with logging enabled ACEs and their
corresponding hitcounts, are logged to the system log. The next packet that
matches a log-enabled ACE is logged, repeating the process of starting the ACL
logging timer. The ACL logging feature displays the ACL hitcounts stored in the
database, which are read from hardware every five seconds.

Setting the `log` keyword in an ACE automatically sets the `count` keyword in
the ACE, enabling statistics for the purpose of reporting hitcounts when the
logging timer expires.

Configure an ACL entry for logging:

    switch(config)# access-list ip testACL
    switch(config-acl)# 30 deny any any any log

Display logging messages through the vtysh shell:

    switch# show vlog daemon ops-switchd

Sample output:

    ops-switchd              |ovs|00833|ops_cls_acl_log|INFO|List testACL,
    seq#30 denied udp 172.16.2.15(1564) -> 17.77.115.80(1780) on vlan 1, port 1,
    direction in

Output after the ACL logging timer expires:

    ops-switchd              |ovs|00838|ops_cls_acl_log|INFO|testACL on 1 (in):
    2544008  30 deny any any any log

Display logging messages through the Linux shell:

    root@switch:~# tail -f /var/log/messages | grep ops_cls_acl_log

    2016-06-05T00:00:03.432+00:00 ops-switchd: ovs|05237|ops_cls_acl_log|INFO|List
    testACL, seq#30 denied 172.16.2.15(1564) -> 17.77.115.80(1780) on vlan 1, port 3,
    direction in

    2016-06-05T00:00:33.507+00:00 ops-switchd: ovs|05238|ops_cls_acl_log|INFO|test on 1
    (in):      2540076  30 deny any any any log


### Configure the ACL logging timer

    access-list log-timer 30

The default and maximum duration of the ACL logging timer is 300 seconds. The
minimum duration is 30 seconds.

### Displaying hardware resource usage
ACLs consume resources from a limited hardware pool.  An ACL does not consume
hardware resources until it is applied to an interface. More ACLs may be created
than can be applied in hardware. Use the following command to display the
consumption of the hardware resources:

    switch# diag-dump hw-resource basic

Depending on the hardware implementation of ACLs in the product, the command
displays something similar to the following:

    =========================================================================
    [Start] Feature hw-resource Time : Sat Jun  4 12:07:03 2016
    =========================================================================
    -------------------------------------------------------------------------
    [Start] Daemon ops-switchd
    -------------------------------------------------------------------------

    Hardware resource usage:

    Ingress:
                  |Rules |Rules   |Group |Group |Counters |Counters |Meters |Meters
    Feature       |Used  |Maximum |ID    |Used  |Used     |Maximum  |Used   |Maximum
    --------------|------|--------|------|------|---------|-------- |-------|-------
    ospf          |     2|    2048|     1|     1|        2|     2048|      0|   4096
    copp          |    20|    1280|     2|     1|        0|     1792|      0|   4096
    aclv4         |     4|     512|     4|     1|        0|      512|      0|   4096
    l3intf        |     8|    1792|     5|     1|        8|     1792|      0|   4096

    Egress:
                  |Rules |Rules   |Group |Group |Counters |Counters |Meters |Meters
    Feature       |Used  |Maximum |ID    |Used  |Used     |Maximum  |Used   |Maximum
    --------------|------|--------|------|------|---------|-------- |-------|-------
    copp          |  20  |     512|     1|     1|      40 |    1024 |     40|    768

### Troubleshooting the configuration

#### IP traffic that was not explicitly denied is blocked
##### Cause
The implicit deny entry is blocking the traffic.
##### Remedy
Add an ACE to explicitly permit the traffic.

#### An empty ACL is applied to an interface and all IP traffic is blocked
##### Cause
The implicit deny entry is blocking the traffic.
##### Remedy
Add an ACE to explicitly permit the traffic.

#### An ACL is applied and is not blocking traffic
##### Cause
The ACL has been configured but is not active.
##### Remedy
Run the command `show access-list commands`.  If a warning message is displayed,
issue the `reset access-list` command.  Re-run `show access-list commands` to
verify the warning message is no longer displayed.

#### Permitted traffic is denied or denied traffic is permitted
##### Cause
Misconfigured ACL.
##### Remedy
Enable the `count` keyword on the troublesome ACEs. While sending traffic, run
the ACL hitcount show command and monitor the counts of the ACEs.

## CLI
For the detailed list of ACL configuration commands, refer to the
[Access Control List CLI Guide](http://openswitch.net/documents/user/access_list_cli).

## REST
The REST interface may be used to retrieve information about configured ACLs.
For more information on REST, refer to the
[REST User Guide](http://openswitch.net/documents/user/rest_api_user_guide).
