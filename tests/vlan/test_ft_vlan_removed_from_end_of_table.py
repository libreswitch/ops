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
# Description: Verify the functionality of deleting a VLAN and reasigned
#              port to another vlan. The Vlan will be deleted from the
#              end of the VLAN list table.
#              No traffic should pass through other vlans.
#
# Author:      Jose Pablo Araya
#
# Topology:       |workStation|-------|Switch|-------|workStation|
#                                        |
#                                        |
#                                        |
#                                  |workStation|
#
# *Requeriments: workStations must have nmap installed
#
# Success Criteria:  PASS -> Vlans is correctly delete it without affecting
#                            the others
#
#                    FAILED -> If other vlans are affected
#
##########################################################################

import pytest
import re
from opstestfw.switch.CLI import *
from opstestfw import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02 wrkston03",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02,\
            lnk03:dut01:wrkston03",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation,\
                            wrkston03:system-category:workstation,\
                            wrkston01:docker-image: openswitch/ubuntutest"}

# Send broadcast traffic through nmap signal tool


def capture(deviceObj, interface="eth0", number=1):
    command = 'nmap -sP 10.1.1.1-254' + "\n"
    # Adding a delay of 2 sec so as all the workstations and links are ready
    time.sleep(2)
    deviceObj.expectHndl.send(command)
    # time to run the nmap command
    time.sleep(5)
    deviceObj.expectHndl.expect('#')
    result = re.findall('\(\d*\s\w*\s\w*\)', deviceObj.expectHndl.before)
    hostsNumber = re.findall('\d?', result[0])
    if hostsNumber[1] != number:
        LogOutput('error', str(deviceObj.expectHndl.before))
        return 1
    else:
        return 0

# Verify if vlan exists or not


def verifyVlan(dut, pVlan, pQuantity=0):
    LogOutput('info', "Validating invalid vlan")
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


def cleanUp(dut, wrk1, wrk2, wrk3):
    LogOutput('info', "############################################")
    LogOutput('info', "Step 13- CleanUp")
    LogOutput('info', "############################################")
    LogOutput('info', "\nCleanUp - Unconfiguring workstation 1")
    wrk1.NetworkConfig(
        interface=wrk1.linkPortMapping['lnk01'],
        ipAddr="10.1.1.5", netMask="255.255.255.0",
        broadcast="10.1.1.255", config=False)
    LogOutput('info', "\nCleanUp - Unconfiguring workstation 2")
    wrk2.NetworkConfig(
        interface=wrk2.linkPortMapping['lnk02'],
        ipAddr="10.1.1.6", netMask="255.255.255.0",
        broadcast="10.1.1.255", config=False)
    LogOutput('info', "\nCleanUp - Unconfiguring workstation 3")
    wrk3.NetworkConfig(
        interface=wrk3.linkPortMapping['lnk03'],
        ipAddr="10.1.1.7", netMask="255.255.255.0",
        broadcast="10.1.1.255", config=False)
    LogOutput('info', "\nCleanUp - Reboot the Switch")
    devRebootRetStruct = dut.Reboot()
    devRebootRetStruct = returnStruct(returnCode=0)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Failed to reboot Switch")
        finalResult.append(devRebootRetStruct.returnCode())
    else:
        LogOutput('info', "Passed Switch Reboot piece")

class Test_vlan_state_removed_from_end_of_table:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_vlan_state_removed_from_end_of_table.testObj = \
            testEnviron(
                topoDict=topoDict)
        Test_vlan_state_removed_from_end_of_table.topoObj = \
            Test_vlan_state_removed_from_end_of_table.testObj.topoObjGet()
        Test_vlan_state_removed_from_end_of_table.dut01Obj = \
            Test_vlan_state_removed_from_end_of_table.topoObj.deviceObjGet(
                device="dut01")
        Test_vlan_state_removed_from_end_of_table.wrkston01 = \
            Test_vlan_state_removed_from_end_of_table.topoObj.deviceObjGet(
                device="wrkston01")
        Test_vlan_state_removed_from_end_of_table.wrkston02 = \
            Test_vlan_state_removed_from_end_of_table.topoObj.deviceObjGet(
                device="wrkston02")
        Test_vlan_state_removed_from_end_of_table.wrkston03 = \
            Test_vlan_state_removed_from_end_of_table.topoObj.deviceObjGet(
                device="wrkston03")

    def teardown_class(cls):
        # Terminate all nodes
        cleanUp(cls.dut01Obj, cls.wrkston01, cls.wrkston02, cls.wrkston03)
        Test_vlan_state_removed_from_end_of_table.topoObj.terminate_nodes()

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
        LogOutput('info', "Step 2- Verify vlans were configured ")
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

    def test_enable_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 3- Enable vlans")
        LogOutput('info', "############################################")
        # Enable vlan 2
        if VlanStatus(deviceObj=self.dut01Obj,
                      vlanId=2, status=True).returnCode() != 0:
            LogOutput('error', "Failed to enable vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed enabling vlan " + str(2))
        # Enable vlan 3
        if VlanStatus(deviceObj=self.dut01Obj,
                      vlanId=3, status=True).returnCode() != 0:
            LogOutput('error', "Failed to enable vlan " + str(3))
            assert(False)
        else:
            LogOutput('info', "Passed enabling vlan " + str(3))
        # Enable vlan 4
        if VlanStatus(deviceObj=self.dut01Obj,
                      vlanId=4, status=True).returnCode() != 0:
            LogOutput('error', "Failed to enable vlan " + str(4))
            assert(False)
        else:
            LogOutput('info', "Passed enabling vlan " + str(4))

    def test_addPort_vlans(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 4- Add ports to vlans")
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
        # Add port to vlan 3
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=3,
            interface=self.dut01Obj.linkPortMapping['lnk02'], access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(3))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(3))
        # Add port to vlan 4
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=4,
            interface=self.dut01Obj.linkPortMapping['lnk03'], access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(4))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(4))

    def test_enable_interfaces(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 5- Enable interfaces")
        LogOutput('info', "############################################")
        # Enable interface - lnk01
        returnStr = InterfaceEnable(
            deviceObj=self.dut01Obj,
            interface=self.dut01Obj.linkPortMapping['lnk01'], enable=True,)
        if returnStr.returnCode() != 0:
            LogOutput('error',
                      "Failed to enable interface {pInterface}".format(
                          pInterface=self.dut01Obj.linkPortMapping['lnk01']))
            assert(False)
        else:
            LogOutput('info',
                      "Passed enable interface {pInterface}".format(
                          pInterface=self.dut01Obj.linkPortMapping['lnk01']))
        # Enable interface - lnk02
        returnStr = InterfaceEnable(
            deviceObj=self.dut01Obj,
            interface=self.dut01Obj.linkPortMapping['lnk02'], enable=True,)
        if returnStr.returnCode() != 0:
            LogOutput('error',
                      "Failed to enable interface {pInterface}".format(
                          pInterface=self.dut01Obj.linkPortMapping['lnk02']))
            assert(False)
        else:
            LogOutput('info',
                      "Passed enable interface {pInterface}".format(
                          pInterface=self.dut01Obj.linkPortMapping['lnk02']))
        # Enable interface - lnk03
        returnStr = InterfaceEnable(
            deviceObj=self.dut01Obj,
            interface=self.dut01Obj.linkPortMapping['lnk03'], enable=True,)
        if returnStr.returnCode() != 0:
            LogOutput('error',
                      "Failed to enable interface {pInterface}".format(
                          pInterface=self.dut01Obj.linkPortMapping['lnk03']))
            assert(False)
        else:
            LogOutput('info', "Passed enable interface {pInterface}".format(
                pInterface=self.dut01Obj.linkPortMapping['lnk03']))
    def test_added_ports(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 6- Verify ports assign correctly")
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
        # Verify port 3
        if verifyVlanPorts(self.dut01Obj, 3,
                           self.dut01Obj.linkPortMapping['lnk02']) != 0:
            LogOutput('error', "Failed to verify port {pPort}".format(
                pPort=self.dut01Obj.linkPortMapping['lnk02']))
            assert(False)
        else:
            LogOutput('info', "Passed verifying port {pPort}".format(
                pPort=self.dut01Obj.linkPortMapping['lnk02']))
        # Verify port 4
        if verifyVlanPorts(self.dut01Obj, 4,
                           self.dut01Obj.linkPortMapping['lnk03']) != 0:
            LogOutput('error', "Failed to verify port {pPort}".format(
                pPort=self.dut01Obj.linkPortMapping['lnk03']))
            assert(False)
        else:
            LogOutput('info', "Passed verifying port {pPort}".format(
                pPort=self.dut01Obj.linkPortMapping['lnk03']))

    def test_sendTraffic(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 7- Send traffic")
        LogOutput('info', "############################################")
        self.wrkston01.NetworkConfig(
            interface=self.wrkston01.linkPortMapping['lnk01'],
            ipAddr="10.1.1.5", netMask="255.255.255.0",
            broadcast="10.1.1.255", config=True)
        self.wrkston02.NetworkConfig(
            interface=self.wrkston02.linkPortMapping['lnk02'],
            ipAddr="10.1.1.6", netMask="255.255.255.0",
            broadcast="10.1.1.255", config=True)
        self.wrkston03.NetworkConfig(
            interface=self.wrkston03.linkPortMapping['lnk03'],
            ipAddr="10.1.1.7", netMask="255.255.255.0",
            broadcast="10.1.1.255", config=True)
        if capture(self.wrkston01,
                   self.wrkston01.linkPortMapping['lnk01'], '1') != 0:
            LogOutput('error', "Failed to send traffic")
            assert(False)
        else:
            LogOutput('info', 'Passed sending traffic and verifying')

    def test_delete_end_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 8- Delete highest vlan from table")
        LogOutput('info', "############################################")
        # Delete last vlan in table
        if AddVlan(deviceObj=self.dut01Obj, vlanId=4,
                   config=False).returnCode() != 0:
            LogOutput('error', "Failed to delete vlan " + str(4))
            assert(False)
        else:
            LogOutput('info', "Passed delete vlan " + str(4))

    def test_deleted_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 9- Verify vlan was deleted ")
        LogOutput('info', "############################################")
        if verifyVlan(self.dut01Obj, 4) != 0:
            LogOutput('error',
                      "Failed to validate vlan {pVlan} was deleted"
                      .format(pVlan="4"))
            assert(False)
        else:
            LogOutput('info', "Passed validating deleted vlan {pVlan}"
                              .format(pVlan="4"))

    def test_reAssign_port(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 10- Re-assign port to other vlan")
        LogOutput('info', "############################################")
        # Add port 4 to vlan 2
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=2,
            interface=self.dut01Obj.linkPortMapping['lnk03'], access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(2))
    def test_added_port(self):
        LogOutput('info', "############################################")
        LogOutput(
            'info', "Step 11- Verify ports re-assign correctly")
        LogOutput('info', "############################################")
        # Verify port assigned to vlan 2
        if verifyVlanPorts(self.dut01Obj, 2,
                           self.dut01Obj.linkPortMapping['lnk03']) != 0:
            LogOutput('error', "Failed to verify port {pPort}".format(
                pPort=self.dut01Obj.linkPortMapping['lnk03']))
            assert(False)
        else:
            LogOutput('info', "Passed verifying port {pPort}".format(
                pPort=self.dut01Obj.linkPortMapping['lnk03']))

    def test_sendTraffic_after(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 12- Send traffic")
        LogOutput('info', "############################################")
        if capture(self.wrkston01,
                   self.wrkston01.linkPortMapping['lnk01'], '2') != 0:
            LogOutput('error', str(ShowVlan(deviceObj=self.dut01Obj).buffer()))
            LogOutput('error', "Failed to send traffic")
            assert(False)
        else:
            LogOutput('info', 'Passed sending traffic and verifying')
