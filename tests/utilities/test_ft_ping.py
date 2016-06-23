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
# functionality of ping Ip-App
#
# For this test, we need below topology
#
# +---------+            +----------+          +-----------+
# |         |            |          |          |           |
# |         |            |          |          |           |
# | Host1   +------------+ Switch1  +----------+ Switch2   |
# |         |            |          |          |           |
# |         |            |          |          |           |
# +---------+            +----------+          +-----------+
#


# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02 wrkston01",
            "topoLinks": "lnk01:wrkston01:dut01,lnk02:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation"}


def configure(**kwargs):
    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Host1 configuration
    LogOutput('info', "Configuring host1 with IPv4 address")
    retStruct = host1.NetworkConfig(ipAddr="10.0.30.1",
                                    netMask="255.255.255.0",
                                    broadcast="10.0.30.255",
                                    interface=host1.linkPortMapping['lnk01'],
                                    config=True)
    if retStruct.returnCode() != 0:
        assert "Failed to configure IPv4 address on Host1"

    LogOutput('info', "Configuring host1 with IPv6 address")
    retStruct = host1.Network6Config(ipAddr="1030::1",
                                     netMask=120,
                                     interface=host1.linkPortMapping['lnk01'],
                                     config=True)
    if retStruct.returnCode() != 0:
        assert "Failed to configure IPv6 address on Host1"

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
                                interface=switch1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface2 on SW1"

    #Entering interface for link 1 SW1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="10.0.30.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 1 SW1, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="1030::2", mask=120,
                                  ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    #Entering interface for link 2 SW1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk02'],
                                  addr="10.0.10.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    LogOutput('info', "Configuring IPv6 address on link 2 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk02'],
                                  addr="1010::2", mask=120,
                                  ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    #Enabling interface 2 SW2
    LogOutput('info', "Enabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface2 on SW2"

    #Entering interface for link 2 SW2, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="10.0.10.3", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Entering interface for link 2 SW2, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="1010::3", mask=120, ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    #Configuring static routes
    LogOutput('info', "Configuring static IPv4 route on host1")
    retStruct = host1.IPRoutesConfig(config=True,
                                     destNetwork="10.0.10.0",
                                     netMask=24, gateway="10.0.30.2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on host1"

    LogOutput('info', "Configuring static IPv4 route on switch2")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.30.0", mask=24,
                              nexthop="10.0.10.2", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on switch2"

    #Entering vtysh SW1
    retStruct = switch1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    #Entering vtysh SW2
    retStruct = switch2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "Configuring static IPv6 route on host1")
    retStruct = host1.IPRoutesConfig(config=True, destNetwork="1010::0",
                                     netMask=120, gateway="1030::2",
                                     ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure static IPv6 route on host1")

    LogOutput('info', "Configuring static IPv6 route on switch2")
    devIntRetStruct = switch2.DeviceInteract(command="conf t")
    devIntRetStruct = switch2.DeviceInteract(command="ipv6"
                                             " route 1030::/120 1010::2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv6 route on switch2"

    devIntRetStruct = switch2.DeviceInteract(command="exit")

    devIntRetStruct = switch1.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)
    devIntRetStruct = switch2.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)

    cmdOut = host1.cmd("netstat -rn")
    LogOutput('info', "IPv4 Route table for workstation 1:\n" + str(cmdOut))


def check_interface_status(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    iter = 0
    while iter != 2:
        retry = 0
        devIntRetStruct = switch2.DeviceInteract(command="start-shell")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter bash shell"

        devIntRetStruct = switch1.DeviceInteract(command="start-shell")
        retCode = devIntRetStruct.get('returnCode')
        assert retCode == 0, "Failed to enter bash shell"

        devIntRetStruct = switch1.DeviceInteract(command="ovs-vsctl get"
                                                " interface 1 admin_state")
        retBuffer = devIntRetStruct.get('buffer')
        if 'down' in retBuffer:
            retry = 1

        devIntRetStruct = switch1.DeviceInteract(command="ovs-vsctl get"
                                                " interface 2 admin_state")
        retBuffer = devIntRetStruct.get('buffer')
        if 'down' in retBuffer:
            retry = 1

        devIntRetStruct = switch2.DeviceInteract(command="ovs-vsctl get"
                                                " interface 1 admin_state")
        retBuffer = devIntRetStruct.get('buffer')
        if 'down' in retBuffer:
            retry = 1

        devIntRetStruct = switch2.DeviceInteract(command="exit")
        devIntRetStruct = switch1.DeviceInteract(command="exit")

        if (retry == 0):
            return True
        else:
            sleep(5)

        iter += 1

    if (retry != 0):
        return False

    return True


def ping_basic(**kwargs):

    host1 = kwargs.get('host1', None)
    switch2 = kwargs.get('switch2', None)

    #Ping IPv4-address from switch2 to host1
    LogOutput('info', "Test ping IPv4-address from switch2 to host1")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping"
    " from switch2 to host1 failed"


def ping_with_datafill_option(**kwargs):

    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Ping IPv4-address from switch2 to host1 with the data-fill parameter
    LogOutput('info', "Test ping IPv4-address from switch2 to host1"
              " with the data-fill parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1"
                                             " data-fill dee")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1 with the data-fill parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping"
    " IPv4-address from switch2 to host1 with the data-fill parameter failed"


def ping_with_datagram_size_option(**kwargs):

    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Ping IPv4-address from switch2 to host1 with the datagram-size parameter
    LogOutput('info', "Test ping IPv4-address from switch2 to host1"
              " with the datagram-size parameter ")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1"
                                             " datagram-size 200")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1 with the datagram-size parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 10.0.30.1 (10.0.30.1) 200(228) bytes of data' \
    and '0% packet loss' in retBuffer, "Ping"
    " IPv4-address from switch2 to host1"
    " with the datagram-size parameter failed"


def ping_with_interval_option(**kwargs):

    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Ping IPv4-address from switch2 to host1 with the interval parameter
    LogOutput('info', "Test ping IPv4-address from switch2 to host1"
              " with the interval parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1"
                                             " interval 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1 with the interval parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping"
    " IPv4-address from switch2 to host1 with the interval parameter failed"


def ping_with_repetition_option(**kwargs):

    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Ping IPv4-address with the repetition parameter from switch2 to host1
    LogOutput('info', "Test ping IPv4-address from switch2 to host1"
              " with the repetition parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1"
                                             " repetitions 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1 with the repetition parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '2 packets transmitted, 2 received, 0% packet loss,' \
    in retBuffer, "Ping"
    " IPv4-address from switch2 to host1"
    " with the repetition parameter failed"


def ping_with_timeout_option(**kwargs):

    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Ping IPv4-address with the timeout parameter from switch2 to host1
    LogOutput('info', "Test ping IPv4-address from switch2 to host1"
              " with the timeout parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1"
                                             " timeout 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1 with the timeout parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping"
    " IPv4-address from switch2 to host1 with the timeout parameter failed"


def ping_with_tos_option(**kwargs):

    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Ping IPv4-address with the TOS parameter from switch2 to host1
    LogOutput('info', "Test ping IPv4-address from switch2 to host1"
              " with the TOS parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1"
                                             " tos 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1 with the TOS parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping"
    " IPv4-address from switch2 to host1 with the TOS parameter failed"


def ping_with_recordroute_option(**kwargs):

    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Ping IPv4-address with the ip-option record-route
    LogOutput('info', "Test ping IPv4-address from switch2 to host1"
              " with the ip-option record-route")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1"
                                             " ip-option record-route")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1 with the ip-option record-route"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'RR:' and '0% packet loss' in retBuffer, "Ping from switch2"
    " to host1 with the ip-option record-route failed"


def ping_with_timestamp_option(**kwargs):

    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Ping IPv4-address with the ip-option include-timestamp
    LogOutput('info', "Test ping IPv4-address from switch2 to host1"
              " with the ip-option include-timestamp")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1"
                                             " ip-option include-timestamp")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1 with the ip-option include-timestamp"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'TS:' and '0% packet loss' in retBuffer, "Ping from switch2"
    " to host1 with the ip-option include-timestamp failed"


def ping_with_timestamp_and_address_option(**kwargs):

    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    #Ping IPv4-address with the ip-option include-timestamp-and-address
    LogOutput('info', "Test ping IPv4-address from switch2 to host1"
              " with the ip-option include-timestamp-and-address")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.30.1"
                                             " ip-option "
                                             "include-timestamp-and-address")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from switch2 to host1 with the ip-option include-timestamp-and-address"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'TS:' and '0% packet loss' in retBuffer, "Ping from"
    " switch2 to host1 with the ip-option"
    " include-timestamp-and-address failed"


def ping6_basic(**kwargs):

    host1 = kwargs.get('host1', None)
    switch2 = kwargs.get('switch2', None)

    #Ping6 from switch2 to host1
    LogOutput('info', "Test ping6 IPv6-address from switch2 to host1")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " from switch2 to host1"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping6"
    " from switch2 to host1 failed"


def ping6_with_datafill_option(**kwargs):

    host1 = kwargs.get('host1', None)
    switch2 = kwargs.get('switch2', None)

    #Ping6 from switch2 to host1 with the data-fill parameter
    LogOutput('info', "Test ping6 IPv6-address from switch2 to host1"
              " with the data-fill parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1"
                                             " data-fill dee")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " with the data-fill parameter from switch2 to host1"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping6"
    " from switch2 to host1 with the data-fill parameter failed"


def ping6_with_datagram_size_option(**kwargs):

    host1 = kwargs.get('host1', None)
    switch2 = kwargs.get('switch2', None)

    #Ping6 from switch2 to host1 with the datagram-size parameter
    LogOutput('info', "Test ping6 IPv6-address from switch2 to host1"
              " with the datagram-size parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1"
                                             " datagram-size 200")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " from switch2 to host1 with the datagram-size parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'PING 1030::1(1030::1) 200 data bytes' \
    and '0% packet loss' in retBuffer, "Ping6"
    " from switch2 to host1 with the datagram-size parameter failed"


def ping6_with_interval_option(**kwargs):

    host1 = kwargs.get('host1', None)
    switch2 = kwargs.get('switch2', None)

    #Ping6 from switch2 to host1 with the interval parameter
    LogOutput('info', "Test ping6 IPv6-address from switch2 to host1"
              " with the interval parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1"
                                             " interval 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " from switch2 to host1 with the interval parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping6"
    " from switch2 to host1 with the interval parameter failed"


def ping6_with_repetition_option(**kwargs):

    host1 = kwargs.get('host1', None)
    switch2 = kwargs.get('switch2', None)

    #Ping6 from switch2 to host1 with the repetition parameter
    LogOutput('info', "Test ping6 IPv6-address from switch1 to switch1"
              " with the repetitions parameter")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1030::1"
                                             " repetitions 2")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping6 IPv6-address"
    " from switch2 to host1 with the repetition parameter"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping6"
    " from switch2 to host1 with the repetition parameter failed"


def ping_network_unreachable(**kwargs):

    switch2 = kwargs.get('switch2', None)

    #Ping network unreachable case
    LogOutput('info', "Test ping network unreachable case")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.11.1.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'Network is unreachable' in retBuffer, "Failure"
    " case test is unsuccessful"


def ping_destination_unreachable(**kwargs):

    switch2 = kwargs.get('switch2', None)

    #Ping destination unreachable case
    LogOutput('info', "Test ping destination host unreachable case")
    devIntRetStruct = switch2.DeviceInteract(command="ping 10.0.10.5")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'Destination Host Unreachable' in retBuffer, "Failure"
    " case test is unsuccessful"


def ping_unknown_host(**kwargs):

    switch2 = kwargs.get('switch2', None)

    #Ping unknown host
    LogOutput('info', "Test ping unknown host case")
    devIntRetStruct = switch2.DeviceInteract(command="ping asdfrgqweewwe")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping hostname"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'unknown host' in retBuffer, "Failure"
    " case test is unsuccessful"


def ping6_network_unreachable(**kwargs):

    switch2 = kwargs.get('switch2', None)

    #Ping6 network unreachable case
    LogOutput('info', "Test ping6 network unreachable case")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 1050::1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv6-address"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'Network is unreachable' in retBuffer, "Failure"
    " case test is unsuccessful"


def ping6_unknown_host(**kwargs):

    switch2 = kwargs.get('switch2', None)

    #Ping6 unknown host
    LogOutput('info', "Test ping unknown host case")
    devIntRetStruct = switch2.DeviceInteract(command="ping6 asdfrgqweewwe")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping hostname"

    retBuffer = devIntRetStruct.get('buffer')
    assert 'unknown host' in retBuffer, "Failure"
    " case test is unsuccessful"


def cleanup(**kwargs):

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    host1 = kwargs.get('host1', None)

    retStruct = switch1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    LogOutput('info', "\nPerforming cleanup")
    LogOutput('info', "unconfiguring static ipv4 route on host1")
    retStruct = host1.IPRoutesConfig(config=False,
                                     destNetwork="10.0.10.0",
                                     netMask=24, gateway="10.0.30.2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure static ipv4 route on host1"

    LogOutput('info', "unconfiguring static ipv6 route on host1")
    retStruct = host1.IPRoutesConfig(config=False, destNetwork="1010::0",
                                     netMask=120, gateway="1030::2",
                                     ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure static ipv6 route on host1")

    LogOutput('info', "Unconfiguring host1 with IPv4 address")
    retStruct = host1.NetworkConfig(ipAddr="10.0.30.1",
                                    netMask="255.255.255.0",
                                    broadcast="10.0.30.255",
                                    interface=host1.linkPortMapping['lnk01'],
                                    config=False)
    if retStruct.returnCode() != 0:
        assert "Failed to unconfigure IPv4 address on Host1"

    LogOutput('info', "unConfiguring host1 with IPv6 address")
    retStruct = host1.Network6Config(ipAddr="1030::1",
                                     netMask=120,
                                     interface=host1.linkPortMapping['lnk01'],
                                     config=False)
    if retStruct.returnCode() != 0:
        assert "Failed to unconfigure IPv6 address on Host1"

    #SW1
    LogOutput('info', "Unconfiguring IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="10.0.30.2", mask=24, config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure an IPv4 address"

    LogOutput('info', "Unconfiguring IPv6 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr="1030::2", mask=120,
                                  ipv6flag=True, config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure an IPv6 address"

    LogOutput('info', "Unconfiguring IPv4 address on link 2 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk02'],
                                  addr="10.0.10.2", mask=24, config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure an ipv4 address"

    LogOutput('info', "unConfiguring IPv6 address on link 2 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk02'],
                                  addr="1010::2", mask=120,
                                  ipv6flag=True, config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure an ipv6 address"

    LogOutput('info', "Disabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=False,
                                interface=switch1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to disable interface1 on SW1"

    LogOutput('info', "Disabling interface2 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=False,
                                interface=switch1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to disable interface2 on SW1"

    #SW2
    LogOutput('info', "Unconfiguring IPv4 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="10.0.10.3", mask=24, config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure an IPv4 address"

    LogOutput('info', "Unconfiguring IPv6 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr="1010::3", mask=120, ipv6flag=True,
                                  config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure an IPv6 address"

    #unconfiguring static routes
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.30.0", mask=24,
                              nexthop="10.0.10.2", config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure static ipv4 route on switch2"

    devIntRetStruct = switch2.DeviceInteract(command="conf t")
    devIntRetStruct = switch2.DeviceInteract(command="no ipv6"
                                             " route 1030::/120 1010::2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static ipv6 route on switch2"

    devIntRetStruct = switch2.DeviceInteract(command="exit")

    LogOutput('info', "Disabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=False,
                                interface=switch2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to disable interface2 on SW2"

    retStruct = switch2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"


class Test_ping:

    def setup_class(cls):
        # Test objaect will parse command line and formulate the env
        Test_ping.testObj = testEnviron(topoDict=topoDict,
                                        defSwitchContext="vtyShell")
        # Get ping topology object
        Test_ping.pingTopoObj = Test_ping.testObj.topoObjGet()

    def teardown_class(cls):

        Test_ping.pingTopoObj.terminate_nodes()

    def test_ping_full(self):

        # Get Device objects
        dut01Obj = self.pingTopoObj.deviceObjGet(device="dut01")
        dut02Obj = self.pingTopoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.pingTopoObj.deviceObjGet(device="wrkston01")
        configure(switch1=dut01Obj, switch2=dut02Obj, host1=wrkston01Obj)

        if (check_interface_status(switch1=dut01Obj,
                    switch2=dut02Obj) is False):

            LogOutput('info', "\n Since Interface state is down ping test"
            " cases are not executed")

            cleanup(switch1=dut01Obj, switch2=dut02Obj, host1=wrkston01Obj)
            return True

        LogOutput('info', "### Basic ping tests ###")
        ping_basic(host1=wrkston01Obj, switch1=dut01Obj, switch2=dut02Obj)
        LogOutput('info', "\n### Ping with options tests ###")
        ping_with_datafill_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping_with_datagram_size_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping_with_interval_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping_with_timeout_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping_with_repetition_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping_with_tos_option(host1=wrkston01Obj, switch2=dut02Obj)

        LogOutput('info', "\n### Ping with extended options tests ###")
        ping_with_recordroute_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping_with_timestamp_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping_with_timestamp_and_address_option(host1=wrkston01Obj,
                                                switch2=dut02Obj)

        LogOutput('info', "\n### Basic ping6 tests ###")
        ping6_basic(host1=wrkston01Obj, switch1=dut01Obj, switch2=dut02Obj)

        LogOutput('info', "\n### Ping6 test with options ###")
        ping6_with_datafill_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping6_with_datagram_size_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping6_with_interval_option(host1=wrkston01Obj, switch2=dut02Obj)
        ping6_with_repetition_option(host1=wrkston01Obj, switch2=dut02Obj)

        LogOutput('info', "\n### Ping failure test cases ###")
        ping_network_unreachable(switch2=dut02Obj)
        ping_destination_unreachable(switch2=dut02Obj)
        ping_unknown_host(switch2=dut02Obj)

        LogOutput('info', "\n### Ping6 failure test cases ###")
        ping6_network_unreachable(switch2=dut02Obj)
        ping6_unknown_host(switch2=dut02Obj)

        cleanup(switch1=dut01Obj, switch2=dut02Obj, host1=wrkston01Obj)
