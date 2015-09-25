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
# Description: With several vlans configured, bring one vlan up and
#              confirm its state, witch one port assigned to it verify
#              its Reason to ok, then issue the command to set the vlan
#              down and confirm its state. Only one vlan should see a
#              change in its state.
#
# Author:      Jose Pablo Araya
#
# Topology:       |Switch|
#
# Success Criteria:  PASS -> Just one of the vlans get the configuration
#                            perfomed
#
#                    FAILED -> If more than one vlan was configured with
#                              same options
#
##########################################################################

import pytest
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
def verifyVlanState(dut, status, numberToFind=1):
    LogOutput('info', "Validating vlan state")
    cont = 0
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.valueGet(key=None)
    for dictionary in returnData:
        print "VLAN STATE dictionary"
        print dictionary
        if dictionary['Status'] == status:
            cont = cont + 1
    if cont == numberToFind:
        return 0
    else:
        return 1


def verifyVlanReason(dut, pReason, numberToFind=1):
    LogOutput('info', "Validating vlan reason")
    cont = 0
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.valueGet(key=None)
    for dictionary in returnData:
        print "VLAN REASON dictionary"
        print dictionary
        if dictionary['Reason'] == pReason:
            cont = cont + 1
    if cont == numberToFind:
        return 0
    else:
        return 1

def cleanUp(dut):
    LogOutput('info', "############################################")
    LogOutput('info', "Step 11- CleanUp")
    LogOutput('info', "############################################")
    # Delete vlan 2
    if AddVlan(deviceObj=dut, vlanId=2,
               config=False).returnCode() != 0:
        LogOutput('error', "Failed to delete vlan " + str(2))
    else:
        LogOutput('info', "Passed delete vlan " + str(2))
    # Delete vlan 3 
    if AddVlan(deviceObj=dut, vlanId=3,
               config=False).returnCode() != 0:
        LogOutput('error', "Failed to delete vlan " + str(3))
    else:
        LogOutput('info', "Passed delete vlan " + str(3))
    # Delete vlan 4  
    if AddVlan(deviceObj=dut, vlanId=4,
               config=False).returnCode() != 0:
        LogOutput('error', "Failed to delete vlan " + str(4))
    else:
        LogOutput('info', "Passed delete vlan " + str(4))


class Test_vlan_state_reason_transition:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_vlan_state_reason_transition.testObj = \
            testEnviron(topoDict=topoDict)
        Test_vlan_state_reason_transition.topoObj = \
            Test_vlan_state_reason_transition.testObj.topoObjGet()
        Test_vlan_state_reason_transition.dut01Obj = \
            Test_vlan_state_reason_transition.topoObj.deviceObjGet(
                device="dut01")

    def teardown_class(cls):
        # Terminate all nodes
        cleanUp(cls.dut01Obj)
        Test_vlan_state_reason_transition.topoObj.terminate_nodes()

    def test_add_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 1- Adding vlans")
        LogOutput('info', "############################################")
        # Add vlan 2
        if AddVlan(deviceObj=self.dut01Obj, vlanId=2).returnCode() != 0:
            LogOutput('error', "Failed to add vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding vlan " + str(2))
        # Add vlan 3
        if AddVlan(deviceObj=self.dut01Obj, vlanId=3).returnCode() != 0:
            LogOutput('error', "Failed to add vlan " + str(3))
            assert(False)
        else:
            LogOutput('info', "Passed adding vlan " + str(3))
        # Add vlan 4
        if AddVlan(deviceObj=self.dut01Obj, vlanId=4).returnCode() != 0:
            LogOutput('error', "Failed to add vlan " + str(4))
            assert(False)
        else:
            LogOutput('info', "Passed adding vlan " + str(4))

    def test_enable_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Enable one of the configured vlans")
        LogOutput('info', "############################################")
        if VlanStatus(deviceObj=self.dut01Obj, vlanId=2,
                      status=True).returnCode() != 0:
            LogOutput('error', "Failed to enable vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed enabling vlan " + str(2))

    def test_verify_vlan_stateDown(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 3- Verify vlan state")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, status="down",
                           numberToFind=3) != 0:
            LogOutput('error', "Failed to verify vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan " + str(2))

    def test_verify_vlan_ReasonNoPort(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 4- Verify vlan reason")
        LogOutput('info', "############################################")
        if verifyVlanReason(dut=self.dut01Obj, pReason="no_member_port") != 0:
            LogOutput('error', "Failed to verify vlan reason ")
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan")

    def test_addPort_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 5- Add port to vlan")
        LogOutput('info', "############################################")
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=2, interface=1, access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(2))

    def test_verify_vlan_stateUp(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 6- Verify vlan state")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, status="up") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan " + str(2))

    def test_verify_vlan_ReasonOk(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 7- Verify vlan reason")
        LogOutput('info', "############################################")
        if verifyVlanReason(dut=self.dut01Obj, pReason="ok") != 0:
            LogOutput('error', "Failed to verify vlan reason ")
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan")

    def test_Disable_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 8- Disable vlan")
        LogOutput('info', "############################################")
        if VlanStatus(deviceObj=self.dut01Obj, vlanId=2,
                      status=False).returnCode() != 0:
            LogOutput('error', "Failed to disable vlan")
            assert(False)
        else:
            LogOutput('info', "Passed disabling vlan")

    def test_verify_vlan_stateDown2(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 9- Verify vlan state down")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, status="down",
                           numberToFind=3) != 0:
            LogOutput('error', "Failed to verify vlan" + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan" + str(2))

    def test_verify_vlan_ReasonDown(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 10- Verify vlan reason")
        LogOutput('info', "############################################")
        if verifyVlanReason(dut=self.dut01Obj, pReason="admin_down",
                            numberToFind=3) != 0:
            LogOutput('error', "Failed to verify vlan reason ")
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan")


