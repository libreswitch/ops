#!/usr/bin/python

# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
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
import re
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

#
# The purpose of this test is to test
# functionality of DHCP-Relay

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02 dut03",
            "topoDevices": "dut01 dut02 dut03 wrkston01",
            "topoLinks": "lnk01:wrkston01:dut01,lnk02:dut01:dut02,\
                          lnk03:dut01:dut03",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            wrkston01:system-category:workstation"}


def configure(**kwargs):
    host1 = kwargs.get('host1', None)
    relay = kwargs.get('switch1', None)
    server1 = kwargs.get('switch2', None)
    server2 = kwargs.get('switch3', None)

    #Host1 configuration
    LogOutput('info', "Configuring host1 with IPv4 address")
    retStruct = host1.NetworkConfig(ipAddr="20.0.0.1",
                                    netMask="255.0.0.0",
                                    broadcast="20.255.255.255",
                                    interface=host1.linkPortMapping['lnk01'],
                                    config=True)
    if retStruct.returnCode() != 0:
        assert "Failed to configure IPv4 address on Host1"

    #Enabling interface 1 on dhcp relay
    LogOutput('info', "Enabling interface 1 on dhcp relay")
    retStruct = InterfaceEnable(deviceObj=relay, enable=True,
                                interface=relay.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on dhcp relay"

    #Entering interface for link 1 dhcp relay, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 1 dhcp relay")
    retStruct = InterfaceIpConfig(deviceObj=relay,
                                  interface=relay.linkPortMapping['lnk01'],
                                  addr="20.0.0.2", mask=8, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Enabling interface 2 on dhcp relay
    LogOutput('info', "Enabling interface 2 on dhcp relay")
    retStruct = InterfaceEnable(deviceObj=relay, enable=True,
                                interface=relay.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 2 on dhcp relay"

    #Entering interface for link 2 dhcp relay, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 dhcp relay")
    retStruct = InterfaceIpConfig(deviceObj=relay,
                                  interface=relay.linkPortMapping['lnk02'],
                                  addr="10.0.10.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Enabling interface 3 on dhcp relay
    LogOutput('info', "Enabling interface 3 on dhcp relay")
    retStruct = InterfaceEnable(deviceObj=relay, enable=True,
                                interface=relay.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 3 on dhcp relay"

    #Entering interface for link 3 dhcp relay, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 3 dhcp relay")
    retStruct = InterfaceIpConfig(deviceObj=relay,
                                  interface=relay.linkPortMapping['lnk03'],
                                  addr="9.0.0.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Enabling interface 1 on server 1
    LogOutput('info', "Enabling interface 1 on server 1")
    retStruct = InterfaceEnable(deviceObj=server1, enable=True,
                                interface=server1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on server 1"

    #Entering interface for link 2 server 1, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 2 server 1")
    retStruct = InterfaceIpConfig(deviceObj=server1,
                                  interface=server1.linkPortMapping['lnk02'],
                                  addr="10.0.10.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Enabling interface 1 on server 2
    LogOutput('info', "Enabling interface 1 on server 2")
    retStruct = InterfaceEnable(deviceObj=server2, enable=True,
                                interface=server2.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on server 2"

    #Entering interface for link 3 server 2, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link 3 server 2")
    retStruct = InterfaceIpConfig(deviceObj=server2,
                                  interface=server2.linkPortMapping['lnk03'],
                                  addr="9.0.0.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    #Configuring static routes on server 1 and server 2
    LogOutput('info', "Configuring static IPv4 route on server 1 to host1")
    retStruct = IpRouteConfig(deviceObj=server1, route="20.0.0.0", mask=8,
                              nexthop="10.0.10.1", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on server1 to host1"

    LogOutput('info', "Configuring static IPv4 route on server 2 to host1")
    retStruct = IpRouteConfig(deviceObj=server2, route="20.0.0.0", mask=8,
                              nexthop="9.0.0.1", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on server2 to host1"

    LogOutput('info', "Configuring static IPv4 route on host1 to server 1")
    retStruct = host1.IPRoutesConfig(config=True,
                                     destNetwork="10.0.10.0",
                                     netMask=24, gateway="20.0.0.2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on host1 to server 1"

    LogOutput('info', "Configuring static IPv4 route on host1 to server 2")
    retStruct = host1.IPRoutesConfig(config=True,
                                     destNetwork="9.0.0.0",
                                     netMask=24, gateway="20.0.0.2")
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route on host1 to server 2"

    cmdOut = host1.cmd("netstat -rn")
    LogOutput('info', "IPv4 Route table for workstation 1:\n" + str(cmdOut))

    #Entering vtysh dhcp relay
    retStruct = relay.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "configure helper address on dhcp relay")
    devIntRetStruct = relay.DeviceInteract(command="conf t")
    devIntRetStruct = relay.DeviceInteract(command="int 1")
    devIntRetStruct = relay.DeviceInteract(command="ip helper-address"
                                           " 10.0.10.2")
    devIntRetStruct = relay.DeviceInteract(command="ip helper-address 9.0.0.2")
    devIntRetStruct = relay.DeviceInteract(command="exit")

    # Assigning secondary ipv4 address
    devIntRetStruct = relay.DeviceInteract(command="int 2")
    devIntRetStruct = relay.DeviceInteract(command="ip address "
                                           "200.0.0.1/24 secondary")
    devIntRetStruct = relay.DeviceInteract(command="exit")
    devIntRetStruct = relay.DeviceInteract(command="exit")

    #Entering vtysh server 1
    retStruct = server1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    #Entering vtysh server 2
    retStruct = server2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    LogOutput('info', "sh run on relay")
    devIntRetStruct = relay.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)

    LogOutput('info', "sh run on server 1")
    devIntRetStruct = server1.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)

    LogOutput('info', "sh run on server 2")
    devIntRetStruct = server2.DeviceInteract(command="sh run")
    retBuffer = devIntRetStruct.get('buffer')
    LogOutput('info', retBuffer)

    # Check connectivity between client and server 1
    LogOutput('info', "Ping from client to server 1")
    retStruct = host1.Ping(ipAddr="10.0.10.2", packetCount=2)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "Ping from client to server 1 failed")
    else:
        LogOutput('info', "Ping from client to server 1 passed")

    # Check connectivity between client and server 2
    LogOutput('info', "Ping from client to server 2")
    retStruct = host1.Ping(ipAddr="9.0.0.2", packetCount=2)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "Ping from client to server 2 failed")
    else:
        LogOutput('info', "Ping from client to server 2 passed")

    LogOutput('info', "Ping from server 1 to client")
    devIntRetStruct = server1.DeviceInteract(command="ping 20.0.0.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from server to client"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping"
    " from server to client failed"

    LogOutput('info', "Ping from server 1 to client passed")

    LogOutput('info', "Ping from server 2 to client")
    devIntRetStruct = server2.DeviceInteract(command="ping 20.0.0.1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to ping IPv4-address"
    " from server to client"

    retBuffer = devIntRetStruct.get('buffer')
    assert '0% packet loss' in retBuffer, "Ping"
    " from server to client failed"

    LogOutput('info', "Ping from server 2 to client passed")

    #Exit vtysh prompt
    retStruct = relay.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    retStruct = server1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    retStruct = server2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"


def configure_server1(server1):

    LogOutput('info', "Configure DHCP server1")

    #Entering vtysh server1
    retStruct = server1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    devIntRetStruct = server1.DeviceInteract(command="conf t")
    devIntRetStruct = server1.DeviceInteract(command="dhcp-server")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enable dhcp-server"

    cmd = "range pool1 start-ip-address 20.0.0.100 end-ip-address 20.0.0.200 \
          netmask 255.0.0.0 broadcast 20.255.255.255 lease-duration 5"
    devIntRetStruct = server1.DeviceInteract(command=cmd)
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to configure ip pool1"

    cmd = "range pool2 start-ip-address 1.0.0.100 end-ip-address 1.0.0.200 \
          netmask 255.0.0.0 broadcast 1.255.255.255 lease-duration 5"
    devIntRetStruct = server1.DeviceInteract(command=cmd)
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to configure ip pool2"

    devIntRetStruct = server1.DeviceInteract(command="exit")
    devIntRetStruct = server1.DeviceInteract(command="exit")

    #Exit vtysh server1
    retStruct = server1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    return True


def configure_server2(server2):

    LogOutput('info', "Configure DHCP server2")

    #Entering vtysh server2
    retStruct = server2.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    devIntRetStruct = server2.DeviceInteract(command="conf t")
    devIntRetStruct = server2.DeviceInteract(command="dhcp-server")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enable dhcp-server"

    cmd = "range pool2 start-ip-address 20.0.0.1 end-ip-address 20.0.0.99 \
          netmask 255.0.0.0 broadcast 20.255.255.255 lease-duration 10"
    devIntRetStruct = server2.DeviceInteract(command=cmd)
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to configure ip pool2"

    devIntRetStruct = server2.DeviceInteract(command="exit")
    devIntRetStruct = server2.DeviceInteract(command="exit")

    #Exit vtysh server2
    retStruct = server2.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    return True


def getIpAddress(dump):

    ifconfigHost1Ipv4Addr = ''
    ifconfigIpv4AddrIdx = 1
    ifconfigIpv4AddrLineNum = 2

    lines = dump.split('\n')
    #extract IPv4 address
    count = 0
    for line in lines:
        if count == ifconfigIpv4AddrLineNum:
            outStr = line.split()
            ifconfigHost1Ipv4AddrTemp1 = outStr[ifconfigIpv4AddrIdx]
            ifconfigHost1Ipv4AddrTemp2 = \
                ifconfigHost1Ipv4AddrTemp1.split(':')
            ifconfigHost1Ipv4Addr = ifconfigHost1Ipv4AddrTemp2[1]
        count = count + 1

    return ifconfigHost1Ipv4Addr


def basic_dhcp_relay(**kwargs):

    host1 = kwargs.get('host1', None)
    server1 = kwargs.get('switch2', None)

    if configure_server1(server1) is False:
        return False

    LogOutput('info', "Configure DHCP client on host1")
    host1.cmd("ip addr del 20.0.0.1/8 dev wrkston01-eth0")
    cmdout = host1.cmd("mv /sbin/dhclient /usr/sbin/dhclient")
    cmdout = host1.cmd("dhclient wrkston01-eth0")

    #parse ifconfig output
    dump = host1.cmd("ifconfig wrkston01-eth0")

    ifconfigHost1Ipv4Addr = getIpAddress(dump)
    if not getIpAddress(dump):
        return False

    return True


def bootp_gateway_configuration(**kwargs):

    host1 = kwargs.get('host1', None)
    relay = kwargs.get('switch1', None)
    server1 = kwargs.get('switch2', None)

    #Entering vtysh relay
    retStruct = relay.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    devIntRetStruct = relay.DeviceInteract(command="conf t")
    devIntRetStruct = relay.DeviceInteract(command="int 1")
    devIntRetStruct = relay.DeviceInteract(command="ip address "
                                           "1.0.0.1/8 secondary")
    devIntRetStruct = relay.DeviceInteract(command="ip bootp-gateway 1.0.0.1")
    devIntRetStruct = relay.DeviceInteract(command="exit")
    devIntRetStruct = relay.DeviceInteract(command="exit")

    retStruct = relay.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # Add static route to connect to relay
    retStruct = IpRouteConfig(deviceObj=server1, route="1.0.0.0", mask=8,
                              nexthop="10.0.10.1", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure static IPv4 route to server1"

    cmdout = host1.cmd("dhclient -r wrkston01-eth0")
    cmdout = host1.cmd("dhclient wrkston01-eth0")

    #parse ifconfig output
    dump = host1.cmd("ifconfig wrkston01-eth0")

    ifconfigHost1Ipv4Addr = getIpAddress(dump)
    if not getIpAddress(dump):
        return False

    return True


def change_config(relay):

    #Entering vtysh relay
    retStruct = relay.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    # delete all ipv4 address
    devIntRetStruct = relay.DeviceInteract(command="conf t")
    devIntRetStruct = relay.DeviceInteract(command="int 2")
    devIntRetStruct = relay.DeviceInteract(command="no ip address"
                                           " 200.0.0.1/24 secondary")
    devIntRetStruct = relay.DeviceInteract(command="no ip address"
                                           " 10.0.10.1/24")

    # Assigning primary and secondary ipv4 address
    devIntRetStruct = relay.DeviceInteract(command="ip address 200.0.0.1/24")
    devIntRetStruct = relay.DeviceInteract(command="ip address "
                                           "10.0.10.1/24 secondary")
    devIntRetStruct = relay.DeviceInteract(command="exit")
    devIntRetStruct = relay.DeviceInteract(command="exit")

    retStruct = relay.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    return True


def relay_with_two_servers(**kwargs):

    host1 = kwargs.get('host1', None)
    relay = kwargs.get('switch1', None)
    server2 = kwargs.get('switch3', None)

    if configure_server2(server2) is False:
        return False

    if change_config(relay) is False:
        return False

    cmdout = host1.cmd("dhclient -r wrkston01-eth0")
    cmdout = host1.cmd("dhclient wrkston01-eth0")

    #parse ifconfig output
    dump = host1.cmd("ifconfig wrkston01-eth0")

    ifconfigHost1Ipv4Addr = getIpAddress(dump)
    if not getIpAddress(dump):
        return False

    return True


def relay_option82_enable_with_replace_policy_mac(**kwargs):

    host1 = kwargs.get('host1', None)
    relay = kwargs.get('switch1', None)

    #option 82 configuration on relay
    #Entering vtysh relay
    retStruct = relay.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    devIntRetStruct = relay.DeviceInteract(command="conf t")
    devIntRetStruct = relay.DeviceInteract(command="dhcp-relay option 82"
                                           " replace mac")
    devIntRetStruct = relay.DeviceInteract(command="dhcp-relay option 82"
                                           " validate")

    devIntRetStruct = relay.DeviceInteract(command="exit")

    retStruct = relay.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    cmdout = host1.cmd("dhclient -r wrkston01-eth0")
    cmdout = host1.cmd("dhclient wrkston01-eth0")

    #parse ifconfig output
    dump = host1.cmd("ifconfig wrkston01-eth0")

    ifconfigHost1Ipv4Addr = getIpAddress(dump)
    if not getIpAddress(dump):
        return False

    return True


def relay_option82_enable_with_replace_policy_ip(**kwargs):

    host1 = kwargs.get('host1', None)
    relay = kwargs.get('switch1', None)

    #option 82 configuration on relay
    #Entering vtysh relay
    retStruct = relay.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    devIntRetStruct = relay.DeviceInteract(command="conf t")
    devIntRetStruct = relay.DeviceInteract(command="dhcp-relay option 82"
                                           " replace ip")
    devIntRetStruct = relay.DeviceInteract(command="dhcp-relay option 82"
                                           " validate")

    devIntRetStruct = relay.DeviceInteract(command="exit")

    retStruct = relay.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    cmdout = host1.cmd("dhclient -r wrkston01-eth0")
    cmdout = host1.cmd("dhclient wrkston01-eth0")

    #parse ifconfig output
    dump = host1.cmd("ifconfig wrkston01-eth0")

    ifconfigHost1Ipv4Addr = getIpAddress(dump)
    if not getIpAddress(dump):
        return False

    return True


def relay_option82_enable_with_keep_policy_mac(**kwargs):

    host1 = kwargs.get('host1', None)
    relay = kwargs.get('switch1', None)

    #option 82 configuration on relay
    #Entering vtysh relay
    retStruct = relay.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    devIntRetStruct = relay.DeviceInteract(command="conf t")
    devIntRetStruct = relay.DeviceInteract(command="dhcp-relay option 82"
                                           " keep mac")
    devIntRetStruct = relay.DeviceInteract(command="dhcp-relay option 82"
                                           " validate")

    devIntRetStruct = relay.DeviceInteract(command="exit")

    retStruct = relay.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    cmdout = host1.cmd("dhclient -r wrkston01-eth0")
    cmdout = host1.cmd("dhclient wrkston01-eth0")

    #parse ifconfig output
    dump = host1.cmd("ifconfig wrkston01-eth0")

    ifconfigHost1Ipv4Addr = getIpAddress(dump)
    if not getIpAddress(dump):
        return False

    return True


def relay_option82_enable_with_keep_policy_ip(**kwargs):

    host1 = kwargs.get('host1', None)
    relay = kwargs.get('switch1', None)

    #option 82 configuration on relay
    #Entering vtysh relay
    retStruct = relay.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    devIntRetStruct = relay.DeviceInteract(command="conf t")
    devIntRetStruct = relay.DeviceInteract(command="dhcp-relay option 82"
                                           " keep ip")
    devIntRetStruct = relay.DeviceInteract(command="dhcp-relay option 82"
                                           " validate")

    devIntRetStruct = relay.DeviceInteract(command="exit")

    retStruct = relay.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    cmdout = host1.cmd("dhclient -r wrkston01-eth0")
    cmdout = host1.cmd("dhclient wrkston01-eth0")

    #parse ifconfig output
    dump = host1.cmd("ifconfig wrkston01-eth0")

    ifconfigHost1Ipv4Addr = getIpAddress(dump)
    if not getIpAddress(dump):
        return False

    return True


def relay_with_server_unreachable(**kwargs):

    host1 = kwargs.get('host1', None)
    server1 = kwargs.get('switch2', None)

    #delete static route from server1 to host1
    LogOutput('info', "unconfiguring static IPv4 route on server 1 to host1")
    retStruct = IpRouteConfig(deviceObj=server1, route="20.0.0.0", mask=8,
                              nexthop="10.0.10.1", config=False)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to unconfigure static IPv4 route on server1 to host1"

    cmdout = host1.cmd("dhclient -r wrkston01-eth0")
    cmdout = host1.cmd("dhclient wrkston01-eth0")

    #parse ifconfig output
    dump = host1.cmd("ifconfig wrkston01-eth0")

    ifconfigHost1Ipv4Addr = getIpAddress(dump)
    if not getIpAddress(dump):
        return False

    return True


class Test_dhcp_relay_configuration:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_dhcp_relay_configuration.testObj = testEnviron(topoDict=topoDict)
        #Get topology object
        Test_dhcp_relay_configuration.topoObj = \
            Test_dhcp_relay_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_dhcp_relay_configuration.topoObj.terminate_nodes()

    def test_configure(self):
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        configure(host1=wrkston01Obj, switch1=dut01Obj,
                  switch2=dut02Obj, switch3=dut03Obj)

    def test_basic_dhcp_relay(self):
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        if basic_dhcp_relay(host1=wrkston01Obj, switch2=dut02Obj) is True:
            LogOutput('info', "dhcp relay basic test passed")
        else:
            LogOutput('error', "dhcp relay basic test failed")

    def test_bootp_gateway_configuration(self):
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        if bootp_gateway_configuration(host1=wrkston01Obj,
                        switch1=dut01Obj, switch2=dut02Obj) is True:
            LogOutput('info', "bootp configuration test passed")
        else:
            LogOutput('error', "bootp configuration test failed")

    def test_relay_with_two_servers(self):
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        if relay_with_two_servers(host1=wrkston01Obj, switch1=dut01Obj,
                                  switch3=dut03Obj) is True:
            LogOutput('info', "dhcp relay basic test with two servers passed")
        else:
            LogOutput('error', "dhcp relay basic test with two servers failed")

    def test_relay_option82_enable_with_replace_policy_mac(self):
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        if relay_option82_enable_with_replace_policy_mac(host1=wrkston01Obj,
                                  switch1=dut01Obj) is True:
            LogOutput('info', "dhcp relay with option 82 "
                      "and replace policy with mac test passed")
        else:
            LogOutput('error', "dhcp relay with option 82"
                      "and replace policy with mac test failed")

    def test_relay_option82_enable_with_replace_policy_ip(self):
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        if relay_option82_enable_with_replace_policy_ip(host1=wrkston01Obj,
                                  switch1=dut01Obj) is True:
            LogOutput('info', "dhcp relay with option 82 "
                      "and replace policy with ip test passed")
        else:
            LogOutput('error', "dhcp relay with option 82"
                      "and replace policy with ip test failed")

    def test_relay_option82_enable_with_keep_policy_mac(self):
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        if relay_option82_enable_with_keep_policy_mac(host1=wrkston01Obj,
                                  switch1=dut01Obj) is True:
            LogOutput('info', "dhcp relay with option 82 "
                      "and keep policy with mac test passed")
        else:
            LogOutput('error', "dhcp relay with option 82"
                      "and replace policy with mac test failed")

    def test_relay_option82_enable_with_keep_policy_ip(self):
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        if relay_option82_enable_with_keep_policy_ip(host1=wrkston01Obj,
                                                     switch1=dut01Obj) is True:
            LogOutput('info', "dhcp relay with option 82 "
                      "and keep policy with ip test passed")
        else:
            LogOutput('error', "dhcp relay with option 82"
                      "and replace policy with ip test failed")

    def test_relay_with_server_unreachable(self):
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        if relay_with_server_unreachable(host1=wrkston01Obj,
                                         switch2=dut02Obj) is True:
            LogOutput('info', "dhcp relay test with one server unreachable"
                      " test passed")
        else:
            LogOutput('error', "dhcp relay test with one server unreachable"
                       " test failed")
