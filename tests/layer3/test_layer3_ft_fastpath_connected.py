#!/usr/bin/env python

# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
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

"""
import switch.CLI

topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 wrkston01 wrkston02",
            "topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,wrkston01:system-category:workstation,wrkston02:system-category:workstation"}

TEST_DESCRIPTION = "Directly Connected Hosts Fast Path Ping Test"
tcInstance.tcInfo(tcName = ResultsDirectory['testcaseName'], tcDesc = TEST_DESCRIPTION)

# Identifying workstations
dut01LinkStruct1 = topology.InterfaceGetByDeviceLink(device=headers.topo['dut01'], link=headers.topo['lnk01'])
dut01Port1 = common.ReturnJSONGetData(json=dut01LinkStruct1)
dut01LinkStruct2 = topology.InterfaceGetByDeviceLink(device=headers.topo['dut01'], link=headers.topo['lnk02'])
dut01Port2 = common.ReturnJSONGetData(json=dut01LinkStruct2)
if dut01Port1 == "1":
    h1 = headers.topo['wrkston01']
    h2 = headers.topo['wrkston02']
else:
    h1 = headers.topo['wrkston02']
    h2 = headers.topo['wrkston01']
linksList = [headers.topo['lnk01'], headers.topo['lnk02']]

tcInstance.defineStep(stepDesc="Connect to switch " + headers.topo['dut01'])
tcInstance.defineStep(stepDesc="Connect to workstations " + h1 + " and " + h2)
tcInstance.defineStep(stepDesc="Bring link up between all devices")
tcInstance.defineStep(stepDesc="Set IPv4 to workstations " + h1 + " and " + h2)
tcInstance.defineStep(stepDesc="Set IPv6 to workstations " + h1 + " and " + h2)
tcInstance.defineStep(stepDesc="Configure IP addresses for interfaces on switch " + headers.topo['dut01'])
tcInstance.defineStep(stepDesc="IPv4 ping between workstations " + h1 + " and " + h2)
tcInstance.defineStep(stepDesc="Verify HIT bit for IPv4 ping in ASIC")
tcInstance.defineStep(stepDesc="IPv6 ping between workstations " + h1 + " and " + h2)
tcInstance.defineStep(stepDesc="Verify HIT bit for IPv6 ping in ASIC")
tcInstance.defineStep(stepDesc="IPv4 and IPv6 ping between switch and workstations")

# Connecting the switch
tcInstance.startStep()

dut01_conn = switch.Connect(headers.topo['dut01'])
if dut01_conn is None:
    common.LogOutput('error', "Failed to connect to dut01")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

tcInstance.endStep()

# Grab the name of the hosts and try connecting to them
tcInstance.startStep()

common.LogOutput('info', "\nConnecting to the workstation " + h1)
devConn_h1 = host.Connect(h1)
if devConn_h1 is None:
    common.LogOutput('error', "\nFailed to connect to workstation " + h1)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nConnecting to the workstation " + h2)
devConn_h2 = host.Connect(h2)
if devConn_h2 is None:
    common.LogOutput('error', "\nFailed to connect to workstation " + h2)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

tcInstance.endStep()

# Enable the links between all devices
tcInstance.startStep()

returnStruct = topology.LinkStatusConfig(links=linksList, enable=1)
retCode = common.ReturnJSONGetCode(json=returnStruct)
if retCode:
   common.LogOutput('error', "Failed to enable links")
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

tcInstance.endStep()

# Configuring IPv4 on the workstation ethernet interfaces
tcInstance.startStep()

common.LogOutput('info', "\nConfiguring IPv4 for workstation " + h1)
retStruct = host.NetworkConfig(
    connection=devConn_h1,
    eth='eth1',
    ipAddr='10.0.0.10',
    netMask='255.255.255.0',
    broadcast='10.0.0.255',
    clear=0)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to configure IPv4 10.0.0.10 on workstation " + h1)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)
else:
    common.LogOutput('info', "\nSucceeded in configuring IPv4 10.0.0.10 on workstation " + h1)

common.LogOutput('info', "\nConfiguring IPv4 gateway for workstation " + h1)
retStruct = host.IPRoutesConfig(
    connection=devConn_h1,
    routeOperation='add',
    destNetwork='0.0.0.0',
    netMask=24,
    via='10.0.0.1',
    eth='eth1',
    metric=1,
    ipv6Flag=0)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to configure IPv4 gateway 10.0.0.1 on workstation " + h1)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)
else:
    common.LogOutput('info', "\nSucceeded in configuring IPv4 gateway 10.0.0.1 on workstation " + h1)

common.LogOutput('info', "\nConfiguring IPv4 for workstation " + h2)
retStruct = host.NetworkConfig(
    connection=devConn_h2,
    eth='eth1',
    ipAddr='11.0.0.10',
    netMask='255.255.255.0',
    broadcast='11.0.0.255',
    clear=0)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to configure IPv4 11.0.0.10 on workstation " + h2)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)
else:
    common.LogOutput('info', "\nSucceeded in configuring IPv4 11.0.0.10 on workstation " + h2)

common.LogOutput('info', "\nConfiguring IPv4 gateway for workstation " + h2)
retStruct = host.IPRoutesConfig(
    connection=devConn_h2,
    routeOperation='add',
    destNetwork='0.0.0.0',
    netMask=24,
    via='11.0.0.1',
    eth='eth1',
    metric=1,
    ipv6Flag=0)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to configure IPv4 gateway 11.0.0.1 on workstation " + h2)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)
else:
    common.LogOutput('info', "\nSucceeded in configuring IPv4 gateway 11.0.0.1 on workstation " + h2)

tcInstance.endStep()

# Configuring IPv6 on the workstation ethernet interfaces
tcInstance.startStep()

common.LogOutput('info', "\nConfiguring IPv6 for workstation " + h1)
retStruct = host.Network6Config(
    connection=devConn_h1,
    eth='eth1',
    ipAddr='2000::2',
    netMask=120,
    clear=0)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to configure IPv6 2000::2 on workstation " + h1)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)
else:
    common.LogOutput('info', "\nSucceeded in configuring IPv6 2000::2 on workstation " + h1)

common.LogOutput('info', "\nConfiguring IPv6 gateway for workstation " + h1)
retStruct = host.IPRoutesConfig(
    connection=devConn_h1,
    routeOperation='add',
    destNetwork='2002::',
    netMask=120,
    via='2000::1',
    eth='eth1',
    metric=1,
    ipv6Flag=1)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to configure IPv6 gateway 2002:: on workstation " + h1)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)
else:
    common.LogOutput('info', "\nSucceeded in configuring IPv6 gateway 2002:: on workstation " + h1)

common.LogOutput('info', "\nConfiguring IPv6 for workstation " + h2)
retStruct = host.Network6Config(
    connection=devConn_h2,
    eth='eth1',
    ipAddr='2002::2',
    netMask=120,
    clear=0)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to configure IPv6 2002::2 on workstation " + h2)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)
else:
    common.LogOutput('info', "\nSucceeded in configuring IPv6 2002::2 on workstation " + h2)

common.LogOutput('info', "\nConfiguring IPv6 gateway for workstation " + h2)
retStruct = host.IPRoutesConfig(
    connection=devConn_h2,
    routeOperation='add',
    destNetwork='2000::',
    netMask=120,
    via='2002::1',
    eth='eth1',
    metric=1,
    ipv6Flag=1)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to configure IPv6 gateway 2000:: on workstation " + h1)
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)
else:
    common.LogOutput('info', "\nSucceeded in configuring IPv6 gateway 2000:: on workstation " + h1)

tcInstance.endStep()

# Entering VTYSH CLI for configuration of IP addresses
tcInstance.startStep()

common.LogOutput('info', "\nEntering vtysh")
returnStructure = switch.CLI.VtyshShell(connection = dut01_conn)
retCode = common.ReturnJSONGetCode(json = returnStructure)
if retCode:
   common.LogOutput('error', "Failed to get vtysh prompt")
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)
else:
    vtyshInfo = common.ReturnJSONGetData(json=returnStructure, dataElement='vtyshPrompt')
    common.LogOutput("debug","vtysh shell buffer: \n"+vtyshInfo)

common.LogOutput('info', "\nEntering configure terminal")
retStruct = switch.DeviceInteract(connection=dut01_conn, command="configure terminal")
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "\nFailed to enter config mode")
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nSetting internal VLAN")
ip_command = "vlan internal range 400 500 ascending"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=ip_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to set internal VLAN")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

intf_command = "interface 1"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=intf_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to enter interface 1")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nGiving no shutdown on interface 1")
no_shut_command = "no shutdown"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=no_shut_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed no shutdown for interface 1")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nGiving an IP address to interface 1")
ip_command = "ip address 10.0.0.1/24"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=ip_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to set IP address for interface 1")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nGiving an IPv6 address to interface 1")
ip_command = "ipv6 address 2000::1/120"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=ip_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to set IPv6 address for interface 1")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

end_command = "exit"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=end_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "Failed to exit interface prompt")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

intf_command = "interface 2"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=intf_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to enter interface 2")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nGiving no shutdown on interface 2")
no_shut_command = "no shutdown"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=no_shut_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed no shutdown for interface 2")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nGiving an IP address to interface 2")
ip_command = "ip address 11.0.0.1/24"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=ip_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to set IP address for interface 2")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nGiving an IPv6 address to interface 2")
ip_command = "ipv6 address 2002::1/120"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=ip_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "\nFailed to set IPv6 address for interface 2")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

end_command = "exit"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=end_command)
retCode = retStruct.get('returnCode')
if retCode:
    common.LogOutput('error', "Failed to exit interface prompt")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

end_command = "exit"
retStruct = switch.DeviceInteract(connection=dut01_conn, command=end_command)
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "Failed to exit from config prompt")
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

returnStructure = switch.CLI.VtyshShell(connection = dut01_conn,configOption="unconfig")
vtyshExitInfo = common.ReturnJSONGetData(json=returnStructure, dataElement='vtyshPrompt')
common.LogOutput("debug","vtysh shell buffer: \n"+vtyshExitInfo)
retCode = common.ReturnJSONGetCode(json = returnStructure)
if retCode:
   common.LogOutput('error', "Failed to exit vtysh prompt")
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

tcInstance.endStep()

#IPv4 ping between workstations
tcInstance.startStep()

common.LogOutput('info', "\nPinging between workstations - IPv4")
retStruct = host.DevicePing(connection=devConn_h2, ipAddr="10.0.0.10")
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "\nFailed to ping host %s from host %s " %(h2, h1))
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nPinging between workstations - IPv4")
retStruct = host.DevicePing(connection=devConn_h1, ipAddr="11.0.0.10")
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "\nFailed to ping host %s from host %s " %(h1, h2))
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

tcInstance.endStep()

#Verifying HIT Bit in ASIC for IPv4 ping
tcInstance.startStep()

retStruct = host.DeviceInteract(connection=devConn_h1, command="ping -c 10 11.0.0.10 &")

common.LogOutput('info', "\nVerifying HIT Bit for IPv4 ping")
appctl_command = "ovs-appctl plugin/debug l3host"

dphit_host1 = None
dphit_host2 = None

for i in range(1,3):
    retStruct = switch.DeviceInteract(connection=dut01_conn, command=appctl_command)
    retCode = retStruct.get('returnCode')
    if retCode:
        common.LogOutput('error', "\novs-appctl command failed")
        tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

    table = retStruct['buffer']
    common.LogOutput('info', "\n" + table)
    rows = table.split('\n')

    host1row = None
    host2row = None


    for row in rows:
        if '10.0.0.10' in row:
            host1row = row
        if '11.0.0.10' in row:
            host2row = row

    if host1row == None:
        common.LogOutput('error', "\nhost 1 not Programmed in ASIC")
        tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

    if host2row == None:
        common.LogOutput('error', "\nhost 2 not Programmed in ASIC")
        tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

    columns = host1row.split()
    dphit_host1 = columns[5]

    columns = host2row.split()
    dphit_host2 = columns[5]

    if dphit_host1 == 'y' and dphit_host2 == 'y':
        break

if dphit_host1 == 'n':
    common.LogOutput('error', "\nDP hit was not set for host 1")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

if dphit_host2 == 'n':
    common.LogOutput('error', "\nDP hit was not set for host 2")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

tcInstance.endStep()

#IPv6 ping between workstations
tcInstance.startStep()

common.LogOutput('info', "\nPinging between workstations - IPv6")
retStruct = host.DevicePing(connection=devConn_h2, ipAddr="2000::2", ipv6Flag=1)
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "\nFailed to ping host %s from host %s " %(h2, h1))
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nPinging between workstations - IPv6")
retStruct = host.DevicePing(connection=devConn_h1, ipAddr="2002::2", ipv6Flag=1)
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "\nFailed to ping host %s from host %s " %(h1, h2))
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

tcInstance.endStep()

#Verifying HIT Bit in ASIC for IPv6 ping
tcInstance.startStep()

retStruct = host.DeviceInteract(connection=devConn_h1, command="ping6 -c 10 2002::2 &")

common.LogOutput('info', "\nVerifying HIT Bit for IPv6 ping")
appctl_command = "ovs-appctl plugin/debug l3v6host"

dphit_host1 = None
dphit_host2 = None

for i in range(1,3):
    retStruct = switch.DeviceInteract(connection=dut01_conn, command=appctl_command)
    retCode = retStruct.get('returnCode')
    if retCode:
        common.LogOutput('error', "\novs-appctl command failed")
        tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

    table = retStruct['buffer']
    common.LogOutput('info', "\n" + table)
    rows = table.split('\n')

    host1row = None
    host2row = None


    for row in rows:
        if '2000:0000:0000:0000:0000:0000:0000:0002' in row:
            host1row = row
        if '2002:0000:0000:0000:0000:0000:0000:0002' in row:
            host2row = row

    if host1row == None:
        common.LogOutput('error', "\nhost 1 not Programmed in ASIC")
        tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

    if host2row == None:
        common.LogOutput('error', "\nhost 2 not Programmed in ASIC")
        tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

    columns = host1row.split()
    dphit_host1 = columns[5]

    columns = host2row.split()
    dphit_host2 = columns[5]

    if dphit_host1 == 'y' and dphit_host2 == 'y':
        break

if dphit_host1 == 'n':
    common.LogOutput('error', "\nDP hit was not set for host 1")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

if dphit_host2 == 'n':
    common.LogOutput('error', "\nDP hit was not set for host 2")
    tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

tcInstance.endStep()

#IPv4 and IPv6 pings between switch and workstations
tcInstance.startStep()

common.LogOutput('info', "\nIPv4 ping between switch and host " + h1)
retStruct = host.DevicePing(connection=devConn_h1, ipAddr="10.0.0.1")
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "\nFailed IPv4 ping between switch and host " + h1)
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nIPv6 ping between switch and host " + h1)
retStruct = host.DevicePing(connection=devConn_h1, ipAddr="2000::1", ipv6Flag=1)
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "\nFailed IPv6 ping between switch and host " + h1)
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nIPv4 ping between switch and host " + h2)
retStruct = host.DevicePing(connection=devConn_h2, ipAddr="11.0.0.1")
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "\nFailed IPv4 ping between switch and host " + h2)
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

common.LogOutput('info', "\nIPv6 ping between switch and host " + h2)
retStruct = host.DevicePing(connection=devConn_h2, ipAddr="2002::1", ipv6Flag=1)
retCode = retStruct.get('returnCode')
if retCode:
   common.LogOutput('error', "\nFailed IPv6 ping between switch and host " + h2)
   tcInstance.setVerdictAction (TC_STEPVERDICT_FAIL, TC_STEPFAILACTION_EXIT)

tcInstance.endStep()"""
