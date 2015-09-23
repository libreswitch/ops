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

import lib
import pytest
import re
import switch
from lib import *
from switch.CLI.lldp import *
from switch.CLI.interface import *
from switch.CLI import *

# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02 dut03 dut04",
            "topoDevices": "dut01 dut02 wrkston01 wrkston02 wrkston03",
            "topoLinks": "lnk01:dut01:dut02,lnk02:dut01:wrkston01,lnk03:dut01:wrkston02,lnk04:dut02:wrkston03,lnk05:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,dut02:system-category:switch,wrkston01:system-category:workstation,wrkston02:system-category:workstation,wrkston03:system-category:workstation"}

def ecmp_ping(**kwargs):
    switch1 = kwargs.get('switch1',None)
    switch2 = kwargs.get('switch2',None)
    host1 = kwargs.get('host1',None)
    host2 = kwargs.get('host2',None)
    host3 = kwargs.get('host3',None)
    caseReturnCode = 0

    #systemctl stop zebra
    #/usr/sbin/zebra --detach --pidfile -vSYSLOG:DBG

    #Enabling interface 1 SW1
    LogOutput('info', "Enabling interface1 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True, interface=switch1.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW1"
       caseReturnCode = 1

    #Enabling interface 2 SW1
    LogOutput('info', "Enabling interface2 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True, interface=switch1.linkPortMapping['lnk02'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW1"
       caseReturnCode = 1

    #Enabling interface 3 SW1
    LogOutput('info', "Enabling interface3 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True, interface=switch1.linkPortMapping['lnk03'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW1"
       caseReturnCode = 1

    #Enabling interface 1 SW2
    LogOutput('info', "Enabling interface1 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True, interface=switch2.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW2"
       caseReturnCode = 1

    #Enabling interface 2 SW2
    LogOutput('info', "Enabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True, interface=switch2.linkPortMapping['lnk04'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW1"
       caseReturnCode = 1

    #Enabling interface 4 SW1
    LogOutput('info', "Enabling interface4 on SW1")
    retStruct = InterfaceEnable(deviceObj=switch1, enable=True, interface=switch1.linkPortMapping['lnk05'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW1"
       caseReturnCode = 1

    #Enabling interface 3 SW2
    LogOutput('info', "Enabling interface2 on SW2")
    retStruct = InterfaceEnable(deviceObj=switch2, enable=True, interface=switch2.linkPortMapping['lnk05'])
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Unable to enable interafce on SW1"
       caseReturnCode = 1


    #Entering interface for link 1 SW1, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=switch1, interface=switch1.linkPortMapping['lnk01'], addr="10.0.30.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=switch1, interface=switch1.linkPortMapping['lnk01'], addr="1030::1", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1

    #Entering interface for link 2 SW1, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=switch1, interface=switch1.linkPortMapping['lnk02'], addr="10.0.10.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=switch1, interface=switch1.linkPortMapping['lnk02'], addr="1010::2", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1

    #Entering interface for link 3 SW1, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=switch1, interface=switch1.linkPortMapping['lnk03'], addr="10.0.20.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=switch1, interface=switch1.linkPortMapping['lnk03'], addr="1020::2", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1

    #Entering interface for link 1 SW2, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=switch2, interface=switch2.linkPortMapping['lnk01'], addr="10.0.30.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=switch2, interface=switch2.linkPortMapping['lnk01'], addr="1030::2", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1

    #Entering interface for link 4 SW2, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=switch2, interface=switch2.linkPortMapping['lnk04'], addr="10.0.40.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=switch2, interface=switch2.linkPortMapping['lnk04'], addr="1040::2", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1

    #Entering interface for link 5 SW1, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=switch1, interface=switch1.linkPortMapping['lnk05'], addr="10.0.50.1", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=switch1, interface=switch1.linkPortMapping['lnk05'], addr="1050::1", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1

    #Entering interface for link 5 SW2, giving an ip address
    retStruct = InterfaceIpConfig(deviceObj=switch2, interface=switch2.linkPortMapping['lnk05'], addr="10.0.50.2", mask=24, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    retStruct = InterfaceIpConfig(deviceObj=switch2, interface=switch2.linkPortMapping['lnk05'], addr="1050::2", mask=120, ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"
       caseReturnCode = 1



    LogOutput('info',"\n\n\n######### Configuring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch1, route="10.0.40.0", mask=24, nexthop="10.0.30.2", config=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch1, route="1040::0", mask=120, nexthop="1030::2", config=True, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\n######### Configuring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.10.0", mask=24, nexthop="10.0.30.1", config=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch2, route="1010::0", mask=120, nexthop="1030::1", config=True, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\n######### Configuring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.20.0", mask=24, nexthop="10.0.30.1", config=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch2, route="1020::0", mask=120, nexthop="1030::1", config=True, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1




    LogOutput('info',"\n\n\n######### Configuring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch1, route="10.0.40.0", mask=24, nexthop="10.0.50.2", config=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch1, route="1040::", mask=120, nexthop="1050::2", config=True, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\n######### Configuring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.10.0", mask=24, nexthop="10.0.50.1", config=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch2, route="1010::", mask=120, nexthop="1050::1", config=True, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\n######### Configuring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.20.0", mask=24, nexthop="10.0.50.1", config=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch2, route="1020::", mask=120, nexthop="1050::1", config=True, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    #Configure host 1

    LogOutput('info',"\n\n\nConfiguring host 1 ipv4")
    retStruct = host1.NetworkConfig(ipAddr="10.0.10.1", netMask="255.255.255.0", interface=host1.linkPortMapping['lnk02'], broadcast="10.0.10.0", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    LogOutput('info',"\n\n\nConfiguring host 1 ipv6")
    retStruct = host1.Network6Config(ipAddr="1010::1", netMask=120, interface=host1.linkPortMapping['lnk02'], broadcast="1010::0", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1



    #Configure host 2

    LogOutput('info',"\n\n\nConfiguring host 2 ipv4")
    retStruct = host2.NetworkConfig(ipAddr="10.0.20.1", netMask="255.255.255.0", interface=host2.linkPortMapping['lnk03'], broadcast="10.0.20.0", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    LogOutput('info',"\n\n\nConfiguring host 2 ipv6")
    retStruct = host2.Network6Config(ipAddr="1020::1", netMask=120, interface=host2.linkPortMapping['lnk03'],broadcast="1020::0",  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"


    #Configure host 3

    LogOutput('info',"\n\n\nConfiguring host 3 ipv4")
    retStruct = host3.NetworkConfig(ipAddr="10.0.40.1", netMask="255.255.255.0", interface=host3.linkPortMapping['lnk04'], broadcast="10.0.40.0", config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv4 address"
       caseReturnCode = 1

    LogOutput('info',"\n\n\nConfiguring host 3 ipv6")
    retStruct = host3.Network6Config(ipAddr="1040::1", netMask=120, interface=host3.linkPortMapping['lnk04'],broadcast="1040::0",  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
       assert "Failed to configure an ipv6 address"


    #Configuring static routes on hosts
    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host1.IPRoutesConfig(config=True, destNetwork="10.0.30.0", netMask=24, gateway="10.0.10.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host1.IPRoutesConfig(config=True, destNetwork="1030::0", netMask=120, gateway="1010::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host1.IPRoutesConfig(config=True, destNetwork="10.0.40.0", netMask=24, gateway="10.0.10.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host1.IPRoutesConfig(config=True, destNetwork="1040::0", netMask=120, gateway="1010::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1


    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host2.IPRoutesConfig(config=True, destNetwork="10.0.30.0", netMask=24, gateway="10.0.20.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host2.IPRoutesConfig(config=True, destNetwork="1030::0", netMask=120, gateway="1020::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host2.IPRoutesConfig(config=True, destNetwork="10.0.40.0", netMask=24, gateway="10.0.20.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host2.IPRoutesConfig(config=True, destNetwork="1040::0", netMask=120, gateway="1020::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host3.IPRoutesConfig(config=True, destNetwork="10.0.30.0", netMask=24, gateway="10.0.40.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host3.IPRoutesConfig(config=True, destNetwork="1030::0", netMask=120, gateway="1040::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host1.IPRoutesConfig(config=True, destNetwork="10.0.50.0", netMask=24, gateway="10.0.10.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host1.IPRoutesConfig(config=True, destNetwork="1050::0", netMask=120, gateway="1010::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host2.IPRoutesConfig(config=True, destNetwork="10.0.50.0", netMask=24, gateway="10.0.20.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host2.IPRoutesConfig(config=True, destNetwork="1050::0", netMask=120, gateway="1020::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host3.IPRoutesConfig(config=True, destNetwork="10.0.50.0", netMask=24, gateway="10.0.40.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host3.IPRoutesConfig(config=True, destNetwork="1050::0", netMask=120, gateway="1040::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host3.IPRoutesConfig(config=True, destNetwork="10.0.10.0", netMask=24, gateway="10.0.40.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host3.IPRoutesConfig(config=True, destNetwork="1010::0", netMask=120, gateway="1040::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info', "Configuring routes on the workstations")
    retStruct = host3.IPRoutesConfig(config=True, destNetwork="10.0.20.0", netMask=24, gateway="10.0.40.2")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv4 address route")
        caseReturnCode = 1

    retStruct = host3.IPRoutesConfig(config=True, destNetwork="1020::0", netMask=120, gateway="1040::2", ipv6Flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to configure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info',"\n\n\nPing after adding static route to S1 and S2")

    LogOutput('info',"\n\n\n Pinging host 1 to host 3 using IPv4")
    retStruct = host1.Ping(ipAddr="10.0.40.1", packetCount=1)
    Sleep(seconds=7, message="")
    #print devIntRetStruct
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv4 ping,Case Failed #####")
    else:
        LogOutput('info', "IPv4 Ping from host 1 to host 3 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed,Case Passed #####\n\n")

    LogOutput('info',"\n Pinging host 1 to host 3 using IPv6")
    retStruct = host1.Ping(ipAddr="1040::1", packetCount=1, ipv6Flag=True)
    Sleep(seconds=7, message="")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv6 ping,Case Failed #####")
    else:
        LogOutput('info', "IPv6 Ping from host 1 to host 3 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed, Case Passed #####\n\n")

    LogOutput('info',"\n\n\n Pinging host 2 to host 3 using IPv4")
    retStruct = host2.Ping(ipAddr="10.0.40.1", packetCount=1)
    Sleep(seconds=7, message="")
    #print devIntRetStruct
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv4 ping, Case Failed #####")
    else:
        LogOutput('info', "IPv4 Ping from host 2 to host 3 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed, Case Passed #####\n\n")

    LogOutput('info',"\n Pinging host 2 to host 3 using IPv6")
    retStruct = host2.Ping(ipAddr="1040::1", packetCount=1, ipv6Flag=True)
    Sleep(seconds=7, message="")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv6 ping, Case Failed #####")
    else:
        LogOutput('info', "IPv6 Ping from host 2 to host 3 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed, Case Passed #####\n\n")



    LogOutput('info',"\n\n\n######### Unconfiguring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch1, route="10.0.40.0", mask=24, nexthop="10.0.30.2", config=False)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nunConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch1, route="1040::", mask=120, nexthop="1030::2", config=False, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv6 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\n######### unConfiguring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.10.0", mask=24, nexthop="10.0.30.1", config=False)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nunconfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch2, route="1010::", mask=120, nexthop="1030::1", config=False, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv6 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\n######### unconfiguring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.20.0", mask=24, nexthop="10.0.30.1", config=False)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nunConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch2, route="1020::", mask=120, nexthop="1030::1", config=False, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv6 address route")
        caseReturnCode = 1




    #LogOutput('info',"\n\n\n######### UnConfiguring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch1, route="10.0.40.0", mask=24, nexthop="10.0.50.2", config=False)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nUnConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch1, route="1040::", mask=120, nexthop="1050::2", config=False, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv6 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\n######### UnConfiguring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.10.0", mask=24, nexthop="10.0.50.1", config=False)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nUnConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch2, route="1010::", mask=120, nexthop="1050::1", config=False, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv6 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\n######### UnConfiguring switch 1 and 2 static routes #########")
    retStruct = IpRouteConfig(deviceObj=switch2, route="10.0.20.0", mask=24, nexthop="10.0.50.1", config=False)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv4 address route")
        caseReturnCode = 1

    #LogOutput('info',"\n\n\nunConfiguring switch 1 and 2 ipv6 routes")
    retStruct = IpRouteConfig(deviceObj=switch2, route="1020::", mask=120, nexthop="1050::1", config=False, ipv6flag=True)
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\nFailed to unconfigure ipv6 address route")
        caseReturnCode = 1

    LogOutput('info',"\n\n\nPing after adding static route to S1 and S2")

    LogOutput('info',"\n\n\n Pinging host 1 to host 3 using IPv4")
    retStruct = host1.Ping(ipAddr="10.0.40.1", packetCount=1)
    Sleep(seconds=7, message="")
    #print devIntRetStruct
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv4 ping, Case Passed #####")
    else:
        LogOutput('info', "IPv4 Ping from host 1 to host 3 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed, Case Failed #####\n\n")

    LogOutput('info',"\n Pinging host 1 to host 2 using IPv6")
    retStruct = host1.Ping(ipAddr="1040::1", packetCount=1, ipv6Flag=True)
    Sleep(seconds=7, message="")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv6 ping, Case Passed #####")
    else:
        LogOutput('info', "IPv6 Ping from host 1 to host 3 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed, Case Failed #####\n\n")

    LogOutput('info',"\n\n\n Pinging host 2 to host 3 using IPv4")
    retStruct = host2.Ping(ipAddr="10.0.40.1", packetCount=1)
    Sleep(seconds=7, message="")
    #print devIntRetStruct
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv4 ping, Case Passed #####")
    else:
        LogOutput('info', "IPv4 Ping from host 2 to host 3 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed, Case Failed #####\n\n")

    LogOutput('info',"\n Pinging host 2 to host 3 using IPv6")
    retStruct = host2.Ping(ipAddr="1040::1", packetCount=1, ipv6Flag=True)
    Sleep(seconds=7, message="")
    retCode = retStruct.returnCode()
    if retCode:
        LogOutput('error', "\n##### Failed to do IPv6 ping, Case Passed #####")
    else:
        LogOutput('info', "IPv6 Ping from host 2 to host 3 return JSON:\n")
        retStruct.printValueString()
        LogOutput('info',"\n##### Ping Passed, Case Failed #####\n\n")



class Test_ecmp_ping:
    def setup_class (cls):
        # Test object will parse command line and formulate the env
        Test_ecmp_ping.testObj = testEnviron(topoDict=topoDict)
        # Get topology object
        Test_ecmp_ping.topoObj = Test_ecmp_ping.testObj.topoObjGet()

    def teardown_class (cls):
        Test_ecmp_ping.topoObj.terminate_nodes()
    def test_ecmp_ping(self):
        # GEt Device objects
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        wrkston03Obj = self.topoObj.deviceObjGet(device="wrkston03")
        retValue = ecmp_ping(switch1=dut01Obj, switch2=dut02Obj, host1=wrkston01Obj, host2=wrkston02Obj, host3=wrkston03Obj)
        if retValue != 0:
            assert "Test failed"
        else:
            LogOutput('info', "test passed\n\n\n\n############################# Next Test #########################\n")"""
