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
from opstestfw.switch.CLI.InterfaceIpConfig import InterfaceIpConfig
from opsvsiutils.vtyshutils import *

'''
TOPOLOGY
+---------------+             +---------------+             +---------------+
|               |             |               |             |               |
| Switch 1     1+-------------+1  Switch 2   2+-------------+1   Switch 3   +
|               |             |               |             |               |
|               |             |               |             |               |
+---------------+             +---------------+             +---------------+

switch 1 configuration
----------------------
vlan 1
    no shutdown
interface 1
    no shutdown
    ip address 7.0.0.1/8

switch 2 configuration
----------------------
vlan 1
    no shutdown
interface 1
    no shutdown
    ip address 7.0.0.2/8
interface 2
    no shutdown
    ip address 8.0.0.2/8

switch 3 configuration
----------------------
vlan 1
    no shutdown
interface 1
    no shutdown
    ip address 8.0.0.3/8
'''

IP_ADDR1 = "7.0.0.1"
IP_ADDR2 = "7.0.0.2"
IP_ADDR3 = "8.0.0.2"
IP_ADDR4 = "8.0.0.3"

DEFAULT_PL = "8"

SW2_ROUTER_ID = "8.0.0.2"
SW3_ROUTER_ID = "8.0.0.3"

AS_NUM1 = "1"
AS_NUM2 = "2"

VTYSH_CR = '\r\n'
MAX_WAIT_TIME = 100
# Topology definition
topoDict = {"topoExecution": 5000,
            "topoTarget": "dut01 dut02 dut03",
            "topoDevices": "dut01 dut02 dut03",
            "topoLinks": "lnk01:dut01:dut02,lnk02:dut02:dut03",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch"}


def enterConfigShell(dut):
    retStruct = dut.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    retStruct = dut.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"
    return True

# If the context is not present already then it will be created
def enterRouterContext(dut,as_num):
    if (enterConfigShell(dut) is False):
        return False

    devIntReturn = dut.DeviceInteract(command="router bgp "+ as_num)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter BGP context"
    return True

def exitContext(dut):
    devIntReturn = dut.DeviceInteract(command="exit")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to exit current context"

    retStruct = dut.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit config terminal"

    retStruct = dut.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"
    return True

def configure_static_route(dut, network, nexthop):
    if (enterConfigShell(dut) is False):
        return False
    cmd = "ip route "+network+" "+nexthop
    devIntReturn = dut.DeviceInteract(command=cmd)
    return True

def configure_route_map(dut, routemap):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "ip prefix-list BGP_PList seq 10 permit any"
    devIntReturn = dut.DeviceInteract(command=cmd)
    cmd = "route-map "+routemap+" permit 20"
    devIntReturn = dut.DeviceInteract(command=cmd)
    devIntReturn = dut.DeviceInteract(command="match"\
                                      " ip address prefix-list BGP_PList")
    devIntReturn = dut.DeviceInteract(command="exit")
    return True

def configure_router_id(dut, as_num, router_id):
    if (enterRouterContext(dut, as_num) is False):
        return False

    LogOutput('info', "Configuring BGP router ID " + router_id)
    devIntReturn = dut.DeviceInteract(command="bgp router-id " + router_id)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set router-id failed"
    return True

def configure_network(dut, as_num, network):
    if (enterRouterContext(dut, as_num) is False):
        return False

    cmd = "network " + network
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set network failed"
    return True

def configure_redistribute(dut, as_num, route_type):
    if (enterRouterContext(dut, as_num) is False):
        return False

    devIntReturn = dut.DeviceInteract(command="redistribute "+route_type)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set redistribute configuration failed"
    return True

def configure_redistribute_rmap(dut, as_num, route_type, routemap):
    if (enterRouterContext(dut, as_num) is False):
        return False
    cmd = "redistribute "+route_type+" route-map "+routemap
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set redistribute route-map"\
                         " configuration failed"
    return True
def configure_neighbor(dut, as_num1, network, as_num2):
    if (enterRouterContext(dut, as_num1) is False):
        return False

    cmd = "neighbor "+network+" remote-as "+as_num2
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor config failed"
    return True

def configure_neighbor_rmap(dut, as_num1, network, as_num2, routemap):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+network+" route-map "+routemap+" out"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor route-map config failed"
    return True


def verify_bgp_routes(dut, network, next_hop):
    dump = SwitchVtyshUtils.vtysh_cmd(dut, "show ip bgp")
    routes = dump.split(VTYSH_CR)
    for route in routes:
        if network in route and next_hop in route:
            return True
    return False

def wait_for_route(dut, network, next_hop, condition=True) :
    for i in range(MAX_WAIT_TIME):
        found = verify_bgp_routes(dut, network, next_hop)
        if found == condition:
            if condition:
                result = "Redistribute configuration successfull"
            else:
                result = "Redistribute configuration not successfull"
            LogOutput('info', result)
            return found
        sleep(1)
    info("### Condition not met after %s seconds ###\n" %
           MAX_WAIT_TIME)
    return found

def configure(**kwargs):
    '''
     - Configures the IP address in SW1, SW2 and SW3
     - Creates router bgp instance on SW1 and SW2
     - Configures the router id
     - Configures the network range
     - Configure redistribute and neighbor
    '''

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    '''
    - Enable the link.
    - Set IP for the switches.
    '''
    # Enabling interface 1 SW1.
    LogOutput('info', "Enabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True,
                                interface=switch1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface1 on SW1"

    # Assigning an IPv4 address on interface 1 of SW1
    LogOutput('info', "Configuring IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr=IP_ADDR1, mask=DEFAULT_PL,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface 1 of SW1"

    # Enabling interface 1 SW2
    LogOutput('info', "Enabling interface1 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on SW2"

    # Assigning an IPv4 address on interface 1 for link 1 SW2
    LogOutput('info', "Configuring IPv4 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr=IP_ADDR2, mask=DEFAULT_PL,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface 1 of SW2"

    # Enabling interface 2 SW2
    LogOutput('info', "Enabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 2 on SW2"

    # Assigning an IPv4 address on interface 1 for link 2 SW2
    LogOutput('info', "Configuring IPv4 address on link 2 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr=IP_ADDR3, mask=DEFAULT_PL,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface 2 of SW2"

    # Enabling interface 1 SW3
    LogOutput('info', "Enabling interface1 on SW3")
    retStruct = InterfaceEnable(deviceObj=switch3, enable=True,
                                interface=switch3.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on SW3"

    # Assigning an IPv4 address on interface 1 for link 2 SW3
    LogOutput('info', "Configuring IPv4 address on link 2 SW3")
    retStruct = InterfaceIpConfig(deviceObj=switch3,
                                  interface=switch3.linkPortMapping['lnk02'],
                                  addr=IP_ADDR4, mask=DEFAULT_PL,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface 1 of SW3"

    '''
    For SW2 and SW3, configure bgp
    '''
    LogOutput('info', "Configuring static routes on SW2")
    result = configure_static_route(switch2,"12.0.0.0/8","7.0.0.1")
    assert result is True, "Setting static route configuration failed for SW2"
    LogOutput('info', "Configuring route-map routes on SW2")
    result = configure_route_map(switch2,"BGP_Rmap")
    assert result is True, "Setting route-map configuration failed for SW2"
    LogOutput('info', "Configuring router-id on SW2")
    result = configure_router_id(switch2, AS_NUM1, SW2_ROUTER_ID)
    assert result is True, "BGP router id set failed for SW2"
    LogOutput('info', "Configuring networks on SW2")
    result = configure_network(switch2, AS_NUM1, "10.0.0.0/8")
    assert result is True, "BGP network creation failed for SW2"
    LogOutput('info', "Configuring redistribute configuration on SW2")
    result = configure_redistribute(switch2, AS_NUM1, "connected")
    assert result is True, "BGP redistribute connected configuration failed"\
                           " for SW2"
    LogOutput('info', "Configuring redistribute route-map configuration on SW2")
    result = configure_redistribute_rmap(switch2, AS_NUM1, "static","BGP_Rmap")
    assert result is True, "BGP redistribute static route-map configuration"\
                           " failed for SW2"
    LogOutput('info', "Configuring bgp neighbor on SW2")
    result = configure_neighbor(switch2, AS_NUM1, IP_ADDR4, AS_NUM2)
    assert result is True, "BGP neighbor configuration failed for SW2"
    LogOutput('info', "Applying route-map to bgp neighbor on SW2")
    result = configure_neighbor_rmap(switch2, AS_NUM1, IP_ADDR4, AS_NUM2,\
                                     "BGP_Rmap")
    assert result is True, "BGP neighbor route-map configuration failed for SW2"
    exitContext(switch2)

    LogOutput('info', "Configuring router-id on SW3")
    result = configure_router_id(switch3, AS_NUM2, SW3_ROUTER_ID)
    assert result is True, "BGP router id set failed for SW3"
    LogOutput('info', "Configuring networks on SW2")
    result = configure_network(switch3, AS_NUM2, "19.0.0.0/8")
    assert result is True, "BGP network creation failed for SW3"
    result = configure_neighbor(switch3, AS_NUM2, IP_ADDR3, AS_NUM1)
    assert result is True, "BGP neighbor configuration failed for SW3"
    exitContext(switch3)

class Test_bgp_redistribute_configuration:
    def setup_class(cls):
        Test_bgp_redistribute_configuration.testObj = \
            testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_bgp_redistribute_configuration.topoObj = \
            Test_bgp_redistribute_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_bgp_redistribute_configuration.topoObj.terminate_nodes()

    def test_configure(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        configure(switch1=dut01Obj, switch2=dut02Obj, switch3=dut03Obj)

        LogOutput('info', "Verifying redistribute configuration")
        wait_for_route(dut02Obj, "7.0.0.0", "0.0.0.0")
        wait_for_route(dut02Obj, "8.0.0.0", "0.0.0.0")
        wait_for_route(dut02Obj, "12.0.0.0", "7.0.0.1")
