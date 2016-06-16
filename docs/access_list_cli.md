# Access Control List (ACL) Commands

## Contents

- [Configuration context](#configuration-context)
  - [Creation, modification, and deletion](#creation-modification-and-deletion)
  - [Log timer](#log-timer)
- [Interface configuration context](#interface-configuration-context)
  - [Application, replacement, and removal](#application-replacement-and-removal)
- [VLAN configuration context](#vlan-configuration-context)
  - [Application, replacement, and removal](#application-replacement-and-removal-1)
- [Global context](#global-context)
  - [Display](#display)
  - [Statistics \(hit counts\)](#statistics-hit-counts)

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
list entries (ACEs) ordered and prioritized by sequence numbers.

The `no` keyword can be used to delete either an ACL or an individual ACE.

An applied ACL will process a packet sequentially against entries in the list
until either the last ACE in the list has been evaluated or the packet matches
an ACE. If no ACEs are matched, the packet will be denied (each ACL has an
implicit default-deny ACE).

Note that an ACL must be applied via the `apply` command (at interface context)
before it will have an effect on traffic. If an ACL with no user-created
entries is applied, it will deny all traffic on the applied interface
(since only the implicit default-deny ACE will be present).

Entering an existing *acl-name* value will cause the existing ACL to be
modified, with any new *sequence-number* value creating an additional ACE, and
any existing *sequence-number* value replacing the existing ACE with the same
sequence number.

If no sequence number is specified, ACEs will be appended to the end of the ACL
with a sequence number equal to the highest ACE currently in the list plus 10.

#### Authority

Admin.

#### Parameters

| Name                | Status   | Syntax                     | Description |
|---------------------|----------|----------------------------|-------------|
| *ip*                | Required | Keyword                    | Create or modify an IPv4 ACL. |
| *acl-name*          | Required | String                     | The name of this ACL. |
| **sequence-number** | Optional | Integer (1-4294967295)     | A sequence number for this ACE. |
| *action*            | Required | Keyword                    | Permit or deny traffic matching this ACE. |
| *comment*           | Required | Keyword                    | Store the remaining entered text as an ACE comment. |
| *ip-protocol*       | Required | Keyword or Integer (1-255) | An IP Protocol number or name. |
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
| **count**           | Optional | Keyword                    | Keep hit counts of the number of packets matching this ACE. |
| **log**             | Optional | Keyword                    | Keep a log of the number of packets matching this ACE. |

#### Examples

Create an ACL with three entries

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 10 permit udp any 172.16.1.0/24
switch(config-acl)# 20 permit tcp 172.16.2.0/16 gt 1023 any
switch(config-acl)# 30 deny any any any count
switch(config-acl)# exit
```

Add a comment to an existing ACE
```
switch(config)# access-list ip My_ACL
switch(config-acl)# 20 comment Permit all TCP ephemeral ports
switch(config-acl)# do show access-list
switch(config-acl)# exit
```

Add an ACE to an existing ACL

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 25 permit icmp 172.16.2.0/16 any
switch(config-acl)# exit
```

Replace an ACE in an existing ACL

```
switch(config)# access-list ip My_ACL
switch(config-acl)# 25 permit icmp 172.17.1.0/16 any
switch(config-acl)# exit
```

Remove an ACE from an ACL

```
switch(config)# access-list ip My_ACL
switch(config-acl)# no 25
switch(config-acl)# exit
```

Remove an ACL

```
switch(config)# no access-list ip My_ACL
```

### Log timer

#### Syntax

```
access-list log-timer {default|<value>}
```

#### Description

Set the log timer frequency for all ACEs with `log` configured.

The first packet that matches an entry with the `log` keyword within an ACL log
timer window (configured with `access-list log-timer`) will have its header
contents extracted and sent to the configured logging destination (console,
syslog server, etc.). Each time the ACL log timer expires, a summary of all
ACEs with `log` configured will be sent to the logging destination.

#### Authority

Admin.

#### Parameters

| Name      | Status   | Syntax           | Description |
|-----------|----------|------------------|-------------|
| *default* | Required | Keyword          | Reset to the default value (300 seconds). |
| *value*   | Required | Integer (30-300) | Specify a value (in seconds). |

#### Examples

Set the ACL log timer to 120 seconds.

```
switch(config)# access-list log-timer 120
```

Reset the ACL log timer to the default value.

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

Only one direction (e.g. inbound) and type (e.g. IPv4) of ACL may be applied to
an interface at a time, thus using the `apply` command on an interface with an
already-applied ACL of the same direction and type will replace the currently-
applied ACL.

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
(following the above examples, *My_ACL* remains applied to interface 2)

```
switch(config)# interface 1
switch(config-if)# apply access-list ip My_Replacement_ACL in
switch(config-if)# exit
switch(config)#
```

Apply no ACL on interface 1
(following the above examples, *My_ACL* remains applied to interface 2)

```
switch(config)# interface 1
switch(config-if)# no apply access-list ip My_Replacement_ACL in
switch(config-if)# exit
switch(config)#
```

## VLAN configuration context

### Application, replacement, and removal

#### Syntax

```
[no] apply access-list ip <acl-name> {in|out}
```

#### Description

Apply an ACL to the current VLAN context.

Only one direction (e.g. inbound) and type (e.g. IPv4) of ACL may be applied to
an VLAN at a time, thus using the `apply` command on an VLAN with an
already-applied ACL of the same direction and type will replace the currently-
applied ACL.

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
(following the above examples, *My_ACL* remains applied to VLAN 2)

```
switch(config)# vlan 1
switch(config-vlan)# apply access-list ip My_Replacement_ACL in
switch(config-vlan)# exit
switch(config)#
```

Apply no ACL on vlan 1
(following the above examples, *My_ACL* remains applied to VLAN 2)

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

Displays configured ACLs and their entries.

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
| **acl-name**  | Optional | String  | Display the ACL matching this name. |
| **config**    | Optional | String  | Display output as CLI commands. |

#### Examples

Display ACLs configured in above examples.

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

Display ACLs configured in above examples as config

```
switch# show access-list config
access-list ip My_ACL
    10 permit udp any 172.16.1.0/24
    20 permit tcp 172.16.2.0/16 gt 1023 any
    30 deny any any any count
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

If an entry does not have the `count` keyword enabled, it will display the `-`
character instead of a hit count.

#### Authority

Admin.

#### Parameters

| Name          | Status   | Syntax  | Description |
|---------------|----------|---------|-------------|
| *all*         | Required | Keyword | Operate on all ACLs. |
| *ip*          | Required | Keyword | Operate on an IPv4 ACL. |
| *acl-name*    | Required | String  | Operate on a named ACL. |
| **interface** | Optional | Keyword | Specify the interface the ACL is applied to. |
| **vlan**      | Optional | Keyword | Specify the VLAN the ACL is applied to. |
| **id**        | Optional | String  | The name or ID of the interface or VLAN. |
| **direction** | Optional | Keyword | Choose **in** to operate on ACLs applied to ingress traffic or **out** for egress traffic. |

#### Examples

Display hit counts for ACL configured in above examples.

```
switch# show access-list hitcounts ip My_ACL interface 1
Statistics for ACL My_ACL (ipv4):
Interface 1 (in):
           Hit Count  Configuration
                   -  10 permit udp any 172.16.1.0/24
                   -  20 permit tcp 172.16.2.0/16 gt 1023 any
                   0  30 deny any any any count
```

Clear hit counts for ACL configured in above examples.

```
switch# clear access-list hitcounts ip My_ACL interface 1
```

Clear hit counts for all configured ACLs.

```
switch# clear access-list hitcounts all
```
