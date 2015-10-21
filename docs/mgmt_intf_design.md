#High level design of management interface

The primary goal of the management module is to facilitate the management of the device. It provides the following:

- Device access and configuration

- Event collection for monitoring, analysis, and correlation

- Device and user authentication, authorization, and accounting

- Device time synchronization

- Device image downloading

The device is configured or monitored through the management interface. All management traffic such as device ssh, tftp and so on, goes through the management interface.

##References

* [Management Interface Design Document - TBL](/docs/mgmt-intf)
* [Management Interface User guide - TBL](/docs/mgmt-intf)
