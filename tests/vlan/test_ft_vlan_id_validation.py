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
# Description: Verify that a VID out of the 802.1Q range or reserved VID
#              cannot be set and
#              also verifies that a VID which already exists cannot not
#              be set again.
#
# Author:      Jose Pablo Araya
#
# Topology:       |Switch|
#
# Success Criteria:  PASS -> Vlan out of range and repeated not configured
#
#                    FAILED -> Vlan out of range or repeated were configured
#
##########################################################################

import pytest
import re
from opstestfw.switch.CLI import *
from opstestfw import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01",
            "topoFilters": "dut01:system-category:switch"}

# Independent functions called-used in main class


def verifyInvalidVlan(dut, pVlan):
    LogOutput('info', "Validating invalid vlan")
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.valueGet(key=None)
    cont = 0
    for dictionary in returnData:
        if dictionary['VLAN'] == str(pVlan):
            cont = cont + 1
    if cont == 0:
        return 0
    else:
        return 1


def verifyVlan(dut, pVlan, pQuantity=0):
    LogOutput('info', "Validating vlan")
    cont = 0
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.buffer()
    vlans = re.findall('VLAN[0-9]*', returnData)
    for vlan in vlans:
        if vlan == "VLAN" + str(pVlan):
            cont = cont + 1
    if cont == pQuantity:
        return 0
    else:
        return 1


def cleanUp(dut):
    LogOutput('info', "############################################")
    LogOutput('info', "Step 7- Clean up ")
    LogOutput('info', "############################################")
    if AddVlan(deviceObj=dut, vlanId=2,
               config=False).returnCode() != 0:
        LogOutput('error', "Failed to delete vlan " + str(2))
    else:
        LogOutput('info', "Passed vlan " + str(2) + " deleted")


def tryInvalidVlan(dut):
    LogOutput('info', "Try adding invalid vlan ")
    if AddVlan(deviceObj=dut, vlanId=4095).returnCode() != 3:
        return 1
    # Verify invalid vlan was not configured
    if verifyInvalidVlan(dut, 4095) != 0:
        return 1
    else:
        return 0


class Test_vlan_Id_Validation:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_vlan_Id_Validation.testObj = testEnviron(topoDict=topoDict)
        Test_vlan_Id_Validation.topoObj = \
            Test_vlan_Id_Validation.testObj.topoObjGet()
        Test_vlan_Id_Validation.dut01Obj = \
            Test_vlan_Id_Validation.topoObj.deviceObjGet(
                device="dut01")

    def teardown_class(cls):
        # Terminate all nodes
        cleanUp(dut=cls.dut01Obj)
        Test_vlan_Id_Validation.topoObj.terminate_nodes()

    def test_invalid_vlan_add(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 1- Invalid vlan not configured")
        LogOutput('info', "############################################")
        if tryInvalidVlan(self.dut01Obj) != 0:
            LogOutput('error',
                      "Failed Invalid vlan configuration " + str(4095))
            assert(False)
        else:
            LogOutput('info', "Passed invalid vlan not added " + str(4095))

    def test_verifyNonVlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Verify no previous vlans are configured ")
        LogOutput('info', "############################################")
        if verifyVlan(self.dut01Obj, 2) != 0:
            LogOutput('error', "Failed to validate previous vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed validating previous vlan " + str(2))

    def test_vlan_add(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 3- Add vlan")
        LogOutput('info', "############################################")
        if AddVlan(deviceObj=self.dut01Obj, vlanId=2).returnCode() != 0:
            LogOutput('error', "Failed to add vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding vlan " + str(2))

    def test_verifyConfVlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 4- Verify vlan was configured ")
        LogOutput('info', "############################################")
        if verifyVlan(self.dut01Obj, 2, 1) != 0:
            LogOutput('error',
                      "Failed to validate vlan {pVlan} configuration"
                      .format(pVlan="2"))
            assert(False)
        else:
            LogOutput('info', "Passed validating vlan " + str(2))

    def test_repeated_vlan_add(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 5- Try to add repeated vlan")
        LogOutput('info', "############################################")
        if AddVlan(deviceObj=self.dut01Obj, vlanId=2).returnCode() != 0:
            LogOutput('error', "Failed to try add repeated vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed try adding repeated vlan " + str(2))

    def test_verifyRepeatedVlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 6- Validate vlan repeated not configured ")
        LogOutput('info', "############################################")
        if verifyVlan(self.dut01Obj, 2, 1) != 0:
            LogOutput('error', "Failed to validate repeated vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed validating repeated vlan " + str(2))
