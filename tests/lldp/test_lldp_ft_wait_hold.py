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
            "topoFilters": "dut01:system-category:switch,dut02:system-category:switch"}

def lldp_wait_hold(**kwargs):
    device1 = kwargs.get('device1',None)
    device2 = kwargs.get('device2',None)

    device1.commandErrorCheck = 0
    device2.commandErrorCheck = 0
    LogOutput('info', "\n\n\nConfig lldp on SW1 and SW2")
    #Entering vtysh SW1


    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    LogOutput('info', "\nConfiguring hold for 2 sec on SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp holdtime 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to set holdtime"

    LogOutput('info', "\nConfiguring transmit time for 5 sec on SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp timer 5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to set transmit time"


    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to get vtysh prompt"

    #Entering config terminal SW2
    devIntRetStruct = device2.ConfigVtyShell(enter=True)
    retCode = devIntRetStruct.returnCode()
    assert retCode==0, "\nFailed to enter config mode"


    LogOutput('info', "\nConfiguring hold for 2 sec on SW2")
    devIntRetStruct = device2.DeviceInteract(command="lldp holdtime 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0,"\nFailed to configure hold time"

    LogOutput('info', "\nConfiguring transmit time for 5 sec on SW2")
    devIntRetStruct = device2.DeviceInteract(command="lldp timer 5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "\nFailed to configure transmit time"

    retStruct= device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    retStruct=device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    retStruct=device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"

    retStruct=device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"


    LogOutput('info', "\nEnabling lldp feature on SW1")
    devIntRetStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = devIntRetStruct.returnCode()
    assert retCode==0, "\nFailed to enable lldp feature"

    LogOutput('info', "\nEnabling lldp feature on SW2")
    devIntRetstruct = LldpConfig(deviceObj=device2, enable=True)
    assert retCode==0, "\nFailed to enable lldp feature"

    #Entering interface SW1
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface= device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to enable interface"

    #Configuring no routing on interface
    #Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    #Entering interface
    LogOutput('info', "Switch 1 interface is :"
              + str(device1.linkPortMapping['lnk01']))
    devIntRetStruct = device1.DeviceInteract(command="interface "
                                             + str(device1.linkPortMapping['lnk01']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"

    devIntRetStruct = device1.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to disable routing"

    #Exiting interface
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    # Exiting Config terminal
    retStruct= device1.ConfigVtyShell(enter=False)
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
    LogOutput('info', "Switch 2 interface is :"
              + str(device2.linkPortMapping['lnk01']))
    devIntRetStruct = device2.DeviceInteract(command="interface "
                                             + str(device2.linkPortMapping['lnk01']))
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

    # Waiting for LLDP message exchange
    time.sleep(15)

    # Parsing neighbour info for SW1
    device1.setDefaultContext(context="linux")
    for retry in range(1, 3):
        LogOutput('info', "\nShowing Lldp neighbourship on SW1")
        retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        # LogOutput('info', "CLI_Switch1")
        LogOutput('info', "CLI_Switch1 Output\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch1 Return Structure")
        retStruct.printValueString()
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
        neiPortId = str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()
        if neiPortId.isdigit() is True or re.match(r'\d{1,2}-\d{1}',neiPortId):
            break
        else:
            # Dump out the ovs-vsctl interface information
            device1.setDefaultContext(context="linux")
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
    device1.setDefaultContext(context="vtyShell")
    assert str((lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()) == str(device2.linkPortMapping['lnk01']), "Case Failed, No Neighbor present for SW1"
    if (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info', "\nCase Passed, Neighborship established by SW1")
        LogOutput('info', "\nPort of SW1 neighbor is :"
                  + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']))
        LogOutput('info', "\nChassie Capabilities available : "
                  + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "
                  + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']))

    # Parsing neighbour info for SW2
    device2.setDefaultContext(context="linux")
    for retry in range(1, 3):
        LogOutput('info', "\nShowing Lldp neighbourship on SW2")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        # LogOutput('info', "CLI_Switch2")
        LogOutput('info', "CLI_Switch2 Output\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbor Port ID: "
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
        neiPortId = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()
        if neiPortId.isdigit() is True or re.match(r'\d{1,2}-\d{1}',neiPortId):
            break
        else:
            # Dump out the ovs-vsctl interface information
            device2.setDefaultContext(context="linux")
            LogOutput('info', "Didn't receive integer value for "
                      "Neightbor_portID, dumping ovs-vsctl interface stats...")
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
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    assert str((lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()) == str(device1.linkPortMapping['lnk01']), "Case Failed, No Neighbor present for SW2"
    if (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info', "\nCase Passed, Neighborship established by SW2")
        LogOutput('info', "\nPort of SW2 neighbor is :"
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']))
        LogOutput('info', "\nChassie Capablities available : "
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']))

    # Disabling lldp SW2
    LogOutput('info', "\nDisabling lldp on SW2")

    # Entering vtysh SW2
    returnStructure = device2.VtyshShell(enter=True)
    retCode = returnStructure.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering config terminal SW2
    devIntRetStruct = device2.ConfigVtyShell(enter=True)
    retCode = devIntRetStruct.returnCode()
    assert retCode == 0, "Failed to enter config prompt"

    LogOutput('info', "\nConfiguring no lldp enable on SW2")
    devIntRetStruct = device2.DeviceInteract(command="no lldp enable")
    retCode = devIntRetStruct.get('returnCode')

    assert retCode == 0, "Failed to disable feature lldp"

    # Exiting configuration terminal
    devIntRetStruct = device2.ConfigVtyShell(enter=False)
    retCode = devIntRetStruct.returnCode()
    assert retCode == 0, "Failed to exit Config prompt"

    # Exiting vtysh terminal
    retStruct = device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Waiting for neighbour entry to ageout in (2*5 = 10 seconds)
    time.sleep(15)
    device1.setDefaultContext(context="linux")
    for retry in range(1, 3):
        LogOutput('info', "\nShowing Lldp neighbourship on SW1")
        retStruct = ShowLldpNeighborInfo(deviceObj=device1,
                                         port=device1.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbor info"

        # LogOutput('info', "CLI_Switch1Link1")
        LogOutput('info', "CLI_Switch1 Output\n" + str(retStruct.buffer()))
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
        if str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip() == "":
            break
        else:
            # Dump out the ovs-vsctl interface information
            device1.setDefaultContext(context="linux")
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
    device1.setDefaultContext(context="vtyShell")
    assert (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip() == "", "Case Failed, Neighbor present for SW1"
    LogOutput('info', "\nNo Neighbour is present for SW1, hence case passed")

    device2.setDefaultContext(context="linux")
    for retry in range(1, 3):
        LogOutput('info', "\nShowing Lldp neighbourship on SW2")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                         port=device2.linkPortMapping['lnk01'])
        retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        # LogOutput('info', "CLI_Switch2")
        LogOutput('info', "CLI_Switch2 Output\n" + str(retStruct.buffer()))
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
        if str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip() == "":
            break
        else:
            # Dump out the ovs-vsctl interface information
            device2.setDefaultContext(context="linux")
            LogOutput('info', "Didn't receive integer value for Neightbor_portID, dumping ovs-vsctl interface stats...")
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
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip() == "", "Case Failed, Neighbor present for SW2"
    LogOutput('info', "\nNo Neighbour is present for SW2, case passed")


@pytest.mark.timeout(1000)
class Test_lldp_configuration:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_lldp_configuration.testObj =\
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        #    Get topology object
        Test_lldp_configuration.topoObj =\
            Test_lldp_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_lldp_configuration.topoObj.terminate_nodes()

    def test_lldp_wait_hold(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        lldp_wait_hold(device1=dut01Obj, device2=dut02Obj)
