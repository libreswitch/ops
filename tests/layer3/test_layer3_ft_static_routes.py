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

from opsvsi.docker import *
from opsvsi.opsvsitest import *
from opsvsiutils.systemutil import *


class myTopo(Topo):
    """Custom Topology Example
    H1[h1-eth0]<--->[1]S1[2]<--->[2]S2[1]<--->[h2-eth0]H2
    """

    def build(self, hsts=2, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws

        # Add list of hosts
        for h in irange(1, hsts):
            host = self.addHost('h%s' % h)

        # Add list of switches
        for s in irange(1, sws):
            switch = self.addSwitch('s%s' % s)

        # Add links between nodes based on custom topo
        self.addLink('h1', 's1')
        self.addLink('h2', 's2')
        self.addLink('s1', 's2')


class staticRouteTest(OpsVsiTest):

    def setupNet(self):

        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        static_routes_topo = \
            myTopo(hsts=2, sws=2, hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(static_routes_topo, switch=VsiOpenSwitch,
                           host=Host, link=OpsVsiLink,
                           controller=None, build=True)

    def testConfigure(self):
        info('\n########## Configuring the topology ##########\n')
        s1 = self.net.switches[0]
        s2 = self.net.switches[1]
        h1 = self.net.hosts[0]
        h2 = self.net.hosts[1]

        # Configure switch s1
        s1.cmdCLI("configure terminal")

        # Configure interface 1 on switch s1
        s1.cmdCLI("interface 1")
        s1.cmdCLI("ip address 10.0.10.2/24")
        s1.cmdCLI("ipv6 address 2000::2/120")
        s1.cmdCLI("exit")

        # Configure interface 2 on switch s1
        s1.cmdCLI("interface 2")
        s1.cmdCLI("ip address 10.0.20.1/24")
        s1.cmdCLI("ipv6 address 2001::1/120")
        s1.cmdCLI("exit")

        # TODO: vtysh infra has an issue while adding and attaching
        # multiple interfaces to the vrf. Once that part of the code is fixed,
        # the following line can be removed. As of now, sometimes the interface
        # does not get added to the vrf.

        info('sw1 configured\n')

        # Configure switch s2
        s2.cmdCLI("configure terminal")

        # Configure interface 1 on switch s2
        s2.cmdCLI("interface 1")
        s2.cmdCLI("ip address 10.0.30.2/24")
        s2.cmdCLI("ipv6 address 2002::2/120")
        s2.cmdCLI("exit")

        # Configure interface 2 on switch s2
        s2.cmdCLI("interface 2")
        s2.cmdCLI("ip address 10.0.20.2/24")
        s2.cmdCLI("ipv6 address 2001::2/120")
        s2.cmdCLI("exit")

        # TODO: vtysh infra has an issue while adding and attaching
        # multiple interfaces to the vrf. Once that part of the code is fixed,
        # the following line can be removed. As of now, sometimes the interface
        # does not get added to the vrf.
        info('sw2 configured\n')

        # Configure host 1
        h1.cmd("ip addr add 10.0.10.1/24 dev h1-eth0")
        h1.cmd("ip addr add 2000::1/120 dev h1-eth0")
        h1.cmd("ip addr del 10.0.0.1/8 dev h1-eth0")

        info('host1 configured\n')

        # Configure host 2
        h2.cmd("ip addr add 10.0.30.1/24 dev h2-eth0")
        h2.cmd("ip addr add 2002::1/120 dev h2-eth0")
        h2.cmd("ip addr del 10.0.0.2/8 dev h2-eth0")

        info('host2 configured\n')

        # Add IPv4 static route on s1 and s2
        s1.cmdCLI("ip route 10.0.30.0/24 10.0.20.2")
        info('static route on sw1 configured\n')

        s2.cmdCLI("ip route 10.0.10.0/24 10.0.20.1")
        info('static route on sw2 configured\n')

        # Add IPv6 static route on s1 and s2
        s1.cmdCLI("ipv6 route 2002::0/120 2001::2")
        s2.cmdCLI("ipv6 route 2000::0/120 2001::1")

        # Add V4 default gateway on hosts h1 and h2
        h1.cmd("ip route add 10.0.20.0/24 via 10.0.10.2")
        h1.cmd("ip route add 10.0.30.0/24 via 10.0.10.2")
        h2.cmd("ip route add 10.0.10.0/24 via 10.0.30.2")
        h2.cmd("ip route add 10.0.20.0/24 via 10.0.30.2")

        # Add V6 default gateway on hosts h1 and h2
        h1.cmd("ip route add 2001::0/120 via 2000::2")
        h1.cmd("ip route add 2002::0/120 via 2000::2")
        h2.cmd("ip route add 2000::0/120 via 2002::2")
        h2.cmd("ip route add 2001::0/120 via 2002::2")

        s1.ovscmd("/usr/bin/ovs-vsctl set interface 1 user_config:admin=up")
        s1.ovscmd("/usr/bin/ovs-vsctl set interface 2 user_config:admin=up")

        s2.ovscmd("/usr/bin/ovs-vsctl set interface 1 user_config:admin=up")
        s2.ovscmd("/usr/bin/ovs-vsctl set interface 2 user_config:admin=up")

        info('admin up configured on sw1 & sw2\n')
        info('\n########## Configuration complete ##########\n')

    def testV4(self):
        info('\n########## IPv4 Ping test ##########\n')
        h1 = self.net.hosts[0]
        h2 = self.net.hosts[1]
        # Ping host2 from host1
        info('\n### Ping host2 from host1 ###\n')
        ret = h1.cmd("ping -c 1 10.0.30.1")

        status = parsePing(ret)

        # Return code means whether the test is successful
        if status:
            info('Ping Passed!\n\n')
        else:
            info('Ping Failed!\n\n')
            # return False

        # Ping host1 from host2
        info('\n### Ping host1 from host2 ###\n')
        ret = h2.cmd("ping -c 1 10.0.10.1")

        status = parsePing(ret)

        # Return code means whether the test is successful
        if status:
            info('Ping Passed!\n\n')
        else:
            info('Ping Failed!\n\n')
            # return False

        info('\n########## IPv4 Ping completed ##########\n')

    def testV6(self):
        info('\n########## IPv6 Ping test ##########\n')
        h1 = self.net.hosts[0]
        h2 = self.net.hosts[1]
        s1 = self.net.switches[0]
        s2 = self.net.switches[1]

        # TODO: For IPv6, we see that even after setting static routes
        # correctly, direct ping from h1 to h2 is not taking place.
        # After subsequent pings between adjacent devices,
        # end to end ping works. We suspect that there is some learning
        # going on in the kernel as regards to neighbour advertisements.
        # Ping s1 from host1
        info('### Ping s1 from host1 ###\n')
        ret = h1.cmd("ping6 -c 1 2000::2")

        status = parsePing(ret)

        # Return code means whether the test is successful
        if status:
            info('Ping Passed!\n\n')
        else:
            info('Ping Failed!\n\n')
            # return False

        # Ping s2 from h2
        info('### Ping s2 from h2 ###\n')
        ret = h2.cmd("ping6 -c 1 2002::2")

        status = parsePing(ret)

        # Return code means whether the test is successful
        if status:
            info('Ping Passed!\n\n')
        else:
            info('Ping Failed!\n\n')
            # return False

        # Ping s2 from s1
        info('### Ping s2 from s1 ###\n')
        ret = s1.cmd("ip netns exec swns ping6 -c 1 2001::2")

        status = parsePing(ret)

        # Return code means whether the test is successful
        if status:
            info('Ping Passed!\n\n')
        else:
            info('Ping Failed!\n\n')
            # return False

        # Ping host2 from host1
        info('### Ping host2 from host1 ###\n')
        ret = h1.cmd("ping6 -c 1 2002::1")

        status = parsePing(ret)

        # Return code means whether the test is successful
        if status:
            info('Ping Passed!\n\n')
        else:
            info('Ping Failed!\n\n')
            # return False

        # Ping host1 from host2
        info('\n### Ping host1 from host2 ###\n')
        ret = h2.cmd("ping6 -c 1 2000::1")

        status = parsePing(ret)

        # Return code means whether the test is successful
        if status:
            info('Ping Passed!\n\n')
        else:
            info('Ping Failed!\n\n')
            # return False

        info('\n########## IPv6 Ping completed ##########\n')

    def testV4_route_delete(self):
        h1 = self.net.hosts[0]
        h2 = self.net.hosts[1]
        s1 = self.net.switches[0]

        info('\n######### Verify deletion of IPv4 static routes ##########\n')
        # Ping host2 from host1
        info('\n### Ping host1 from host2 ###\n')
        ret = h1.cmd("ping -c 1 10.0.30.1")

        status = parsePing(ret)

        # Return code means whether the test is successful
        if status:
            info('Ping Passed!\n\n')
        else:
            info('Ping Failed!\n\n')
            # return False

        # Delete IPv4 route on switch1 towards host2 network
        info('\n### Delete ip route on sw1 to h2 network ###\n')
        s1.cmdCLI("no ip route 10.0.30.0/24 10.0.20.2")

        # Ping host1 from host2
        info('\n### Ping host1 from host2, it should fail ###\n')
        ret = h1.cmd("ping -c 1 10.0.30.1")

        status = parsePing(ret)
        # Test successful if ping fails
        if not status:
            info('Success: Ping Failed!\n\n')
        else:
            info('Failed: Ping Successful!\n\n')
            # return False

        info('\n########## IPv4 route delete test completed ##########\n')

    def testV6_route_delete(self):
        h1 = self.net.hosts[0]
        h2 = self.net.hosts[1]
        s1 = self.net.switches[0]

        info('\n######### Verify deletion of IPv6 static routes ##########\n')

        # Ping host1 from host2
        info('### Ping host1 from host2 ###\n')
        ret = h1.cmd("ping6 -c 1 2002::1")

        status = parsePing(ret)

        # Return code means whether the test is successful
        if status:
            info('Ping Passed!\n\n')
        else:
            info('Ping Failed!\n\n')
            # return False

        # Delete IPv6 route to host2 on switch1
        info('\n### Delete ipv6 route on sw1 to h2 network ###\n')
        s1.cmdCLI("no ipv6 route 2002::0/120 2001::2")

        # Ping host1 from host2
        info('\n### Ping host1 from host2, it should fail ###\n')
        ret = h1.cmd("ping6 -c 1 2002::1")

        status = parsePing(ret)

        # Test successful if ping fails
        if not status:
            info('Success: Ping Failed!\n\n')
        else:
            info('Failed: Ping Successful!\n\n')
            # return False

        info('\n########## IPv6 route delete test completed ##########\n')


class Test_zebra_static_routes_ft:

    def setup_class(cls):
        Test_zebra_static_routes_ft.test = staticRouteTest()

    def teardown_class(cls):
        # Stop the Docker containers, and
        # mininet topology
        Test_zebra_static_routes_ft.test.net.stop()

    def test_testConfigure(self):
        # Function to configure the topology
        self.test.testConfigure()

    def test_testV4(self):
        # Function to test V4 ping
        self.test.testV4()

    def test_testV6(self):
        # Function to test V6 ping
        self.test.testV6()

    def test_testV4_route_delete(self):
        # Function to test V4 route delete
        self.test.testV4_route_delete()

    def test_testV6_route_delete(self):
        # Function to test V6 route delete
        self.test.testV6_route_delete()

    def __del__(self):
        del self.test
