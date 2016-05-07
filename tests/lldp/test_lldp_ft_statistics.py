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

from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch, \
                 dut02:system-category:switch"}


def lldp_statistics(**kwargs):
    device1 = kwargs.get('device1', None)
    device2 = kwargs.get('device2', None)

    # Setting tx time to 5 sec on SW1 and SW2
    # Entering vtysh SW1
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    # Setting tx time to 5 seconds on SW1
    LogOutput('info', "\nConfiguring transmit time of 5 sec on SW1")
    devIntRetStruct = device1.DeviceInteract(command="lldp timer 5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to set transmit time"

    # Entering vtysh SW2
    retStruct = device2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to get vtysh prompt"

    # Entering config terminal SW2
    devIntRetStruct = device2.ConfigVtyShell(enter=True)
    retCode = devIntRetStruct.returnCode()
    assert retCode == 0, "\nFailed to enter config mode"

    # Setting tx time to 5 seconds on SW2
    LogOutput('info', "\nConfiguring transmit time of 5 sec on SW2")
    devIntRetStruct = device2.DeviceInteract(command="lldp timer 5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "\nFailed to configure transmit time"

    # Exiting Config terminal SW1
    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting Config terminal SW2
    retStruct = device2.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    # Exiting vtysh terminal SW1
    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Exiting vtysh terminal SW2
    retStruct = device2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    # Enabling interface 1 SW1
    LogOutput('info', "Enabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True,
                                interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enabling interafce on SW1"

    # Enabling interface 1 SW2
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True,
                                interface=device2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to enable interface on SW2"

    # Configuring lldp on SW1
    LogOutput('info', "\n\n\nConfig lldp on SW1")
    retStruct = LldpConfig(deviceObj=device1, enable=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Unable to configure LLDP on SW1"

    # Configuring lldp on SW2
    LogOutput('info', "\n\n\nConfig lldp on SW2")
    retStruct = LldpConfig(deviceObj=device2, enable=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Configure lldp on SW2"

    # Waiting for neighbour entry to flood
    Sleep(seconds=10, message="\nWaiting")

    # Verify the transmitted and received packets
    LogOutput('info', "\nShowing LLDP statistics on SW1")
    device1.setDefaultContext(context="linux")
    tx_packets_cnt = 0
    rx_packets_cnt = 0
    stats_updated = False

    for retry in range(1, 10):
        retStruct = ShowLldpStatistics(deviceObj=device1)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show lldp statistics"

        retStruct.valueGet(key='globalStats')
        Global = retStruct.valueGet(key='globalStats')

        rx_packets_cnt = int(Global['Total_Packets_Received'])
        tx_packets_cnt = int(Global['Total_Packets_Transmitted'])

        if (rx_packets_cnt == 0 or tx_packets_cnt == 0):
            LogOutput('info', "\n\n\n lldp on statistics not updated")
            Sleep(seconds=5, message="\nWaiting")
            continue

        Sleep(seconds=15, message="\nWaiting to send more packets")

        retStruct = ShowLldpStatistics(deviceObj=device1)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Failed to show lldp statistics"

        retStruct.valueGet(key='globalStats')
        Global = retStruct.valueGet(key='globalStats')
        LogOutput('info', "\nTotal Packets Received: " +
                  str(Global['Total_Packets_Received']))
        LogOutput('info', "\nTotal Packets Transmitted: " +
                  str(Global['Total_Packets_Transmitted']))

        if (int(Global['Total_Packets_Received']) >= (rx_packets_cnt + 1) and
                int(Global['Total_Packets_Transmitted']) >= (tx_packets_cnt + 1)):
            stats_updated = True
            break

    # end loop

    if stats_updated is False:
        LogOutput('info', "Didn't Update LLDP Tx/Rx statistics")
        # Dump Device1
        LogOutput('info', "Device1 DUMP:")
        device1.setDefaultContext(context="linux")
        devCmd = "ovs-vsctl list interface "\
        + str(device1.linkPortMapping['lnk01'])
        neighbor_output = device1.cmd(devCmd)
        opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                    + str(neighbor_output))
        devCmd = "ip netns exec swns ifconfig "\
        + str(device1.linkPortMapping['lnk01'])
        ifconfig_output = device1.cmd(devCmd)
        opstestfw.LogOutput('info', devCmd + " output\n"
                    + str(ifconfig_output))

        # Dump Device2
        LogOutput('info', "Device2 DUMP")
        device2.setDefaultContext(context="linux")
        devCmd = "ovs-vsctl list interface "\
        + str(device2.linkPortMapping['lnk01'])
        neighbor_output = device2.cmd(devCmd)
        opstestfw.LogOutput('info', "ovs-vsctl list interface output:\n"
                    + str(neighbor_output))
        devCmd = "ip netns exec swns ifconfig "\
        + str(device2.linkPortMapping['lnk01'])
        ifconfig_output = device2.cmd(devCmd)
        opstestfw.LogOutput('info', devCmd + " output\n"
                    + str(ifconfig_output))
        assert False, "\nCase for LLDP packets Tx/Rx Failed"
    else:
        # Set my default context to linux temporarily
        device1.setDefaultContext(context="vtyShell")
        LogOutput('info', "Case LLDP Tx/Rx Passed")

@pytest.mark.timeout(1000)
class Test_lldp_configuration:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_lldp_configuration.testObj = \
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        # Get topology object
        Test_lldp_configuration.topoObj = \
            Test_lldp_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_lldp_configuration.topoObj.terminate_nodes()

    def test_lldp_statistics(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        lldp_statistics(device1=dut01Obj, device2=dut02Obj)
