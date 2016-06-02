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


# This test checks the following commands:
#   * ip prefix-list <prefix-list-name> seq <seq-num> (permit|deny) <prefix>
#              ge <prefix length> le <prefix length>
#
#   * neighbor <neighbor-router-id> route-map <prefix-list> (in|out)
#   * neighbor <neighbor-router-id> prefix-list <prefix-list> (in|out)
#

'''
TOPOLOGY
+---------------+             +---------------+        +--------------+
|               |             |               |        |              |
| Switch 1     1+-------------+1  Switch 2    2+------+1   Switch 3   |
|   BGP1        |             |     BGP2      |        |    BGP3      |
|               |             |               |        |              |
+---------------+             +---------------+        +--------------+

Configuration of BGP1:
----------------------------------------------------------------------------
!
ip prefix-list BGP1_IN seq 5 deny 11.0.0.0/8
ip prefix-list BGP1_IN seq 10 permit 10.0.0.0/8
ip prefix-list BGP1_IN seq 15 permit 150.168.15.0/24 ge 25 le 28
ip prefix-list BGP1_IN seq 20 permit 192.168.15.0/24 ge 27
ip prefix-list BGP1_IN seq 25 deny 192.168.15.0/24 le 25
!
!
!
router bgp 1
     bgp router-id 8.0.0.1
     network 9.0.0.0/8
     neighbor 8.0.0.2 remote-as 2
     neighbor 8.0.0.2 prefix-list BGP1_IN in
!
vlan 1
    no shutdown
interface 1
    no shutdown
    ip address 8.0.0.1/8

Configuration of BGP2:
----------------------------------------------------------------------------
!
ipv6 prefix-list plist_v6 seq 10 permit 2ccd:1:1::/67
ipv6 prefix-list plist_v6 seq 20 deny 4ddc:1:1::/64
ip prefix-list p2 seq 4294967295 permit any
ip prefix-list A_sample_name_to_verify_the_max_length_of_the_prefix_list_name_that_can_be_confd seq 5 deny any
!
!
route-map BGP2_Rmap1 permit 10
     match ip address prefix-list A_sample_name_to_verify_the_max_length_of_the_prefix_list_name_that_can_be_confd
!
router bgp 2
     bgp router-id 8.0.0.2
     network 10.0.0.0/8
     network 11.0.0.0/8
     network 150.168.15.64/26
     network 192.168.15.128/25
     network 192.168.15.16/28
     network 192.168.15.32/27
     neighbor 2001::3 remote-as 3
     neighbor 2001::3 prefix-list plist_v6 in
     neighbor 8.0.0.1 remote-as 1
     neighbor 8.0.0.1 route-map BGP2_Rmap2 in
     neighbor 8.0.0.1 prefix-list p2 out
!
vlan 1
    no shutdown
interface 1
    no shutdown
    ip address 8.0.0.2/8
interface 2
    no shutdown
    ipv6 address 2001::2/64

Configuration of BGP3:
----------------------------------------------------------------------------
!
router bgp 3
     bgp router-id 8.0.0.3
     network 2ccd:1:1::/67
     network 4ddc:1:1::/64
     neighbor 2001::2 remote-as 2
!
vlan 1
    no shutdown
interface 1
    no shutdown
    ipv6 address 2001::3/64


Expected routes of BGP1:
----------------------------------------------------------------------------
#show ip bgp
Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
              i internal, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete

Local router-id 8.0.0.1
   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.0/8       8.0.0.2                  0      0, weight 32768 2 i
*> 150.168.15.64/26 8.0.0.2                  0      0, weight 32768 2 i
*> 192.168.15.16/28 8.0.0.2                  0      0, weight 32768 2 i
*> 192.168.15.32/27 8.0.0.2                  0      0, weight 32768 2 i
*> 9.0.0.0/8        0.0.0.0                  0      0, weight 32768  i
Total number of entries 5


Expected routes of BGP2:
----------------------------------------------------------------------------
#show ip bgp
Local router-id 8.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.0/8       0.0.0.0                  0      0, weight 32768  i
*> 11.0.0.0/8       0.0.0.0                  0      0, weight 32768  i
*> 150.168.15.64/26 0.0.0.0                  0      0, weight 32768  i
*> 192.168.15.128/25 0.0.0.0                  0      0, weight 32768  i
*> 192.168.15.16/28 0.0.0.0                  0      0, weight 32768  i
*> 192.168.15.32/27 0.0.0.0                  0      0, weight 32768  i
Total number of entries 6

#show ipv6 bgp
Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
              i internal, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete

Local router-id 8.0.0.2
   Network          Next Hop            Metric LocPrf Weight Path
*> 2ccd:1:1::/67    2001::3                  0      0, weight 327683 i
Total number of entries 1

Expected routes of BGP3:
----------------------------------------------------------------------------
#show ipv6 bgp
Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
              i internal, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete

Local router-id 8.0.0.3
   Network          Next Hop            Metric LocPrf Weight Path
*> 2ccd:1:1::/67    ::                       0      0, weight 32768 i
*> 4ddc:1:1::/64    ::                       0      0, weight 32768 i
Total number of entries 2

'''

IP_ADDR1 = "8.0.0.1"
IP_ADDR2 = "8.0.0.2"
IPv6_ADDR2 = "2001::2"
IPv6_ADDR3 = "2001::3"
DEFAULT_PL = "8"
DEFAULT_v6PL = "64"
AS_NUM1 = "1"
AS_NUM2 = "2"
AS_NUM3 = "3"
SW1_ROUTER_ID = "8.0.0.1"
SW2_ROUTER_ID = "8.0.0.2"
SW3_ROUTER_ID = "8.0.0.3"
ROUTE_MAX_WAIT_TIME = 300

# Topology definition
topoDict = {"topoExecution": 5000,
            "topoType": "physical",
            "topoTarget": "dut01 dut02 dut03",
            "topoDevices": "dut01 dut02 dut03",
            "topoLinks": "lnk01:dut01:dut02, lnk02:dut02:dut03",
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

def configure_route_map(dut, routemap, prefix_list):
    if (enterConfigShell(dut) is False):
        return False

    cmd = "route-map "+routemap+" permit 10"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter route-map context"
    devIntReturn = dut.DeviceInteract(command="match"\
                                      " ip address prefix-list "+prefix_list)
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
        cmd = "ip prefix-list "+name+" seq "+seq+" "+action+" "+prefix
    elif ge != 0 and le == 0:
        cmd = "ip prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" ge "+\
              str(ge)
    elif ge == 0 and le != 0:
        cmd = "ip prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" le "+\
              str(le)
    elif ge != 0 and le != 0:
        cmd = "ip prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" ge "+\
              str(ge)+" le "+str(le)
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Unable to configure ip prefix list"
    return True

def verify_prefix_list_config(dut, name, seq, action, prefix, ge, le):
    if (enterConfigShell(dut) is False):
        return False

    if ge == 0 and le == 0:
        cmd = "ip prefix-list "+name+" seq "+seq+" "+action+" "+prefix
    elif ge != 0 and le == 0:
        cmd = "ip prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" ge "+\
              str(ge)
    elif ge == 0 and le != 0:
        cmd = "ip prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" le "+\
              str(le)
    elif ge != 0 and le != 0:
        cmd = "ip prefix-list "+name+" seq "+seq+" "+action+" "+prefix+" ge "+\
              str(ge)+" le "+str(le)
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 3, "Configured wrong ipv6 prefix list"
    return True

def configure_ipv6_prefix_list(dut, name, seq, action, prefix, ge, le):
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

def configure_neighbor_rmap(dut, as_num1, network, as_num2, routemap, direction):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+network+" route-map "+routemap+" "+direction
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor route-map config failed"
    return True

def configure_neighbor_prefix_list(dut, as_num1, network, as_num2, plist,\
                                  direction):
    if (enterRouterContext(dut, as_num1) is False):
        return False
    cmd = "neighbor "+network+" prefix-list "+plist+" "+direction
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set neighbor prefix-list config failed"
    return True


def verify_routes(name, dut, network, next_hop, ipv6, attempt=1):
    if (enterConfigShell(dut) is False):
        return False

    if ipv6 is True:
        devIntReturn = dut.DeviceInteract(command="do show ipv6 bgp")
    else:
        devIntReturn = dut.DeviceInteract(command="do show ip bgp")
    routes=  devIntReturn.get('buffer')
    routes = routes.split('\r\n')
    for rte in routes:
        if (network in rte) and (next_hop in rte):
            return True
    return False

def wait_for_route(name, dut, network, next_hop, route_exist, ipv6):
    for i in range(ROUTE_MAX_WAIT_TIME):
        attempt = i + 1
        found = verify_routes(name, dut, network, next_hop, ipv6, attempt)
        if found == route_exist:
            if route_exist:
                result = "Route was found"
            else:
                result = "Route was not found"

            LogOutput('info',result)
            return found

        sleep(1)
        LogOutput('info',"Attempt #%s" %attempt)
    LogOutput('info',"Condition not met after %s seconds " %
             ROUTE_MAX_WAIT_TIME)
    return found

def verify_bgp_routes(name,dut, network, next_hop, route_exist, ipv6):

    found = wait_for_route(name, dut, network, next_hop, route_exist, ipv6)

    if route_exist == True:
        assert found, "Route %s -> %s exists on %s" % \
                      (network, next_hop, name)
    elif route_exist == False:
        assert not found, "Route %s -> %s does not exist on %s" % \
                          (network, next_hop, name)
def configure(**kwargs):
    '''
     - Configure the IP address in SW1, SW2
     - Configure ip prefix list
     - Configure route-map
     - Create router bgp instance on SW1 and SW2
     - Configure the router id
     - Configure the network range
     - Configure the neighbor
     - Apply route-map to neighbor on SW1
    '''

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)
    switch3 = kwargs.get('switch3', None)

    # Configuring ip prefix-list on switch 1
    LogOutput('info', "Configuring ip prefix list configuration on SW1")
    result = configure_prefix_list(switch1, "BGP1_IN", "5", "deny",\
                                   "11.0.0.0/8", 0, 0)
    assert result is True, "Setting ip prefix list configuration failed for SW1"
    result = configure_prefix_list(switch1, "BGP1_IN", "10", "permit",\
                                   "10.0.0.0/8", 0, 0)
    assert result is True, "Setting ip prefix list configuration failed for SW1"
    result = configure_prefix_list(switch1, "BGP1_IN", "15", "permit",\
                                   "150.168.15.0/24", 25, 28)
    assert result is True, "Setting ip prefix list configuration failed for SW1"
    result = configure_prefix_list(switch1, "BGP1_IN", "20", "permit",\
                                   "192.168.15.0/24", 27, 0)
    assert result is True, "Setting ip prefix list configuration failed for SW1"
    result = configure_prefix_list(switch1, "BGP1_IN", "25", "deny",\
                                   "192.168.15.0/24", 0, 25)
    assert result is True, "Setting ip prefix list configuration failed for SW1"

    # Configuring BGP on switch 1
    LogOutput('info', "Configuring router-id on SW1")
    result = configure_router_id(switch1, AS_NUM1, SW1_ROUTER_ID)
    assert result is True, "BGP router id set failed for SW1"

    LogOutput('info', "Configuring networks on SW1")
    result = configure_network(switch1, AS_NUM1, "9.0.0.0/8")
    assert result is True, "BGP network creation failed for SW1"

    LogOutput('info', "Configuring bgp neighbor on SW1")
    result = configure_neighbor(switch1, AS_NUM1, IP_ADDR2, AS_NUM2)
    assert result is True, "BGP neighbor configuration failed for SW1"

    result = configure_neighbor(switch2, AS_NUM2, IPv6_ADDR3, AS_NUM3)
    assert result is True, "BGP neighbor configuration failed for SW2"

    LogOutput('info', "Applying ip prefix-list to bgp neighbor on SW1")
    result = configure_neighbor_prefix_list(switch1, AS_NUM1, IP_ADDR2,\
                                            AS_NUM2,"BGP1_IN","in")
    # Enabling interface 1 on SW1.
    LogOutput('info', "Enabling interface 1 on SW1")
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

    # Configuring ip prefix-list on switch 2
    LogOutput('info', "Configuring ip prefix list configuration on SW2")
    result = configure_prefix_list(switch2, "A_sample_name_to_verify_the_"\
                                   "max_length_of_the_prefix_list_name_that_"\
                                   "can_be_confd", "5", "deny",\
                                   "any", 0, 0)
    assert result is True, "Setting ip prefix list configuration failed for SW2"
    LogOutput('info', "Configuring ip prefix list configuration on SW2")
    result = configure_prefix_list(switch2, "p2", "4294967295", "permit",\
                                   "any", 0, 0)
    assert result is True, "Setting ip prefix list configuration failed for SW2"


    # Conifigure ipv6 prefix list on switch 2
    LogOutput('info', "Configuring ipv6 prefix list configuration on SW2")
    result = configure_ipv6_prefix_list(switch2, "plist_v6", "10", "permit",\
                                   "2ccd:1:1::/67", 0, 0)
    assert result is True, "Setting ipv6 prefix list configuration failed for SW2"
    LogOutput('info', "Configuring ipv6 prefix list configuration on SW2")
    result = configure_ipv6_prefix_list(switch2, "plist_v6", "20", "deny",\
                                   "4ddc:1:1::/64", 0, 0)
    assert result is True, "Setting ipv6 prefix list configuration failed for SW2"

    # Boundary and limit testing and Negative testing for ip prefix list
    LogOutput('info', "Boundary and limit testing and Negative testing for"\
              " ip prefix list configuration on SW2")

    result = verify_prefix_list_config(switch2, "p2", "0", "deny",\
                                   "any", 0, 0)
    if result is True:
        LogOutput('info',"Setting wrong ip prefix list configuration"\
                  " failed for SW2")
    assert result is True, "Setting wrong ip prefix list configuration"\
                           " succeeded for SW2"
    result = verify_prefix_list_config(switch2, "p2", "4294967296", "deny",\
                                   "any", 0, 0)
    if result is True:
        LogOutput('info',"Setting wrong ip prefix list configuration"\
                  " failed for SW2")
    assert result is True, "Setting wrong ip prefix list configuration"\
                           " succeeded for SW2"

    result = verify_prefix_list_config(switch2, "p2", "-429", "deny",\
                                   "any", 0, 0)
    if result is True:
        LogOutput('info',"Setting wrong ip prefix list configuration"\
                  " failed for SW2")
    assert result is True, "Setting wrong ip prefix list configuration"\
                           " succeeded for SW2"
    # Configuring Route-map on switch 2
    LogOutput('info', "Configuring route-map on SW2")
    result = configure_route_map(switch2,"BGP2_Rmap1","A_sample_name_to_verify_the_"\
                                   "max_length_of_the_prefix_list_name_that_"\
                                   "can_be_confd")
    assert result is True, "Setting route-map configuration failed for SW2"

    # Configuring BGP on switch 2
    LogOutput('info', "Configuring router-id on SW2")
    result = configure_router_id(switch2, AS_NUM2, SW2_ROUTER_ID)
    assert result is True, "BGP router id set failed for SW2"

    LogOutput('info', "Configuring networks on SW2")
    result = configure_network(switch2, AS_NUM2, "10.0.0.0/8")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_network(switch2, AS_NUM2, "11.0.0.0/8")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_network(switch2, AS_NUM2, "150.168.15.64/26")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_network(switch2, AS_NUM2, "192.168.15.128/25")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_network(switch2, AS_NUM2, "192.168.15.16/28")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_network(switch2, AS_NUM2, "192.168.15.32/27")
    assert result is True, "BGP network creation failed for SW2"
    result = configure_neighbor(switch2, AS_NUM2, IP_ADDR1, AS_NUM1)
    assert result is True, "BGP neighbor configuration failed for SW2"

    LogOutput('info', "Applying ipv6 prefix-list to bgp neighbor on SW2")
    result = configure_neighbor_prefix_list(switch2, AS_NUM2, IPv6_ADDR3,\
                                            AS_NUM3,"plist_v6","in")

    LogOutput('info', "Applying ipv6 prefix-list to bgp neighbor on SW2")
    result = configure_neighbor_prefix_list(switch2, AS_NUM2, IPv6_ADDR3,\
                                            AS_NUM3,"plist_v6","in")

    LogOutput('info', "Applying route-map to bgp neighbor on SW2")
    result = configure_neighbor_rmap(switch2, AS_NUM2, IP_ADDR1, AS_NUM1,\
                                     "BGP2_Rmap1","in")
    assert result is True, "BGP neighbor route-map configuration failed for SW2"


    LogOutput('info', "Applying ip prefix-list to bgp neighbor on SW2")
    result = configure_neighbor_prefix_list(switch2, AS_NUM2, IP_ADDR1,\
                                            AS_NUM1,"p2","out")

   # Enabling interface 1 on SW2
    LogOutput('info', "Enabling interface 1 on SW2")
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

    # Enabling interface 2 on SW2
    LogOutput('info', "Enabling interface 2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True,
                                interface=switch2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 2 on SW2"

    # Assigning an IPv6 address on interface 1 for link 2 SW2
    LogOutput('info', "Configuring IPv6 address on link 2 SW2")
    retStruct = InterfaceIpConfig(deviceObj=switch2,
                                  interface=switch2.linkPortMapping['lnk02'],
                                  addr=IPv6_ADDR2, mask=DEFAULT_v6PL,
                                  ipv6flag=True,config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address on interface 2 of SW2"

    # Configuring BGP on switch 3
    LogOutput('info', "Configuring router-id on SW3")
    result = configure_router_id(switch3, AS_NUM3, SW3_ROUTER_ID)
    assert result is True, "BGP router id set failed for SW3"

    LogOutput('info', "Configuring networks on SW3")
    result = configure_network(switch3, AS_NUM3, "2ccd:1:1::/67")
    assert result is True, "BGP network creation failed for SW3"
    result = configure_network(switch3, AS_NUM3, "4ddc:1:1::/64")
    assert result is True, "BGP network creation failed for SW3"

    result = configure_neighbor(switch3, AS_NUM3, IPv6_ADDR2, AS_NUM2)
    assert result is True, "BGP neighbor configuration failed for SW3"
    exitContext(switch3)

    # Enabling interface 1 on SW3
    LogOutput('info', "Enabling interface 1 on SW3")
    retStruct = InterfaceEnable(deviceObj=switch3, enable=True,
                                interface=switch3.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface 1 on SW3"

    # Assigning an IPv6 address on interface 1 for link 2 SW3
    LogOutput('info', "Configuring IPv6 address on link 2 SW3")
    retStruct = InterfaceIpConfig(deviceObj=switch3,
                                  interface=switch3.linkPortMapping['lnk02'],
                                  addr=IPv6_ADDR3, mask=DEFAULT_v6PL,
                                  ipv6flag=True,config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address on interface 1 of SW3"

@pytest.mark.timeout(600)
class Test_bgp_ip_prefix_list_configuration:
    def setup_class(cls):
        Test_bgp_ip_prefix_list_configuration.testObj = \
            testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_bgp_ip_prefix_list_configuration.topoObj = \
            Test_bgp_ip_prefix_list_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_bgp_ip_prefix_list_configuration.topoObj.terminate_nodes()

    def test_configure(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        configure(switch1=dut01Obj, switch2=dut02Obj, switch3=dut03Obj)

        LogOutput('info', "Verifying routes")

        LogOutput('info', "Network 9.0.0.0/8 , Next-Hop 0.0.0.0"\
                  " should exist in SW1")
        verify_bgp_routes("SW1", dut01Obj, "9.0.0.0", "0.0.0.0",\
                          route_exist = True, ipv6 = False)

        LogOutput('info', "Network 10.0.0.0/8 , Next-Hop %s"\
                  " should exist in SW1"%IP_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "10.0.0.0/8", IP_ADDR2,\
                          route_exist = True, ipv6 = False)

        LogOutput('info', "Network 150.168.15.64/26 , Next-Hop %s"\
                  " should exist in SW1"%IP_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "150.168.15.64/26", IP_ADDR2,\
                          route_exist = True, ipv6 = False)

        LogOutput('info', "Network 192.168.15.16/28 , Next-Hop  %s"\
                  " should exist in SW1"%IP_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "192.168.15.16/28", IP_ADDR2,\
                          route_exist = True, ipv6 = False)

        LogOutput('info', "Network 192.168.15.32/27 , Next-Hop  %s"\
                  " should exist in SW1"%IP_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "192.168.15.32/27", IP_ADDR2,\
                          route_exist = True, ipv6 = False)

        LogOutput('info', "Network 192.168.15.128/25 , Next-Hop  %s"\
                  " should not exist in SW1"%IP_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "192.168.15.128/25", IP_ADDR2,\
                          route_exist = False, ipv6 = False)

        LogOutput('info', "Network 11.0.0.0/8 , Next-Hop  %s"\
                  " should not exist in SW1"%IP_ADDR2)
        verify_bgp_routes("SW1", dut01Obj, "11.0.0.0/8", IP_ADDR2,\
                           route_exist = False, ipv6 = False)

        LogOutput('info', "Network 10.0.0.0/8 , Next-Hop 0.0.0.0"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "10.0.0.0/8","0.0.0.0",\
                           route_exist = True, ipv6 = False)

        LogOutput('info', "Network 11.0.0.0/8 , Next-Hop 0.0.0.0"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "11.0.0.0/8","0.0.0.0",\
                           route_exist = True, ipv6 = False)

        LogOutput('info', "Network 150.168.15.64/26 , Next-Hop 0.0.0.0"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "150.168.15.64/26","0.0.0.0",\
                           route_exist = True, ipv6 = False)

        LogOutput('info', "Network 192.168.15.128/25 , Next-Hop 0.0.0.0"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "192.168.15.128/25","0.0.0.0",\
                           route_exist = True, ipv6 = False)

        LogOutput('info', "Network 192.168.15.16/28 , Next-Hop 0.0.0.0"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "192.168.15.16/28","0.0.0.0",\
                          route_exist = True, ipv6 = False)

        LogOutput('info', "Network 192.168.15.32/27 , Next-Hop 0.0.0.0"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "192.168.15.32/27","0.0.0.0",\
                          route_exist = True, ipv6 = False)

        LogOutput('info', "Network 9.0.0.0 , Next-Hop %s"\
                  " should not exist in SW2"%IP_ADDR1)
        verify_bgp_routes("SW2",dut02Obj,"9.0.0.0", IP_ADDR1,\
                           route_exist = False, ipv6 = False)

        LogOutput('info', "Network  2ccd:1:1::/67 , Next-Hop 2001::3"\
                  " should exist in SW2")
        verify_bgp_routes("SW2", dut02Obj, "2ccd:1:1::/67","2001::3",\
                          route_exist = True, ipv6 = True)

        LogOutput('info', "Network 4ddc:1:1::/64 , Next-Hop 2001::3"\
                  " should not exist in SW2")
        verify_bgp_routes("SW2",dut02Obj,"4ddc:1:1::/64", "2001::3",\
                           route_exist = False, ipv6 = True)
