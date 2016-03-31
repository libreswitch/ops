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
import re
from opstestfw.switch.CLI import *
from opstestfw import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "wrkston01 wrkston02 dut01",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}


# Independent functions called-used in main class

def verifyVlanState(dut, status, numberToFind):
    LogOutput('info', "Verifying vlan state")
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.valueGet()
    for dictionary in returnData:
        if dictionary['VLAN'] == numberToFind and \
                dictionary['Status'] == status:
            return 0
    return 1


def verifyVlanReason(dut, pReason, numberToFind):
    LogOutput('info', "Verifying vlan reason")
    devRetStruct = ShowVlan(deviceObj=dut)
    returnData = devRetStruct.valueGet()
    for dictionary in returnData:
        if dictionary['VLAN'] == numberToFind and \
                dictionary['Reason'] == pReason:
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


def verifyPing(clientSource, destIPAddress):
    devRetStruct = clientSource.Ping(ipAddr=destIPAddress)
    if devRetStruct.returnCode() != 0:
        LogOutput('error', "Ping failed...\n")
        return False
    else:
        LogOutput('info', "Ping to " + destIPAddress + "... \n")
        packet_loss = devRetStruct.valueGet(key='packet_loss')
    if packet_loss != 0:
        LogOutput('error', "Packet Loss > 0%, lost " + str(packet_loss))
        return False
    else:
        LogOutput('info', "Success is 100%...\n")
    return True


def cleanUp(dut, wrkston01Obj, wrkston02Obj):
    LogOutput('info', "############################################")
    LogOutput('info', "Step 16- CleanUp")
    LogOutput('info', "############################################")
    finalResult = []
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

    LogOutput('info', "\nCLEANUP - Unconfiguring workstation 1")
    finalResult.append(unConfigureWorkstation(
        wrkston01Obj,
        wrkston01Obj.linkPortMapping['lnk01'], "192.168.30.10",
        "255.255.255.0", "192.168.30.255"))
    LogOutput('info', "\nCLEANUP - Unconfiguring workstation 2")
    finalResult.append(unConfigureWorkstation(
        wrkston02Obj,
        wrkston02Obj.linkPortMapping['lnk02'], "192.168.30.11",
        "255.255.255.0", "192.168.30.255"))

    LogOutput('info', "\nCLEANUP - Reboot the switches")
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


def unConfigureWorkstation(deviceObj, int, ipAddr, netMask, broadcast):
    retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                        netMask=netMask,
                                        broadcast=broadcast,
                                        interface=int, configFlag=False)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to unconfigure IP on workstation " +
                  deviceObj.device)
        return False
    cmdOut = deviceObj.cmd("ifconfig " + int)
    LogOutput('info', "Ifconfig info for workstation " +
              deviceObj.device + ":\n" + cmdOut)
    return True


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
        Test_vlan_state_reason_transition.wrkston01Obj = \
            Test_vlan_state_reason_transition.topoObj.deviceObjGet(
                device="wrkston01")
        Test_vlan_state_reason_transition.wrkston02Obj = \
            Test_vlan_state_reason_transition.topoObj.deviceObjGet(
                device="wrkston02")

    def teardown_class(cls):
        # Terminate all nodes
        cleanUp(cls.topoObj.deviceObjGet(device="dut01"),
                cls.topoObj.deviceObjGet(device="wrkston01"),
                cls.topoObj.deviceObjGet(device="wrkston02"))
        Test_vlan_state_reason_transition.topoObj.terminate_nodes()

    def test_initialize_clients(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 1- Configure workstations")
        LogOutput('info', "############################################")

        LogOutput('info', "\nConfiguring Host A IP Address")
        devRetStruct = self.wrkston01Obj.NetworkConfig(
            ipAddr="192.168.30.10",
            netMask="255.255.255.0",
            broadcast="192.168.30.255",
            interface=self.wrkston01Obj.linkPortMapping['lnk01'],
            config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Host A: cannot set IP Address\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Host A has been configured"
                      + " with an IP Address")

        LogOutput('info', "\nConfiguring Host B IP Address")
        devRetStruct = self.wrkston02Obj.NetworkConfig(
            ipAddr="192.168.30.11",
            netMask="255.255.255.0",
            broadcast="192.168.30.255",
            interface=self.wrkston02Obj.linkPortMapping['lnk02'],
            config=True)
        if devRetStruct.returnCode() != 0:
            LogOutput('error', "Host B: cannot set IP Address\n")
            assert devRetStruct.returnCode() == 0
        else:
            LogOutput('info', "Passed - Host B has been configured"
                      + "  with an IP Address")

    def test_add_vlans(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Adding vlans")
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

    def test_verifyConfVlans(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 3- Verify vlans were configured ")
        LogOutput('info', "############################################")
        # Verify vlan 2
        if verifyVlan(self.dut01Obj, 2, 1) != 0:
            LogOutput('error',
                      "Failed to validate vlan {pVlan} configuration"
                      .format(pVlan="2"))
            assert(False)
        else:
            LogOutput('info', "Passed validating vlan " + str(2))
        # Verify vlan 3
        if verifyVlan(self.dut01Obj, 3, 1) != 0:
            LogOutput('error',
                      "Failed to validate vlan {pVlan} configuration"
                      .format(pVlan="3"))
            assert(False)
        else:
            LogOutput('info', "Passed validating vlan " + str(3))
        # Verify vlan 4
        if verifyVlan(self.dut01Obj, 4, 1) != 0:
            LogOutput('error',
                      "Failed to validate vlan {pVlan} configuration"
                      .format(pVlan="4"))
            assert(False)
        else:
            LogOutput('info', "Passed validating vlan " + str(4))

    def test_verify_vlan_stateShutdown(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 4- Verify vlan status before enabling it")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, status="down",
                           numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2) + "status")
            assert(False)
        elif verifyVlanState(dut=self.dut01Obj, status="down",
                             numberToFind="3") != 0:
            LogOutput('error', "Failed to verify vlan " + str(3) + "status")
            assert(False)
        elif verifyVlanState(dut=self.dut01Obj, status="down",
                             numberToFind="4") != 0:
            LogOutput('error', "Failed to verify vlan " + str(4) + "status")
            assert(False)
        else:
            LogOutput('info', "Passed verifying all vlans status")

    def test_verify_vlan_ReasonShutdown(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 5- Verify vlan reason before enabling it")
        LogOutput('info', "############################################")
        if verifyVlanReason(dut=self.dut01Obj,
                            pReason="admin_down", numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2) + " reason")
            assert(False)
        elif verifyVlanReason(dut=self.dut01Obj,
                              pReason="admin_down", numberToFind="3") != 0:
            LogOutput('error', "Failed to verify vlan " + str(3) + " reason")
            assert(False)
        elif verifyVlanReason(dut=self.dut01Obj,
                              pReason="admin_down", numberToFind="4") != 0:
            LogOutput('error', "Failed to verify vlan " + str(4) + " reason")
            assert(False)
        else:
            LogOutput('info', "Passed verifying all vlans reason value")

    def test_enable_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 6- Enable one of the configured vlans")
        LogOutput('info', "############################################")
        if VlanStatus(deviceObj=self.dut01Obj, vlanId=2,
                      status=True).returnCode() != 0:
            LogOutput('error', "Failed to enable vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed enabling vlan " + str(2))

    def test_verify_vlan_stateNoShutdown(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 7- Verify vlan status")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, status="down",
                           numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2) + "status")
            assert(False)
        elif verifyVlanState(dut=self.dut01Obj, status="down",
                             numberToFind="3") != 0:
            LogOutput('error', "Failed to verify vlan " + str(3) + "status")
            assert(False)
        elif verifyVlanState(dut=self.dut01Obj, status="down",
                             numberToFind="4") != 0:
            LogOutput('error', "Failed to verify vlan " + str(4) + "status")
            assert(False)
        else:
            LogOutput('info', "Passed verifying all vlans status")

    def test_verify_vlan_ReasonNoShutdown(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 8- Verify vlan reason")
        LogOutput('info', "############################################")
        if verifyVlanReason(dut=self.dut01Obj,
                            pReason="no_member_port", numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2) + " reason")
            assert(False)
        elif verifyVlanReason(dut=self.dut01Obj,
                              pReason="admin_down", numberToFind="3") != 0:
            LogOutput('error', "Failed to verify vlan " + str(3) + " reason")
            assert(False)
        elif verifyVlanReason(dut=self.dut01Obj,
                              pReason="admin_down", numberToFind="4") != 0:
            LogOutput('error', "Failed to verify vlan " + str(4) + " reason")
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan")

    def test_addPort_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 9- Add port to vlan")
        LogOutput('info', "############################################")
        port = self.dut01Obj.linkPortMapping['lnk01']
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=2, interface=port, access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port " + port + " to vlan 2")
            assert(False)
        elif verifyVlanPorts(self.dut01Obj, "2", port):
            LogOutput('info', "Passed adding port " + port + " to vlan 2")
        else:
            LogOutput('error', "Failed to add port " + port + " to vlan 2")
            assert(False)

        port = self.dut01Obj.linkPortMapping['lnk02']
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=2, interface=port, access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port " + port + " to vlan 2")
            assert(False)
        elif verifyVlanPorts(self.dut01Obj, "2", port):
            LogOutput('info', "Passed adding port " + port + " to vlan 2")
        else:
            LogOutput('error', "Failed to add port " + port + " to vlan 2")
            assert(False)

    def test_verify_vlan_stateUp(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 10- Verify vlan status")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, status="up",
                           numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2) + "status")
            assert(False)
        elif verifyVlanState(dut=self.dut01Obj, status="down",
                             numberToFind="3") != 0:
            LogOutput('error', "Failed to verify vlan " + str(3) + "status")
            assert(False)
        elif verifyVlanState(dut=self.dut01Obj, status="down",
                             numberToFind="4") != 0:
            LogOutput('error', "Failed to verify vlan " + str(4) + "status")
            assert(False)
        else:
            LogOutput('info', "Passed verifying all vlans status")

    def test_verify_vlan_ReasonOk(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 11- Verify vlan reason")
        LogOutput('info', "############################################")
        if verifyVlanReason(dut=self.dut01Obj,
                            pReason="ok", numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2) + "reason ")
            assert(False)
        elif verifyVlanReason(dut=self.dut01Obj,
                              pReason="admin_down", numberToFind="3") != 0:
            LogOutput('error', "Failed to verify vlan " + str(3) + " reason")
            assert(False)
        elif verifyVlanReason(dut=self.dut01Obj,
                              pReason="admin_down", numberToFind="4") != 0:
            LogOutput('error', "Failed to verify vlan " + str(4) + " reason")
            assert(False)
        else:
            LogOutput('info', "Passed verifying vlan")

    def test_Disable_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 12- Disable vlan")
        LogOutput('info', "############################################")
        if VlanStatus(deviceObj=self.dut01Obj, vlanId=2,
                      status=False).returnCode() != 0:
            LogOutput('error', "Failed to disable vlan" + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed disabling vlan" + str(2))

    def test_verify_vlan_stateDown2(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 13- Verify vlan status down")
        LogOutput('info', "############################################")
        if verifyVlanState(dut=self.dut01Obj, status="down",
                           numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2) + "status")
            assert(False)
        elif verifyVlanState(dut=self.dut01Obj, status="down",
                             numberToFind="3") != 0:
            LogOutput('error', "Failed to verify vlan " + str(3) + "status")
            assert(False)
        elif verifyVlanState(dut=self.dut01Obj, status="down",
                             numberToFind="4") != 0:
            LogOutput('error', "Failed to verify vlan " + str(4) + "status")
            assert(False)
        else:
            LogOutput('info', "Passed verifying all vlans status")

    def test_verify_vlan_ReasonDown(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 14- Verify vlan reason")
        LogOutput('info', "############################################")
        if verifyVlanReason(dut=self.dut01Obj,
                            pReason="admin_down", numberToFind="2") != 0:
            LogOutput('error', "Failed to verify vlan " + str(2) + " reason")
            assert(False)
        elif verifyVlanReason(dut=self.dut01Obj,
                              pReason="admin_down", numberToFind="3") != 0:
            LogOutput('error', "Failed to verify vlan " + str(3) + " reason")
            assert(False)
        elif verifyVlanReason(dut=self.dut01Obj,
                              pReason="admin_down", numberToFind="4") != 0:
            LogOutput('error', "Failed to verify vlan " + str(4) + " reason")
            assert(False)
        else:
            LogOutput('info', "Passed verifying all vlans reason value")

    def test_ping_hosts(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 15- Verify ping between hosts")
        LogOutput('info', "############################################\n")
        LogOutput('info', "Ping between clients in vlan 2\n")
        ping = verifyPing(self.wrkston01Obj, destIPAddress="192.168.30.11")
        if ping is not False:
            LogOutput('error', "Client in wrkston01 shouldn't reach \
            " + " client in wrkston02\n")
            assert devRetStruct.returnCode() != 0
        else:
            LogOutput('info', "Passed - Ping between clients"
                      + " is unreachable on the disabled vlan\n")
