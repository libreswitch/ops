#!/usr/bin/env python

# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
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

"""Layer 3 test file.

Name:
    test_layer3_ft_lag_fastpath_routed

Objective:
    To verify the correct functionality of a layer 3 configuration over a
    configured LAG.

Topology:
    2 switches
    2 hosts
"""

from opstestfw.switch.CLI import (
    InterfaceEnable,
    InterfaceIpConfig,
    InterfaceLagIdConfig,
    IpRouteConfig,
    lagCreation
)

from opstestfw.testEnviron import LogOutput, testEnviron


# Topology definition
topoDict = {'topoExecution': 1000,
            'topoTarget': 'dut01 dut02',
            'topoType': 'physical',
            'topoDevices': 'dut01 dut02 wrkston01 wrkston02',
            'topoLinks': 'lnk01:dut01:wrkston01,'
                         'lnk04:dut02:wrkston02,'
                         'lnk02:dut01:dut02,'
                         'lnk03:dut01:dut02',
            'topoFilters': 'dut01:system-category:switch,'
                           'dut02:system-category:switch,'
                           'wrkston01:system-category:workstation,'
                           'wrkston02:system-category:workstation'}


def fastpath_ping(**kwargs):
    """Test description.

    Topology:

        [h1] <-----> [s1] <-----> [s2] <-----> [h2]

    Objective:
        Test successful and failure ping executions betwen h1 and h2 through
        two switches configured with static routes and a LAG. The ping
        executions will be done using IPv4 and IPv6.

    Cases:
        - Execute successful pings between hosts with static routes configured.
        - Execute unsuccessful pings between hosts when there are no static
          routes configured.
    """
    switch1 = kwargs.get('device1', None)
    switch2 = kwargs.get('device2', None)
    host1 = kwargs.get('device3', None)
    host2 = kwargs.get('device4', None)

    ###########################################################################
    #                                                                         #
    #                   [H1] ------- ping -------> [H2]                       #
    #                                                                         #
    ###########################################################################
    LogOutput('info', 'Pinging host 1 to host 2 using IPv4')
    ret_struct = host1.Ping(ipAddr='10.0.30.1', packetCount=5)

    assert not ret_struct.returnCode(), 'Failed to do IPv4 ping'

    LogOutput('info', 'IPv4 Ping from host 1 to host 2 return JSON:\n')
    ret_struct.printValueString()
    LogOutput('info', 'IPv4 Ping Passed')

    LogOutput('info', 'Pinging host 1 to host 2 using IPv6')
    ret_struct = host1.Ping(ipAddr='2002::1', packetCount=5, ipv6Flag=True)

    assert not ret_struct.returnCode(), 'Failed to do IPv6 ping'

    LogOutput('info', 'IPv6 Ping from host 1 to host 2 return JSON:\n')
    ret_struct.printValueString()
    LogOutput('info', 'IPv6 Ping Passed')

    ###########################################################################
    #                                                                         #
    #                   [H1] <------- ping ------- [H2]                       #
    #                                                                         #
    ###########################################################################
    LogOutput('info', 'Pinging host 2 to host 1 using IPv4')
    ret_struct = host2.Ping(ipAddr='10.0.10.1', packetCount=5)

    assert not ret_struct.returnCode(), 'Failed to do IPv4 ping'

    LogOutput('info', 'IPv4 Ping from host 2 to host 1 return JSON:\n')
    ret_struct.printValueString()
    LogOutput('info', 'IPv4 Ping Passed')

    LogOutput('info', 'Pinging host 2 to host 1 using IPv6')
    ret_struct = host2.Ping(ipAddr='2000::1', packetCount=5, ipv6Flag=True)

    assert not ret_struct.returnCode(), 'Failed to do IPv6 ping'

    LogOutput('info', 'IPv6 Ping from host 2 to host 1 return JSON:\n')
    ret_struct.printValueString()
    LogOutput('info', 'IPv6 Ping Passed')

    ###########################################################################
    # Removing static routes                                                  #
    ###########################################################################
    LogOutput('info', 'Removing static Routes on s1 and s2')
    ret_struct = IpRouteConfig(deviceObj=switch1,
                               route='10.0.30.0',
                               mask=24,
                               nexthop='10.0.20.2',
                               config=False)
    assert not ret_struct.returnCode(), \
        'Failed to unconfigure IPv4 address route'

    ret_struct = IpRouteConfig(deviceObj=switch2,
                               route='10.0.10.0',
                               mask=24,
                               nexthop='10.0.20.1',
                               config=False)
    assert not ret_struct.returnCode(), \
        'Failed to unconfigure IPv4 address route'

    ret_struct = IpRouteConfig(deviceObj=switch1,
                               route='2002::',
                               mask=120,
                               nexthop='2001::2',
                               config=False,
                               ipv6flag=True)
    assert not ret_struct.returnCode(), \
        'Failed to unconfigure IPv6 address route'

    ret_struct = IpRouteConfig(deviceObj=switch2,
                               route='2000::',
                               mask=120,
                               nexthop='2001::1',
                               config=False,
                               ipv6flag=True)
    assert not ret_struct.returnCode(), \
        'Failed to unconfigure IPv6 address route'

    LogOutput('info', 'Ping after removing static route from S1 and S2')
    ###########################################################################
    #                                                                         #
    #                   [H1] ------- ping -------> [H2]                       #
    #                                                                         #
    ###########################################################################
    # IPv4
    LogOutput('info', 'Pinging host 1 to host 2 using IPv4')
    ret_struct = host1.Ping(ipAddr='10.0.30.1', packetCount=1)

    assert ret_struct.returnCode(), 'Failed: Successful IPv4 ping done!'

    LogOutput('info', 'IPv4 Ping from host 1 to host 2 return JSON:\n')
    ret_struct.printValueString()
    LogOutput('info', 'IPv4 Ping Passed')

    # IPv6
    LogOutput('info', 'Pinging host 1 to host 2 using IPv6')
    ret_struct = host1.Ping(ipAddr='2002::1', packetCount=1, ipv6Flag=True)

    assert ret_struct.returnCode(), 'Failed: Successful IPv6 ping done!'

    LogOutput('info', 'IPv6 Ping from host 1 to host 2 return JSON:\n')
    ret_struct.printValueString()
    LogOutput('info', 'IPv6 Ping Passed')

    ###########################################################################
    #                                                                         #
    #                   [H1] <------- ping ------- [H2]                       #
    #                                                                         #
    ###########################################################################
    # IPv4
    LogOutput('info', 'Pinging host 2 to host 1 using IPv4')
    ret_struct = host2.Ping(ipAddr='10.0.10.1', packetCount=1)

    assert ret_struct.returnCode(), 'Failed: Successful IPv4 ping done!'

    LogOutput('info', 'IPv4 Ping from host 2 to host 1 return JSON:\n')
    ret_struct.printValueString()
    LogOutput('info', 'IPv4 Ping Passed')

    # IPv6
    LogOutput('info', 'Pinging host 2 to host 1 using IPv6')
    ret_struct = host2.Ping(ipAddr='2000::1', packetCount=1, ipv6Flag=True)

    assert ret_struct.returnCode(), 'Failed: Successful IPv6 ping done!'

    LogOutput('info', 'IPv6 Ping from host 2 to host 1 return JSON:\n')
    ret_struct.printValueString()
    LogOutput('info', 'IPv6 Ping Passed')


class TestFastpathPing:
    """Test Configuration Class for Fastpath Ping.

    Topology:
        - Switch 1
        - Switch 2
        - Workstation 1
        - Workstation 2

    Test Cases:
        - test_fastpath_ping
    """

    @classmethod
    def setup_class(cls):
        """Class configuration method executed after class is instantiated.

        Test topology is created and Topology object is stored as topoObj
        """
        # Test object will parse command line and formulate the env
        TestFastpathPing.testObj = testEnviron(topoDict=topoDict)
        # Get topology object
        TestFastpathPing.topoObj = TestFastpathPing.testObj.topoObjGet()

    @classmethod
    def teardown_class(cls):
        """Class configuration executed before class is destroyed.

        All docker containers are destroyed
        """
        TestFastpathPing.topoObj.terminate_nodes()

    def setup_method(self, method):
        """Class configuration method executed before running all test cases.

        All devices will be configured before running test cases.
        """
        dut01 = self.topoObj.deviceObjGet(device='dut01')
        dut02 = self.topoObj.deviceObjGet(device='dut02')
        hst01 = self.topoObj.deviceObjGet(device='wrkston01')
        hst02 = self.topoObj.deviceObjGet(device='wrkston02')

        test_lag_id = 100

        ######################################################################
        # Configuration switch 1
        ######################################################################

        # Create LAG 100
        LogOutput('info', 'Creating LAG %s on switch' % test_lag_id)
        ret_struct = lagCreation(deviceObj=dut01,
                                 lagId=test_lag_id,
                                 configFlag=True)
        assert not ret_struct.returnCode(), \
            'Unable to create LAG %s on device' % test_lag_id

        # Enable interface 1
        LogOutput('info',
                  'Enabling interface %s on device' % 'lnk01')

        ret_struct = InterfaceEnable(
                        deviceObj=dut01,
                        enable=True,
                        interface=dut01.linkPortMapping['lnk01'])
        assert not ret_struct.returnCode(), \
            'Unable to enable interface %s on device' % 'lnk01'

        # Enable interface 2
        LogOutput('info',
                  'Enabling interface %s on device' % 'lnk02')

        ret_struct = InterfaceEnable(
                        deviceObj=dut01,
                        enable=True,
                        interface=dut01.linkPortMapping['lnk02'])
        assert not ret_struct.returnCode(), \
            'Unable to enable interface %s on device' % 'lnk02'

        # Enable interface 3
        LogOutput('info',
                  'Enabling interface %s on device' % 'lnk03')

        ret_struct = InterfaceEnable(
                        deviceObj=dut01,
                        enable=True,
                        interface=dut01.linkPortMapping['lnk03'])
        assert not ret_struct.returnCode(), \
            'Unable to enable interface %s on device' % 'lnk03'

        # Configure interface IPv4 address
        LogOutput('info', 'Configuring interface IPv4 address')
        ret_struct = InterfaceIpConfig(
                        deviceObj=dut01,
                        interface=dut01.linkPortMapping['lnk01'],
                        addr='10.0.10.2',
                        mask=24,
                        config=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure interface IPv6 address
        LogOutput('info', 'Configuring interface IPv6 address')
        ret_struct = InterfaceIpConfig(
                        deviceObj=dut01,
                        interface=dut01.linkPortMapping['lnk01'],
                        addr='2000::2',
                        mask=120,
                        config=True,
                        ipv6flag=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure LAG IPv4 address
        LogOutput('info', 'Configuring LAG IPv4 address')
        ret_struct = InterfaceIpConfig(
                        deviceObj=dut01,
                        lag=test_lag_id,
                        addr='10.0.20.1',
                        mask=24,
                        config=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure LAG IPv6 address
        LogOutput('info', 'Configuring LAG IPv6 address')
        ret_struct = InterfaceIpConfig(
                        deviceObj=dut01,
                        lag=test_lag_id,
                        addr='2001::1',
                        mask=120,
                        config=True,
                        ipv6flag=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure LAG to interface 2
        LogOutput('info',
                  'Configuring LAG %s to interface %s' % (test_lag_id,
                                                          'lnk02'))

        ret_struct = InterfaceLagIdConfig(
                        deviceObj=dut01,
                        interface=dut01.linkPortMapping['lnk02'],
                        lagId=test_lag_id,
                        enable=True)
        assert not ret_struct.returnCode(), \
            'Unable to configure LAG %s to interface %s' % (test_lag_id,
                                                            'lnk02')

        # Configure LAG to interface 3
        LogOutput('info',
                  'Configuring LAG %s to interface %s' % (test_lag_id,
                                                          'lnk03'))

        ret_struct = InterfaceLagIdConfig(
                        deviceObj=dut01,
                        interface=dut01.linkPortMapping['lnk03'],
                        lagId=test_lag_id,
                        enable=True)
        assert not ret_struct.returnCode(), \
            'Unable to configure LAG %s to interface %s' % (test_lag_id,
                                                            'lnk03')

        # Configure Static Route
        # IPv4 route to interface on switch 2
        LogOutput('info', 'Configuring IPv4 static route')
        ret_struct = IpRouteConfig(deviceObj=dut01,
                                   route='10.0.30.0',
                                   mask=24,
                                   nexthop='10.0.20.2',
                                   config=True)
        assert not ret_struct.returnCode(), 'Failed to configure static route'

        # IPv6 route to interface on switch 2
        LogOutput('info', 'Configuring IPv6 static route')
        ret_struct = IpRouteConfig(deviceObj=dut01,
                                   route='2002::',
                                   mask=120,
                                   nexthop='2001::2',
                                   config=True,
                                   ipv6flag=True)
        assert not ret_struct.returnCode(), 'Failed to configure static route'

        ######################################################################
        # Configuration switch 2
        ######################################################################

        # Create LAG 100
        LogOutput('info', 'Creating LAG %s on switch' % test_lag_id)
        ret_struct = lagCreation(deviceObj=dut02,
                                 lagId=test_lag_id,
                                 configFlag=True)
        assert not ret_struct.returnCode(), \
            'Unable to create LAG %s on device' % test_lag_id

        # Enable interface 2
        LogOutput('info',
                  'Enabling interface %s on device' % 'lnk02')

        ret_struct = InterfaceEnable(
                        deviceObj=dut02,
                        enable=True,
                        interface=dut02.linkPortMapping['lnk02'])
        assert not ret_struct.returnCode(), \
            'Unable to enable interface %s on device' % 'lnk02'

        # Enable interface 3
        LogOutput('info',
                  'Enabling interface %s on device' % 'lnk03')

        ret_struct = InterfaceEnable(
                        deviceObj=dut02,
                        enable=True,
                        interface=dut02.linkPortMapping['lnk03'])
        assert not ret_struct.returnCode(), \
            'Unable to enable interface %s on device' % 'lnk03'

        # Enable interface 4
        LogOutput('info',
                  'Enabling interface %s on device' % 'lnk04')

        ret_struct = InterfaceEnable(
                        deviceObj=dut02,
                        enable=True,
                        interface=dut02.linkPortMapping['lnk04'])
        assert not ret_struct.returnCode(), \
            'Unable to enable interface %s on device' % 'lnk01'

        # Configure interface IPv4 address
        LogOutput('info', 'Configuring interface IPv4 address')
        ret_struct = InterfaceIpConfig(
                        deviceObj=dut02,
                        interface=dut02.linkPortMapping['lnk04'],
                        addr='10.0.30.2',
                        mask=24,
                        config=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure interface IPv6 address
        LogOutput('info', 'Configuring interface IPv6 address')
        ret_struct = InterfaceIpConfig(
                        deviceObj=dut02,
                        interface=dut02.linkPortMapping['lnk04'],
                        addr='2002::2',
                        mask=120,
                        config=True,
                        ipv6flag=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure LAG IPv4 address
        LogOutput('info', 'Configuring LAG IPv4 address')
        ret_struct = InterfaceIpConfig(
                        deviceObj=dut02,
                        lag=test_lag_id,
                        addr='10.0.20.2',
                        mask=24,
                        config=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure LAG IPv6 address
        LogOutput('info', 'Configuring LAG IPv6 address')
        ret_struct = InterfaceIpConfig(
                        deviceObj=dut02,
                        lag=test_lag_id,
                        addr='2001::2',
                        mask=120,
                        config=True,
                        ipv6flag=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure LAG to interface 2
        LogOutput('info',
                  'Configuring LAG %s to interface %s' % (test_lag_id,
                                                          'lnk02'))

        ret_struct = InterfaceLagIdConfig(
                        deviceObj=dut02,
                        interface=dut02.linkPortMapping['lnk02'],
                        lagId=test_lag_id,
                        enable=True)
        assert not ret_struct.returnCode(), \
            'Unable to configure LAG %s to interface %s' % (test_lag_id,
                                                            'lnk02')

        # Configure LAG to interface 3
        LogOutput('info',
                  'Configuring LAG %s to interface %s' % (test_lag_id,
                                                          'lnk03'))

        ret_struct = InterfaceLagIdConfig(
                        deviceObj=dut02,
                        interface=dut02.linkPortMapping['lnk03'],
                        lagId=test_lag_id,
                        enable=True)
        assert not ret_struct.returnCode(), \
            'Unable to configure LAG %s to interface %s' % (test_lag_id,
                                                            'lnk03')

        # Configure Static Route
        # IPv4 route to interface on switch 1
        LogOutput('info', 'Configuring IPv4 static route')
        ret_struct = IpRouteConfig(deviceObj=dut02,
                                   route='10.0.10.0',
                                   mask=24,
                                   nexthop='10.0.20.1',
                                   config=True)
        assert not ret_struct.returnCode(), 'Failed to configure static route'

        # IPv6 route to interface on switch 1
        LogOutput('info', 'Configuring IPv6 static route')
        ret_struct = IpRouteConfig(deviceObj=dut02,
                                   route='2000::',
                                   mask=120,
                                   nexthop='2001::1',
                                   config=True,
                                   ipv6flag=True)
        assert not ret_struct.returnCode(), 'Failed to configure static route'

        ######################################################################
        # Configuration host 1
        ######################################################################

        # Configure IPv4 address
        LogOutput('info', 'Configuring IPv4 Address')
        ret_struct = hst01.NetworkConfig(
                            ipAddr='10.0.10.1',
                            netMask='255.255.255.0',
                            interface=hst01.linkPortMapping['lnk01'],
                            broadcast='10.0.10.0',
                            config=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure IPv6 address
        LogOutput('info', 'Configuring IPv6 Address')
        ret_struct = hst01.Network6Config(
                            ipAddr='2000::1',
                            netMask=120,
                            interface=hst01.linkPortMapping['lnk01'],
                            broadcast='2000::0',
                            config=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure Static Routes
        # IPv4 Route to LAG on switch 2
        LogOutput('info', 'Configuring IPv4 route for host')
        ret_struct = hst01.IPRoutesConfig(destNetwork='10.0.20.0',
                                          netMask=24,
                                          gateway='10.0.10.2',
                                          config=True)
        assert not ret_struct.returnCode(), \
            'Failed to configure IP address static route'

        # IPv6 Route to LAG on switch 2
        LogOutput('info', 'Configuring IPv6 route for host')
        ret_struct = hst01.IPRoutesConfig(destNetwork='2001::0',
                                          netMask=120,
                                          gateway='2000::2',
                                          config=True,
                                          ipv6Flag=True)
        assert not ret_struct.returnCode(), \
            'Failed to configure IP address static route'

        # IPv4 Route to interface on switch 2
        LogOutput('info', 'Configuring IPv4 route for host')
        ret_struct = hst01.IPRoutesConfig(destNetwork='10.0.30.0',
                                          netMask=24,
                                          gateway='10.0.10.2',
                                          config=True)
        assert not ret_struct.returnCode(), \
            'Failed to configure IP address static route'

        # IPv6 Route to interface on switch 2
        LogOutput('info', 'Configuring IPv6 route for host')
        ret_struct = hst01.IPRoutesConfig(destNetwork='2002::0',
                                          netMask=120,
                                          gateway='2000::2',
                                          config=True,
                                          ipv6Flag=True)
        assert not ret_struct.returnCode(), \
            'Failed to configure IP address static route'

        ######################################################################
        # Configuration host 2
        ######################################################################

        # Configure IPv4 address
        LogOutput('info', 'Configuring IPv4 Address')
        ret_struct = hst02.NetworkConfig(
                            ipAddr='10.0.30.1',
                            netMask='255.255.255.0',
                            interface=hst02.linkPortMapping['lnk04'],
                            broadcast='10.0.30.0',
                            config=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure IPv6 address
        LogOutput('info', 'Configuring IPv6 Address')
        ret_struct = hst02.Network6Config(
                            ipAddr='2002::1',
                            netMask=120,
                            interface=hst02.linkPortMapping['lnk04'],
                            broadcast='2002::0',
                            config=True)
        assert not ret_struct.returnCode(), 'Failed to configure an IP address'

        # Configure Static Routes
        # IPv4 Route to LAG on switch 1
        LogOutput('info', 'Configuring IPv4 route for host')
        ret_struct = hst02.IPRoutesConfig(destNetwork='10.0.20.0',
                                          netMask=24,
                                          gateway='10.0.30.2',
                                          config=True)
        assert not ret_struct.returnCode(), \
            'Failed to configure IP address static route'

        # IPv6 Route to LAG on switch 1
        LogOutput('info', 'Configuring IPv6 route for host')
        ret_struct = hst02.IPRoutesConfig(destNetwork='2001::0',
                                          netMask=120,
                                          gateway='2002::2',
                                          config=True,
                                          ipv6Flag=True)
        assert not ret_struct.returnCode(), \
            'Failed to configure IP address static route'

        # IPv4 Route to interface on switch 1
        LogOutput('info', 'Configuring IPv4 route for host')
        ret_struct = hst02.IPRoutesConfig(destNetwork='10.0.10.0',
                                          netMask=24,
                                          gateway='10.0.30.2',
                                          config=True)
        assert not ret_struct.returnCode(), \
            'Failed to configure IP address static route'

        # IPv6 Route to interface on switch 1
        LogOutput('info', 'Configuring IPv6 route for host')
        ret_struct = hst02.IPRoutesConfig(destNetwork='2000::0',
                                          netMask=120,
                                          gateway='2002::2',
                                          config=True,
                                          ipv6Flag=True)
        assert not ret_struct.returnCode(), \
            'Failed to configure IP address static route'

    def test_fastpath_ping(self):
        """Fastpath ping case.

        Topology:
            - dut01: Switch 1
            - dut02: Switch 2
            - wrkston01: Host 1
            - wrkston02: Host 2
        """
        dut01 = self.topoObj.deviceObjGet(device='dut01')
        dut02 = self.topoObj.deviceObjGet(device='dut02')
        wrkston01 = self.topoObj.deviceObjGet(device='wrkston01')
        wrkston02 = self.topoObj.deviceObjGet(device='wrkston02')
        fastpath_ping(device1=dut01,
                      device2=dut02,
                      device3=wrkston01,
                      device4=wrkston02)
