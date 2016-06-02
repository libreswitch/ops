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
from opsvsiutils.bgpconfig import *

#
# This test checks the following commands:
#   * ipv6 prefix-list <prefix-list-name> seq <seq-num> (permit|deny) <prefix>
#            ge <prefix length> le <prefix length>
#   * route map <route-map-name> permit seq_num
#   *   match ipv6 address prefix-list <prefix-list>
#   *
#   * network X:X::X:X/M
#

'''
TOPOLOGY
+---------------+             +---------------+
|               |             |               |
| Switch 1     1+-------------+1  Switch 2    |
|  BGP1         |             |     BGP2      |
|               |             |               |
+---------------+             +---------------+


Configuration of BGBGP1_IN:
----------------------------------------------------------------------------
!
ipv6 prefix-list BGP1_IN seq 10 deny 9966:1:2::/64 ge 80 le 100
ipv6 prefix-list BGP1_IN seq 20 permit 7d5d:1:1::/64 le 70
ipv6 prefix-list BGP1_IN seq 30 permit 5d5d:1:1::/64 le 70
ipv6 prefix-list BGP1_IN seq 40 permit 2ccd:1:1::/64 ge 65
ipv6 prefix-list BGP1_IN seq 50 permit 4ddc:1:1::/64
!
!
!
route-map BGP1_IN permit 10
     match ipv6 address prefix-list BGP1_IN
!
router bgp 1
     bgp router-id 8.0.0.1
     network 3dcd:1:1::/64
     neighbor 2001::2 remote-as 2
     neighbor 2001::2 route-map BGP1_IN in
!
vlan 1
    no shutdown
interface 1
    no shutdown
    ipv6 address 2001::1/64

Configuration of BGP2:
----------------------------------------------------------------------------
!
ipv6 prefix-list A_sample_name_to_verify_the_max_length_of_the_prefix_list_\
                 name_that_can_be_confd seq 4294967295 permit any
ipv6 prefix-list p2 seq 5 deny any
!
!
!
route-map BGP2_Rmap2 permit 10
     match ipv6 address prefix-list p2
route-map BGP2_Rmap1 permit 10
     match ipv6 address prefix-list A_sample_name_to_verify_the_max_length_\
                                    of_the_prefix_list_name_that_can_be_confd
!
router bgp 2
     bgp router-id 8.0.0.2
     network 2ccd:1:1::/67
     network 4ddc:1:1::/64
     network 5d5d:1:1::/69
     network 7d5d:1:1::/85
     network 9966:1:2::/85
     neighbor 2001::1 remote-as 1
     neighbor 2001::1 route-map BGP2_Rmap2 in
!
vlan 1
    no shutdown
interface 1
    no shutdown
    ipv6 address 2001::2/64

Expected routes of BGP1:
----------------------------------------------------------------------------
Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
              i internal, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete

Local router-id 8.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 2ccd:1:1::/67    2001::2                  0      0, weight 327682 i
*> 3dcd:1:1::/64    ::                       0      0, weight 32768 i
*> 4ddc:1:1::/64    2001::2                  0      0, weight 327682 i
*> 5d5d:1:1::/69    2001::2                  0      0, weight 327682 i
Total number of entries 4


Expected routes of BGP2:
----------------------------------------------------------------------------
Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
              i internal, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete

Local router-id 8.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 2ccd:1:1::/67    ::                       0      0, weight 32768 i
*> 4ddc:1:1::/64    ::                       0      0, weight 32768 i
*> 5d5d:1:1::/69    ::                       0      0, weight 32768 i
*> 7d5d:1:1::/85    ::                       0      0, weight 32768 i
*> 9966:1:2::/85    ::                       0      0, weight 32768 i
Total number of entries 5

'''
IPv6_ADDR1 = "2001::1"
IPv6_ADDR2 = "2001::2"
DEFAULT_PL = "64"
AS_NUM1 = "1"
AS_NUM2 = "2"
SW1_ROUTER_ID = "8.0.0.1"
SW2_ROUTER_ID = "8.0.0.2"
VTYSH_CR = '\r\n'
ROUTE_MAX_WAIT_TIME = 300

# Topology definition
topoDict = {"topoExecution": 5000,
            "topoType": "physical",
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

def configure_route_map(dut, routemap, prefix_list):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "route-map "+routemap+" permit 10"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter route-map context"
    devIntReturn = dut.DeviceInteract(command="match"\
                                      " ipv6 address prefix-list "+prefix_list)
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

def configure_neighbor(dut, as_num1, network, as_num2):
    if (enterRouterContext(dut, as_num1) is False):
        return False

    cmd = "neighbor "+network+" remote-as "+as_num2
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor config failed"
    return True

def configure_prefix_list(dut, name, seq, action, prefix, ge, le):
    if (enterConfigShell(dut) is False):
        return False

    if ge == 0 and le == 0:
        cmd = "ipv6 prefix-list "+name+" seq "+seq+" "+action+" "+prefix
    elif ge != 0 and le == 0:
        cmd = "ipv6 prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" ge "+\
              str(ge)
    elif ge == 0 and le != 0:
        cmd = "ipv6 prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" le "+\
              str(le)
    elif ge != 0 and le != 0:
        cmd = "ipv6 prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" ge "+\
              str(ge)+" le "+str(le)
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Unable to configure ipv6 prefix"
    return True

def verify_prefix_list_config(dut, name, seq, action, prefix, ge, le):
    if (enterConfigShell(dut) is False):
        return False

    if ge == 0 and le == 0:
        cmd = "ipv6 prefix-list "+name+" seq "+seq+" "+action+" "+prefix
    elif ge != 0 and le == 0:
        cmd = "ipv6 prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" ge "+\
              str(ge)
    elif ge == 0 and le != 0:
        cmd = "ipv6 prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" le "+\
              str(le)
    elif ge != 0 and le != 0:
        cmd = "ipv6 prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" ge "+\
              str(ge)+" le "+str(le)
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 3, "Configured wrong ipv6 prefix list"
    return True

def configure_neighbor_rmap(dut, as_num1, network, as_num2, routemap, direction):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+network+" route-map "+routemap+" in"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor route-map config failed"
    return True


def verify_routes(name, dut, network, next_hop, attempt=1):
    LogOutput('info',"Verifying route on switch %s [attempt #%d] - Network: %s, "
             "Next-Hop: %s " %
             (name, attempt, network, next_hop))

    routes = SwitchVtyshUtils.vtysh_cmd(dut, "show ipv6 bgp")
    routes = routes.split(VTYSH_CR)
    for rte in routes:
        if (network in rte) and (next_hop in rte):
            return True
    return False

def wait_for_route(name, dut, network, next_hop, route_exist):
    for i in range(ROUTE_MAX_WAIT_TIME):
        attempt = i + 1
        found = verify_routes(name, dut, network, next_hop, attempt)
        if found == route_exist:
            if route_exist:
                result = "Route was found"
            else:
                result = "Route was not found"

            LogOutput('info',result)
            return found

        sleep(1)

    LogOutput('info',"Condition not met after %s seconds " %
             ROUTE_MAX_WAIT_TIME)
    return found

def verify_bgp_routes(name,dut, network, next_hop, route_exist):

    found = wait_for_route(name, dut, network, next_hop, route_exist)

    if route_exist == True:
        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, name)
    elif route_exist == False:
        assert not found, "Route %s -> %s does not exist on %s" % \
                          (network, next_hop, name)
def configure(**kwargs):
    '''
     - Configure the IP address in SW1, SW2
     - Configure ipv6 prefix
     - Configure route-map
     - Create router bgp instance on SW1 and SW2
     - Configure the router id
     - Configure the network range
     - Configure the neighbor
     - Apply route-map to neighbor on SW1
    '''

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)


    # Configuring ipv6 prefix-list on switch 1
    LogOutput('info', "Configuring ipv6 prefix configuration on SW1")
    result = configure_prefix_list(switch1, "BGP1_IN", "10", "deny",\
                                   "9966:1:2::/64", 80, 100)
    assert result is True, "Setting ipv6 prefix configuration failed for SW1"
    result = configure_prefix_list(switch1, "BGP1_IN", "20", "permit",\
                                   "7d5d:1:1::/64", 0, 70)
    assert result is True, "Setting ipv6 prefix configuration failed for SW1"
    result = configure_prefix_list(switch1, "BGP1_IN", "30", "permit",\
                                   "5d5d:1:1::/64", 0, 70)
    assert result is True, "Setting ipv6 prefix configuration failed for SW1"
    result = configure_prefix_list(switch1, "BGP1_IN", "40", "permit",\
                                   "2ccd:1:1::/64", 65, 0)
    assert result is True, "Setting ipv6 prefix configuration failed for SW1"
    result = configure_prefix_list(switch1, "BGP1_IN", "50", "permit",\
                                   "4ddc:1:1::/64", 0, 0)
    assert result is True, "Setting ipv6 prefix configuration failed for SW1"

    # Configuring Route-map on switch 1
    LogOutput('info', "Configuring route-map on SW1")
    result = configure_route_map(switch1,"BGP1_IN","BGP1_IN")
    assert result is True, "Setting route-map configuration failed for SW1"

   # Configuring BGP on switch 1
    LogOutput('info', "Configuring router-id on SW1")
    result = configure_router_id(switch1, AS_NUM1, SW1_ROUTER_ID)
    assert result is True, "BGP router id set failed for SW1"

    LogOutput('info', "Configuring networks on SW1")
    result = configure_network(switch1, AS_NUM1, "3dcd:1:1::/64")
    assert result is True, "BGP network creation failed for SW1"

    LogOutput('info', "Configuring bgp neighbor on SW1")
    result = configure_neighbor(switch1, AS_NUM1, IPv6_ADDR2, AS_NUM2)
    assert result is True, "BGP neighbor configuration failed for SW1"
    LogOutput('info', "Applying route-map to bgp neighbor on SW1")
    result = configure_neighbor_rmap(switch1, AS_NUM1, IPv6_ADDR2, AS_NUM2,\
                                     "BGP1_IN","in")
    assert result is True, "BGP neighbor route-map configuration failed for SW1"
    exitContext(switch1)
    sleep(5)

    # Enabling interface 1 SW1.
    LogOutput('info', "Enabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True,
                                interface=switch1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface1 on SW1"

    # Assigning an IPv4 address on interface 1 of SW1
    LogOutput('info', "Configuring IPv6 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=switch1,
                                  interface=switch1.linkPortMapping['lnk01'],
                                  addr=IPv6_ADDR1, mask=DEFAULT_PL,
                                  ipv6flag=True,config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address on interface 1 of SW1"

    # Configuring ipv6 prefix-list on switch 2
    LogOutput('info', "Configuring ipv6 prefix list configuration on SW2")
    result = configure_prefix_list(switch2, "A_sample_name_to_verify_the_"\
                                   "max_length_of_the_prefix_list_name_that_"\
                                   "can_be_confd", "4294967295", "permit",\
                                   "any", 0, 0)
    assert result is True, "Setting ipv6 prefix list configuration failed for SW2"
    LogOutput('info', "Configuring ipv6 prefix list configuration on SW2")
    result = configure_prefix_list(switch2, "p2", "5", "deny",\
                                   "any", 0, 0)
    assert result is True, "Setting ipv6 prefix list configuration failed for SW2"

    # Boundary and limit testing and Negative testing for prefix list
    LogOutput('info', "Boundary and limit testing and Negative testing for"\
              " ipv6 prefix list configuration on SW2")

    result = verify_prefix_list_config(switch2, "p2", "0", "deny",\
                                   "any", 0, 0)
    if result is True:
        LogOutput('info',"Setting wrong ipv6 prefix list configuration"\
                  " failed for SW2")
    assert result is True, "Setting wrong ipv6 prefix list configuration"\
                           " succeeded for SW2"
    result = verify_prefix_list_config(switch2, "p2", "4294967296", "deny",\
                                   "any", 0, 0)
    if result is True:
        LogOutput('info',"Setting wrong ipv6 prefix list configuration"\
                  " failed for SW2")
    assert result is True, "Setting wrong ipv6 prefix list configuration"\
                           " succeeded for SW2"
    result = verify_prefix_list_config(switch2, "p2", "-429", "deny",\
                                   "any", 0, 0)
    if result is True:
        LogOutput('info',"Setting wrong ipv6 prefix list configuration"\
                  " failed for SW2")
    assert result is True, "Setting wrong ipv6 prefix list configuration"\
                           " succeeded for SW2"

    # Configuring Route-map on switch 2
    LogOutput('info', "Configuring route-map on SW2")
    result = configure_route_map(switch2,"BGP2_Rmap1","A_sample_name_to_verify_the_"\
                                   "max_length_of_the_prefix_list_name_that_"\
                                   "can_be_confd")
    assert result is True, "Setting route-map configuration failed for SW2"
    LogOutput('info', "Configuring route-map on SW2")
    result = configure_route_map(switch2,"BGP2_Rmap2","p2")
    assert result is True, "Setting route-map configuration failed for SW2"

    # Configuring BGP on switch 2
    LogOutput('info', "Configuring router-id on SW2")
    result = configure_router_id(switch2, AS_NUM2, SW2_ROUTER_ID)
    assert result is True, "BGP router id set failed for SW2"

    LogOutput('info', "Configuring networks on SW2")
    result = configure_network(switch2, AS_NUM2, "2ccd:1:1::/67")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_network(switch2, AS_NUM2, "7d5d:1:1::/85")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_network(switch2, AS_NUM2, "5d5d:1:1::/69")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_network(switch2, AS_NUM2, "9966:1:2::/85")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_network(switch2, AS_NUM2, "4ddc:1:1::/64")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_neighbor(switch2, AS_NUM2, IPv6_ADDR1, AS_NUM1)
    assert result is True, "BGP neighbor configuration failed for SW1"
    LogOutput('info', "Applying route-map to bgp neighbor on SW2")
    result = configure_neighbor_rmap(switch2, AS_NUM2, IPv6_ADDR1, AS_NUM1,\
                                     "BGP2_Rmap1","out")
    assert result is True, "BGP neighbor route-map configuration failed for SW2"

    LogOutput('info', "Applying route-map to bgp neighbor on SW2")
    result = configure_neighbor_rmap(switch2, AS_NUM2, IPv6_ADDR1, AS_NUM1,\
                                     "BGP2_Rmap2","in")
    assert result is True, "BGP neighbor route-map configuration failed for SW2"
    exitContext(switch2)
    sleep(10)

    # Enabling interface 1 SW2
    LogOutput('info', "Enabling interface1 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on SW2"

    # Assigning an IPv4 address on interface 1 for link 1 SW2
    LogOutput('info', "Configuring IPv6 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk01'],
                                  addr=IPv6_ADDR2, mask=DEFAULT_PL,
                                  ipv6flag=True,config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address on interface 1 of SW2"

@pytest.mark.timeout(600)
class Test_bgp_ipv6_prefix_list_configuration:
    def setup_class(cls):
        Test_bgp_ipv6_prefix_list_configuration.testObj = \
            testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_bgp_ipv6_prefix_list_configuration.topoObj = \
            Test_bgp_ipv6_prefix_list_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_bgp_ipv6_prefix_list_configuration.topoObj.terminate_nodes()

    def test_configure(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        configure(switch1=dut01Obj, switch2=dut02Obj)

        LogOutput('info', "Verifying routes")

        LogOutput('info', "Network 3dcd:1:1::/64 , Next-Hop ::"\
                  " should exist in SW1")
        verify_bgp_routes("SW1", dut01Obj, "3dcd:1:1::/64", "::",\
                          route_exist = True)

        LogOutput('info', "Network 2ccd:1:1::/67 , Next-Hop %s"\
                  " should exist in SW1"%IPv6_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "2ccd:1:1::/67", IPv6_ADDR2,\
                          route_exist = True)


        LogOutput('info', "Network 4ddc:1:1::/64 , Next-Hop  %s"\
                  " should exist in SW1"%IPv6_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "4ddc:1:1::/64", IPv6_ADDR2,\
                          route_exist = True)

        LogOutput('info', "Network 5d5d:1:1::/69 , Next-Hop  %s"\
                  " should exist in SW1"%IPv6_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "5d5d:1:1::/69", IPv6_ADDR2,\
                          route_exist = True)

        LogOutput('info', "Network 9966:1:2::/85 , Next-Hop  %s"\
                  " should not exist in SW1"%IPv6_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "9966:1:2::/85", IPv6_ADDR2,\
                          route_exist = False)

        LogOutput('info', "Network 7d5d:1:1::/85 , Next-Hop  %s"\
                  " should not exist in SW1"%IPv6_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "7d5d:1:1::/85", IPv6_ADDR2,\
                          route_exist = False)


        LogOutput('info', "Network 2ccd:1:1::/67 , Next-Hop ::"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "2ccd:1:1::/67","::",\
                           route_exist = True)

        LogOutput('info', "Network 4ddc:1:1::/64 , Next-Hop ::"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "4ddc:1:1::/64","::",\
                           route_exist = True)

        LogOutput('info', "Network 5d5d:1:1::/69 , Next-Hop ::"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "5d5d:1:1::/69","::",\
                           route_exist = True)

        LogOutput('info', "Network 7d5d:1:1::/85 , Next-Hop ::"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "7d5d:1:1::/85","::",\
                           route_exist = True)

        LogOutput('info', "Network  9966:1:2::/85 , Next-Hop ::"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, " 9966:1:2::/85","::",\
                          route_exist = True)

        LogOutput('info', "Network 3dcd:1:1::/64, Next-Hop %s"\
                  " should not exist in SW2"%IPv6_ADDR1)
        verify_bgp_routes("SW2",dut02Obj,"3dcd:1:1::/64", IPv6_ADDR1,\
                           route_exist = False)
