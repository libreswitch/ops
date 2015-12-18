OpenSwitch Check_MK Agent
--------------------
[Check_MK][1] is an open source monitoring solution that provides application, operating system, and hardware monitoring for servers and networking elements. The OpenSwitch Check_MK agent feature allows an OpenSwitch node to be monitored by Check_MK.

The OpenSwitch Check_MK Agent is a relatively small agent, based on the [Check_MK Linux Agent][3],  that runs system and OVSDB commands to gather and report system data to the Check_MK server.

The figure below shows the high level view of OPS Check_MK Agent:
```ditaa
                   +---------------------------------+
+------------+     |  +--------------+   +--------+  |
| Check_MK   |     |  |   OPS        |   |        |  |
| Server     +--------+   Check_MK   +---+ OVSDB  |  |
| (e.g. OMD) |     |  |   Agent      |   |        |  |
|            |     |  +------+-------+   +--------+  |
+------------+     |         |                       |
                   |  +------+--------------------+  |
                   |  |          Linux            |  |
                   |  +---------------------------+  |
                   |                                 |
                   |            OpenSwitch           |
                   +---------------------------------+
```
                                                                                         
[1]: https://mathias-kettner.de/check_mk.html
[2]: https://www.nagios.org/
[3]: https://mathias-kettner.de/checkmk_linuxagent.html
