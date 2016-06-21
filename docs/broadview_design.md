# High-level Design of the BroadView Feature

## Contents
- [Design choices](#design-choices)
- [Participating modules](#participating-modules)
- [References](#references)

## Design choices

The BroadView daemon was chosen as it would export the BST Instrumentation Statistics in the Open BroadView Instrumentation defined REST API (JSON). This allows OpenSwitch to have the BroadView REST API support and allows Collectors and Instrumentation Apps to support OpenSwitch based switches. The same statistics are also available from the OVSDB Schema and would serve Collectors and Management systems that support OVSDB.

## Participating modules
```
                          +----+                           
+--------------------+    | O  |                           
|                    |    | V  |                           
| BroadView Daemon   <----> S  |                           
|                    |    | D  |                           
+--------------------+    | B  |                           
                          | |  |                           
                          | S  |                           
                          | e  |     +----------------+
                          | r  |     |                |
                          | v  <---->+     Driver     |
                          | e  |     |                |
                          | r  |     +----------------+
                          +----+                           

```
The BroadView daemon interfaces with the OVSDB-Server, so it is loosely coupled with the driver. The driver is responsible for obtaining statistics from the switch silicon and populating the BST statistics counters defined via the OVSDB schema. The driver is the *publisher* of the data and the BroadView Daemon is the *subscriber* (consumer) to the data. This allows the design to be modular, with simple, well-defined interfaces.

The BroadView daemon gets the configuration from the OVSDB schema. It exports statistics via its REST API using JSON messaging to a collector or controller.

## References
- [BroadView design](/documents/user/broadview_design)
- [BroadView user guide](/documents/user/broadview_user_guide)
