#!/usr/bin/python

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
from opsvsiutils.vtyshutils import *
from opsvsiutils.bgpconfig import *

#
# This test checks the following commands:
# * ip as-path access-list WORD (deny|permit) .LINE
#
# * neighbor (A.B.C.D|X:X::X:X|WORD) filter-list WORD (in|out)
#
# Topology:
#   S1 [interface 1]<--->[interface 2] S2


NUM_OF_SWITCHES = 2
NUM_HOSTS_PER_SWITCH = 0
SWITCH_PREFIX = "s"

DEFAULT_PL = "8"
DEFAULT_NETMASK = "255.0.0.0"

nbrFilterLists = []
def addNbrFilterList(nbr, list_, dir_):
    nbrFilterLists.append([nbr, list_, dir_])

filterLists = []
def addFilterList(list_, dir_, asn):
    filterLists.append([list_, dir_, asn])

class myTopo(Topo):
    def build(self, hsts=0, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws

        switch = self.addSwitch("%s1" % SWITCH_PREFIX)
        switch = self.addSwitch(name="%s2" % SWITCH_PREFIX,
                                cls=PEER_SWITCH_TYPE,
                                **self.sopts)

        # Link the switches
        for i in range(1, NUM_OF_SWITCHES):
            self.addLink("%s%s" % (SWITCH_PREFIX, i),
                         "%s%s" % (SWITCH_PREFIX, i+1))


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
            bgp_cfg = self.bgpConfigArr[i]

            info("### Setting IP %s/%s on switch %s ###\n" %
                 (bgp_cfg.routerid, DEFAULT_PL, switch.name))

            # Configure the IPs between the switches
            if isinstance(switch, VsiOpenSwitch):
                switch.cmdCLI("configure terminal")
                switch.cmdCLI("interface 1")
                switch.cmdCLI("no shutdown")
                switch.cmdCLI("ip address %s/%s" % (bgp_cfg.routerid,
                                                    DEFAULT_PL))
                switch.cmdCLI("exit")
            else:
                switch.setIP(ip=bgp_cfg.routerid, intf="%s-eth1" % switch.name)

            i += 1

    def setup_bgp_config(self):
        info("\n########## Setup of BGP configurations... ##########\n")

        # Create BGP configurations
        self.bgpConfig1 = BgpConfig("1", "8.0.0.1", "9.0.0.0")
        self.bgpConfig2 = BgpConfig("2", "8.0.0.2", "11.0.0.0")

        # Add additional network for the BGPs.
        self.bgpConfig1.addNetwork("10.0.0.0")

        # Add the neighbors for each BGP config
        self.bgpConfig1.addNeighbor(self.bgpConfig2)
        self.bgpConfig2.addNeighbor(self.bgpConfig1)

        self.bgpConfigArr = [self.bgpConfig1, self.bgpConfig2]

        # Configure filter-list entries
        addFilterList("BGP%s_OUT" %(self.bgpConfig1.asn), "deny", "%s" %(self.bgpConfig2.asn))

        # Configure neighbor with filter-list
        addNbrFilterList("8.0.0.2", "BGP%s_OUT" %(self.bgpConfig1.asn), "out")

    def apply_bgp_config(self):
        info("\n########## Applying BGP configurations... ##########\n")
        self.all_cfg_array = []

        i = 0
        for bgp_cfg in self.bgpConfigArr:
            info("### Applying configurations for BGP: %s ###\n" %
                 bgp_cfg.routerid)
            cfg_array = []

            # Add any filter-lists
            self.add_filter_list_configs(bgp_cfg, cfg_array)

            print cfg_array
            SwitchVtyshUtils.vtysh_cfg_cmd(self.net.switches[i], cfg_array)

            del cfg_array[:]

            # Initiate BGP configuration
            cfg_array.append("router bgp %s" % bgp_cfg.asn)
            cfg_array.append("bgp router-id %s" % bgp_cfg.routerid)

            # Add the networks this bgp will be advertising
            for network in bgp_cfg.networks:
                cfg_array.append("network %s/%s" % (network, DEFAULT_PL))

            # Add the neighbors of this switch
            for neighbor in bgp_cfg.neighbors:
                cfg_array.append("neighbor %s remote-as %s" %
                                 (neighbor.routerid, neighbor.asn))

            if bgp_cfg.asn is "1":
                # Add the neighbor filter-list configs
                self.add_neighbor_filter_list_configs(cfg_array)

            SwitchVtyshUtils.vtysh_cfg_cmd(self.net.switches[i], cfg_array)
            print cfg_array

            # Add the configuration arrays to an array so that it can be used
            # for verification later.
            self.all_cfg_array.append(cfg_array)

            i += 1

    def add_filter_list_configs(self, bgp_cfg, cfg_array):
        # Add any filter-lists
        for filterList in filterLists:
            listName = filterList[0]
            listAction = filterList[1]
            listMatch = filterList[2]

            cfg_array.append("ip as-path access-list %s %s %s" %
                             (listName, listAction, listMatch))


    def add_neighbor_filter_list_configs(self, cfg_array):
        # Add the neighbor filter-lists
        for filterList in nbrFilterLists:
            neighbor = filterList[0]
            listName = filterList[1]
            direction = filterList[2]

            cfg_array.append("neighbor %s filter-list %s %s" %
                             (neighbor, listName, direction))

    def remove_neighbor_filter_list_configs(self, cfg_array):
        # Remove the neighbor filter-lists
        for filterList in nbrFilterLists:
            neighbor = filterList[0]
            listName = filterList[1]
            direction = filterList[2]

            cfg_array.append("no neighbor %s filter-list %s %s" %
                             (neighbor, listName, direction))

    def verify_bgp_running(self):
        info("\n########## Verifying bgp processes.. ##########\n")

        for switch in self.net.switches:
            pid = switch.cmd("pgrep -f bgpd").strip()
            assert (pid != ""), "bgpd process not running on switch %s" % \
                                switch.name

            info("### bgpd process exists on switch %s ###\n" % switch.name)

    def verify_bgp_configs(self):
        info("\n########## Verifying all configurations.. ##########\n")

        i = 0
        for switch in self.net.switches:
            bgp_cfg_array = self.all_cfg_array[i]

            for cfg in bgp_cfg_array:
                res = SwitchVtyshUtils.verify_cfg_exist(switch, [cfg])
                assert res, "Config \"%s\" was not correctly configured!" % cfg

            i += 1

        info("### All configurations were verified successfully ###\n")

    def verify_bgp_routes(self):
        info("\n########## Verifying routes... ##########\n")

        # For each bgp, verify that it is indeed advertising itself
        self.verify_advertised_routes()

        # For each switch, verify the number of routes received
        self.verify_routes_received()

    def verify_advertised_routes(self):
        info("### Verifying advertised routes... ###\n")

        i = 0
        for bgp_cfg in self.bgpConfigArr:
            switch = self.net.switches[i]

            next_hop = "0.0.0.0"

            for network in bgp_cfg.networks:
                found = SwitchVtyshUtils.wait_for_route(switch, network,
                                                        next_hop)

                assert found, "Could not find route (%s -> %s) on %s" % \
                              (network, next_hop, switch.name)

            i += 1

    def verify_routes_received(self):
        info("### Verifying routes received... ###\n")

        # Check route on switch 1
        switch = self.net.switches[0]
        neighbor = self.bgpConfig1.neighbors[0]
        network = neighbor.networks[0]
        next_hop = neighbor.routerid

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s does not exist on %s" \
                      % (network, next_hop, switch.name)

        # Check routes on switch 2
        switch = self.net.switches[1]
        neighbor = self.bgpConfig2.neighbors[0]

        # Second network should not exist.
        network = neighbor.networks[1]
        next_hop = neighbor.routerid
        route_should_exist = False

        info("### Verifying routes for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should NOT exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop,
                                                route_should_exist)

        assert not found, "Route %s -> %s exists on %s" \
                      % (network, next_hop, switch.name)

        # First network should not exist.
        network = neighbor.networks[0]

        info("### Network: %s, Next-hop: %s - Should NOT exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop,
                                                route_should_exist)

        assert not found, "Route %s -> %s exists on %s" \
                          % (network, next_hop, switch.name)

    def reconfigure_neighbor(self):
        info("### Reset connection from BGP2 via reconfiguring neighbor ###\n")
        switch = self.net.switches[1]
        neighbor = self.bgpConfig2.neighbors[0]

        cfg_array = []
        cfg_array.append("router bgp %s" % self.bgpConfig2.asn)
        cfg_array.append("no neighbor %s" % neighbor.routerid)

        SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

        info("### Waiting for route to be removed ###\n")
        network = neighbor.networks[1]
        next_hop = neighbor.routerid
        route_should_exist = False

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop,
                                                route_should_exist)

        assert not found, "Route %s -> %s exists on %s" \
                          % (network, next_hop, switch.name)

        info("### Reconfiguring neighbor (BGP1) on BGP2 ###\n")
        cfg_array = []
        cfg_array.append("router bgp %s" % self.bgpConfig2.asn)
        cfg_array.append("neighbor %s remote-as %s" % (neighbor.routerid,
                                                       neighbor.asn))
        SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

        info("### Waiting for route to be received again ###\n")

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s was not found on %s" \
                      % (network, next_hop, switch.name)


@pytest.mark.timeout(600)
class Test_bgpd_filterlist:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_bgpd_filterlist.test_var = bgpTest()

    def teardown_class(cls):
        Test_bgpd_filterlist.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_bgp_full(self):
        self.test_var.setup_bgp_config()
        self.test_var.configure_switch_ips()
        self.test_var.verify_bgp_running()
        self.test_var.apply_bgp_config()
        self.test_var.verify_bgp_configs()
        self.test_var.verify_bgp_routes()
