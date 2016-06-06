#!/usr/bin/python

# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
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
from opsvsi.docker import *
from opsvsi.opsvsitest import *

#
# The purpose of this test is to test DHCP server address lease
# configurations for static allocations and verify the
# allocations in OVSDB and DHCP client interface.
#
# For this test, we need 2 hosts connected to a switch
# which start exchanging DHCP messages.
#
# S1 [interface 1]<--->[interface 1] H1
# S1 [interface 2]<--->[interface 2] H2
#


class myTopo(Topo):
    def build(self, hsts=2, sws=1, **_opts):
        '''Function to build the topology of two hosts\
           and two switches'''
        self.hsts = hsts
        self.sws = sws
        # Add list of hosts
        for h in irange(1, hsts):
            host = self.addHost('h%s' % h)
        # Add list of switches
        for s in irange(1, sws):
            switch = self.addSwitch('s%s' % s)
        # Add links between nodes based on custom topology
        self.addLink('h1', 's1')
        self.addLink('h2', 's1')


class dhcpIPV4StaticPoolConfigCTTest(OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=2, sws=1,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                                       switch=VsiOpenSwitch,
                                       host=Host,
                                       link=OpsVsiLink, controller=None,
                                       build=True)

        self.host1Pool = "host1"
        self.host2Pool = "host2"
        self.ipv4AddressHost1 = "10.0.0.50"
        self.ipv4AddressHost2 = "20.0.0.50"
        self.macAddressHost1 = ""
        self.macAddressHost2 = ""
        self.dhcpServerEnable = "dhcp-server"

    def testConfigure(self):
        info('\n### Test DHCP server static IPV4 configuration ###\n')
        info('\n### Configuring static IPV4 address allocation ###\n')
        ifconfigHost1MacAddr = ""
        ifconfigHost2MacAddr = ""
        ifconfigMacAddrIdx = 4
        ifconfigMacAddrLineNum = 0
        s1 = self.net.switches[0]

        # Configure switch s1
        s1.cmdCLI("configure terminal")

        # Configure interface 1 on switch s1
        s1.cmdCLI("interface 1")
        s1.cmdCLI("no shutdown")
        s1.cmdCLI("ip address 10.0.10.1/8")
        s1.cmdCLI("ipv6 address 2000::1/120")
        s1.cmdCLI("exit")

        # Configure interface 2 on switch s1
        s1.cmdCLI("interface 2")
        s1.cmdCLI("no shutdown")
        s1.cmdCLI("ip address 20.0.0.1/8")
        s1.cmdCLI("ipv6 address 2001::1/120")
        s1.cmdCLI("end")

        # We need to get mac addresses for hosts 1 and 2 via ifconfig command
        # and use the values to configure static address assignments
        h1 = self.net.hosts[0]
        h2 = self.net.hosts[1]

        dump = h1.cmd("ifconfig h1-eth0")
        lines = dump.split('\n')
        count = 0
        for line in lines:
            if count == ifconfigMacAddrLineNum:
                outStr = line.split()
                ifconfigHost1MacAddr = outStr[ifconfigMacAddrIdx]
                break
        dump = h2.cmd("ifconfig h2-eth0")
        lines = dump.split('\n')
        count = 0
        for line in lines:
            if count == ifconfigMacAddrLineNum:
                outStr = line.split()
                ifconfigHost2MacAddr = outStr[ifconfigMacAddrIdx]
                break
        assert ifconfigHost1MacAddr != "", \
            "Mac address parsing failed for host 1"
        assert ifconfigHost2MacAddr != "", \
            "Mac address parsing failed for host 2"

        self.macAddressHost1 = ifconfigHost1MacAddr
        self.macAddressHost2 = ifconfigHost2MacAddr

        host1PoolCmd = "static "+self.ipv4AddressHost1 + \
            " match-mac-address "+self.macAddressHost1
        host2PoolCmd = "static "+self.ipv4AddressHost2 + \
            " match-mac-address "+self.macAddressHost2

        s1.cmdCLI("configure terminal")
        s1.cmdCLI(self.dhcpServerEnable)
        s1.cmdCLI(host1PoolCmd)
        s1.cmdCLI(host2PoolCmd)

        s1.cmdCLI("end")

        info('\n### DHCP server static IPV4 pool '\
             'configured on Switch s1 ###\n')

    def testdhcpServerStaticIPV4PoolConfig(self):
        info('\n### Verify DHCP server static IPV4 pool config in db ###\n')
        s1 = self.net.switches[0]

        # Parse "show dhcp-server" output.
        # This section will have all the
        # DHCP server static IPV4 pool configuration entries.
        # Then parse line by line to match the contents
        dump = s1.cmdCLI("show dhcp-server")
        lines = dump.split('\n')
        count = 0
        for line in lines:
                if (self.ipv4AddressHost1 in line and
                self.macAddressHost1 in line):
                    count = count + 1
                elif (self.ipv4AddressHost2 in line and
                self.macAddressHost2 in line):
                    count = count + 1

        assert count == 2, \
        "DHCP server static IPV4 pool config not populated in DB"

        info('\n### testdhcpServerStaticIPV4PoolConfig: Test Passed ###\n')

    def testConfigureDhcpClient(self):
        info('\n### Configure DHCP clients for dynamic '\
             'IPV4 address in db ###\n')

        h1 = self.net.hosts[0]
        h2 = self.net.hosts[1]

        h1.cmd("ifconfig -a")
        h1.cmd("ip addr del 10.0.0.1/8 dev h1-eth0")
        h1.cmd("dhclient h1-eth0")

        h2.cmd("ifconfig -a")
        h2.cmd("ip addr del 10.0.0.2/8 dev h2-eth0")
        h2.cmd("dhclient h2-eth0")

        info('\n### DHCP clients h1 and h2 configured \
        for dynamic IPV4 pool ###\n')

    def testdhcpClientStaticIPV4AddressConfig(self):
        info('\n### Verify DHCP clients h1 and h2 '\
             'static IPV4 address config in db ###\n')

        h1 = self.net.hosts[0]
        h2 = self.net.hosts[1]
        s1 = self.net.switches[0]

        ifconfigHost1MacAddr = ""
        ifconfigHost2MacAddr = ""
        ifconfigHost1Ipv4Addr = ""
        ifconfigHost2Ipv4Addr = ""
        ifconfigIpv4PrefixPattern = "inet addr:"
        ifconfigIpv4AddrIdx = 1
        ifconfigMacAddrIdx = 4
        ifconfigIpv4AddrLineNum = 1
        ifconfigMacAddrLineNum = 0
        dhcpMacAddrHost1 = ""
        dhcpMacAddrHost2 = ""
        dhcpMacAddrIdx = 5
        dhcpIpv4AddrHost1 = ""
        dhcpIpv4AddrHost2 = ""
        dhcpIpv4AddrIdx = 6

        # Parse the "ifconfig" outputs for interfaces
        # h1-eth0 and h2-eth0 for hosts 1 and 2
        # respectively and save the values for ipaddresses
        # and mac addresses into variables above
        dump = h1.cmd("ifconfig h1-eth0")
        lines = dump.split('\n')
        count = 0
        for line in lines:
            if count == ifconfigMacAddrLineNum:
                outStr = line.split()
                ifconfigHost1MacAddr = outStr[ifconfigMacAddrIdx]
            elif count == ifconfigIpv4AddrLineNum:
                outStr = line.split()
                ifconfigHost1Ipv4AddrTemp1 = outStr[ifconfigIpv4AddrIdx]
                ifconfigHost1Ipv4AddrTemp2 = \
                    ifconfigHost1Ipv4AddrTemp1.split(':')
                ifconfigHost1Ipv4Addr = ifconfigHost1Ipv4AddrTemp2[1]
            count = count + 1
        dump = h2.cmd("ifconfig h2-eth0")
        lines = dump.split('\n')
        count = 0
        for line in lines:
            if count == ifconfigMacAddrLineNum:
                outStr = line.split()
                ifconfigHost2MacAddr = outStr[ifconfigMacAddrIdx]
            elif count == ifconfigIpv4AddrLineNum:
                outStr = line.split()
                ifconfigHost2Ipv4AddrTemp1 = outStr[ifconfigIpv4AddrIdx]
                ifconfigHost2Ipv4AddrTemp2 = \
                    ifconfigHost2Ipv4AddrTemp1.split(':')
                ifconfigHost2Ipv4Addr = ifconfigHost2Ipv4AddrTemp2[1]
            count = count + 1

        # Parse the "show dhcp-server leases" output
        # and verify if the values for interfaces
        # h1-eth0 and h2-eth0 for hosts
        # 1 and 2 respectively are present in the lease dB
        dump = s1.cmdCLI("show dhcp-server leases")
        lines = dump.split('\n')
        count = 0
        for line in lines:
            if ifconfigHost1MacAddr in line:
                outStr = line.split()
                dhcpIpv4AddrHost1 = outStr[dhcpIpv4AddrIdx]
                assert dhcpIpv4AddrHost1 == ifconfigHost1Ipv4Addr, \
                "IPV4 address for host 1 "\
                "does not match the address in DHCP lease database"
            elif ifconfigHost2MacAddr in line:
                outStr = line.split()
                dhcpIpv4AddrHost2 = outStr[dhcpIpv4AddrIdx]
                assert dhcpIpv4AddrHost2 == ifconfigHost2Ipv4Addr, \
                "IPV4 address for host 2 "\
                "does not match the address in DHCP lease database"

        info('\n### testdhcpClientStaticIPV4AddressConfig: Test Passed ###\n')


@pytest.mark.skipif(True, reason="Test case is causing docker space issues")
class Test_dhcp_tftp_commands:

    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_dhcp_tftp_commands.dhcpIPV4StaticPoolConfigCTTest = \
                                      dhcpIPV4StaticPoolConfigCTTest()

    def teardown_class(cls):
        # Stop the Docker containers, and
        # mininet topology
        Test_dhcp_tftp_commands.dhcpIPV4StaticPoolConfigCTTest.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.dhcpIPV4StaticPoolConfigCTTest

    def test_dhcp_tftp_full(self):
        info('\n########## Test DHCP server static IPV4 '\
             'configuration ##########\n')
        self.dhcpIPV4StaticPoolConfigCTTest.testConfigure()
        self.dhcpIPV4StaticPoolConfigCTTest. \
        testdhcpServerStaticIPV4PoolConfig()
        self.dhcpIPV4StaticPoolConfigCTTest. \
        testdhcpClientStaticIPV4AddressConfig()
        info('\n########## End of test DHCP server static IPV4 '\
             'configuration ##########\n')
