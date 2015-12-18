Checkmk Agent Test Cases
========================

## Contents

- [Test with Open Monitoring Daemon](#test-with-open-monitoring-daemon)
	- [Objective](#objective)
	- [Requirements](#requirements)
	- [Setup](#setup)
		- [Topology diagram](#topology-diagram)
		- [Test Setup](#test-setup)
	- [Test result criteria](#test-result-criteria)
		- [Test pass criteria](#test-pass-criteria)
		- [Test fail criteria](#test-fail-criteria)

##  Test with Open Monitoring Daemon
### Objective
The test case uses the Open Monitoring Daemon (OMD) to connect to OpenSwitch
and view system statistics.

### Requirements

A physical or virtual OpenSwitch Device Under Test (DUT), and a docker container running Open Monitoring Daemon (OMD) software.

### Setup
#### Topology diagram

```ditaa
    +----------------+         +----------------+
    |                |         |                |
    |                |         |                |
    |      OMD       +---------+     Switch     |
    |                |         |                |
    |                |         |                |
    +----------------+         +----------------+
```

#### Test Setup
**Switch** is connected to OMD via Interface 1:

```
!
interface 1
    no shutdown
    ip address 9.0.0.1/8
!
```

**OMD** is configured as follows:

1. Start the OMD docker image openswitch/omd which is hosted on dockerhub.
2. Ping the OpenSwitch DUT to ensure it is reachable from OMD.
3. Login to the OMD dashboard at http://<OMD server IP>/default/check_mk/.
4. Add the OpenSwitch DUT IP (9.0.0.1) for monitoring.

### Test result criteria

Verify that the Openswitch DUT system statistics are reported in the OMD dashboard.
 
#### Test pass criteria
The OMD dashboard reports system statistics of the monitored OpenSwitch DUT.

#### Test fail criteria
The test case is considered failing if:

- OMD is not able to connect to or discover the OpenSwitch DUT.
- The system statistics of the OpenSwitch DUT are not reported in the OMD dashboard.
- The system statistics are not updated periodically in the OMD dashboard.
