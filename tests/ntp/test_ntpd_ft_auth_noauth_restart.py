
#Copyright (C) 2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.



import pytest
import re
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *
import pprint

#NTP server IPs
global WORKSTATION_IP_ADDR_SER1
global WORKSTATION_IP_ADDR_SER2
global SERVER_UNREACHABLE


# Topology definition
topoDict = {"topoType" : "virtual",
            "topoExecution": 3000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston01:docker-image:openswitch/centos_ntp,\
                            wrkston02:system-category:workstation,\
                            wrkston02:docker-image:openswitch/centos_ntp",
            "topoLinkFilter": "lnk01:dut01:interface:1,lnk02:dut01:interface:2"}

#configure the switch and the workstations
def switchWsConfig(dut01, wrkston01, wrkston02):
    global WORKSTATION_IP_ADDR_SER1
    global WORKSTATION_IP_ADDR_SER2
    global SERVER_UNREACHABLE
    info('\n### Configuring workstation 1 as a local NTP server with authentication###\n')
    info('### Configuring workstation 2 as a local NTP server without authentication###\n')
    sleep(10)
    wrkston01.cmd("echo \"authenticate yes\" >> /etc/ntp.conf")
    wrkston01.cmd("ntpd -c /etc/ntp.conf")
    wrkston02.cmd("ntpd -c /etc/ntp.conf")
    sleep(10)
    out = wrkston01.cmd("ntpq -p -n")
    info("\nworkstation1 --> \n%s\n"%(pprint.pformat(out)))
    #check if the public NTP server is reachable fot the local NTP server
    if ".INIT." in out or "Connection refused" in out:
        SERVER_UNREACHABLE = True
    else:
        SERVER_UNREACHABLE = False
    #retrieve the IP address of the workstation 1
    ifConfigCmdOut = wrkston01.cmd("ifconfig eth0")
    lines = ifConfigCmdOut.split('\n')
    target = 'inet'
    for line in lines:
        word = line.split()
        for i,w in enumerate(word):
            if w == target:
               WORKSTATION_IP_ADDR_SER1 = word[i+1]
               break
    info("### Workstation 1 IP address: %s\n" % WORKSTATION_IP_ADDR_SER1)
    #retrieve the IP address of the workstation 2
    ifConfigCmdOut = wrkston02.cmd("ifconfig eth0")
    lines = ifConfigCmdOut.split('\n')
    target = 'inet'
    for line in lines:
        word = line.split()
        for i,w in enumerate(word):
            if w == target:
               WORKSTATION_IP_ADDR_SER2 = word[i+1]
               break
    out = wrkston02.cmd("ntpq -p -n")
    info("\nworkstation2 --> \n%s\n"%(pprint.pformat(out)))
    if SERVER_UNREACHABLE == False:
        if ".INIT." in out or "Connection refused" in out:
            SERVER_UNREACHABLE = True
        else:
            SERVER_UNREACHABLE = False
    info("### Workstation 2 IP address: %s\n" % WORKSTATION_IP_ADDR_SER2)
    devIntReturn = dut01.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter bash shell"
    info("### Configuring NTP servers on the Switch###\n")
    dut01.cmdVtysh(command="vtysh")
    dut01.cmdVtysh(command="configure terminal")
    dut01.cmdVtysh(command="ntp authentication-key 55 md5 secretpassword")
    dut01.cmdVtysh(command="ntp trusted-key 55")
    dut01.cmdVtysh(command="ntp authentication enable")
    dut01.cmdVtysh(command="ntp server %s key 55" % WORKSTATION_IP_ADDR_SER1)
    dut01.cmdVtysh(command="ntp server %s prefer " % WORKSTATION_IP_ADDR_SER2)

#function to verify if the NTP servers are associated with the switch without any error
def validateNtpAssociationInfo(dut01, wrkston01, wrkston02):
    global WORKSTATION_IP_ADDR_SER1
    global WORKSTATION_IP_ADDR_SER2
    out = dut01.cmdVtysh(command="do show ntp associations")
    lines = out.split('\n')
    for line in lines:
        if WORKSTATION_IP_ADDR_SER1 in line:
           assert ('.NKEY.' or '.TIME.' or '.RATE.' or '.AUTH.') not in line,\
               "### NTP client has incorrect information###\n"
        if WORKSTATION_IP_ADDR_SER2 in line:
           assert ('.NKEY.' or '.TIME.' or '.RATE.' or '.AUTH.') not in line,\
               "### NTP client has incorrect information###\n"
    return True

#function to validate if time on the switch is synchronized with preferred NTP server
def validateNtpStatus(dut01, wrkston01, wrkston02):
    global WORKSTATION_IP_ADDR_SER2
    out = dut01.cmdVtysh(command="do show ntp status")
    if 'Synchronized' in out:
        return True
    return False

#function to restart the NTPD daemon on the switch
def restartNTPDaemon(dut01, wrkston01, wrkston02):
    info("\n### Verifying the NTPD restartability ###\n")
    dut01.cmdVtysh(command="exit")
    dut01.cmdVtysh(command="exit")
    dut01.DeviceInteract(command="systemctl restart ops-ntpd")
    sleep(30)
    out = dut01.DeviceInteract(command="ps -ef | grep ntpd")
    info("\ndut01 'restart ops-ntpd' --> \n%s\n"%(pprint.pformat(out)))
    if 'ntpd -c' in out['buffer']:
        info("### OPS-NTPD Daemon restart successful ###\n")
    else:
        error("### OPS-NTPD Daemon restart FAILED ###\n")
    dut01.DeviceInteract(command="vtysh")
    dut01.DeviceInteract(command="configure terminal")

#function to check that local NTP servers are configured and time on the switch is synchronized
def chkNTPAssociationandStatus(dut01, wrkston01, wrkston02):
    global SERVER_UNREACHABLE
    info("\n### Checking NTP associations and NTP status ###\n")
    total_timeout = 600
    timeout = 10
    check1 = False
    check2 = False
    for t in range(0, total_timeout, timeout):
        sleep(5)
        if check1 == False:
            check1 = validateNtpAssociationInfo(dut01, wrkston01, wrkston02)
        if check2 == False:
            check2 = validateNtpStatus(dut01, wrkston01, wrkston02)
        if check1 == True and check2 == True:
            return True
    if SERVER_UNREACHABLE == True:
        info("\n### Local NTP server could not reach Public NTP server###\n")
        out = dut01.cmdVtysh(command="do show ntp status")
        info("\ndut01 'do show ntp status' --> \n%s\n"%(pprint.pformat(out)))
        out = dut01.cmdVtysh(command="do show ntp associations")
        info("\ndut01 'do show ntp associations' --> \n%s\n"%(pprint.pformat(out)))
        out = wrkston01.cmd("ntpq -p -n")
        info("\nworkstation1 --> \n%s\n"%(pprint.pformat(out)))
        out = wrkston02.cmd("ntpq -p -n")
        info("\nworkstation2 --> \n%s\n"%(pprint.pformat(out)))
        return True
    info("\nTimeout occured, test FAIL\n")
    out = dut01.cmdVtysh(command="do show ntp status")
    info("\ndut01 'do show ntp status' --> \n%s\n"%(pprint.pformat(out)))
    out = dut01.cmdVtysh(command="do show ntp associations")
    info("\ndut01 'do show ntp associations' --> \n%s\n"%(pprint.pformat(out)))
    out = wrkston01.cmd("ntpq -p -n")
    info("\nworkstation1 --> \n%s\n"%(pprint.pformat(out)))
    out = wrkston02.cmd("ntpq -p -n")
    info("\nworkstation2 --> \n%s\n"%(pprint.pformat(out)))
    error("\n### Timeout occured, NTP config failed###\n")
    return False

#timeout increased to provide enough time to download the images from docker hub
@pytest.mark.timeout(2400)
class TestNtpClientConfig:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        TestNtpClientConfig.testObj =\
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        #Get topology object
        TestNtpClientConfig.topoObj = \
            TestNtpClientConfig.testObj.topoObjGet()

    def teardown_class(cls):
        TestNtpClientConfig.topoObj.terminate_nodes()

    def testNtpAuthNoauthFunctionality(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        switchWsConfig(dut01Obj, wrkston01Obj, wrkston02Obj)
        status = chkNTPAssociationandStatus(dut01Obj, wrkston01Obj, wrkston02Obj)
        assert status == True, \
            "\n### NTP associations and status verification failed ###\n"
        info("\n### NTP associations and status is verified ###\n")

    def testNTPRestartability(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        restartNTPDaemon(dut01Obj, wrkston01Obj, wrkston02Obj)
        status = chkNTPAssociationandStatus(dut01Obj, wrkston01Obj, wrkston02Obj)
        assert status == True, \
            "\n### NTP associations and status verification failed after restarting OPS-NTPD daemon ###\n"
        info("\n### OPS-NTPD daemon restartability test verified###\n")
