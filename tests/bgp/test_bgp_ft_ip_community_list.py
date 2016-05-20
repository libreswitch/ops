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

# This test checks the following commands:
#
#   * ip community-list WORD (permit | deny) .LINE
#   * route map <route-map-name> permit seq_num
#   *   match community-list WORD
#
# Topology:
#   S2[interface 1] <---> [interface 1] S1 [interface 2] <------> [interface 1]S3
#
# Configuration of BGP1:
# ----------------------------------------------------------------------------
# !
# ip community-list BGP_IN permit 2:0
# ip community-list BGP_IN deny 3:0
# !
# route-map BGP_RMAP permit 10
#     match community BGP_IN
# !
# router bgp 1
#     bgp router-id 9.0.0.1
#     network 15.0.0.0/8
#     neighbor 10.0.0.2 remote-as 3
#     neighbor 10.0.0.2 route-map BGP_RMAP in
#     neighbor 9.0.0.2 remote-as 2
#     neighbor 9.0.0.2 route-map BGP_RMAP in
# !
# interface 1
#    no shutdown
#    ip address 9.0.0.1/8
# interface 2
#    no shutdown
#    ip address 10.0.0.1/8
#
#
# Configuration of BGP2:
# ----------------------------------------------------------------------------
# !
# route-map BGP_2 permit 10
#     set community 2:0
# !
# router bgp 2
#     bgp router-id 9.0.0.2
#     network 12.0.0.0/8
#     neighbor 9.0.0.1 remote-as 1
#     neighbor 9.0.0.1 route-map BGP_2 out
# !
# interface 1
#    no shutdown
#    ip address 9.0.0.2/8
#
#
#
# Configuration of BGP3:
# -----------------------------------------------------------------------------
# !
# route-map BGP_3 permit 10
#     set community 3:0
# !
# router bgp 3
#     bgp router-id 10.0.0.2
#     network 20.0.0.0/8
#     neighbor 10.0.0.1 remote-as 1
#     neighbor 10.0.0.1 route-map BGP_3 out
# !
# interface 1
#    no shutdown
#    ip address 10.0.0.2/8
#
# Expected routes of BGP1:
# ----------------------------------------------------------------------------
# Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
#              i internal, S Stale, R Removed
# Origin codes: i - IGP, e - EGP, ? - incomplete
#
# Local router-id 9.0.0.1
#   Network          Next Hop            Metric LocPrf Weight Path
# *> 12.0.0.0/8       9.0.0.2                  0      0      0 2 i
# *> 15.0.0.0/8       0.0.0.0                  0      0  32768  i
# Total number of entries 3
#
# Expected routes of BGP2:
# -----------------------------------------------------------------------------
# Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
#              i internal, S Stale, R Removed
# Origin codes: i - IGP, e - EGP, ? - incomplete
#
# Local router-id 9.0.0.2
#   Network          Next Hop            Metric LocPrf Weight Path
# *> 12.0.0.0/8       0.0.0.0                  0      0  32768  i
# *> 15.0.0.0/8       9.0.0.1                  0      0      0 1 i
# Total number of entries 3

# Expected routes of BGP3:
# -----------------------------------------------------------------------------
# Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
#              i internal, S Stale, R Removed
# Origin codes: i - IGP, e - EGP, ? - incomplete
#
#  Local router-id 10.0.0.2
#    Network          Next Hop            Metric LocPrf Weight Path
# *> 12.0.0.0/8       10.0.0.1                 0      0      0 1 2 i
# *> 15.0.0.0/8       10.0.0.1                 0      0      0 1 i
# *> 20.0.0.0/8       0.0.0.0                  0      0  32768  i


NUM_OF_SWITCHES = 3
NUM_HOSTS_PER_SWITCH = 0
SWITCH_PREFIX = "s"

DEFAULT_PL = "8"
DEFAULT_NETMASK = "255.0.0.0"


class myTopo(Topo):
    def build(self, hsts=0, sws=3, **_opts):
        self.hsts = hsts
        self.sws = sws

        switch = self.addSwitch("%s1" % SWITCH_PREFIX)
        switch = self.addSwitch("%s2" % SWITCH_PREFIX)
        switch = self.addSwitch("%s3" % SWITCH_PREFIX)

        # Link the switches
        self.addLink("s1","s2")
        self.addLink("s3","s1")


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

            if switch.name == 's1' :
                switch.cmdCLI("configure terminal")
                switch.cmdCLI("interface 2")
                switch.cmdCLI("no shutdown")
                switch.cmdCLI("ip address 10.0.0.1/8")
                switch.cmdCLI("exit")

            # Configure the IPs between the switches
            if isinstance(switch, VsiOpenSwitch):
                switch.cmdCLI("configure terminal")
                switch.cmdCLI("interface 1")
                switch.cmdCLI("no shutdown")
                switch.cmdCLI("ip address %s/%s" % (bgp_cfg.routerid,
                                                    DEFAULT_PL))
                switch.cmdCLI("exit")

            i += 1

    def setup_bgp_config(self):
        info("\n########## Setup of BGP configurations... ##########\n")

        # Create BGP configurations
        self.bgpConfig1 = BgpConfig("1", "9.0.0.1", "15.0.0.0")
        self.bgpConfig2 = BgpConfig("2", "9.0.0.2", "12.0.0.0")
        self.bgpConfig3 = BgpConfig("3", "10.0.0.2","20.0.0.0")

        # Add the neighbors for each BGP config
        self.bgpConfig1.addNeighbor(self.bgpConfig2)
        self.bgpConfig2.addNeighbor(self.bgpConfig1)

        self.bgpConfigArr = [self.bgpConfig1, self.bgpConfig2, self.bgpConfig3]

    def apply_bgp_config(self):
        info("\n########## Applying BGP configurations... ##########\n")
        self.all_cfg_array = []

        i = 0
        for bgp_cfg in self.bgpConfigArr:
            info("### Applying configurations for BGP: %s ###\n" %
                 bgp_cfg.routerid)
            cfg_array = []

            if i == 0:
                info("### Applying community list configurations for BGP1")
                cfg_array.append("ip community-list BGP_IN permit 2:0")
                cfg_array.append("ip community-list BGP_IN deny 3:0")
                info("### Applying route-map configurations for BGP1")
                cfg_array.append("route-map BGP_RMAP permit 10")
                cfg_array.append("match community BGP_IN")

            if i == 1:
                cfg_array.append("route-map BGP_2 permit 10")
                cfg_array.append("set community 2:0")

            if i == 2:
                cfg_array.append("route-map BGP_3 permit 10")
                cfg_array.append("set community 3:0")


            SwitchVtyshUtils.vtysh_cfg_cmd(self.net.switches[i], cfg_array)

            del cfg_array[:]

            # Initiate BGP configuration
            cfg_array.append("router bgp %s" % bgp_cfg.asn)
            cfg_array.append("bgp router-id %s" % bgp_cfg.routerid)

            # Add the networks this bgp will be advertising
            for network in bgp_cfg.networks:
                cfg_array.append("network %s/%s" % (network, DEFAULT_PL))

            if i == 0:
               cfg_array.append("neighbor 10.0.0.2 remote-as 3")
               cfg_array.append("neighbor 10.0.0.2 route-map BGP_RMAP in")
               cfg_array.append("neighbor 9.0.0.2 remote-as 2")
               cfg_array.append("neighbor 9.0.0.2 route-map BGP_RMAP in")

            if i == 1:
               cfg_array.append("neighbor 9.0.0.1 remote-as 1")
               cfg_array.append("neighbor 9.0.0.1 route-map BGP_2 out")

            if i == 2:
               cfg_array.append("neighbor 10.0.0.1 remote-as 1")
               cfg_array.append("neighbor 10.0.0.1 route-map BGP_3 out")

            SwitchVtyshUtils.vtysh_cfg_cmd(self.net.switches[i], cfg_array)

            # Add the configuration arrays to an array so that it can be used
            # for verification later.
            self.all_cfg_array.append(cfg_array)

            i += 1


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

        switch = self.net.switches[0]

        # Network of BGP2 should be permitted by BGP1
        network = "12.0.0.0/8"
        next_hop = "9.0.0.2"

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)

        # Network of BGP3 should NOT be permitted by BGP1
        network = "20.0.0.0/8"
        next_hop = "10.0.0.2"
        verify_route_exists = False

        info("### Verifying routes for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should NOT exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop,
                                                verify_route_exists)

        assert not found, "Route %s -> %s does not exist on %s" % \
                          (network, next_hop, switch.name)

        # Network of BGP1 should be permitted by BGP2
        switch = self.net.switches[1]
        network = "15.0.0.0/8"
        next_hop = "9.0.0.1"

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)


        # Network of BGP1 should be permitted by BGP3
        switch = self.net.switches[2]
        network = "15.0.0.0/8"
        next_hop = "10.0.0.1"

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)


    def verify_no_ip_community(self):
        info("\n########## Verifying no ip prefix-list ##########\n")
        switch = self.net.switches[0]

        cmd = "no ip community-list BGP_IN"

        info("### Unconfiguring ip community-list BGP_IN ###\n")
        SwitchVtyshUtils.vtysh_cfg_cmd(switch, [cmd])

        cfg = "ip community-list BGP_IN permit 2:0"
        info("### Checking ip community-list config ###\n")
        exists = SwitchVtyshUtils.verify_cfg_exist(switch, [])
        assert not exists, "Config \"%s\" was not removed" % cfg

        cfg = "ip community-list BGP_IN permit 3:0"
        info("### Checking ip community-list config ###\n")
        exists = SwitchVtyshUtils.verify_cfg_exist(switch, [])
        assert not exists, "Config \"%s\" was not removed" % cfg

        info("### ip community-list  configs were successfully removed ###\n")


@pytest.mark.timeout(600)
class Test_bgpd_routemap:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_bgpd_routemap.test_var = bgpTest()

    def teardown_class(cls):
        Test_bgpd_routemap.test_var.net.stop()

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
        self.test_var.verify_no_ip_community()
