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
from opstestfw.switch.CLI import *
from opstestfw import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01",
            "topoLinks": "lnk01:dut01:wrkston01",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation"}


# Independent functions called-used in main class
def verifyVlanState(dut, status, numberToFind):
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.valueGet(key=None)
    for dictionary in returnData:
        if dictionary['VLAN'] == numberToFind and \
                dictionary['Status'] == status:
            return 0
    return 1

# Verify a given vlan exists in the vlan table


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

# Verify a port has been assigned to a vlan


def verifyVlanPorts(dut, vlanID, port):
    assigned = False
    returnCLS = ShowVlan(deviceObj=dut)
    showVlanOutput = returnCLS.valueGet()
    for myDictionary in showVlanOutput:
        if myDictionary['VLAN'] == vlanID and \
                port in myDictionary['Interfaces']:
            assigned = True
            return assigned
    return assigned


def cleanUp(dut):
    LogOutput('info', "############################################")
    LogOutput('info', "Step 8- Clean up ")
    LogOutput('info', "############################################")
    if AddVlan(deviceObj=dut, vlanId=2,
               config=False).returnCode() != 0:
        LogOutput('error', "Failed to delete vlan " + str(2))
    else:
        LogOutput('info', "Passed vlan " + str(2) + " deleted")

    finalResult = []

    LogOutput('info', "\nCLEANUP - Reboot the switch")
    devRebootRetStruct = dut.Reboot()
    devRebootRetStruct = returnStruct(returnCode=0)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Failed to reboot Switch 1")
        finalResult.append(devRebootRetStruct.returnCode())
    else:
        LogOutput('info', "Passed Switch 1 Reboot piece")

    for i in finalResult:
        if not i:
            LogOutput('error', "Errors were detected while cleaning \
                    devices")
            return
    LogOutput('info', "Cleaned up devices")


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

    def test_add_vlans(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 1- Adding vlans")
        LogOutput('info', "############################################")
        # Add vlan 2
        if AddVlan(deviceObj=self.dut01Obj, vlanId=2).returnCode() != 0:
            LogOutput('error', "Failed to add vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding vlan " + str(2))

    def test_verifyConfVlans(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Verify vlan was configured ")
        LogOutput('info', "############################################")
        # Verify vlan 2
        if verifyVlan(self.dut01Obj, 2, 1) != 0:
            LogOutput('error',
                      "Failed to validate vlan {pVlan} configuration"
                      .format(pVlan="2"))
            assert(False)
        else:
            LogOutput('info', "Passed validating vlan " + str(2))

    def test_verify_vlan_stateDown(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 3- Verify vlan state")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, status="down",
                           numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan " + str(2))

    def test_addPort_vlans(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 4- Add port to vlans")
        LogOutput('info', "############################################")
        # Add port to vlan 2
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=2,
            interface=self.dut01Obj.linkPortMapping['lnk01'], access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(2))

    def test_added_ports(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 5- Verify ports assign correctly")
        LogOutput('info', "############################################")
        # Verify port 2
        if verifyVlanPorts(self.dut01Obj, 2,
                           self.dut01Obj.linkPortMapping['lnk01']) != 0:
            LogOutput('error', "Failed to verify port {pPort}".format(
                pPort=self.dut01Obj.linkPortMapping['lnk01']))
            assert(False)
        else:
            LogOutput('info', "Passed verifying port {pPort}".format(
                pPort=self.dut01Obj.linkPortMapping['lnk01']))

    def test_enable_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 6- Enable vlan")
        LogOutput('info', "############################################")
        if VlanStatus(deviceObj=self.dut01Obj, vlanId=2,
                      status=True).returnCode() != 0:
            LogOutput('error', "Failed to enable vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed enabling vlan " + str(2))

    def test_verify_vlan_stateUp(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 7- Verify vlan state")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, status="up",
                           numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan state")
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan " + str(2))
