#!/usr/bin/env python

# Copyright (C) 2015-2016 Hewlett Packard Enterprise Development LP)
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
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01",
            "topoLinks": "lnk01:dut01:wrkston01",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation"}


interface_loopback_id = "10"
# Hardcode loopback interface, interface ID not valid for all platforms


def loopback_l3(**kwargs):
    switch = kwargs.get('device1', None)
    wrkstn = kwargs.get('device2', None)

    LogOutput('info', "Loopback l3 reachability test")
    retStruct = LoopbackInterfaceEnable(deviceObj=switch,
                                        loopback=interface_loopback_id, addr="192.168.1.5",
                                        mask=24, config=True, enable=True)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface IP address")
        assert(False)

    retStruct = InterfaceEnable(deviceObj=switch, enable=True,
                                interface = switch.linkPortMapping['lnk01'] )

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enable interface")
        assert(False)

    retStruct = InterfaceIpConfig(deviceObj=switch,
                                  interface = switch.linkPortMapping['lnk01'],
                                  addr="192.168.2.1", mask=24, config=True)

    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to configure interface Ip address ")
        assert(False)

    # configure Ip on the host
    retStructObj = wrkstn.NetworkConfig(ipAddr="192.168.2.3",
                                        netMask="255.255.255.0",
                                        broadcast="192.168.1.255",
                                        interface=
                                        wrkstn.linkPortMapping['lnk01'],
                                        config=True)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")

    retCmdout = wrkstn.DeviceInteract(command=
                                      "ip route add 192.168.1.0/24 via \
                                       192.168.2.1")
    LogOutput('info', "Pinging between workstation1 and dut01")

    retStruct = wrkstn.Ping(ipAddr="192.168.1.5", packetCount=10)
    retCode = retStruct.returnCode()
    assert retCode == 0, "failed to ping switch"
    LogOutput('info', "IPv4 Ping from workstation 1 to dut01 return JSON:\n" +
              str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))


def negative_l3_reach(**kwargs):
    switch = kwargs.get('device1', None)
    wrkstn = kwargs.get('device2', None)

    LogOutput('info', "Loopback negative l3 reachability test")
    retStruct = LoopbackInterfaceEnable(deviceObj=switch,
                                        loopback=interface_loopback_id,
                                        enable=False)
    LogOutput('info', "Pinging between workstation1 and dut01 ")

    retStruct = wrkstn.Ping(ipAddr="192.168.1.5", packetCount=10)
    retCode = retStruct.returnCode()
    if retCode == 0:
        LogOutput('info', "failed to ping switch")
    LogOutput('info', "IPv4 Ping from workstation 1 to dut01 return JSON:\n" +
              str(retStruct.retValueString()))

    packet_loss = retStruct.valueGet(key='packet_loss')
    packets_sent = retStruct.valueGet(key='packets_transmitted')
    packets_received = retStruct.valueGet(key='packets_received')
    LogOutput('info', "Packets Sent:\t" + str(packets_sent))
    LogOutput('info', "Packets Recv:\t" + str(packets_received))
    LogOutput('info', "Packet Loss %:\t" + str(packet_loss))

    if retStruct.returnCode() != 0:
        LogOutput('info', "Failed to ping loopback.\
                  Negative test case passed")

    retStructObj = wrkstn.NetworkConfig(ipAddr="192.168.2.3",
                                        netMask="255.255.255.0",
                                        broadcast="192.168.1.255",
                                        interface=
                                        wrkstn.linkPortMapping['lnk01'],
                                        config=False)
    if retStructObj.returnCode() != 0:
        LogOutput('error', "Failed to configure IP on workstation")


class Test_loopback:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_loopback.testObj = testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_loopback.topoObj = Test_loopback.testObj.topoObjGet()

    def teardown_class(cls):
        Test_loopback.topoObj.terminate_nodes()

    def test_loopback_l3_reach(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkstonObj = self.topoObj.deviceObjGet(device="wrkston01")
        retValue = loopback_l3(device1=dut01Obj, device2=wrkstonObj)

    def test_negative_l3_reach(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkstonObj = self.topoObj.deviceObjGet(device="wrkston01")
        retValue = negative_l3_reach(device1=dut01Obj, device2=wrkstonObj)
