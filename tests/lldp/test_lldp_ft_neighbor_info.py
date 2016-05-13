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
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

MGMT_PATTERN_IP4 = "192.168.1.1"
MGMT_PATTERN_IP6 = "fd12:3456:789a:1::"

MGMT_INTF_IP4_MASK = "24"
MGMT_INTF_IP6_MASK = "64"

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
    LogOutput('info', "Device2 DUMP")
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

def lldp_neighbor_info(**kwargs):
    device1 = kwargs.get('device1', None)
    device2 = kwargs.get('device2', None)

    device1.commandErrorCheck = 0
    device2.commandErrorCheck = 0
    LogOutput('info', "\n\n\nConfig lldp on SW1 and SW2")

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

    # Entering config terminal SW1
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

    # Entering interface 2
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

    ##### END ############

    # Case#1
    # Enter Configure IPv4 mgmt pattern SW1
    # Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering config terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    LogOutput('info', "\nConfigure IPv4 mgmt pattern SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp management-address "
                                             + MGMT_PATTERN_IP4)
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set mgmt pattern"

    # Exiting Config terminal
    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Parsing neighbour info for SW2
    device2.setDefaultContext(context="linux")

    # Waiting for LLDP message exchange
    Sleep(seconds=5, message="\nWaiting")

    # Verify neighbour info on SW2
    for retry in range(1, 5):
        # Parsing neighbour info for SW2
        LogOutput('info', "\nShowing LLDP neighbour on SW2")
        Sleep(seconds=5, message="Delay")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                     port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()

        lnk01PrtStats = retStruct.valueGet(key='portStats')
        mgmt_pattern = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                       ['Neighbor_Management_address']).rstrip()

        if (mgmt_pattern == MGMT_PATTERN_IP4):
            LogOutput('info', "Neighbour Management Address : " + mgmt_pattern)
            break

    if mgmt_pattern != MGMT_PATTERN_IP4:
        lldp_debug_dump(device1, device2)
        assert mgmt_pattern == MGMT_PATTERN_IP4, \
            "Case Failed, Management pattern present for SW1"

    device2.setDefaultContext(context="vtyShell")

    # Case#2
    # Enter Configure IPv6 mgmt pattern SW1
    # Entering VTYSH terminal
    device1.setDefaultContext(context="vtyShell")
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering config terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    LogOutput('info', "\nConfigure IPv6 mgmt pattern SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp management-address "
                                             + MGMT_PATTERN_IP6)
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set mgmt pattern"

    # Exiting Config terminal
    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Parsing neighbour info for SW2
    device2.setDefaultContext(context="linux")

    # Waiting for LLDP message exchange
    Sleep(seconds=5, message="\nWaiting")

    # Verify neighbour info on SW2
    for retry in range(1, 5):
        # Parsing neighbour info for SW2
        LogOutput('info', "\nShowing LLDP neighbour on SW2")
        Sleep(seconds=5, message="Delay")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                     port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()

        lnk01PrtStats = retStruct.valueGet(key='portStats')
        mgmt_pattern = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                       ['Neighbor_Management_address']).rstrip()

        if (mgmt_pattern == MGMT_PATTERN_IP6):
            LogOutput('info', "Neighbour Management Address : " + mgmt_pattern)
            break

    if mgmt_pattern != MGMT_PATTERN_IP6:
        lldp_debug_dump(device1, device2)
        assert mgmt_pattern == MGMT_PATTERN_IP6, \
            "Case Failed, IPv6 mgmt pattern present for SW1"

    if (mgmt_pattern == MGMT_PATTERN_IP6):
        LogOutput('info', "Neighbour Management Address : " + mgmt_pattern)

    device2.setDefaultContext(context="vtyShell")

    # Case#3
    # Enter Configure static ip on mgmt intf in SW1
    # Entering VTYSH terminal
    device1.setDefaultContext(context="vtyShell")
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering config terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    devIntRetStruct = device1.DeviceInteract(command="no lldp m")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to remove lldp mgmt pattern"

    # Exiting Config terminal
    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Configure IPv4 static im mgmt intf SW1
    LogOutput('info', "\nConfigure IPv4 static in mgmt intf SW1")
    retStruct = MgmtInterfaceConfig(deviceObj=device1, config=True,
                                    ipmode="static", addr=MGMT_PATTERN_IP4,
                                    mask=MGMT_INTF_IP4_MASK)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to set IPv4 in mgmt intf"

    # Configure IPv6 static in mgmt intf SW1
    LogOutput('info', "\nConfigure IPv6 static in mgmt intf SW1")
    retStruct = MgmtInterfaceConfig(deviceObj=device1, ipmode="static",
                                    addr=MGMT_PATTERN_IP6,
                                    mask=MGMT_INTF_IP6_MASK)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to set IPv6 in mgmt intf"

    retStruct = MgmtInterfaceConfig(deviceObj=device1, config=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of mgmt intf"

    # Waiting for LLDP message exchange
    Sleep(seconds=5, message="\nWaiting")

    # Verify neighbour info on SW2
    for retry in range(1, 5):
        # Parsing neighbour info for SW2
        LogOutput('info', "\nShowing LLDP neighbour on SW2")
        Sleep(seconds=5, message="Delay")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                     port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()

        lnk01PrtStats = retStruct.valueGet(key='portStats')
        mgmt_pattern = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                       ['Neighbor_Management_address']).rstrip()

        if (MGMT_PATTERN_IP6 in mgmt_pattern and MGMT_PATTERN_IP4 in mgmt_pattern):
            LogOutput('info', "Neighbour Management Address : " + mgmt_pattern)
            break

    assert (MGMT_PATTERN_IP6 in mgmt_pattern and
            MGMT_PATTERN_IP4 in mgmt_pattern), \
        "Case Failed, IPv6 mgmt pattern present for SW1"

    if (MGMT_PATTERN_IP6 in mgmt_pattern and MGMT_PATTERN_IP4 in mgmt_pattern):
        LogOutput('info', "Neighbour Management Address : " + mgmt_pattern)
    # Exit Configure static ip on mgmt intf in SW1

    # Case#4
    # Enter LLDP Clear Neighbour info in SW2
    device1.setDefaultContext(context="vtyShell")

    LogOutput('info', "\nDisabling lldp feature on SW1")
    devIntRetStruct = LldpConfig(deviceObj=device1, enable=False)
    retCode = devIntRetStruct.returnCode()
    assert retCode == 0, "\nFailed to disable lldp feature"

    # Entering VTYSH terminal
    device2.setDefaultContext(context="vtyShell")
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering config terminal SW1
    retStruct = device2.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    LogOutput('info', "\nLLDp clear neighbour info in SW2")
    devIntRetStruct = device2.DeviceInteract(command="lldp clear neighbors")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to execute lldp clear neighbors"

    # Exiting Config terminal
    retStruct = device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Waiting for LLDP message exchange
    Sleep(seconds=5, message="\nWaiting")

    # Verify neighbour info on SW2
    for retry in range(1, 5):
        # Parsing neighbour info for SW2
        LogOutput('info', "\nShowing LLDP neighbour on SW2")
        Sleep(seconds=5, message="Delay")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                     port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()

        lnk01PrtStats = retStruct.valueGet(key='portStats')

        neighbor_entries = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                           ['Neighbor_Entries']).rstrip()

        neighbor_deleted = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                           ['Neighbor_Entries_Deleted']).rstrip()

        if (int(neighbor_entries) == 0 and int(neighbor_deleted) >= 1):
            LogOutput('info', "Neighbor_Entries Cleared")
            break

    assert int(neighbor_entries) == 0, "Failed to delete neighbour info"

    assert int(neighbor_deleted) >= 1, "Failed to delete neighbour info"


    # Case#5
    # Enter LLDP Clear counter in SW2
    device1.setDefaultContext(context="vtyShell")

    LogOutput('info', "\nDisabling lldp feature on SW1")
    devIntRetStruct = LldpConfig(deviceObj=device1, enable=False)
    retCode = devIntRetStruct.returnCode()
    assert retCode == 0, "\nFailed to disable lldp feature"

    # Entering VTYSH terminal
    device2.setDefaultContext(context="vtyShell")
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering config terminal SW1
    retStruct = device2.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    LogOutput('info', "\nLLDP clear counter in SW2")
    devIntRetStruct = device2.DeviceInteract(command="lldp clear counter")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to execute lldp clear counter"

    # Exiting Config terminal
    retStruct = device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Waiting for LLDP message exchange
    Sleep(seconds=5, message="\nWaiting")

    # Verify neighbour info on SW2
    for retry in range(1, 5):
        # Parsing neighbour info for SW2
        LogOutput('info', "\nShowing LLDP neighbour on SW2")
        Sleep(seconds=5, message="Delay")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                     port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()

        lnk01PrtStats = retStruct.valueGet(key='portStats')

        neighbor_entries = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                           ['Neighbor_Entries']).rstrip()

        neighbor_deleted = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                           ['Neighbor_Entries_Deleted']).rstrip()

        if (int(neighbor_entries) == 0 and int(neighbor_deleted) >= 1):
            LogOutput('info', "Neighbor_Entries Cleared")
            break

    assert int(neighbor_entries) == 0, "Failed to clear counters"

    assert int(neighbor_deleted) == 0, "Failed to clear counters"

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

    def test_lldp_neighbor_info(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        lldp_neighbor_info(device1=dut01Obj, device2=dut02Obj)
