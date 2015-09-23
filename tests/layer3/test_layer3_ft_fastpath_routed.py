"""#!/usr/bin/env python

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

#import lib
import pytest
import re
from  opstestfw import *
from opstestfw.switch.CLI import *
#import switch
#from lib import *
#from opstestfw.switch.CLI.lldp import *
#from opstestfw.switch.CLI.interface import *
from opstestfw.switch.CLI import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:dut02,lnk03:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch,dut02:system-category:switch,wrkston01:system-category:workstation,wrkston02:system-category:workstation"}

def fastpath_ping(**kwargs):
    device1 = kwargs.get('device1',None)
    device2 = kwargs.get('device2',None)
    device3 = kwargs.get('device3',None)
    device4 = kwargs.get('device4',None)
    caseReturnCode = 0



    #TEST_DESCRIPTION = "Virtual Topology / Physical Topology Sample Test"
    #tcInstance.tcInfo(tcName = ResultsDirectory['testcaseName'], tcDesc = TEST_DESCRIPTION)

    #Enabling interface 1 SW1
    LogOutput('info', "Enabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW1"
       caseReturnCode = 1


    #Entering interface for link 1 SW1, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=device1, interface=device1.linkPortMapping['lnk01'], addr="10.0.10.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=device1, interface=device1.linkPortMapping['lnk01'], addr="2000::2", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1





    #Enabling interface 2 SW1
    LogOutput('info', "Enabling interface2 on SW1")
    retStruct = InterfaceEnable(deviceObj=device1, enable=True, interface=device1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW1"
       caseReturnCode = 1

    #Entering interface 2 SW1, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=device1, interface=device1.linkPortMapping['lnk02'], addr="10.0.20.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=device1, interface=device1.linkPortMapping['lnk02'], addr="2001::1", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1


    #Enabling interface 1 SW2
    LogOutput('info', "Enabling interface1 on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW2"
       caseReturnCode = 1


    #Entering interface for link 3 SW2, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=device2, interface=device2.linkPortMapping['lnk03'], addr="10.0.30.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=device2, interface=device2.linkPortMapping['lnk03'], addr="2002::2", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1

    #Enabling interface 2 SW2
    LogOutput('info', "Enabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=device2, enable=True, interface=device2.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW2"
       caseReturnCode = 1


    #Entering interface for link 2 SW2, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=device2, interface=device2.linkPortMapping['lnk02'], addr="10.0.20.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=device2, interface=device2.linkPortMapping['lnk02'], addr="2001::2", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1


    #Configure host 1

    LogOutput('info',"\n\n\nConfiguring host 1 ipv4")
    retStruct = device3.NetworkConfig(ipAddr="10.0.10.1", netMask="255.255.255.0", interface=device3.linkPortMapping['lnk01'], broadcast="10.0.10.0", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    LogOutput('info',"\n\n\nConfiguring host 1 ipv6")
    retStruct = device3.Network6Config(ipAddr="2000::1", netMask=120, interface=device3.linkPortMapping['lnk01'], broadcast="2000::0", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1



    #Configure host 2

    LogOutput('info',"\n\n\nConfiguring host 2 ipv4")
    retStruct = device4.NetworkConfig(ipAddr="10.0.30.1", netMask="255.255.255.0", interface=device4.linkPortMapping['lnk03'], broadcast="10.0.30.0", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    LogOutput('info',"\n\n\nConfiguring host 2 ipv6")
    retStruct = device4.Network6Config(ipAddr="2002::1", netMask=120, interface=device4.linkPortMapping['lnk03'],broadcast="2002::0",  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1

    #Configuring static routes on switches


    LogOutput('info',"\n\n\n######### Configuring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=device1, route="10.0.30.0", mask=24, nexthop="10.0.20.2", config=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nConfiguring switch 1 and 2 routes")
    retStruct = IpRouteConfig(deviceObj=device2, route="10.0.10.0", mask=24, nexthop="10.0.20.1", config=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=device1, route="2002::", mask=120, nexthop="2001::2", config=True, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    retStruct = IpRouteConfig(deviceObj=device2, route="2000::", mask=120, nexthop="2001::1", config=True, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    #Configuring static routes on hosts
    LogOutput('info', "Configuring routes on the workstations")
    retStruct = device3.IPRoutesConfig(config=True, destNetwork="10.0.20.0", netMask=24, gateway="10.0.10.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = device3.IPRoutesConfig(config=True, destNetwork="10.0.30.0", netMask=24, gateway="10.0.10.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = device4.IPRoutesConfig(config=True, destNetwork="10.0.10.0", netMask=24, gateway="10.0.30.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = device4.IPRoutesConfig(config=True, destNetwork="10.0.20.0", netMask=24, gateway="10.0.30.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1



    # Add V6 default gateway on hosts h1 and h2

    retStruct = device3.IPRoutesConfig(config=True, destNetwork="2001::0", netMask=120, gateway="2000::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    retStruct = device3.IPRoutesConfig(config=True, destNetwork="2002::0", netMask=120, gateway="2000::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    retStruct = device4.IPRoutesConfig(config=True, destNetwork="2000::0", netMask=120, gateway="2002::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    retStruct = device4.IPRoutesConfig(config=True, destNetwork="2001::0", netMask=120, gateway="2002::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1



    LogOutput('info',"\n\n\nPing after adding static route to S1 and S2")

    LogOutput('info',"\n\n\n Pinging host 1 to host 2 using IPv4")
    retStruct = device3.Ping(ipAddr="10.0.30.1", packetCount=1)
    Sleep(seconds=7, message="")
    #print devIntRetStruct
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv4 ping #####")
    else:
        LogOutput('info', "IPv4 Ping from host 1 to host 2 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed #####\n\n")

    LogOutput('info',"\n Pinging host 1 to host 2 using IPv6")
    retStruct = device3.Ping(ipAddr="2002::1", packetCount=1, ipv6Flag=True)
    Sleep(seconds=7, message="")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv6 ping #####")
    else:
        LogOutput('info', "IPv4 Ping from host 1 to host 2 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed #####\n\n")




    LogOutput('info',"\n\n\n Pinging host 2 to host 1 using IPv4")
    retStruct = device4.Ping(ipAddr="10.0.10.1", packetCount=1)
    Sleep(seconds=7, message="")
    #print devIntRetStruct
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv4 ping #####")
    else:
        LogOutput('info', "IPv4 Ping from host  2 to host 1 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed #####\n\n")

    LogOutput('info',"\n Pinging host 2 to host 1 using IPv6")
    retStruct = device4.Ping(ipAddr="2000::1", packetCount=1, ipv6Flag=True)
    Sleep(seconds=7, message="")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv6 ping #####")
    else:
        LogOutput('info', "IPv4 Ping from host 2 to host 1 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed #####\n\n")


    #Verifying Hit bit in ASIC for IPv4 ping
    LogOutput('info', "\Verifying HIT Bit for IPv4 ping")
    appctl_command = "ovs-appctl plugin/debug l3route"

    # check device1
    retStruct = device1.DeviceInteract(command=appctl_command)
    retCode = retStruct['returnCode']
    if retCode:
        LogOutput('error', "couldn't get l3route debug");
    else:
        table = retStruct['buffer']
        rows = table.split('\n')
        routerow = None
        for row in rows:
            if '10.0.30.0' in row:
                routerow = row

        if routerow == None:
            LogOutput('error', "route not programmed in ASIC on device1")
        else:
            columns = routerow.split()
            routehit = columns[5]
            if routehit != 'Y':
                LogOutput('error', "route not selected in ASIC on device1")

    # check device2
    returnStruct = device2.DeviceInteract(command=appctl_command)
    retCode = retStruct['returnCode']
    if retCode:
        LogOutput('error', "couldn't get l3route debug");
    else:
        table = retStruct['buffer']
        rows = table.split('\n')
        routerow = None
        for row in rows:
            if '10.0.10.0' in row:
                routerow = row

        if routerow == None:
            LogOutput('error', "route not programmed in ASIC on device2")
        else:
            columns = routerow.split()
            routehit = columns[5]
            if routehit != 'Y':
                LogOutput('error', "route not selected in ASIC on device2")


    #Remove IPv4 and IPv6 static route on s1
    LogOutput('info',"\n\n\n######## Removing static Routes on s1 and s2 #########")
    retStruct = IpRouteConfig(deviceObj=device1, route="10.0.30.0", mask=24, nexthop="10.0.20.2", config=False)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv4 address route")
        caseReturnCode = 1

    retStruct = IpRouteConfig(deviceObj=device2, route="10.0.10.0", mask=24, nexthop="10.0.20.1", config=False)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv4 address route")
        caseReturnCode = 1

    retStruct = IpRouteConfig(deviceObj=device1, route="2002::", mask=120, nexthop="2001::2", config=False, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv6 address route")
        caseReturnCode = 1

    retStruct = IpRouteConfig(deviceObj=device2, route="2000::", mask=120, nexthop="2001::1", config=False, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv6 address route")
        caseReturnCode = 1





    LogOutput('info',"\n\n\n\n\nPing after removing static route from S1 and S2")
    LogOutput('info',"\n\n\n Pinging host 1 to host 2 using IPv4")
    retStruct = device3.Ping(ipAddr="10.0.30.1", packetCount=1)
    Sleep(seconds=7, message="")
    #print devIntRetStruct
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv4 ping #####")
    else:
        LogOutput('info', "IPv4 Ping from host 1 to host 2 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed #####\n\n")

    LogOutput('info',"\n Pinging host 1 to host 2 using IPv6")
    retStruct = device3.Ping(ipAddr="2002::1", packetCount=1, ipv6Flag=True)
    Sleep(seconds=7, message="")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv6 ping #####")
    else:
        LogOutput('info', "IPv4 Ping from host 1 to host 2 return JSON:\n")
        retStruct.printValueString()

        LogOutput('info',"\n##### Ping Passed #####\n\n")




    LogOutput('info',"\n\n\n Pinging host 2 to host 1 using IPv4")
    retStruct = device4.Ping(ipAddr="10.0.10.1", packetCount=1)
    Sleep(seconds=7, message="")
    #print devIntRetStruct
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv4 ping #####")
    else:
        LogOutput('info', "IPv4 Ping from host 2 to host 1 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed ######\n\n")

    LogOutput('info',"\n Pinging host 2 to host 1 using IPv6")
    retStruct = device4.Ping(ipAddr="2000::1", packetCount=1, ipv6Flag=True)
    Sleep(seconds=7, message="")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv6 ping ######")

    else:
        LogOutput('info', "IPv4 Ping from host 2 to host 1 return JSON:\n")
        retStruct.printValueString()

        LogOutput('info',"\n##### Ping Passed #####\n\n")



class Test_fastpath_ping:
    def setup_class (cls):
	# Test object will parse command line and formulate the env
	Test_fastpath_ping.testObj = testEnviron(topoDict=topoDict)
	# Get topology object
	Test_fastpath_ping.topoObj = Test_fastpath_ping.testObj.topoObjGet()

    def teardown_class (cls):
        Test_fastpath_ping.topoObj.terminate_nodes()
    def test_fastpath_ping(self):
	# GEt Device objects
	dut01Obj = self.topoObj.deviceObjGet(device="dut01")
	dut02Obj = self.topoObj.deviceObjGet(device="dut02")
	wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
	wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
	retValue = fastpath_ping(device1=dut01Obj, device2=dut02Obj, device3=wrkston01Obj, device4=wrkston02Obj)
	if retValue != 0:
            assert "Test failed"
	else:
	    LogOutput('info', "test passed\n\n\n\n############################# Next Test #########################\n")"""
