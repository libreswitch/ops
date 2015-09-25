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
###############################################################################
# Name:        dynamicLinkAggregation_noModSet.py
#
# Description: Tests that a previously configured dynamic Link Aggregation does
#              not stop forwarding traffic when the link is reconfigured with
#              the same initial settings. The current link should keep working
#              fine and the configuration retain the same settings
#
# Author:      Jose Calvo
#
# Topology:  |Host A| ---- |Switch A| ---------------- |Switch B| ---- |Host B|
#                                  (Dynamic LAG - 3 links)
#
# Success Criteria:  PASS -> Traffic flow between hosts is not stopped after
#                            applying dynamic LAG configuration and current
#                            configuration is not modified
#
#                    FAILED -> Traffic between hosts stops crossing the static
#                              LAG link or configuration changes, interfaces
#                              reset or any other unexpected behavior
#
###############################################################################

import pytest
import threading
from opstestfw.switch.CLI import *
from opstestfw import *

topoDict = {"topoExecution": 2000,
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut02:wrkston02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut01:dut02,\
                          lnk05:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}


def lag_createDynamic(dutA, dutB):
    devices = []
    devices.append(dutA)
    devices.append(dutB)
    for dev in devices:
        setCreate = lagCreation(
            deviceObj=dev,
            lagId=1,
            configFlag=True
        ).returnCode()
        setMode = lagMode(
            deviceObj=dev,
            lagId=1,
            lacpMode="active"
        ).returnCode()
        if setCreate != 0 or setMode != 0:
            return -1
        for i in range(2, 5):
            retCode = InterfaceLagIdConfig(
                deviceObj=dev,
                lagId=1,
                interface=i,
                enable=True
                ).returnCode()
            if retCode != 0:
                return retCode
    return 0


def ping_host(source):
    retStruct = source.Ping(ipAddr="192.168.1.11")
    if retStruct.returnCode() != 0:
        LogOutput('error', "Ping failed...\n")
        retCode = -1
    else:
        LogOutput('info', "Ping to 192.168.1.11... \n")
        packet_loss = retStruct.valueGet(key='packet_loss')
        if packet_loss != 0:
            LogOutput('error', "Packet Loss > 0%, lost" + str(packet_loss))
            retCode = -1
        else:
            LogOutput('info', "Success is 100%...\n")
            retCode = 0
    return retCode


def validateStep(code, step):
    if code != 0:
        raise Exception("Test case failed on step " + str(step) + "\n\n")


class trafficCheck (threading.Thread):
    def __init__(self, source):
        threading.Thread.__init__(self)
        self.host = source
        self.flag = True

    def run(self):
        i = 1
        while self.flag is True:
            LogOutput('info', "Ping: Try number " + str(i) + "\n\n")
            retCode = ping_host(self.host)
            try:
                validateStep(retCode, 7)
            except Exception as err:
                LogOutput('error', "TEST FAILED: " + str(err))
                self.flag = False
            i = i + 1

    def stop(self):
        self.flag = False


class Test_ft_framework_basics:
    def setup_class(cls):
        Test_ft_framework_basics.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_basics.topoObj =\
            Test_ft_framework_basics.testObj.topoObjGet()

    def teardown_class(cls):
        Test_ft_framework_basics.topoObj.terminate_nodes()

    def test_initializeDev(self):
        LogOutput('info', "#############################")
        LogOutput('info', "STEP 1 - INITIALIZING DEVICES\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut01Obj.Reboot()
        dut02Obj.Reboot()
        LogOutput('info', "\n        STEP 1 COMPLETE      ")
        LogOutput('info', "#############################")

    def test_setLinks(self):
        LogOutput('info', "\n")
        LogOutput('info', "#######################")
        LogOutput('info', "STEP 2 - ENABLING LINKS\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")

        LogOutput('info', "Configuring Switch A, Interface 1...")
        InterfaceEnable(
            deviceObj=dut01Obj,
            enable=True,
            interface=dut01Obj.linkPortMapping['lnk01']
        )
        LogOutput('info', "Configuring Switch A, Interface 2...")
        InterfaceEnable(
            deviceObj=dut01Obj,
            enable=True,
            interface=dut01Obj.linkPortMapping['lnk03']
        )
        LogOutput('info', "Configuring Switch A, Interface 3...")
        InterfaceEnable(
            deviceObj=dut01Obj,
            enable=True,
            interface=dut01Obj.linkPortMapping['lnk04']
        )
        LogOutput('info', "Configuring Switch A, Interface 4...")
        InterfaceEnable(
            deviceObj=dut01Obj,
            enable=True,
            interface=dut01Obj.linkPortMapping['lnk05']
        )
        LogOutput('info', "\nConfiguring Switch B, Interface 1...")
        InterfaceEnable(
            deviceObj=dut02Obj,
            enable=True,
            interface=dut02Obj.linkPortMapping['lnk02']
        )
        LogOutput('info', "Configuring Switch B, Interface 2...")
        InterfaceEnable(
            deviceObj=dut02Obj,
            enable=True,
            interface=dut02Obj.linkPortMapping['lnk03']
        )
        LogOutput('info', "Configuring Switch B, Interface 3...")
        InterfaceEnable(
            deviceObj=dut02Obj,
            enable=True,
            interface=dut02Obj.linkPortMapping['lnk04']
        )
        LogOutput('info', "Configuring Switch B, Interface 4...")
        InterfaceEnable(
            deviceObj=dut02Obj,
            enable=True,
            interface=dut02Obj.linkPortMapping['lnk05']
        )

        LogOutput('info', "\nConfiguring Host A IP Address")
        retCode = wrkston01Obj.NetworkConfig(
            ipAddr="192.168.1.10",
            netMask="255.255.255.0",
            broadcast="192.168.1.255",
            interface=wrkston01Obj.linkPortMapping['lnk01'],
            config=True
        ).returnCode()
        try:
            validateStep(retCode, 2)
        except Exception as err:
            LogOutput('error', "Host A: cannot set IP Address\n" + str(err))

        LogOutput('info', "\nConfiguring Host B IP Address")
        retCode = wrkston02Obj.NetworkConfig(
            ipAddr="192.168.1.11",
            netMask="255.255.255.0",
            broadcast="192.168.1.255",
            interface=wrkston02Obj.linkPortMapping['lnk02'],
            config=True
        ).returnCode()
        try:
            validateStep(retCode, 2)
        except Exception as err:
            LogOutput('error', "Host B: cannot set IP Address\n" + str(err))

        LogOutput('info', "\n        STEP 2 COMPLETE      ")
        LogOutput('info', "#############################")

    def test_setVlans(self):
        LogOutput('info', "\n")
        LogOutput('info', "#########################")
        LogOutput('info', "STEP 3 - CREATING VLAN 10\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retCode = VlanStatus(
            deviceObj=dut01Obj,
            vlanId=10,
            status=True
        ).returnCode()

        try:
            validateStep(retCode, 3)
        except Exception as err:
            LogOutput('error', "TEST FAILED: " + str(err))

        retCode = VlanStatus(
            deviceObj=dut02Obj,
            vlanId=10,
            status=True
        ).returnCode()

        try:
            validateStep(retCode, 3)
        except Exception as err:
            LogOutput('error', "TEST FAILED: " + str(err))

        LogOutput('info', "        STEP 3 COMPLETE      ")
        LogOutput('info', "#############################")

    def test_assignVlans(self):
        devices = []
        LogOutput('info', "\n")
        LogOutput('info', "########################################")
        LogOutput('info', "STEP 4 - ASSIGNING VLAN 10 TO INTERFACES\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devices.append(dut01Obj)
        devices.append(dut02Obj)
        for dev in devices:
            for i in range(1, 4):
                retCode = AddPortToVlan(
                    deviceObj=dev,
                    vlanId=10,
                    interface=i,
                    access=True
                ).returnCode()

                try:
                    validateStep(retCode, 4)
                except Exception as err:
                    LogOutput('error', "TEST FAILED: " + str(err))

        LogOutput('info', "        STEP 4 COMPLETE      ")
        LogOutput('info', "#############################")

    def test_createLag(self):
        LogOutput('info', "\n")
        LogOutput('info', "##################################")
        LogOutput('info', "STEP 5 - CREATING LINK AGGREGATION\n")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retCode = lag_createDynamic(dut01Obj, dut02Obj)
        try:
            validateStep(retCode, 5)
        except Exception as err:
            LogOutput('error', "TEST FAILED: " + str(err))

        LogOutput('info', "        STEP 5 COMPLETE      ")
        LogOutput('info', "#############################")

    def test_sendTraffic(self):
        LogOutput('info', "\n")
        LogOutput('info', "######################################")
        LogOutput('info', "STEP 6 - SENDING PACKETS BETWEEN HOSTS\n")
        host01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retCode = ping_host(host01Obj)

        try:
            validateStep(retCode, 6)
        except Exception as err:
            LogOutput('error', "TEST FAILED: " + str(err))

        LogOutput('info', "        STEP 6 COMPLETE      ")
        LogOutput('info', "#############################")

    def test_reapplyLagSend(self):
        LogOutput('info', "\n")
        LogOutput('info', "###################################")
        LogOutput('info', "STEP 7 - SEND TRAFFIC AND APPLY LAG\n")
        host01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        t = trafficCheck(host01Obj)
        t.start()
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        retCode = lag_createDynamic(dut01Obj, dut02Obj)
        try:
            validateStep(retCode, 7)
        except Exception as err:
            LogOutput('error', "TEST FAILED: " + str(err))

        t.stop()
        LogOutput('info', "       STEP 7 COMPLETE - TEST COMPLETE      ")
        LogOutput('info', "############################################")
