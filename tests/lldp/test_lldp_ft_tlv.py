#!/usr/bin/env pythonll Rights Reserved.
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
# under the License
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
# All Rights Reserved.

from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *
from opstestfw import testEnviron
from opstestfw import LogOutput
from opstestfw import Sleep


# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02 wrkston01",
            "topoLinks": "lnk01:dut01:dut02,lnk02:dut02:wrkston01",
            "topoFilters": "dut01:system-category:switch,dut02:system-\
                 category:switch,wrkston01:system-category:workstation, \
                 wrkston01:\docker-image:host/freeradius-ubuntu"}


def lldp_tlv(**kwargs):
    device1 = kwargs.get('device1', None)
    device2 = kwargs.get('device2', None)

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
    LogOutput('info', "Switch 1 interface is : " +
              str(device1.linkPortMapping['lnk01']))
    devIntRetStruct = device1.DeviceInteract(
        command="interface " + str(device1.linkPortMapping['lnk01']))
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

    # Configuring no routing on interface
    # Entering VTYSH terminal
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device2.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    # Entering interface 1
    LogOutput('info', "Switch 2 interface is : " +
              str(device2.linkPortMapping['lnk01']))
    devIntRetStruct = device2.DeviceInteract(
        command="interface " + str(device2.linkPortMapping['lnk01']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"

    devIntRetStruct = device2.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to disable routing"

    # Exiting interface
    devIntRetStruct = device2.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit interface"

    # Exiting config terminal
    retStruct = device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting VTYSH terminal
    retStruct = device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Setting tx time to 5 sec on SW1 and SW2
    # Entering vtysh SW1
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    # Setting tx time to 5 seconds on SW1
    LogOutput('info', "\nConfiguring transmit time of 5 sec on SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp timer 5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set transmit time"

    # Entering vtysh SW2
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to get vtysh prompt"

    # Entering config terminal SW2
    devIntRetStruct = device2.ConfigVtyShell(enter=True)
    retCode = devIntRetStruct.returnCode()
    assert retCode == 0, "\nFailed to enter config mode"

    # Setting tx time to 5 seconds on SW2
    LogOutput('info', "\nConfiguring transmit time of 5 sec on SW2")
    devIntRetStruct = device2.DeviceInteract(command="lldp timer 5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "\nFailed to configure transmit time"

    # Exiting Config terminal SW1
    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting Config terminal SW2
    retStruct = device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting vtysh terminal SW1
    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Exiting vtysh terminal SW2
    retStruct = device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Configuring lldp on SW1
    LogOutput('info', "\n\n\nConfig lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to configure LLDP on SW1"

    # Enabling interface 1 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enabling interafce on SW1"

    # Configuring lldp on SW2
    LogOutput('info', "\n\n\nConfig lldp on SW2")
    retStruct = LldpConfig(deviceObj=device2, enable=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Configure lldp on SW2"

    # Enabling interface 1 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True,
                                interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enable interface on SW2"

    # Waiting for neighbour to advertise
    Sleep(seconds=25, message="\nWaiting")
    # Set my default context to linux temporarily
    device1.setDefaultContext(context="linux")
    # Start loop
    for retry in range(1, 3):
        # Parsing neighbour info for SW1
        LogOutput('info', "\nShowing Lldp neighbourship on SW1")
        retStruct = ShowLldpNeighborInfo(deviceObj=device1,
                                         port=device1.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighbour info"

        LogOutput('info', "CLI_Switch1")
        retStruct.printValueString()
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbor Port ID: "
                  + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]
                        ['Neighbor_portID']).rstrip())
        neiPortId = str(lnk01PrtStats[device1.linkPortMapping['lnk01']]
                        ['Neighbor_portID']).rstrip()
        if neiPortId.isdigit() is True or re.match(r'\d{1,2}-\d{1}',neiPortId):
            break
        else:
            # Dump out the ovs-vsctl interface information
            LogOutput('info', "Didn't receive integer value for "
                      "Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device1.linkPortMapping['lnk01'])\
                + " | grep lldp_neighbor_info"
            neighbor_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device1.linkPortMapping['lnk01'])
            ifconfig_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd + " output\n" +
                                str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    # end loop
    # Set my default context to linux temporarily

    device1.setDefaultContext(context="vtyShell")
    assert str((lnk01PrtStats[device1.linkPortMapping['lnk01']]
                ['Neighbor_portID']).rstrip()) == device2.linkPortMapping['lnk01'], \
        "Case Failed, No Neighbor present for SW1"
    assert ("null" not in lnk01PrtStats[device1.linkPortMapping['lnk01']]
            ['Neighbor_chassisName']), \
        "Case Failed, Neighbor Chassis-Name is not present"
    assert ("null" not in lnk01PrtStats[device1.linkPortMapping['lnk01']]
            ['Neighbor_chassisDescription']), \
        "Case Failed, Neighbor Chassis-Description is not present"
    assert ("Bridge, Router" in lnk01PrtStats[device1.linkPortMapping['lnk01']]
            ['Chassis_Capabilities_Available']), \
            "Case Failed, Neighbor Chassis-Capabilities is not available"
    if (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info', "\nCase Passed, Neighborship established by SW1")
        LogOutput('info', "\nNeighbor Chassis-Name :" +
                  str(lnk01PrtStats[device1.linkPortMapping['lnk01']]
                      ['Neighbor_chassisName']))
        LogOutput('info', "\nNeighbor Chassis-Description :" +
                  str(lnk01PrtStats[device1.linkPortMapping['lnk01']]
                      ['Neighbor_chassisDescription']))
        LogOutput('info', "\nChassie Capabilities available : " +
                  str(lnk01PrtStats[device1.linkPortMapping['lnk01']]
                      ['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : " +
                  str(lnk01PrtStats[device1.linkPortMapping['lnk01']]
                      ['Chassis_Capabilities_Enabled']))

    # Parsing neighbour info for SW2

    # Loop for switch 2
    device2.setDefaultContext(context="linux")
    for retry in range(1, 3):
        LogOutput('info', "\nShowing Lldp neighborship on SW2")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                         port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show neighour info"
        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbor Port ID: "
                  + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                        ['Neighbor_portID']).rstrip())
        neiPortId = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                        ['Neighbor_portID']).rstrip()
        if neiPortId.isdigit() is True or re.match(r'\d{1,2}-\d{1}',neiPortId):
            break
        else:
            # Dump out the ovs-vsctl interface information
            LogOutput('info', "Didn't receive integer value for "
                      "Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk01'])\
                + " | grep lldp_neighbor_info"
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk01'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd + " output\n" +
                                str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")

    assert str((lnk01PrtStats[device2.linkPortMapping['lnk01']]
                ['Neighbor_portID']).rstrip()) == device1.linkPortMapping['lnk01'], \
        "Case Failed, No Neighbor present for SW1"
    assert ("null" not in lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Neighbor_chassisName']), \
        "Case Failed, Neighbor Chassis-Name is not present"
    assert ("null" not in lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Neighbor_chassisDescription']), \
        "Case Failed, Neighbor Chassis-Description is not present"
    assert ("Bridge, Router" in lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Chassis_Capabilities_Available']), \
        "Case Failed, Neighbor Chassis-Capabilities is not available"
    if (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info', "\nCase Passed, Neighborship established by SW2")
        LogOutput('info', "\nNeighbor Chassis-Name :" +
                  str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                      ['Neighbor_chassisName']))
        LogOutput('info', "\nNeighbor Chassis-Description :" +
                  str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                      ['Neighbor_chassisDescription']))
        LogOutput('info', "\nChassie Capablities available : " +
                  str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                      ['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : " +
                  str(lnk01PrtStats[device2.linkPortMapping['lnk01']]
                      ['Chassis_Capabilities_Enabled']))

    # Disabling chassie name for neighbor
    # Entering vtysh SW1
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    # Disabling system-name on SW1
    LogOutput('info', "\nDisabling system-name for SW1")
    devIntRetStruct = \
        device1.DeviceInteract(command="no lldp select-tlv system-name")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set no lldp select-tlv system-name"

    # Checking SW2 to see if system-name is removed
    device2.setDefaultContext(context="linux")
    for retry in range(1, 3):
        LogOutput('info', "\n\nCase 1:System-Name Disabled")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                         port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "\nFailed to show neighbor info"

        LogOutput('info', "CLI_Switch2")
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        if (lnk01PrtStats[device2.linkPortMapping['lnk01']]
                ['Neighbor_chassisName']) == "":
            break
        else:
            # Dump out the ovs-vsctl interface information
            LogOutput('info', "Didn't clear Neighbor Chassis-Name")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk01'])\
                + " | grep lldp_neighbor_info"
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk01'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd + " output\n" +
                                str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Neighbor_chassisName']) == "", \
        "Case Failed, Neighbor Chassis-Name is present"
    LogOutput('info', "#Case Passed,No neighbor Chassis-Name present#")

    # Enabling System-Name
    LogOutput('info', "\nEnabling System-Name for SW1")
    devIntRetStruct = \
        device1.DeviceInteract(command="lldp select-tlv system-name")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set lldp select-tlv system-name"

    # Checking SW2 to see if system-name is reset
    LogOutput('info', "\n\nCase 2 :System-Name Enabled")
    # Parsing lldp neighbour info SW2
    device2.setDefaultContext(context="linux")
    for retry in range(1, 3):

        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                         port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "\nFailed to show neighbor info"
        LogOutput('info', "CLI_Switch2")
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        if ("null" not in lnk01PrtStats[device2.linkPortMapping['lnk01']]
                ['Neighbor_chassisName']):
            break
        else:
            # Dump out the ovs-vsctl interface information
            LogOutput('info', "Didn't receive Chassis-Name")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk01'])\
                + " | grep lldp_neighbor_info"
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk01'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd + " output\n" +
                                str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    assert ("null" not in lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Neighbor_chassisName']), \
        "Case Failed, Neighbor Chassis-Name is not present"
    LogOutput('info', "#Case Passed,Neighbor Chassis-Name is present#")

    # Disabling Neighbor Chassis-Description
    LogOutput('info', "\nDisabling System-Description for SW1")
    devIntRetStruct = \
        device1.DeviceInteract(command="no lldp select-tlv system-description")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set no lldp select-tlv system-description"

    # Checking SW2 to see if system-description is removed

    LogOutput('info', "\n\nCase 3: System-Description Disabled")
    # Parsing lldp neighbour info SW2
    device2.setDefaultContext(context="linux")
    for retry in range(1, 3):
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                         port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "\nFailed to show neighbor info"
        LogOutput('info', "CLI_Switch2")
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        if (lnk01PrtStats[device2.linkPortMapping['lnk01']]
                ['Neighbor_chassisDescription']) == "":
            break
        else:
            # Dump out the ovs-vsctl interface information
            LogOutput('info', "Didn't receive System-Description")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk01'])\
                + " | grep lldp_neighbor_info"
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk01'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")

    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Neighbor_chassisDescription']) == "", \
        "Case Failed, Neighbor Chassis-Description is present"
    LogOutput('info', "#Case Passed,No neighbor Chassis-Description present#")

    # Enabling System-Description
    LogOutput('info', "\nEnabling System-description for SW1")
    devIntRetStruct = \
        device1.DeviceInteract(command="lldp select-tlv system-description")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set lldp select-tlv system-description"

    # Checking SW2 to see if system-name is reset

    LogOutput('info', "\n\nCase 4: System-Description Enabled")
    # Parsing lldp neighbour info SW2
    device2.setDefaultContext(context="linux")
    for retry in range(1, 3):
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                         port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "\nFailed to show neighbor info"
        LogOutput('info', "CLI_Switch2")
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        if ("null" not in lnk01PrtStats[device2.linkPortMapping['lnk01']]
                ['Neighbor_chassisDescription']):
            break
        else:
            # Dump out the ovs-vsctl interface information
            LogOutput('info', "Didn't receive System-Description")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk01'])\
                + " | grep lldp_neighbor_info"
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk01'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    assert ("null" not in lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Neighbor_chassisDescription']), \
        "Case Failed, Neighbor Chassis-Description is not present"
    LogOutput('info', "#Case Passed,Neighbor Chassis-Description is present#")

    # Disabling System-Capabilities
    LogOutput('info', "\nDisabling Neighor Chassis-Capabilities for SW1")
    devIntRetStruct = device1.DeviceInteract(
        command="no lldp select-tlv system-capabilities")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set no lldp select-tlv system-capabilities"

    # Checking SW2 to see if system-Capabilities is removed

    LogOutput('info', "\n\nCase 5: System-Capabilities disabled")
    device2.setDefaultContext(context="linux")
    for retry in range(1, 3):
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                         port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "\nFailed to show neighbor info"

        LogOutput('info', "CLI_Switch2")
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        if (lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Chassis_Capabilities_Available']) == "" and \
           (lnk01PrtStats[device2.linkPortMapping['lnk01']]
                ['Chassis_Capabilities_Enabled']) == "":
            break
        else:
            # Dump out the ovs-vsctl interface information
            LogOutput('info', "Didn't receive System-Capabilities")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk01'])\
                + " | grep lldp_neighbor_info"
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk01'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Chassis_Capabilities_Available']) == "", \
        "Case Failed, Neighbor Chassis-Capabilities is available"
    LogOutput('info',
              "#Case Passed,No neighbor Chassis-capablities available#")
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Chassis_Capabilities_Enabled']) == "", \
        "Case Failed, Neighbor Chassis-Capabilities is enabled"
    LogOutput('info', "#Case Passed,No neighbor Chassis-capablities enabled#")

    # System-Capabilities Enabled
    LogOutput('info', "\nEnabling Neighbor Chassis-Capabilities for SW1")
    devIntRetStruct = \
        device1.DeviceInteract(command="lldp select-tlv system-capabilities")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set lldp select-tlv system-capabilities"

    # Checking SW2 to see if system-name is reset

    LogOutput('info', "\n\nCase 6: System-Capabilities enabled")
    device2.setDefaultContext(context="linux")
    for retry in range(1, 3):
        retStruct = ShowLldpNeighborInfo(deviceObj=device2,
                                         port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode == 0, "\nFailed to show neighbor info"

        LogOutput('info', "CLI_Switch2")
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        if ("Bridge, Router" in lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Chassis_Capabilities_Available']) and\
           "Bridge, Router" in (lnk01PrtStats[device2.linkPortMapping['lnk01']]
                                ['Chassis_Capabilities_Enabled']):
            break
        else:
            # Dump out the ovs-vsctl interface information
            LogOutput('info', "Didn't receive System-Capabilities")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk01'])\
                + " | grep lldp_neighbor_info"
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk01'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    assert ("Bridge, Router" in lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Chassis_Capabilities_Available']), \
        "Case Failed, Neighbor Chassis-Capabilities is not available"
    LogOutput('info', "#Case Passed,Neighbor Chassis-capablities available#")
    assert ("Bridge, Router" in lnk01PrtStats[device2.linkPortMapping['lnk01']]
            ['Chassis_Capabilities_Enabled']), \
        "Case Failed, Neighbor Chassis-Capabilities is not enabled"
    LogOutput('info', "#Case Passed,Neighbor Chassis-capablities enabled#")

    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"


@pytest.mark.timeout(1000)
class Test_lldp_configuration:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_lldp_configuration.testObj = \
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        # Get topology object
        Test_lldp_configuration.topoObj = \
            Test_lldp_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_lldp_configuration.topoObj.terminate_nodes()

    def test_lldp_tlv(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        lldp_tlv(device1=dut01Obj, device2=dut02Obj)
