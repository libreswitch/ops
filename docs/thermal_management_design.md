High level design of Thermal Management
=======================================
There are two components to thermal management in OpenSwitch: the temperature sensor daemon, and the fan daemon.

The temperature sensor daemon reads the state of system thermal sensors and compares the readings to vendor-specified thresholds for status and fan levels.

The fan daemon reads the fan level values determined by the temperature sensor daemon and sets the fan speed to an appropriate value. The fan daemon also reads the RPM information from fans and reports the information so you can verify that the fans are operating properly.

Design choices
--------------
The temperature sensor and fan daemons could have been unified into one daemon. However, the simplicity of the two-daemon architecture simplified the design and implementation.

In addition, the temerature sensor daemon does not attempt to read the temperature of processor or switch chip sensors.

Participating modules
---------------------
```ditaa
  +--------+
  |database|
  +-^-----^+
    |     |
    |     |
+-----+  +----+
|tempd|  |fand|
+-----+  +----+
   |      |
   |      |
+--v------v-+
|config_yaml|
+-----------+
   |       |
   |       |
 +-v-+  +--v----+
 |i2c|  |hw desc|
 +---+  +-------+
```
Both tempd and fand periodically poll the hardware to determine presence and status of the fans and sensors (through i2c operations) that were discovered by reading the YAML hardware description files through config\_yaml. When either of them detect a change, they calculate any new state information and update the database. The temperature daemon is responsible for calculating the alarm state and fan speed setting for each sensor. The fan daemon is responsible for reading the reported fan speed setting for each sensor and determining the worst-case sensor value and setting the fan speeds based on that value.

The user is allowed to override the fan speed calculated by the fan daemon, so that the fans can be set to low speed (for example), to reduce fan noise. However, if the worst-case fan speed setting calculated by the temperature daemon would result in the fan speed being set to the maximum speed, the fan daemon ignores the fan speed override set by the user and instructs the fans to go to full speed. This is to prevent thermal damage if the cooling at the fan speed set by the user is inadequate. The fan speed override (other\_config:fan\_speed\_override row in Subsystem table) can be set to one of `slow`, `normal`, `medium`, `fast`, or `max`. If the setting is not specified, the speed calculated by the fan daemon from the worst-case temperature sensor value is used to set the fan speed.

OVSDB-Schema
------------
The fan and temperature daemons populate and use data in the Subsystem, Fan, and Temp\_sensor tables. The Subsystem table has references for all of the Fans and Temp\_sensors that are provided by the Subystem table, as well as the fan speed override (other\_config:fan\_speed\_override).
