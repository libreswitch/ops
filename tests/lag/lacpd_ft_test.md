# LACP Daemon Feature Test Cases

## Contents

* [Transferring interface to another LAG with CLI](#transferring-interface-to-another-LAG-with-CLI)
* [LACP aggregation key packet validation](#LACP-aggregation-key-packet-validation)
* [LAG created with one LAG at the time, configured by CLI](#LAG-created-with-one-LAG-at-the-time,-configured-by-CLI)
* [LAG with cross links with same aggregation key using CLI](#LAG-with-cross-links-with-same-aggregation-key-using-CLI)
* [LAG created with different aggregation key configured with CLI](#LAG-created-with-different-aggregation-key-configured-with-CLI)
* [LACP aggregation key with hosts](#LACP-aggregation-key-with-hosts)

## Transferring interface to another LAG with CLI
### Objective
Transferring an interface to another LAG without passing the interface on the
other side of the link cause the link to get in state Out of Sync and not
Collecting/Distributing using CLI interface for configuration
### Requirements
- Modular Framework or OSTL
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup
#### Topology Diagram
```
+--------+                  +--------+
|        1------------------1        |
|        |                  |        |
|        2------------------2        |
|   s1   |                  |   s2   |
|        3------------------3        |
|        |                  |        |
|        4------------------4        |
+--------+                  +--------+
```

### Test Setup
### Description
1. Turn on interfaces 1-4 in both switches
2. Create LAG 100 in switch 1 with active state
3. Create LAG 100 in switch 2 with active state
4. Associate interfaces 1 and 2 to the LAG from both switches
5. Wait 30 seconds for switches to negotiate LAG state
6. Request information from interface 1 in both switches
7. Validations on switch 1 in interface 1 for LAG 100
8. Validations on switch 2 in interface 1 for LAG 100
9. Create LAG 200 in switch 1
10. Associate interface 1 to lag 200
11. Associate interface 3 to lag 200
12. Associate interface 4 to lag 100, to keep lag 100 with two interfaces
13. Wait switches to negotiate new LAG state
14. Get LAG information for interface 1,2,3 and 4 in switch 1
15. Get LAG information for interface 1 and 2 in Switch 2
16. Validation on switch 1
17. Validation for switch 2


### Test Result Criteria
#### Test Pass Criteria
* Validations in steps 7 and 8
  - Validate name, it must be lag100 for both switches
  - Validate local key, it must be 100 for both switches
  - Validate remote key, it must be 100 for both switches
  - Validate local state, it must be In Sync and Collecting/Distributing for
 both switches
  - Validate remote state, it must be In Sync and Collecting/Distributing
for both switches

* Validations in step 16
  - Validate lag name for interface 1 is lag200 for switch 1
  - Validate local key for interface 1 is 200 for switch 1
  - Validate remote key for interface 1 is 100 for switch 1
  - Validate lag state for interface 1 is Active, Long timeout, Aggregable
and Out of Sync for switch 1
  - Validate lag state for interface 2 is Sync and Collecting/Distributing
for switch 1
  - Validate lag state for interfaces 3 and 4 are in default for switch 1

* Validations in step 17
  - Validate lag name is lag100 for switch 2
  - Validate local key for interface 1 is 100 for switch 2
  - Validate remote key for interface 1 is 200 for switch 2
  - Validate lag state is Out of Sync and not Collecting/Distributing for
switch 2 interface 1 for switch 2
  - Validate lag state for interface 2 is In Sync and
Collecting/Distributing for switch 2
#### Test Fail Criteria
* Validations in steps 7 and 8
  - Validate name, it is not lag100 for both switches
  - Validate local key, it is not 100 for both switches
  - Validate remote key, it is not 100 for both switches
  - Validate local state, it is not In Sync and Collecting/Distributing for
both switches
  - Validate remote state, it is not In Sync and Collecting/Distributing for
both switches

* Validations in step 16
  - Validate lag name for interface 1 is not lag200 for switch 1
  - Validate local key for interface 1 is not 200 for switch 1
  - Validate remote key for interface 1 is not 100 for switch 1
  - Validate lag state for interface 1 is not Active, Long timeout,
  Aggregable and Out of Sync for switch 1
  - Validate lag state for interface 2 is not Sync and
  Collecting/Distributing for switch 1
  - Validate lag state for interfaces 3 and 4 are not in default for switch
  1

* Validations in step 17
  - Validate lag name is not lag100 for switch 2
  - Validate local key for interface 1 is not 100 for switch 2
  - Validate remote key for interface 1 is not 200 for switch 2
  - Validate lag state is not Out of Sync and is not Collecting/Distributing
  for switch 2
  interface 1 for switch 2
  - Validate lag state for interface 2 is not In Sync and is not Collecting/Distributing for switch 2

## LACP aggregation key packet validation
### Objective
Capture LACPDUs packets and validate the aggregation key is set correctly for
both switches
### Requirements
- Modular Framework or OSTL
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup
#### Topology Diagram
```
+--------+                  +--------+
|        1------------------1        |
|   s1   |                  |   s2   |
|        2------------------2        |
+--------+                  +--------+
```
### Test Setup
### Description
1. Turn on interfaces 1 and 2 in both switches
2. Create LAG 100 in switch 1
3. Create LAG 200 in switch 2
4. Associate interfaces 1 and 2 to lag in both switches
5. Get MAC address from switch 1 and 2
6. Take capture from interface 1 in switch 1
7. Get information from packet capture parse in a map with key-value
8. Validate key sent from switch 1 using interface 1 to switch 2 is 100
9. Validate key sent from switch 1 using interface 2 to switch 2 is 100
10. Validate key sent from switch 2 using interface 1 to switch 1 is 200
11. Validate key sent from switch 2 using interface 2 to switch 1 is 200

### Test Result Criteria
#### Test Pass Criteria
* LAGs are configured correctly on both switches
* Key sent from switch 1 using interface 1 to switch 2 is 100
* Key sent from switch 1 using interface 2 to switch 2 is 100
* Key sent from switch 2 using interface 1 to switch 1 is 200
* Key sent from switch 2 using interface 2 to switch 1 is 200
#### Test Fail Criteria
* LAGs are not configured correctly on both switches
* Key sent from switch 1 using interface 1 to switch 2 is not 100
* Key sent from switch 1 using interface 2 to switch 2 is not 100
* Key sent from switch 2 using interface 1 to switch 1 is not 200
* Key sent from switch 2 using interface 2 to switch 1 is not 200

## LAG created with one LAG at the time, configured by CLI
### Objective
Verify only interfaces associated with the same
aggregation key get to Collecting/Distributing state
### Requirements
- Modular Framework or OSTL
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup
#### Topology Diagram
```
+------------+
|            |
|     s1     |
|            |
+-1--2--3--4-+
  |  |  |  |
  |  |  |  |
  |  |  |  |
  |  |  |  |
+-1--2--3--4-+
|            |
|     s2     |
|            |
+------------+
```

### Test Setup
### Description
1. Turn on interfaces 1-4 in switches 1 and 2
2. Create LAG 150 in switch 1
3. Create LAG 150 in switch 2
4. Create LAG 400 in switch 2
5. Associate interfaces 1-4 to LAG 150 in switch 1
6. Associate interfaces 1 and 2 to LAG 150 in switch 2
7. Associate interfaces 3 and 3 to LAG 400 in switch 2
8. Wait for switches to negotiate LAG state
9. Get information for interface 1-4 in switch 1 using CLI command
"show lacp interface"
10. Get information for interface 1-4 in switch 2 using CLI command
"show lacp interface"
11. Validations in switch 1
12. Validations in switch 2

### Test Result Criteria
#### Test Pass Criteria
* LAGs are configured correctly on both switches
* Validations in step 11
  - Validate interface 1 has state In Sync and Collecting/Distributing
  - Validate interface 2 has state In Sync and Collecting/Distributing
  - Validate interface 3 has state Out of Sync and not
  Collecting/Distributing
  - Validate interface 4 has state Out of Sync and not
  Collecting/Distributing
* Validations in step 12
  - Validate interface 1 has state In Sync and Collecting/Distributing
  - Validate interface 2 has state In Sync and Collecting/Distributing
  - Validate interface 3 has state Out of Sync and not
  Collecting/Distributing
  - Validate interface 4 has state Out of Sync and not
  Collecting/Distributing
#### Test Fail Criteria
* LAGs are not configured correctly on both switches
* Validations in step 11
  - Validate interface 1 is not In Sync and Collecting/Distributing
  - Validate interface 2 is not In Sync and Collecting/Distributing
  - Validate interface 3 is not Out of Sync and not Collecting/Distributing
  - Validate interface 4 is not Out of Sync and not Collecting/Distributing
* Validations in step 12
  - Validate interface 1 is not In Sync and Collecting/Distributing
  - Validate interface 2 is not In Sync and Collecting/Distributing
  - Validate interface 3 is not Out of Sync and not Collecting/Distributing
  - Validate interface 4 is not Out of Sync and not Collecting/Distributing

## LAG with cross links with same aggregation key using CLI
### Objective
Verify LAGs should be formed independent of port IDs as long
as aggregation key is the same, using CLI for configuration
### Requirements
- Modular Framework or OSTL
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup

#### Topology Diagram
```
+--------------------+
|                    |
|         s1         |
|                    |
+-1--2--3----5--6--7-+
  |  |  |    |  |  |
  |  |  |    |  |  |
  |  |  |    |  |  |
  |  |  |    |  |  |
+-1--2--3----6--7--5-+
|                    |
|         s2         |
|                    |
+--------------------+
```
### Test Setup
### Description
1. Turn on interfaces 1-3 and 5-7 in switch 1 and 2
2. Create LAG 150, 250 and 350 in switch 1 and 2
3. Associate interface 1 to LAG 150 in switch 1
4. Associate interface 5 to LAG 150 in switch 1
5. Associate interface 2 to LAG 250 in switch 1
6. Associate interface 6 to LAG 250 in switch 1
7. Associate interface 3 to LAG 350 in switch 1
8. Associate interface 7 to LAG 350 in switch 1
9. Associate interface 1 to LAG 150 in switch 2
10. Associate interface 6 to LAG 150 in switch 2
11. Associate interface 2 to LAG 250 in switch 2
12. Associate interface 7 to LAG 250 in switch 2
13. Associate interface 3 to LAG 350 in switch 2
14. Associate interface 5 to LAG 350 in switch 2
15. Wait 30 seconds for LAG negotiation between switches
16. Get information for interfaces 5-7 in both switches with CLI command
"show lacp interfaces"
17. Validations on switch 1
18. Validations on switch 2

### Test Result Criteria
#### Test Pass Criteria
* LAGs are configured correctly on both switches
* Validations in step 17
  - Validate lag name for interface 5 is 150
  - Validate lag name for interface 6 is 250
  - Validate lag name for interface 7 is 350
  - Validate lag state for interface 5 is In Sync and
  Collecting/Distributing
  - Validate lag state for interface 6 is In Sync and
  Collecting/Distributing
  - Validate lag state for interface 7 is In Sync and
  Collecting/Distributing
* Validations in step 18
  - Validate lag name for interface 5 is 350
  - Validate lag name for interface 6 is 150
  - Validate lag name for interface 7 is 250
  - Validate lag state for interface 5 is In Sync and
  Collecting/Distributing
  - Validate lag state for interface 6 is In Sync and
  Collecting/Distributing
  - Validate lag state for interface 7 is In Sync and
  Collecting/Distributing
#### Test Fail Criteria
* LAGs are not configured correctly on both switches
* Validations in step 17
  - Validate lag name for interface 5 is not 150
  - Validate lag name for interface 6 is not 250
  - Validate lag name for interface 7 is not 350
  - Validate lag state for interface 5 is not In Sync and
  Collecting/Distributing
  - Validate lag state for interface 6 is not In Sync and
  Collecting/Distributing
  - Validate lag state for interface 7 is not In Sync and
  Collecting/Distributing
* Validations in step 18
  - Validate lag name for interface 5 is not 350
  - Validate lag name for interface 6 is not 150
  - Validate lag name for interface 7 is not 250
  - Validate lag state for interface 5 is not In Sync and
  Collecting/Distributing
  - Validate lag state for interface 6 is not In Sync and
  Collecting/Distributing
  - Validate lag state for interface 7 is not In Sync and
  Collecting/Distributing

## LAG created with different aggregation key configured wit CLI
### Objective
Verify LAGs with different names from switches can get connected as long as
all interfaces connected have same aggregation key, using CLI interface for
configuration
### Requirements
- Modular Framework or OSTL
- Script is in tests/test_ft_lacp_aggregation_key.py

### Setup

#### Topology Diagram
```
+--------+                  +--------+
|        1------------------1        |
|   s1   |                  |   s2   |
|        2------------------2        |
+--------+                  +--------+
```
### Test Setup
### Description
1. Turn interfaces 1 and 2 in both switches
2. Create LAG 10 in switch 1
3. Create LAG 20 in switch 2
4. Associate interface 1 and 2 to lag 10 in switch 1
5. Associate interface 1 and 2 to lag 20 in switch 2
6. Wait 30 seconds for LAG negotiations between switches
7. Get information from interface 1 and 2 from both switches using CLI command
"show lacp interface"
8. Validations in switch 1
9. Validations in switch 2

### Test Result Criteria
#### Test Pass Criteria
* LAGs are configured correctly on both switches
* Validations in step 8
  - Validate interface 1 and 2 are In Sync and Collecting/Distributing in
  local state
  - Validate interface 1 and 2 are In Sync and Collecting/Distributing in
  remote state
* Validations in step 9
  - Validate interface 1 and 2 are In Sync and Collecting/Distributing in
  local state
  - Validate interface 1 and 2 are In Sync and Collecting/Distributing in
  remote state
#### Test Fail Criteria
* LAGs are not configured correctly on both switches
* Validations in step 8
  - Validate interface 1 and 2 are not In Sync and Collecting/Distributing
  in local state
  - Validate interface 1 and 2 are not In Sync and Collecting/Distributing
  in remote state
* Validations in step 9
  - Validate interface 1 and 2 are not In Sync and Collecting/Distributing
  in local state
  - Validate interface 1 and 2 are not In Sync and Collecting/Distributing
  in remote state

## LACP aggregation key with hosts
### Objective
Verify test cases for aggregation key functionality including hosts
connected to the switches
### Requirements
- Modular Framework or OSTL
- Script is in tests/test_ft_lacp_agg_key_hosts.py
### Setup
#### Topology Diagram
```
+-------+                                +-------+
|       |                                |       |
|  hs1  |                                |  hs2  |
|       |                                |       |
+--1----+                                +----1--+
   |                                          |
   |                                          |
   |                                          |
   |                                          |
   |                                          |
+--3---------+                      +---------2--+
|            |                      |            |
|            |                      |            |
|    sw1     |                      |     sw2    |
|            |                      |            |
+-1-2--------+                      +----------1-+
  | |                                          |
  | |                                          |
  | |                                          |
  | |                                          |
  | |LAG                                       |LAG
  | |                                          |
  | |             +------------+               |
  | |             |            |               |
  | +-------------2            |               |
  +---------------1    sw3     3---------------+
                  |            |
                  +------4-----+
                         |
                         |
                         |
                         |
                     +---1---+
                     |       |
                     |  hs3  |
                     |       |
                     +-------+
```
### Test Setup
### Description
1. Turn on interfaces 1-3 in switch 1
2. Turn on interfaces 1 and 2 in switch 2
3. Turn on interfaces 1-4 in switch 3
4. Create LAG 10 in Switch 1
5. Create LAG 20 in Switch 2
6. Create LAG 310 and 320 in Switch 3
7. Associate interfaces 1 and 2 to LAG 10 in Switch 1
8. Associate interface 1 to LAG 20 in Switch 2
9. Associate interface 1 and 2 to LAG 210 in Switch 3
10. Associate interface 3 to LAG 320 in Switch 3
11. Configure IP 10.0.10.1 for host 1
12. Configure IP 10.0.20.1 for host 2
13. Configure IP 10.0.10.2 for host 3, to be able to ping with host 1
14. Create Vlan 100 in switch 1
15. Create Vlan 200 in switch 2
16. Create Vlans 100 and 200 in switch 3
17. Associate Vlan 100 to LAG 10 in switch 1
18. Associate Vlan 200 to LAG 20 in switch 2
19. Associate Vlan 100 to LAG 310 in switch 3
20. Associate Vlan 200 to LAG 320 in switch 3
21. Associate interface 3 in switch 1 to vlan 100
22. Associate interface 4 in switch 3 to vlan 100
23. Ping between Host 1 and Host 3
24. Associate interface 2 in switch 2 to vlan 200
25. Associate interface 4 in switch 3 to vlan 200
26. Remove IP 10.0.10.2 from host 3
27. Configure IP 10.0.20.2 to host 3
28. Ping between Host 2 and Host 3
29. Change interface 2 from Switch 3 to LAG 320
30. Get state from interfaces 1 and 2 in switch 1 with CLI command
"show lacp interface"
31. Get state from interfaces 2 in switch 2 with CLI command
"show lacp interface"
32. Change interface 4 in switch 3 to Vlan 100
33. Get state from interfaces 1, 2 and 3 in switch 3 with CLI command
"show lacp interface"
34. Ping between Host 2 and Host 3
35. Remove IP 10.0.20.2 to host 3
36. Configure IP 10.0.10.1 to host 3
37. Ping between Host 1 and Host 3

### Test Result Criteria
#### Test Pass Criteria
* LAGs are configured correctly on both switches
* Validate Host 1 and Host 3 can ping each other after step 23
* Validate Host 2 and Host 3 can ping each other after step 28
* Validate ping in step 28
* Validations in after step 32
  - Validate LACP state for interface 2 in switch 3 is Out of Sync and not
  in Collecting/Distributing
  - Validate LACP state for interface 2 in switch 1 is Out of Sync and not
  in Collecting/Distributing
  - Validate LACP state for interface 1 in switch 1 is Sync and
  Collecting/Distributing
  - Validate LACP state for interface 1 in switch 2 is Sync and
  Collecting/Distributing
  - Validate LACP state for interface 1 in switch 3 is Sync and
  Collecting/Distributing
  - Validate LACP state for interface 3 in switch 3 is Sync and
  Collecting/Distributing
  - Validate Host 2 and Host 3 can ping each other
* Validate Host 2 and Host 3 can ping each other after step 34
* Validate Host 1 and Host 3 can ping each other after step 37

#### Test Fail Criteria
* LAGs are not configured correctly on both switches
* Validate Host 1 and Host 3 can't ping each other after step 23
* Validate Host 2 and Host 3 can't ping each other after step 28
* Validations in after step 32
  - Validate LACP state for interface 2 in switch 3 is not Out of Sync and
  is in Collecting/Distributing
  - Validate LACP state for interface 2 in switch 1 is not Out of Sync and
  is in Collecting/Distributing
  - Validate LACP state for interface 1 in switch 1 is not Sync and
  Collecting/Distributing
  - Validate LACP state for interface 1 in switch 2 is not Sync and
  Collecting/Distributing
  - Validate LACP state for interface 1 in switch 3 is not Sync and
  Collecting/Distributing
  - Validate LACP state for interface 3 in switch 3 is not Sync and
  Collecting/Distributing
  - Validate Host 2 and Host 3 can't ping each other
* Validate Host 2 and Host 3 can't ping each other after step 34
* Validate Host 1 and Host 3 can't ping each other after step 37
