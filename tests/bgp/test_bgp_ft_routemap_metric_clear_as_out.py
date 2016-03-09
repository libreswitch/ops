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
+---------------+             +---------------+           +---------------+
|               |             |               |           |               |
| Switch 1     1+-------------+1  Switch 2   2+-----------+2   Switch 3   |
|               |             |               |           |               |
|               |             |               |           |               |
+---------------+             +---------------+           +---------------+

switch 1 configuration
----------------------

#  router bgp 1
#  bgp router-id 8.0.0.1
#  network 11.0.0.0/8
#  neighbor 8.0.0.2 remote-as 2
#  neighbor 8.0.0.2 route-map 1 in

#  interface 1
#  no shutdown
#  ip address 8.0.0.1/8
switch 2 configuration
----------------------

# router bgp 2
#  bgp router-id 8.0.0.2
#  network 15.0.0.0/8
#  neighbor 8.0.0.1 remote-as 1
#  neighbor 40.0.0.2 remote-as 3

interface 1
    no shutdown
    ip address 8.0.0.2/8
interface 2
    no shutdown
    ip address 40.0.0.1/8
switch 3 configuration
----------------------

# router bgp 3
#  bgp router-id 8.0.0.3
#  network 12.0.0.0/8
#  neighbor 40.0.0.1 remote-as 2

interface 1
    no shutdown
    ip address 40.0.0.2/8

'''

IP_ADDR1 = "8.0.0.1"
IP_ADDR2_1 = "8.0.0.2"
IP_ADDR2_2 = "40.0.0.1"
IP_ADDR3 = "40.0.0.2"
DEFAULT_PL = "8"

SW1_ROUTER_ID = "8.0.0.1"
SW2_ROUTER_ID = "8.0.0.2"
SW3_ROUTER_ID = "8.0.0.3"


NETWORK_SW1 = "11.0.0.0/8"
NETWORK_SW2 = "15.0.0.0/8"
NETWORK_SW3 = "12.0.0.0/8"

AS_NUM1 = "1"
AS_NUM2 = "2"
AS_NUM3 = "3"

VTYSH_CR = '\r\n'
MAX_WAIT_TIME = 100

# Topology definition
topoDict = {"topoExecution": 5000,
            "topoTarget": "dut01 dut02 dut03",
            "topoDevices": "dut01 dut02 dut03",
            "topoLinks": "lnk01:dut01:dut02, lnk02:dut02:dut03",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch"}

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
                result = "Configuration successfull"
            else:
                result = "Configuration not successfull"
            LogOutput('info', result)
            return found
        sleep(1)
    info("### Condition not met after %s seconds ###\n" %
           MAX_WAIT_TIME)
    return found

def enterVtyshContext(dut):
    retStruct = dut.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"
    return True

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

def clearSoftOutAsn(dut, asn):
    if (enterConfigShell(dut) is False):
        return False

    devIntReturn = dut.DeviceInteract(command="do clear bgp "+ asn +
                                      " soft out")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to execute clear bgp %s soft out" % asn
    return True

def enterNoRouterContext(dut,as_num):
    if (enterConfigShell(dut) is False):
        return False

    devIntReturn = dut.DeviceInteract(command="no router bgp "+ as_num)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to exit BGP context"
    return True

def exitVtyshContext(dut):
    retStruct = dut.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"
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

def configure_route_map_set_metric(dut, routemap, as_num, metric):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "route-map "+routemap+" permit 20"
    cmd1 = "set metric "+metric
    devIntReturn = dut.DeviceInteract(command=cmd)
    devIntReturn = dut.DeviceInteract(command=cmd1)
    return True

def configure_route_map_match_metric(dut, routemap, as_num, metric):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "route-map "+routemap+" permit 20"
    cmd1 = "match metric "+metric
    devIntReturn = dut.DeviceInteract(command=cmd)
    devIntReturn = dut.DeviceInteract(command=cmd1)
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

def configure_no_route_map(dut, routemap):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "no route-map "+routemap+" permit 20"
    devIntReturn = dut.DeviceInteract(command=cmd)
    return True


def configure_neighbor_rmap_out(dut, as_num1, network, as_num2, routemap):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+network+" route-map "+routemap+" out"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor route-map out config failed"
    return True

def configure_peer_group(dut, as_num1, group):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+group+" peer-group"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set peer group in config failed"
    return True

def configure_peer_group_member(dut, as_num1, peer_ip, group):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+peer_ip+" peer-group "+group
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set peer group memeber in config failed"
    return True

def configure_neighbor_rmap_in(dut, as_num1, network, as_num2, routemap):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+network+" route-map "+routemap+" in"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor route-map in config failed"
    return True

def verify_routemap_set_metric_clear_soft_out_as(**kwargs):
    LogOutput('info',"\n\n########## Verifying route-map set metric test 1" \
                     " for clear soft out as command##########\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    metric = "10"

    LogOutput('info',"Configuring route-map on SW2")
    result=configure_route_map_set_metric(switch2,"BGP_OUT",AS_NUM2, metric)
    assert result is True, "Failed to configure route-map on SW2"

    LogOutput('info',"Configuring route context on SW2")
    result = enterRouterContext(switch2,AS_NUM2)
    assert result is True, "Failed to configure router Context on SW2"

    LogOutput('info',"Configuring neighbor route-map on SW2 for peer 1")
    result = configure_neighbor_rmap_out(switch2, AS_NUM2, IP_ADDR1, AS_NUM1,
                                         "BGP_OUT")
    assert result is True, "Failed to configure neighbor route-map on SW2" \
                           "for peer 1"

    LogOutput('info',"Configuring neighbor route-map on SW2 for peer 3")
    result = configure_neighbor_rmap_out(switch2, AS_NUM2, IP_ADDR3, AS_NUM3,
                                         "BGP_OUT")
    assert result is True, "Failed to configure neighbor route-map on SW2" \
                           "for peer 3"
    clearSoftOutAsn(switch2, AS_NUM1)
    clearSoftOutAsn(switch2, AS_NUM3)

    exitContext(switch1)
    exitContext(switch2)
    exitContext(switch3)

    network = neighbor_network_2 = NETWORK_SW2
    metric_str = ' 10 '
    set_metric_flag_1 = False
    set_metric_flag_3 = False
    next_hop1 = "8.0.0.2"
    next_hop3 = "40.0.0.1"

    found = wait_for_route(switch1, network,
                           next_hop1)

    assert found, "Could not find route (%s -> %s) on %s" % \
                              (network, next_hop1, switch1.name)

    found = wait_for_route(switch3, network,
                           next_hop3)

    assert found, "Could not find route (%s -> %s) on %s" % \
                              (network, next_hop3, switch3.name)


    dump = SwitchVtyshUtils.vtysh_cmd(switch1, "sh ip bgp")
    lines = dump.split('\n')
    for line in lines:
        print line
        if neighbor_network_2 in line and metric_str in line:
            set_metric_flag_1 = True

    assert (set_metric_flag_1 == True), "Failure to verify clear bgp as soft" \
                                        " out command on peer 2" \
                                        " for neighbor %s" % IP_ADDR1
    LogOutput('info',"### 'clear bgp as soft out' validated succesfully " \
                     "on peer 2 for neighbor %s###\n" % IP_ADDR1)

    dump = SwitchVtyshUtils.vtysh_cmd(switch3, "sh ip bgp")
    lines = dump.split('\n')
    for line in lines:
        print line
        if neighbor_network_2 in line and metric_str in line:
            set_metric_flag_3 = True

    assert (set_metric_flag_3 == True), "Failure to verify clear bgp as soft" \
                                        " out command on peer 2" \
                                        " for neighbor %s" % IP_ADDR3
    LogOutput('info',"### 'clear bgp as soft out' validated succesfully " \
                     "on peer 2 for neighbor %s###\n" % IP_ADDR3)

def configure(**kwargs):
    '''
     - Configures the IP address in SW1, SW2 and SW3
     - Creates router bgp instance on SW1, SW2 and SW3
     - Configures the router id
     - Configures the network range
     - Configure neighbor
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
                                  addr=IP_ADDR2_1, mask=DEFAULT_PL,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface 1 of SW2"
    # Enabling interface 2 SW2
    LogOutput('info', "Enabling interface 2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 2 on SW2"

    # Assigning an IPv4 address on interface 2 for link 2 SW2
    LogOutput('info', "Configuring IPv4 address on link 2 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr=IP_ADDR2_2, mask=DEFAULT_PL,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface 2 of SW2"


    # Enabling interface 1 SW3
    LogOutput('info', "Enabling interface 1 on SW3")
    retStruct = InterfaceEnable(deviceObj=switch3, enable=True,
                                interface=switch3.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on SW3"

    # Assigning an IPv4 address on interface 1 for link 2 SW3
    LogOutput('info', "Configuring IPv4 address on link 2 SW3")
    retStruct = InterfaceIpConfig(deviceObj=switch3,
                                  interface=switch3.linkPortMapping['lnk02'],
                                  addr=IP_ADDR3, mask=DEFAULT_PL,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface 2 of SW3"

#   For SW1, SW2 and SW3, configure bgp
    LogOutput('info',"Configuring route context on SW1")
    result = enterRouterContext(switch1,AS_NUM1)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring router id on SW1")
    result = configure_router_id(switch1,AS_NUM1,SW1_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW1"
    LogOutput('info',"Configuring networks on SW1")
    result = configure_network(switch1,AS_NUM1,"11.0.0.0/8")
    assert result is True, "Failed to configure network on SW1"
    LogOutput('info',"Configuring neighbors on SW1")
    result = configure_neighbor(switch1,AS_NUM1,IP_ADDR2_1,AS_NUM2)
    assert result is True, "Failed to configure neighbor on SW1"

    LogOutput('info',"Configuring route context on SW2")
    result = enterRouterContext(switch2, AS_NUM2)
    assert result is True, "Failed to configure router Context on SW2"
    LogOutput('info',"Configuring router id on SW2")
    result = configure_router_id(switch2,AS_NUM2,SW2_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW2"
    LogOutput('info',"Configuring networks on SW2")
    result = configure_network(switch2,AS_NUM2,"15.0.0.0/8")
    assert result is True, "Failed to configure network on SW2"
    LogOutput('info',"Configuring neighbor 1 on SW2")
    result = configure_neighbor(switch2,AS_NUM2,IP_ADDR1,AS_NUM1)
    assert result is True, "Failed to configure neighbor 1 on SW2"
    LogOutput('info',"Configuring neighbor 3 on SW2")
    result = configure_neighbor(switch2,AS_NUM2,IP_ADDR3, AS_NUM3)
    assert result is True, "Failed to configure neighbor 3 on SW2"

    LogOutput('info',"Configuring route context on SW3")
    result = enterRouterContext(switch3, AS_NUM3)
    assert result is True, "Failed to configure router Context on SW3"
    LogOutput('info',"Configuring router id on SW3")
    result = configure_router_id(switch3,AS_NUM3,SW3_ROUTER_ID)
    assert result is True, "Failed to configure router Context on SW3"
    LogOutput('info',"Configuring networks on SW3")
    result = configure_network(switch3,AS_NUM3,"12.0.0.0/8")
    assert result is True, "Failed to configure network on SW3"
    LogOutput('info',"Configuring neighbor on SW3")
    result = configure_neighbor(switch3,AS_NUM3,IP_ADDR2_2,AS_NUM2)
    assert result is True, "Failed to configure neighbor on SW3"

class Test_bgp_metric_clear_as_configuration:
    def setup_class(cls):
        Test_bgp_metric_clear_as_configuration.testObj = \
            testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_bgp_metric_clear_as_configuration.topoObj = \
            Test_bgp_metric_clear_as_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_bgp_metric_clear_as_configuration.topoObj.terminate_nodes()

    def test_configure(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")

        configure(switch1=dut01Obj, switch2=dut02Obj, switch3=dut03Obj)
        verify_routemap_set_metric_clear_soft_out_as(switch1=dut01Obj,
                                                     switch2=dut02Obj,
                                                     switch3=dut03Obj)
