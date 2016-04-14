# COPP

## Contents
- [Display commands](#display-commands)

## Display commands

### show copp statistics

#### Syntax


`show copp statistics [<protocol-name>]`

#### Description
Displays control plane policing (CoPP) statistics for all protocols, or a specific protocol.

#### Authority
Operator.

#### Parameters

| Parameter | Status   | Syntax         | Description                                                   |
|:-----------|:----------|:----------------:|:-----------------------------------------------------------------|
| **protocol-name** | Optional| String  | Name of a protocol for wich to retrieve CoPP statistics. To see a list of all supported protocol names, use the command: **show copp statistics ?** |

##### Example
```
switch# sh copp statistics acl-logging
        Control Plane Packet: ACL LOGGING packets

          rate (pps):                     5
          burst size (pkts):              5
          local_priority:                 0

          packets_passed:                 5        bytes_passed:               320
          packets_dropped:                5        bytes_dropped:              320


switch# sh copp statistics
        Control Plane Packets Total Statistics

          total_packets_passed:        5500        total_bytes_passed:      352000
          total_packets_dropped:       5500        total_bytes_dropped:     352000


        Control Plane Packet: BGP packets

          rate (pps):                  5000
          burst size (pkts):           5000
          local_priority:                 9

          packets_passed:              5000        bytes_passed:            320000
          packets_dropped:             5000        bytes_dropped:           320000


        Control Plane Packet: LLDP packets

          rate (pps):                   500
          burst size (pkts):            500
          local_priority:                 8

          packets_passed:               500        bytes_passed:             32000
          packets_dropped:              500        bytes_dropped:            32000

```
