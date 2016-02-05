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
#   * ip prefix-list <prefix-list-name> seq <seq-num> (permit|deny) <prefix>
#              ge <prefix length> le <prefix length>
#
#   * neighbor <neighbor-router-id> route-map <prefix-list> (in|out)
#
# Topology:
#   S1 [interface 1]<--->[interface 2] S2
#
# Configuration of BGP1:
# ----------------------------------------------------------------------------
# !
# router bgp 1
#  bgp router-id 8.0.0.1
#  network 9.0.0.0/8
#  neighbor 8.0.0.2 remote-as 2
#  neighbor 8.0.0.2 route-map BGP1_IN in
# !
# ip prefix-list BGP1_IN seq 5 deny 11.0.0.0/8
# ip prefix-list BGP1_IN seq 10 permit 10.0.0.0/8
# ip prefix-list BGP1_IN seq 15 permit 150.168.15.0/24 ge 25 le 28
# ip prefix-list BGP1_IN seq 20 permit 192.168.15.0/24 ge 27
# ip prefix-list BGP1_IN seq 25 deny 192.168.15.0/24 le 25
# !
# route-map BGP1_IN permit 5
#  description A route-map description for testing.
#  match ip address prefix-list BGP1_IN
# !
#
# Configuration of BGP2:
# ----------------------------------------------------------------------------
# !
# router bgp 2
#  bgp router-id 8.0.0.2
#  network 10.0.0.0/8
#  network 11.0.0.0/8
#  network 150.168.15.64/26
#  network 192.168.15.128/25
#  network 192.168.15.16/28
#  network 192.168.15.32/27
#  neighbor 8.0.0.1 remote-as 1
# !
#
# Expected routes of BGP1:
# ----------------------------------------------------------------------------
# BGP table version is 0, local router ID is 8.0.0.1
#    Network          Next Hop            Metric LocPrf Weight Path
# *> 9.0.0.0          0.0.0.0                  0         32768 i
# *> 10.0.0.0         8.0.0.2                  0             0 2 i
# *> 150.168.15.64/26 8.0.0.2                  0      0      0 2 i
# *> 192.168.15.16/28 8.0.0.2                  0      0      0 2 i
# *> 192.168.15.32/27 8.0.0.2                  0      0      0 2 i

#
# Expected routes of BGP2:
# ----------------------------------------------------------------------------
# BGP table version is 0, local router ID is 8.0.0.2
# Origin codes: i - IGP, e - EGP, ? - incomplete
#
#    Network            Next Hop            Metric LocPrf Weight Path
# *> 9.0.0.0            8.0.0.1                  0             0  1 i
# *> 10.0.0.0           0.0.0.0                  0         32768  i
# *> 11.0.0.0           0.0.0.0                  0         32768  i
# *> 150.168.15.64/26   0.0.0.0                  0      0  32768  i
# *> 192.168.15.128/25  0.0.0.0                  0      0  32768  i
# *> 192.168.15.16/28   0.0.0.0                  0      0  32768  i
# *> 192.168.15.32/27   0.0.0.0                  0      0  32768  i

NUM_OF_SWITCHES = 2
NUM_HOSTS_PER_SWITCH = 0
SWITCH_PREFIX = "s"

DEFAULT_PL = "8"
DEFAULT_NETMASK = "255.0.0.0"


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
        self.bgpConfig2 = BgpConfig("2", "8.0.0.2", "10.0.0.0")
        # Add additional network for BGP2.
        self.bgpConfig2.addNetwork("11.0.0.0")
        self.bgpConfig2.addNetwork("150.168.15.64")
        self.bgpConfig2.addNetwork("192.168.15.16")
        self.bgpConfig2.addNetwork("192.168.15.128")
        self.bgpConfig2.addNetwork("192.168.15.32")



        # Add the neighbors for each BGP config
        self.bgpConfig1.addNeighbor(self.bgpConfig2)
        self.bgpConfig2.addNeighbor(self.bgpConfig1)

        self.bgpConfigArr = [self.bgpConfig1, self.bgpConfig2]

        # Configure "deny" for "in" of the second network of BGP2
        neighbor = self.bgpConfig1.neighbors[0]
        network = neighbor.networks[1]
        prefixList = PrefixList("BGP%s_IN" % self.bgpConfig1.asn, 5, "deny",
                                network, DEFAULT_PL)

        self.bgpConfig1.prefixLists.append(prefixList)
        self.bgpConfig1.addRouteMap(neighbor, prefixList, "in", "permit")

        # Configure so that the other route can be permitted
        network = neighbor.networks[0]
        prefixList = PrefixList("BGP%s_IN" % self.bgpConfig1.asn, 10, "permit",
                                network, DEFAULT_PL)

        self.bgpConfig1.prefixLists.append(prefixList)

        # ip prefix-list WORD seq num permit prefix ge <length> le <length>

        prefixList = PrefixListEntry("BGP%s_IN" % self.bgpConfig1.asn, 15, "permit",
                                "150.168.15.0", "24", "25", "28")

        self.bgpConfig1.prefixListEntries.append(prefixList)

        prefixList = PrefixListEntry("BGP%s_IN" % self.bgpConfig1.asn, 20, "permit",
                                "192.168.15.0", "24", "27", "0")

        self.bgpConfig1.prefixListEntries.append(prefixList)

        prefixList = PrefixListEntry("BGP%s_IN" % self.bgpConfig1.asn, 25, "deny",
                                "192.168.15.0", "24", "0", "25")

        self.bgpConfig1.prefixListEntries.append(prefixList)


    def apply_bgp_config(self):
        info("\n########## Applying BGP configurations... ##########\n")
        self.all_cfg_array = []

        i = 0
        for bgp_cfg in self.bgpConfigArr:
            info("### Applying configurations for BGP: %s ###\n" %
                 bgp_cfg.routerid)
            cfg_array = []

            # Add any prefix-lists
            self.add_prefix_list_configs(bgp_cfg, cfg_array)

            # Add route-map configs
            self.add_route_map_configs(bgp_cfg, cfg_array)

            SwitchVtyshUtils.vtysh_cfg_cmd(self.net.switches[i], cfg_array)

            del cfg_array[:]

            # Initiate BGP configuration
            cfg_array.append("router bgp %s" % bgp_cfg.asn)
            cfg_array.append("bgp router-id %s" % bgp_cfg.routerid)

            # Add the networks this bgp will be advertising
            for network in bgp_cfg.networks:
                if network == "150.168.15.64":
                    cfg_array.append("network %s/%s" % (network, "26"))
                elif network == "192.168.15.128":
                    cfg_array.append("network %s/%s" % (network, "25"))
                elif network == "192.168.15.32":
                    cfg_array.append("network %s/%s" % (network, "27"))
                elif network == "192.168.15.16":
                    cfg_array.append("network %s/%s" % (network, "28"))
                else :
                    cfg_array.append("network %s/%s" % (network, DEFAULT_PL))

            # Add the neighbors of this switch
            for neighbor in bgp_cfg.neighbors:
                cfg_array.append("neighbor %s remote-as %s" %
                                 (neighbor.routerid, neighbor.asn))

            # Add the neighbor route-maps configs
            self.add_neighbor_route_map_configs(bgp_cfg, cfg_array)

            SwitchVtyshUtils.vtysh_cfg_cmd(self.net.switches[i], cfg_array)

            # Add the configuration arrays to an array so that it can be used
            # for verification later.
            self.all_cfg_array.append(cfg_array)

            i += 1

    def add_route_map_configs(self, bgp_cfg, cfg_array):
        for routeMap in bgp_cfg.routeMaps:
            prefixList = routeMap[1]
            action = routeMap[3]
            cfg_array.append("route-map %s %s %d" %
                             (prefixList.name, action,
                              prefixList.seq_num))


            cfg_array.append("match ip address prefix-list %s" %
                             prefixList.name)


    def add_prefix_list_configs(self, bgp_cfg, cfg_array):
        # Add any prefix-lists
        for prefixList in bgp_cfg.prefixLists:
            cfg_array.append("ip prefix-list %s seq %d %s %s/%s" %
                                (prefixList.name, prefixList.seq_num,
                                 prefixList.action, prefixList.network,
                                 prefixList.prefixLen))
        for prefixList in bgp_cfg.prefixListEntries:
            if prefixList.ge != '0' and prefixList.le == '0' \
                and prefixList.network != "any":
                cfg_array.append("ip prefix-list %s seq %d %s %s/%s ge %s" %
                                (prefixList.name, prefixList.seq_num,
                                 prefixList.action, prefixList.network,
                                 prefixList.prefixLen, prefixList.ge))

            elif prefixList.ge == '0' and prefixList.le != '0' \
                and prefixList.network != "any" :
                cfg_array.append("ip prefix-list %s seq %d %s %s/%s le %s" %
                                (prefixList.name, prefixList.seq_num,
                                 prefixList.action, prefixList.network,
                                 prefixList.prefixLen, prefixList.le))

            elif prefixList.network == "any":
               cfg_array.append("ip prefix-list %s seq %d %s %s" %
                                (prefixList.name, prefixList.seq_num,
                                 prefixList.action, prefixList.network))

            else :
                cfg_array.append("ip prefix-list %s seq %d %s %s/%s ge %s le %s" %
                                (prefixList.name, prefixList.seq_num,
                                 prefixList.action, prefixList.network,
                                 prefixList.prefixLen, prefixList.ge,
                                 prefixList.le))


    def add_neighbor_route_map_configs(self, bgp_cfg, cfg_array):
        # Add the route-maps
        for routeMap in bgp_cfg.routeMaps:
            neighbor = routeMap[0]
            prefixList = routeMap[1]
            dir = routeMap[2]

            cfg_array.append("neighbor %s route-map %s %s" %
                             (neighbor.routerid, prefixList.name, dir))

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
        neighbor = self.bgpConfig1.neighbors[0]
        next_hop = neighbor.routerid

        # First network of BGP2 should be permitted
        network = neighbor.networks[0]

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)

        # Second network of BGP2 should NOT be permitted
        network = neighbor.networks[1]
        verify_route_exists = False

        info("### Verifying routes for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should NOT exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop,
                                                verify_route_exists)

        assert not found, "Route %s -> %s does not exist on %s" % \
                          (network, next_hop, switch.name)

        # Third network of BGP2 should be permitted
        network = neighbor.networks[2]

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)


        # Fourth network of BGP2 should be permitted
        network = neighbor.networks[3]

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)


        # Fifth network of BGP2 should NOT be permitted
        network = neighbor.networks[4]
        verify_route_exists = False

        info("### Verifying routes for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should NOT exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop,
                                                verify_route_exists)

        assert not found, "Route %s -> %s does not exist on %s" % \
                          (network, next_hop, switch.name)


        # Sixth network of BGP2 should be permitted
        network = neighbor.networks[5]

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)


    def verify_no_ip_prefix_list(self):
        info("\n########## Verifying no ip prefix-list ##########\n")
        switch = self.net.switches[0]
        for prefixList in self.bgpConfig1.prefixLists:
            cfg = "ip prefix-list %s seq %d %s %s/%s" % (prefixList.name,
                                                                  prefixList.seq_num,
                                                                  prefixList.action,
                                                                  prefixList.network,
                                                                  prefixList.prefixLen)
            cmd = "no %s" % cfg

            info("### Unconfiguring ip prefix-list %s ###\n" % prefixList.name)
            SwitchVtyshUtils.vtysh_cfg_cmd(switch, [cmd])

            info("### Checking ip prefix-list config ###\n")
            exists = SwitchVtyshUtils.verify_cfg_exist(switch, [cfg])
            assert not exists, "Config \"%s\" was not removed" % cfg

        for prefixList in self.bgpConfig1.prefixListEntries:
            if prefixList.ge == '0' and prefixList.le != '0':
                     cfg = "ip prefix-list %s seq %d %s %s/%s le %s" % (prefixList.name,
                                                                  prefixList.seq_num,
                                                                  prefixList.action,
                                                                  prefixList.network,
                                                                  prefixList.prefixLen,
                                                                  prefixList.le)

            elif prefixList.ge != '0' and prefixList.le == '0':
                     cfg = "ip prefix-list %s seq %d %s %s/%s ge %s" % (prefixList.name,
                                                                  prefixList.seq_num,
                                                                  prefixList.action,
                                                                  prefixList.network,
                                                                  prefixList.prefixLen,
                                                                  prefixList.ge)

            else:
                     cfg = "ip prefix-list %s seq %d %s %s/%s ge %s le %s" % (prefixList.name,
                                                                  prefixList.seq_num,
                                                                  prefixList.action,
                                                                  prefixList.network,
                                                                  prefixList.prefixLen,
                                                                  prefixList.ge,
                                                                  prefixList.le)


            cmd = "no %s" % cfg

            info("### Unconfiguring ip prefix-list %s ###\n" % prefixList.name)
            SwitchVtyshUtils.vtysh_cfg_cmd(switch, [cmd])

            info("### Checking ip prefix-list config ###\n")
            exists = SwitchVtyshUtils.verify_cfg_exist(switch, [cfg])
            assert not exists, "Config \"%s\" was not removed" % cfg

        info("### ip prefix-list configs were successfully removed ###\n")


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
        self.test_var.verify_no_ip_prefix_list()
