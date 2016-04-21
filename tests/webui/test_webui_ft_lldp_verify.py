#!/usr/bin/env python

# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
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
import json
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *
from webui import *

MGMT_PATTERN_IP4 = "192.168.1.1"
MGMT_PATTERN_IP6 = "fd12:3456:789a:1::"

MGMT_INTF_IP4_MASK = "24"
MGMT_INTF_IP6_MASK = "64"

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02 wrkston01",
            "topoLinks": "lnk01:dut01:dut02,\
                          lnk02:dut01:wrkston01",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston01:docker-image:host/freeradius-ubuntu",
            "topoLinkFilter": "lnk02:dut01:interface:eth0"}

switchMgmtAddr1 = "10.10.10.2"
switchMgmtAddr2 = "10.10.10.3"
restClientAddr = "10.10.10.4"
broadcast = "10.10.10.255"
netmask = "255.255.255.0"
subnetMaskBits = 24


def configRestEnvironment(dut01, dut02, wrkston01):
    # Configuring REST environment
    global switchMgmtAddr1
    global switchMgmtAddr2
    global restClientAddr

    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface="mgmt",
                                  addr=switchMgmtAddr1,
                                  mask=subnetMaskBits,
                                  config=True)
    assert retStruct.returnCode() == 0, 'Failed to configure IP on switchport'
    info('### Successfully configured ip on switch1 port ###\n')
    cmdOut = dut01.cmdVtysh(command="show run")
    info('### Running config of the switch1:\n' + cmdOut + ' ###\n')

    retStruct = InterfaceIpConfig(deviceObj=dut02,
                                  interface="mgmt",
                                  addr=switchMgmtAddr2,
                                  mask=subnetMaskBits,
                                  config=True)
    assert retStruct.returnCode() == 0, 'Failed to configure IP on switchport'
    info('### Successfully configured ip on switch2 port ###\n')
    cmdOut = dut02.cmdVtysh(command="show run")
    info('### Running config of the switch2:\n' + cmdOut + ' ###\n')

    info('### Configuring workstations ###\n')
    retStruct = wrkston01.NetworkConfig(
                                ipAddr=restClientAddr,
                                netMask=netmask,
                                broadcast=broadcast,
                                interface=wrkston01.linkPortMapping['lnk02'],
                                config=True)

    assert retStruct.returnCode() == 0, 'Failed to configure IP on workstation'
    info('### Successfully configured IP on workstation ###\n')
    cmdOut = wrkston01.cmd("ifconfig " + wrkston01.linkPortMapping['lnk02'])
    info('### Ifconfig info for workstation 1:\n' + cmdOut + '###\n')

    retStruct = GetLinuxInterfaceIp(deviceObj=wrkston01)
    assert retStruct.returnCode() == 0, 'Failed to get linux interface ip on\
      switch'
    info("### Successful in getting linux interface "
         "ip on the workstation ###\n")

    retStruct = returnStruct(returnCode=0)
    return retStruct


def deviceCleanup(dut01, dut02, wrkston01):
    retStruct = wrkston01.NetworkConfig(
                                ipAddr=restClientAddr,
                                netMask=netmask,
                                broadcast=broadcast,
                                interface=wrkston01.linkPortMapping['lnk02'],
                                config=False)
    assert retStruct.returnCode() == 0, 'Failed to unconfigure IP address on\
     workstation 1'
    info('### Successfully unconfigured ip on Workstation 1 ###\n')
    cmdOut = wrkston01.cmd("ifconfig " + wrkston01.linkPortMapping['lnk02'])
    info('### Ifconfig info for workstation 1:\n' + cmdOut + ' ###')

    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface="mgmt",
                                  addr=switchMgmtAddr1,
                                  mask=subnetMaskBits,
                                  config=False)
    assert retStruct.returnCode() == 0, 'Failed to unconfigure IP address on\
     dut01 port'
    info('### Unconfigured IP address on dut01 port " ###\n')
    cmdOut = dut01.cmdVtysh(command="show run")
    info('Running config of the switch:\n' + cmdOut)
    retStruct = returnStruct(returnCode=0)
    return retStruct


def restTestLldpInterfaces(wrkston01):
    global switchMgmtAddr2

    retStruct = wrkston01.RestCmd(switch_ip=switchMgmtAddr1,
                                  url="/rest/v1/system/interfaces/1",
                                  method="GET")
    assert retStruct.returnCode() == 0, \
        'Failed to execute rest cmd "GET for url=/rest/v1/system/interfaces"'
    info('### Success in executing the rest command \
     "GET for url=/rest/v1/system/interfaces/1" ###\n')
    info('http return code' + retStruct.data['http_retcode'])
    assert retStruct.data[
        'http_retcode'].find('200') != -1, 'Rest GET interfaces Failed\n' +\
        retStruct.data['response_body']
    info('### Success in Rest GET interfaces ###\n')
    info('###' + retStruct.data['response_body'] + '###\n')

    # TEST 1 - Check to see if LLDP NEIGHBOR INFO TAG IS PRESENT
    assert retStruct.data[
        "response_body"].find('lldp_neighbor_info') != -1, 'Failed in checking the \
         GET METHOD JSON response validation for lldp_neighbor_info tag'
    info('### Success in Rest GET for lldp_neighbor_info tag ###\n')
    rspDict = json.loads(retStruct.data["response_body"])

    # TEST 2 - Check to see if LLDP NEIGHBOR INFO - IP MGMT TAG IS PRESENT
    assert retStruct.data[
        "response_body"].find('mgmt_ip_list') != -1, 'Failed in checking the \
         GET METHOD JSON response validation for mgmt_ip_list tag'
    info('### Success in Rest GET for mgmt_ip_list tag ###\n')

    # TEST 3 - Check to see if NEIGHBOR INFO - IP MGMT TAG MATCHES EXP VALUE
    try:
        lldp_ip = rspDict["status"]["lldp_neighbor_info"]["mgmt_ip_list"]
    except ValueError:
        info('### Value error in Rest GET for mgmt_ip_list ###\n')
    assert lldp_ip == switchMgmtAddr2, 'Failed in checking the GET \
          METHOD JSON response validation for mgmt_ip_list value'
    info('### Success in Rest GET for mgmt_ip_list value = expected ###\n')

    # TEST 4 - Check to see if LLDP STATISTICS TAG IS PRESENT
    assert retStruct.data[
        "response_body"].find('lldp_statistics') != -1, 'Failed in checking \
         the GET METHOD JSON response validation for lldp_statistics tag'
    info('### Success in Rest GET for lldp_statistics tag ###\n')

    # TEST 5 - Check to see if LLDP STATISTICS TAG FOR XMIT IS PRESENT
    assert retStruct.data[
        "response_body"].find('lldp_tx') != -1, 'Failed\
        in checking the GET METHOD JSON response validation for lldp_tx tag'
    info('### Success in Rest GET for lldp_tx tag ###\n')

    # TEST 6 - Check to see if LLDP STATISTICS TAG FOR XMIT IS > 0
    try:
        lldp_tx = int(rspDict["statistics"]["lldp_statistics"]["lldp_tx"])
    except ValueError:
        info('### Value error in Rest GET for lldp_tx ###\n')
    assert lldp_tx != 0, 'Failed in checking the GET METHOD JSON \
                          response validation for lldp_tx value = 0'
    info('### Success in Rest GET - lldp_tx value > 0 ###\n')

    # TEST 7 - Check to see if LLDP STATISTICS TAG FOR RCV IS PRESENT
    assert retStruct.data[
        "response_body"].find('lldp_rx') != -1, 'Failed\
          in checking the GET METHOD JSON response validation for lldp_rx tag'
    info('### Success in Rest GET for lldp_rx tag ###\n')

    # TEST 8 - Check to see if LLDP STATISTICS TAG FOR RCV > 0
    try:
        lldp_rx = int(rspDict["statistics"]["lldp_statistics"]["lldp_rx"])
    except ValueError:
        info('### Value error in Rest GET for lldp_rx ###\n')
    assert lldp_rx != 0, 'Failed in checking the GET \
          METHOD JSON response validation for lldp_rx value = 0'
    info('### Success in Rest GET - lldp_rx value > 0 ###\n')

    retStruct = returnStruct(returnCode=0)
    return retStruct


def setupLldp(**kwargs):
    device1 = kwargs.get('device1', None)
    device2 = kwargs.get('device2', None)

    device1.commandErrorCheck = 0
    device2.commandErrorCheck = 0
    info('\n\n\nConfig lldp on SW1 and SW2')

    info('\nEnabling lldp feature on SW1')
    devIntRetStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = devIntRetStruct.returnCode()
    assert retCode == 0, "\nFailed to enable lldp feature"

    info('\nEnabling lldp feature on SW2')
    devIntRetstruct = LldpConfig(deviceObj=device2, enable=True)
    assert retCode == 0, "\nFailed to enable lldp feature"

    # Entering interface SW1
    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "\nFailed to enable interface"

    # Configuring no routing on interface
    # Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    # Entering interface
    info('Switch 1 interface is :' +
         str(device1.linkPortMapping['lnk01']))
    devIntRetStruct = \
        device1.DeviceInteract(command="interface " +
                               str(device1.linkPortMapping['lnk01']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"

    devIntRetStruct = device1.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to disable routing"

    # Exiting interface
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    # Exiting Config terminal
    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"
    # End configure no routing switch 1 port over lnk01

    # Entering interface SW2
    retStruct = InterfaceEnable(deviceObj=device2, enable=True,
                                interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enable interface"

    # Configuring no routing on interface
    # Entering VTYSH terminal
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device2.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    # Entering interface
    info('Switch 2 interface is :' +
         str(device2.linkPortMapping['lnk01']))
    devIntRetStruct = \
        device2.DeviceInteract(command="interface " +
                               str(device2.linkPortMapping['lnk01']))

    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"

    devIntRetStruct = device2.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to disable routing"

    # Exiting interface
    devIntRetStruct = device2.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    # Exiting Config terminal
    retStruct = device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"
    # End configure no routing on switch 2 port over lnk01

    # Waiting for initial LLDP message exchange
    time.sleep(30)

    # Dump out LLDP neighbor info via CLI to compare to REST later
    retStruct = ShowLldpNeighborInfo(deviceObj=device1,
                                     port=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to show neighbour info"

    info('CLI_Switch1 Output\n' + str(retStruct.buffer()))
    info('CLI_Switch1 Return Structure')
    retStruct.printValueString()

@pytest.mark.skipif(True, reason="waiting for desicion when Modular ft comes out")
@pytest.mark.timeout(1000)
class Test_lldp_configuration:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_lldp_configuration.testObj = \
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        # Get topology object
        Test_lldp_configuration.topoObj = \
            Test_lldp_configuration.testObj.topoObjGet()
        wrkston01Obj = Test_lldp_configuration.topoObj.deviceObjGet(
            device="wrkston01")
        wrkston01Obj.CreateRestEnviron()

    def teardown_class(cls):
        Test_lldp_configuration.topoObj.terminate_nodes()

    def test_setup_lldp_env(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        setupLldp(device1=dut01Obj, device2=dut02Obj)

    def test_config_rest_environment(self):
        info('#######################################################\n')
        info('######        Configure REST environment           ####\n')
        info('#######################################################\n')
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retStruct = configRestEnvironment(dut01Obj, dut02Obj, wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to config REST environment'
        info('### Successful in config REST environment test ###\n')

    def test_rest_lldp_interfaces(self):
        info('#######################################################\n')
        info('######   Testing REST Interfaces basic functionality   ####\n')
        info('#######################################################\n')
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retStruct = restTestLldpInterfaces(wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to test rest Interfaces'
        info('### Successful in test rest Interfaces ###\n')

    def test_clean_up_devices(self):
        info('#######################################################\n')
        info('######    Device Cleanup - rolling back config     ####\n')
        info('#######################################################\n')
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retStruct = deviceCleanup(dut01Obj, dut02Obj, wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to cleanup device'
        info('### Successfully Cleaned up devices ###\n')
