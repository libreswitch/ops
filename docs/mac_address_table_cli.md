# Display Support for MAC Address Table

## Contents

- [Display commands](#display-commands)

    - [show mac-address-table](#show-mac-address-table)

    - [show mac-address-table [ dynamic ]](#show-mac-address-table-dynamic)

    - [show mac-address-table address < mac-address >](#show-mac-address-table-address-mac-address)



## Display commands

### show mac-address-table

#### Syntax

```

show mac-address-table [dynamic] [port <ports> | vlan <VLAN_ID>] [address  <A:B:C:D:E:F>]

```

#### Description

This command displays all of the learnt MAC addresses in the device with following information:


-   MAC address

-   VLAN Information

-   Learnt from ASIC

-   Port name



#### Authority



Admin user.



#### Parameters



N/A



#### Examples



```

switch# show mac-address-table

MAC age-time            : 300 seconds

Number of MAC addresses : 3



MAC Address          VLAN     Type      Port

--------------------------------------------------

00:01:01:01:01:02   2        dynamic    2

00:01:01:01:01:03   1        dynamic    3

switch#



```

### show mac-address-table [ dynamic ]



#### Syntax



```

 show mac-address-table [ dynamic ] [ port < 2 | 1-2 > ]

```



#### Description



This command displays details of all MAC addresses learnt on specified ports.



#### Authority



Admin user.



#### Parameters



| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| ** 1 or 1-2 or 1,lag1 ** | Optional | 1-2,3 | Show all learnt MAC addresses on specified ports.|



#### Examples



```

switch# show mac-address-table dynamic port 1

MAC age-time            : 300 seconds

Number of MAC addresses : 1



MAC Address          VLAN     Type      Port

--------------------------------------------------

00:01:01:01:01:03    1        dynamic    1



switch# show mac-address-table dynamic port 1-2

MAC age-time            : 300 seconds

Number of MAC addresses : 2



MAC Address          VLAN     Type      Port

--------------------------------------------------

00:01:01:01:01:02    2        dynamic    2

00:01:01:01:01:03    1        dynamic    1

```
#### Syntax

```

 show mac-address-table [ dynamic ] [ vlan < 2 | 1-2 > ]

```



#### Description



This command displays details of all MAC addresses learnt on specified VLANS.



#### Authority



Admin user.



#### Parameters



| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| ** 1 or 1-2 ** | Optional | 1-2,3 | Show all MAC addresses learnt on specified VLANs.|



#### Examples

```

switch# show mac-address-table dynamic vlan 1

MAC age-time            : 300 seconds

Number of MAC addresses : 1



MAC Address        VLAN     Type      Port

--------------------------------------------------

00:01:01:01:01:03   1       dynamic     1



switch# show mac-address-table dynamic vlan 2-3

MAC age-time            : 300 seconds

Number of MAC addresses : 2



MAC Address          VLAN     Type      Port

--------------------------------------------------

00:01:01:01:01:02     2       dynamic    2

00:01:01:01:0c:02     3       dynamic    2

```


### show mac-address-table address < mac-address >



#### Syntax



```

 show mac-address-table address <A:B:C:D:E:F>

```



#### Description

This command displays details of specified learnt MAC address.

#### Authority

Admin user.

#### Parameters



| Parameter | Status   | Syntax | Description |

|-----------|----------|----------------------|

| **< A:B:C:D:E:F >** | Required | < A:B:C:D:E:F > | Show details of the learnt MAC address.|



#### Examples



```

switch# show mac-address-table address 00:01:01:01:01:03

MAC age-time            : 300 seconds

Number of MAC addresses : 1



MAC Address          VLAN     Type      Port

--------------------------------------------------

00:01:01:01:01:03   1        dynamic     1

```
