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
import math
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *
from opstestfw.switch.CLI.InterfaceIpConfig import InterfaceIpConfig
from opsvsiutils.vtyshutils import *

'''
TOPOLOGY
+---------------+             +---------------+
|               |             |               |
| Switch 1     1+-------------+1  Switch 2    |
|               |             |               |
|               |             |               |
+---------------+             +---------------+

switch 1 configurations:
----------------------------------------------
route-map 1 permit 1
     set ipv6 next-hop global 2001::3
!
router bgp 1
     bgp router-id 9.0.0.1
     network 2ccd:1:1::/67
     network 5d5d:1:1::/69
     network 7d5d:1:1::/85
     network 9966:1:2::/85
     neighbor 2001::2 remote-as 2
     neighbor 2001::2 route-map 1 out
!
vlan 1
    no shutdown
interface 1
    no shutdown
    ipv6 address 2001::1/64

switch 2 configurations:
------------------------------------------------

route-map 1 permit 1
     set ipv6 next-hop local fe80::c823:75ff:fe57:945d
!
router bgp 2
     bgp router-id 9.0.0.2
     network 3dcd:1:1::/64
     neighbor 2001::1 remote-as 1
     neighbor 2001::1 route-map 1 in
!
vlan 1
    no shutdown
interface 1
    no shutdown
    ipv6 address 2001::2/64
------------------------------------------------
'''

IP_ADDR1 = "2001::1"
IP_ADDR2 = "2001::2"

SW1_ROUTER_ID = "9.0.0.1"
SW2_ROUTER_ID = "9.0.0.2"

AS_NUM1 = "1"
AS_NUM2 = "2"

MAX_WAIT_TIME = 100
topoDict = {"topoExecution": 5000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch"}

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

def enterNoRouterContext(dut,as_num):
    if (enterConfigShell(dut) is False):
        return False

    devIntReturn = dut.DeviceInteract(command="no router bgp "+ as_num)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to exit BGP context"
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

def configure_no_route_map(dut, routemap):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "no route-map "+routemap+" permit 20"
    devIntReturn = dut.DeviceInteract(command=cmd)
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

def configure_neighbor(dut, as_num1, network, as_num2):
    if (enterRouterContext(dut, as_num1) is False):
        return False

    cmd = "neighbor "+network+" remote-as "+as_num2
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor config failed"
    return True

def configure_neighbor_rmap_out(dut, as_num1, network, as_num2, routemap):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+network+" route-map "+routemap+" out"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor route-map out config failed"
    return True

def configure_neighbor_rmap_in(dut, as_num1, network, as_num2, routemap):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+network+" route-map "+routemap+" in"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor route-map in config failed"
    return True

def configure_route_map_set_ipv6(dut,routemap,nexthop):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "route-map "+routemap+" permit 20"
    cmd1 = "set ipv6 next-hop global "+nexthop
    devIntReturn = dut.DeviceInteract(command=cmd)
    devIntReturn = dut.DeviceInteract(command=cmd1)
    return True

def configure_route_map_match_ipv6(dut,routemap,nexthop):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "route-map "+routemap+" permit 20"
    cmd1 = "match ipv6 next-hop "+nexthop
    devIntReturn = dut.DeviceInteract(command=cmd)
    devIntReturn = dut.DeviceInteract(command=cmd1)
    return True

def configure_route_map_match_ipv6_deny(dut,routemap,nexthop):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "route-map "+routemap+" deny 20"
    cmd1 = "match ipv6 next-hop "+nexthop
    devIntReturn = dut.DeviceInteract(command=cmd)
    devIntReturn = dut.DeviceInteract(command=cmd1)
    return True

def verify_bgp_routes(dut, network, next_hop):
    dump = SwitchVtyshUtils.vtysh_cmd(dut, "show ipv6 bgp")
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
                result = "configuration successfull"
            else:
                result = "configuration not successfull"
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

    # Assigning an IPv6 address on interface 1 of SW1
    LogOutput('info', "Configuring IPv6 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr=IP_ADDR1, mask="64",ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address on interface 1 of SW1"

    # Assigning an IPv4 address on interface 1 of SW1
    LogOutput('info', "Configuring IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr=SW1_ROUTER_ID, mask="8",
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

    # Assigning an IPv6 address on interface 1 for link 1 SW2
    LogOutput('info', "Configuring IPv4 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr=IP_ADDR2, mask="64",ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address on interface 1 of SW2"

    # Assigning an IPv4 address on interface 1 for link 1 SW2
    LogOutput('info', "Configuring IPv4 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr=SW2_ROUTER_ID, mask="8",
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface 1 of SW2"


    '''
    For SW1 and SW2, configure bgp
    '''
    LogOutput('info',"Configuring route context on SW1")
    result = enterRouterContext(switch1,AS_NUM1)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring router id on SW1")
    result = configure_router_id(switch1,AS_NUM1,SW1_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"2ccd:1:1::/67")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"5d5d:1:1::/69")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"7d5d:1:1::/85")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"9966:1:2::/85")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring neighbors on SW1")
    result = configure_neighbor(switch1,AS_NUM1,IP_ADDR2,AS_NUM2)
    assert result is True, "Failed to configur neighbor on SW1"

    LogOutput('info',"Configuring route context on SW2")
    result = enterRouterContext(switch2, AS_NUM2)
    assert result is True, "Failed to configure router Context on SW2"
    LogOutput('info',"Configuring router id on SW2")
    result = configure_router_id(switch2,AS_NUM2,SW2_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW2"
    LogOutput('info',"Configuring networks on SW2")
    result = configure_network(switch2,AS_NUM2,"3dcd:1:1::/64")
    assert result is True, "Failed to configure network on SW2"
    LogOutput('info',"Configuring neighbors on SW2")
    result = configure_neighbor(switch2,AS_NUM2,IP_ADDR1,AS_NUM1)
    assert result is True, "Failed to configur neighbor on SW2"

def verify_routemap_set_ipv6(**kwargs):
    LogOutput('info',"\n########## Verifying route-map set ipv6 global##########\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    LogOutput('info',"Configuring no router bgp")
    result = enterNoRouterContext(switch1,AS_NUM1)
    assert result is True,"Failed to configure router Context on SW1"

    LogOutput('info',"Configuring route-map on SW1")
    result=configure_route_map_set_ipv6(switch1,"BGP_OUT","2001::3")
    assert result is True, "Failed to configure route-map on SW1"

    LogOutput('info',"Configuring route context on SW1")
    result = enterRouterContext(switch1,AS_NUM1)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring router id on SW1")
    result = configure_router_id(switch1,AS_NUM1,SW1_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"2ccd:1:1::/67")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"5d5d:1:1::/69")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"7d5d:1:1::/85")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"9966:1:2::/85")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring neighbors on SW1")
    result = configure_neighbor(switch1,AS_NUM1,IP_ADDR2,AS_NUM2)
    assert result is True, "Failed to configure neighbor on SW1"

    LogOutput('info',"Configuring neighbor route-map on SW1")
    result = configure_neighbor_rmap_out(switch1, AS_NUM1, IP_ADDR2, AS_NUM2, "BGP_OUT")
    assert result is True, "Failed to configure neighbor route-map on SW1"


    exitContext(switch2)
    wait_for_route(switch2, "2ccd:1:1::", "2001::3")
    wait_for_route(switch2, "9966:1:2::", "2001::3")
    wait_for_route(switch2, "5d5d:1:1::", "2001::3")
    wait_for_route(switch2, "7d5d:1:1::", "2001::3")
    wait_for_route(switch2, "3dcd:1:1::", "::")

    dump = SwitchVtyshUtils.vtysh_cmd(switch2, "sh ipv6 bgp")

    set_ipv6_flag = False
    ipv6_nexthop_count = 0

    lines = dump.split('\n')
    for line in lines:
        if "2ccd:1:1::" in line or "5d5d:1:1::" in line or \
           "7d5d:1:1::" in line or "9966:1:2::" in line  and "2001::3" in line:
            ipv6_nexthop_count += 1

    if ipv6_nexthop_count == 4:
       set_ipv6_flag = True

    assert (set_ipv6_flag == True), "Failure to configure 'set ipv6 nexthop global'"

    LogOutput('info',"### 'set ipv6 nexthop global' running succesfully ###\n")


def verify_routemap_match_ipv6(**kwargs):
    LogOutput('info',"\n\n########## Verifying route-map match ipv6 ##########\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    LogOutput('info',"Configuring no router bgp on SW2")
    result = enterNoRouterContext(switch2,AS_NUM2)
    assert result is True,"Failed to configure router Context on SW2"

    LogOutput('info',"Configuring route-map on SW2")
    result=configure_route_map_match_ipv6(switch2,"BGP_IN","2001::3")
    assert result is True, "Failed to configure route-map on SW2"

    LogOutput('info',"Configuring route context on SW2")
    result = enterRouterContext(switch2,AS_NUM2)
    assert result is True, "Failed to configure router Context on SW2"
    LogOutput('info',"Configuring router id on SW2")
    result = configure_router_id(switch2,AS_NUM2,SW2_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW2"

    LogOutput('info',"Configuring networks on SW2")
    result = configure_network(switch2,AS_NUM2,"3dcd:1:1::/64")
    assert result is True, "Failed to configure network on SW2"

    LogOutput('info',"Configuring neighbors on SW2")
    result = configure_neighbor(switch2,AS_NUM2,IP_ADDR1,AS_NUM1)
    assert result is True, "Failed to configur neighbor on SW2"

    LogOutput('info',"Configuring neighbor route-map on SW2")
    result = configure_neighbor_rmap_in(switch2, AS_NUM2, IP_ADDR1, AS_NUM1, "BGP_IN")
    assert result is True, "Failed to configure neighbor route-map on SW2"

    exitContext(switch2)
    wait_for_route(switch2, "2ccd:1:1::", "2001::3")
    wait_for_route(switch2, "9966:1:2::", "2001::3")
    wait_for_route(switch2, "5d5d:1:1::", "2001::3")
    wait_for_route(switch2, "7d5d:1:1::", "2001::3")
    wait_for_route(switch2, "3dcd:1:1::", "::")


    dump = SwitchVtyshUtils.vtysh_cmd(switch2, "sh ipv6 bgp")

    set_ipv6_flag = False
    ipv6_nexthop_count = 0

    lines = dump.split('\n')
    for line in lines:
        if "2ccd:1:1::" in line or "5d5d:1:1::" in line or \
           "7d5d:1:1::" in line or "9966:1:2::" in line  and "2001::3" in line:
            ipv6_nexthop_count += 1

    if ipv6_nexthop_count == 4:
       set_ipv6_flag = True

    assert (set_ipv6_flag == True), "Failure to configure 'match ipv6 next-hop'"

    LogOutput('info',"### 'match ipv6 next-hop' running succesfully ###\n")

def verify_routemap_match_ipv6_1(**kwargs):
    LogOutput('info',"\n\n########## Verifying route-map match ipv6 ##########\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    LogOutput('info',"Configuring no router bgp on SW2")
    result = enterNoRouterContext(switch2,AS_NUM2)
    assert result is True,"Failed to configure router Context on SW2"

    LogOutput('info',"Configuring route-map on SW2")
    result=configure_no_route_map(switch2,"BGP_IN")
    assert result is True, "Failed to configure route-map on SW2"

    LogOutput('info',"Configuring route-map on SW2")
    result=configure_route_map_match_ipv6_deny(switch2,"BGP_IN","2001::3")
    assert result is True, "Failed to configure route-map on SW2"

    LogOutput('info',"Configuring route context on SW2")
    result = enterRouterContext(switch2,AS_NUM2)
    assert result is True, "Failed to configure router Context on SW2"
    LogOutput('info',"Configuring router id on SW2")
    result = configure_router_id(switch2,AS_NUM2,SW2_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW2"

    LogOutput('info',"Configuring networks on SW2")
    result = configure_network(switch2,AS_NUM2,"3dcd:1:1::/64")
    assert result is True, "Failed to configure network on SW2"

    LogOutput('info',"Configuring neighbors on SW2")
    result = configure_neighbor(switch2,AS_NUM2,IP_ADDR1,AS_NUM1)
    assert result is True, "Failed to configur neighbor on SW2"

    LogOutput('info',"Configuring neighbor route-map on SW2")
    result = configure_neighbor_rmap_in(switch2, AS_NUM2, IP_ADDR1, AS_NUM1, "BGP_IN")
    assert result is True, "Failed to configure neighbor route-map on SW2"

    exitContext(switch2)
    dump = SwitchVtyshUtils.vtysh_cmd(switch2, "sh ipv6 bgp")

    set_ipv6_flag = False
    ipv6_nexthop_count = 0

    lines = dump.split('\n')
    for line in lines:
        if "2ccd:1:1::" in line or "5d5d:1:1::" in line or \
           "7d5d:1:1::" in line or "9966:1:2::" in line  and "2001::3" in line:
            ipv6_nexthop_count += 1

    if ipv6_nexthop_count == 4:
       set_ipv6_flag = True

    assert (set_ipv6_flag == False), "Failure to configure 'match ipv6 next-hop'"

    LogOutput('info',"### 'match ipv6 next-hop' running succesfully ###\n")

@pytest.mark.timeout(600)
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

        configure(switch1=dut01Obj, switch2=dut02Obj)
        verify_routemap_set_ipv6(switch1=dut01Obj, switch2=dut02Obj)
        verify_routemap_match_ipv6(switch1=dut01Obj, switch2=dut02Obj)
        verify_routemap_match_ipv6_1(switch1=dut01Obj, switch2=dut02Obj)
