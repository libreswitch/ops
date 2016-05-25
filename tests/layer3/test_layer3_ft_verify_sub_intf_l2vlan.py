#!/usr/bin/env python

# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
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
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 ",
            "topoDevices": "dut01 wrkston01 wrkston02 wrkston03",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:wrkston02,\
                          lnk03:dut01:wrkston03",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation,\
                            wrkston03:system-category:workstation"}


def l3_route(**kwargs):
# pinging from host to host
    device1 = kwargs.get('device1', None)
    wrkstn1 = kwargs.get('device2', None)
    wrkstn2 = kwargs.get('device3', None)
    wrkstn3 = kwargs.get('device4', None)

    retStruct = InterfaceEnable(deviceObj = device1, enable = True,
                    interface=device1.linkPortMapping['lnk01'])
    retStruct = InterfaceEnable(deviceObj = device1, enable = True,
                    interface=device1.linkPortMapping['lnk01'] + ".10")

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = InterfaceEnable(deviceObj = device1, enable = True,
                                interface=device1.linkPortMapping['lnk02'])

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface IP address")
        assert(False)

    retStruct = InterfaceEnable(deviceObj = device1, enable = True,
                                interface=device1.linkPortMapping['lnk03'])

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)
    devIntReturn = device1.DeviceInteract(command = "vtysh")
    devIntReturn = device1.DeviceInteract(command = "conf t")
    devIntReturn = device1.DeviceInteract(command = "vlan 100")
    devIntReturn = device1.DeviceInteract(command = "no shutdown")
    devIntReturn = device1.DeviceInteract(command = "exit")
    devIntReturn = device1.DeviceInteract(command = "exit")
    devIntReturn = device1.DeviceInteract(command = "exit")

    devIntRetStruct1 = AddPortToVlan(deviceObj = device1,
                                     vlanId = 100,
                                     interface = device1.
                                     linkPortMapping['lnk02'],
                                     access = True,
                                     config = True)

    devIntRetStruct2 = AddPortToVlan(deviceObj = device1,
                                     vlanId = 100,
                                     interface = device1.
                                     linkPortMapping['lnk03'],
                                     access = True,
                                     config = True)

    if devIntRetStruct1.returnCode() != 0 \
       or devIntRetStruct2.returnCode() != 0:
        LogOutput('error',
                  "Failed to add vlan to port")
        assert(False)
    else:
        LogOutput('info', "Passed Adding Vlan to port")

    # configure Ip on the host
    retStructObj = wrkstn2.NetworkConfig(ipAddr = "172.168.1.2",
                                         netMask = "255.255.255.0",
                                         broadcast = "172.168.1.255",
                                         interface=wrkstn2.
                                         linkPortMapping['lnk02'],
                                         config = True)

    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")

    retStructObj = wrkstn3.NetworkConfig(ipAddr = "172.168.1.3",
                                         netMask = "255.255.255.0",
                                         broadcast = "172.168.1.255",
                                         interface = wrkstn3.
                                         linkPortMapping['lnk03'],
                                         config = True)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")
    LogOutput('info', "Pinging between workstation1 and dworkstation3")

    retStruct = wrkstn2.Ping(ipAddr = "172.168.1.3", packetCount=10)
    retCode = retStruct.returnCode()
    assert retCode == 0, "failed to ping Host3"

    LogOutput('info', "ping workstation 2 to workstation 3 return \
                       JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key = 'packet_loss')
    packets_sent = retStruct.valueGet(key = 'packets_transmitted')
    packets_received = retStruct.valueGet(key = 'packets_received')
    packets_error = retStruct.valueGet(key = 'packets_errors')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
    LogOutput('info', "Packet Errors:\t" + str(packets_error))
    assert packets_received > 1, "failed to ping Host3"

    # pinging from work statiosdd to switch 1
    retStruct = InterfaceIpConfig(deviceObj = device1,
                    interface=device1.linkPortMapping['lnk01'] + ".10",
                    addr = "192.168.1.1", mask = 24, config = True)

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = Dot1qEncapsulation(deviceObj = device1,
                    subInterface=device1.linkPortMapping['lnk01'] + ".10",
                                   dot1q=True, vlan=100, enable = True)

    # configure Ip on the host
    retCmdout = wrkstn1.DeviceInteract(command = "ip link add link " +
                                       wrkstn1.linkPortMapping['lnk01'] +
                                       " name eth1.100 type vlan id 100")
    retStructObj = wrkstn1.NetworkConfig(ipAddr = "192.168.1.2",
                                         netMask = "255.255.255.0",
                                         broadcast = "192.168.1.255",
                                         interface = "eth1.100")

    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")

    retStruct = wrkstn1.Ping(ipAddr = "192.168.1.1", packetCount=10)
    retCode = retStruct.returnCode()
    assert retCode == 0, "failed to ping switch"

    LogOutput('info', "IPv4 Ping from workstation 1 to switch 1 return \
                       JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key = 'packet_loss')
    packets_sent = retStruct.valueGet(key = 'packets_transmitted')
    packets_received = retStruct.valueGet(key = 'packets_received')
    packets_error = retStruct.valueGet(key = 'packets_errors')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
    LogOutput('info', "Packet Errors:\t" + str(packets_error))
    assert packets_received > 1, "failed to ping switch"

    # changing Vlan and verifying ping
    retStruct = Dot1qEncapsulation(deviceObj = device1,
                    subInterface=device1.linkPortMapping['lnk01'] + ".10",
                                   dot1q=True, vlan=200, enable = True)

    sleep(2)
    retStruct = wrkstn1.Ping(ipAddr = "192.168.1.1", packetCount=10)
    retCode = retStruct.returnCode()
    assert retCode != 0, "able to ping switch"
    LogOutput('info', "IPv4 Ping from workstation 1 to dut01 return JSON:\n" +
              str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key = 'packet_loss')
    packets_sent = retStruct.valueGet(key = 'packets_transmitted')
    packets_received = retStruct.valueGet(key = 'packets_received')
    packets_error = retStruct.valueGet(key = 'packets_errors')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
    LogOutput('info', "Packet Errors:\t" + str(packets_error))
    assert packets_received != packets_sent, "able to ping switch1"
    LogOutput('info', "Failed to ping switch\
                  Negative test case passed")

    # after removing dot1 encapsulation trying to ping host-switch
    retStruct = Dot1qEncapsulation(deviceObj = device1,
                    subInterface=device1.linkPortMapping['lnk01'] + ".10",
                                   dot1q = False, vlan = 200, enable = True)

    sleep(2)
    retStruct = wrkstn1.Ping(ipAddr = "192.168.1.1", packetCount = 10)
    retCode = retStruct.returnCode()
    assert retCode != 0, "failed to ping switch"

    LogOutput('info', "IPv4 Ping from workstation1 to switch 1 return \
                       JSON:\n" + str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key = 'packet_loss')
    packets_sent = retStruct.valueGet(key = 'packets_transmitted')
    packets_received = retStruct.valueGet(key = 'packets_received')
    packets_error = retStruct.valueGet(key = 'packets_errors')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
    LogOutput('info', "Packet Errors:\t" + str(packets_error))
    assert packets_received == 0, "able to ping switch"

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
        dut02Obj = self.topoObj.deviceObjGet(device = "wrkston01")
        wrkston1Obj = self.topoObj.deviceObjGet(device = "wrkston02")
        wrkston2Obj = self.topoObj.deviceObjGet(device = "wrkston03")
        retValue = l3_route(device1=dut01Obj, device2 = dut02Obj,
                            device3=wrkston1Obj, device4 = wrkston2Obj)
