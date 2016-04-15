#!/usr/bin/env python

# Copyright(C) 2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0(the "License"); you may
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
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:dut02, \
                          lnk02:dut02:wrkston01, \
                          lnk03:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch, \
                            dut02:system-category:switch, \
                            wrkston01:system-category:workstation, \
                            wrkston02:system-category:workstation"}


def l3_route(**kwargs):
    device1 = kwargs.get('device1', None)
    device2 = kwargs.get('device2', None)
    wrkstn1 = kwargs.get('device3', None)
    wrkstn2 = kwargs.get('device4', None)

    retStruct = InterfaceEnable(deviceObj = device1, enable = True,
                                interface = device1.linkPortMapping['lnk01'])
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)
    retStruct = InterfaceIpConfig(deviceObj = device1,
                                  interface = device1.linkPortMapping['lnk01'],
                                  addr = "20.0.1.2", mask = 24, config = True)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)
    retStruct = InterfaceEnable(deviceObj = device1, enable = True,
                    interface = device1.linkPortMapping['lnk01'] + ".100")

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = InterfaceIpConfig(deviceObj = device1,
                    interface = device1.linkPortMapping['lnk01'] + ".100",
                    addr = "192.168.1.2", mask = 24, config = True)

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface Ip address ")
        assert(False)

    retStruct = Dot1qEncapsulation(deviceObj = device1,
                    subInterface = device1.linkPortMapping['lnk01'] + ".100",
                    dot1q = True, vlan = 100)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = InterfaceEnable(deviceObj = device1, enable = True,
                    interface = device1.linkPortMapping['lnk01'] + ".200")

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface IP address")
        assert(False)

    retStruct = InterfaceIpConfig(deviceObj = device1,
                    interface = device1.linkPortMapping['lnk01'] + ".200",
                    addr = "182.158.1.2", mask=24, config = True)

    retStruct = Dot1qEncapsulation(deviceObj = device1,
                    subInterface = device1.linkPortMapping['lnk01'] + ".200",
                    dot1q = True, vlan=200)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface Ip address ")
        assert(False)

    retStruct = InterfaceEnable(deviceObj = device2, enable = True,
                    interface = device2.linkPortMapping['lnk01'])

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)
    devIntReturn = device2.DeviceInteract(command="vtysh")
    devIntReturn = device2.DeviceInteract(command="conf t")
    devIntReturn = device2.DeviceInteract(command="vlan 100")
    devIntReturn = device2.DeviceInteract(command="no shutdown")
    devIntReturn = device2.DeviceInteract(command="vlan 200")
    devIntReturn = device2.DeviceInteract(command="no shutdown")
    devIntReturn = device2.DeviceInteract(command="exit")
    devIntReturn = device2.DeviceInteract(command="exit")
    devIntReturn = device2.DeviceInteract(command="exit")

    devIntRetStruct1 = AddPortToVlan(
            deviceObj = device2,
            vlanId = 100,
            interface = device2.linkPortMapping['lnk01'],
            allowed = True,
            config = True)

    devIntRetStruct2 = AddPortToVlan(
            deviceObj = device2,
            vlanId = 200,
            interface = device2.linkPortMapping['lnk01'],
            allowed = True,
            config = True)

    if devIntRetStruct1.returnCode() != 0 \
                or devIntRetStruct2.returnCode() != 0:
        LogOutput('error',
                      "Failed to add vlan to port")
        assert(False)
    else:
        LogOutput('info', "Passed Adding Vlan to port")

    retStruct = InterfaceEnable(deviceObj = device2, enable = True,
                    interface = device2.linkPortMapping['lnk02'])

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = InterfaceEnable(deviceObj = device2, enable = True,
                    interface = device2.linkPortMapping['lnk03'])

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    devIntRetStruct1 = AddPortToVlan(
            deviceObj = device2,
            vlanId = 100,
            interface = device2.linkPortMapping['lnk02'],
            access = True,
            config = True)
    devIntRetStruct2 = AddPortToVlan(
            deviceObj = device2,
            vlanId = 200,
            interface = device2.linkPortMapping['lnk03'],
            access = True,
            config = True)

    if devIntRetStruct1.returnCode() != 0 \
                or devIntRetStruct2.returnCode() != 0:
        LogOutput('error',
                      "Failed to configured vlan in the interface")
        assert(False)
    else:
        LogOutput('info', "Passed interface vlan configured")

    # configure Ip on the host
    retStructObj = wrkstn1.NetworkConfig(ipAddr = "192.168.1.1",
                netMask = "255.255.255.0",
                broadcast = "192.168.1.255",
                interface = wrkstn1.linkPortMapping['lnk02'],
                config = True)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")
    retCmdout = wrkstn1.DeviceInteract(command=
    "ip route add 182.158.1.0/24 via 192.168.1.2")

    retStructObj = wrkstn2.NetworkConfig(ipAddr = "182.158.1.1",
                netMask = "255.255.255.0",
                broadcast = "192.168.1.255",
                interface = wrkstn2.linkPortMapping['lnk03'],
                config = True)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")
    retCmdout = wrkstn2.DeviceInteract(command=
    "ip route add 192.168.1.0/24  via 182.158.1.2")
    LogOutput('info', "Pinging between workstation1 and dut01")

    retStruct = wrkstn1.Ping(ipAddr = "182.158.1.1", packetCount=10)
    retCode = retStruct.returnCode()
    assert retCode == 0, "failed to ping switch"

    LogOutput('info', "IPv4 Ping from workstation 1 to dut01 return JSON:\n" \
             + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
    assert packets_received >= 1 , "failed to ping switch"


def deviceCleanup(**kwargs):
    device1 = kwargs.get('device1', None)
    device2 = kwargs.get('device2', None)
    wrkstn1 = kwargs.get('device3', None)
    wrkstn2 = kwargs.get('device4', None)

    retStruct = InterfaceEnable(deviceObj = device1, enable=False,
                    interface = device1.linkPortMapping['lnk01'] + ".100")

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = InterfaceIpConfig(deviceObj = device1,
                    interface = device1.linkPortMapping['lnk01'] + ".100",
                    addr = "192.168.1.2", mask=24, config = False)

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface Ip address ")
        assert(False)

    retStruct = Dot1qEncapsulation(deviceObj = device1,
                    subInterface = device1.linkPortMapping['lnk01'] + ".100",
                    dot1q = False, vlan=100)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = InterfaceEnable(deviceObj = device1, enable=False,
                    interface = device1.linkPortMapping['lnk01'] + ".200")

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface IP address")
        assert(False)

    retStruct = InterfaceIpConfig(deviceObj = device1,
                    interface = device1.linkPortMapping['lnk01'] + ".200",
                    addr = "182.168.1.2", mask=24, config = False)

    retStruct = Dot1qEncapsulation(deviceObj = device1,
                    subInterface = device1.linkPortMapping['lnk01'] + ".200",
                    dot1q = False, vlan=200)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface Ip address ")
        assert(False)

    LogOutput('info', "vlan reconfiguring ")
    devVlanRetStruct1 = AddVlan(
                deviceObj = device2,
                vlanId = 100,
                config = False)

    devVlanRetStruct2 = AddVlan(
                deviceObj = device2,
                vlanId = 200,
                config = False)

    if devVlanRetStruct1.returnCode() != 0 \
                or devVlanRetStruct2.returnCode() != 0:
        LogOutput('error',
                      "Failed to add vlan")
        assert(False)
    else:
        LogOutput('info', "Passed Adding Vlan")

    devIntRetStruct1 = AddPortToVlan(
            deviceObj = device2,
            vlanId = 100,
            interface = device2.linkPortMapping['lnk01'],
            allowed = True,
            config = False)

    devIntRetStruct2 = AddPortToVlan(
            deviceObj = device2,
            vlanId = 200,
            interface = device2.linkPortMapping['lnk01'],
            allowed = True,
            config = False)

    if devIntRetStruct1.returnCode() != 0 \
                or devIntRetStruct2.returnCode() != 0:
        LogOutput('error',
                      "Failed to add vlan to port")
        assert(False)
    else:
        LogOutput('info', "Passed Adding Vlan to port")

    DevretStruct = InterfaceEnable(deviceObj = device2, enable=False,
                       interface = device2.linkPortMapping['lnk02'])

    if DevretStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    devIntRetStruct1 = AddPortToVlan(
            deviceObj = device2,
            vlanId = 100,
            interface = device2.linkPortMapping['lnk02'],
            access = True,
            config = False)
    retStruct = InterfaceEnable(deviceObj = device2, enable=False,
                    interface = device2.linkPortMapping['lnk03'])

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    devIntRetStruct2 = AddPortToVlan(
            deviceObj = device2,
            vlanId = 200,
            interface = device2.linkPortMapping['lnk03'],
            access = True,
            config = False)

    if devIntRetStruct1.returnCode() != 0 \
                or devIntRetStruct2.returnCode() != 0:
        LogOutput('error',
                      "Failed to configured vlan in the interface")
        assert(False)
    else:
        LogOutput('info', "Passed interface vlan configured")

    # configure Ip on the host
    retStructObj = wrkstn1.NetworkConfig(ipAddr = "192.168.1.1",
    netMask = "255.255.255.0", broadcast = "192.168.1.255",
    interface = wrkstn1.linkPortMapping['lnk02'], config = False)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")

    retStructObj = wrkstn2.NetworkConfig(ipAddr = "182.168.1.1",
                netMask = "255.255.255.0",
                broadcast = "192.168.1.255",
                interface = wrkstn2.linkPortMapping['lnk03'],
                config = False)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")
    LogOutput('info', "Pinging between workstation1 and dut01")

@pytest.mark.skipif(True, reason="skipped test case due to random gate job failures.")
class Test_subInt:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_subInt.testObj = testEnviron(topoDict=topoDict)
        # Get topology object
        Test_subInt.topoObj = Test_subInt.testObj.topoObjGet()

    def teardown_class(cls):
        Test_subInt.topoObj.terminate_nodes()

    def test_l3_route(self):
        dut01Obj = self.topoObj.deviceObjGet(device = "dut01")
        dut02Obj = self.topoObj.deviceObjGet(device = "dut02")
        wrkston1Obj = self.topoObj.deviceObjGet(device = "wrkston01")
        wrkston2Obj = self.topoObj.deviceObjGet(device = "wrkston02")
        retValue = l3_route(device1 = dut01Obj, device2 = dut02Obj,
                            device3 = wrkston1Obj, device4 = wrkston2Obj)

    def test_deviceCleanup(self):
        LogOutput('info', "Reverting the configuration")
        dut01Obj = self.topoObj.deviceObjGet(device = "dut01")
        dut02Obj = self.topoObj.deviceObjGet(device = "dut02")
        wrkston1Obj = self.topoObj.deviceObjGet(device = "wrkston01")
        wrkston2Obj = self.topoObj.deviceObjGet(device = "wrkston02")
        retValue = deviceCleanup(device1 = dut01Obj, device2 = dut02Obj,
                                device3 = wrkston1Obj, device4 = wrkston2Obj)
