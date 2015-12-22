# Source Interface Selection

## Contents

- [Overview](#overview)
- [Configuring the source-interface](#configuring-the-source-interface)
- [Verifying the configuration](#verifying-the-configuration)
    - [Viewing source-interface information](#viewing-source-interface-information)
    - [Viewing the snapshot of active configurations](#viewing-the-snapshot-of-active-configurations)
- [Related features](#related-features)

## Overview

The source interface selection is used to set the IP address of an interface, or IP address-defined interface as the source interface for the TFTP protocol or all the specified protocols.

### Syntax:
`ip source-interface <protocol-ID | all>  <interface <id>| address <ip-address>>`
`[no] ip source-interface <protocol-ID | all>`
`show  ip source-interface [tftp]`

### Explanation of Parameters:

-protocol-ID--Specifies the  different software applications like telnet, tftp, radius, sflow etc. we can specify different source ips for different apps by using protocol-ID

-all--Specifies same source IP for all applications.
-address--Sets the IP address of an interface as the source IP.
-interface--Sets an interface as the source interface.
Note: As of now the CLI infra is ready, end to end functionality of source interface selection is not implemented.

## Examples:
### Configuring the source-interface

-Configuring a source-interface IP address to TFTP protocol

ops-as5712(config)# ip source-interface tftp address 1.1.1.1
Note: As of now the CLI infra is ready, end to end functionality of source interface selection to the TFTP protocol is not implemented.

-Configuring a source-interface IP address to all the specified protocols

ops-as5712(config)# ip source-interface all address 1.1.1.1
Note: As of now the CLI infra is ready, end to end functionality of source interface selection for all the specicied protocols is not implemented.

-Configuring a source-interface to TFTP protocol

ops-as5712(config)# ip source-interface tftp interface 1
Note: As of now the CLI infra is ready, end to end functionality of source interface selection to the TFTP protocol is not implemented.

-Configuring a source-interface to all the specified protocols

ops-as5712(config)# ip source-interface all interface 1
Note: As of now the CLI infra is ready, end to end functionality of source interface selection for all the specicied protocols is not implemented.

-Unconfigure the source-interface from the TFTP protocol.

ops-as5712(config)# no ip source-interface tftp
Note: As of now the CLI infra is ready, end to end functionality of source interface selection to the TFTP protocol is not implemented.

-Unconfigure the source-interface from all the specified protocols.

ops-as5712(config)# no ip source-interface all
Note: As of now the CLI infra is ready, end to end functionality of source interface selection for all the specicied protocols is not implemented.

## Verifying the configuration
### Viewing source-interface information

-Verify that the source-interface is on the TFTP protocol.
```
ops-as5712# show ip source-interface tftp

Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp            1.1.1.1
```

-Verify that source-interface to all the specified protocols
```
ops-as5712# show ip source-interface

Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp            1.1.1.1
```

-Verify that the source-interface from the TFTP protocol.
```
ops-as5712# show ip source-interface tftp

Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp
```

-Verify that unconfiguring the source-interface from all the specified protocols.
```
ops-as5712# show ip source-interface

Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp
```

### Viewing the snapshot of active configurations.
```
ops-as5712# show ip source-interface

Source-interface Configuration Information

Protocol        Source Interface
--------        ----------------
tftp            1.1.1.1

ops-as5712# show running-config interface
Current configuration:
!
!
!
interface 1
    no shutdown
    ip address 1.1.1.1/24
source interface
    1.1.1.1
```

## Related features
No related features.