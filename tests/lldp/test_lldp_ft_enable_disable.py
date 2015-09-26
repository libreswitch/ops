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
            "topoLinks": "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,dut02:system-category:switch"}
def lldp_enable_disable(**kwargs):
    device1 = kwargs.get('device1',None)
    device2 = kwargs.get('device2',None)

    #Configuring lldp on SW1
    LogOutput('info', "\n\n\nConfig lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to configure LLDP on SW1"

    #Enabling interface 1 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enabling interafce on SW1"

    LogOutput('info', "\n\n\nConfig lldp on SW2")
    retStruct = LldpConfig(deviceObj=device2, enable=True)
    retCode = retStruct.returnCode()
    assert retCode==0, "Configure lldp on SW2"

    #Enabling interface 1 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to enable interface on SW2"

    #Waiting for neighbour entry to flood
    Sleep(seconds=30, message="\nWaiting")

    #Parsing neighbour info for SW1
    LogOutput('info', "\nShowing Lldp neighbourship on SW1")
    retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to show neighbour info"

    LogOutput('info', "CLI_Switch1")
    retStruct.printValueString()
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
    assert int((lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())==1, "Case Failed, No Neighbor present for SW1"
    if (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']):
       LogOutput('info',"\nCase Passed, Neighborship established by SW1")
       LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']))
       LogOutput('info',"\nChassie Capabilities available : "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
       LogOutput('info', "\nChassis Capabilities Enabled : "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']))
    #Parsing neighbour info for SW2
    LogOutput('info', "\nShowing Lldp neighborship on SW2")
    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])

    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to show neighour info"

    LogOutput('info', "CLI_Switch2")
    retStruct.printValueString()
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
    assert int((lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())==1, "Case Failed, No Neighbor present for SW2"
    if (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']):
       LogOutput('info',"\nCase Passed, Neighborship established by SW2")
       LogOutput('info', "\nPort of SW2 neighbor is :" + str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']))
       LogOutput('info',"\nChassie Capablities available : "+ str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Available']))
       LogOutput('info', "\nChassis Capabilities Enabled : "+ str( lnk01PrtStats[device2.linkPortMapping['lnk01']]['Chassis_Capabilities_Enabled']))

    LogOutput('info', "\nDisabling lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    LogOutput('info', "\nDisabling lldp on SW2")
    retStruct = LldpConfig(deviceObj=device2, enable=False)
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    Sleep(seconds=2, message="\nWaiting")

    #Parsing lldp neighbour info SW1
    LogOutput('info', "\nShowing Lldp neighborship on SW1")
    retStruct = ShowLldpNeighborInfo(deviceObj=device1, port=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Failed to show neighbor info"

    LogOutput('info', "CLI_Switch1")
    retStruct.printValueString()

    lnk01PrtStats = retStruct.valueGet(key='portStats')
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
    assert (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()=="" ,"Case Failed, Neighbor present for SW1"
    if (lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']):
       LogOutput('info',"\nCase Failed, Neighborship still present on SW1")
       LogOutput('info', "\nPort of SW1 neighbor is :" + str(lnk01PrtStats[device1.linkPortMapping['lnk01']]['Neighbor_portID']))

    else:
       LogOutput('info',"\nCase Passed, No Neighbor is present for SW1")

    #Parsing lldp neighbour info SW2
    LogOutput('info', "\nShowing Lldp neighborship on SW2")
    retStruct = ShowLldpNeighborInfo(deviceObj=device2, port=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "\nFailed to show neighbor info"
    lnk01PrtStats = retStruct.valueGet(key='portStats')
    LogOutput('info', "CLI_Switch2")
    retStruct.printValueString()
    LogOutput('info', "\nExpected Neighbor Port ID: "+str(lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip())
    assert (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']).rstrip()=="", "Case Failed, Neighbor present for SW2"
    if (lnk01PrtStats[device2.linkPortMapping['lnk01']]['Neighbor_portID']):
       LogOutput('info',"\nCase Failed, Neighborship is still present on SW2")

    else :
       LogOutput('info',"Case Passed, No Neighbor is present for SW2")


    # Down the interfaces
    LogOutput('info', "Disabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=False, interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode==0, "Unable to disable interface"

    LogOutput('info', "Disabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=False, interface=device2.linkPortMapping['lnk01'])
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

    def test_lldp_enable_disable(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retValue = lldp_enable_disable(device1=dut01Obj, device2=dut02Obj)"""
