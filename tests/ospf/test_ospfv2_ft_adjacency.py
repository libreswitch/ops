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
+---------------+             +---------------+
|               |   Area1     |               |
| Switch 1     1+-------------+1  Switch 2    +
|               |             |               |
|               |             |               |
+---------------+             +---------------+

Switch 1 Configuration
IP ADDR is 10.10.10.1
Router Id is 1.1.1.1


Switch 2 Configuration
IP ADDR is 10.10.10.2
Router Id is 2.2.2.2

'''

OSPF1_IF_ADDR = "10.10.10.1"
OSPF2_IF_ADDR = "10.10.10.2"

SW1_ROUTER_ID = "1.1.1.1"
SW2_ROUTER_ID = "2.2.2.2"

OSPF_NETWORK_PL = "24"
OSPF_NETWORK_MASK = "255.255.255.0"

VTYSH_CR = '\r\n'
ADJACENCY_MAX_WAIT_TIME = 50


# Topology definition
topoDict = {"topoExecution": 5000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch"}


def enterConfigShell(dut01):
    retStruct = dut01.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    retStruct = dut01.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    return True


# If the context is not present already then it will be created
def enterRouterContext(dut01):
    if (enterConfigShell(dut01) is False):
        return False

    devIntReturn = dut01.DeviceInteract(command="router ospf")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter OSPF context"

    return True


def enterInterfaceContext(dut01, interface, enable):
    if (enterConfigShell(dut01) is False):
        return False

    cmd = "interface " + str(interface)
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter Interface context"

    if (enable is True):
        dut01.DeviceInteract(command="no shutdown")
        dut01.DeviceInteract(command="no routing")

    return True


def exitContext(dut01):
    devIntReturn = dut01.DeviceInteract(command="exit")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to exit current context"

    retStruct = dut01.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit config terminal"

    retStruct = dut01.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    return True


def deleteRouterInstanceTest(dut01):
    if (enterConfigShell(dut01) is False):
        return False

    devIntReturn = dut01.DeviceInteract(command="no router ospf")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to delete OSPF context failed"

    return True


def configure_router_id(dut, router_id):
    if (enterRouterContext(dut) is False):
        return False

    LogOutput('info', "Configuring OSPF router ID " + router_id)
    devIntReturn = dut.DeviceInteract(command="router-id " + router_id)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set router-id failed"

    return True


def configure_network_area(dut01, network, area):
    if (enterRouterContext(dut01) is False):
        return False

    cmd = "network " + network + " area " + area
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set network area id failed"

    return True


def verify_ospf_adjacency(dut01, dut02_router_id, print_nbrs=False):
        neighbors = SwitchVtyshUtils.vtysh_cmd(dut01, "show ip ospf neighbor")

        if print_nbrs:
            info("%s\n" % neighbors)

        nbrs = neighbors.split(VTYSH_CR)

        for nbr in nbrs:
            if dut02_router_id in nbr:
                return True

        return False


def wait_for_adjacency(dut01, dut02_router_id, condition=True,
                       print_nbrs=False):
        for i in range(ADJACENCY_MAX_WAIT_TIME):
            found = verify_ospf_adjacency(dut01, dut02_router_id, print_nbrs)

            if found == condition:
                if condition:
                    result = "Adjacency formed with " + dut02_router_id
                else:
                    result = "Adjacency not formed with " + dut02_router_id

                LogOutput('info', result)
                return found

            sleep(1)

        info("### Condition not met after %s seconds ###\n" %
             ADJACENCY_MAX_WAIT_TIME)

        return found


def configure(**kwargs):
    '''
     - Configures the IP address in SW1 and SW2
     - Creates router ospf instances
     - Configures the router id
     - Configures the network range and area
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
                                  addr=OSPF1_IF_ADDR, mask=OSPF_NETWORK_PL,
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
                                  addr=OSPF2_IF_ADDR, mask=OSPF_NETWORK_PL,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface 1 of SW2"

    '''
    For all the switches
    - Create the instance.
    - Configure network range and area id.
    - Configure the router Id.
    '''
    result = configure_router_id(switch1, SW1_ROUTER_ID)
    assert result is True, "OSPF router id set failed for SW1"
    LogOutput('info', "Configuring OSPF network for SW1")
    result = configure_network_area(switch1, "10.10.10.0/24", "1")
    assert result is True, "OSPF network creation failed for SW1"
    exitContext(switch1)  # In config context

    result = configure_router_id(switch2, SW2_ROUTER_ID)
    assert result is True, "OSPF router id set failed for SW2"
    LogOutput('info', "Configuring OSPF network for SW2")
    result = configure_network_area(switch2, "10.10.10.0/24", "1")
    assert result is True, "OSPF network creation failed for SW1"
    exitContext(switch2)  # In config context


class Test_ospf_configuration:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_ospf_configuration.testObj = testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_ospf_configuration.topoObj = \
            Test_ospf_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_ospf_configuration.topoObj.terminate_nodes()

    def test_configure(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        configure(switch1=dut01Obj, switch2=dut02Obj)

    def test_nbr_discovery(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")

        configure(switch1=dut01Obj, switch2=dut02Obj)
        LogOutput('info', "Wait for adjacency to form between SW1 and SW2")
        if wait_for_adjacency(dut01Obj, SW2_ROUTER_ID) is True:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % SW2_ROUTER_ID)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                          % SW2_ROUTER_ID

        if wait_for_adjacency(dut02Obj, SW1_ROUTER_ID) is True:
            LogOutput('info', "Adjacency formed in SW2 with SW1 (Router-id %s)"
                      % SW1_ROUTER_ID)

        else:
            assert False, "Adjacency not formed in SW2 with SW1(Router-id %s)"\
                          % SW1_ROUTER_ID
