# DHCP-TFTP server


## Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuring a DHCP server](#configuring-a-dhcp-server)
   - [Setting up a basic DHCP configuration](#setting-up-a-basic-dhcp-configuration)
      - [Changing to dhcp-server context](#changing-to-dhcp-server-context)
      - [Setting the dynamic range configuration](#setting-the-dynamic-range-configuration)
      - [Setting static configurations](#setting-static-configurations)
      - [Setting the DHCP options configuration](#setting-the-dhcp-options-configuration)
      - [Setting the DHCP match configuration](#setting-the-dhcp-match-configuration)
      - [Setting the DHCP BOOTP configuraion](#setting-the-dhcp-bootp-configuraion)
- [Verifying the DHCP server configuration](#verifying-the-dhcp-server-configuration)
   - [Viewing DHCP server configuration information](#viewing-dhcp-server-configuration-information)
   - [Viewing DHCP server leases information](#viewing-dhcp-server-leases-information)
- [Configuring a TFTP server](#configuring-a-tftp-server)
   - [Setting up a basic TFTP configuration](#setting-up-a-basic-tftp-configuration)
      - [Changing to tftp-server context](#changing-to-tftp-server-context)
      - [Setting the TFTP server configuration](#setting-the-tftp-server-configuration)
      - [Setting the TFTP server secure mode configuration](#setting-the-tftp-server-secure-mode-configuration)
- [Verifying the TFTP server configuration](#verifying-the-tftp-server-configuration)

## Overview
This guide provides details for configuring the DHCP-TFTP server that is present in the switch. All DHCP configurations work in the dhcp-server context. All TFTP configurations work in the tftp-server context.

## Prerequisites
All of the interfaces on which the DHCP-TFTP server listens must be administratively up. To enable a DHCP server, at least one dynamic range configuration must be set. Both the interface IP address and the IP addresses range configured for DHCP clients must be in the same subnet. To configure a static IP address for requests coming to an interface, a dynamic range configuration must be previously set for that interface, and the static IP address and dynamic IP addresses range must be in the same subnet.

## Configuring a DHCP server
### Setting up a basic DHCP configuration
#### Changing to dhcp-server context
The `dhcp-server` command changes the configure terminal context to the dhcp-server context.
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)#
```
#### Setting the dynamic range configuration
The `range <range-name> start-ip-address( <ipv4_address> | <ipv6_address> ) end-ip-address ( <ipv4_address> | <ipv6_address> ) netmask <subnet_mask> broadcast <broadcast_address> match tags <match_tag_names> set tag <set_tag_name> prefix-len <prefix_length_value> lease-duration <lease_duration_value>` static command sets the dynamic range configuration for the DHCP server. Each dynamic range configuration should have a unique name.
- Parameter `start-ip-address` sets the first ip address of the dynamic range.
- Parameter `end-ip-address` sets the last ip address of the dynamic range.
- Parameters `start-ip-address`and `end-ip-address` are not optional.
- Parameter `netmask` sets the subnet mask.
- Parameter `broadcast` sets the broadcast address for the range specified, but it must not be set without setting `netmask`.
- Parameter `prefix-len` sets the prefix length for IPv6 address range. Either IPv4 or IPv6 address can be set for the dynamic range.
- Paramaters `netmask` and `broadcast` should not be specified for IPv6 address range while parameter `prefix-len` must not be set for the IPv4 address range.
- Parameter `set tags` sets alphanumeric labels which marks networks so that dhcp options may be specified on a per-network basis. Only one tag should be specified for this parameter.
- Parameter `match-tags` sets the matching labels. Mutliple tags can be set for this parameter.
- Parameter `lease-duration` sets the lease time. If this parameter is not specified, default value of 60 minutes is set.
```
ops-as5712(config-dhcp-server)# range dynamic_1 start-ip-address 10.0.0.1 end-ip-address 10.255.255.254 netmask 255.0.0.0 broadcast 10.255.255.255 match tags tag1,tag2,tag3 set tag tag4
ops-as5712(config-dhcp-server)# range dynamic start-ip-address 10.0.0.1 end-ip-address 10.255.255.254 netmask 255.0.0.0 broadcast 10.255.255.255 match tags tag1,tag2,tag3 set tag tag4
ops-as5712(config-dhcp-server)#
ops-as5712(config-dhcp-server)#
ops-as5712(config-dhcp-server)# range dynamic_2 start-ip-address 2001:0db8:85a3:0000:0000:8a2e:0370:7334 end-ip-address 2001:0db8:85a3:0000:0000:8a2e:0370:7340  prefix-len 64  match tags tag6,tag7,tag8 set tag tag5
```

To remove the dynamic configuration, use the `no range range <range-name> start-ip-address ( <ipv4_address> | <ipv6_address> ) end-ip-address ( <ipv4_address> | <ipv6_address> ) netmask <subnet_mask> broadcast <broadcast_address> match tags <match_tag_names> set tag <set_tag_name> prefix-len <prefix_length_value> lease-duration <lease_duration_value> static` command.
```
ops-as5712(config-dhcp-server)# no range dynamic_1 start-ip-address 10.0.0.1 end-ip-address 10.255.255.254 netmask 255.0.0.0 broadcast 10.255.255.255 match tags tag1,tag2,tag3 set tag tag4
ops-as5712(config-dhcp-server)# range dynamic start-ip-address 10.0.0.1 end-ip-address 10.255.255.254 netmask 255.0.0.0 broadcast 10.255.255.255 match tags tag1,tag2,tag3 set tag tag4
ops-as5712(config-dhcp-server)#
ops-as5712(config-dhcp-server)#
ops-as5712(config-dhcp-server)# no range dynamic_2 start-ip-address 2001:0db8:85a3:0000:0000:8a2e:0370:7334 end-ip-address 2001:0db8:85a3:0000:0000:8a2e:0370:7340  prefix-len 64  match tags tag6,tag7,tag8 set tag tag5
```
#### Setting static configurations
The `static  ( <ipv4_address> | <ipv6_address> ) match-mac-addresses <mac_addresses> match-client-hostname <hostname> match-client-id <client-id> set tags <set_tag_names> lease-duration <lease_duration_value>'`command sets the static IP allocation configuration.
- Parameter `static` sets the ip address for the static ip address allocation.
- Parameter `match-mac-addresses` sets the MAC address of the client. The user can specify multiple MAC addresses for the static IP but only one MAC address should be active at any point.
- Paremeters `match-client-hostname` and `match-client-id` sets the client hostname and clied ID respectively.
- Parameters `match-mac-addresses`, `match-client-hostname` and `match-client-id` are optional but at lease one of these three parameters should be specified.
- Paramater `set tags` sets alphanumeric labels which marks networks so that dhcp options may be specified on a per-network basis.
- Parameter `set tags` is optional. If specified, mutliple tags can be set.
-  Parameter `lease-duration` sets the lease time. If this parameter is not specified, default value of 60 minutes is set.
```
ops-as5712(config-dhcp-server)#
ops-as5712(config-dhcp-server)#
ops-as5712(config-dhcp-server)# static 10.0.0.5 match-mac-addresses 36:d4:1b:12:ea:52 match-client-hostname 95_h2 set tags tag1,tag2,tag3 lease-duration 65
```
To remove the static configuration, use the `no static  ( <ipv4_address> | <ipv6_address> ) match-mac-addresses <mac_addresses> match-client-hostname <hostname> match-client-id <client-id> set tags <set_tag_names> lease-duration <lease_duration_value>` command.
```
ops-as5712(config-dhcp-server)#
ops-as5712(config-dhcp-server)#
ops-as5712(config-dhcp-server)# no static 10.0.0.5 match-mac-addresses 36:d4:1b:12:ea:52 match-client-hostname 95_h2 set tags tag1,tag2,tag3 lease-duration 65
```
#### Setting the DHCP options configuration
The  `set option-name <option_name> option-value <option_value>  match tags <match_tag_names> ipv6` command sets the DHCP options by specifying the option-name, and the `option set option-number <option_number> option-value <option_value>  match tags <match_tag_names> ipv6` command sets the DHCP options by specifying the option-number.

- Parameer `option-name` sets the DHCP option name,
- Parameter `option-number` sets the DHCP option number.
- Parameter `option-value` sets the DHCP option value.
- Parameter `match-tags` sets the matching labels (optional).
```
The list of supported `option-name` and corresponding `option-number` for IPv4 are:

| option-name              | option-number |
|--------------------------|---------------|
| netmask                  | 1             |
| time-offset              | 2             |
| router                   | 3             |
| dns-server               | 6             |
| log-server               | 7             |
| lpr-server               | 9             |
| hostname                 | 12            |
| boot-file-size           | 13            |
| domain-name              | 15            |
| swap-server              | 16            |
| root-path                | 17            |
| extension-path           | 18            |
| ip-forward-enable        | 19            |
| non-local-source-routing | 20            |
| policy-filter            | 21            |
| max-datagram-reassembly  | 22            |
| default-ttl              | 23            |
| mtu                      | 26            |
| all-subnets-local        | 27            |
| broadcast                | 28            |
| router-discovery         | 31            |
| router-solicitation      | 32            |
| static-route             | 33            |
| trailer-encapsulation    | 34            |
| arp-timeout              | 35            |
| ethernet-encap           | 36            |
| tcp-ttl                  | 37            |
| tcp-keepalive            | 38            |
| nis-domain               | 40            |
| nis-server               | 41            |
| ntp-server               | 42            |
| vendor-encap             | 43            |
| netbios-ns               | 44            |
| netbios-dd               | 45            |
| netbios-nodetype         | 46            |
| netbios-scope            | 47            |
| x-windows-fs             | 48            |
| x-windows-dm             | 49            |
| requested-address        | 50            |
| lease-time               | 51            |
| option-overload          | 52            |
| message-type             | 53            |
| server-identifier        | 54            |
| parameter-request        | 55            |
| message                  | 56            |
| max-message-size         | 57            |
| T1                       | 58            |
| T2                       | 59            |
| vendor-class             | 60            |
| client-id                | 61            |
| nis+-domain              | 64            |
| nis+-server              | 65            |
| tftp-server              | 66            |
| bootfile-name            | 67            |
| mobile-ip-home           | 68            |
| smtp-server              | 69            |
| pop3-server              | 70            |
| nntp-server              | 71            |
| irc-server               | 74            |
| user-class               | 77            |
| FQDN                     | 81            |
| agent-id                 | 82            |
| client-arch              | 93            |
| client-interface-id      | 94            |
| client-machine-id        | 97            |
| subnet-select            | 118           |
| domain-search            | 119           |
| sip-server               | 120           |
| classless-static-route   | 121           |
| vendor-id-encap          | 125           |
| server-ip-address        | 255           |

The list of supported `option-name` and corresponding `option-number` for IPv6 are:

| option-name              | option-number |
|--------------------------|---------------|
| client-id                | 1             |
| server-id                | 2             |
| ia-na                    | 3             |
| ia-ta                    | 4             |
| iaaddr                   | 5             |
| oro                      | 6             |
| preference               | 7             |
| unicast                  | 12            |
| status                   | 13            |
| rapid-commit             | 14            |
| user-class               | 15            |
| vendor-class             | 16            |
| vendor-opts              | 17            |
| sip-server-domain        | 21            |
| sip-server               | 22            |
| dns-server               | 23            |
| domain-search            | 24            |
| nis-server               | 27            |
| nis+-server              | 28            |
| nis-domain               | 29            |
| nis+-domain              | 30            |
| sntp-server              | 31            |
| information-refresh-time | 32            |
| FQDN                     | 39            |
| ntp-server               | 56            |
| bootfile-url             | 59            |
| bootfile-param           | 60            |

Refer to RFC 2132 for the format of a valid `option-value` parameter for the corresponding `option-name`/`option-number` options.

```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)#option set option-name Router option-value 10.0.0.1 match tags tag1,tag2,tag3
ops-as5712(config-dhcp-server)#option set option-number 3 option-value 10.0.0.1 match tags tag1,tag2,tag3
```

To remove the DHCP options configuration, use the `no option set option-name <option_name> option-value <option_value>  match tags <match_tag_names> ipv6` and `no option set option-number <option_number> option-value <option_value>  match tags <match_tag_names> ipv6` commands.

```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# no option set option-name Router option-value 10.0.0.1 match tags tag1,tag2,tag3
ops-as5712(config-dhcp-server)# no option set option-number 3 option-value 10.0.0.1 match tags tag1,tag2,tag3
```

#### Setting the DHCP match configuration
The `match set tag <set_tag_name> match-option-name <option_name> match-option-value <option_value>` and `match set tag <set_tag_name> match-option-number <option_number> match-option-value <option_value>` commands set the configuration for the server to set the tag if the client sends a DHCP option of the given number or name.
- Parameter `match-option-name` sets the option name to be matched in the client request.
- Parameter `match-option-value` sets the option number to be matched in the client request.
- Parameter `match-option-value` is optional. If this parameter is not specified, this command sets the tag if the client sends a DHCP option of the given name. If the option value is specified, then the tag would be set only if the option is sent and matches the value.
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# match set tag tag1 match-option-name Router match-option-value 10.0.0.1
ops-as5712(config-dhcp-server)# match set tag tag1 match-option-number 3 match-option-value 10.0.0.1
```
To remove the DHCP match configuration, use the `no match set tag <set_tag_name> match-option-name <option_name> match-option-value <option_value>` and `no match set tag <set_tag_name> match-option-number <option_number> match-option-value <option_value>` commands.
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# no match set tag tag1 match-option-name Router match-option-value 10.0.0.1
ops-as5712(config-dhcp-server)# no match set tag tag1 match-option-number 3 match-option-value 10.0.0.1
```
#### Setting the DHCP BOOTP configuraion
The `boot set file <file_name> match tag <match_tag_name>` command sets the BOOTP options that are returned by the DHCP server.
- Parameter `file` sets the file name.
- Optional parameter `match tag` sets the matching labels.
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# boot set file /tmp/tftp_file match tag tag1
```
To remove the DHCP BOOTP configuration use the `no boot set file <file_name> match tag <match_tag_name>` command.
```
ops-as5712# configure terminal
ops-as5712(config)# dhcp-server
ops-as5712(config-dhcp-server)# no boot set file /tmp/tftp_file match tag tag1
```

## Verifying the DHCP server configuration
### Viewing DHCP server configuration information
The `show dhcp-server` command displays information about the DHCP server configuration. The information incudes the details of dynamic, static, options, match, and BOOTP configuration.

```
ops-as5712# show dhcp-server

DHCP dynamic IP allocation configuration
----------------------------------------
Name     Start IP Address    End IP Address    Netmask     Broadcast
----------------------------------------------------------------------------
dynamic  10.0.0.1           10.255.255.254    255.0.0.0   10.255.255.255


DHCP static IP allocation configuration
---------------------------------------
IP Address  Hostname  Lease time  MAC-Address        Set tags
----------------------------------------------------------------------------
10.0.0.25   95_h2     65          36:d4:1b:12:ea:52  tag1,tag2,tag3


DHCP options configuration
--------------------------
Option Number  Option Name       Option Value          ipv6   Match tags
----------------------------------------------------------------------------
3              *                 10.0.0.1              False  tag1,tag2,tag3
*              Router            10.0.0.1              False  tag1,tag2,tag3


DHCP Match configuration
------------------------
Option Number  Option Name       Option Value          Set tag
--------------------------------------------------------------
3              *                 10.0.0.1              tag1
*              Router            10.0.0.1              tag1


DHCP BOOTP configuration
------------------------
Tag               File
----------------------
tag1              /tmp/tftp_file
```
### Viewing DHCP server leases information
The `show dhcp-server leases` command displays information about the DHCP server leases database. The database is updated by the DHCP server whenever an IP address is assigned to the client and a lease entry is expired or modified. The information includes the IP address, MAC address, lease expiry time, the client hostname, and the client ID.
```
ops-as5712# show dhcp-server leases

Expiry Time               MAC Address        IP Address  Hostname and Client-id
-------------------------------------------------------------------------------
Wed Sep 23 23:07:12 2015  df:36:12:1b:54:ea  10.0.0.5    95_h1            *
Wed Sep 23 22:05:10 2015  36:d4:1b:12:ea:52  10.0.0.25   95_h2            *
```


## Configuring a TFTP server
### Setting up a basic TFTP configuration
#### Changing to tftp-server context
The `tftp-server` command changes the configure terminal context to the tftp-server context.
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)#
```
#### Setting the TFTP server configuration
The `enable` command enables the TFTP server.
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# enable
```
To disable the TFTP server, use the `no enable` command.
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# no enable
```
#### Setting the TFTP server secure mode configuration
The `secure-mode` command enables the TFTP server secure mode.
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# secure-mode
```
To disable TFTP server secure mode, use the `no secure-mode` command.
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# no secure-mode
```
#### Setting the TFTP server root path configuration
The `path <path_name>` command sets the TFTP root path configuration. Only absolute paths (starting with /) are allowed, and relative paths are not allowed.
```
ops-as5712# configure terminal
ops-as5712(config)# tftp-server
ops-as5712(config-tftp-server)# path /tmp/
```

## Verifying the TFTP server configuration
### Viewing the TFTP server information
The `show tftp-server` command displays information about the TFTP server configuration. The information includes details of the TFTP server, secure mode, and the path configuration.
```
ops-as5712# show tftp-server

TFTP server configuration
-------------------------
TFTP server : Enabled
TFTP server secure mode : Enabled
TFTP server file path : /tmp/
```
