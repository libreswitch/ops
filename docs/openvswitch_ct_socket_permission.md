Openvswitch Socket Permissions
===========================


## Contents
- [openvswitch socket permissions](#openvswitch-socket-permissions)

##  L2 interface configuration
### Objective
Test case checks that the permissions of ovsdb socket files are valid.
### Requirements
- Virtual Mininet Test Setup
- **CT File**:  ops-openvswitch/ops/tests/test_openvswitch_ct_socket_permission.py (socket permissions)

### Setup
#### Topology Diagram
```ditaa
                           +--------+
                           |        |
                           |   S1   |
                           |        |
                           +--------+
```

### Description
1. Validate that the socket files in /var/run/openvswitch have file permission of type ‘srwxrw’ and has ‘ovsdb_users’ as file owner.
