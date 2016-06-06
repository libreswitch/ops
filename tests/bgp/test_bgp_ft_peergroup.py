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
# This case primarily tests the peer group. The test encapsulates the following
# commands:
#   * router bgp <asn>
#   * bgp router-id <router-id>
#   * network <network>
#   * neighbor <peer-group-name> peer-group
#   * neighbor <peer> remote-as <asn>
#   * neighbor <peer> peer-group <peer-group-name>
#   * no neighbor <peer> peer-group <peer-group-name>
#
# Topology: Two switches are running BGP. Peer group configuration is used to
#           configure the neighbor from BGP1.
#
# S1 [interface 1]<--->[interface 1] S2
#

BGP1_ASN = "1"
BGP1_ROUTER_ID = "9.0.0.1"
BGP1_NETWORK = "11.0.0.0"

BGP2_ASN = "2"
BGP2_ROUTER_ID = "9.0.0.2"
BGP2_NETWORK = "12.0.0.0"

BGP1_NEIGHBOR = BGP2_ROUTER_ID
BGP1_NEIGHBOR_ASN = BGP2_ASN

BGP2_NEIGHBOR = BGP1_ROUTER_ID
BGP2_NEIGHBOR_ASN = BGP1_ASN

BGP_NETWORK_PL = "8"
BGP_NETWORK_MASK = "255.0.0.0"

BGP_ROUTER_IDS = [BGP1_ROUTER_ID, BGP2_ROUTER_ID]
BGP_PEER_GROUP = "extern-peer-group"

BGP1_CONFIG = ["router bgp %s" % BGP1_ASN,
               "bgp router-id %s" % BGP1_ROUTER_ID,
               "network %s/%s" % (BGP1_NETWORK, BGP_NETWORK_PL),
               "neighbor %s peer-group" % BGP_PEER_GROUP,
               "neighbor %s remote-as %s" % (BGP_PEER_GROUP,
                                             BGP1_NEIGHBOR_ASN),
               "neighbor %s peer-group %s" % (BGP1_NEIGHBOR, BGP_PEER_GROUP)]

BGP2_CONFIG = ["router bgp %s" % BGP2_ASN,
               "bgp router-id %s" % BGP2_ROUTER_ID,
               "network %s/%s" % (BGP2_NETWORK, BGP_NETWORK_PL),
               "neighbor %s peer-group" % BGP_PEER_GROUP,
               "neighbor %s remote-as %s" % (BGP_PEER_GROUP,
                                             BGP2_NEIGHBOR_ASN),
               "neighbor %s peer-group %s" % (BGP2_NEIGHBOR, BGP_PEER_GROUP)]

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

    def verify_bgp_running(self):
        info("\n########## Verifying bgp processes.. ##########\n")

        for switch in self.net.switches:
            pid = switch.cmd("pgrep -f bgpd").strip()
            assert (pid != ""), "bgpd process not running on switch %s" % \
                                switch.name

            info("### bgpd process exists on switch %s ###\n" % switch.name)

    def configure_bgp(self):
        info("\n########## Applying BGP configurations... ##########\n")

        i = 0
        for switch in self.net.switches:
            cfg_array = BGP_CONFIGS[i]
            i += 1

            SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

    def verify_bgp_routes(self):
        info("\n########## Verifying routes... ##########\n")

        self.verify_bgp_route(self.net.switches[0], BGP2_NETWORK,
                              BGP2_ROUTER_ID)
        self.verify_bgp_route(self.net.switches[1], BGP1_NETWORK,
                              BGP1_ROUTER_ID)

    def verify_configs(self):
        info("\n########## Verifying all configurations.. ##########\n")

        for i in range(0, len(BGP_CONFIGS)):
            bgp_cfg = BGP_CONFIGS[i]
            switch = self.net.switches[i]

            for cfg in bgp_cfg:
                res = SwitchVtyshUtils.verify_cfg_exist(switch, [cfg])
                assert res, "Config \"%s\" was not correctly configured!" % cfg

        info("### All configurations were verified successfully ###\n")

    def verify_bgp_route(self, switch, network, next_hop):
        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Could not find route (%s -> %s) on %s" % \
                      (network, next_hop, switch.name)

    def unconfigure_peer_group(self):
        switch = self.net.switches[0]

        info("\n########## Unconfiguring peer-group on %s ##########\n" %
             switch.name)

        cfg_array = []
        cfg_array.append("router bgp %s" % BGP1_ASN)
        cfg_array.append("no neighbor %s peer-group %s" % (BGP1_NEIGHBOR,
                                                           BGP_PEER_GROUP))

        SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

    def verify_bgp_route_removed(self):
        info("\n########## Verifying route removed after "
             "peer removed from peer-group ##########\n")

        switch = self.net.switches[1]
        network = BGP1_NETWORK
        next_hop = BGP1_ROUTER_ID
        verify_route_exists = False

        # Verify that the neighbor's route info should be removed.
        found = SwitchVtyshUtils.wait_for_route(switch, network,
                                                next_hop,
                                                verify_route_exists)

        assert not found, "Route still exists! (%s -> %s) on %s" % \
                          (network, next_hop, switch.name)

    def verify_no_peer_group(self):
        info("\n########### Verifying no peer-group ##########\n")
        info("### Removing peer-group ###\n")

        switch = self.net.switches[0]
        cfg_array = []
        cfg_array.append("router bgp %s" % BGP1_ASN)
        peer_group_cfg = "neighbor %s" % BGP_PEER_GROUP
        cfg_array.append("no %s" % peer_group_cfg)

        SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

        info("### Verifying peer-group config removed ###\n")

        exists = SwitchVtyshUtils.verify_cfg_exist(switch, [peer_group_cfg])

        assert not exists, "Peer-group was not unconfigured"

        info("### Peer-group unconfigured successfully ###\n")


@pytest.mark.skipif(True, reason="Disabling because modular framework tests "
"were enable")
class Test_bgpd_peergroup:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_bgpd_peergroup.test_var = bgpTest()

    def teardown_class(cls):
        Test_bgpd_peergroup.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_bgp_full(self):
        self.test_var.configure_switch_ips()
        self.test_var.verify_bgp_running()
        self.test_var.configure_bgp()
        self.test_var.verify_configs()
        self.test_var.verify_bgp_routes()
        self.test_var.unconfigure_peer_group()
        self.test_var.verify_bgp_route_removed()
        self.test_var.verify_no_peer_group()
