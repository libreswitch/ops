
OpenSwitch Check_MK Agent User Guide
--------------------
## Contents
- [Overview](#overview)
- [Configuration](#configuration)
- [Extending the Check_MK Agent](#extending-the-checkmk-agent)

##Overview
The OpenSwitch Check_MK Agent is based on the [Check_MK Agent] [1].  It is enabled by default in the OpenSwitch distribution, and does not have any associated CLI commands (to enable/disable).

The Check_MK agent listens on TCP port 6556 for data collection queries. To quickly test if the Check_MK agent is working, telnet to the OpenSwitch node with port 6556: 

    server> telnet openswitch 6556
    Trying 10.0.0.1...
	Connected to openswitch.
	Escape character is '^]'.
	<<<check_mk>>>
	Version: 1.1.8
	AgentOS: linux
	<<<df>>>
	/dev/sda1     ext3     1008888    223832    733808      24% /
		/dev/sdc1     ext3     1032088    284648    695012    30% /lib/modules
	<<<ps>>>
	init [3]
	/sbin/syslogd
	/sbin/klogd -x
	/usr/sbin/cron
	/sbin/getty 38400 tty2

For test purposes, the Check_MK agent can be executed from the shell on an OpenSwitch node:

	openswitch> /usr/bin/checkmk-agent

Both telnet output (shown above) and shell output should be identical.

##Configuration
The Check_MK agent is invoked by systemd via socket activation. The OpenSwitch Check_MK agent contains two preconfigured standard [systemd][2] socket service activation files, `checkmk-agent@.service` and `checkmk-agent.socket`. These OpenSwitch Check MK agent activation files can be changed for site-specific customization of the Check_MK Linux agent.


##Extending the Check_MK Agent
The open source Linux Check_MK Agent is modified in OpenSwitch to report additional information specific to OpenSwitch. For example, interface statistics are fetched from the OVSDB.

Check_MK reporting can be extended by adding check scripts in the `/usr/lib/check_mk_agent/local` directory. See the [Check_MK documentation][3] for more details.
[1]: https://mathias-kettner.de/checkmk_linuxagent.html
[2]: http://www.freedesktop.org/software/systemd/man/systemd.socket.html
[3]: https://mathias-kettner.de/checkmk_localchecks.html
