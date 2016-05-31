# Access Control List (ACL) Commands

## Contents

- [Configuration context](#configuration-context)
  - [Creation, modification, and deletion](#creation-modification-and-deletion)
  - [Log timer](#log-timer)
  - [Reset](#reset)
- [Interface configuration context](#interface-configuration-context)
  - [Application, replacement, and removal](#application-replacement-and-removal)
- [VLAN configuration context](#vlan-configuration-context)
  - [Application, replacement, and removal](#application-replacement-and-removal-1)
- [Global context](#global-context)
  - [Display](#display)
  - [Statistics \(hit counts\)](#statistics-hit-counts)
  - [Log timer](#log-timer-1)

## Configuration context

### Creation, modification, and deletion

#### Syntax

```
[no] access-list ip <acl-name>

    [no] [<sequence-number>]
         {permit|deny}
         {any|ah|gre|esp|icmp|igmp|pim|<ip-protocol-num>}
         {any|<src-ip-address>[/{<prefix-length>|<subnet-mask>}]}
         {any|<dst-ip-address>[/{<prefix-length>|<subnet-mask>}]}
         [count] [log]

    [no] [<sequence-number>]
         {permit|deny}
         {sctp|tcp|udp}
         {any|<src-ip-address>[/{<prefix-length>|<subnet-mask>}]}
         [{eq|gt|lt|neq} <port>|range <min-port> <max-port>]
         {any|<dst-ip-address>[/{<prefix-length>|<subnet-mask>}]}
         [{eq|gt|lt|neq} <port>|range <min-port> <max-port>]
         [count] [log]

    [no] [<sequence-number>]
         comment ...
```

#### Description

Creates an access control list (ACL) comprised of one or more access control
list entries (ACEs) that are ordered and prioritized by sequence numbers.

The `no` keyword is used to delete either an ACL or an individual ACE.

An applied ACL processes a packet sequentially against entries in the list
until either the the packet matches an ACE or the last ACE in the list has
been evaluated. If no ACEs are matched, the packet is denied (each ACL has an
implicit default-deny ACE).

**Note:** An ACL must be applied using the `apply` command (at interface context)
before it has an effect on traffic. If an ACL with no user-created
entries is applied, it denies all traffic on the applied interface
(since only the implicit default-deny ACE is present).

Entering an existing *acl-name* value causes modification to the existing ACL,
with any new *sequence-number* value creating an additional ACE, and
any existing *sequence-number* value replacing an existing ACE with that same
sequence number.

If no sequence number is specified, ACEs are appended to the end of the ACL
with a sequence number equal to the highest ACE currently in the list plus 10.

#### Authority

Admin.

#### Parameters

| Name                | Status   | Syntax                     | Description |
|---------------------|----------|----------------------------|-------------|
| *ip*                | Required | Keyword                    | Create or modify an IPv4 ACL. |
| *acl-name*          | Required | String                     | The name of the ACL. |
| **sequence-number** | Optional | Integer (1-4294967295)     | A sequence number for the ACE. |
| *action*            | Required | Keyword                    | Permit or deny traffic matching the ACE. |
| *comment*           | Required | Keyword                    | Store the remaining entered text as an ACE comment. |
| *ip-protocol*       | Required | Keyword or Integer (1-255) | An IP protocol number or name. |
| *src-ip-address*    | Required | IP Address or Keyword      | The source IP host, network address, or `any`. |
| *dst-ip-address*    | Required | IP Address or Keyword      | The destination IP host, network address, or `any`. |
| **prefix-length**   | Optional | Integer (1-32)             | The address bits to mask (CIDR subnet mask notation). |
| **subnet-mask**     | Optional | Dotted Subnet Mask         | The address bits to mask (dotted decimal notation). |
| **eq**              | Optional | Keyword                    | Layer 4 port is equal to *port*. |
| **gt**              | Optional | Keyword                    | Layer 4 port is greater than *port*. |
| **lt**              | Optional | Keyword                    | Layer 4 port is less than *port*. |
| **neq**             | Optional | Keyword                    | Layer 4 port is not equal to *port*. |
| **port**            | Optional | Integer (0-65535)          | A single Layer 4 port. |
| **range**           | Optional | Keyword                    | Layer 4 port between *min-port*-*max-port* (inclusive). |
| **min-port**        | Optional | Integer (0-65535)          | The start of a  Layer 4 port range. |
| **max-port**        | Optional | Integer (0-65535)          | The end of a Layer 4 port range. |
| **count**           | Optional | Keyword                    | Keep hit counts of the number of packets matching the ACE. |
| **log**             | Optional | Keyword                    | Keep a log of the number of packets matching the ACE. |

#### Examples

Create an ACL with three entries:

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 10 permit udp any 172.16.1.0/24
switch(config-acl)# 20 permit tcp 172.16.2.0/16 gt 1023 any
switch(config-acl)# 30 deny any any any count
switch(config-acl)# exit
```

Add a comment to an existing ACE:
```
switch(config)# access-list ip My_ACL
switch(config-acl)# 20 comment Permit all TCP ephemeral ports
switch(config-acl)# do show access-list
switch(config-acl)# exit
```

Add an ACE to an existing ACL:

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 25 permit icmp 172.16.2.0/16 any
switch(config-acl)# exit
```

Replace an ACE in an existing ACL:

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 25 permit icmp 172.17.1.0/16 any
switch(config-acl)# exit
```

Remove an ACE from an ACL:

```
switch(config)# access-list ip My_ACL
switch(config-acl)# no 25
switch(config-acl)# exit
```

Remove an ACL:

```
switch(config)# no access-list ip My_ACL
```

### Reset

#### Syntax

```
reset access-list all
```

#### Description

Reset the configuration and application of all ACLS to match the active
configuration. Active configuration means the configuration has passed platform
support and capacity checks and is either programmed or pending programming in
hardware.

#### Authority

Admin.

#### Parameters

| Name       | Status   | Syntax  | Description |
|------------|----------|---------|-------------|
| *all*      | Required | Keyword | Operate on all ACLs. |

#### Examples

Reset the entry configuration and application of all ACLs:

```
switch(config)# reset access-list all
```

### Log timer

#### Syntax

```
access-list log-timer {default|<value>}
```

#### Description

Set the log timer frequency for all ACEs with `log` configured.

The first packet that matches an entry with the `log` keyword within an ACL log
timer window (configured with `access-list log-timer`) has its header
contents extracted and sent to the configured logging destination (for example,
console or syslog server). Each time the ACL log timer expires, a summary of all
ACEs with `log` configured is sent to the logging destination.

#### Authority

Admin.

#### Parameters

| Name      | Status   | Syntax           | Description |
|-----------|----------|------------------|-------------|
| *default* | Required | Keyword          | Reset to the default value (300 seconds). |
| *value*   | Required | Integer (30-300) | Specify a value (in seconds). |

#### Examples

Set the ACL log timer to 120 seconds:

```
switch(config)# access-list log-timer 120
```

Reset the ACL log timer to the default value:

```
switch(config)# access-list log-timer default
```

## Interface configuration context

### Application, replacement, and removal

#### Syntax

```
[no] apply access-list ip <acl-name> {in|out}
```

#### Description

Apply an ACL to the current interface context.

Only one direction (for example, inbound) and type (for example, IPv4) of ACL
may be applied to an interface at a time, thus using the `apply` command on
an interface with an already-applied ACL of the same direction and type
replaces the currently-applied ACL.

#### Authority

Admin.

#### Parameters

| Name        | Status   | Syntax  | Description |
|-------------|----------|---------|-------------|
| *ip*        | Required | Keyword | Apply an IPv4 ACL. |
| *acl-name*  | Required | String  | Name of the ACL to apply. |
| *direction* | Required | Keyword | Choose *in* to apply to inbound (ingress) traffic or *out* for outbound (egress) traffic. |

#### Examples

Apply *My_ACL* to ingress traffic on interfaces 1 and 2

```
switch(config)# interface 1
switch(config-if)# apply access-list ip My_ACL in
switch(config-if)# exit
switch(config)# interface 2
switch(config-if)# apply access-list ip My_ACL in
switch(config-if)# exit
switch(config)#
```

Replace *My_ACL* with *My_Replacement_ACL* on interface 1
(following the above example, *My_ACL* remains applied to interface 2):

```
switch(config)# interface 1
switch(config-if)# apply access-list ip My_Replacement_ACL in
switch(config-if)# exit
switch(config)#
```

Apply no ACL on interface 1
(following the above example, *My_ACL* remains applied to interface 2):

```
switch(config)# interface 1
switch(config-if)# no apply access-list ip My_Replacement_ACL in
switch(config-if)# exit
switch(config)#
```

## VLAN configuration context

**Note**: Applying ACLs to VLANs is not yet supported by all OpenSwitch
          components. The CLI commands presented in this document are
          available, but the ACLs are not programmed unless all components
          are enhanced to support VLAN ACL apply operations.*

### Application, replacement, and removal

#### Syntax

```
[no] apply access-list ip <acl-name> {in|out}
```

#### Description

Apply an ACL to the current VLAN context.

Only one direction (for example, inbound) and type (for example, IPv4) of ACL
may be applied to a VLAN at a time, thus using the `apply` command on a VLAN
with an already-applied ACL of the same direction and type replaces the
currently-applied ACL.

#### Authority

Admin.

#### Parameters

| Name        | Status   | Syntax  | Description |
|-------------|----------|---------|-------------|
| *ip*        | Required | Keyword | Apply an IPv4 ACL. |
| *acl-name*  | Required | String  | Name of the ACL to apply. |
| *direction* | Required | Keyword | Choose *in* to apply to inbound (ingress) traffic or *out* for outbound (egress) traffic. |

#### Examples

Apply *My_ACL* to ingress traffic on VLANs 1 and 2

```
switch(config)# vlan 1
switch(config-vlan)# apply access-list ip My_ACL in
switch(config-vlan)# exit
switch(config)# vlan 2
switch(config-vlan)# apply access-list ip My_ACL in
switch(config-vlan)# exit
switch(config)#
```

Replace *My_ACL* with *My_Replacement_ACL* on VLAN 1
(following the above example, *My_ACL* remains applied to VLAN 2):

```
switch(config)# vlan 1
switch(config-vlan)# apply access-list ip My_Replacement_ACL in
switch(config-vlan)# exit
switch(config)#
```

Apply no ACL on VLAN 1
(following the above example, *My_ACL* remains applied to VLAN 2):

```
switch(config)# vlan 1
switch(config-vlan)# no apply access-list ip My_Replacement_ACL in
switch(config-vlan)# exit
switch(config)#
```

## Global context

### Display

#### Syntax

```
show access-list [{interface|vlan} <id> [{in|out}]] [ip] [<acl-name>] [config]
```

#### Description

Displays configured, active ACLs and their entries.

By default, `show access-list` displays the ACL configuration active in the
system. Active configuration means the configuration has passed platform
support and capacity checks, and is either programmed or pending programming in
hardware.

By specifying the `configuration` token, the user-specified
configuration is displayed, whether or not it is active. This command
displays a warning if the active and user-specified configuration do not match.
In such a case, the user may wish to use the `reset access-list` command
(see [reset](#reset)).

Specifying `commands` displays active ACL entries as well as the state of
any `apply` commands on interfaces.

#### Authority

Admin.

#### Parameters

| Name          | Status   | Syntax  | Description |
|---------------|----------|---------|-------------|
| **interface** | Optional | Keyword | Display ACLs applied to a specified interface name. |
| **vlan**      | Optional | Keyword | Display ACLs applied to a specified VLAN ID. |
| **id**        | Optional | String  | The name or ID of the interface or VLAN. |
| **direction** | Optional | String  | Choose **in** to limit display to ingress ACLs or **out** for egress ACLs. |
| **ip**        | Optional | Keyword | Limit display to IPv4 ACLs. |
| **acl-name**  | Optional | String  | Display the ACL matching the name. |
| **commands**  | Optional | String  | Display output as CLI commands. |
| **configuration** | Optional | String  | Display the user-specified configuration. |

#### Examples

Display ACLs configured in examples from previous sections:

```
switch# show access-list
Type       Name
  Sequence Comment
           Action                          L3 Protocol
           Source IP Address               Source L4 Port(s)
           Destination IP Address          Destination L4 Port(s)
           Additional Parameters
-------------------------------------------------------------------------------
IPv4       My_ACL
        10 permit                          udp
           any
           172.16.1.0/24
        20 Permit all TCP ephemeral ports
           permit                          tcp
           172.16.2.0/16                    >  1023
           any
        30 deny                            any
           any
           any
           Hit-counts: enabled
-------------------------------------------------------------------------------
```

Display ACLs configured and applied in above examples as CLI commands:

```
switch# show access-list commands
access-list ip My_ACL
    10 permit udp any 172.16.1.0/24
    20 permit tcp 172.16.2.0/16 gt 1023 any
    30 deny any any any count
interface 2
    apply access-list ip My_ACL in
```

### Statistics (hit counts)

#### Syntax

```
show access-list hitcounts ip <acl-name> [{interface|vlan} <id> [{in|out}]]

clear access-list hitcounts {all|ip <acl-name> {interface|vlan} <id> [{in|out}]}
```

#### Description

Display or clear hit counts for ACEs with the `count` keyword in the specified
ACL.

If an entry does not have the `count` keyword enabled, it displays the `-`
character instead of a hit count.

#### Authority

Admin.

#### Parameters

| Name          | Status   | Syntax  | Description |
|---------------|----------|---------|-------------|
| *all*         | Required | Keyword | Operate on all ACLs. |
| *ip*          | Required | Keyword | Operate on an IPv4 ACL. |
| *acl-name*    | Required | String  | Operate on a named ACL. |
| **interface** | Optional | Keyword | Specify the interface to which the ACL is applied. |
| **vlan**      | Optional | Keyword | Specify the VLAN to which the ACL is applied. |
| **id**        | Optional | String  | The name or ID of the interface or VLAN. |
| **direction** | Optional | Keyword | Choose **in** to operate on ACLs applied to ingress traffic or **out** for egress traffic. |

#### Examples

Display hit counts for ACL configured in above examples:

```
switch# show access-list hitcounts ip My_ACL interface 1
Statistics for ACL My_ACL (ipv4):
Interface 1 (in):
           Hit Count  Configuration
                   -  10 permit udp any 172.16.1.0/24
                   -  20 permit tcp 172.16.2.0/16 gt 1023 any
                   0  30 deny any any any count
```

Clear hit counts for ACL configured in above examples:

```
switch# clear access-list hitcounts ip My_ACL interface 1
```

Clear hit counts for all configured ACLs:

```
switch# clear access-list hitcounts all
```

### Log timer

#### Syntax

```
show access-list log-timer
```

#### Description

Display ACL log timer configuration. See [log timer](#log-timer) configuration
for information on changing this setting.

#### Authority

Admin.

#### Parameters

No parameters.

#### Examples

```
switch# show access-list log-timer
```
