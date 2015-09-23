#!/usr/bin/env python

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
from halonvsi.docker import *
from halonvsi.halon import *
from halonutils.halonutil import *

class slowRoutingTests( HalonTest ):

  def setupNet(self):
    # if you override this function, make sure to
    # either pass getNodeOpts() into hopts/sopts of the topology that
    # you build or into addHost/addSwitch calls
    self.net = Mininet(topo=SingleSwitchTopo(k=2,
                                             hopts=self.getHostOpts(),
                                             sopts=self.getSwitchOpts()),
                                             switch=HalonSwitch,
                                             host=HalonHost,
                                             link=HalonLink, controller=None,
                                             build=True)

  def slow_routing_direct_connected(self):
    info("########## Verify slow path routing for directly connected hosts ##########\n")
    # configuring Halon, in the future it would be through
    # proper Halon commands
    s1 = self.net.switches[ 0 ]
    h1 = self.net.hosts[ 0 ]
    h2 = self.net.hosts[ 1 ]

    # Configure switch s1
    s1.cmdCLI("configure terminal")

    # Configure interface 1 on switch s1
    s1.cmdCLI("interface 1")
    #s1.cmdCLI("no shutdown")
    s1.cmdCLI("ip address 192.168.1.1/24")
    time.sleep(2)
    s1.cmdCLI("ipv6 address 2000::1/120")
    s1.cmdCLI("exit")

    # Configure interface 2 on switch s1
    s1.cmdCLI("interface 2")
    #s1.cmdCLI("no shutdown")
    s1.cmdCLI("ip address 192.168.2.1/24")
    time.sleep(2)
    s1.cmdCLI("ipv6 address 2002::1/120")
    s1.cmdCLI("exit")

    # HALON_TODO: Using "no shutdown" needs sleep of 10 seconds.
    # Uncomment below line and remove ovs-vsctl command once issue is resolved

    #time.sleep(10)

    # Bring interface 1 up
    s1.cmd("/usr/bin/ovs-vsctl set interface 1 user_config:admin=up")

    # Bring interface 2 up
    s1.cmd("/usr/bin/ovs-vsctl set interface 2 user_config:admin=up")

    # Configure host 1
    info("Configuring host 1 with 192.168.1.2/24\n")
    h1.cmd("ip addr add 192.168.1.2/24 dev h1-eth0")
    h1.cmd("ip route add 192.168.2.0/24 via 192.168.1.1");
    info("Configuring host 1 with 2000::2/120\n")
    h1.cmd("ip addr add 2000::2/120 dev h1-eth0")
    h1.cmd("ip route add 2002::0/120 via 2000::1")

    # Configure host 2
    info("Configuring host 2 with 192.168.2.2/24\n")
    h2.cmd("ip addr add 192.168.2.2/24 dev h2-eth0")
    h2.cmd("ip route add 192.168.1.0/24 via 192.168.2.1");
    info("Configuring host 2 with 2002::2/120\n")
    h2.cmd("ip addr add 2002::2/120 dev h2-eth0")
    h2.cmd("ip route add 2000::0/120 via 2002::1")

    # Ping from host 1 to switch
    info("Ping s1 from h1\n")
    output = h1.cmd("ping 192.168.1.1 -c2")
    status = parsePing(output)
    assert status, "Ping Failed\n"
    info("Ping Success\n")

    # Ping from host 2 to switch
    info("Ping s1 from h2\n")
    output = h2.cmd("ping 192.168.2.1 -c2")
    status = parsePing(output)
    assert status, "Ping Failed"
    info("Ping Success\n")

    # Ping from host 1 to host 2
    info("Ping h2 from h1\n")
    output = h1.cmd("ping 192.168.2.2 -c2")
    status = parsePing(output)
    assert status, "Ping Failed"
    info("Ping Success\n")

    # Ping from host 1 to switch
    info("IPv6 Ping s1 from h1\n")
    output = h1.cmd("ping6 2000::1 -c2")
    status = parsePing(output)
    assert status, "Ping Failed"
    info("Ping Success\n")

    # Ping from host 2 to switch
    info("IPv6 Ping s1 from h2\n")
    output = h2.cmd("ping6 2002::1 -c2")
    status = parsePing(output)
    assert status, "Ping Failed"
    info("Ping Success\n")

    # Ping from host 1 to host 2
    info("IPv6 Ping h2 from h1\n")
    output = h1.cmd("ping6 2002::2 -c2")
    status = parsePing(output)
    assert status, "Ping Failed"
    info("Ping Success\n")

    info("########## Slow path routing for directly connected hosts passed ##########\n")

class Test_slow_routing:

  def setup_class(cls):
    Test_slow_routing.test = slowRoutingTests()

  # Test for slow routing between directly connected hosts
  def test_slow_routing_direct_connected(self):
    self.test.slow_routing_direct_connected()

  def teardown_class(cls):
    Test_slow_routing.test.net.stop()

  def __del__(self):
    del self.test
