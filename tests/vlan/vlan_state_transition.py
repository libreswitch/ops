# (C) Copyright 2015 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
##########################################################################
# Description: Verify the status of the Vlan change from up to down correctly.
#               The status of a vlan is changed from down to up when a port is
#               added to the vlan and the vlan has been brought up with the
#               respective command.
#
# Author:      Jose Pablo Araya
#
# Topology:       |Switch|
#
# Success Criteria:  PASS -> Vlans status is correctly verifyed
#                            in every scenario
#
#                    FAILED -> If vlan status is wrong showed in one
#                              of the scenarios
#
##########################################################################

import pytest
import re
import opstestfw
from opstestfw.switch.CLI import *
from opstestfw import testEnviron
from opstestfw import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01",
            "topoFilters": "dut01:system-category:switch"}


# Independent functions called-used in main class
def verifyVlanState(dut, pStatus, numberToFind=1):
    LogOutput('info', "Validating vlan state")
    cont = 0
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.valueGet(key=None)
    for dictionary in returnData:
        if dictionary['Status'] == pStatus:
            cont = cont + 1
    if cont == numberToFind:
        return 0
    else:
        return 1

def cleanUp(dut):
    LogOutput('info', "############################################")
    LogOutput('info', "Step 6- Clean up ")
    LogOutput('info', "############################################")
    if AddVlan(deviceObj=dut, vlanId=2,
               config=False).returnCode() != 0:
        LogOutput('error', "Failed to delete vlan " + str(2)
    else:
        LogOutput('info', "Passed vlan " + str(2) + " deleted")


class Test_vlan_state_transition:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_vlan_state_transition.testObj = testEnviron(topoDict=topoDict)
        Test_vlan_state_transition.topoObj = \
            Test_vlan_state_transition.testObj.topoObjGet()
        Test_vlan_state_transition.dut01Obj = \
            Test_vlan_state_transition.topoObj.deviceObjGet(
                device="dut01")

    def teardown_class(cls):
        # Terminate all nodes
        cleanUp(cls.dut01Obj)
        Test_vlan_state_transition.topoObj.terminate_nodes()

    def test_add_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 1- Adding vlan")
        LogOutput('info', "############################################")
        # Add vlan 2
        if AddVlan(deviceObj=self.dut01Obj, vlanId=2).returnCode() != 0:
            LogOutput('error', "Failed to add vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding vlan " + str(2))

    def test_verify_vlan_stateDown(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Verify vlan state")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, pStatus="down") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan " + str(2))

    def test_addPort_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 3- Add port to vlan")
        LogOutput('info', "############################################")
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=2, interface=1, access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(2))

    def test_enable_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 4- Enable vlan")
        LogOutput('info', "############################################")
        if VlanStatus(deviceObj=self.dut01Obj, vlanId=2,
                      status=True).returnCode() != 0:
            LogOutput('error', "Failed to enable vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed enabling vlan " + str(2))

    def test_verify_vlan_stateUp(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 5- Verify vlan state")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, pStatus="up") != 0:
            LogOutput('error', "Failed to verify vlan state")
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan " + str(2))
