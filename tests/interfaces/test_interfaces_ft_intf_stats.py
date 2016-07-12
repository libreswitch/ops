# (C) Copyright 2015-Present Hewlett Packard Enterprise Development LP
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
# Test Plan for Interfaces:
#
# USER CONFIG
#
# Interface Statistics
#
# Verify Interface Statistics
#
# dut01: vtysh cmd:     configure terminal
# dut01: vtysh cmd:     vlan 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     interface 2
# dut01: vtysh cmd:     no routing
# dut01: vtysh cmd:     vlan access 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     interface 1
# dut01: vtysh cmd:     no routing
# dut01: vtysh cmd:     vlan access 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     <collect baseline for stats>
# wrkston01: shell cmd: ping <to wrkston02 ip addr>
#      : action   :     sleep(5)
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     stats updated correctly
# wrkston02: shell cmd: ping <to wrkston01 ip addr>
#      : action   :     sleep(5)
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     stats updated correctly
#      : action   :     sleep(10)
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     stats not updated


import pytest
from opstestfw import *
from opstestfw.switch.CLI import *

# Topology definition

topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01, \
                          lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}

STAT_SYNC_DELAY_SECS = 8
PING_BYTES = 128
PING_CNT = 30
RC_ERR_FMT = "vtysh exit code non-zero, %d"
NET_1 = "10.10.10"
WS1_IP = NET_1 + ".1"
WS2_IP = NET_1 + ".2"
NET1_MASK = "255.255.255.0"
NET1_BCAST = NET_1 + ".0"
PACKET_LOSS = 15

class Test_template:

    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_template.testObj = testEnviron(topoDict=topoDict)
        Test_template.topoObj = Test_template.testObj.topoObjGet()

    def teardown_class(cls):
        # Terminate all nodes
        Test_template.topoObj.terminate_nodes()
        LogOutput('info', "Tearing Down Topology")

    def init_intf(self, host, link):
        retStruct = host.NetworkConfig(ipAddr=host._ip,
                                    netMask=host._netm,
                                    interface=host._intf,
                                    broadcast=host._bcast, config=True)
        retCode = retStruct.returnCode()
        if retCode != 0:
            assert "Failed to configure host"

    def init_devices(self):
        # Switch 1
        self.s1 = self.topoObj.deviceObjGet(device="dut01")

        # Reboot the switch
        LogOutput('info', "Rebooting the switch")
        self.s1.Reboot()

        # Workstation 1
        self.w1 = self.topoObj.deviceObjGet(device="wrkston01")
        self.w1._ip = WS1_IP
        self.w1._netm = NET1_MASK
        self.w1._bcast = NET1_BCAST
        self.w1._intf = self.w1.linkPortMapping['lnk01']
        # Workstation 2
        self.w2 = self.topoObj.deviceObjGet(device="wrkston02")
        self.w2._ip = WS2_IP
        self.w2._netm = NET1_MASK
        self.w2._bcast = NET1_BCAST
        self.w2._intf = self.w2.linkPortMapping['lnk02']

        # Bring up the interfaces
        LogOutput('info', "Bringup up w1 eth1")
        self.init_intf(self.w1, 'lnk01')
        LogOutput('info', "Bringup up w2 eth1")
        self.init_intf(self.w2, 'lnk02')

        LogOutput('info', "Device init complete")

    def open_vtysh(self):
        self.vtyconn = self.s1
        rc = self.vtyconn.VtyshShell()

    def close_vtysh(self):
        rc = self.vtyconn.VtyshShell(configOption="exit")

    def startup_sequence(self):
        # Setup devices
        LogOutput('info', "Setting up devices")
        self.init_devices()

        # Start vtysh session
        LogOutput('info', "Opening up vtysh session")
        self.open_vtysh()

    def verify_ping(self, src, dest, expected):
        retry = 3
        current_iteration = 1
        while current_iteration <= retry:
            out = src.Ping(ipAddr=dest._ip, interval=.2, errorCheck=False,
                           packetCount=PING_CNT)

            if out is None:
                assert 1 == 0, "ping command failed, no output"

            LogOutput("info", "%s" % out.data)
            success = False;
            if out.data['packet_loss'] <= PACKET_LOSS:
                success = True;
                break
            current_iteration += 1

        assert success == expected, "ping was %s, expected %s" % (success, expected)

    def baseline_stats(self):
        interface_1 = self.s1.linkPortMapping['lnk01']
        self.i1_stat = InterfaceStatisticsShow(deviceObj=self.s1,
            interface=interface_1)

    def verify_stats(self, incr=True):
        # Retry loop around tx and rx stats.
        interface_1 = self.s1.linkPortMapping['lnk01']
        interface_2 = self.s1.linkPortMapping['lnk02']
        for iteration in range(0, 5):
            pass_cases = 0
            i1_new = InterfaceStatisticsShow(deviceObj=self.s1,
            interface=interface_1)
            rx_base = self.i1_stat.valueGet(key='RX')
            rx_new = i1_new.valueGet(key='RX')
            tx_base = self.i1_stat.valueGet(key='TX')
            tx_new = i1_new.valueGet(key='TX')
            if (int(rx_new['bytes']) - int(rx_base['bytes'])) < (PING_CNT * PING_BYTES):
                LogOutput('info', "Retrying statistic - waiting for rx_bytes to update")
                Sleep(seconds=5, message="\nWaiting")
                continue
            pass_cases = pass_cases + 1
            if (int(tx_new['bytes']) - int(tx_base['bytes'])) < (PING_CNT * PING_BYTES):
                LogOutput('info', "Retrying statistic - waiting for tx_bytes to update")
                Sleep(seconds=5, message="\nWaiting")
                continue
            pass_cases = pass_cases + 1
            if (int(rx_new['inputPackets']) - int(rx_base['inputPackets'])) < PING_CNT:
                LogOutput('info', "Retrying statistic - waiting for rx_packets to update")
                Sleep(seconds=5, message="\nWaiting")
                continue
            pass_cases = pass_cases + 1
            if (int(tx_new['outputPackets']) - int(tx_base['outputPackets'])) < PING_CNT:
                LogOutput('info', "Retrying statistic - waiting for tx_packets to update")
                Sleep(seconds=5, message="\nWaiting")
                continue
            pass_cases = pass_cases + 1
            if pass_cases == 4:
                break

        # If we hit the following asserts, we have an issue

        # Verify RX_bytes
        assert (int(rx_new['bytes']) - int(rx_base['bytes'])) >= \
                (PING_CNT * PING_BYTES), \
                "rx_bytes wrong. Was %d, is %d" % (int(rx_base['bytes']), \
                                                   int(rx_new['bytes']))

        # Verify TX_bytes
        assert (int(tx_new['bytes']) - int(tx_base['bytes'])) >= \
                (PING_CNT * PING_BYTES), \
                "tx_bytes wrong. Was %d, is %d" % (int(tx_new['bytes']), \
                                                   int(tx_base['bytes']))
        # Verify RX_packets
        assert (int(rx_new['inputPackets']) - int(rx_base['inputPackets'])) >= PING_CNT, \
                "rx_packets wrong. Was %d, is %d" % (int(rx_base['inputPackets']), \
                                                   int(rx_new['inputPackets']))

        # Verify TX_packets
        assert (int(tx_new['outputPackets']) - int(tx_base['outputPackets'])) >= PING_CNT, \
                "tx_packets wrong. Was %d, is %d" % (int(tx_base['outputPackets']), \
                                                   int(tx_new['outputPackets']))

        # Verify RX error
        assert int(rx_new['inputErrors']) == int(rx_base['inputErrors']), \
                "rx_error wrong. Was %d, is %d" % (int(rx_base['inputErrors']), \
                                                   int(rx_new['inputErrors']))

        # Verify TX error
        assert int(tx_new['inputErrors']) == int(tx_base['inputErrors']), \
                "tx_error wrong. Was %d, is %d" % (int(tx_base['inputErrors']), \
                                                   int(tx_new['inputErrors']))

        # Verify RX dropped
        assert int(rx_new['dropped']) == int(rx_base['dropped']), \
                "rx_dropped wrong. Was %d, is %d" % (int(rx_base['dropped']), \
                                                   int(rx_new['dropped']))

        # Verify TX dropped
        assert int(tx_new['dropped']) == int(tx_base['dropped']), \
                "tx_dropped wrong. Was %d, is %d" % (int(tx_base['dropped']), \
                                                   int(tx_new['dropped']))

        # Verify RX CRC
        assert int(rx_new['CRC_FCS']) == int(rx_base['CRC_FCS']), \
                "rx_crc wrong. Was %d, is %d" % (int(rx_base['CRC_FCS']), \
                                                   int(rx_new['CRC_FCS']))

        # Verify TX collision
        assert int(tx_new['collision']) == int(tx_base['collision']), \
                "tx_collision wrong. Was %d, is %d" % (int(tx_base['collision']), \
                                                   int(tx_new['collision']))

    def cmd_set_1(self, obj):
        # Issue "configure terminal" command
        interface_1 = self.s1.linkPortMapping['lnk01']
        interface_2 = self.s1.linkPortMapping['lnk02']
        LogOutput("info", "sending configure terminal")
        rc = obj.cmd("configure terminal")
        LogOutput("info", "sending vlan 10")
        rc = obj.cmd("vlan 10")
        LogOutput("info", "sending no shutdown")
        rc = obj.cmd("no shutdown")
        LogOutput("info", "sending exit")
        rc = obj.cmd("exit")
        LogOutput("info", "sending interface %s"%interface_2)
        rc = obj.cmd("interface %s"%interface_2)
        LogOutput("info", "sending no routing")
        rc = obj.cmd("no routing")
        LogOutput("info", "sending vlan access 10")
        rc = obj.cmd("vlan access 10")
        LogOutput("info", "sending no shutdown")
        rc = obj.cmd("no shutdown")
        LogOutput("info", "sending exit")
        rc = obj.cmd("exit")
        LogOutput("info", "sending interface %s"%interface_1)
        rc = obj.cmd("interface %s"%interface_1)
        LogOutput("info", "sending no routing")
        rc = obj.cmd("no routing")
        LogOutput("info", "sending vlan access 10")
        rc = obj.cmd("vlan access 10")
        LogOutput("info", "sending no shutdown")
        rc = self.vtyconn.cmd("no shutdown")

    def test_statistics(self):
        # Get everything initially configured
        LogOutput('info', "*****Testing statistics*****")
        self.startup_sequence()
        interface_1 = self.s1.linkPortMapping['lnk01']
        interface_2 = self.s1.linkPortMapping['lnk02']

        # Configure interfaces 1 & 2 on vlan 10, with 1 down and 2 up.
        LogOutput('info',
            "Cfg intfs %s & %s on vlan 10, with %s down and %s up"% (interface_1, interface_2, interface_1, interface_2))
        self.cmd_set_1(self.vtyconn)

        # Back out to CLI main
        rc = self.vtyconn.cmd("exit")
        rc = self.vtyconn.cmd("exit")

        Sleep(seconds=10, message="\nWaiting")
        # Baseline the statistics
        LogOutput('info', "Baselining the statistics")
        self.baseline_stats()

        # Ping w2->w3, switch port 1 to switch port 2.
        LogOutput('info', "Ping w1->w2")
        self.verify_ping(self.w1, self.w2, True)

        # Verify stats are correctly updated.
        sleep(STAT_SYNC_DELAY_SECS)
        LogOutput('info', "Verify stats are correctly updated")
        self.verify_stats(incr=True)

        # Baseline the statistics
        LogOutput('info', "Baselining the statistics")
        self.baseline_stats()

        # Ping w3->w2, switch port 1 to switch port 2.
        LogOutput('info', "Ping w2->w1")
        self.verify_ping(self.w2, self.w1, True)

        # Verify stats are correctly updated.
        sleep(STAT_SYNC_DELAY_SECS)
        LogOutput('info', "Verify stats are correctly updated")
        self.verify_stats(incr=True)

        LogOutput('info', "succeeded!")
