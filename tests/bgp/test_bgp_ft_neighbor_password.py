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
from opsvsiutils.vtyshutils import *
from opsvsiutils.bgpconfig import *

#
# This case tests if neighbor password CLI is working. It checks if MD5
# authentication is configured with the same password on both BGP peers. If the
# password is not same the connection will not be made. It also tests no
# neighbor password which does not enable MD5 authentication between BGP peers
#
# The following command is tested:
#   * neighbor <peer> password <passwd>
#   * no neighbor <peer> password
#
# S1 [interface 1]<--->[interface 1] S2
#

BGP1_ASN = "1"
BGP1_ROUTER_ID = "9.0.0.1"
BGP1_NETWORK = "11.0.0.0"
BGP1_PASSWORD = "1234"
BGP1_WRONG_PASSWORD = "12"

BGP2_ASN = "2"
BGP2_ROUTER_ID = "9.0.0.2"
BGP2_NETWORK = "12.0.0.0"
BGP2_PASSWORD = "1234"

BGP1_NEIGHBOR = BGP2_ROUTER_ID
BGP1_NEIGHBOR_ASN = BGP2_ASN
BGP1_NEIGHBOR_PASSWD = BGP1_PASSWORD

BGP2_NEIGHBOR = BGP1_ROUTER_ID
BGP2_NEIGHBOR_ASN = BGP1_ASN
BGP2_NEIGHBOR_PASSWD = BGP2_PASSWORD

BGP_NETWORK_PL = "8"
BGP_NETWORK_MASK = "255.0.0.0"
BGP_ROUTER_IDS = [BGP1_ROUTER_ID, BGP2_ROUTER_ID]

BGP1_CONFIG = ["router bgp %s" % BGP1_ASN,
               "bgp router-id %s" % BGP1_ROUTER_ID,
               "network %s/%s" % (BGP1_NETWORK, BGP_NETWORK_PL),
               "neighbor %s remote-as %s" % (BGP1_NEIGHBOR, BGP1_NEIGHBOR_ASN),
               "neighbor %s password %s" % (BGP1_NEIGHBOR,
                                            BGP1_NEIGHBOR_PASSWD)]

BGP2_CONFIG = ["router bgp %s" % BGP2_ASN,
               "bgp router-id %s" % BGP2_ROUTER_ID,
               "network %s/%s" % (BGP2_NETWORK, BGP_NETWORK_PL),
               "neighbor %s remote-as %s" % (BGP2_NEIGHBOR, BGP2_NEIGHBOR_ASN),
               "neighbor %s password %s" % (BGP2_NEIGHBOR,
                                            BGP2_NEIGHBOR_PASSWD)]

BGP_CONFIGS = [BGP1_CONFIG, BGP2_CONFIG]

NUM_OF_SWITCHES = 2
NUM_HOSTS_PER_SWITCH = 0

SWITCH_PREFIX = "s"


class myTopo(Topo):
    def build(self, hsts=0, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws

        switch = self.addSwitch("%s1" % SWITCH_PREFIX)
        switch = self.addSwitch(name="%s2" % SWITCH_PREFIX,
                                cls=PEER_SWITCH_TYPE,
                                **self.sopts)

        # Connect the switches
        for i in irange(2, sws):
            self.addLink("%s%s" % (SWITCH_PREFIX, i-1),
                         "%s%s" % (SWITCH_PREFIX, i))


class bgpTest(OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=SWITCH_TYPE,
                           host=OpsVsiHost,
                           link=OpsVsiLink,
                           controller=None,
                           build=True)

    def configure_switch_ips(self):
        info("\n########## Configuring switch IPs.. ##########\n")

        i = 0
        for switch in self.net.switches:
            # Configure the IPs between the switches
            if isinstance(switch, VsiOpenSwitch):
                switch.cmdCLI("configure terminal")
                switch.cmdCLI("interface 1")
                switch.cmdCLI("no shutdown")
                switch.cmdCLI("ip address %s/%s" % (BGP_ROUTER_IDS[i],
                                                    BGP_NETWORK_PL))
                switch.cmdCLI("exit")
            else:
                switch.setIP(ip=BGP_ROUTER_IDS[i],
                             intf="%s-eth1" % switch.name)
            i += 1

    def configure_bgp(self):
        info("\n########## Configuring BGP on all switches.. ##########\n")

        i = 0
        for switch in self.net.switches:
            cfg_array = BGP_CONFIGS[i]
            i += 1

            SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

    def verify_bgp_running(self):
        info("\n########## Verifying bgp processes.. ##########\n")

        for switch in self.net.switches:
            pid = switch.cmd("pgrep -f bgpd").strip()
            assert (pid != ""), "bgpd process not running on switch %s" % \
                                switch.name

            info("### bgpd process exists on switch %s ###\n" % switch.name)

    def verify_neighbor_password(self):
        info("\n########## Verifying neighbor password ##########\n")

        switch = self.net.switches[1]
        found = SwitchVtyshUtils.wait_for_route(switch, BGP1_NETWORK,
                                                BGP1_ROUTER_ID)

        assert found, "TCP connection not established(%s -> %s) on %s" % \
                      (BGP1_NETWORK, BGP1_ROUTER_ID, switch.name)

        info("### Connection established succesfully ###\n")

    def change_password(self, password):
        info("### Changing password to \"%s\" ###\n" % password)
        switch = self.net.switches[0]
        cfg_array = []
        cfg_array.append("router bgp %s" % BGP1_ASN)
        cfg_array.append("neighbor %s password %s" % (BGP1_NEIGHBOR, password))
        SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

    def change_to_no_neighbor_password(self):
        info("### Unsetting password ###\n")

        switch = self.net.switches[0]
        cfg_array = []
        cfg_array.append("router bgp %s" % BGP1_ASN)
        cfg_array.append("no neighbor %s password" % BGP1_NEIGHBOR)
        SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

        switch = self.net.switches[1]
        cfg_array = []
        cfg_array.append("router bgp %s" % BGP2_ASN)
        cfg_array.append("no neighbor %s password" % BGP2_NEIGHBOR)
        SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

    def verify_no_connection(self):
        info("### Verifying no connection ###\n")

        switch = self.net.switches[1]
        verify_route_exists = False

        found = SwitchVtyshUtils.wait_for_route(switch, BGP1_NETWORK,
                                                BGP1_ROUTER_ID,
                                                verify_route_exists)

        assert not found, "TCP connection should not be established"

    def verify_incorrect_password(self):
        info("\n########## Verifying incorrect password ##########\n")

        self.change_password(BGP1_WRONG_PASSWORD)
        self.verify_no_connection()

    def verify_no_neighbor_password(self):
        info("\n########## Verifying \"no neighbor password\" ##########\n")

        self.change_to_no_neighbor_password()
        self.verify_no_connection()


class Test_bgpd_neighbor_password:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_bgpd_neighbor_password.test_var = bgpTest()

    def teardown_class(cls):
        Test_bgpd_neighbor_password.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_bgp_full(self):
        self.test_var.configure_switch_ips()
        self.test_var.configure_bgp()
        self.test_var.verify_neighbor_password()
        self.test_var.verify_incorrect_password()
        self.test_var.change_password(BGP1_PASSWORD)
        self.test_var.verify_neighbor_password()
        self.test_var.verify_no_neighbor_password()
