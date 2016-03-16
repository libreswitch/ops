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

switch 1 configuration
----------------------

#  router bgp 1
#  bgp router-id 8.0.0.1
#  network 9.0.0.0/8
#  neighbor 8.0.0.2 remote-as 2
#  neighbor 8.0.0.2 route-map 1 in

#  interface 1
#  no shutdown
#  ip address 8.0.0.1/8
switch 2 configuration
----------------------

# router bgp 2
#  bgp router-id 8.0.0.2
#  network 10.0.0.0/8
#  network 11.0.0.0/8
#  neighbor 8.0.0.1 remote-as 1

interface 1
    no shutdown
    ip address 8.0.0.2/8

'''

IP_ADDR1 = "8.0.0.1"
IP_ADDR2 = "8.0.0.2"

DEFAULT_PL = "8"

SW1_ROUTER_ID = "8.0.0.1"
SW2_ROUTER_ID = "8.0.0.2"

AS_NUM1 = "1"
AS_NUM2 = "2"

VTYSH_CR = '\r\n'
MAX_WAIT_TIME = 100
# Topology definition
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

def configure_route_map_set_community(dut, routemap, as_num):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "route-map "+routemap+" permit 20"
    cmd1 = "set community 2:0 3:0 4:0"
    devIntReturn = dut.DeviceInteract(command=cmd)
    devIntReturn = dut.DeviceInteract(command=cmd1)
    return True

def configure_route_map_set_commlist_delete(dut, routemap, as_num,commlist):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "route-map "+routemap+" permit 20"
    cmd1 = "set comm-list "+commlist+" delete"
    devIntReturn = dut.DeviceInteract(command=cmd)
    devIntReturn = dut.DeviceInteract(command=cmd1)
    return True

def configure_ip_community(dut,commlist,community):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "ip community-list "+commlist+" permit "+community
    devIntReturn = dut.DeviceInteract(command=cmd)
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
                result = "configuration successfull"
            else:
                result = "configuration not successfull"
            LogOutput('info', result)
            return found
        sleep(1)
    info("### Condition not met after %s seconds ###\n" %
           MAX_WAIT_TIME)
    return found

def verify_routemap_set_community(**kwargs):
    LogOutput('info',"\n\n########## Verifying route-map 'set community'##########\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    LogOutput('info',"Configuring no router bgp on SW1")
    result = enterNoRouterContext(switch1,AS_NUM1)
    assert result is True,"Failed to configure router Context on SW1"

    LogOutput('info',"Configuring route-map on SW1")
    result=configure_route_map_set_community(switch1,"BGP_OUT",AS_NUM1)
    assert result is True, "Failed to configure route-map on SW1"

    LogOutput('info',"Configuring route context on SW1")
    result = enterRouterContext(switch1,AS_NUM1)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring router id on SW1")
    result = configure_router_id(switch1,AS_NUM1,SW1_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"9.0.0.0/8")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring neighbors on SW1")
    result = configure_neighbor(switch1,AS_NUM1,IP_ADDR2,AS_NUM2)
    assert result is True, "Failed to configur neighbor on SW1"
    LogOutput('info',"configuring neighbor routemap on SW1")
    result = configure_neighbor_rmap_out(switch1,  AS_NUM1, IP_ADDR2, AS_NUM2, "BGP_OUT")
    assert result is True, "Failed to configure neighbor route-map on SW2"

    exitContext(switch2)
    wait_for_route(switch2, "10.0.0.0", "0.0.0.0")
    wait_for_route(switch2, "11.0.0.0", "0.0.0.0")
    wait_for_route(switch2, "9.0.0.0", "8.0.0.1")

    dump = SwitchVtyshUtils.vtysh_cmd(switch2, "sh ip bgp 9.0.0.0")
    set_community_flag = False

    lines = dump.split('\n')
    for line in lines:
        if 'Community: 2:0 3:0 4:0' in line:
            set_community_flag = True


    assert (set_community_flag == True) , "Failed to configure 'set community'"

    LogOutput('info',"### 'set community' running succesfully ###\n")


def verify_routemap_set_comm_list(**kwargs):
    LogOutput('info',"\n\n########## Verifying route-map 'set comm-list delete'##########\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    LogOutput('info',"Configuring no router bgp on SW2")
    result = enterNoRouterContext(switch2,AS_NUM2)
    assert result is True,"Failed to configure router Context on SW2"

    LogOutput('info',"Configuring community-list on SW2")
    result=configure_ip_community(switch2,"test","2:0")
    assert result is True, "Failed to configure route-map on SW2"


    LogOutput('info',"Configuring route-map on SW2")
    result=configure_route_map_set_commlist_delete(switch2,"BGP_IN",AS_NUM2,"test")
    assert result is True, "Failed to configure route-map on SW2"

    LogOutput('info',"Configuring route context on SW2")
    result = enterRouterContext(switch2,AS_NUM2)
    assert result is True, "Failed to configure router Context on SW2"
    LogOutput('info',"Configuring router id on SW2")
    result = configure_router_id(switch2,AS_NUM2,SW2_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW2"
    LogOutput('info',"Configuring networks on SW2")
    result = configure_network(switch2,AS_NUM2,"10.0.0.0/8")
    assert result is True, "Failed to configure network on SW2"
    LogOutput('info',"Configuring networks on SW2")
    result = configure_network(switch2,AS_NUM2,"11.0.0.0/8")
    assert result is True, "Failed to configure network on SW2"

    LogOutput('info',"Configuring neighbors on SW2")
    result = configure_neighbor(switch2,AS_NUM2,IP_ADDR1,AS_NUM1)
    assert result is True, "Failed to configur neighbor on SW2"
    LogOutput('info',"configuring neighbor routemap on SW2")
    result = configure_neighbor_rmap_in(switch2,  AS_NUM2, IP_ADDR1, AS_NUM1, "BGP_IN")
    assert result is True, "Failed to configure neighbor route-map on SW2"

    exitContext(switch2)
    wait_for_route(switch2, "10.0.0.0", "0.0.0.0")
    wait_for_route(switch2, "11.0.0.0", "0.0.0.0")
    wait_for_route(switch2, "9.0.0.0", "8.0.0.1")

    dump = SwitchVtyshUtils.vtysh_cmd(switch2, "sh ip bgp 9.0.0.0")
    set_aggregator = False

    lines = dump.split('\n')
    for line in lines:
        if 'Community: 2:0 ' in line:
            set_aggregator = True


    assert (set_aggregator == False) , "Failed to configure 'set comm-list delete'"

    LogOutput('info',"### 'set comm-list delete' running succesfully ###\n")


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




#    For SW1 and SW2, configure bgp
    LogOutput('info',"Configuring route context on SW1")
    result = enterRouterContext(switch1,AS_NUM1)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring router id on SW1")
    result = configure_router_id(switch1,AS_NUM1,SW1_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"9.0.0.0/8")
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
    result = configure_network(switch2,AS_NUM2,"10.0.0.0/8")
    assert result is True, "Failed to configure network on SW2"
    LogOutput('info',"Configuring networks on SW2")
    result = configure_network(switch2,AS_NUM2,"11.0.0.0/8")
    assert result is True, "Failed to configure network on SW2"

    LogOutput('info',"Configuring neighbors on SW2")
    result = configure_neighbor(switch2,AS_NUM2,IP_ADDR1,AS_NUM1)
    assert result is True, "Failed to configur neighbor on SW2"


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

        verify_routemap_set_community(switch1=dut01Obj, switch2=dut02Obj)
        verify_routemap_set_comm_list(switch1=dut01Obj, switch2=dut02Obj)
