#!/usr/bin/env python

# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
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

import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch.OVS import *

#
# The purpose of this test is to test
# functionality of Traceroute Ip-App
#
# For this test, we need below topology
#
#       +---+----+        +--------+        +--------+
#       |        |        |        |        |        |
#       +switch1 +--------|switch2 |--------+switch3 +
#       |        |        |        |        |        |
#       +---+----+        +--------+        +--------+
#           |
#           |
#           |
#      +----+---+
#      |        |
#      +  host1 +
#      |        |
#      +--------+
#


# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02 dut03",
            "topoDevices": "dut01 dut02 dut03 wrkston01",
            "topoLinks": "lnk01:dut01:dut02,lnk02:dut02:dut03,\
                          lnk03:dut01:wrkston01",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            wrkston01:system-category:workstation"}


def configure(**kwargs):
    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)
    host1 = kwargs.get('host1', None)

    #Enabling interface 1 SW1
    LogOutput('info', "Enabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True,
                                interface=switch1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface1 on SW1"

    #Enabling interface 2 SW1
    LogOutput('info', "Enabling interface2 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True,
                                interface=switch1.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface2 on SW1"

    #Enabling interface 1 SW2
    LogOutput('info', "Enabling interface1 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface1 on SW2"

    #Enabling interface 2 SW2
    LogOutput('info', "Enabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface2 on SW2"

    #Enabling interface 2 SW3
    LogOutput('info', "Enabling interface2 on SW3")
    retStruct = InterfaceEnable(deviceObj=switch3, enable=True,
                                interface=switch3.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface2 on SW3"

    #Entering interface for link 1 SW1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="10.0.30.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 1 SW1, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="1030::1", mask=120,
                                  ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    # Entering interface for link 2 SW1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk03'],
                                  addr="10.0.10.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an ipv4 address"

    LogOutput('info', "Configuring IPv6 address on link 2 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk03'],
                                  addr="1010::2", mask=120,
                                  ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an ipv6 address"

    #Entering interface for link 1 SW2, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr="10.0.30.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 1 SW2, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr="1030::2", mask=120, ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    #Entering interface for link 2 SW2, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="10.0.40.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 2 SW2, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 2 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="2030::2", mask=120, ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    #Entering interface for link 2 SW3, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 SW3")
    retStruct = InterfaceIpConfig(deviceObj=switch3,
                                  interface=switch3.linkPortMapping['lnk02'],
                                  addr="10.0.40.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 2 SW3, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 2 SW3")
    retStruct = InterfaceIpConfig(deviceObj=switch3,
                                  interface=switch3.linkPortMapping['lnk02'],
                                  addr="2030::1", mask=120, ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    LogOutput('info', "Configuring static ipv4 route on switch1")
    retStruct = IpRouteConfig(deviceObj=switch1, route="10.0.40.0", mask=24,
                              nexthop="10.0.30.2", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv4 address route"

    LogOutput('info', "Configuring static ipv4 route on switch2")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.10.0", mask=24,
                              nexthop="10.0.30.1", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv4 address route"

    LogOutput('info', "Configuring static ipv4 route on switch3")
    retStruct = IpRouteConfig(deviceObj=switch3, route="10.0.30.0", mask=24,
                              nexthop="10.0.40.2", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv4 address route"

    LogOutput('info', "Configuring static ipv4 route on switch3")
    retStruct = IpRouteConfig(deviceObj=switch3, route="10.0.10.0", mask=24,
                              nexthop="10.0.40.2", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv4 address route"

    #Entering vtysh SW1
    retStruct = switch1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    #Entering vtysh SW2
    retStruct = switch2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    #Entering vtysh SW3
    retStruct = switch3.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "Configuring static ipv6 route on switch 1")
    devIntRetStruct = switch1.DeviceInteract(command="conf t")
    devIntRetStruct = switch1.DeviceInteract(command="ipv6"
                                             " route 2030::/120 1030::2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv6 address route"

    devIntRetStruct = switch1.DeviceInteract(command="exit")

    LogOutput('info', "Configuring static ipv6 route on switch 2")
    devIntRetStruct = switch2.DeviceInteract(command="conf t")
    devIntRetStruct = switch2.DeviceInteract(command="ipv6"
                                             " route 1010::/120 1030::1")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv6 address route"

    devIntRetStruct = switch2.DeviceInteract(command="exit")

    LogOutput('info', "Configuring static ipv6 route on switch 3")
    devIntRetStruct = switch3.DeviceInteract(command="conf t")
    devIntRetStruct = switch3.DeviceInteract(command="ipv6"
                                             " route 1030::/120 2030::2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv6 address route"

    devIntRetStruct = switch3.DeviceInteract(command="exit")

    LogOutput('info', "Configuring static ipv6 route on switch 3")
    devIntRetStruct = switch3.DeviceInteract(command="conf t")
    devIntRetStruct = switch3.DeviceInteract(command="ipv6"
                                             " route 1010::/120 2030::2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure ipv6 address route"

    devIntRetStruct = switch3.DeviceInteract(command="exit")

    # Configure host 1
    LogOutput('info', "\nConfiguring host 1 IPv4")
    retStruct = host1.NetworkConfig(ipAddr="10.0.10.1",
                                    netMask="255.255.255.0",
                                    interface=host1.linkPortMapping['lnk03'],
                                    broadcast="10.0.10.0", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    LogOutput('info', "\nConfiguring host 1 IPv6")
    retStruct = host1.Network6Config(ipAddr="1010::1", netMask=120,
                                     interface=host1.linkPortMapping['lnk03'],
                                     broadcast="1010::0", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"
    #Configuring static routes
    # Configuring static routes on host 1
    LogOutput('info', "Configuring routes on the workstations")
    retCode = host1.DeviceInteract(command="route add default gw 10.0.10.2")
    #retCode = retStruct.returnCode()
    if retCode == 0:
        LogOutput('error', "\nFailed to configure ipv4 address route")

    retStruct = host1.IPRoutesConfig(config=True, destNetwork="1030::0",
                                     netMask=120, gateway="1010::2",
                                     ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")

    retStruct = host1.IPRoutesConfig(config=True, destNetwork="2030::0",
                                     netMask=120, gateway="1010::2",
                                     ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")

    devIntRetStruct = switch1.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    devIntRetStruct = switch2.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    devIntRetStruct = switch3.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)


def traceroute_basic(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)
    host1 = kwargs.get('host1', None)

    #Traceroute with IPv4-address from switch3 to host1
    LogOutput('info', "Test traceroute with IPv4-address \
from switch3 to host1")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute 10.0.10.1")
    retCode = devIntRetStruct.get('returnCode')

    assert retCode == 0, "Failed to traceroute with IPv4-address"
    " from switch3 to host1"

    retBuffer = devIntRetStruct.get('buffer')
    assert '10.0.10.1' in retBuffer, "Traceroute with IPv4-address"
    " from switch3 to host1 failed"

    #Traceroute with hostname from switch3 to host1
    LogOutput('info', "Test traceroute with hostname from switch3 to host1")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute host1")
    retCode = devIntRetStruct.get('returnCode')

    assert retCode == 0, "Failed to traceroute with hostname"
    " from switch3 to host1"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'host1' in retBuffer, "Traceroute with hostname"
    " from switch3 to host1 failed"


def traceroute_with_options(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)
    host1 = kwargs.get('host1', None)
    #Traceroute from switch3 to host1 with the maxttl parameter
    LogOutput('info', "Test traceroute from switch3 to host1"
              " with the maxttl parameter")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute 10.0.10.1"
                                             " maxttl 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute"
    " from switch3 to host1 with the maxttl parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '10.0.10.1' in retBuffer, "Traceroute"
    "from switch3 to host1 with the maxttl parameter failed"

    #Traceroute from switch3 to host1 with the minttl parameter
    LogOutput('info', "Test traceroute from switch3 to host1"
              " with the minttl parameter")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute 10.0.10.1"
                                             " minttl 1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute"
    " from switch3 to host1 with the minttl parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '10.0.10.1' in retBuffer, "Traceroute"
    "from switch3 to host1 with the minttl parameter failed"

    #Traceroute from switch3 to host1 with the dstport parameter
    LogOutput('info', "Test traceroute from switch3 to host1"
              " with the dstport parameter")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute 10.0.10.1"
                                             " dstport 33434")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute"
    " from switch3 to host1 with the dstport parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '10.0.10.1' in retBuffer, "Traceroute"
    "from switch3 to host1 with the dstport parameter failed"

    #Traceroute from switch3 to host1 with the probes parameter
    LogOutput('info', "Test traceroute from switch3 to host1"
              " with the probes parameter")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute 10.0.10.1"
                                             " probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute"
    " from switch3 to host1 with the probes parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '10.0.10.1' in retBuffer, "Traceroute"
    "from switch3 to host1 with the probes parameter failed"

     #Traceroute from switch3 to host1 with the timeout parameter
    LogOutput('info', "Test traceroute from switch3 to host1"
              " with the timeout parameter")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute 10.0.10.1"
                                             " timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute"
    " from switch3 to host1 with the timeout parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '10.0.10.1' in retBuffer, "Traceroute"
    "from switch3 to host1 with the timeout parameter failed"


def traceroute6_basic(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)
    host1 = kwargs.get('host1', None)

    #Traceroute with IPv6-address from switch3 to host1
    LogOutput('info', "Test traceroute with IPv6-address \
from switch3 to host1")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute6 1010::1")
    retCode = devIntRetStruct.get('returnCode')

    assert retCode == 0, "Failed to traceroute with IPv6-address"
    " from switch3 to host1"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'traceroute to 1010::1' in retBuffer, "Traceroute with IPv6-address"
    " from switch3 to host1 failed"


def traceroute6_with_options(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)
    host1 = kwargs.get('host1', None)

     #Traceroute6 from switch3 to host1 with the maxttl parameter
    LogOutput('info', "Test traceroute6 from switch3 to host1"
              " with the maxttl parameter")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute6 1010::1"
                                             " maxttl 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6"
    " from switch3 to host1 with the maxttl parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'traceroute to 1010::1' in retBuffer, "Traceroute6"
    "from switch3 to host1 with the maxttl parameter failed"

    #Traceroute6 from switch3 to host1 with the dstport parameter
    LogOutput('info', "Test traceroute6 from switch3 to host1"
              " with the dstport parameter")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute6 1010::1"
                                             " dstport 334")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6"
    " from switch3 to host1 with the dstport parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'traceroute to 1010::1' in retBuffer, "Traceroute6"
    "from switch3 to host1 with the dstport parameter failed"

    #Traceroute6 from switch3 to host1 with the probes parameter
    LogOutput('info', "Test traceroute6 from switch3 to host1"
              " with the probes parameter")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute6 1010::1"
                                             " probes 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6"
    " from switch3 to host1 with the probes parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'traceroute to 1010::1' in retBuffer, "Traceroute6"
    "from switch3 to host1 with the probes parameter failed"

    #Traceroute6 from switch3 to host1 with the timeout parameter
    LogOutput('info', "Test traceroute6 from switch3 to host1"
              " with the timeout parameter")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute6 1010::1"
                                             " timeout 3")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6"
    " from switch3 to host1 with the timeout parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'traceroute to 1010::1' in retBuffer, "Traceroute6"
    "from switch3 to host1 with the timeout parameter failed"


def traceroute_failure_cases(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)
    host1 = kwargs.get('host1', None)

    #Traceroute network unreachable case
    LogOutput('info', "Test traceroute network unreachable case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute 10.11.1.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute with IPv4-address"

    retBuffer = devIntRetStruct.get('buffer')
    #LogOutput('info', retBuffer)
    assert 'Network is unreachable' in retBuffer, "Failure"
    " case test is unsuccessful"

    #Traceroute destination unreachable case
    LogOutput('info', "Test traceroute destination host unreachable case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute 10.0.40.5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute with IPv4-address"

    retBuffer = devIntRetStruct.get('buffer')
    #LogOutput('info', retBuffer)
    assert '!H' in retBuffer, "Failure"
    " case test is unsuccessful"

    #Traceroute unknown host
    LogOutput('info', "Test traceroute unknown host case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute \
asdfrgqweewwe")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute with hostname"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'traceroute: unknown host' in retBuffer, "Failure"
    " case test is unsuccessful"

    #Traceroute with maxttl is lesthan the number of hops case
    LogOutput('info', "Test traceroute with maxttl \
is lesthan the number of hops case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute 10.0.10.1 \
maxttl 1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute with maxttl"

    retBuffer = devIntRetStruct.get('buffer')
    #LogOutput('info', retBuffer)
    assert '2 10.0.10.1' not in retBuffer, "Failure"
    " case test is unsuccessful"

    #Traceroute with minttl and maxxttl are lesthan the number of hops case
    LogOutput('info', "Test traceroute with  minttl and maxttl \
is lesthan the number of hops case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute \
10.0.10.1 maxttl 1 minttl 1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute with  minttl and maxttl \
is lesthan the number of hops case"

    retBuffer = devIntRetStruct.get('buffer')
    #LogOutput('info', retBuffer)
    assert '1   10.0.40.2' in retBuffer, "Failure"
    " case test is unsuccessful"

    #Traceroute with the probes exceeds the maximum supported by the platform
    LogOutput('info', "Test traceroute with probes exceeds \
the maximum supported by the platform case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute \
10.0.10.1 probes 6")
    retCode = devIntRetStruct.get('returncode')
    assert retCode != 0, "Failure case test is unsuccessful"
    retBuffer = devIntRetStruct.get('buffer')
    assert 'Unknown command' in retBuffer, "Failure"
    " case test is unsuccessful"


def traceroute6_failure_cases(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)
    host1 = kwargs.get('host1', None)
    #Traceroute6 network unreachable case
    LogOutput('info', "Test traceroute6 network unreachable case")
    devIntRetStruct = switch2.DeviceInteract(command="traceroute6 1050::4")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute with IPv6-address"

    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    assert 'Network is unreachable' in retBuffer, "Failure"
    " case test is unsuccessful"

    #Traceroute6 destination unreachable case( this case is not working
    #correctly : recheck)
    LogOutput('info', "Test traceroute6 destination host unreachable case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute6 2030::4")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute with IPv6-address"

    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    assert '!H' in retBuffer, "Failure"
    " case test is unsuccessful"

    #Traceroute6 unknown host
    LogOutput('info', "Test traceroute6 unknown host case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute6 \
asdfrgqweewwe")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 hostname"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'traceroute: unknown host' in retBuffer, "Failure"
    " case test is unsuccessful"

    #Traceroute6 with maxttl is lesthan the number of hops case
    LogOutput('info', "Test traceroute6 with maxttl \
is lesthan the number of hops case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute6 \
1010::1 maxttl 1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to traceroute6 with maxttl"

    retBuffer = devIntRetStruct.get('buffer')
    #LogOutput('info', retBuffer)
    assert '2 1010::1' not in retBuffer, "Failure"
    " case test is unsuccessful"

    #Traceroute6 with probes exceeds the maximum supported by the platform
    LogOutput('info', "Test traceroute6 with probes exceeds \
the maximum supported by the platform case")
    devIntRetStruct = switch3.DeviceInteract(command="traceroute6 \
1010::1 probes 6")
    retCode = devIntRetStruct.get('returnCode')
    retBuffer = devIntRetStruct.get('buffer')
    assert 'Unknown command' in retBuffer, "Failure"
    " case test is unsuccessful"


def exit_vtysh_shell(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    retStruct = switch1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    retStruct = switch2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    retStruct = switch3.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"


class Test_traceroute:

    def setup_class(cls):
        # Test objaect will parse command line and formulate the env
        Test_traceroute.testObj = testEnviron(topoDict=topoDict,
                                              defSwitchContext="vtyShell")
        # Get traceroute topology object
        Test_traceroute.tracerouteTopoObj = Test_traceroute.testObj.topoObjGet()

    def teardown_class(cls):

        Test_traceroute.tracerouteTopoObj.terminate_nodes()

    def test_traceroute_full(self):

        # Get Device objects
        dut01Obj = self.tracerouteTopoObj.deviceObjGet(device="dut01")
        dut02Obj = self.tracerouteTopoObj.deviceObjGet(device="dut02")
        dut03Obj = self.tracerouteTopoObj.deviceObjGet(device="dut03")
        wrkston01Obj = self.tracerouteTopoObj.deviceObjGet(device="wrkston01")
        configure(switch1=dut01Obj, switch2=dut02Obj,
                  switch3=dut03Obj, host1=wrkston01Obj)

        LogOutput('info', "### Basic traceroute tests ###")
        traceroute_basic(switch1=dut01Obj, switch2=dut02Obj,
                         switch3=dut03Obj, host1=wrkston01Obj)

        LogOutput('info', "\n### Traceroute with options tests ###")
        traceroute_with_options(switch1=dut01Obj, switch2=dut02Obj,
                                switch3=dut03Obj, host1=wrkston01Obj)

        traceroute6_basic(switch1=dut01Obj, switch2=dut02Obj,
                          switch3=dut03Obj, host1=wrkston01Obj)

        LogOutput('info', "\n### Traceroute6 test with options ###")
        traceroute6_with_options(switch1=dut01Obj, switch2=dut02Obj,
                                 switch3=dut03Obj, host1=wrkston01Obj)

        LogOutput('info', "\n### Traceroute failure test cases ###")
        traceroute_failure_cases(switch1=dut01Obj, switch2=dut02Obj,
                                 switch3=dut03Obj, host1=wrkston01Obj)

        LogOutput('info', "\n### Traceroute6 failure test cases ###")
        traceroute6_failure_cases(switch1=dut01Obj, switch2=dut02Obj,
                                  switch3=dut03Obj, host1=wrkston01Obj)

        LogOutput('info', "\n### Basic traceroute6 tests ###")

        exit_vtysh_shell(switch1=dut01Obj, switch2=dut02Obj, switch3=dut03Obj)
