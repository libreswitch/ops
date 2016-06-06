#!/usr/bin/python

# Copyright (C) 2015-2016 Hewlett Packard Enterprise Development LP
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
# This case tests configuration between two BGP instances by
# verifying that the advertised routes are received on both instances running
# BGP. Hosts on each router also pings each other after routes are setup.
#
# The following commands are tested:
#   * ip prefix-list <list-name> seq <seq-num> (permit|deny) <network>
#   * route-map <name> permit <seq>
#   *   description <description>
#   *   match ip address prefix-list <list-name>
#   * router bgp <asn>
#   * bgp router-id <router-id>
#   * network <network>
#   * neighbor <peer-group-name> peer-group
#   * neighbor <peer-group-name> remote-as <asn>
#   * neighbor <peer> peer-group <peer-group-name>
#   * neighbor <peer> route-map <name> (in|out)
#
#   S1 [interface 1]<--->[interface 1] S2
#   |                                  |
#  H1                                  H2

BGP1_ASN = "1"
BGP1_ROUTER_ID = "9.0.0.1"
BGP1_NETWORK1 = "10.0.0.0"
BGP1_NETWORK2 = "11.0.0.0"
BGP1_NETWORK3 = "13.0.0.0"
BGP1_GATEWAY = "11.0.1.254"
BGP1_PREFIX_LIST = "BGP%s_IN" % BGP1_ASN

BGP2_ASN = "2"
BGP2_ROUTER_ID = "9.0.0.2"
BGP2_NETWORK1 = "12.0.0.0"
BGP2_GATEWAY = "12.0.1.254"
BGP2_PREFIX_LIST = "BGP%s_IN" % BGP2_ASN

BGP_GATEWAYS = [BGP1_GATEWAY, BGP2_GATEWAY]
BGP_GW_PREFIX = "24"
BGP_GW_NETMASK = "255.255.255.0"

BGP1_NEIGHBOR = BGP2_ROUTER_ID
BGP1_NEIGHBOR_ASN = BGP2_ASN

BGP2_NEIGHBOR = BGP1_ROUTER_ID
BGP2_NEIGHBOR_ASN = BGP1_ASN

BGP_NETWORK_PL = "8"
BGP_NETWORK_MASK = "255.0.0.0"
BGP_ROUTER_IDS = [BGP1_ROUTER_ID, BGP2_ROUTER_ID]

BGP_PEER_GROUP = "extern-peer-group"

BGP1_CONFIG = ["ip prefix-list %s seq 5 deny %s/%s" % (BGP1_PREFIX_LIST,
                                                       BGP1_NETWORK1,
                                                       BGP_NETWORK_PL),
               # Permit the second network to be advertised
               "ip prefix-list %s seq 10 permit %s/%s" % (BGP1_PREFIX_LIST,
                                                          BGP1_NETWORK2,
                                                          BGP_NETWORK_PL),
               "route-map %s permit 5" % BGP1_PREFIX_LIST,
               "description BGP1 Testing",
               "match ip address prefix-list %s" % BGP1_PREFIX_LIST,
               "router bgp %s" % BGP1_ASN,
               "bgp router-id %s" % BGP1_ROUTER_ID,
               "network %s/%s" % (BGP1_NETWORK1, BGP_NETWORK_PL),
               "network %s/%s" % (BGP1_NETWORK2, BGP_NETWORK_PL),
               "neighbor %s peer-group" % BGP_PEER_GROUP,
               "neighbor %s remote-as %s" % (BGP_PEER_GROUP,
                                             BGP1_NEIGHBOR_ASN),
               "neighbor %s peer-group %s" % (BGP1_NEIGHBOR, BGP_PEER_GROUP),
               "neighbor %s route-map %s out" % (BGP1_NEIGHBOR,
                                                 BGP1_PREFIX_LIST)]

BGP2_CONFIG = ["ip prefix-list %s seq 5 deny %s/%s" % (BGP2_PREFIX_LIST,
                                                       BGP1_NETWORK3,
                                                       BGP_NETWORK_PL),
               # Permit network 2 of BGP1 to be received
               "ip prefix-list %s seq 10 permit %s/%s" % (BGP2_PREFIX_LIST,
                                                          BGP1_NETWORK2,
                                                          BGP_NETWORK_PL),
               "route-map %s permit 5" % BGP2_PREFIX_LIST,
               "description BGP2 Testing",
               "match ip address prefix-list %s" % BGP2_PREFIX_LIST,
               "router bgp %s" % BGP2_ASN,
               "bgp router-id %s" % BGP2_ROUTER_ID,
               "network %s/%s" % (BGP2_NETWORK1, BGP_NETWORK_PL),
               "neighbor %s peer-group" % BGP_PEER_GROUP,
               "neighbor %s remote-as %s" % (BGP_PEER_GROUP,
                                             BGP2_NEIGHBOR_ASN),
               "neighbor %s peer-group %s" % (BGP2_NEIGHBOR, BGP_PEER_GROUP),
               "neighbor %s route-map %s in" % (BGP2_NEIGHBOR,
                                                BGP2_PREFIX_LIST)]

BGP_CONFIGS = [BGP1_CONFIG, BGP2_CONFIG]

# The host IPs are in the same network as the routers
HOST1_IP_ADDR = "11.0.1.1"
HOST2_IP_ADDR = "12.0.1.1"
HOST_IP_ADDRS = [HOST1_IP_ADDR, HOST2_IP_ADDR]

NUM_OF_SWITCHES = 2
NUM_HOSTS = 2

SWITCH_PREFIX = "s"
HOST_PREFIX = "h"

PING_ATTEMPTS = 10

class myTopo(Topo):
    def build(self, hsts=0, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws

        switch = self.addSwitch("%s1" % SWITCH_PREFIX)
        switch = self.addSwitch(name="%s2" % SWITCH_PREFIX,
                                cls=PEER_SWITCH_TYPE,
                                **self.sopts)

        # Add the hosts. One per switch.
        for i in irange(1, hsts):
            hostName = "%s%s" % (HOST_PREFIX, i)
            self.addHost(hostName)

        # Connect the hosts to the switches
        for i in irange(1, sws):
            self.addLink("%s%s" % (SWITCH_PREFIX, i),
                         "%s%s" % (HOST_PREFIX, i))

        # Connect the switches
        for i in irange(2, sws):
            self.addLink("%s%s" % (SWITCH_PREFIX, i-1),
                         "%s%s" % (SWITCH_PREFIX, i))


class bgpTest(OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS,
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
            # Configure the IPs of the interfaces
            if isinstance(switch, VsiOpenSwitch):
                # Configure the gateways for the switches
                switch.cmdCLI("configure terminal")
                switch.cmdCLI("interface 1")
                switch.cmdCLI("no shutdown")
                switch.cmdCLI("ip address %s/%s" % (BGP_GATEWAYS[i],
                                                    BGP_GW_PREFIX))
                switch.cmdCLI("exit")

                # Configure the IPs for the interfaces between the switches
                switch.cmdCLI("configure terminal")
                switch.cmdCLI("interface 2")
                switch.cmdCLI("no shutdown")
                switch.cmdCLI("ip address %s/%s" % (BGP_ROUTER_IDS[i],
                                                    BGP_NETWORK_PL))
                switch.cmdCLI("exit")
            else:
                # Configure the gateways for the switches
                switch.setIP(ip=BGP_GATEWAYS[i], prefixLen=BGP_GW_PREFIX,
                             intf="%s-eth1" % switch.name)

                # Configure the IPs for the interfaces between the switches
                switch.setIP(ip=BGP_ROUTER_IDS[i],
                             intf="%s-eth2" % switch.name)
            i += 1

        # Configure the IPs for the hosts
        i = 0
        for host in self.net.hosts:
            host.setIP(ip=HOST_IP_ADDRS[i], intf="%s-eth0" % host.name)
            host.cmd("route add default gw %s" % BGP_GATEWAYS[i])
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
            info("### Applying BGP config on switch %s ###\n" % switch.name)
            cfg_array = BGP_CONFIGS[i]
            i += 1

            SwitchVtyshUtils.vtysh_cfg_cmd(switch, cfg_array)

    def verify_bgp_routes(self):
        info("\n########## Verifying routes... ##########\n")

        info("### Checking the following routes that SHOULD exist: ###\n")
        self.verify_bgp_route_exists(self.net.switches[0],
                                     BGP2_NETWORK1,
                                     BGP2_ROUTER_ID)

        self.verify_bgp_route_exists(self.net.switches[1],
                                     BGP1_NETWORK2,
                                     BGP1_ROUTER_ID)

        info("### Checking the following routes that SHOULD NOT exist ###\n")
        self.verify_bgp_route_doesnt_exists(self.net.switches[1],
                                            BGP1_NETWORK1,
                                            BGP1_ROUTER_ID)

        self.verify_bgp_route_doesnt_exists(self.net.switches[1],
                                            BGP1_NETWORK3,
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

    def verify_bgp_route_exists(self, switch, network, next_hop):
        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop)

        assert found, "Could not find route (%s -> %s) on %s" % \
                      (network, next_hop, switch.name)

    def verify_bgp_route_doesnt_exists(self, switch, network, next_hop):
        route_should_exist = False
        found = SwitchVtyshUtils.wait_for_route(switch, network, next_hop,
                                                route_should_exist)

        assert not found, "Route should not exist (%s -> %s) on %s" % \
                          (network, next_hop, switch.name)

    def get_ping_hosts_result(self):
        h1 = self.net.hosts[0]
        h2 = self.net.hosts[1]

        info("### Ping %s from %s ###\n" % (h1.name, h2.name))
        ret = h1.cmd("ping -c 1 %s" % HOST2_IP_ADDR)
        return parsePing(ret)

    def verify_hosts_ping_OK(self):
        info("\n########## Verifying PING successful.. ##########\n")

        for i in range(PING_ATTEMPTS):
            result = self.get_ping_hosts_result()
            if result:
                break

        assert result, "PING failed"

        info("### Pings successful ###\n")

    def verify_hosts_ping_fail(self):
        info("\n########## Verifying PING Failure (negative case) ##########\n")

        result = self.get_ping_hosts_result()
        assert not result, "PING did not fail when it was supposed to."


@pytest.mark.skipif(True, reason="Disabling because modular framework tests "
"were enable")
class Test_bgpd_routemaps_with_hosts_ping:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_bgpd_routemaps_with_hosts_ping.test_var = bgpTest()

    def teardown_class(cls):
        Test_bgpd_routemaps_with_hosts_ping.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_bgp_full(self):
        self.test_var.configure_switch_ips()
        self.test_var.verify_bgp_running()
        self.test_var.verify_hosts_ping_fail()
        self.test_var.configure_bgp()
        self.test_var.verify_configs()
        self.test_var.verify_bgp_routes()
        self.test_var.verify_hosts_ping_OK()
