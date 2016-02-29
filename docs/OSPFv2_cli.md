OSPFv2 commands
======
# Contents
- [OSPFv2 configuration command](#ospfv2-configuration-commands)
	- [Config context commands](#config-context-commands)
		- [Create OSPF instance](#create-ospf-instance)
		- [Remove OSPF instance](#remove-ospf-instance)
	- [Router OSPF context commands](#router-ospf-context-commands)
		- [Set router ID](#set-router-id)
		- [Set router ID to default](#set-router-id-to-default)
		- [Set OSPF network for the area](#set-ospf-network-for-the-area)
		- [Unset OSPF network for the area](#unset-ospf-network-for-the-area)
		- [Enable OSPF area authentication](#enable-ospf-area-authentication)
		- [Disable OSPF area authentication](#disable-ospf-area-authentication)
		- [Set cost for default LSA summary](#set-cost-for-default-lsa-summary)
		- [Set cost for default LSA summary to default](#set-cost-for-default-lsa-summary-to-default)
		- [Set the area as NSSA](#set-the-area-as-nssa)
		- [Unset the area as NSSA](#unset-the-area-as-nssa)
		- [Configure the area as stub](#configure-the-area-as-stub)
		- [Unset the area as stub](#unset-the-area-as-stub)
		- [Summarize intra-area paths](#summarize-intra-area-paths)
		- [Filter networks between OSPF areas](#filter-networks-between-ospf-areas)
		- [Disable filtering of networks between OSPF areas](#disable-filtering-of-networks-between-ospf-areas)
		- [Configure OSPF virtual links](#configure-ospf-virtual-links)
		- [Delete OSPF virtual links](#delete-ospf-virtual-links)
		- [Set OSPF virtual links authentication keys](#set-ospf-virtual-links-authentication-keys)
		- [Delete OSPF virtual links authentication keys](#delete-ospf-virtual-links-authentication-keys)
		- [Set OSPF virtual links delay and interval](#set-ospf-virtual-link-delays-and-intervals)
		- [Set OSPF virtual links delay or interval to default](#set-ospf-virtual-links-delay-or-interval-to-default)
		- [Control distribution of default route information](#control-distribution-of-default-route-information)
		- [Disable distribution of default route information](#disable-distribution-of-default-route-information)
		- [Set default metric for redistributed routes](#set-default-metric-for-redistributed-routes)
		- [Set default metric of redistributed routes to default](#set-default-metric-of-redistributed-routes-to-default)
		- [Define OSPF administrative distance](#define-ospf-administrative-distance)
		- [Set OSPF administrative distance to default](#set-ospf-administrative-distance-to-default)
		- [Set OSPF administrative distance for a particular route type](#set-ospf-administrative-distance-for-a-particular-route-type)
		- [Set OSPF administrative distance for a particular route type to default](#set-ospf-administrative-distance-for-a-particular-route-type-to-default)
		- [Stub router advertisement](#stub-router-advertisement)
		- [Advertise normal cost metric](#advertise-normal-cost-metric)
		- [Log changes in the adjacency state](#log-changes-in-the-adjacency-state)
		- [Disable logging changes in the adjacency state](#disable-logging-changes-in-the-adjacency-state)
		- [Suppress routing updates](#suppress-routing-updates)
		- [Enable router to send routing updates](#enable-router-to-send-routing-updates)
		- [Enable auto cost calculation](#enable-auto-cost-calculation)
		- [Disable auto cost calculation](#disable-auto-cost-calculation)
		- [Enable OSPF opaque LSA](#enable-ospf-opaque-lsa)
		- [Disable OSPF opaque LSA](#disable-ospf-opaque-lsa)
		- [Enable OSPF RFC1583 compatibility](#enable-ospf-rfc1583-compatibility)
		- [Disable OSPF RFC1583 compatibility](#disable-ospf-rfc1583-compatibility)
		- [Redistribute routes into OSPF](#redistribute-routes-into-ospf)
		- [Disable redistributing routes into OSPF](#disable-redistributing-routes-into-ospf)
		- [Set OSPF timers](#set-ospf-timers)
		- [Set OSPF timers to default](#set-ospf-timers-to-default)
		- [Set OSPF throttling parameters](#set-ospf-throttling-parameters)
		- [Set OSPF throttling parameters to default](#set-ospf-throttling-parameters-to-default)
		- [Configure NBMA neighbor](#configure-nbma-neighbor)
		- [Remove NBMA neighbor](#remove-nbma-neighbor)
		- [Set the interface as OSPF passive interface](#set-the-interface-as-ospf-passive-interface)
		- [Set the interface as OSPF active interface](#set-the-interface-as-ospf-active-interface)
	- [Interface context commands](#interface-context-commands)
		- [Enable authentication on the interface](#enable-authentication-on-the-interface)
		- [Disable authentication on the interface](#disable-authentication-on-the-interface)
		- [Set time interval between hello packets for the interface](#set-time-interval-between-hello-packets-for-the-interface)
		- [Set time interval between hello packets for the interface to default](#set-time-interval-between-hello-packets-for-the-interface-to-default)
		- [Set neighbor dead interval for the interface](#set-neighbor-dead-interval-for-the-interface)
		- [Set neighbor dead interval for the interface to default](#set-neighbor-dead-interval-for-the-interface-to-default)
		- [Disable MTU mismatch detection](#disable-mtu-mismatch-detection)
		- [Enable MTU mismatch detection](#enable-mtu-mismatch-detection)
		- [Set the interface cost](#set-the-interface-cost)
		- [Set the interface cost to default](#set-the-interface-cost-to-default)
		- [Set OSPF network type for the interface](#set-ospf-network-type-for-the-interface)
		- [Set OSPF network type for the interface to default](#set-ospf-network-type-for-the-interface-to-default)
		- [Set the OSPF priority for the interface](#set-the-ospf-priority-for-the-interface)
		- [Set the OSPF priority for the interface to default](#set-the-ospf-priority-for-the-interface-to-default)
		- [Set the retransmit interval for the interface](#set-the-retransmit-interval-for-the-interface)
		- [Set the retransmit interval for the interface to default](#set-the-retransmit-interval-for-the-interface-to-default)
		- [Set the transmit delay for the interface](#set-the-transmit-delay-for-the-interface)
		- [Set the transmit delay for the interface to default](#set-the-transmit-delay-for-the-interface-to-default)
	- [OSPFv2 show commands](#ospfv2-show-commands)
		- [Show general OSPF configurations](#show-general-ospf-configurations)
		- [Show OSPF database information](#show-ospf-database-information)
		- [Show OSPF interface information](#show-ospf-interface-information)
		- [Show OSPF neighbor information](#show-ospf-neighbor-information)
		- [Show OSPF routing table](#show-ospf-routing-table)
		- [Show OSPF active non default configurations](#show-ospf-active-non-default-configurations)

# OSPFv2 configuration commands
In vtysh every command belongs to a particular context.
## Config context commands
### Create OSPF instance
#### Syntax ####
`router ospf`
#### Description ####
This command creates the OSPF instance (if not created already) and enters the 'router ospf' context.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# router ospf
```
### Remove OSPF instance
#### Syntax ####
`no router ospf`
#### Description ####
This command removes the OSPF instance.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# no router ospf
```
## Router OSPF context commands
### Set router ID
#### Syntax ####
`router-id <router_address>`
#### Description ####
This command sets an id for the router in an IPv4 address format.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Syntax | Description |
|:---------|:----------:|:------------|
| *router_address* | A.B.C.D | Router id in IPv4 address format. |
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# router-id 1.1.1.1
```
### Set router ID to default
#### Syntax ####
`no router-id`
#### Description ####
This command unconfigures the router-id for the instance. The Router-id is changed to the global router-id, if configured. Otherwise, it is changed to the dynamically selected router-id.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no router-id
```
### Set OSPF network for the area
#### Syntax ####
`network <network_prefix> area (<area_ip>|<area_id>)`
#### Description ####
This command will run the OSPF protocol on the configured network address. The interfaces which have an IP address configured in this network or in a subset of this network, will participate in the OSPF protocol.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Syntax    | Description  |
|:-----------------|:----------|:-------------|
| *network_prefix* | A.B.C.D/M | Specify the network prefix for the area.|
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# network 10.10.10.0/24 area 1
switch(config-router)# network 100.10.10.0/24 area 0.0.0.2
```
### Unset OSPF network for the area
#### Syntax ####
`no network <network_prefix> area (<area_ip>|<area_id>)`
#### Description ####
This command disables OSPF on the network. The interfaces which have an IP address configured in this network or in a subset of this network, will stop participating in the OSPF protocol.
#### Authority ####
All users.
#### Parameters ####
| Parameter        | Syntax    | Description  |
|:-----------------|:----------|:-------------|
| *network_prefix* | A.B.C.D/M | Specify the network prefix for the area.|
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax       | Description          |
|:----------|:------------:|:---------------------|
| *area_ip* | A.B.C.D      | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no network 10.10.10.0/24 area 1
switch(config-router)# no network 100.10.10.0/24 area 0.0.0.2
```
### Enable OSPF area authentication
#### Syntax ####
`area  (<area_ip>|<area_id>) authentication [message-digest]`
#### Description ####
This command enables authentication for an area.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

Parameters for enabling authentication.

| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **authentication** | Required | Literal | Enable authentication for the area with a simple password. |
| **message-digest** | Optional| Literal  | Enable message-digest authentication.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# area  1 authentication
switch(config-router)# area 0.0.0.2 authentication
switch(config-router)#
switch(config-router)# area 0.0.0.2 authentication message-digest
switch(config-router)#
```
### Disable OSPF area authentication
#### Syntax
`no area  (<area_ip>|<area_id>) authentication`
#### Description
This command disables authentication for an area.
#### Authority
All users.
#### Parameters
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.


| Parameter | Status   | Syntax | Description |
|:-----------|:----------|:-------------:|:--------------|
| **authentication** | Required | Literal | Disable authentication for the area. |
#### Examples
```
switch# configure terminal
switch# router ospf
switch#(config-router) no area  1 authentication
switch#(config-router)
```
### Set cost for default LSA summary
#### Syntax ####
`area (<area_ip>|<area_id>) default-cost <cost>`
#### Description ####
This command sets the cost of default-summary LSAs announced to NSSA or the stub areas.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **default-cost** | Required | Literal | Sets the cost of default-summary LSAs announced to NSSA or the stub areas. |
| *cost* | Required | 0-16777215 | Cost of default-summary LSAs announced to the stubby areas. |
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# area  1 default-cost 2
switch(config-router)# area 0.0.0.2 default-cost 2
switch(config-router)#
```
### Set cost for default LSA summary to default
#### Syntax ####
`no area (<area_ip>|<area_id>) default-cost [<cost>]`
#### Description ####
This command resets the cost of the default-summary LSAs announced to NSSA or stub areas, to the default. The default value is one.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **default-cost** | Required | Literal | Sets the cost of the default-summary LSAs announced to NSSA or stub areas, to default. |
| *cost* | Optional | 0-16777215 | Configured cost of default-summary LSAs announced to the stubby areas. |
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no area  1 default-cost 2
switch(config-router)# no area 0.0.0.2 default-cost 2
switch(config-router)#
```
### Set the area as NSSA
#### Syntax ####
`area (<area_ip>|<area_id>) nssa {translate-candidate|translate-never|translate-always} [no-summary]`
#### Description ####
This command changes the area type to NSSA (Not So Stubby Area).
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

Choose one of the parameters from the following table to configure ABR (area border router).

| Parameter | Status| Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **translate-candidate** | Optional | Literal | Configure NSSA-ABR for translate election. This is the default behaviour.|
| **translate-never** | Optional | Literal | Configure NSSA-ABR to never translate.
| **translate-always** | Optional | Literal | Configure NSSA-ABR to always translate.

| Parameter | Status| Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **nssa** | Required | Literal | Configure OSPF area as NSSA.|
| **no-summary** | Optional | Literal |  Do not inject inter-area routes into NSSA.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 1 nssa
switch(config-router)# area 1 nssa  no-summary
switch(config-router)# area 1 nssa translate-always no-summary
switch(config-router)# area 1 nssa translate-always
switch(config-router)#
```
### Unset the area as NSSA
#### Syntax ####
`no area (<area_ip>|<area_id>) nssa [no_summary]`
#### Description ####
This command unsets the area type as NSSA (Not So Stubby Area). That is,the configured area will not be NSSA. The `no area (<area_ip>|<area_id>) nssa no_summary` command enables sending inter-area routes into NSSA, but will not unset the area as NSSA.
#### Authority ####
All users.
#### Parameters
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Status| Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **nssa** | Required | Literal | Unset area as NSSA.|
| **no-summary** | Optional | Literal |  Inject inter-area routes into NSSA.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no area 1 nssa
switch(config-router)# no area 1 nssa  no-summary
switch(config-router)#
```
### Configure the area as stub
#### Syntax ####
`area (<area_ip>|<area_id>) stub [no_summary]`
#### Description ####
This command sets the area type as stub.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Status| Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **stub** | Required | Literal | Configure OSPF area as stub.|
| **no-summary** | Optional | Literal |  Do not inject inter-area routes into stub areas.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 1 stub
switch(config-router)# area 1 stub no-summary
switch(config-router)#
```
### Unset the area as stub
#### Syntax ####
`no area (<area_ip>|<area_id>) stub [no_summary]`
#### Description ####
This command unsets the area type as stub. This means that the configured area becomes an area type default.
The `no area (<area_ip>|<area_id>) stub no_summary` command will stop sending inter-area routes into the stub area, but will not unset the area as stub.
#### Authority ####
All users.
#### Parameters
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Status| Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **stub** | Required | Literal | Unset area as stub.|
| **no-summary** | Optional | Literal |  Inject inter-area routes into stub areas.
### Summarize intra-area paths
#### Syntax ####
`area (<area_ip>|<area_id>) range <ipv4_address> {cost <range_cost> | not-advertise}`
#### Description ####
This command summarizes the routes with the matching address or masks. This command only works for border routers.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Status| Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **ipv4_address** | Required | A.B.C.D/M | Area range prefix.|

Choose one of the parameter sets from the following tables.

| Parameter[1] |Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **cost** | Literal | User specified metric for this range.|
| **range_cost** | 0-16777215 | Metric for this range. |

| Parameter[2] |Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **not-advertise** | Literal | Do not advertise this range to other areas.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# area  1 range  16.77.114.0/24
switch(config-router)# area  1 range  16.77.114.0/24 cost 40
switch(config-router)# area  1 range  16.77.114.0/24 not-advertise
```
### Unset summarization
#### Syntax ####
`no area (<area_ip>|<area_id>) range <ipv4_address> {cost <range_cost> | not-advertise}`
#### Description ####
This command unsets the route summarization for the configured IPv4 prefix address on the ABR.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description                           |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Status| Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **ipv4_address** | Required | A.B.C.D/M | Area range prefix.|

Choose one of the parameter sets from the following tables.

| Parameter[1] |Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **cost** | Literal | User specified metric for this range.|
| **range_cost** | 0-16777215 | Metric for this range. |

| Parameter[2] |Syntax| Description|
|:-----------|:----------|:----------------:|:-------------------|
| **not-advertise** | Literal | Do not advertise this range to other areas.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no area  1 range  16.77.114.0/24
switch(config-router)# no area  1 range  16.77.114.0/24 cost 40
switch(config-router)# no area  1 range  16.77.114.0/24 not-advertise
```
### Filter networks between OSPF areas
#### Syntax ####
`area (<area_ip>|<area_id>) filter-list <list-name> (in|out)`
#### Description ####
This command filters networks between OSPF areas. The filtering is done as per the prefix lists. This command is only used on area border routers.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| **filter-list** | Literal| Filter networks/routes between OSPF areas.|

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| *list-name* | - | Prefix list name.|

Select one of the parameters from the following table to filter incoming networks or outgoing networks.

| Parameter | Description |
|:-----------|:-----------|
| **in** | Filter networks sent to this area. |
| **out** | Filter networks sent from this area. |
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 1 filter-list list1 in
switch(config-router)# area 1 filter-list list2 out
switch(config-router)#
```
### Disable filtering of networks between OSPF areas
#### Syntax ####
`no area (<area_ip>|<area_id>) filter-list <list-name>  (in|out)`
#### Description ####
This command disables network filtering for a particular area. This command is only used on area border routers.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| **filter-list** | Literal| Stop filtering networks/routes between OSPF areas.|

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| *list-name* | - | Prefix list name.|

Select one of the parameters from the following table to disable filtering for either incoming networks or outgoing networks.

| Parameter | Description |
|:-----------|:-----------|
| **in** | Disable filtering of networks sent to this area. |
| **out** | Disable filtering of networks sent from this area. |
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no area 1 filter-list list1 in
switch(config-router)# no area 1 filter-list list2 out
switch(config-router)#
```
### Configure OSPF virtual links
#### Syntax ####
`area (<area_ip>|<area_id>) virtual-link <remote_address> {authentication (message-digest|null)}`
#### Description ####
This command creates a virtual link with the remote ABR and optionally sets authentication type that will be used.
The `area (<area_ip>|<area_id>) virtual-link <remote_address>` command creates an OSPF virtual link with remote ABR.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| **virtual-link** | Literal| Configure a virtual link.|
| *remote_address* | A.B.C.D | Router ID of the remote ABR.|

| Parameter | Syntax | Syntax | Description |
|:-----------|:----------------:|:----------------:|:------------------|
| **authentication** | Optional | Literal| Select authentication type for the virtual link.|

Choose one of the authentication types from the following table.

| Parameter | Description |
|:-----------|:----------------:|:------------------|
| **message-digest** | Set authentication as message-digest.|
| **null** | Use null authentication.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 100 virtual-link  100.0.1.1
switch(config-router)# area 100 virtual-link  100.0.1.1 authentication message-digest
switch(config-router)# area 100 virtual-link  100.0.1.1 authentication null
```
### Delete OSPF virtual links
#### Syntax ####
`no area (<area_ip>|<area_id>) virtual-link <remote_address> [authentication]`
#### Description ####
This command deletes a virtual link with the remote ABR and optionally sets authentication type to the default. The `no area (<area_ip>|<area_id>) virtual-link <remote_address>` command deletes an OSPF virtual link with remote ABR.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| **virtual-link** | Literal| Configure a virtual link to the default settings/Delete the virtual link.|
| *remote_address* | A.B.C.D | Router ID of the remote ABR.|

| Parameter | Syntax | Syntax | Description |
|:-----------|:----------------:|:----------------:|:------------------|
| **authentication** | Optional | Literal| Set the authentication type for virtual link to the default. By default the virtual link will have no authentication.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no area 100 virtual-link  100.0.1.1
switch(config-router)# no area 100 virtual-link  100.0.1.1 authentication
```
### Set OSPF virtual links authentication keys
#### Syntax ####
`area (<area_ip>|<area_id>) virtual-link <remote_address> [authentication-key <auth_key> | message-digest-key <key_id> md5 <key> ]`
#### Description ####
This command sets the authentication key that is used for a particular authentication. The `area (<area_ip>|<area_id>) virtual-link <remote_address> authentication-key <auth_key>` command sets a plain text authentication key and the `area (<area_ip>|<area_id>) virtual-link <remote_address> message-digest-key <key_id> md5 <key>` command sets the message digest authentication key.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| **virtual-link** | Literal| Configure a virtual link.|
| *remote_address* | A.B.C.D | Router ID of the remote ABR.|

Choose one of the parameter sets from the following tables.

| Parameter[1] | Syntax | Description |
|:-----------|:----------------:|:------------------|
| **authentication-key** | Literal| Set authentication key for plain text authentication.|
| *auth_key* | -| Key value for authentication.|

| Parameter[2] | Syntax | Description |
|:-----------|:----------------:|:------------------|
| **message-digest-key** | Literal| Set authentication key for message digest authentication.|
| *key_id* | 1-255 | Key identification number.|
| **md5** | Literal | Use message-digest algorithm as md5.|
| *key* | - | message-digest key string.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 100 virtual-link  100.0.1.1 authentication-key  openswitch
switch(config-router)# area 100 virtual-link  100.0.1.1 message-digest-key  1 md5 openswitch
```
### Delete OSPF virtual links authentication keys
#### Syntax ####
`no area (<area_ip>|<area_id>) virtual-link <remote_address> (authentication-key | message-digest-key) [<key_id>]`
#### Description ####
This command deletes the authentication key that is used for a particular authentication.
The `no area (<area_ip>|<area_id>) virtual-link <remote_address> authentication-key` command deletes the plain text authentication key and the `no area (<area_ip>|<area_id>) virtual-link <remote_address> message-digest-key <key_id>` command deletes the message digest authentication key.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| **virtual-link** | Literal| Configure a virtual link.|
| *remote_address* | A.B.C.D | Router ID of the remote ABR.|

Choose one of the parameter sets from the following tables.

| Parameter[1] | Syntax | Description |
|:-----------|:----------------:|:------------------|
| **authentication-key** | Literal| Delete authentication key for plain text authentication.|

| Parameter[2] | Syntax | Description |
|:-----------|:----------------:|:------------------|
| **message-digest-key** | Literal| Delete authentication key for message digest authentication.|
| *key_id* | 1-255 | Key identification number. This is optional, if not given deletes all the message digest keys.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no area 100 virtual-link  100.0.1.1 authentication-key
switch(config-router)# no area 100 virtual-link  100.0.1.1 message-digest-key
switch(config-router)# no area 100 virtual-link  100.0.1.1 message-digest-key 1
```
### Set OSPF virtual link delays and intervals
#### Syntax ####
`area (<area_ip>|<area_id>) virtual-link <remote_address> (hello-interval | retransmit-interval | transmit-delay  | dead-interval) <time_value>`
#### Description ####
This command sets the time intervals and time delays for virtual links.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| **virtual-link** | Literal| Configure a virtual link.|
| *remote_address* | A.B.C.D | Router ID of the remote ABR.|

Choose one of the following parameters for which time interval or delay is to be set.

| Parameter | Description |
|:-----------|:------------------|
| **hello-interval** | Set time interval between OSPF hello packets.|
| **retransmit-interval** | Set time between retransmitting lost link state advertisements.|
| **transmit-delay** | Set time delay in Link state transmission.|
| **dead-interval** | Set interval after which a neighbor is declared dead if no response comes.|

Set the delay or interval for the above selected parameter.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| *time_value* | 1-65535 | Time delay/interval for the above parameters.|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# area 100 virtual-link  100.0.1.1 hello-interval 30
switch(config-router)# area 100 virtual-link  100.0.1.1 retransmit-interval 30
switch(config-router)# area 100 virtual-link  100.0.1.1 transmit-delay 30
switch(config-router)# area 100 virtual-link  100.0.1.1 dead-interval 30
```
### Set OSPF virtual links delay or interval to default
#### Syntax ####
`no area (<area_ip>|<area_id>) virtual-link <remote_address> (hello-interval | retransmit-interval | transmit-delay  | dead-interval)`
#### Description ####
This command sets the time interval and delay defaults for virtual links.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to identify the area.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:---------------------------------------|
| *area_ip* | A.B.C.D | OSPF area identifier in IPv4 address format. |
| *area_id* | 0-4294967295 | Pass the OSPF area identifier as a decimal value.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| **virtual-link** | Literal| Configure a virtual link.|
| *remote_address* | A.B.C.D | Router ID of the remote ABR.|

Choose any of the parameters in the following table to set the time interval or time delay defaults.

| Parameter | Description |
|:-----------|:------------------|
| **hello-interval** | Set time interval OSPF hello packets to the default. Default value is 10 seconds.|
| **retransmit-interval** | Set time between retransmitting lost link state advertisements to the default. Default value is 5 seconds.|
| **transmit-delay** | Set delay in Link state transmission to the default. The default value is 1 second.|
| **dead-interval** | Set interval after which a neighbor is declared dead, to default. The default value is 40 seconds (Generally 4 times the hello packet interval).|
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no area 100 virtual-link  100.0.1.1 hello-interval
switch(config-router)# no area 100 virtual-link  100.0.1.1 retransmit-interval
switch(config-router)# no area 100 virtual-link  100.0.1.1 transmit-delay
switch(config-router)# no area 100 virtual-link  100.0.1.1 dead-interval
```
### Control distribution of default route information
#### Syntax ####
`default-information originate {always}`
#### Description ####
This command controls the distribution of default route information.
#### Authority ####
All users.
#### Parameters ####
Use one of the following set of parameters to configure default route information distribution.

| Parameter[1] | Syntax         | Description |
|:-----------|:----------------:|:------------------|
| **always** | Literal| Always advertise the default route even if no default route in present.|

#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# default-information  originate
switch(config-router)# default-information  originate always
switch(config-router)#
```
### Disable distribution of default route information
#### Syntax ####
`no default-information originate`
#### Description ####
This command disables the distribution of default route information.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no default-information originate
switch(config-router)#
```
### Set default metric for redistributed routes
#### Syntax ####
`default-metric <metric_value>`
#### Description ####
This command sets the default metric to use for redistributed routes in the OSPF. The metric values are dependent on bandwidth, MTU, and so on.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *metric_value* | Required | 0-16777214  | Sets the default metric value to use for redistributed routes.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# default-metric  37
```
### Set default metric of redistributed routes to default
#### Syntax ####
`no default-metric [metric_value]`
#### Description ####
This command sets the default metric to be used for redistributed routes into OSPF to the default. The default value is 20.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax | Description |
|:-----------|:----------|:------------:|:----------------|
| *metric_value* | Optional | 0-16777214  | Sets the default metric value to use for redistributed routes.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no default-metric
switch(config-router)# no default-metric 37
```
### Define OSPF administrative distance
#### Syntax ####
`distance <admin_distance>`
#### Description ####
This command defines an administrative distance for OSPF. Administrative distance is used as a criteria to select the best route when multiple routes are present.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *admin_distance* | Required | 1-255 | OSPF administrative distance.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# distance 100
```
### Set OSPF administrative distance to default
#### Syntax ####
`no distance <admin_distance>`
#### Description ####
This command sets the OSPF administrative distance to the default. The default value is 110.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *admin_distance* | Required | 1-255 | OSPF administrative distance.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no distance 100
```
### Set OSPF administrative distance for a particular route type
#### Syntax ####
`distance ospf {intra-area <intra_area>|inter-area <inter_area>|external <ext_area>}`
#### Description ####
This command sets the OSPF administrative distance for different OSPF route types.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameter sets from the following tables.

| Parameter[1] | Syntax | Description |
|:-----------|:-----------:|:----------------|
| **intra-area** | Literal| OSPF administrative distance for intra area routes.
| *intra_area* | 1-255| OSPF administrative distance.

| Parameter[2] | Syntax | Description |
|:-----------|:-----------:|:----------------|
| **inter-area** | Literal| OSPF administrative distance for inter area routes.
| *inter_area* | 1-255| OSPF administrative distance.

| Parameter[3] | Syntax | Description |
|:-----------|:-----------:|:----------------|
| **external** | Literal| OSPF administrative distance for external routes.
| *ext_area* | 1-255| OSPF administrative distance.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# distance ospf inter-area 110
switch(config-router)# distance ospf intra-area 110
switch(config-router)# distance ospf external 110
switch(config-router)# distance ospf external 110 inter-area 110
```
### Set OSPF administrative distance for a particular route type to default
#### Syntax ####
`no distance (intra-area |inter-area |external)`
#### Description ####
This command sets the OSPF administrative distance for different OSPF route types to the default. The default value is 110.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table.

| Parameter | Description |
|:-----------|:----------------|
| **intra-area** | OSPF administrative distance for intra area routes to the default.
| **inter-area** | OSPF administrative distance for inter area routes to the default.
| **external** | OSPF administrative distance for external routes to the default.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no distance ospf inter-area
switch(config-router)# no distance ospf intra-area
switch(config-router)# no distance ospf external
```
### Stub router advertisement
#### Syntax ####
`max-metric router-lsa {on-startup <time_startup>}`
#### Description ####
This command maximizes the cost metrics for Router LSA. The Router LSA, or type-1 LSA, has a 16-bit field (65535 in decimal) to represent the “interface output cost”.
Maximizing the Router LSA will take the traffic away from the router being configured. Without any argument, maximized cost will be set administratively (indefinitely).
#### Authority ####
All users.
#### Parameters ####
| Parameter | Syntax | Description |
|:-----------|:--------------:|:----------------|
| **on-startup** | Literal | Automatically advertises stub Router-LSA (or maximizes the router-LSA cost metric), for specified time interval, upon OSPF startup.
| *time_startup* | 5-86400 | Time (seconds) to advertise self as stub-router.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# max-metric router-lsa
switch(config-router)# max-metric router-lsa on-startup 3000
```
### Advertise normal cost metric
#### Syntax ####
`no max-metric router-lsa (on-startup)`
#### Description ####
This command advertises the normal cost metrics instead of advertising the maximized cost metric. This setting causes the router to be considered in traffic forwarding.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Syntax | Description |
|:-----------|:--------------:|:----------------|
| **on-startup** | Literal | Does not automatically advertise the stub Router LSA (or maximize the Router LSA cost metric) during OSPF startup.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no max-metric router-lsa
switch(config-router)# no max-metric router-lsa on-startup
```
### Log changes in the adjacency state
#### Syntax ####
`log-adjacency-changes [detail]`
#### Description ####
This command configures the router to log the adjacency status changes.
With the optional *detail* argument, all the changes in the adjacency status are displayed. Without the optional *detail* argument, only status changes to full or regressions are displayed.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| **detail** | Optional | Literal | Send a syslog message for all the link state changes.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# log-adjacency-changes
switch(config-router)# log-adjacency-changes detail
```
### Disable logging changes in the adjacency state
#### Syntax ####
`no log-adjacency-changes [detail]`
#### Description ####
This command disables logging a syslog message when there is an OSPF link state change or when a neighbor goes up or down. The `no log-adjacency-changes` command disables logging completely.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax | Description |
|:-----------|:----------|:---------------:|:---------------------|
| **detail** | Optional | Literal | Disable logging link state changes. Neighbor up or down events are still be reported.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no log-adjacency-changes
switch(config-router)# no log-adjacency-changes detail
```
### Suppress routing updates
#### Syntax ####
`passive-interface default`
#### Description ####
This command configures all interfaces by default to OSPFv2 passive mode. The interfaces in passive mode won't send routing updates, but advertise the interface as a stub link in the Router-LSA (Link State Advertisement) for this router. This allows you to advertise addresses on such connected interfaces without having to originate AS-External/Type-5 LSAs (which has global flooding scope), as it would occur if connected addresses were redistributed into OSPF.
If an adjacency exists with the router being configured, then it will be dropped immediately and the router appears down. You must configure the interface using the `no ip ospf passive` command under the interface context to activate an interface for OSPFv2.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# passive-interface default
```
### Enable router to send routing updates
#### Syntax ####
`no passive-interface default`
#### Description ####
This command enables sending routing updates from any router interface being configured. This enables the router to establish any adjacency if one exists.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no passive-interface default
```
### Enable auto cost calculation
#### Syntax ####
`auto-cost reference-bandwidth <ref_bandwidth>`
#### Description ####
This command enables automatic OSPF interface cost calculation depending on the bandwidth.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax | Description |
|:-----------|:----------|:-------------:|:----------------|
| *ref_bandwidth* | Required | 1-4294967 |  The reference bandwidth in terms of Mbits per second.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# auto-cost reference-bandwidth 10000
```
### Disable auto cost calculation
#### Syntax ####
`no auto-cost reference-bandwidth`
#### Description ####
This command disables automatic OSPF interface cost calculation depending on the bandwidth. If the user has configured any cost, then that will set or default cost will be set. The default reference bandwidth is 40000 Mbps.

#### Authority ####
All users.

#### Parameters ####
No parameters.

#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no auto-cost reference-bandwidth
```
### Enable OSPF opaque LSA
#### Syntax ####
`capability opaque`
#### Description ####
This command enables handling OSPF opaque LSA on the router.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# capability opaque
```
### Disable OSPF opaque LSA
#### Syntax ####
`no capability opaque`
#### Description ####
This command disables handling OSPF opaque LSA on the router. By default handling opaque LSA is disabled.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no capability opaque
```
### Enable OSPF RFC1583 compatibility
#### Syntax ####
`compatible rfc1583`
#### Description ####
This command enables OSPF compatibility with RFC1583 (backward compatibility). If RFC1583 compatibility is enabled then the route cost calculation follows a different method.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# compatible rfc1583
```
### Disable OSPF RFC1583 compatibility
#### Syntax ####
`no compatible rfc1583`
#### Description ####
This command disables OSPF compatibility with RFC1583 (backward compatibility). By default the RFC1583 compatibility is disabled.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no compatible rfc1583
```
### Redistribute routes into OSPF
#### Syntax ####
`redistribute {bgp | connected | static}`
#### Description ####
This command redistributes routes originating from other protocols to OSPF.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters sets from the following tables to redistribute routes to OSPF.

| Parameter[1] | Syntax | Description |
|:-----------|:-------------:|:----------------|
| **bgp** | Literal | Redistribute BGP routes into OSPF.

| Parameter[2] | Syntax | Description |
|:-----------|:-------------:|:----------------|
| **connected** | Literal | Redistribute connected routes (directly attached subnet or host).

| Parameter[3] | Syntax | Description |
|:-----------|:-------------:|:----------------|
| **static** | Literal |  Redistribute static routes into OSPF.

#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# redistribute connected
switch(config-router)# redistribute bgp
switch(config-router)# redistribute static
```
### Disable redistributing routes into OSPF
#### Syntax ####
`no redistribute {bgp | connected | static}`
#### Description ####
This command disables redistributing routes originating from other protocols to OSPF.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters sets from the following tables to disable redistributing routes into OSPF.

| Parameter[1] | Syntax | Description |
|:-----------|:-------------:|:----------------|
| **bgp** | Literal | Disable redistributing BGP routes into OSPF.

| Parameter[2] | Syntax | Description |
|:-----------|:-------------:|:----------------|
| **connected** | Literal |  Disable redistributing connected routes (directly attached subnet or host).

| Parameter[3] | Syntax | Description |
|:-----------|:-------------:|:----------------|
| **static** | Literal |   Disable redistributing static routes into OSPF.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no redistribute connected
switch(config-router)# no redistribute bgp
switch(config-router)# no redistribute static
```
### Set OSPF timers
#### Syntax ####
`timers lsa-group-pacing <time_interval>`
#### Description ####
This command sets timers for the OSPF LSA. The `timers lsa-group-pacing` parameter configures the time interval for grouping different LSAs of the same age.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Syntax | Description |
|:-----------|:----------|:----------------|
| **lsa-group-pacing** | Literal | Sets the timer for LSA grouping of the same age and dropping the group when the timer expires.
| *time_interval* | 1-1800 | Time interval in seconds.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# timers lsa-group-pacing 75
```
### Set OSPF timers to default
#### Syntax ####
`no timers lsa-group-pacing`
#### Description ####
This command sets timers for the OSPF LSA to the default. The `no timers lsa-group-pacing` command configures the time interval for grouping different LSAs of the same age to the default.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Syntax | Description |
|:-----------|:----------|:----------------|
| **lsa-group-pacing** | Literal | Sets the timer for LSA grouping LSAs of the same age to the default. The default value is 10 seconds.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no timers lsa-group-pacing
```
### Set OSPF throttling parameters
#### Syntax ####
`timers throttle spf <spf_delay_time> <spf_hold_time> <spf_maximum_time>`
#### Description ####
This command sets the rate limit values for OSPF SPF calculation. The `timers throttle spf` command sets rate limits for SPF calculation. Initial SPF calculation is done after a specific delay named *start time interval*. After each topology change (needing SPF calculation) the hold time is doubled until the maximum hold time is reached. If there is no more topology change before the hold timer expires, then the hold time is set back to the *start time interval* value and the process continues. Throttling is done to avoid continuous spike in cpu usage.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Syntax | Description |
|:-----------|:----------|:----------|:----------------|
| **spf** | Literal | Sets the rate limit for SPF calculation.
| *spf_delay_time* | 1-600000 | Set delay in milliseconds for initial SPF calculation.
| *spf_hold_time* | 1-600000 | Set initial hold time for next SPF calculation.
| *spf_maximum_time* | 1-600000 | Set maximum hold time for SPF calculation.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# timers throttle spf 100 100000 300000
```
### Set OSPF throttling parameters to default
#### Syntax ####
`no timers throttle spf`
#### Description ####
This command sets the rate limit values for OSPF SPF calculation to the default.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Syntax | Description |
|:-----------|:----------|:----------|:----------------|
| **spf** | Literal | Sets the rate limit for SPF calculation to the default. The default start time, hold time and maximum hold time are 200, 1000 and 10000 respectively.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)# no timers throttle spf
```
### Configure NBMA neighbor
#### Syntax ####
`neighbor <neighbor_ip> {poll-interval <poll_value> | priority <priority_value>}`
#### Description ####
This command specifies the NBMA neighbor and can also optionally set priority and polling interval (in seconds) for that neighbor.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *neighbor_ip* | Required | A.B.C.D | IP address of the neighbor.

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| **poll-interval** | Optional | Literal | Sets the dead neighbor polling interval.
| *poll_value* | Optional | 1-65535 | Polling interval value in seconds.

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| **priority** | Optional | Literal | Sets priority for the neighbor.
| *priority_value* | Optional | 0-255 | Priority value for the neighbor.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)#
switch(config-router)# neighbor 16.77.114.14
switch(config-router)# neighbor 16.77.114.14 poll-interval 40
switch(config-router)# neighbor 16.77.114.14 priority 20
switch(config-router)# neighbor 16.77.114.14 priority 20 poll-interval 40
```
### Remove NBMA neighbor
#### Syntax ####
`no neighbor <neighbor_ip> {poll-interval | priority}`
#### Description ####
This command removes a NBMA neighbor and can also reset priority and polling interval (in seconds) for that neighbor as a default.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *neighbor_ip* | Required | A.B.C.D | IP address of the neighbor.

Choose one of the parameters from the following table to set the default value for the neighbor configuration.

| Parameter | Description |
|:-----------|:----------|
| **poll-interval** | Sets the dead neighbor polling interval to the default. The default value is 60 seconds.
| **priority** | Sets the neighbor priority to the default. The default value is 0.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)#
switch(config-router)# no neighbor 16.77.114.14
switch(config-router)# no neighbor 16.77.114.14 poll-interval
switch(config-router)# no neighbor 16.77.114.14 priority
```
### Set the interface as OSPF passive interface
#### Syntax ####
`passive-interface <interface>`
#### Description ####
This command configures the interface as an OSPF passive interface. With this setting the interface does not participate in the OSPF protocol.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *interface* | Required | System defined | Interface name as defined by the system.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)#
switch(config-router)# passive-interface 1
```
### Set the interface as OSPF active interface
#### Syntax ####
`no passive-interface <interface>`
#### Description ####
This command resets the interface as active. With this setting the interface starts participating in the OSPF.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *interface* | Required | System defined | Interface name as defined by the system.
#### Examples ####
```
switch# configure terminal
switch# router ospf
switch(config-router)#
switch(config-router)# no passive-interface 1
```
## Interface context commands
### Enable authentication on the interface
#### Syntax ####
`ip ospf authentication null`
`ip ospf authentication {message-digest}`
`ip ospf authentication-key <key>`
`ip ospf message-digest-key <key_id> md5 <message_digest_key>`
#### Description ####
These commands enable authentication on the interface. The `ip ospf authentication null` command disables authentication on the interface, in case it was enabled by area level authentication commands. The `ip ospf authentication` command enables simple authentication on the interface. The `ip ospf authentication message-digest` command enables message digest authentication on the interface.
To set the key for authentication the `ip ospf authenticati on-key <key>` and `ip ospf message-digest-key <key_id> md5 <message_digest_key>` commands are used.
#### Authority ####
All users.
#### Parameters ####
Parameters for enabling null authentication:

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| **null** | Optional | Literal | Disables authentication on the interface, in case it was enabled by area level authentication commands.
Parameters for enabling authentication:

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| **message-digest** | Optional | Literal | Enables message digest authentication.
Parameters for setting the simple authentication key:

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:----------------|
| *key* | Required | - | Key for authentication.
Parameters for setting the message digest authentication key:

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:-----------------|
| *key_id* | Required | 1-255 | Key id of the authentication key.
| **md5** | Required | Literal | Uses the md5 authentication algorithm.
| *message_digest_key* | Required | - | Key for message digest authentication.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# ip ospf authentication
switch(config-if)# ip ospf authentication-key openswitch
switch(config-if)# ip ospf authentication message-digest
switch(config-if)# ip ospf message-digest-key 1 md5 openswitch
```
### Disable authentication on the interface
#### Syntax ####
`no ip ospf authentication`
`no ip ospf authentication-key`
`no ip ospf message-digest-key <key_id>`
#### Description ####
These commands disable authentication on the interface. The `no ip ospf authentication` command disables authentication on the interface completely.
To unset the key for authentication use the `no ip ospf authentication-key` and `no ip ospf message-digest-key <key_id>` commands.
#### Authority ####
All users.
#### Parameters ####
Parameters for removing the message digest authentication key:

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *key_id* | Required | 1-255 | Key id of the authentication key.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# no ip ospf authentication
switch(config-if)# no ip ospf authentication-key
switch(config-if)# no ip ospf message-digest-key 1
```
### Set time interval between hello packets for the interface
#### Syntax ####
`ip ospf hello-interval <hello_interval>`
#### Description ####
This command sets interval in seconds, between hello packets.
#### Authority ####
All users.
#### Parameters ####
Parameters for removing the message digest authentication key:

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *hello_interval* | Required | 1-65535 | Time interval in seconds.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# ip ospf hello-interval 120
```
### Set time interval between hello packets for the interface to default
#### Syntax ####
`no ip ospf hello-interval`
#### Description ####
This command sets the interval between hello packets in seconds. The default value is 10 seconds.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# no ip ospf hello-interval
```
### Set neighbor dead interval for the interface
#### Syntax ####
`ip ospf dead-interval <dead_interval>`
#### Description ####
This command sets the interval in seconds, in which a neighbor connected to the interface is declared dead.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *dead_interval* | Required | 1-65535 | Time interval in seconds.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# ip ospf dead-interval 120
```
### Set neighbor dead interval for the interface to default
#### Syntax ####
`no ip ospf dead-interval`
#### Description ####
This command sets the interval in seconds, after which a neighbor connected to the interface is declared dead to the default. The default value is 40 seconds (four times the hello-interval).
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# no ip ospf dead-interval
```
### Disable MTU mismatch detection
#### Syntax ####
`ip ospf mtu-ignore`
#### Description ####
This command disables the MTU mismatch detection on the interface. When the MTU value in the database description packet that is coming from a neighbor is larger than the router can handle then the packet may be dropped without this setting.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# ip ospf mtu-ignore
```
### Enable MTU mismatch detection
#### Syntax ####
`no ip ospf mtu-ignore`
#### Description ####
This command enables the MTU mismatch detection on the interface. When the MTU value in the database description packet that is coming from a neighbor is larger than the router can handle, the packet may be dropped with this setting.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# no ip ospf mtu-ignore
```
### Set the interface cost
#### Syntax ####
`no ip ospf cost <interface_cost>`
#### Description ####
This command sets the cost (metric) associated with a particular interface. The interface cost is used as a parameter to calculate the best routes.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax | Description |
|:-----------|:----------|:----------------:|:--------------|
| *interface_cost* | Required | 1-65535 | Interface cost value.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# ip ospf cost 100
```
### Set the interface cost to default
#### Syntax ####
`no ip ospf cost`
#### Description ####
This command sets the cost (metric) associated with a particular interface to the default. The default cost is calculated automatically depending on the bandwidth of the interface.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# no ip ospf cost
```
### Set OSPF network type for the interface
#### Syntax ####
`ip ospf network (broadcast|point-to-point)`
#### Description ####
This command explicitly sets the network type for the interface.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table as the interface network type.

| Parameter | Description |
|:-----------|:----------|
| **broadcast** | Sets the OSPF network type as a broadcast multi-access network.
| **point-to-point** | Sets the OSPF network type as a point-to-point network.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# ip ospf network broadcast
switch(config-if)# ip ospf network point-to-point
```
### Set OSPF network type for the interface to default
#### Syntax ####
`no ip ospf network`
#### Description ####
This command sets the network type for the interface to the system default.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# no ip ospf network
```
### Set the OSPF priority for the interface
#### Syntax ####
`ip ospf priority <priority_value>`
#### Description ####
This command sets the OSPF priority for the interface. The larger the numeric value of the priority, the higher the chances there is for it to become the designated router. Setting a priority of 0 makes the router ineligible to become a designated router.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *priority_value* | Required | 0-255 | OSPF priority value.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# ip ospf priority 50
```
### Set the OSPF priority for the interface to default
#### Syntax ####
`no ip ospf priority`
#### Description ####
This command sets the OSPF priority for the interface to the default. The default priority for any interface is one.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# no ip ospf priority
```
### Set the retransmit interval for the interface
#### Syntax ####
`ip ospf retransmit-interval <retransmit_interval>`
#### Description ####
This command sets time interval between transmitting and then retransmitting the lost link state advertisements for the interface.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *retransmit_interval* | Required | 3-65535 | Time interval in seconds.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# ip ospf retransmit-interval 10
```
### Set the retransmit interval for the interface to default
#### Syntax ####
`no ip ospf retransmit-interval`
#### Description ####
This command sets the time interval between transmitting and then retransmitting the lost link state advertisements for the interface to the default. The default value is five seconds.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# no ip ospf retransmit-interval
```
### Set the transmit delay for the interface
#### Syntax ####
`ip ospf transmit-delay <transmit_delay_time>`
#### Description ####
This command sets the time delay for the OSPF packet transmission. The LSA age is incremented by this value when transmitting.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *transmit_delay_time* | Required | 1-65535 | Time interval in seconds.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# ip ospf transmit-delay 10
```
### Set the transmit delay for the interface to default
#### Syntax ####
`no ip ospf transmit-delay`
#### Description ####
This command sets the time delay for the OSPF packet transmission to the default. The default value is one second.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# configure terminal
switch# interface 1
switch(config-if)# no ip ospf transmit-delay
```
# OSPFv2 show commands
### Show general OSPF configurations
#### Syntax ####
`show ip ospf [border-routers]`
#### Description ####
This command shows information on a variety of general OSPF, area, state, and configuration information.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| **border-routers** | Optional | Literal | Show information only of border-routers.
#### Examples ####
```
switch# show ip ospf
OSPF Routing Process, Router ID: 16.77.114.14
 Supports only single TOS (TOS0) routes
 This implementation conforms to RFC2328
 RFC1583Compatibility flag is enabled
 OpaqueCapability flag is enabled
 Stub router advertisement is configured
   Enabled for 2000s after start-up
 Initial SPF scheduling delay 3000 millisec(s)
 Minimum hold time between consecutive SPFs 3000 millisec(s)
 Maximum hold time between consecutive SPFs 5000 millisec(s)
 Hold time multiplier is currently 1
 Refresh timer 10 secs
 This router is an ABR, This router is ASBR
 Number of external LSA 0. Checksum Sum 0x00000000
 Number of opaque AS LSA 0. Checksum Sum 0x00000000
 Number of areas attached to this router: 2
 All adjacency changes are logged

 Area ID: 0.0.0.0 (Backbone)
   Number of interfaces in this area: Total: 1, Active: 1
   Number of fully adjacent neighbors in this area: 0
   Area has no authentication
   SPF algorithm last executed 24m00s ago
   SPF algorithm executed 2 times
   Number of LSA 2
   Number of router LSA 1. Checksum Sum 0x0000267e
   Number of network LSA 0. Checksum Sum 0x00000000
   Number of summary LSA 1. Checksum Sum 0x00006220
   Number of ASBR summary LSA 0. Checksum Sum 0x00000000
   Number of NSSA LSA 0. Checksum Sum 0x00000000
   Number of opaque link LSA 0. Checksum Sum 0x00000000
   Number of opaque area LSA 0. Checksum Sum 0x00000000

 Area ID: 0.0.0.1
   Number of interfaces in this area: Total: 1, Active: 1
   Number of fully adjacent neighbors in this area: 1
   Area has message digest authentication
   Number of full virtual adjacencies going through this area: 0
   SPF algorithm executed 7 times
   Number of LSA 3
   Number of router LSA 2. Checksum Sum 0x00012363
   Number of network LSA 1. Checksum Sum 0x00008761
   Number of summary LSA 0. Checksum Sum 0x00000000
   Number of ASBR summary LSA 0. Checksum Sum 0x00000000
   Number of NSSA LSA 0. Checksum Sum 0x00000000
   Number of opaque link LSA 0. Checksum Sum 0x00000000
   Number of opaque area LSA 0. Checksum Sum 0x00000000

switch# show ip ospf border-routers
============ OSPF router routing table =============
R    16.77.114.14          [10] area: 0.0.0.1, ABR
                           via 16.77.114.14, eth0

```
### Show OSPF database information
#### Syntax ####
`show ip ospf database {asbr-summary|external|network|router|summary|nssa-external|opaque-link|opaque-area|opaque-as|max-age} [<lsa_id>] {self-originate | adv-router <router_id>}`
#### Description ####
This command shows the OSPF link state database summary. The `show ip ospf database` command displays the link state database overview. Use the filters as parameters to get information for a particular link state.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to filter the link state database information.

| Parameter | Description |
|:-----------|:--------------|
| **asbr-summary** | Show ASBR summary link states (LSA type 4).
| **external** | Show external link states (LSA type 5).
| **network** | Show  network LSAs.
| **router** | Show router LSAs.
| **summary** | Show network-summary link states (LSA type 3).
| **nssa-external** | Show NSSA external link states (LSA type 7).
| **opaque-link** | Show opaque Link-Local LSAs.
| **opaque-area** | Show opaque Area LSAs.
| **opaque-as** | Show opaque AS LSAs.
| **max-age** | Show LSAs in max age list.

Parameter to filter the link state database according to link state id.

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *lsa_id* | Optional | A.B.C.D | Show information filtered by link state identifier.

Choose a set of parameters from the following tables for additional filtering.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:--------------|
| **self-originate** | Literal | Shows self-originated link states.

| Parameter | Syntax         | Description |
|:-----------|:----------------:|:--------------|
| **adv-router** | Literal | Shows link states for a particular advertising router.
| *router_id* | A.B.C.D | Router id of the advertising router.
#### Examples ####
```
switch# ip ospf database

       OSPF Router with ID (16.77.114.14)

                Router Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       ChkSum  Link count
16.77.114.14    16.77.114.14     723 0x80000004 0x247f 0

                Summary Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       ChkSum  Route
16.77.114.0     16.77.114.14     482 0x80000003 0x0f79 16.77.114.0/24

                Router Link States (Area 0.0.0.1)

Link ID         ADV Router      Age  Seq#       ChkSum  Link count
16.77.114.12    16.77.114.12     830 0x80000004 0x5483 1
16.77.114.14    16.77.114.14     633 0x80000004 0xcae2 1

                Net Link States (Area 0.0.0.1)

Link ID         ADV Router      Age  Seq#       ChkSum
16.77.114.12    16.77.114.12     790 0x80000002 0x8562

switch# show ip ospf database asbr-summary

    OSPF Router with id(192.168.239.66) (Process ID 300)
                Displaying Summary ASB Link States(Area 0.0.0.0)
 LS age: 1463
 Options: (No TOS-capability)
 LS Type: Summary Links(AS Boundary Router)
 Link State ID: 172.16.245.1 (AS Boundary Router address)
 Advertising Router: 172.16.241.5
 LS Seq Number: 80000072
 Checksum: 0x3548
 Length: 28
 Network Mask: 0.0.0.0
       TOS: 0  Metric: 1

switch# show ip ospf database external

     OSPF Router with id(192.168.239.66) (Autonomous system 300)
                   Displaying AS External Link States
 LS age: 280
 Options: (No TOS-capability)
 LS Type: AS External Link
 Link State ID: 10.105.0.0 (External Network Number)
 Advertising Router: 172.16.70.6
 LS Seq Number: 80000AFD
 Checksum: 0xC3A
 Length: 36
 Network Mask: 255.255.0.0
       Metric Type: 2 (Larger than any link state path)
       TOS: 0
       Metric: 1
       Forward Address: 0.0.0.0
       External Route Tag: 0

switch# show ip ospf database network

       OSPF Router with ID (2.2.2.2)


                Net Link States (Area 0.0.0.1 [NSSA])

  LS age: 3600
  Options: 0x2  : *|-|-|-|-|-|E|*
  LS Flags: 0x3
  LS Type: network-LSA
  Link State ID: 16.77.114.10 (address of Designated Router)
  Advertising Router: 16.77.114.10
  LS Seq Number: 80000001
  Checksum: 0x6988
  Length: 32
  Network Mask: /24
        Attached Router: 16.77.114.10
        Attached Router: 16.77.114.11

  LS age: 754
  Options: 0x8  : *|-|-|-|N/P|-|-|*
  LS Flags: 0x6
  LS Type: network-LSA
  Link State ID: 16.77.114.11 (address of Designated Router)
  Advertising Router: 1.1.1.1
  LS Seq Number: 80000003
  Checksum: 0xb1b5
  Length: 32
  Network Mask: /24
        Attached Router: 2.2.2.2
        Attached Router: 1.1.1.1

  LS age: 104
  Options: 0x8  : *|-|-|-|N/P|-|-|*
  LS Flags: 0x3
  LS Type: network-LSA
  Link State ID: 16.77.114.11 (address of Designated Router)
  Advertising Router: 2.2.2.2
  LS Seq Number: 80000002
  Checksum: 0x95ce
  Length: 32
  Network Mask: /24
        Attached Router: 2.2.2.2
        Attached Router: 1.1.1.1


switch# show ip ospf database router

       OSPF Router with ID (2.2.2.2)


                Router Link States (Area 0.0.0.1 [NSSA])

  LS age: 676
  Options: 0x8  : *|-|-|-|N/P|-|-|*
  LS Flags: 0x6
  Flags: 0x0
  LS Type: router-LSA
  Link State ID: 1.1.1.1
  Advertising Router: 1.1.1.1
  LS Seq Number: 80000007
  Checksum: 0xc7b8
  Length: 36
   Number of Links: 1

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 16.77.114.11
     (Link Data) Router Interface address: 16.77.114.11
      Number of TOS metrics: 0
       TOS 0 Metric: 10


  LS age: 680
  Options: 0x8  : *|-|-|-|N/P|-|-|*
  LS Flags: 0x3
  Flags: 0x2 : ASBR
  LS Type: router-LSA
  Link State ID: 2.2.2.2
  Advertising Router: 2.2.2.2
  LS Seq Number: 80000008
  Checksum: 0xbcc3
  Length: 36
   Number of Links: 1

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 16.77.114.11
     (Link Data) Router Interface address: 16.77.114.10
      Number of TOS metrics: 0
       TOS 0 Metric: 65535


switch# show ip ospf database summary

       OSPF Router with id(192.168.239.66) (Process ID 300)
                Displaying Summary Net Link States(Area 0.0.0.0)
 LS age: 1401
 Options: (No TOS-capability)
 LS Type: Summary Links(Network)
 Link State ID: 172.16.240.0 (summary Network Number)
 Advertising Router: 172.16.241.5
 LS Seq Number: 80000072
 Checksum: 0x84FF
 Length: 28
 Network Mask: 255.255.255.0
       TOS: 0  Metric: 1

switch# show ip ospf database nssa-external

       OSPF Router with ID (2.2.2.2)


                NSSA-external Link States (Area 0.0.0.1 [NSSA])

  LS age: 43
  Options: 0xa  : *|-|-|-|N/P|-|E|*
  LS Flags: 0xb
  LS Type: NSSA-LSA
  Link State ID: 0.0.0.0 (External Network Number for NSSA)
  Advertising Router: 2.2.2.2
  LS Seq Number: 80000001
  Checksum: 0xc81d
  Length: 36
  Network Mask: /0
        Metric Type: 2 (Larger than any link state path)
        TOS: 0
        Metric: 1
        NSSA: Forward Address: 16.77.114.10
        External Route Tag: 0

switch# show ip ospf database external 0.0.0.0

       OSPF Router with ID (2.2.2.2)

                AS External Link States

  LS age: 338
  Options: 0x2  : *|-|-|-|-|-|E|*
  LS Flags: 0xb
  LS Type: AS-external-LSA
  Link State ID: 0.0.0.0 (External Network Number)
  Advertising Router: 2.2.2.2
  LS Seq Number: 80000004
  Checksum: 0xaa1c
  Length: 36
  Network Mask: /0
        Metric Type: 2 (Larger than any link state path)
        TOS: 0
        Metric: 1
        Forward Address: 0.0.0.0
        External Route Tag: 0

switch# show ip ospf database network 16.77.114.11

       OSPF Router with ID (2.2.2.2)


                Net Link States (Area 0.0.0.1 [NSSA])

  LS age: 805
  Options: 0x8  : *|-|-|-|N/P|-|-|*
  LS Flags: 0x6
  LS Type: network-LSA
  Link State ID: 16.77.114.11 (address of Designated Router)
  Advertising Router: 1.1.1.1
  LS Seq Number: 80000003
  Checksum: 0xb1b5
  Length: 32
  Network Mask: /24
        Attached Router: 2.2.2.2
        Attached Router: 1.1.1.1

  LS age: 154
  Options: 0x8  : *|-|-|-|N/P|-|-|*
  LS Flags: 0x3
  LS Type: network-LSA
  Link State ID: 16.77.114.11 (address of Designated Router)
  Advertising Router: 2.2.2.2
  LS Seq Number: 80000002
  Checksum: 0x95ce
  Length: 32
  Network Mask: /24
        Attached Router: 2.2.2.2
        Attached Router: 1.1.1.1

```
### Show OSPF interface information
#### Syntax ####
`show ip ospf interface [<interface_name>]`
#### Description ####
This command displays information about OSPF-enabled interfaces.
#### Authority ####
All users.
#### Parameters ####
| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *interface_name* | Optional | System defined | Shows information only of a particular interface.
#### Examples ####
```
switch# show ip ospf interface
eth0 is up
  MTU 1500 bytes, BW 0 Mbps <UP,BROADCAST,RUNNING>
  Internet Address 16.77.114.10/24, Area 0.0.0.1 [NSSA]
  MTU mismatch detection:enabled
  Router ID 2.2.2.2, Network Type BROADCAST, Cost: 333
  Transmit Delay is 1 sec, State Backup, Priority 100
  Designated Router (ID) 1.1.1.1, Interface Address 16.77.114.11
  Backup Designated Router (ID) 2.2.2.2, Interface Address 16.77.114.10
  Saved Network-LSA sequence number 0x80000002
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 1.976s
  Neighbor Count is 1, Adjacent neighbor count is 1
lo is up
  ifindex 1, MTU 65536 bytes, BW 0 Kbit <UP,LOOPBACK,RUNNING>
  OSPF not enabled on this interface
----------
----------

switch# show ip ospf interface eth0
eth0 is up
  ifindex 444, MTU 1500 bytes, BW 0 Kbit <UP,BROADCAST,RUNNING>
  Internet Address 16.77.114.10/24, Broadcast 16.77.114.255, Area 0.0.0.1 [NSSA]
  MTU mismatch detection:enabled
  Router ID 2.2.2.2, Network Type BROADCAST, Cost: 333
  Transmit Delay is 1 sec, State Backup, Priority 100
  Designated Router (ID) 1.1.1.1, Interface Address 16.77.114.11
  Backup Designated Router (ID) 2.2.2.2, Interface Address 16.77.114.10
  Multicast group memberships: OSPFAllRouters OSPFDesignatedRouters
  Timer intervals configured, Hello 10s, Dead 40s, Wait 40s, Retransmit 5
    Hello due in 1.976s
  Neighbor Count is 1, Adjacent neighbor count is 1
```
### Show OSPF neighbor information
#### Syntax ####
`show ip ospf neighbor {<interface_name> | <neighbor_id>} [detail] [all]`
#### Description ####
This command displays information about OSPF neighbors.
#### Authority ####
All users.
#### Parameters ####
Choose one of the parameters from the following table to get information about a particular neighbor.

| Parameter | Status   | Syntax         | Description |
|:-----------|:----------|:----------------:|:--------------|
| *interface_name* | Optional | System defined | Shows information only of a neighbor connected to a particular interface.|
| *neighbor_id* | Optional | A.B.C.D | Shows information about a particular neighbor.|

Choose the following optional parameters to format the result.

| Parameter | Description |
|:-----------|:--------------|
| **detail** | Shows detailed information about the neighbors.
| **all** | Shows information about all the neighbors include those which are dead.
#### Examples ####
```
switch# show ip ospf neighbor

    Neighbor ID Pri State         Dead Time  Address       Interface          RXmtL RqstL DBsmL
1.1.1.1         120 Full/DR        31.403s  16.77.114.11  eth0:16.77.114.10     1     0     0

switch# show ip ospf neighbor eth0

    Neighbor ID Pri State         Dead Time  Address       Interface          RXmtL RqstL DBsmL
1.1.1.1         120 Full/DR        31.403s  16.77.114.11  eth0:16.77.114.10     1     0     0

switch# show ip ospf neighbor detail

 Neighbor 1.1.1.1, interface address 16.77.114.11
    In the area 0.0.0.1 [NSSA] via interface eth0
    Neighbor priority is 120, State is Full, 17 state changes
    Most recent state change statistics:
      Progressive change 56m55s ago
      Regressive change 56m55s ago, due to SeqNumberMismatch
    DR is 16.77.114.11, BDR is 16.77.114.10
    Options 72 *|O|-|-|N/P|-|-|*
    Dead timer due in 37.217s
    Database Summary List 0
    Link State Request List 0
    Link State Retransmission List 1

switch# show ip ospf neighbor all

    Neighbor ID Pri State         Dead Time  Address       Interface          RXmtL RqstL DBsmL
1.1.1.1         120 Full/DR        31.403s  16.77.114.11  eth0:16.77.114.10     1     0     0

//No down status neighbors.
```
### Show OSPF routing table
#### Syntax ####
`show ip ospf route`
#### Description ####
This command displays the OSPF routing table.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# show ip ospf  route
============ OSPF network routing table ============
N    16.77.114.0/24        [65535] area: 0.0.0.1
                           directly attached to eth0

============ OSPF router routing table =============

============ OSPF external routing table ===========
```
### Show OSPF active non default configurations
#### Syntax ####
`show running-configuration ospf`
#### Description ####
This command displays the OSPF active configurations.
#### Authority ####
All users.
#### Parameters ####
No parameters.
#### Examples ####
```
switch# show running-config ospf

Building OSPF configuration...

Current configuration:
!
ospf enable

router ospf
 ospf router-id 2.2.2.2
 log-adjacency-changes detail
 compatible rfc1583
 timers throttle spf 3000 3000 5000
 max-metric router-lsa
 area 0.0.0.1 authentication message-digest
 area 0.0.0.1 nssa translate-always
 neighbor 16.77.114.10 priority 30 poll-interval 30
 default-metric 30
 default-information originate always
 distance 110
 distance ospf inter-area 40 external 30
 capability opaque
!
end
```
