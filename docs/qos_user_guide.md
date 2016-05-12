# Quality of Service User Guide
<!-- Version 2 -->

## Contents

- [Overview](#overview)
	- [End-to-end behavior](#end-to-end-behavior)
		- [Best effort service](#best-effort-service)
		- [Ethernet class of service](#ethernet-class-of-service)
		- [Internet differentiated services](#internet-differentiated-services)
	- [Queuing and scheduling](#queuing-and-scheduling)
		- [Queue profiles](#queue-profiles)
		- [Schedule profiles](#schedule-profiles)
			- [Strict priority (SP)](#strict-priority-sp)
			- [Deficit weighted round robin (DWRR)](#deficit-weighted-round-robin-dwrr)
			- [Strict priority plus deficit weighted round robin](#strict-priority-plus-deficit-weighted-round-robin)
- [Definition of terms](#definition-of-terms)
- [Configuring QoS trust](#configuring-qos-trust)
	- [Configuring Ethernet class of service](#configuring-ethernet-class-of-service)
	- [Configuring Ethernet 802.1D class of service](#configuring-ethernet-8021d-class-of-service)
	- [Configuring Internet DiffServ](#configuring-internet-diffserv)
- [Configuring queue profiles](#configuring-queue-profiles)
- [Configuring schedule profiles](#configuring-schedule-profiles)
- [Configuring expedited forwarding using priority queuing](#configuring-expedited-forwarding-using-priority-queuing)
- [Monitoring queue operation](#monitoring-queue-operation)
- [References](#references)

## Overview
Quality of Service (QoS) features allow network devices the ability to customize servicing behaviors to different kinds of traffic reflecting each traffic type's unique characteristics and importance your organization:
- Ensure uniform and efficient traffic-handling throughout the network, while keeping the most important traffic moving at an acceptable speed, regardless of current bandwidth usage.
- Exercise control over the priority settings of inbound traffic arriving at each network device.

Packets traverse a network device in 4 stages.  QoS configuration affects stages 1, 3, and 4:
1. **Initial prioritization**
    - QoS trust mode
2. **Destination determination**
3. **Queuing**
    - QoS queue profile
4. **Transmission Scheduling**
    - QoS schedule profile

Besides the packet itself, network devices keep other information regarding the packet collectively called 'metadata':
- arrival port
- arrival VLAN and/or VRF
- destination port
- destination VLAN and/or VRF
- local-priority
- color
- etc

QoS functionality within the network device uses **local-priority** and **color** metadata:

**Local-priority** is generally one of 8 levels (0-7). Zero is the lowest priority. The allowed maximum will vary per product family.  It is used to determine which queues a packet will use.

**Color** is one of three values (0-2), commonly named green (0), yellow (1), and red (2). These are mostly used with packets marked with Assured Forwarding (AF) DSCP values. The default is green (0).

In summary:
- **QoS trust mode** configures how arriving packets are assigned the initial values of their local-priority and color.
- **QoS queue profiles** configures which queues packets will use awaiting transmission.
- **QoS schedule profiles** configures the order of queues selected to transmit packets.


### End-to-end behavior

The QoS configuration of each network device along the path between the source and destination must be aligned to achieve the desired end-to-end behavior.  There are three basic service schemes for end-to-end demarcating different types of traffic:
- Best Effort Service
- Ethernet Class of Service (CoS)
- Internet Differentiated Services (DiffServ)

These three are not mutually exclusive.  Different ports can use different service behaviors.  For your network as a whole, it is best to select one to use as the primary end-to-end behavior. The other two should only be used on an exception basis.

#### Best effort service
This is the simplest behavior.  All traffic is treated equally in a first-come, first-served manner.  If the traffic load is low in relation to the capacity of the network links, then there is no need for the administrative complexity and costs of maintaining an end-to-end policy.  This is sometimes called 'over provisioning' - all link speeds are well higher than the peak loads.

#### Ethernet class of service
The  Ethernet standard 802.1Q provides a means to mark packets with one of eight Classes of Service (CoS).  A 3-bit Priority Code Point field is within the 16-bit Ethernet VLAN tag to mark the packet's class of service:

```ditaa
    +--------+--------+--------+----------+-----------+--------
    | mac-da | mac-sa | 0x8100 | VLAN tag | ethertype | data...
    +--------+--------+--------+----------+-----------+--------
                              /            \
                             /              \
                            /                \
                         +-----+-----+---------+
                         | pcp | dei | vlan_id |
                         +-----+-----+---------+
```
The standard recommends the types of traffic that should use each of the eight classes of service based on their behavior aggregate:


|   CoS    | Traffic Type           | Example Prococols |
|:--------:|:-----------------------|:------------------|
|    7     | Network Control        | STP, PVST         |
|    6     | Internetwork Control   | BGP, OSPF, PIM    |
|    5     | Voice (<10ms latency)  | VoIP(UDP)         |
|    4     | Video (<100ms latency) | RTP               |
|    3     | Critical Applications  | SQL RPC, SNMP     |
|    2     | Excellent Effort       | NFS, SMB          |
|    0     | Best Effort            | HTTP, TELNET      |
|    1     | Background             | SMTP, IMAP        |

Notice that CoS 1 is the lowest CoS and zero is the next higher.  This was deliberate to allow specifying traffic below default (Best Effort) traffic.


#### Internet differentiated services
This is the most sophisticated behavior. Internet Protocol standards (RFC) provides a means to mark packets with one of sixty four service classes, via the Differentiated Services Code Point (DSCP).  The DSCP value is carried within the upper 6-bits of 8-bit IPv4 Type-of-Service (ToS) or IPv6 Traffic Class (TC) header fields.

```ditaa
     IPv4
    +-----+-----+-----+----+--------+-----+-------+--------+-------|-------+-----
    | ver | tos | len | id | offset | ttl | proto | chksum | ip-sa | ip-da | data
    +-----+-----+-----+----+--------+-----+-------+--------+-------|-------+-----
         /       \
        /         \
       +------+-----+
       | dscp | ecn |
       +------+-----+
        \         /
     IPv6\       /
    +-----+-----+-----+-------+-------------+-----------+-------+-------+-----
    | ver | tc  | len | label | next_header | hop_limit | ip-sa | ip-da | data
    +-----+-----+-----+-------+-------------+-----------+-------+-------+-----
```

More standards specify the per-hop behavior (PHB) for many of the code points that is beyond the scope of this document.  The Wikipedia [Differentiated Services](https://en.wikipedia.org/wiki/Differentiated_services) article is a good starting place.

   |  DSCP  |     Name     | Service Class           | RFC
   |:------:|:------------:|:------------------------|:-----
   |   56   |     CS6      | Network Control         | 2474
   |   46   |     EF       | Telephony               | 3246
   |   40   |     CS5      | Signaling               | 2474
   |34,36,38|AF41,AF42,AF43| Multimedia Conferencing | 2597
   |   32   |     CS4      | Real-Time Interactive   | 2474
   |26,28,30|AF31,AF32,AF33| Multimedia Streaming    | 2597
   |   24   |     CS3      | Broadcast Video         | 2474
   |18,20,22|AF21,AF22,AF23| Low-Latency Data        | 2597
   |   16   |     CS2      | OAM                     | 2474
   |10,12,14|AF11,AF12,AF13| High-Throughput Data    | 2597
   |   00   |   CS0,BE,DF  | Standard                | 2474
   |   08   |     CS1      | Low-Priority Data       | 3662

Notice that DSCP CS1 (8) is the lowest priority and CS0 (0) is the next higher.  This was deliberate to allow specifying traffic below standard (best-effort or default-forwarding).


### Queuing and scheduling
When using end-to-end behavior Ethernet Class of Service or Internet Differentiated Services, different priorities of traffic must be placed in different queues so the network device can service them appropriately.  Separate queues allow delay or jitter sensitive traffic to be serviced before more less-time critical or bulk traffic.

#### Queue profiles

Queue policies configure the queues different priorities of traffic will use. Queues are numbered in priority order with zero being the lowest priority.  The larger the queue number the higher priority of the queue.

#### Schedule profiles

Schedule policies configure the order of the queues that packets are taken off (de-queued) to be transmitted. The schedule discipline is the algorithm the scheduler employs each time (round) it must select the next packet for transmission.

##### Strict priority (SP)

This is the simplest of scheduling disciplines.  For each round, the scheduler will select the packet from the highest priority (numbered) queue for transmission.  Effectively, it will always empty all packets from the highest priority queue before any other lower priority queue.

While this does provide prioritization of traffic, when spikes of high priority traffic occur it will prevent lower priority traffic from being transmitted (aka 'queue starvation').

##### Deficit weighted round robin (DWRR)

Deficit weighted round robin can limit queue starvation by providing a fairer distribution of available bandwidth across the priorities.  Lower priority queues will have some service even when packets are present in higher priority queues. The degree to which this occurs depends on the weights assigned to each queue.

Each non-empty queue has a deficit counter, which is used to track the amount of bytes it is allowed to send.  The counter starts at zero when a packet arrives at an empty queue.

At the start of the round, the deficit counters of all non-empty queues are incremented by a quantum value in proportion to their weight.  Then the scheduler will inspect the non-empty queues in decreasing priority order, comparing the queue's deficit counter against the packet size at the head of the queue.  The round ends when a deficit counter is found that is larger than the packet size.  That packet is de-queued for transmission and the queue's deficit counter is decremented.

In general, the deficit counters of lower priority queues will be larger (i.e. they build up a deficit) than the deficit counters of higher priority queues.  With a mix of large and small packet sizes of high priority  traffic, the deficit counters of higher priority queues will have some rounds where they will be smaller than the size of the queue at head of queue.  This occasionally allows traffic from lower priority queues to be selected for transmission.

##### Strict priority plus deficit weighted round robin

SP plus DWRR is a hybrid of two disciplines primarily used in networks carrying voice traffic.  Queuing delay and jitter (i.e. variance in delay) can readily affect the quality of a voice call.  To prevent these conditions, voice traffic should be in the highest priority queue, but what of the traffic in other queues?

Using strict priority for all queues would be good for the voice, but increases the risk of lower priority queue starvation.  DWRR for all queues would be fairer to the lower priority traffic, but at the risk of increased voice traffic delay and jitter.

SP plus DWRR solves both problems.  The highest priority queue is scheduled using strict priority, while the remaining seven lower priority queues use DWRR discipline.

On each round, the scheduler first checks the highest priority queue.  When it has a packet ready, that packet will selected for immediate transmission.  When the highest priority queue is empty, the scheduler uses DWRR discipline to fairly select the next packet for transmission from the remaining lower priority queues.


## Definition of terms
| Term | Description |
|:-----------|:---------------------------------------|
| **Class** | For networking, a set of packets sharing some common characteristic (e.g. all IPv4 packets) |
| **Codepoint**| Used in two different ways -- either as the name of a packet header field or as the name of the values carried within a packet header field: *Example 1: Priority code point (PCP) is the name of a field in the [IEEE 802.1Q](http://www.ieee802.org/1/pages/802.1Q.html) VLAN tag. Example 2: Differentiated services codepoint (DSCP) is the name of values carried within the DS field of the header field.*
| **Color** | A metadata label associated with each packet within the switch with three values: "green", "yellow", or "red". It is used by the switch when packets encounter congestion for resource (queue) to distinguish which packets should be dropped. It is used by the switch when packets encounter congestion for resource (queue) to distinguish which packets should be dropped. |
| **Class of service (CoS)** | A 3-bit value used to mark packets with one of eight classes (levels of priority). It is carried within the priority code point (PCP) field of the [IEEE 802.1Q](http://www.ieee802.org/1/pages/802.1Q.html) VLAN tag. |
| **Differentiated services codepoint (DSCP)** | A 6-bit value used to mark packets for different per-hop behavior as originally defined by [IETF RFC 2474](https://tools.ietf.org/html/rfc2474). It is carried within the differentiated services (DS) field of the IPv4 or IPv6 header. |
| **Local-priority** | A meta-data label associated with a packet within a network switch. It is used by the switch to distinguish packets for different treatment (e.g. queue assignment, etc.) |
| **Metadata** | Information labels associated with each packet in the switch, separate from the packet headers and data. These labels are used by the switch in its handling of the packet. Examples: arrival port, egress port, VLAN membership, local priority, color, etc. |
| **Priority code point (PCP)** | The name of a 3-bit field in the [IEEE 802.1Q](http://www.ieee802.org/1/pages/802.1Q.html) VLAN tag.  It carries the CoS value to mark a packet with one of eight classes (priority levels). |
| **Quality of service (QoS)** | General term used when describing or measuring performance. For networking, it means how different classes of packets are treated across the network or device. For more information, see [https://en.wikipedia.org/wiki/Quality_of_service](https://en.wikipedia.org/wiki/Quality_of_service). |
| **Traffic class (TC)** | General term for a set of packets sharing some common characteristic. It used to be the name of an 8-bit field in the IPv6 header originally defined by [IETF RFC 2460](https://tools.ietf.org/html/rfc2460#section-7). This field name was changed to differentiated services by [IETF RFC 2474](https://tools.ietf.org/html/rfc2474). |
| **Type of service (ToS)** | General term when there are different levels of treatment (e.g. fare class).  It used to be the name of an 8-bit field in the IPv4 header originally defined by [IETF RFC 791](https://tools.ietf.org/html/rfc791). This field name was changed to differentiated services by [IETF RFC 2474](https://tools.ietf.org/html/rfc2474)|


## Configuring QoS trust
QoS trust mode configures the network device end-to-end behavior selected by your organization.  The purpose is to set the initial value of the local-priority and color packet metadata.

The trust mode for all ports can be set in the top-level (global) configuration context with the command **qos trust [none | cos | dscp]**.  The command **no qos trust** will revert the trust mode back to the initial trust mode.  Use the command **show qos trust default** at any time to view the initial trust mode.

There must always be a trust mode configured for every port.  Each product automatically provisions OpenSwitch with a default trust mode for all ports.  Use the command **show qos trust ** to view the current trust mode.  Do not use **show running-configuration** as it will only display changes from the default values.

Each port can have its own trust mode configured.  This will override the top-level (global) trust mode.  In the interface configuration context, enter the command **qos trust [none | cos | dscp]**.  To revert the port back to using the default trust mode, in the interface configuration context enter the command **no qos trust**.

**Note:** The only way to remove qos trust mode from the running configuration display is to revert back to the initial trust mode via **no qos trust**. The same is true for port overrides: Only **no qos trust** will remove the override from the running configuration display.

### Configuring Ethernet class of service
To configure all ports to use Ethernet class of service:
```ditaa
    #configure terminal
    (config)#qos trust cos
```
To configure only one Ethernet port or all members of a link aggregation group (LAG):
```ditaa
    #configure terminal
    (config)# interface 1
    (config-if)# qos trust cos
    (config)# interface lag 100
    (config-if)# qos trust cos
    (config)# interface 2
    (config-if)# lag 10
    (config)# interface 3
    (config-if)# lag 10
```

If **qos trust cos** is configured, the network device uses the **CoS Map** to determine which local-priority and color to assign the packet.  To display the configuration of the CoS Map:
```ditaa
    # show qos cos-map
    code_point local_priority color   name
    ---------- -------------- ------- ----
    0          1              green   Best_Effort
    1          0              green   Background
    2          2              green   Excellent_Effort
    3          3              green   Critical_Applications
    4          4              green   Video
    5          5              green   Voice
    6          6              green   Internetwork_Control
    7          7              green   Network_Control
```

The above configuration follows IEEE 802.1Q standard assignments.

### Configuring Ethernet 802.1D class of service

IEEE 802.1Q is the most current Ethernet standard for class of service.  It superseded an earlier standard, 802.1D, in 2005.  IEEE 802.1Q slightly changed the ordering of the classes of service from its predecessor IEEE 802.1D for CoS 2 and CoS 0:

| CoS 802.1Q               | CoS 802.1D               |
|:-------------------------|:-------------------------|
| 7 Network Control        | 7 Network Control        |
| 6 Internetwork Control   | 6 Voice (<10ms latency)  |
| 5 Voice (<10ms latency)  | 5 Video (<100ms latency) |
| 4 Video (<100ms latency) | 4 Controlled Load        |
| 3 Critical Applications  | 3 Excellent Effort       |
| **2 Excellent Effort**   | **0 Best Effort**        |
| **0 Best Effort**        | **2 Spare**              |
| 1 Background             | 1 Background             |

Note that in 802.1D, both CoS 2 and CoS 1 are below CoS 0 (Best Effort).

When an OpenSwitch device is installed in a network of devices following 802.1D class of service, the QoS Cos Map must be re-configured to follow the 802.1D standard by swapping the assignments of CoS 0 and 2:
```ditaa
    #configure terminal
    (config)#qos cos-map 0 local-priority 2 color green name Best_Effort
    (config)#qos cos-map 2 local-priority 1 color green name Spare
    # show qos cos-map
    code_point local_priority color   name
    ---------- -------------- ------- ----
    0          2              green   Best_Effort
    1          0              green   Background
    2          1              green   Spare
    3          3              green   Critical_Applications
    4          4              green   Video
    5          5              green   Voice
    6          6              green   Internetwork_Control
    7          7              green   Network_Control
```

### Configuring Internet DiffServ
To configure all ports to use Internet differentiated services:
```ditaa
    #configure terminal
    (config)#qos trust dscp
```
To configure only one Ethernet port or all the members of a link aggregation group (LAG):
```ditaa
    #configure terminal
     (config)# interface 1
    (config-if)# qos trust dscp
    (config)# interface lag 100
    (config-if)# qos trust dscp
    (config)# interface 2
    (config-if)# lag 10
    (config)# interface 3
    (config-if)# lag 10
```

For **qos trust dscp**, the network device uses the **DSCP Map** to determine which local-priority and color to assign the packet.  Use **show qos dscp-map** to display the configuration of the DSCP Map.


## Configuring queue profiles
The queue profile determines the assignment of local-priority to queues. A queue-profile must be configured on every port at all times.

OpenSwitch automatically provisions each network device with an initial queue profile named **default**.  Use the command **show qos queue-profile default** to view the product default queue profile.  Do not use **show running-configuration** as it will only display changes from the initial values.

The default queue-profile assigns each local-priority to the queue of the same number.  This should work most all situations.  A new queue profile can be created anytime by entering the command **qos queue-profile NAME**.  Use **map queue QUEUENUM local-priority PRI** commands to assign local-priorities to queues.

Finally, use the **apply qos queue-profile NAME schedule-profile NAME** command to configure all ports to use the new profile.

## Configuring schedule profiles
The schedule profile determines the order of queues selected to transmit a packet. A schedule profile must be configured on every port at all times.

OpenSwitch automatically provisions each network device with an initial schedule profile named **default**.  Use the command **show schedule-profile default** to view the product default schedule profile.  Do not use **show running-configuration** as it will only display changes from the initial values.


## Configuring expedited forwarding using priority queuing
In many organizations, the network carries voice over IP (VoIP) traffic.  It is delay and jitter sensitive, so dwell time in network devices must be kept to a minimum. It is critical that all network devices in the path have their per-hop behaviors configured identically to handle this traffic.

The objective is to configure the network device to have a dedicated queue just for voice traffic, and have that queue serviced before any other traffic.

As a prerequisite, voice traffic packets must be uniquely identified.  Many networks using DiffServ mark voice packets with Expedited Forwarding (EF) DSCP.

To configure all ports to have DSCP EF packets, use the highest priority queue that is serviced first before any other queues' packets. Follow these five steps:
1. Change the default DSCP Map code point to local-priority assignments so EF has its own local-priority (5).
2. Configure a queue profile that puts the EF packets in the highest priority queue.
3. Configure an SP plus DWRR schedule profile.
4. Apply the queue and schedule profiles.
5. Configure global trust mode to DSCP.

**Step 1: Change the default DSCP Map for code points using local-priority 5**
The default DSCP Map has DSCP EF assigned to local-priority 5.  It is necessary to have packets with DSCP EF be the sole user of local priority 5.  The default DSCP Map has 8 code points, 40 through 47 (CS5), mapping to local-priority 5.  The other seven code points have to be reassigned to another local-priority, depending on which protocol(s) are using these code points in your network.  This example assumes CS5 is used by Call Signaling protocols and will be assigned local-priority 6.

```ditaa
    #configure terminal
    (config)# qos dscp-map 40 local-priority 6 color green name CS5
    (config)# qos dscp-map 41 local-priority 6 color green
    (config)# qos dscp-map 42 local-priority 6 color green
    (config)# qos dscp-map 43 local-priority 6 color green
    (config)# qos dscp-map 44 local-priority 6 color green
    (config)# qos dscp-map 45 local-priority 6 color green
    (config)# qos dscp-map 47 local-priority 6 color green
```
Now DSCP EF is the only code point using local-priority 5.

**Step 2: Create queue profile**
Create a queue profile that maps local-priority 5 to queue 7.

```ditaa
    #configure terminal
    (config)# qos queue-profile ef_priority
    (config-queue)# name queue 7 Voice_Priority_Queue
    (config-queue)# map queue 7 local-priority 5
    (config-queue)# map queue 6 local-priority 7
    (config-queue)# map queue 5 local-priority 6
    (config-queue)# map queue 4 local-priority 4
    (config-queue)# map queue 3 local-priority 3
    (config-queue)# map queue 2 local-priority 2
    (config-queue)# map queue 1 local-priority 1
    (config-queue)# map queue 0 local-priority 0
```
**Step 3: Create an SP plus DWRR schedule profile**
Create a schedule profile that services queue 7 using strict priority (SP) and the remaining queues using DWRR).  This example will give all DWRR queues equal weight.  The actual weight values will be different in your network.

```ditaa
    #configure terminal
    (config)# qos schedule-profile sp_dwrr
    (config-schedule)# strict queue 7
    (config-schedule)# dwrr queue 6 weight 1
    (config-schedule)# dwrr queue 5 weight 1
    (config-schedule)# dwrr queue 4 weight 1
    (config-schedule)# dwrr queue 3 weight 1
    (config-schedule)# dwrr queue 2 weight 1
    (config-schedule)# dwrr queue 1 weight 1
    (config-schedule)# dwrr queue 0 weight 1
```
**Step 4: Apply the policies to all ports**
Apply the queue and schedule profiles to all ports from the configuration context.

```ditaa
    #configure terminal
    (config)# apply qos queue-profile ef_priority schedule-profile sp_dwrr
```

**Step 5 Configure DSCP trust mode to all ports**

```ditaa
    #configure terminal
    (config)# qos trust dscp
```

## Monitoring queue operation
The **show interface IFACE queues** command will display the number of packets and bytes the queue has transmitted.  Also displayed is the number of packets that were not transmitted.

```
switch# show interface 1 queues

Interface 1 is  (Administratively down)
 Admin state is down
 State information: admin_down
         Tx Packets             Tx Bytes  Tx Packet Errors
 Q0             100                 8000                 0
 Q1         1234567          12345678908                 5
 Q2              0                     0                 0
 Q3              0                     0                 0
 Q4              0                     0                 0
 Q5              0                     0                 0
 Q6              0                     0                 0
 Q7              0                     0                 0
```

## References

* [IEEE 802.1Q-2014](http://www.ieee802.org/1/pages/802.1Q-2014.html) *Bridges and Bridged Networks*
* [IETF RFC 791](https://tools.ietf.org/html/rfc791) *Internet Protocol Specification*
* [IETF RFC 2460](https://tools.ietf.org/html/rfc2460) *Internet Protocol, Version 6 (IPv6) Specification*
* [IETF RFC 2474](https://tools.ietf.org/html/rfc2474) *Definition of the Differentiated Services Field (DS Field) in the IPv4 and IPv6 Headers*
    * [IETF RFC 2475](https://tools.ietf.org/html/rfc2475) *An Architecture for Differentiated Services*
    * [IETF RFC 2497](https://tools.ietf.org/html/rfc2497) *Assured Forwarding PHB Group*
    * [IETF RFC 3246](https://tools.ietf.org/html/rfc3246) *An Expedited Forwarding PHB (Per-Hop Behavior)*
* [IETF RFC 3260](https://tools.ietf.org/html/rfc3260) *New Terminology and Clarifications for Diffserv*
