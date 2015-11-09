#!/usr/bin/env python

# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
#
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
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *

import sys
import time
import socket
import random

#Two ECMP nexthops are configured and two separate flows are sent through the
#ECMP links. Different ECMP hash methods are configured and the test confirms
#that the flows pick different nexthops based on the 4-tuples in the flow.
#The 4-tuples for the flows are selected manually today based on trial and error,
#but the right way would be to select the tuples by using the ASIC APIs
#that calculate nexthop link for an input tuple.
#Note: There is a possibility that the tuples this script uses would not cause the
#ASIC to pick different nexthops when ECMP configuration changes in the future
#or for different ASICs. We should use the ASIC APIs to pick the right tuples
#programatically.


topoDict = {"topoExecution": 1000,
            "topoType": "physical",
            "topoDevices": "dut01 dut02 wrkston01",
            "topoTarget": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:wrkston01",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation"}

def switch_reboot(dut01):
    # Reboot switch
    LogOutput('info', "Reboot switch")
    dut01.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct

def get_tx_stats(dutObj, intf1, intf2):
    intf1Stats = InterfaceStatisticsShow(deviceObj=dutObj, interface=intf1)
    intf2Stats = InterfaceStatisticsShow(deviceObj=dutObj, interface=intf2)

    if intf1Stats.returnCode() != 0 or intf2Stats.returnCode() != 0:
        LogOutput('error', "Can't show interface information")
        assert(False)

    tx1 = intf1Stats.valueGet(key='TX')
    tx1 = tx1['outputPackets']
    tx2 = intf2Stats.valueGet(key='TX')
    tx2 = tx2['outputPackets']
    return int(tx1), int(tx2)

# If txstop has atleast 70% of num pkts sent, then pick that as the selected
# interface
def get_selected_intf(tx1start, tx1stop, tx2start, tx2stop, num_pkts, intf1, intf2):
    selectedIntf = "None"
    if (tx1stop > (tx1start + (num_pkts * .7))):
        selectedIntf = intf1
    if (tx2stop > (tx2start + (num_pkts * .7))):
        selectedIntf = intf2
    return selectedIntf

def enable_ecmp_hash(dutObj, hashmethod):
    cmd = "no ip ecmp load-balance " + hashmethod + " disable"
    retStruct = dutObj.ConfigVtyShell(enter=True)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enter vtysh config prompt")
        assert(False)
    retStruct = dutObj.DeviceInteract(command=cmd)
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to enable ecmp load-balance " + hashmethod)
        assert(False)
    retStruct = dutObj.ConfigVtyShell(enter=False)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to exit vtysh config prompt")
        assert(False)

def disable_ecmp_hash(dutObj, hashmethod):
    cmd = "ip ecmp load-balance " + hashmethod + " disable"
    retStruct = dutObj.ConfigVtyShell(enter=True)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enter vtysh config prompt")
        assert(False)
    retStruct = dutObj.DeviceInteract(command=cmd)
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to disable ecmp load-balance " + hashmethod)
        assert(False)
    retStruct = dutObj.ConfigVtyShell(enter=False)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to exit vtysh config prompt")
        assert(False)

def disable_all_ecmp_hash(dutObj):
    retStruct = dutObj.ConfigVtyShell(enter=True)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enter vtysh config prompt")
        assert(False)
    retStruct = dutObj.DeviceInteract(command="ip ecmp load-balance src-ip disable")
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to disable ecmp load-balance src-ip")
        assert(False)
    retStruct = dutObj.DeviceInteract(command="ip ecmp load-balance dst-ip disable")
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to disable ecmp load-balance dst-ip")
        assert(False)
    retStruct = dutObj.DeviceInteract(command="ip ecmp load-balance src-port disable")
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to disable ecmp load-balance src-port")
        assert(False)
    retStruct = dutObj.DeviceInteract(command="ip ecmp load-balance dst-port disable")
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to disable ecmp load-balance dst-port")
        assert(False)
    retStruct = dutObj.ConfigVtyShell(enter=False)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to exit vtysh config prompt")
        assert(False)

def enable_all_ecmp_hash(dutObj):
    retStruct = dutObj.ConfigVtyShell(enter=True)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to enter vtysh config prompt")
        assert(False)
    retStruct = dutObj.DeviceInteract(command="no ip ecmp load-balance src-ip disable")
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to enable ecmp load-balance src-ip")
        assert(False)
    retStruct = dutObj.DeviceInteract(command="no ip ecmp load-balance dst-ip disable")
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to enable ecmp load-balance dst-ip")
        assert(False)
    retStruct = dutObj.DeviceInteract(command="no ip ecmp load-balance src-port disable")
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to enable ecmp load-balance src-port")
        assert(False)
    retStruct = dutObj.DeviceInteract(command="no ip ecmp load-balance dst-port disable")
    if retStruct.get('returnCode') != 0:
        LogOutput('error', "Failed to enable ecmp load-balance dst-port")
        assert(False)
    retStruct = dutObj.ConfigVtyShell(enter=False)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to exit vtysh config prompt")
        assert(False)

def run_nexthop_calc(dutObj, intf1, intf2,
                     srcport1, dstip1, dstport1,
                     srcport2, dstip2, dstport2):
    tx1start, tx2start = get_tx_stats(dutObj, intf1, intf2)
    send_udp_packets(srcport1, dstip1, dstport1, num_pkts)
    sleep(10)
    tx1stop, tx2stop = get_tx_stats(dutObj, intf1, intf2)

    selectedIntf1 = get_selected_intf(tx1start, tx1stop, tx2start, tx2stop,
                                      num_pkts, intf1, intf2)
    LogOutput('info', "Nexthop interface for (" + str(srcport1) + ", " +
              dstip1 + ", " + str(dstport1) + ") is " + selectedIntf1)

    tx1start, tx2start = get_tx_stats(dutObj, intf1, intf2)
    send_udp_packets(srcport2, dstip2, dstport2, num_pkts)
    sleep(10)
    tx1stop, tx2stop = get_tx_stats(dut01Obj, intf1sw1, intf2sw1)

    selectedIntf2 = get_selected_intf(tx1start, tx1stop, tx2start, tx2stop,
                                      num_pkts, intf1, intf2)
    LogOutput('info', "Nexthop interface for (" + str(srcport2) + ", " +
              dstip2 + ", " + str(dstport2) + ") is " + selectedIntf2)
    return selectedIntf1, selectedIntf2

# Send some UDP packets with the given srcport, dstport, dstip, numpkts.
# Quite hacky way of doing this, but generate a python socket program to
# send packets, save the program to host filesystem and execute it. Any better
# way to do this? host iperf doesn't seem to support changing source port
# or to sent a specified number of packets. Also, this method does not require
# an iperf server to be configured and running on another host.
def send_udp_packets(src_port, dst_ip, dst_port, num_pkts):
        filename = "/tmp/testfile" + str(random.randint(1,1000))
        cmd = """echo -e \"
#!/usr/bin/env python
import socket
import sys
import time
message = 'Hello OpenSwitch.'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_address = ('0.0.0.0', """ + str(src_port) + """ )
sock.bind(client_address)
server_address = ('""" + str(dst_ip) + """\', """ + str(dst_port) + """ )
for x in range(0, """ + str(num_pkts) + """):
   sock.sendto(message, server_address)
   time.sleep(0.1)
\" >  """ + filename
        cmdOut = wrkston01Obj.cmd(cmd)
        cmdOut = wrkston01Obj.cmd("sed -i '1d' " + filename)
        cmdOut = wrkston01Obj.cmd("chmod +x " + filename)
        cmdOut = wrkston01Obj.cmd(filename)
        cmdOut = wrkston01Obj.cmd("rm -f " + filename)

def clean_up(dut01, dut02):
    listDut = [dut01, dut02]
    for currentDut in listDut:
        devRebootRetStruct = switch_reboot(currentDut)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch")
            assert(False)
    else:
        LogOutput('info', "Passed Switch Reboot ")

class Test_ft_ecmp_hash:

    dut01Obj = None
    dut02Obj = None
    workston01Obj = None

    def setup_class(cls):
        Test_ft_ecmp_hash.testObj = testEnviron(topoDict=topoDict)
        Test_ft_ecmp_hash.topoObj = Test_ft_ecmp_hash.testObj.topoObjGet()

    def teardown_class(cls):
        clean_up(dut01Obj, dut02Obj)
        Test_ft_ecmp_hash.topoObj.terminate_nodes()
        LogOutput('info', "\nDone teardown_class############################\n")

    def test_ecmp_hash(self):
        global listDut
        global dut01Obj
        global dut02Obj
        global wrkston01Obj
        global intf1sw1
        global intf2sw1
        global intf1sw2
        global intf2sw2
        global num_pkts
        global intf3sw1

        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        intf1sw1 = dut01Obj.linkPortMapping['lnk01']
        intf2sw1 = dut01Obj.linkPortMapping['lnk02']
        intf3sw1 = dut01Obj.linkPortMapping['lnk03']
        intf1sw2 = dut02Obj.linkPortMapping['lnk01']
        intf2sw2 = dut02Obj.linkPortMapping['lnk02']
        num_pkts = 100

        listDut = [dut01Obj, dut02Obj]


    ##########################################################################
    # Step 2 - Configure the switches
    ##########################################################################

    def test_configure_switches(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 1 - Configure ecmp routes in the switches")
        LogOutput('info', "################################################")
        # Switch configuration

        retStruct = InterfaceEnable(deviceObj=dut01Obj,
                                    enable=True,
                                    interface=dut01Obj.linkPortMapping['lnk01'])
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable lnk01 on dut01")
            assert(False)
        else:
            LogOutput('info', "Succesfully enabled lnk01 on dut01")

        retStruct = InterfaceEnable(deviceObj=dut01Obj,
                                    enable=True,
                                    interface=dut01Obj.linkPortMapping['lnk02'])
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable lnk02 on dut01")
            assert(False)
        else:
            LogOutput('info', "Succesfully enabled lnk02 on dut01")

        retStruct = InterfaceEnable(deviceObj=dut02Obj,
                                    enable=True,
                                    interface=dut02Obj.linkPortMapping['lnk01'])
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable lnk01 on dut02")
            assert(False)
        else:
            LogOutput('info', "Succesfully enabled lnk01 on dut02")

        retStruct = InterfaceEnable(deviceObj=dut01Obj,
                                    enable=True,
                                    interface=dut01Obj.linkPortMapping['lnk03'])
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable lnk03 on dut01")
            assert(False)
        else:
            LogOutput('info', "Succesfully enabled lnk03 on dut01")

        retStruct = InterfaceEnable(deviceObj=dut02Obj,
                                    enable=True,
                                    interface=dut02Obj.linkPortMapping['lnk02'])
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable lnk02 on dut02")
            assert(False)
        else:
            LogOutput('info', "Succesfully enabled lnk02 on dut02")

        retStruct = InterfaceIpConfig(deviceObj=dut01Obj,
                                      interface=dut01Obj.linkPortMapping['lnk01'],
                                      addr="100.0.0.1",
                                      mask=24,
                                      config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure IP on lnk01 on dut01")
            assert(False)
        else:
            LogOutput('info', "Successfully configured IP on lnk01 on dut01")

        retStruct = InterfaceIpConfig(deviceObj=dut01Obj,
                                      interface=dut01Obj.linkPortMapping['lnk02'],
                                      addr="200.0.0.1",
                                      mask=24,
                                      config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure IP on lnk02 on dut01")
            assert(False)
        else:
            LogOutput('info', "Successfully configured IP on lnk02 on dut01")

        retStruct = InterfaceIpConfig(deviceObj=dut01Obj,
                                      interface=dut01Obj.linkPortMapping['lnk03'],
                                      addr="10.0.0.2",
                                      mask=24,
                                      config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure IP on lnk03 on dut01")
            assert(False)
        else:
            LogOutput('info', "Successfully configured IP on lnk03 on dut01")

        retStruct = InterfaceIpConfig(deviceObj=dut02Obj,
                                      interface=dut02Obj.linkPortMapping['lnk01'],
                                      addr="100.0.0.2",
                                      mask=24,
                                      config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure IP on lnk01 on dut02")
            assert(False)
        else:
            LogOutput('info', "Successfully configured IP on lnk01 on dut02")

        retStruct = InterfaceIpConfig(deviceObj=dut02Obj,
                                      interface=dut02Obj.linkPortMapping['lnk02'],
                                      addr="200.0.0.2",
                                      mask=24,
                                      config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure IP on lnk02 on dut02")
            assert(False)
        else:
            LogOutput('info', "Successfully configured IP on lnk02 on dut02")

        retStructRouteCfg = IpRouteConfig(deviceObj=dut01Obj,
                                          route="30.0.0.0",
                                          mask=24,
                                          nexthop="100.0.0.2")
        if retStructRouteCfg.returnCode() != 0:
            LogOutput('error', "Failed to configure route 30.0.0.0/24 100.0.0.2")
            assert(False)
        else:
            LogOutput('info', "Successfully configured route 30.0.0.0/24 100.0.0.2")
        retStructRouteCfg = IpRouteConfig(deviceObj=dut01Obj,
                                          route="30.0.0.0",
                                          mask=24,
                                          nexthop="200.0.0.2")
        if retStructRouteCfg.returnCode() != 0:
            LogOutput('error', "Failed to configure route 30.0.0.0/24 200.0.0.2")
            assert(False)
        else:
            LogOutput('info', "Successfully configured route 30.0.0.0/24 200.0.0.2")

        retStruct = wrkston01Obj.NetworkConfig(ipAddr="10.0.0.4",
                                        netMask="255.255.255.0",
                                        broadcast="10.0.0.255",
                                        interface=wrkston01Obj.linkPortMapping['lnk03'],
                                        config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure IP 10.0.0.4 on workstation1")
            assert(False)
        else:
            LogOutput('info', "Successfully configured IP 10.0.0.4 on workstation 01")
        cmdOut = wrkston01Obj.cmd("ip route add 30.0.0.0/24 via 10.0.0.2")
        LogOutput('info', "ip route add 30.0.0.0/24 via 10.0.0.2 done on workstation 01\n")

    def test_disable_all_hash(self):
        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 2 - Test disable all hash")
        LogOutput('info', "################################################")

        disable_all_ecmp_hash(dut01Obj)
        intf1, intf2 = run_nexthop_calc(dut01Obj, intf1sw1, intf2sw1,
                                        10024, "30.0.0.1", 10024,
                                        10023, "30.0.0.4", 10023)

        if intf1 != intf2:
            LogOutput('error', "Disable all hashing failed")
            error(False)
        else:
            LogOutput('info', "Disable all hashing success")

    def test_l4src_hash(self):
        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 3 - Test src port hash")
        LogOutput('info', "################################################")

        enable_all_ecmp_hash(dut01Obj)
        intf1, intf2 = run_nexthop_calc(dut01Obj, intf1sw1, intf2sw1,
                                        10024, "30.0.0.1", 10024,
                                        10023, "30.0.0.1", 10024)

        if intf1 == intf2:
            LogOutput('error', "src port hashing failed")
            error(False)
        else:
            LogOutput('info', "src port hashing success")

        LogOutput('info', "Step 3.II - Test disable src port hash")

        disable_ecmp_hash(dut01Obj, "src-port")
        intf1, intf2 = run_nexthop_calc(dut01Obj, intf1sw1, intf2sw1,
                                        10024, "30.0.0.1", 10024,
                                        10023, "30.0.0.1", 10024)

        if intf1 != intf2:
            LogOutput('error', "disabling src port hashing failed")
            error(False)
        else:
            LogOutput('info', "disabling src port hashing success")


    def test_l4dst_hash(self):
        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 4 - Test dst port hash")
        LogOutput('info', "################################################")

        enable_all_ecmp_hash(dut01Obj)
        intf1, intf2 = run_nexthop_calc(dut01Obj, intf1sw1, intf2sw1,
                                        10024, "30.0.0.1", 10024,
                                        10024, "30.0.0.1", 10023)

        if intf1 == intf2:
            LogOutput('error', "dst port hashing failed")
            error(False)
        else:
            LogOutput('info', "dst port hashing success")

        LogOutput('info', "Step 4.II - Test disable dst port hash")

        disable_ecmp_hash(dut01Obj, "dst-port")
        intf1, intf2 = run_nexthop_calc(dut01Obj, intf1sw1, intf2sw1,
                                        10024, "30.0.0.1", 10024,
                                        10024, "30.0.0.1", 10023)

        if intf1 != intf2:
            LogOutput('error', "disabling dst port hashing failed")
            error(False)
        else:
            LogOutput('info', "disabling dst port hashing success")

    def test_l3dst_hash(self):
        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 5 - Test dest IP hash")
        LogOutput('info', "################################################")

        enable_all_ecmp_hash(dut01Obj)
        intf1, intf2 = run_nexthop_calc(dut01Obj, intf1sw1, intf2sw1,
                                        10024, "30.0.0.1", 10024,
                                        10024, "30.0.0.4", 10024)

        if intf1 == intf2:
            LogOutput('error', "dst IP hashing failed")
            error(False)
        else:
            LogOutput('info', "dst IP hashing success")

        LogOutput('info', "Step 5.II - Test disable dst IP hash")

        disable_ecmp_hash(dut01Obj, "dst-ip")
        intf1, intf2 = run_nexthop_calc(dut01Obj, intf1sw1, intf2sw1,
                                        10024, "30.0.0.1", 10024,
                                        10024, "30.0.0.4", 10024)

        if intf1 != intf2:
            LogOutput('error', "disabling dst IP hashing failed")
            error(False)
        else:
            LogOutput('info', "disabling dst IP hashing success")

    def test_l3src_hash(self):
        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 6 - Test src IP hash")
        LogOutput('info', "################################################")

        enable_all_ecmp_hash(dut01Obj)
        tx1start, tx2start = get_tx_stats(dut01Obj, intf1sw1, intf2sw1)
        send_udp_packets(10024, "30.0.0.1", 10024, num_pkts)
        sleep(10)
        tx1stop, tx2stop = get_tx_stats(dut01Obj, intf1sw1, intf2sw1)
        intf1 = get_selected_intf(tx1start, tx1stop, tx2start, tx2stop,
                                  num_pkts, intf1sw1, intf2sw1)
        LogOutput('info', "Nexthop interface for (" + str(10024) + ", " +
                  "src:10.0.0.4" + ", " + str(10024) + ") is " + intf1)

        retStruct = wrkston01Obj.NetworkConfig(ipAddr="10.0.0.1",
                                        netMask="255.255.255.0",
                                        broadcast="10.0.0.255",
                                        interface=wrkston01Obj.linkPortMapping['lnk03'],
                                        config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure IP 10.0.0.1 on workstation1")
            assert(False)
        else:
            LogOutput('info', "Successfully configured IP 10.0.0.1 on workstation 01")
        cmdOut = wrkston01Obj.cmd("ip route add 30.0.0.0/24 via 10.0.0.2")
        LogOutput('info', "ip route add 30.0.0.0/24 via 10.0.0.2 done on workstation 01\n")

        tx1start, tx2start = get_tx_stats(dut01Obj, intf1sw1, intf2sw1)
        send_udp_packets(10024, "30.0.0.1", 10024, num_pkts)
        sleep(10)
        tx1stop, tx2stop = get_tx_stats(dut01Obj, intf1sw1, intf2sw1)
        intf2 = get_selected_intf(tx1start, tx1stop, tx2start, tx2stop,
                                  num_pkts, intf1sw1, intf2sw1)
        LogOutput('info', "Nexthop interface for (" + str(10024) + ", " +
                  "src:10.0.0.1" + ", " + str(10024) + ") is " + intf2)

        if intf1 == intf2:
            LogOutput('error', "src IP hashing failed")
            error(False)
        else:
            LogOutput('info', "src IP hashing success")

        LogOutput('info', "Step 6.II - Test disable src IP hash")

        disable_ecmp_hash(dut01Obj, "src-ip")
        tx1start, tx2start = get_tx_stats(dut01Obj, intf1sw1, intf2sw1)
        send_udp_packets(10024, "30.0.0.1", 10024, num_pkts)
        sleep(10)
        tx1stop, tx2stop = get_tx_stats(dut01Obj, intf1sw1, intf2sw1)
        intf1 = get_selected_intf(tx1start, tx1stop, tx2start, tx2stop,
                                  num_pkts, intf1sw1, intf2sw1)
        LogOutput('info', "Nexthop interface for (" + str(10024) + ", " +
                  "src:10.0.0.1" + ", " + str(10024) + ") is " + intf1)

        retStruct = wrkston01Obj.NetworkConfig(ipAddr="10.0.0.4",
                                        netMask="255.255.255.0",
                                        broadcast="10.0.0.255",
                                        interface=wrkston01Obj.linkPortMapping['lnk03'],
                                        config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configure IP 10.0.0.4 on workstation1")
            assert(False)
        else:
            LogOutput('info', "Successfully configured IP 10.0.0.4 on workstation 01")
        cmdOut = wrkston01Obj.cmd("ip route add 30.0.0.0/24 via 10.0.0.2")
        LogOutput('info', "ip route add 30.0.0.0/24 via 10.0.0.2 done on workstation 01\n")

        tx1start, tx2start = get_tx_stats(dut01Obj, intf1sw1, intf2sw1)
        send_udp_packets(10024, "30.0.0.1", 10024, num_pkts)
        sleep(10)
        tx1stop, tx2stop = get_tx_stats(dut01Obj, intf1sw1, intf2sw1)
        intf2 = get_selected_intf(tx1start, tx1stop, tx2start, tx2stop,
                                  num_pkts, intf1sw1, intf2sw1)
        LogOutput('info', "Nexthop interface for (" + str(10024) + ", " +
                  "src:10.0.0.4" + ", " + str(10024) + ") is " + intf2)
        if intf1 != intf2:
            LogOutput('error', "disabling src IP hashing failed")
            error(False)
        else:
            LogOutput('info', "disabling src IP hashing success")

        LogOutput('info', "All tests passed ! ")
