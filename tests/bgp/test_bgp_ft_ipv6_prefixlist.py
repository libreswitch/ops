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
#   * ipv6 prefix-list <prefix-list-name> seq <seq-num> (permit|deny) <prefix>
#            ge <prefix length> le <prefix length>
#   * route map <route-map-name> permit seq_num
#   *   match ipv6 address prefix-list <prefix-list>
#   *
#   * network X:X::X:X/M
#
# Topology:
#   S1 [interface 1]<--->[interface 2] S2
#
# Configuration of BGP1:
# ----------------------------------------------------------------------------
# !
# ipv6 prefix-list p1 description IPV6 Prefix Test
# ipv6 prefix-list p1 seq 10 deny 9966:1:2::/64 ge 80 le 100
# ipv6 prefix-list p1 seq 20 permit 7d5d:1:1::/64 le 70
# ipv6 prefix-list p1 seq 30 permit 5d5d:1:1::/64 le 70
# ipv6 prefix-list p1 seq 40 permit 2ccd:1:1::/64 ge 65
# ipv6 prefix-list p1 seq 50 permit 4ddc:1:1::/64
# !
# !
# route-map r2 permit 10
#     match ipv6 address prefix-list p2
# !
# router bgp 1
#     bgp router-id 9.0.0.1
#     network 2ccd:1:1::/67
#     network 5d5d:1:1::/69
#     network 7d5d:1:1::/85
#     network 9966:1:2::/85
#     neighbor 2001::2 remote-as 2
#     neighbor 2001::2 route-map r2 out
# !
# interface 1
#    no shutdown
#    ip address 9.0.0.1/8
#    ipv6 address 2001::1/64
#
#
# Configuration of BGP2:
# ----------------------------------------------------------------------------
# router bgp 2
#     bgp router-id 9.0.0.2
#     network 3dcd:1:1::/64
#     neighbor 2001::1 remote-as 1
# !
# interface 1
#    no shutdown
#    ip address 9.0.0.2/8
#    ipv6 address 2001::2/64
#
# Expected routes of BGP1:
# ----------------------------------------------------------------------------
# Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
#              i internal, S Stale, R Removed
# Origin codes: i - IGP, e - EGP, ? - incomplete
#
# Local router-id 9.0.0.1
#    Network          Next Hop            Metric LocPrf Weight Path
# *> 2ccd:1:1::/67    ::                       0      0  32768  i
# *> 3dcd:1:1::/64    2001::2                  0      0      0 2 i
# *> 4ddc:1:1::/64    ::                       0      0  32768  i
# *> 5d5d:1:1::/69    ::                       0      0  32768  i
# *> 7d5d:1:1::/85    ::                       0      0  32768  i
# *> 9966:1:2::/85    ::                       0      0  32768  i
#
#
# Expected routes of BGP2:
# ----------------------------------------------------------------------------
# Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
#              i internal, S Stale, R Removed
# Origin codes: i - IGP, e - EGP, ? - incomplete
#
# Local router-id 9.0.0.2
#   Network          Next Hop            Metric LocPrf Weight Path
#   Network          Next Hop            Metric LocPrf Weight Path
# *> 2ccd:1:1::/67    2001::1                  0      0      0 1 i
# *> 3dcd:1:1::/64    ::                       0      0  32768  i
# *> 4ddc:1:1::/64    2001::1                  0      0      0 1 i
# *> 5d5d:1:1::/69    2001::1                  0      0      0 1 i

# Total number of entries 4

NUM_OF_SWITCHES = 2
NUM_HOSTS_PER_SWITCH = 0
SWITCH_PREFIX = "s"


class myTopo(Topo):
    def build(self, hsts=0, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws

        switch = self.addSwitch("%s1" % SWITCH_PREFIX)
        switch = self.addSwitch("%s2" % SWITCH_PREFIX)

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
        j = 1
        for switch in self.net.switches:
            bgp_cfg = self.bgpConfigArr[i]


            # Configure the IPs between the switches
            if isinstance(switch, VsiOpenSwitch):
                switch.cmdCLI("configure terminal")
                switch.cmdCLI("interface 1")
                switch.cmdCLI("no shutdown")
                switch.cmdCLI("ipv6 address 2001::%s/64" % str(j) )
                switch.cmdCLI("exit")

            i += 1
            j += 1

    def setup_bgp_config(self):
        info("\n########## Setup of BGP configurations... ##########\n")

        # Create BGP configurations
        self.bgpConfig1 = BgpConfig("1", "9.0.0.1", "2ccd:1:1::")
        self.bgpConfig2 = BgpConfig("2", "9.0.0.2", "3dcd:1:1::")

        # Add additional network for BGP2.
        self.bgpConfig1.addNetwork("7d5d:1:1::")
        self.bgpConfig1.addNetwork("5d5d:1:1::")
        self.bgpConfig1.addNetwork("9966:1:2::")
        self.bgpConfig1.addNetwork("4ddc:1:1::")


        self.bgpConfigArr = [self.bgpConfig1, self.bgpConfig2]

        prefixList = PrefixListEntry("p1", 10, "deny",
                                "9966:1:2::", "64", "80", "100")

        self.bgpConfig1.prefixListEntries.append(prefixList)

        prefixList = PrefixListEntry("p1", 20, "permit",
                                "7d5d:1:1::", "64", "0", "70")

        self.bgpConfig1.prefixListEntries.append(prefixList)

        prefixList = PrefixListEntry("p1", 30, "permit",
                                "5d5d:1:1::", "64", "0", "70")

        self.bgpConfig1.prefixListEntries.append(prefixList)

        prefixList = PrefixListEntry("p1", 40, "permit",
                                "2ccd:1:1::", "64", "65", "0")

        self.bgpConfig1.prefixListEntries.append(prefixList)


        prefixList = PrefixListEntry("p1", 50, "permit",
                                "4ddc:1:1::", "64", "0", "0")

        self.bgpConfig1.prefixListEntries.append(prefixList)


    def apply_bgp_config(self):
        info("\n########## Applying BGP configurations... ##########\n")
        self.all_cfg_array = []
        i = 0
        j = 2
        for bgp_cfg in self.bgpConfigArr:
            cfg_array = []

            # Add any prefix-lists
            self.add_prefix_list_configs(bgp_cfg, cfg_array)

            if i is 0 :
                cfg_array.append("ipv6 prefix-list p1 description IPV6 Prefix Test")

            # Add route-map configs
            info("\n########## Configuring route-map and applying match ipv6"\
                 " ##########\n")
            if i is 0 :
                cfg_array.append("route-map r1 permit 10")

                cfg_array.append("match ipv6 address prefix-list p1")

            sleep(5)

            SwitchVtyshUtils.vtysh_cfg_cmd(self.net.switches[i], cfg_array)

            del cfg_array[:]

            info("\n########## Configuring router bgp ##########\n")
            # Initiate BGP configuration
            cfg_array.append("router bgp %s" % bgp_cfg.asn)
            cfg_array.append("bgp router-id %s" % bgp_cfg.routerid)

            sleep(5)

            info("\n########## Configuring IPv6 networks ##########\n")
            # Add the networks this BGP Router will be advertising
            for network in bgp_cfg.networks:
                if network == "2ccd:1:1::":
                    cfg_array.append("network %s/%s" % (network, "67"))
                elif network == "5d5d:1:1::":
                    cfg_array.append("network %s/%s" % (network, "69"))
                elif network == "7d5d:1:1::":
                    cfg_array.append("network %s/%s" % (network, "85"))
                elif network == "9966:1:2::":
                    cfg_array.append("network %s/%s" % (network, "85"))
                elif network == "3dcd:1:1::":
                    cfg_array.append("network %s/%s" % (network, "64"))
                elif network == "4ddc:1:1::":
                    cfg_array.append("network %s/%s" % (network, "64"))

            sleep(5)
            # Add the neighbors of this switch
            info("\n########## Configuring neighbors ##########\n")
            cfg_array.append("neighbor 2001::%s remote-as %s" %
                                 (str(j), str(j)))

            # Add the neighbor route-maps configs
            info("\n########## Applying route-map to neighbor ##########\n")
            if i is 0 :
                cfg_array.append("neighbor 2001::2 route-map r1 out")

            SwitchVtyshUtils.vtysh_cfg_cmd(self.net.switches[i], cfg_array)

            # Add the configuration arrays to an array so that it can be used
            # for verification later.
            self.all_cfg_array.append(cfg_array)
            i += 1
            j -= 1


    def add_prefix_list_configs(self, bgp_cfg, cfg_array):
        # Add any prefix-lists

        for prefixList in bgp_cfg.prefixListEntries:

            if prefixList.ge != '0' and prefixList.le == '0' \
                and prefixList.network != "any":
                cfg_array.append("ipv6 prefix-list %s seq %d %s %s/%s ge %s" %
                                (prefixList.name, prefixList.seq_num,
                                 prefixList.action, prefixList.network,
                                 prefixList.prefixLen, prefixList.ge))

            elif prefixList.ge == '0' and prefixList.le != '0' \
                and prefixList.network != "any" :
                cfg_array.append("ipv6 prefix-list %s seq %d %s %s/%s le %s" %
                                (prefixList.name, prefixList.seq_num,
                                 prefixList.action, prefixList.network,
                                 prefixList.prefixLen, prefixList.le))

            elif  prefixList.ge != '0' and prefixList.le != '0' \
                and prefixList.network != "any" :
                cfg_array.append("ipv6 prefix-list %s seq %d %s %s/%s ge %s"\
                                 " le %s" %
                                (prefixList.name, prefixList.seq_num,
                                 prefixList.action, prefixList.network,
                                 prefixList.prefixLen, prefixList.ge,
                                 prefixList.le))

            elif  prefixList.ge == '0' and prefixList.le == '0' \
                and prefixList.network != "any" :
                cfg_array.append("ipv6 prefix-list %s seq %d %s %s/%s" %
                                (prefixList.name, prefixList.seq_num,
                                 prefixList.action, prefixList.network,
                                 prefixList.prefixLen))

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
        self.verify_bgp_running()
        for switch in self.net.switches:
            bgp_cfg_array = self.all_cfg_array[i]

            for cfg in bgp_cfg_array:
                res = SwitchVtyshUtils.verify_cfg_exist(switch, [cfg])
                assert res, "Config \"%s\" was not correctly configured!" % cfg

            i += 1

        info("### All configurations were verified successfully ###\n")

    def verify_bgp_routes(self):
        info("\n########## Verifying routes... ##########\n")

        # For each switch, verify the number of routes received
        self.verify_routes_received()


    def verify_routes_received(self):
        info("### Verifying routes received... ###\n")

        switch = self.net.switches[1]
        next_hop = "2001::1"

        # First network of BGP1 should be permitted
        network = "2ccd:1:1::"

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)

        # Second network of BGP1 should  be permitted
        network = "5d5d:1:1::/69"

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)

        # Third network of BGP1 should NOT be permitted
        network = "7d5d:1:1::/85"
        verify_route_exists = False

        info("### Verifying routes for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should NOT exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop,
                                                verify_route_exists)

        assert not found, "Route %s -> %s does not exist on %s" % \
                          (network, next_hop, switch.name)

        # Fourth network of BGP1 should NOT be permitted
        network = "9966:1:2::/85"
        verify_route_exists = False

        info("### Verifying routes for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should NOT exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop,
                                                verify_route_exists)

        assert not found, "Route %s -> %s does not exist on %s" % \
                          (network, next_hop, switch.name)

        # Fiftth network of BGP1 should be permitted
        network = "4ddc:1:1::/64"
        verify_route_exists = False

        info("### Verifying route for switch %s ###\n" % switch.name)
        info("### Network: %s, Next-hop: %s - Should exist... ###\n" %
             (network, next_hop))

        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, switch.name)


    def verify_no_ip_prefix_list(self):
        info("\n########## Verifying no ip prefix-list ##########\n")
        switch = self.net.switches[0]

        for prefixList in self.bgpConfig1.prefixListEntries:
            if prefixList.ge == '0' and prefixList.le != '0':
                     cfg = "ipv6 prefix-list %s seq %d %s %s/%s le %s" % (prefixList.name,
                                                                  prefixList.seq_num,
                                                                  prefixList.action,
                                                                  prefixList.network,
                                                                  prefixList.prefixLen,
                                                                  prefixList.le)

            elif prefixList.ge != '0' and prefixList.le ==  '0':
                     cfg = "ipv6 prefix-list %s seq %d %s %s/%s ge %s" % (prefixList.name,
                                                                  prefixList.seq_num,
                                                                  prefixList.action,
                                                                  prefixList.network,
                                                                  prefixList.prefixLen,
                                                                  prefixList.ge)

            elif prefixList.ge != '0' and prefixList.le !=  '0':
                     cfg = "ipv6 prefix-list %s seq %d %s %s/%s ge %s le %s" % (prefixList.name,
                                                                  prefixList.seq_num,
                                                                  prefixList.action,
                                                                  prefixList.network,
                                                                  prefixList.prefixLen,
                                                                  prefixList.ge,
                                                                  prefixList.le)

            else :
                     cfg = "ipv6 prefix-list %s seq %d %s %s/%s" % (prefixList.name,
                                                                  prefixList.seq_num,
                                                                  prefixList.action,
                                                                  prefixList.network,
                                                                  prefixList.prefixLen)
            cmd = "no %s" % cfg

            info("### Unconfiguring ipv6 prefix-list %s ###\n" % prefixList.name)
            SwitchVtyshUtils.vtysh_cfg_cmd(switch, [cmd])

            info("### Checking ipv6 prefix-list config ###\n")
            exists = SwitchVtyshUtils.verify_cfg_exist(switch, [cfg])
            assert not exists, "Config \"%s\" was not removed" % cfg

        info("### ipv6 prefix-list configs were successfully removed ###\n")


class Test_bgpd_ipv6:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_bgpd_ipv6.test_var = bgpTest()

    def teardown_class(cls):
        Test_bgpd_ipv6.test_var.net.stop()

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
