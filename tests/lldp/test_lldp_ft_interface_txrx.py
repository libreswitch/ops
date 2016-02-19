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
            "topoLinks": "lnk01:dut01:dut02,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch"}

def lldp_interface_txrx(**kwargs):
    device1 = kwargs.get('device1',None)
    device2 = kwargs.get('device2',None)

    device1.commandErrorCheck = 0
    device2.commandErrorCheck = 0
    #Defining the test steps
    LogOutput('info', "\n\nCase 1:\nSW 1 : lldp tx and rx enabled on link 1")
    LogOutput('info', "\n\nCase 2:\nSW 1 : lldp tx disabled on link 2")
    LogOutput('info', "\n\nCase 3:\nSW 1 : lldp rx disabled on link 3")
    LogOutput('info', "\n\nCase 4:\nSW 1 : lldp tx and rx disabled on link 4")


    #Entering interface for link 2 SW1, disabling tx
    retStruct = LldpInterfaceConfig(deviceObj=device1, interface=device1.linkPortMapping['lnk02'], transmission=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable tx on SW1"

    #Entering interface for link 3 SW1, disabling rx
    retStruct = LldpInterfaceConfig(deviceObj=device1, interface=device1.linkPortMapping['lnk03'], reception=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable rx on SW1"

    #Entering interface for link 4 SW1, disabling rx and tx
    retStruct = LldpInterfaceConfig(deviceObj=device1, interface=device1.linkPortMapping['lnk04'], transmission=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable tx on SW1"

    retStruct = LldpInterfaceConfig(deviceObj=device1, interface=device1.linkPortMapping['lnk04'], reception=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable rx on SW1"

    #Configuring lldp on SW1
    LogOutput('info', "\n\n\nConfig lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to configure LLDP on SW1"

    #Configuring lldp on SW1
    LogOutput('info', "\n\n\nConfig lldp on SW2")
    retStruct = LldpConfig(deviceObj=device2, enable=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to configure lldp on SW2"

    # Configuring no routing on interface
    #Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Entering interface
    LogOutput('info', "Switch 1 interface is :"+str(device1.linkPortMapping['lnk01']))
    devIntRetStruct = device1.DeviceInteract(command="interface "
                                             +str(device1.linkPortMapping['lnk01']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to enter interface"

    devIntRetStruct = device1.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to disable routing"

    #Exiting interface
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to exit interface"

    #Exiting Config terminal
    retStruct= device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting VTYSH terminal
    retStruct=device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"
    # End configuring no routiner on switch1 port over lnk01

    #Enabling interface 1 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW1"

    #Enabling interface 2 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW1"

    # Configuring no routing on interface
    #Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Entering interface
    LogOutput('info', "Switch 1 interface is :"+str(device1.linkPortMapping['lnk02']))
    devIntRetStruct = device1.DeviceInteract(command="interface "+str(device1.linkPortMapping['lnk02']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to enter interface"

    devIntRetStruct = device1.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to disable routing"

    #Exiting interface
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to exit interface"

    #Exiting Config terminal
    retStruct= device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting VTYSH terminal
    retStruct=device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"
    # End configuring no routing switch 1 port over lnk02

    #Enabling interface 3 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW1"

    # Configuring no routing on interface
    #Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Entering interface
    LogOutput('info', "Switch 1 interface is :"+str(device1.linkPortMapping['lnk03']))
    devIntRetStruct = device1.DeviceInteract(command="interface "+str(device1.linkPortMapping['lnk03']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to enter interface"

    devIntRetStruct = device1.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to disable routing"

    #Exiting interface
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to exit interface"

    #Exiting Config terminal
    retStruct= device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting VTYSH terminal
    retStruct=device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"
    # End configure no routing switch 1 port over lnk03

    #Enabling interface 4 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk04'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW1"

    # Configuring no routing on interface
    #Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Entering interface
    LogOutput('info', "Switch 1 interface is :"+str(device1.linkPortMapping['lnk04']))
    devIntRetStruct = device1.DeviceInteract(command="interface "+str(device1.linkPortMapping['lnk04']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to enter interface"

    devIntRetStruct = device1.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to disable routing"

    #Exiting interface
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to exit interface"

    #Exiting Config terminal
    retStruct= device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting VTYSH terminal
    retStruct=device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"
    # End configure no routing switch1 port over lnk04

    #Enabling interface 1 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW2"

    # Configure no routing switch2 port over lnk01
    #Entering VTYSH terminal
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device2.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Entering interface 1
    LogOutput('info', "Switch 2 interface is : "+str(device2.linkPortMapping['lnk01']))
    devIntRetStruct = device2.DeviceInteract(command="interface "+str(device2.linkPortMapping['lnk01']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to enter interface"

    devIntRetStruct = device2.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to disable routing"

    #Exiting interface
    devIntRetStruct = device2.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to exit interface"

    #Exiting config terminal
    retStruct= device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting VTYSH terminal
    retStruct=device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"
    # End configure switch2 no routing on port over lnk01

    #Enabling interface 2 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW2"

    # Configure no routing on switch2 port over lnk02
    #Entering VTYSH terminal
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device2.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Entering interface 1
    LogOutput('info', "Switch 2 interface is : "+str(device2.linkPortMapping['lnk02']))
    devIntRetStruct = device2.DeviceInteract(command="interface "+str(device2.linkPortMapping['lnk02']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to enter interface"

    devIntRetStruct = device2.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to disable routing"

    #Exiting interface
    devIntRetStruct = device2.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to exit interface"

    #Exiting config terminal
    retStruct= device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting VTYSH terminal
    retStruct=device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"
    # End configure no routing on switch 2 port over lnk02

    #Enabling interface 3 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW2"

    # Configure no routing switch2 port over lnk03
    #Entering VTYSH terminal
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device2.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Entering interface 1
    LogOutput('info', "Switch 2 interface is : "+str(device2.linkPortMapping['lnk03']))
    devIntRetStruct = device2.DeviceInteract(command="interface "+str(device2.linkPortMapping['lnk03']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to enter interface"

    devIntRetStruct = device2.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to disable routing"

    #Exiting interface
    devIntRetStruct = device2.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to exit interface"

    #Exiting config terminal
    retStruct= device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting VTYSH terminal
    retStruct=device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"
    # End configure no routing on switch 2 port over lnk03

    #Enabling interface 4 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk04'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW2"

    # Configure no routing switch2 port over lnk04
    #Entering VTYSH terminal
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device2.ConfigVtyShell(enter=True)
    retCode= retStruct.returnCode()
    assert retCode==0, "Failed to enter config terminal"

    #Entering interface 1
    LogOutput('info', "Switch 2 interface is : "+str(device2.linkPortMapping['lnk04']))
    devIntRetStruct = device2.DeviceInteract(command="interface "+str(device2.linkPortMapping['lnk04']))
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to enter interface"

    devIntRetStruct = device2.DeviceInteract(command="no routing")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to disable routing"

    #Exiting interface
    devIntRetStruct = device2.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode==0, "Failed to exit interface"

    #Exiting config terminal
    retStruct= device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to come out of config terminal"

    #Exiting VTYSH terminal
    retStruct=device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to exit vtysh prompt"
    # End configure no routing switch2 port over lnk04

    #Waiting for neighbour entry to flood
    Sleep(seconds=30, message="\nWaiting ")

    #Parsing neighbour info for SW1 and SW2
    #Case 1
    LogOutput('info', "\n\n\n### Case 1: tx and rx enabled on SW1 ###\n\n\n")
    device1.setDefaultContext(context="linux")
    for retry in range(1, 3):
        LogOutput('info', "\nShowing Lldp neighborship by SW1 on Link 1")
        retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode==0, "\nFailed to show neighbor info"
    
        LogOutput('info', "CLI_Switch1Link1 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch1Link1 Return Structure")
        retStruct.printValueString()
        lnk01PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
        neiPortId = str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()
        if neiPortId.isdigit() is True:
            break
        else:
            # Dump out the ovs-vsctl interface information
            device1.setDefaultContext(context="linux")
            LogOutput('info', "Didn't receive integer value for Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device1.linkPortMapping['lnk01'])
            neighbor_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device1.linkPortMapping['lnk01'])
            ifconfig_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n" 
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device1.setDefaultContext(context="vtyShell")
    #assert int((lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())==1, "Case Failed, No Neighbor is present for SW1 on Link 1"
    assert int((lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())== int(device2.linkPortMapping['lnk01']), "Case Failed, No Neighbor is present for SW1 on Link 1"
    if (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info',"Case Passed, Neighborship established by SW1 on Link1")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capabilities available : "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))

    device2.setDefaultContext(context="linux")
    for retry in range(1,3):
        LogOutput('info', "\nShowing Lldp neighborship on SW2 Link 1")
        retStruct= ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
        retCode = retStruct.returnCode()
        assert retCode==0, "\nFailed to show neighbor info"
        lnk01PrtStats = retStruct.valueGet(key='portStats')
    
        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
        neiPortId = str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()
        if neiPortId.isdigit() is True:
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
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    #assert int((lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())==1, "Case Failed, No Neighbor is present for SW2 on link 1"
    assert int((lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())== int(device1.linkPortMapping['lnk01']), "Case Failed, No Neighbor is present for SW2 on link 1"
    if (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info',"\nCase Passed, Neighborship established by SW2 on Link 1")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capablities available : "+ str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+ str( lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']
))

    LogOutput('info', "\n\n\n### Case 2: tx disabled on SW1 ###\n\n\n")

    device1.setDefaultContext(context="linux")
    for retry in range(1,3):
        LogOutput('info', "\nShowing Lldp neighborship on Link 2 for SW1")
        retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk02'])
        retCode = retStruct.returnCode()
        assert retCode==0, "\nFailed to show neighbor info"
        lnk02PrtStats = retStruct.valueGet(key='portStats')
    
        LogOutput('info', "CLI_Switch1 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch1 Return Structure")
        retStruct.printValueString()
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip())
        neiPortId = str(lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip()
        if neiPortId.isdigit() is True:
            break
        else:
            # Dump out the ovs-vsctl interface information
            device1.setDefaultContext(context="linux")
            LogOutput('info', "Didn't receive integer value for Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device1.linkPortMapping['lnk02'])
            neighbor_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device1.linkPortMapping['lnk02'])
            ifconfig_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device1.setDefaultContext(context="vtyShell")
    #assert int((lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip())==2, "Case Failed, No Neighbor present for SW1 on Link 2"
    assert int((lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip())== int(device2.linkPortMapping['lnk02']), "Case Failed, No Neighbor present for SW1 on Link 2"
    if (lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']):
        LogOutput('info',"Case Passed,  Neighborship established for SW1 on link 2")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capabilities available : "+str(lnk02PrtStats[device1.linkPortMapping['lnk02']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+str(lnk02PrtStats[device1.linkPortMapping['lnk02']]['Chassis_Capabilities_Enabled']))

    device2.setDefaultContext(context="linux")
    for retry in range(1,3):
        LogOutput('info', "\nShowing Lldp neighborship for SW2 on Link 2 ")
        
        retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk02'])
        retCode = retStruct.returnCode()
        assert retCode==0, "\nFailed to show neighbor info"
        lnk02PrtStats = retStruct.valueGet(key='portStats')
        
        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()
        LogOutput('info', "\nExpected Neighbor Port ID: "
                  + str(lnk02PrtStats[device2.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip())
        if str(lnk02PrtStats[device2.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip() == "" :
            break
        else:
            # Dump out the ovs-vsctl interface information
            device2.setDefaultContext(context="linux")
            LogOutput('info', "Didn't receive integer value for Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk02'])
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk02'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    assert (lnk02PrtStats[device2.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip()=="", "Case Failed, Neighbor is present for SW2 Link 2"    
    if (lnk02PrtStats[device2.linkPortMapping['lnk02']]['Neighbor_portID']):
        LogOutput('info',"\nCase Failed, Neighborship established by SW2 on Link 2")
        LogOutput('info', "\nPort of SW2 neighbor is :" + str(lnk02PrtStats[device2.linkPortMapping['lnk02']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capablities available : "+ str(lnk02PrtStats[device2.linkPortMapping['lnk02']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+ str( lnk02PrtStats[device2.linkPortMapping['lnk02']]['Chassis_Capabilities_Enabled']
))
    else :
        LogOutput('info',"Case Passed ,No Neighbor is present for SW2 on Link 2")


    #Case 3

    LogOutput('info', "\n\n\n### Case 3: rx disabled on SW1 ###\n\n\n")
    device1.setDefaultContext(context="linux")
    for retry in range(1,3):
        LogOutput('info', "\nShowing Lldp neighborship for SW1 on Link 3")
        retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk03'])
        retCode = retStruct.returnCode()
        assert retCode==0, "\nFailed to show neighbor info"
    
        lnk03PrtStats = retStruct.valueGet(key='portStats')
    
        LogOutput('info', "CLI_Switch1 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch1 Return Structure")
        retStruct.printValueString()
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk03PrtStats[device1.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip())
        if str(lnk03PrtStats[device1.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip() == "":
            break
        else:
            # Dump out the ovs-vsctl interface information
            device1.setDefaultContext(context="linux")
            LogOutput('info', "Didn't receive integer value for Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device1.linkPortMapping['lnk03'])
            neighbor_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device1.linkPortMapping['lnk03'])
            ifconfig_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device1.setDefaultContext(context="vtyShell")
    assert (lnk03PrtStats[device1.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip()=="", "Case Failed, Neighbor present for SW1 Link 3"
    if (lnk03PrtStats[device1.linkPortMapping['lnk03']]['Neighbor_portID']):
        LogOutput('info',"\nCase Failed, Neighborship established by SW1 on Link 3")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk03PrtStats[device1.linkPortMapping['lnk03']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capabilities available : "+str(lnk03PrtStats[device1.linkPortMapping['lnk03']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+str(lnk03PrtStats[device1.linkPortMapping['lnk03']]['Chassis_Capabilities_Enabled']))

    else:
        LogOutput('info',"Case Passed, No Neighbor is present for SW1 on Link 3")

    device2.setDefaultContext(context="linux")
    for retry in range(1,3):
        LogOutput('info', "\nShowing Lldp neighborship for SW2 on Link 3")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk03'])
        retCode = retStruct.returnCode()
        assert retCode==0, "\nFailed to show neighbor info"
        lnk03PrtStats = retStruct.valueGet(key='portStats')
    
        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip())
        neiPortId = str(lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip()
        if neiPortId.isdigit() is True:
            break
        else:
            # Dump out the ovs-vsctl interface information
            device2.setDefaultContext(context="linux")
            LogOutput('info', "Didn't receive integer value for Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk03'])
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk03'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    #assert int((lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip())==3, "Case Passed, No Neighbor is present for SW2 on Link 3"
    assert int((lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip())== int(device1.linkPortMapping['lnk03']), "Case Passed, No Neighbor is present for SW2 on Link 3"
    if (lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']):
        LogOutput('info',"\nCase Passed, Neighborship established by SW2 on Link 3")
        LogOutput('info', "\nPort of SW2 neighbour is :" + str(lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capablities available : "+ str(lnk03PrtStats[device2.linkPortMapping['lnk03']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+ str( lnk03PrtStats[device2.linkPortMapping['lnk03']]['Chassis_Capabilities_Enabled']))

    #Case 4

    LogOutput('info', "\n\n\n### Case 4:tx and rx disabled on SW1 ###\n\n\n")

    device1.setDefaultContext(context="linux")
    for retry in range(1,3):
        LogOutput('info', "\nShowing Lldp neighborship on SW1 Port 4")
        retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk04'])
        retCode = retStruct.returnCode()
        assert retCode==0, "\nFailed to show neighbor info"
    
    
        LogOutput('info', "CLI_Switch1 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch1 Return Structure")
        retStruct.printValueString()
    
        lnk04PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk04PrtStats[device1.linkPortMapping['lnk04']]['Neighbor_portID']).rstrip())
        if str(lnk04PrtStats[device1.linkPortMapping['lnk04']]['Neighbor_portID']).rstrip() == "":
            break;
        else:
            # Dump out the ovs-vsctl interface information
            device1.setDefaultContext(context="linux")
            LogOutput('info', "Didn't receive integer value for Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device1.linkPortMapping['lnk04'])
            neighbor_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device1.linkPortMapping['lnk04'])
            ifconfig_output = device1.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device1.setDefaultContext(context="vtyShell")
    assert (lnk04PrtStats[device1.linkPortMapping['lnk04']]['Neighbor_portID']).rstrip()=="", "Case Failed, Neighbor is present for SW1 on Link 4"
    if (lnk04PrtStats[device1.linkPortMapping['lnk04']]['Neighbor_portID']):
        LogOutput('info',"\nCase Failed, Neighborship established by SW1 on Link 4")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk04PrtStats[device1.linkPortMapping['lnk04']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capabilities available : "+str(lnk04PrtStats[device1.linkPortMapping['lnk04']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+str(lnk04PrtStats[device1.linkPortMapping['lnk04']]['Chassis_Capabilities_Enabled']))
    else:
        LogOutput('info',"Case Passed, No Neighbor is present for SW1 on Link 4")

    device2.setDefaultContext(context="linux")
    for retry in range(1,3):
        LogOutput('info', "\nShowing Lldp neighborship on SW2")
        retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk04'])
        retCode = retStruct.returnCode()
        assert retCode==0, "Failed to show neighbor info"
        lnk04PrtStats = retStruct.valueGet(key='portStats')
        LogOutput('info', "CLI_Switch2 Output:\n" + str(retStruct.buffer()))
        LogOutput('info', "CLI_Switch2 Return Structure")
        retStruct.printValueString()
        LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk04PrtStats[device2.linkPortMapping['lnk04']]['Neighbor_portID']).rstrip())
        if str(lnk04PrtStats[device2.linkPortMapping['lnk04']]['Neighbor_portID']).rstrip() == "":
            break
        else:
            # Dump out the ovs-vsctl interface information
            device2.setDefaultContext(context="linux")
            LogOutput('info', "Didn't receive integer value for Neightbor_portID, dumping ovs-vsctl interface stats...")
            devCmd = "ovs-vsctl list interface "\
                + str(device2.linkPortMapping['lnk04'])
            neighbor_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                                + str(neighbor_output))
            devCmd = "ip netns exec swns ifconfig "\
                + str(device2.linkPortMapping['lnk04'])
            ifconfig_output = device2.cmd(devCmd)
            opstestfw.LogOutput('info', devCmd
                                + " output\n"
                                + str(ifconfig_output))
            Sleep(seconds=10, message="Delay")
    device2.setDefaultContext(context="vtyShell")
    assert (lnk04PrtStats[device2.linkPortMapping['lnk04']]['Neighbor_portID']).rstrip()=="", "Case Failed, Neighbor is present for SW1 on Link 4"

    if (lnk04PrtStats[device2.linkPortMapping['lnk04']]['Neighbor_portID']):
        LogOutput('info',"\nCase Failed, Neighborship established by SW2 on Link 4")
        LogOutput('info', "\nPort of SW2 neighbour is :" + str(lnk04PrtStats[device2.linkPortMapping['lnk04']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capablities available : "+ str(lnk04PrtStats[device2.linkPortMapping['lnk04']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+ str( lnk04PrtStats[device2.linkPortMapping['lnk04']]['Chassis_Capabilities_Enabled']
))

    else :
        LogOutput('info',"Case Passed, No Neighbor is present for SW2 on Link 4")

    # Down the interfaces
    LogOutput('info', "Disabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=False, interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    retStruct = InterfaceEnable(deviceObj=device1, enable=False, interface=device1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    retStruct = InterfaceEnable(deviceObj=device1, enable=False, interface=device1.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    retStruct = InterfaceEnable(deviceObj=device1, enable=False, interface=device1.linkPortMapping['lnk04'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    LogOutput('info', "Disabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=False, interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    retStruct = InterfaceEnable(deviceObj=device2, enable=False, interface=device2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    retStruct = InterfaceEnable(deviceObj=device2, enable=False, interface=device2.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    retStruct = InterfaceEnable(deviceObj=device2, enable=False, interface=device2.linkPortMapping['lnk04'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"
    

@pytest.mark.timeout(1000)
class Test_lldp_configuration:
    def setup_class (cls):
        # Test object will parse command line and formulate the env
        Test_lldp_configuration.testObj = testEnviron(topoDict=topoDict,
                                                      defSwitchContext=\
                                                        "vtyShell")
        #    Get topology object
        Test_lldp_configuration.topoObj = Test_lldp_configuration.testObj.topoObjGet()

    def teardown_class (cls):
        Test_lldp_configuration.topoObj.terminate_nodes()

    def test_lldp_interface_txrx(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retValue = lldp_interface_txrx(device1=dut01Obj, device2=dut02Obj)
