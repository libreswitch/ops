#!/usr/bin/env python

# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
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
from  opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch"}

def lldp_debug_dump(device1, device2):
    # Dump Device1
    LogOutput('info', "Device1 DUMP:")
    device1.setDefaultContext(context="linux")
    devCmd = "ovs-vsctl list interface "\
        + str(device1.linkPortMapping['lnk01'])
    neighbor_output = device1.cmd(devCmd)
    opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                        + str(neighbor_output))
    devCmd = "ip netns exec swns ifconfig "\
        + str(device1.linkPortMapping['lnk01'])
    ifconfig_output = device1.cmd(devCmd)
    opstestfw.LogOutput('info', devCmd + " output\n"
                        + str(ifconfig_output))

    # Dump Device2
    LogOutput('info', "\nDevice2 DUMP")
    device2.setDefaultContext(context="linux")
    devCmd = "ovs-vsctl list interface "\
        + str(device2.linkPortMapping['lnk01'])
    neighbor_output = device2.cmd(devCmd)
    opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                        + str(neighbor_output))
    devCmd = "ip netns exec swns ifconfig "\
        + str(device2.linkPortMapping['lnk01'])
    ifconfig_output = device2.cmd(devCmd)
    opstestfw.LogOutput('info', devCmd + " output\n"
                        + str(ifconfig_output))


def lldp_enable_disable(**kwargs):
    device1 = kwargs.get('device1', None)
    device2 = kwargs.get('device2', None)

    ######## Configuration Start ##########
    # Enabling interface 1 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enabling interface on SW1"

    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    LogOutput('info', "\n\n\nConfig SW1 LLDP timer to 5 sec")
    devIntRetStruct = device1.DeviceInteract(command="lldp timer 5\r")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set SW1 LLDP timer 5 seconds"

    # Entering interface
    LogOutput('info', "Switch 1 interface is :"
              + str(device1.linkPortMapping['lnk01']))
    devIntRetStruct =\
        device1.DeviceInteract(command="interface "
                               + str(device1.linkPortMapping['lnk01']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"

    devIntRetStruct = device1.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to disable routing"

    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"
    # End section to disable routing on the port

    # Enabling interface 1 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True,
                                interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enable interface on SW2"

    # Section to disable routing on port
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device2.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    LogOutput('info', "\n\n\nConfig SW2 LLDP to 5 sec")
    devIntRetStruct = device2.DeviceInteract(command="lldp timer 5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set LLDP timer 5 seconds"

    # Entering interface 1
    LogOutput('info', "Switch 2 interface is : "
              + str(device2.linkPortMapping['lnk01']))
    devIntRetStruct =\
        device2.DeviceInteract(command="interface "
                               + str(device2.linkPortMapping['lnk01']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"

    devIntRetStruct = device2.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to disable routing"

    devIntRetStruct = device2.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    retStruct = device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Configuring lldp on SW1
    LogOutput('info', "\n\n\nConfig lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to configure LLDP on SW1"

    # Configuring lldp on SW2
    LogOutput('info', "\n\n\nConfig lldp on SW2")
    retStruct = LldpConfig(deviceObj=device2, enable=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Configure lldp on SW2"


    retStruct = device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"
    # End section of disable routing on a port
    # Waiting for neighbour entry to flood
    Sleep(seconds=5, message="\nWaiting")

    # Set my default context to linux temporarily
    device1.setDefaultContext(context="linux")

    # Verify neighbour info on SW1
    neighbor_found = False
    for retry in range(1, 5):
        # Parsing neighbour info for SW1
        LogOutput('info', "\nShowing LLDP neighbour on SW1")
        Sleep(seconds=5, message="Delay")
        retStruct = ShowLldpNeighborInfo(deviceObj=device1,
                                         port=device1.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        LogOutput('info', "CLI_Switch1 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch1 Return Structure")
        retStruct.printValueString()
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbour Port ID: "
                  + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
        neiPortId = str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()
        if neiPortId.isdigit() is True or re.match(r'\d{1,2}-\d{1}',neiPortId):
            break
        else:
            device1.setDefaultContext(context="linux")
            # Dump out the ovs-vsctl interface information
            LogOutput('info', "Didn't receive integer value for "
                      "Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device1.linkPortMapping['lnk01'])
            neighbor_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device1.linkPortMapping['lnk01'])
            ifconfig_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    # end loop
    # Set my default context to linux temporarily
    device1.setDefaultContext(context="vtyShell")
    assert str((lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()) == str(device2.linkPortMapping['lnk01']), "Case Failed, No Neighbor present for SW1"
    if (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info', "\nCase Passed, Neighbour established by SW1")
        LogOutput('info', "\nPort of SW1 neighbour is :"
                  + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']))
        LogOutput('info', "\nChassie Capabilities available : "
                  + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "
                  + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']))

    # Verify neighbour info on SW2
    neighbor_found = False
    device2.setDefaultContext(context="linux")
    for retry in range(1, 5):
        LogOutput('info', "\nShowing LLDP neighbour SW2")
        Sleep(seconds=5, message="Delay")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                         port=device2.linkPortMapping['lnk01'])

        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbour Port ID: "
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
        neiPortId = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()
        if (((lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()) == device1.linkPortMapping['lnk01']):
            neighbor_found = True

        if neiPortId.isdigit() is True or re.match(r'\d{1,2}-\d{1}',neiPortId):
            break

    if neighbor_found is False:
        # Dump out the ovs-vsctl interface information
        LogOutput('info', "\n ####### LLDP DUMP START ##############")
        lldp_debug_dump(device1, device2)
        LogOutput('info', "\n ####### LLDP DUMP END ##############")
        assert 0, "Case Failed, No Neighbour present for SW2"

    device2.setDefaultContext(context="vtyShell")
    assert str((lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()) == str(device1.linkPortMapping['lnk01']), "Case Failed, No Neighbor present for SW2"
    if (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info', "\nCase Passed, Neighbour established by SW2")
        LogOutput('info', "\nPort of SW2 neighbour is :"
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']))
        LogOutput('info', "\nChassie Capabilities available : "
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']))


    LogOutput('info', "\nDisabling lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to disable interface"

    LogOutput('info', "\nDisabling LLDP on SW2")
    retStruct = LldpConfig(deviceObj=device2, enable=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to disable interface"

    # Verify neighbour cleared on SW1
    device1.setDefaultContext(context="linux")
    neighbor_cleared = False
    for retry in range(1, 3):
        LogOutput('info', "\nShowing Lldp neighbour on SW1")
        Sleep(seconds=5, message="\nWaiting")
        retStruct = ShowLldpNeighborInfo(deviceObj=device1,
                                         port=device1.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        LogOutput('info', "CLI_Switch1 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch1 Return Structure")
        retStruct.printValueString()

        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbour Port ID: "
                  + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())

        if str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip() == "":
            neighbor_cleared = True
            break


    if neighbor_cleared is False:
        if (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']):
            LogOutput('info', "\n ####### LLDP DUMP START ##############")
            lldp_debug_dump(device1, device2)
            LogOutput('info', "\n ####### LLDP DUMP END ##############")
            assert False, "Case Failed, Neighbour Still present on SW1"
    else:
        LogOutput('info', "\nCase Passed, No Neighbour is present for SW1")

    # Verify neighbour cleared on SW2
    device2.setDefaultContext(context="linux")
    neighbor_cleared = False
    for retry in range(1, 3):
        LogOutput('info', "\nShowing LLDP neighbour on SW2")
        Sleep(seconds=5, message="\nWaiting")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "\nFailed to show neighbour info"
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()
        LogOutput('info', "\nExpected Neighbour Port ID: "
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())

        if str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip() == "":
            neighbor_cleared = True
            break


    device2.setDefaultContext(context="vtyShell")
    if neighbor_cleared is False:
        if (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']):
            LogOutput('info', "\n ####### LLDP DUMP START ##############")
            lldp_debug_dump(device1, device2)
            LogOutput('info', "\n ####### LLDP DUMP END ##############")
            assert False, "Case Failed, Neighbour present for SW2"
    else:
        LogOutput('info', "Case Passed, No Neighbour is present for SW2")

    # Down the interfaces
    LogOutput('info', "Disabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=False,
                                interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to disable interface"

    LogOutput('info', "Disabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=False,
                                interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to disable interface"


@pytest.mark.timeout(1000)
class Test_lldp_configuration:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_lldp_configuration.testObj =\
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        #    Get topology object
        Test_lldp_configuration.topoObj = \
            Test_lldp_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_lldp_configuration.topoObj.terminate_nodes()

    def test_lldp_enable_disable(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        lldp_enable_disable(device1=dut01Obj, device2=dut02Obj)
