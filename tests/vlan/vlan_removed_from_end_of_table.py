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
import opstestfw
import re
from opstestfw.switch.CLI import *
from opstestfw import testEnviron
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
                            wrkston03:system-category:workstation"}


def capture(**kwargs):
    deviceObj = kwargs.get('deviceObj', None)
    interface = kwargs.get('interface', "eth0")
    number = kwargs.get('number', 1)
    command = 'nmap -sP 10.1.1.1-254' + "\n"
    deviceObj.expectHndl.send(command)
    time.sleep(5)
    deviceObj.expectHndl.expect('#')
    result = re.findall('\(\d*\s\w*\s\w*\)', deviceObj.expectHndl.before)
    hostsNumber = re.findall('\d?', result[0])
    if hostsNumber[1] != number:
        return 1
    else:
        return 0

def cleanUp(dut):
    LogOutput('info', "############################################")
    LogOutput('info', "Step 8- CleanUp")
    LogOutput('info', "############################################")
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
        cleanUp(cls.dut01Obj)
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

    def test_enable_vlan(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 2- Enable vlans")
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
        LogOutput('info', "Step 3- Add ports to vlans")
        LogOutput('info', "############################################")
        # Add port 2 to vlan 2
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=2, interface=2, access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(2))
        # Add port 3 to vlan 3
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=3, interface=3, access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(3))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(3))
        # Add port 4 to vlan 4
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=4, interface=4, access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(4))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(4))

    def test_sendTraffic(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 4- Send traffic")
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
        if capture(deviceObj=self.wrkston01,
                   interface=self.wrkston01.linkPortMapping['lnk01'],
                   number='1') != 0:
            LogOutput('error', "Failed to send traffic")
            assert(False)
        else:
            LogOutput('info', 'Passed sending traffic and verifying')

    def test_delete_middle_vlan(self):
        LogOutput('info', "############################################")
        LogOutput(
            'info', "Step 5- Delete highest vlan value of VID from table")
        LogOutput('info', "############################################")
        # Delete last vlan in table
        if AddVlan(deviceObj=self.dut01Obj, vlanId=4,
                   config=False).returnCode() != 0:
            LogOutput('error', "Failed to delete vlan " + str(3))
            assert(False)
        else:
            LogOutput('info', "Passed delete vlan " + str(3))

    def test_ReAssign_Port(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 6- Re-assign port to vlan")
        LogOutput('info', "############################################")
        # Add port 4 to vlan 2
        returnStr = AddPortToVlan(
            deviceObj=self.dut01Obj, vlanId=2, interface=4, access=True,
            allowed=False, tag=False, config=True)
        if returnStr.returnCode() != 0:
            LogOutput('error', "Failed to add port to vlan " + str(2))
            assert(False)
        else:
            LogOutput('info', "Passed adding port to vlan " + str(2))

    def test_sendTraffic2(self):
        LogOutput('info', "############################################")
        LogOutput('info', "Step 7- Send traffic")
        LogOutput('info', "############################################")
        if capture(deviceObj=self.wrkston01,
                   interface=self.wrkston01.linkPortMapping['lnk01'],
                   number='2') != 0:
            LogOutput('error', "Failed to send traffic")
            assert(False)
        else:
            LogOutput('info', 'Passed sending traffic and verifying')

