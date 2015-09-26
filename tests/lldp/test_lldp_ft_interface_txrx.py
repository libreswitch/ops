"""#!/usr/bin/env python

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
            "topoLinks": "lnk01:dut01:dut02,lnk02:dut01:dut02,lnk03:dut01:dut02,lnk04:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,dut02:system-category:switch"}

def lldp_interface_txrx(**kwargs):
    device1 = kwargs.get('device1',None)
    device2 = kwargs.get('device2',None)

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

    #Enabling interface 3 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW1"

    #Enabling interface 4 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk04'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW1"

    #Enabling interface 1 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW2"

    #Enabling interface 2 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW2"

    #Enabling interface 3 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW2"

    #Enabling interface 4 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk04'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW2"

    #Waiting for neighbour entry to flood
    Sleep(seconds=30, message="\nWaiting ")

    #Parsing neighbour info for SW1 and SW2
    #Case 1
    LogOutput('info', "\n\n\n### Case 1: tx and rx enabled on SW1 ###\n\n\n")

    LogOutput('info', "\nShowing Lldp neighborship by SW1 on Link 1")
    retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"

    LogOutput('info', "CLI_Switch1Link1")
    retStruct.printValueString()
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
    assert int((lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())==1, "Case Failed, No Neighbor is present for SW1 on Link 1"
    if (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info',"Case Passed, Neighborship established by SW1 on Link1")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capabilities available : "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))

    LogOutput('info', "\nShowing Lldp neighborship on SW2 Link 1")
    retStruct= ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"
    lnk01PrtStats = retStruct.valueGet(key='portStats')

    LogOutput('info', "CLI_Switch2")
    retStruct.printValueString()
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
    assert int((lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())==1, "Case Failed, No Neighbor is present for SW2 on link 1"
    if (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']):
        LogOutput('info',"\nCase Passed, Neighborship established by SW2 on Link 1")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capablities available : "+ str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+ str( lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']
))

    LogOutput('info', "\n\n\n### Case 2: tx disabled on SW1 ###\n\n\n")

    LogOutput('info', "\nShowing Lldp neighborship on Link 2 for SW1")

    retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"
    lnk02PrtStats = retStruct.valueGet(key='portStats')

    LogOutput('info', "CLI_Switch1")
    retStruct.printValueString()
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip())
    assert int((lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip())==2, "Case Failed, No Neighbor present for SW1 on Link 2"
    if (lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']):
        LogOutput('info',"Case Passed,  Neighborship established for SW1 on link 2")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk02PrtStats[device1.linkPortMapping['lnk02']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capabilities available : "+str(lnk02PrtStats[device1.linkPortMapping['lnk02']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+str(lnk02PrtStats[device1.linkPortMapping['lnk02']]['Chassis_Capabilities_Enabled']))

    LogOutput('info', "\nShowing Lldp neighborship for SW2 on Link 2 ")

    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"
    lnk02PrtStats = retStruct.valueGet(key='portStats')


    LogOutput('info', "CLI_Switch2")
    retStruct.printValueString()
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk02PrtStats[device2.linkPortMapping['lnk02']]['Neighbor_portID']).rstrip())
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

    LogOutput('info', "\nShowing Lldp neighborship for SW1 on Link 3")
    retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"

    lnk03PrtStats = retStruct.valueGet(key='portStats')

    LogOutput('info', "CLI_Switch1")
    retStruct.printValueString()
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk03PrtStats[device1.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip())
    assert (lnk03PrtStats[device1.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip()=="", "Case Failed, Neighbor present for SW1 Link 3"
    if (lnk03PrtStats[device1.linkPortMapping['lnk03']]['Neighbor_portID']):
        LogOutput('info',"\nCase Failed, Neighborship established by SW1 on Link 3")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk03PrtStats[device1.linkPortMapping['lnk03']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capabilities available : "+str(lnk03PrtStats[device1.linkPortMapping['lnk03']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+str(lnk03PrtStats[device1.linkPortMapping['lnk03']]['Chassis_Capabilities_Enabled']))

    else:
        LogOutput('info',"Case Passed, No Neighbor is present for SW1 on Link 3")

    LogOutput('info', "\nShowing Lldp neighborship for SW2 on Link 3")
    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"
    lnk03PrtStats = retStruct.valueGet(key='portStats')

    LogOutput('info', "CLI_Switch2")
    retStruct.printValueString()
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip())
    assert int((lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']).rstrip())==3, "Case Passed, No Neighbor is present for SW2 on Link 3"
    if (lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']):
        LogOutput('info',"\nCase Passed, Neighborship established by SW2 on Link 3")
        LogOutput('info', "\nPort of SW2 neighbour is :" + str(lnk03PrtStats[device2.linkPortMapping['lnk03']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capablities available : "+ str(lnk03PrtStats[device2.linkPortMapping['lnk03']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+ str( lnk03PrtStats[device2.linkPortMapping['lnk03']]['Chassis_Capabilities_Enabled']))

    #Case 4

    LogOutput('info', "\n\n\n### Case 4:tx and rx disabled on SW1 ###\n\n\n")

    LogOutput('info', "\nShowing Lldp neighborship on SW1 Port 4")

    retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk04'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"


    LogOutput('info', "CLI_Switch1")
    retStruct.printValueString()

    lnk04PrtStats = retStruct.valueGet(key='portStats')
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk04PrtStats[device1.linkPortMapping['lnk04']]['Neighbor_portID']).rstrip())
    assert (lnk04PrtStats[device1.linkPortMapping['lnk04']]['Neighbor_portID']).rstrip()=="", "Case Failed, Neighbor is present for SW1 on Link 4"
    if (lnk04PrtStats[device1.linkPortMapping['lnk04']]['Neighbor_portID']):
        LogOutput('info',"\nCase Failed, Neighborship established by SW1 on Link 4")
        LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk04PrtStats[device1.linkPortMapping['lnk04']]['Neighbor_portID']))
        LogOutput('info',"\nChassie Capabilities available : "+str(lnk04PrtStats[device1.linkPortMapping['lnk04']]['Chassis_Capabilities_Available']))
        LogOutput('info', "\nChassis Capabilities Enabled : "+str(lnk04PrtStats[device1.linkPortMapping['lnk04']]['Chassis_Capabilities_Enabled']))
    else:
        LogOutput('info',"Case Passed, No Neighbor is present for SW1 on Link 4")

    LogOutput('info', "\nShowing Lldp neighborship on SW2")
    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk04'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to show neighbor info"
    lnk04PrtStats = retStruct.valueGet(key='portStats')
    LogOutput('info', "CLI_Switch2")
    retStruct.printValueString()
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk04PrtStats[device2.linkPortMapping['lnk04']]['Neighbor_portID']).rstrip())
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

class Test_lldp_configuration:
    def setup_class (cls):
        # Test object will parse command line and formulate the env
        Test_lldp_configuration.testObj = testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_lldp_configuration.topoObj = Test_lldp_configuration.testObj.topoObjGet()

    def teardown_class (cls):
        Test_lldp_configuration.topoObj.terminate_nodes()

    def test_lldp_interface_txrx(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retValue = lldp_interface_txrx(device1=dut01Obj, device2=dut02Obj)"""
