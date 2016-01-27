
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

SERVER1 = "198.55.111.50"
SERVER2 = "17.253.38.253"
global WORKSTATION_IP_ADDR

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01",
            "topoLinks": "lnk01:dut01:wrkston01",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston01:docker-image:openswitch/centos_ntp",
            "topoLinkFilter": "lnk01:dut01:interface:eth0"}

def switchWsConfig(dut01, wrkston01):
    global WORKSTATION_IP_ADDR
    info('### Configuring workstation ###\n')
    wrkston01.cmd("ntpd -c /etc/ntp.conf")
    ifConfigCmdOut = wrkston01.cmd("ifconfig eth0")
    lines = ifConfigCmdOut.split('\n')
    target = 'inet'
    for line in lines:
        word = line.split()
        for i,w in enumerate(word):
            if w == target:
               WORKSTATION_IP_ADDR = word[i+1]
               break
    devIntReturn = dut01.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter bash shell"
    info("\n###Configuring Switch###\n")
    dut01.cmdVtysh(command="vtysh")
    dut01.cmdVtysh(command="configure terminal")
    dut01.cmdVtysh(command="ntp server %s version 4" % SERVER1)
    dut01.cmdVtysh(command="ntp server %s " % SERVER2)
    dut01.cmdVtysh(command="ntp server %s prefer" % WORKSTATION_IP_ADDR)

def validateFunctionality(dut01, wrkston01):
    global WORKSTATION_IP_ADDR
    dut01.cmdVtysh(command="do show ntp authentication-keys")
    dut01.cmdVtysh(command="do show ntp status")
    sleep(5)
    out = dut01.cmdVtysh(command="do show ntp associations")
    print(out)
    lines = out.split('\n')
    for line in lines:
        if WORKSTATION_IP_ADDR in line:
           if ('.NKEY.' or '.INIT.' or '.TIME.' or '.RATE.' or '.AUTH.') in line:
              return False
    return True

class Test_Ntpserver_Feature:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_Ntpserver_Feature.testObj =\
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        #    Get topology object
        Test_Ntpserver_Feature.topoObj = \
            Test_Ntpserver_Feature.testObj.topoObjGet()

    def teardown_class(cls):
        Test_Ntpserver_Feature.topoObj.terminate_nodes()

    def test_feature(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        switchWsConfig(dut01Obj, wrkston01Obj)
        for t in range(0,120,10):
            sleep(5)
            status = validateFunctionality(dut01Obj, wrkston01Obj)
            if status == True:
                info("\n###NTP Functionality is working###\n")
                return
        error("\n###Timeout occured, NTP config failed###\n")
