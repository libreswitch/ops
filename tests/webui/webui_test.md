# Web UI Test Cases

## Contents
- [Description](#description)
- [Interface configuration](#interface-configuration)
- [Overview page](#overview-page)
- [LLDP verify](#lldp-verify)
- [LAG configuration](#lag-configuration)
- [ECMP page](#ecmp-page)

## Description
The purpose of the Web UI feature tests is to ensure that the REST calls the Web UI makes do not break due to changes in schema or data.

## Interface configuration

### Objective
Verify the following:

- A basic port can be created.
- An interface and a port can be patched to have admin state up.
- An interface can be patched to add other states such as, duplex, auto-negotiation, and flow-control.

### Requirements

- OpenSwitch
- Ubuntu workstation
- Interface 1

### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

### Description
This test case validates that a basic port can be configured, then that port along with an interface can be patched to set the admin state to 'up'.  The other interface configuration parameters are also patched: duplex, auto-negotiation, and flow-control.

### Test 1

Create port 1 via POST then use PATCH to modify interface 1 and port 1.
Port patch:
```
   [{"op": "add","path": "/admin","value": "up"}]
```

Interface patch:

```
   [{"op": "add","path": "/user_config","value": {"admin": "up"}}]
```

### Test 2

Create port 2 and patch using the following:

```
   [{"op": "add","path": "/user_config","value": {"autoneg": "off","duplex": "half","pause": "rxtx"}}]
```

### Test result criteria

#### Test pass criteria

Port creation should return a `201 CREATED`.  The patch commands should return a `204 NO CONTENT`.

### Test fail criteria

Any result other than the ones listed above.

## Overview page

### Objective

Verify the various database columns used by the overview page exist.

### Requirements

- OpenSwitch
- Ubuntu workstation
- Interface 1

### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

### Description
This test validates various database columns from the **system** table and the **system/subsystems/base** table.  Part of this test ensures that the names have not changed.

### Test 1
From the **system/subsystems/base** table validate the following columns exist:


```
'Product Name', 'part_number', 'onie_version','base_mac_address', 'serial_number', 'vendor','max_interface_speed', 'max_transmission_unit','interface_count'
```

### Test 2
From the **system** table validate the following columns exist:

```
'hostname', 'switch_version'
```

### Test result criteria

#### Test pass criteria

If all columns are present, the test passes.

### Test fail criteria

If any column is missing the test fails.

## LLDP verify

### Objective
Given two connected switches with LLDP enabled, verify the following:

- A basic port can be created.
- An interface and a port can be patched to have admin state up.
- An interface can be patched to add other states, such as duplex, auto-negotiation, and flow-control.

### Requirements

- OpenSwitches (2) - connected on interface 1
- Ubuntu workstation - send REST request, rcv response

### Setup
Two switches connected together on interface 1. Both switches configured with LLDP enabled, and interface 1 is up and connected.
One host connected only to switch 1 sends a REST request, and then LLDP information in the response is examined for the expected return information.

#### Topology diagram
```ditaa
+----------------+         +----------------+          +---------------+
|                |         |                |          |               |
|                |         |                |          |               |
|    Local Host  +---------+    Switch 1    +----------+    Switch 2   +
|                |         |                |          |               |
|                |         |                |          |               |
+----------------+         +----------------+          +---------------+
```

### Description
These test cases validate that the LLDP information in the REST response is well formed.

### Test 1
Check to see if the LLDP Neighbor Info tag is present in the well-formed response expected by the webui:

   ```
   [{"status":..."lldp_neighbor_info"}]
   ```

### Test 2
Check to see if the mgmt_ip_list tag is present in the well-formed response expected by the webui:
   ```
   [{"status":..."lldp_neighbor_info":{...{"mgmt_ip_list"}}}]
   ```

### Test 3
Check to see if the mgmt_ip_list value matches the expected value (for example, the IP of switch 2):
   ```
   [{"status":..."lldp_neighbor_info":{...{"mgmt_ip_list":"10.10.10.3"}}}]
   ```

### Test 4
Check to see if the LLDP statistics tag is present in the well-formed response expected by the webui:
   ```
   [{"statistics":{..."lldp_statistics"}}]
   ```
### Test 5
Check to see if the LLDP statistics tag for XMIT is present in the well-formed response expected by the webui:
   ```
   [{"statistics":{..."lldp_statistics":...{"lldp_xmit"}}}]
   ```
### Test 6
Check to see if the LLDP statistics tag for XMIT > 0 is present in the well-formed response expected by the webui:
   ```
   [{"statistics":{..."lldp_statistics":...{"lldp_xmit":"11"}}}]
   ```
### Test 7
Check to see if the LLDP statistics tag for RCV is present in the well-formed response expected by the webui:
   ```
   [{"statistics":{..."lldp_statistics":...{"lldp_rcv"}}}]
   ```
### Test 8
Check to see if the LLDP statistics tag for RCV > 0 is present in the well-formed response expected by the webui:
   ```
   [{"statistics":{..."lldp_statistics":...{"lldp_rcv":"11"}}}]
```
### Test result criteria

#### Test pass criteria

All tests should pass in order for the response to be considered well-formed for the LLDP configuration.

### Test fail criteria

Any of the tests to check for a well-formed LLDP response fail.

## LAG configuration

### Objective
Verify the following:

- A basic L2 dynamic LAG port can be created.
- An interface can be patched to have admin state up, and lacp-aggregation-key set to the corresponding lagId.
- The LAG port can be created with a set of member interfaces and atributes: lacp mode, vlan mode, and the admin state.

### Requirements

- OpenSwitch
- Ubuntu workstation h1 and h2
- Interface 1 and 2
- LAG 12

### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+           +----------------+         +----------------+
|                |         |                |           |                |         |                |
|                |         |                |           |                |         |                |
|   Local Host 1 +---------+    Switch 1    |           |   Switch 2     +---------+   Local Host 2 |
|                |         |                |           |                |         |                |
|                |         |                |           |                |         |                |
+----------------+         +----------------+           +----------------+         +----------------+
```

### Description
This test case creates and validates that a basic LAG port can be configured and returns a status of 'OK'. Then that port, along with the interface, can be patched to set the admin state to 'up'.  The test case also verifies that the other LAG port configuration parameters are also created at the same time: lacp mode, vlan mode, and the admin state.

### Test 1

Patch interfaces 1 and 2.

Interface patch:

   ```
   [{"op": "add","path": "/user_config","value": {"admin": "up"}}]
   [{"op": "add","path": "/other_config","value": {"lacp-aggregation": "lag12"}}]
   ```

Post a new LAG port 12 that has two interfaces: 1 and 2.`

Create LAG port 12 on both switches using the following:

   ```
   {"configuration":
      { "interfaces": ["/rest/v1/system/interfaces/1", "/rest/v1/system/interfaces/2"],
        "name": "lag12",
        "lacp": "active",
        "vlan_mode": "trunk",
      },
      "referenced_by": [{"uri":"/rest/v1/system/bridges/bridge_normal" }]
    }

   ```
### Test result criteria

#### Test pass criteria

Port creation should return a `201 CREATED` result.  The patch commands should return a `204 NO CONTENT` result.

### Test fail criteria

Any result other than the ones listed above.

### Test 2

Delete the LAG 12 port on both switches.

Interface patch:

   ```
   [{"op": "add","path": "/user_config","value": {"admin": "up"}}]
   ```

Send a DELETE request to delete the LAG 12 via the path /rest/v1/system/ports/lag12.

Patch interface 1 and 2 to remove `lacp-aggregation-key` on both switches:

   ```
   [{"op": "remove","path": "/other_config/lacp-aggregation-key"}]
   ```
### Test Result Criteria

#### Test pass criteria

Port deletion should return a `404 NOt Found` message. The port GET command should return a `404 Not Found` message.

### Test fail criteria

Any result other than the ones listed above.

## ECMP page

### Objective

Verify the ECMP status and its load balancing options.

### Requirements

- OpenSwitch
- Ubuntu workstation


### Setup

#### Topology diagram
```ditaa
+----------------+         +----------------+
|                |         |                |
|                |         |                |
|    Local Host  +---------+    Switch 1    |
|                |         |                |
|                |         |                |
+----------------+         +----------------+
```

### Description
This test validates the ECMP status, out of box behavior, and dynamic configuration. Part of this test ensures the names havenot changed.

### Test1
Check the ECMP initial configuration out of box.

### Test result criteria

#### Test pass criteria
The system configuration does not have ecmp data.

### Test fail criteria
The system configuration contains ecmp data.

### Test 2
Enable ecmp.

ECMP enable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"enabled": "true"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration has ecmp property "enabled" : "true".

### Test fail criteria
The system configuration does not have ecmp property "enabled" : "true".

### Test 3
Enable ecmp load balancing by destination IP.

ECMP load balancing by destination IP enable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"hash_dstip_enabled": "true"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "hash_dstip_enabled" : "true".

### Test fail criteria
The system configuration does not have ecmp property "hash_dstip_enabled" : "true".

### Test 4
Enable ecmp load balancing by source IP.

ECMP load balancing by source IP enable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"hash_srcip_enabled": "true"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "hash_srcip_enabled" : "true".

### Test fail criteria
The system configuration does not have ecmp property "hash_srcip_enabled" : "true".

### Test 5
Enable ecmp load balancing by destination port.

ECMP load balancing by destination port enable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"hash_dstport_enabled": "true"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "hash_dstport_enabled" : "true".

### Test fail criteria
The system configuration does not have ecmp property "hash_dstport_enabled" : "true".

### Test 6
Enable ecmp load balancing by source port.

ECMP load balancing by source port enable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"hash_srcport_enabled": "true"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "hash_srcport_enabled" : "true".

### Test fail criteria
The system configuration does not have ecmp property "hash_srcport_enabled" : "true".

### Test 7
Enable ecmp resilient hash.

ECMP resilient hash enable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"resilient_hash_enabled": "true"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "resilient_hash_enabled" : "true".

### Test fail criteria
The system configuration does not have ecmp property "resilient_hash_enabled" : "true".

### Test 8
Disable ecmp load balancing by destination IP.

ECMP load balancing by destination ip disable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"hash_dstip_enabled": "false"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "hash_dstip_enabled" : "false".

### Test fail criteria
The system configuration does not have ecmp property "hash_dstip_enabled" : "false".

### Test 9
Disable ecmp load balancing by source IP.

ECMP load balancing by source ip disable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"hash_srcip_enabled": "false"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "hash_srcip_enabled" : "false".

### Test fail criteria
The system configuration does not have ecmp property "hash_srcip_enabled" : "false".

### Test 10
Disable ecmp load balancing by destination port.

ECMP load balancing by destination port disable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"hash_dstport_enabled": "false"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "hash_dstport_enabled" : "false".

### Test fail criteria
The system configuration does not have ecmp property "hash_dstport_enabled" : "false".

### Test 11
Disable ecmp load balancing by source port

ECMP load balancing by source port disable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"hash_srcport_enabled": "false"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "hash_srcport_enabled" : "false".

### Test fail criteria
The system configuration doesnot have ecmp property "hash_srcport_enabled" : "false".

### Test 12
Disable ecmp resilient hash.

ECMP resilient hash disable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"resilient_hash_enabled": "false"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "resilient_hash_enabled" : "false".

### Test fail criteria
The system configuration does not have ecmp property "resilient_hash_enabled" : "false".

### Test 13
Disable ecmp.

ECMP disable patch:
```
[{"op": "add", "path": "/ecmp_config", "value": {"enabled": "false"}}]
```

### Test result criteria

#### Test pass criteria
The system configuration must have ecmp property "enabled" : "false".

### Test fail criteria
The system configuration does not have ecmp property "enabled" : "false".
