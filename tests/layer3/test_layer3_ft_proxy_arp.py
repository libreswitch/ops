#!/usr/bin/env python

# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
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
import pexpect
import re
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

# Topology Diagram #
'''
+--------+               +--------+                +--------+
|        |             1 |        | 2,3,4---       |Host02, |
|Host01  +---------------+Dut01   +----------------+Host03, |
|        |               |        |                |Host04--|
+--------+               +--------+                +--------+
'''
# Global variables.
# Number of Hosts should always be greater then 1.
NO_OF_HOST = 5
SOURCE_HOST_MASK = 16
IP_MASK = 24
DUT_DEST_HOST_IP = "20.0.0.2"
HOST_DUT_ROUTE_IP = "20.0.1.0"
DUT_SRC_HOST_IP = "20.0.1.1"
DUT_SRC_HOST_MOD_IP = "20.0.1.3"
DUT_SRC_HOST_IP_SECONDARY = "20.0.1.4"
SRC_HOST_DUT_IP = "20.0.1.2"
HOST_IP_STRING = "20.0.0"


# Support function to reboot the switch
def switch_reboot(deviceObj):
    LogOutput('info', "Reboot switch " + deviceObj.device)
    deviceObj.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct


def ping_test(**kwargs):
    source_host = kwargs.get('switch2', None)
    # Ping IPv4-address from switch2 to other switches
    for x in range(1, NO_OF_HOST):
        ip_add_id = x + 2
        cmd = str("ping " + HOST_IP_STRING + ".%d repetitions 5" % ip_add_id)
        source_host.DeviceInteract(command=cmd)


def isMacPresent(string):
    string = str(string)
    p = re.compile(ur'(?:[0-9a-fA-F]:?){12}')
    Mac = re.search(p, string)
    if Mac is None:
        return False
    return True


def getMacFromString(string):
    string = str(string)
    Mac = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})',
                    string, re.I).group()
    return Mac


def show_arp_table(dut):
    devIntReturn = dut.DeviceInteract(command="show arp")
    arp_table = devIntReturn.get('buffer')
    return arp_table


def enterVtysh(dut01):
    retStruct = dut01.DeviceInteract(command="vtysh")
    retCode = retStruct.get('returnCode')
    if retCode == 0:
        return True
    else:
        return False


def exitVtysh(dut01):
    out = dut01.DeviceInteract(command="exit")
    retCode = out.get('returnCode')
    assert retCode == 0, "Failed to exit vtysh"
    return True


def enterInterfaceContext(dut01, interface):
    if(enterVtysh(dut01)) is False:
        print "In Vtysh already"
    retStruct = dut01.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    cmd = "interface " + str(interface)
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter Interface context"

    return True


def exitInterfaceContext(dut01):
    cmd = "exit"
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to exit Interface context"

    retStruct = dut01.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit config terminal"

    retStruct = dut01.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    return True


def getSwitchMac(dut01):
    switchMac = ""
    devIntReturn = dut01.DeviceInteract(command="show interface 1")
    systemDetails = devIntReturn.get('buffer')
    switchDetail = systemDetails.split('\r\n')

    for detail in switchDetail:
        if "MAC Address" in detail:
            switchMac = getMacFromString(detail)

    return switchMac


def startBackgroundPingToOtherHosts(host):
    for x in range(1, NO_OF_HOST):
        ip_add_id = x + 2
        cmd = str("nohup ping " + HOST_IP_STRING + "%d &" % ip_add_id)
        host.DeviceInteract(command=cmd)


def verifyARPTable(dut01, hosts):
    switchMac = getSwitchMac(dut01)
    sourceARPTable = show_arp_table(hosts[0])
    arpDetail = sourceARPTable.split('\r\n')
    macInARPTable = ""

    for x in range(1, NO_OF_HOST):
        ip_add_id = x + 2
        ipString = str(HOST_IP_STRING + ".%d" % ip_add_id)
        for detail in arpDetail:
            if (ipString in detail):
                if isMacPresent(detail):
                    macInARPTable = getMacFromString(detail)
                    if switchMac != macInARPTable:
                        return False
                else:
                    return False

    return True


def pingAndVerifyARPTable(dut01, hosts):
    ping_test(switch2=hosts[0])
    return verifyARPTable(dut01, hosts)


def enterBashShell(dut):
    devIntReturn = dut.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter bash shell"
    return True


def enterSWNameSpace(dut):
    # Enter Bash Shell
    if(enterBashShell(dut) is False):
        return False

    cmd = "ip netns exec swns bash"
    devIntReturn = dut.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter Software namespace"

    return True


def configureInterfaceAndAddRoute(dut, host, lnk, ipAddress):
    LogOutput('info', "Configuring IPv4 address ")
    retStruct = InterfaceIpConfig(deviceObj=host,
                                  interface=host.linkPortMapping[lnk],
                                  addr=ipAddress, mask=IP_MASK, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        LogOutput('info', "Failed to configure an IPv4 address")

    retStruct = InterfaceEnable(deviceObj=host, enable=True,
                                interface=host.linkPortMapping[lnk])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface"

    retStruct = IpRouteConfig(deviceObj=host, route=HOST_DUT_ROUTE_IP,
                              mask=IP_MASK, nexthop=DUT_DEST_HOST_IP)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to add route"

    # Adding the DUT port to VLAN 9
    dutInterface = dut.linkPortMapping[lnk]
    if (enterInterfaceContext(dut, dutInterface) is False):
        return False

    devIntReturn = dut.DeviceInteract(command="no shutdown")
    devIntReturn = dut.DeviceInteract(command="no routing")
    devIntReturn = dut.DeviceInteract(command="vlan acces 9")

    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Adding port to VLAN interface failed"

    if (exitInterfaceContext(dut) is False):
        return False


def initial_configure(dut01, hosts):
    # Enable interface and configure Ip
    LogOutput('info', "Enabling interface1 on %s" % dut01.device)
    interface_value = dut01.linkPortMapping["lnk01"]
    retStruct = InterfaceEnable(deviceObj=dut01,
                                enable=True,
                                interface=interface_value)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface"

    # Assigning an IPv4 address on interface
    LogOutput('info', "Configuring IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface=interface_value,
                                  addr=DUT_SRC_HOST_IP, mask=IP_MASK,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address on interface "

    # Entering interface for link 1 SW1, giving an IPv6 address
    LogOutput('info', "Configuring IPv6 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface=dut01.linkPortMapping['lnk01'],
                                  addr="1030::2", mask=120,
                                  ipv6flag=True, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    # Enabling interface of Source host.
    LogOutput('info', "Enabling interface on SW2")
    retStruct = InterfaceEnable(deviceObj=hosts[0], enable=True,
                                interface=hosts[0].linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface on SW2"

    # Giving an IPv6 address on Source host.
    LogOutput('info', "Configuring IPv6 address on link 1 SW2")
    retStruct = InterfaceIpConfig(deviceObj=hosts[0],
                                  interface=hosts[0].linkPortMapping['lnk01'],
                                  addr="1030::3", mask=120, ipv6flag=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv6 address"

    # Entering interface for link Source host, giving an IPv4 address
    LogOutput('info', "Configuring IPv4 address on link of source host")
    retStruct = InterfaceIpConfig(deviceObj=hosts[0],
                                  interface=hosts[0].linkPortMapping['lnk01'],
                                  addr=SRC_HOST_DUT_IP,
                                  mask=SOURCE_HOST_MASK, config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure an IPv4 address"

    # Configuring VLAN on DUT for the destination hosts.
    devIntReturn = dut01.DeviceInteract(command="vtysh")
    devIntReturn = dut01.DeviceInteract(command="config t")
    devIntReturn = dut01.DeviceInteract(command="vlan 9")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    devIntReturn = dut01.DeviceInteract(command="exit")
    devIntReturn = dut01.DeviceInteract(command="interface vlan 9")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    cmd = "ip add " + str(DUT_DEST_HOST_IP) + "/" + str(IP_MASK)
    devIntReturn = dut01.DeviceInteract(command=cmd)
    devIntReturn = dut01.DeviceInteract(command="exit")
    devIntReturn = dut01.DeviceInteract(command="exit")

    # Configure hosts with IP address and route to source with nexhop of DUT.
    for x in range(1, NO_OF_HOST):
        ip_add_id = x + 2
        lnkId = x + 1
        lnk = str('lnk0%d' % lnkId)
        ip_address = str(HOST_IP_STRING + ".%d" % ip_add_id)
        configureInterfaceAndAddRoute(dut01, hosts[x], lnk, ip_address)


def clearARPTable(dut, lnk):
    # disabling interface2 SW2
    LogOutput('info', "Disabling interface")
    retStruct = InterfaceEnable(deviceObj=dut, enable=False,
                                interface=dut.linkPortMapping[lnk])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to disable interface"

    # Enabling interface2 SW2
    LogOutput('info', "Enabling interface")
    retStruct = InterfaceEnable(deviceObj=dut, enable=True,
                                interface=dut.linkPortMapping[lnk])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to enable interface"


def enableDisableProxyARPState(dut, interface, enable):
    if (enterInterfaceContext(dut, interface) is False):
        return False
    if enable:
        devIntReturn = dut.DeviceInteract(command="ip proxy-arp")
    else:
        devIntReturn = dut.DeviceInteract(command="no ip proxy-arp")
    devIntReturn = dut.DeviceInteract(command="exit")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Enabling/disabling Proxy ARP failed"

    if (exitInterfaceContext(dut) is False):
        return False

    cmd = "sysctl net.ipv4.conf." + str(interface) + ".proxy_arp"
    out = dut.DeviceInteract(command=cmd)
    proxy_arp_state = out.get('buffer')
    if enable:
        assert "net.ipv4.conf." + str(interface) + ".proxy_arp = 1" \
            in proxy_arp_state, "Failed to verify Proxy ARP is enabled"\
            " on L3 port in kernel via sysctl"
    else:
        assert "net.ipv4.conf." + str(interface) + ".proxy_arp = 0" \
            in proxy_arp_state, "Failed to verify Proxy ARP is enabled "\
            "on L3 port in kernel via sysctl"

    if(enterVtysh(dut) is False):
        return False


def verifyProxyARPInShowInterface(dut, interface, enable):
    if(enterVtysh(dut)) is False:
        return False

    cmdOut = dut.cmdVtysh(command="show interface" + str(interface))
    if enable:
        assert 'Proxy ARP is enabled' in cmdOut, "Failed to validate the" \
            "presence of string 'Proxy ARP is enabled'in show interface output"
    else:
        assert 'Proxy ARP is enabled' not in cmdOut, "Failed to validate the "\
            "absence of String 'Proxy ARP is enabled' in show interface output"


def proxyARPonL3PortTest(dut01, hosts):
    if pingAndVerifyARPTable(dut01, hosts):
        assert 0, "Failed to verify that the Proxy ARP funtionality is "\
                  "disabled by default"

    if (enterSWNameSpace(dut01) is False):
        return False

    # Routing should be enabled by default
    out = dut01.DeviceInteract(command="sysctl net.ipv4.ip_forward")
    ip_forward_state = out.get('buffer')
    assert 'net.ipv4.ip_forward = 1' in ip_forward_state, "Failed to verify"\
        "ip forwarding is enabled by default"

    # Proxy ARP should be disabled by default
    interface = dut01.linkPortMapping['lnk01']
    cmd = "sysctl net.ipv4.conf." + str(interface) + ".proxy_arp"
    out = dut01.DeviceInteract(command=cmd)
    proxy_arp_state = out.get('buffer')
    assert "net.ipv4.conf." + str(interface) + ".proxy_arp = 0" \
        in proxy_arp_state, "Failed to verify Proxy ARP is disabled "\
        "by default on L3 port in kernel via sysctl"

    # Enable Proxy ARP on L3 port
    enableDisableProxyARPState(dut01, interface, True)
    verifyProxyARPInShowInterface(dut01, interface, True)

    # Save the configuration on SW1.
    runCfg = "copy running-config startup-config"
    devIntReturn = dut01.DeviceInteract(command=runCfg)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to save the running configuration"

    # Perform reboot of SW1.
    devRebootRetStruct = switch_reboot(dut01)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Switch1 reboot - FAILED")
        assert(devRebootRetStruct.returnCode() == 0)
    else:
        LogOutput('info', "Switch1 reboot - SUCCESS")

    verifyProxyARPInShowInterface(dut01, interface, True)
    clearARPTable(hosts[0], 'lnk01')

    if (exitVtysh(dut01) is False):
        return False

    # Disable Proxy ARP on L3 port
    enableDisableProxyARPState(dut01, interface, True)
    verifyProxyARPInShowInterface(dut01, interface, True)

    if pingAndVerifyARPTable(dut01, hosts):
        assert "Verification of Proxy ARP functionality on disable failed"

    if(exitVtysh(dut01)) is False:
        return False

    return True


def proxyARPOnIpChangeAndSecondaryIpConfiguredInterfaceTest(dut01, hosts):
    # This function requires the the config on the DUT ot be present.
    if (enterSWNameSpace(dut01) is False):
        return False

    if (enterVtysh(dut01) is False):
        return False

    if pingAndVerifyARPTable(dut01, hosts):
        assert "Verification of Proxy ARP functionality failed"

    if(exitVtysh(dut01)) is False:
        return False

    # Enable Proxy ARP on L3 port
    interface = dut01.linkPortMapping['lnk01']
    enableDisableProxyARPState(dut01, interface, True)

    # Assigning secondary IPv4 address on interface
    LogOutput('info', "Configuring secondary IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface=dut01.linkPortMapping['lnk01'],
                                  addr=DUT_SRC_HOST_IP_SECONDARY,
                                  mask=SOURCE_HOST_MASK,
                                  secondary=True,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to configure a secondary IPv4 address on interface "

    if(enterBashShell(dut01) is False):
        return False

    cmd = "sysctl net.ipv4.conf." + str(interface) + ".proxy_arp"
    out = dut01.DeviceInteract(command=cmd)
    proxy_arp_state = out.get('buffer')
    assert "net.ipv4.conf." + str(interface) + ".proxy_arp = 1" \
        in proxy_arp_state, "Failed to verify Proxy ARP is enabled"\
        " on L3 port in kernel via sysctl"

    if(enterVtysh(dut01) is False):
        return False

    verifyProxyARPInShowInterface(dut01, interface, True)

    if pingAndVerifyARPTable(dut01, hosts):
        LogOutput('info', "Proxy ARP functionality successfully verified.")
    else:
        assert 0, "Proxy ARP verification failed"

    return True


def proxyARPOnIpModificationAndInterfaceFlapWithTrafficInBackground(dut01,
                                                                    hosts):
    # This function needs thei DUT to be in proxy ARP enabled state.
    # IP Modification test with traffic in background.
    if (enterSWNameSpace(dut01) is False):
        return False

    clearARPTable(hosts[0], 'lnk01')
    if (enterSWNameSpace(hosts[0]) is False):
        return False

    startBackgroundPingToOtherHosts(hosts[0])

    LogOutput('info', "Modifying IPv4 address on link 1 SW1")
    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface=dut01.linkPortMapping['lnk01'],
                                  addr=DUT_SRC_HOST_MOD_IP, mask=IP_MASK,
                                  config=True)
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Failed to modify an IPv4 address on interface "

    if(enterVtysh(hosts[0]) is False):
        return False

    if verifyARPTable(dut01, hosts):
        LogOutput('info', "Proxy ARP functionality successfully verified"
                  "on IP modification.")
    else:
        LogOutput('info', "Proxy ARP verification failed on IP"
                  "address modification .")

    if(exitVtysh(dut01) is False):
        return False

    # Disable Proxy ARP with traffic in background.
    interface = dut01.linkPortMapping['lnk01']
    enableDisableProxyARPState(dut01, interface, False)
    verifyProxyARPInShowInterface(dut01, interface, False)

    clearARPTable(hosts[0], 'lnk01')

    if verifyARPTable(dut01, hosts):
        LogOutput('info', "Failed to verify Proxy ARP functionality "
                  " on Disable with traffic in background.")
    else:
        LogOutput('info', "Proxy ARP functionality successfully verified"
                  " on Disable with traffic in background.")

    # Enable back proxy ARP with traffic in background.
    enableDisableProxyARPState(dut01, 1, True)
    verifyProxyARPInShowInterface(dut01, 1, True)

    if verifyARPTable(dut01, hosts):
        LogOutput('info', "Proxy ARP functionality successfully verified"
                  " on Enable with traffic in background.")
    else:
        LogOutput('info', "Failed to verify Proxy ARP functionality "
                  " on Enable with traffic in background.")
    no_of_reboots = 5

    for x in range(0, no_of_reboots):
        # Interface Flapping - Disable
        retStruct = InterfaceEnable(deviceObj=dut01, enable=False,
                                    interface=dut01.linkPortMapping["lnk01"])
        # Clear the ARP table in source host.
        clearARPTable(hosts[0], 'lnk01')
        # Interface Flapping - Enable
        retStruct = InterfaceEnable(deviceObj=dut01, enable=True,
                                    interface=dut01.linkPortMapping["lnk01"])

        if verifyARPTable(dut01, hosts):
            LogOutput('info', "Proxy ARP functionality successfully verified"
                      " on interface Enable with traffic in background.")
        else:
            LogOutput('info', "Failed to verify Proxy ARP functionality "
                      " on interface Enable with traffic in background.")

    return True


def proxyARPOnRoutingStatusModificationWithTrafficInBackground(dut01, hosts):
    # Function requires proxy ARP to be enabled and traffic in background
    # Disable routing on the interface and verifying proxy ARP behavior.
    if (enterSWNameSpace(dut01) is False):
        return False

    if (enterInterfaceContext(dut01, 1) is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="no routing")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "No routing failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False

    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.1.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.1.proxy_arp = 0' in proxy_arp_state, "Failed to "\
        "verify Proxy ARP is disabled on no routing"

    clearARPTable(hosts[0], 'lnk01')

    if verifyARPTable(dut01, hosts):
        LogOutput('info', "Failed to verify Proxy ARP functionality "
                  " on Disable Routing with traffic in background.")
    else:
        LogOutput('info', "Proxy ARP functionality successfully verified"
                  " on Disable Routing with traffic in background.")

    # Enable Routing back and verify Proxy ARP behavior with traffic in bg.
    interface = dut01.linkPortMapping['lnk01']
    if (enterInterfaceContext(dut01, interface) is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="routing")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Enable routing failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    enableDisableProxyARPState(dut01, interface, True)
    verifyProxyARPInShowInterface(dut01, interface, True)

    if verifyARPTable(dut01, hosts):
        LogOutput('info', "Proxy ARP functionality successfully verified"
                  " on Enable Routing  with traffic in background.")
    else:
        LogOutput('info', "Failed to verify Proxy ARP functionality "
                  " on Enable Routing with traffic in background.")

    return True


def proxyARPOnMultipleReloadsWithTrafficInBackground(dut01, hosts):
    # Function requires proxy ARP to be enabled and traffic in background
    # Save the configuration on SW1.
    runCfg = "copy running-config startup-config"
    devIntReturn = dut01.DeviceInteract(command=runCfg)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to save the running configuration"

    # Perform multiple reboots on  SW1.
    devRebootRetStruct = switch_reboot(dut01)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Switch1 reboot - FAILED")
        assert(devRebootRetStruct.returnCode() == 0)
    else:
        LogOutput('info', "Switch1 reboot - SUCCESS")

    devRebootRetStruct = switch_reboot(dut01)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Switch1 reboot - FAILED")
        assert(devRebootRetStruct.returnCode() == 0)
    else:
        LogOutput('info', "Switch1 reboot - SUCCESS")

    devRebootRetStruct = switch_reboot(dut01)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Switch1 reboot - FAILED")
        assert(devRebootRetStruct.returnCode() == 0)
    else:
        LogOutput('info', "Switch1 reboot - SUCCESS")

    cmdOut = dut01.cmdVtysh(command="show interface 1")
    assert 'Proxy ARP is enabled' in cmdOut, "Failed to validate the" \
        " presence of string 'Proxy ARP is enabled' in show interface output"
    if verifyARPTable(dut01, hosts):
        LogOutput('info', "Proxy ARP functionality successfully verified"
                  " after multiple reboots with traffic in background.")
    else:
        LogOutput('info', "Failed to verify Proxy ARP functionality "
                  " after multiple reboots with traffic in background.")

    if (enterSWNameSpace(hosts[0]) is False):
        return False

    devIntRetStruct = hosts[0].DeviceInteract(command="killall -9 ping")

    if(enterVtysh(hosts[0]) is False):
        return False

    return True


def proxyARPonL2PortTest(dut01):
    # No routing
    if (enterSWNameSpace(dut01) is False):
        return False
    # Enable ip proxy ARP
    interface = dut01.linkPortMapping['lnk01']
    enableDisableProxyARPState(dut01, interface, True)
    verifyProxyARPInShowInterface(dut01, interface, True)

    if (enterInterfaceContext(dut01, 1) is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="no routing")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "No routing failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False

    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.1.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.1.proxy_arp = 0' in proxy_arp_state, "Failed to "\
        "verify Proxy ARP cannot be enabled on L2 port in kernel via sysctl"

    if(enterVtysh(dut01) is False):
        return False

    verifyProxyARPInShowInterface(dut01, interface, False)
    if(exitVtysh(dut01) is False):
        return False

    return True


def proxyARPonSplitParentInterfaceTest(dut01):
    # disabling interface1 SW2
    if (enterSWNameSpace(dut01) is False):
        return False

    if(enterVtysh(dut01) is False):
        return False

    # disabling interface1 SW1
    LogOutput('info', "Disabling interface on SW1")
    retStruct = InterfaceEnable(deviceObj=dut01, enable=False,
                                interface=dut01.linkPortMapping['lnk01'])
    retCode = retStruct.returnCode()
    if retCode != 0:
        assert "Unable to disable interface on SW1"

    if(exitVtysh(dut01) is False):
        return False

    # enable Proxy ARP on a non-split parent interface
    if (enterInterfaceContext(dut01, 54) is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="ip proxy-arp")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Enabling Proxy ARP failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False
    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.54.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.54.proxy_arp = 1' in proxy_arp_state, "Failed to "\
        "verify Proxy ARP is Enabled on a non split parent interface in "\
        "kernel via sysctl"

    if(enterVtysh(dut01)) is False:
        return False

    cmdOut = dut01.cmdVtysh(command="show interface 54")
    assert 'Proxy ARP is enabled' in cmdOut, "Failed to validate the " \
        "presence of string 'Proxy ARP is enabled' in show interface output"

    if(exitVtysh(dut01) is False):
        return False

    # Proxy ARP should be disabled on a split interface.
    if (enterInterfaceContext(dut01, 54) is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="split \n y")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Split failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False
    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.54.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.54.proxy_arp = 0' in proxy_arp_state, "Failed to "\
        "verify Proxy ARP is disabled on split interface in kernel via sysctl"

    if(enterVtysh(dut01)) is False:
        return False

    cmdOut = dut01.cmdVtysh(command="show interface 54")
    assert 'Proxy ARP is enabled' not in cmdOut, "Failed to validate the "\
        "absence of String 'Proxy ARP is enabled' in show interface output "\

    if(exitVtysh(dut01) is False):
        return False

    return True


def proxyARPonSplitChildInterfaceTest(dut01):
    if (enterSWNameSpace(dut01) is False):
        return False

    # Proxy ARP on a non-split child interface
    if (enterInterfaceContext(dut01, 53-1) is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="ip proxy-arp")
    retCode = devIntReturn.get('returnCode')
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False
    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.53-1.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.53-1.proxy_arp = 0' in proxy_arp_state, "Failed to "\
        "verify Proxy ARP is not enabled for a non split child interface in "\
        "kernel via sysctl"

    if(enterVtysh(dut01)) is False:
        return False

    cmdOut = dut01.cmdVtysh(command="show interface 53-1")
    assert 'Proxy ARP is enabled' not in cmdOut, "Failed to validate the "\
        "absence of String 'Proxy ARP is enabled' in show interface output "\

    if(exitVtysh(dut01) is False):
        return False

    # Split interface.
    if (enterInterfaceContext(dut01, 53) is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="split \n y")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Split failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(exitVtysh(dut01) is False):
        return False

    # Proxy ARP on a split child interface
    if (enterInterfaceContext(dut01, "53-1") is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="ip proxy-arp")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Enabling proxy ARP failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False
    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.53-1.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.53-1.proxy_arp = 1' in proxy_arp_state, "Failed to "\
        "verify Proxy ARP is enabled on split child interface in kernel "\
        "via sysctl"

    if(enterVtysh(dut01)) is False:
        return False

    cmdOut = dut01.cmdVtysh(command="show interface 53-1")
    assert 'Proxy ARP is enabled' in cmdOut, "Failed to validate the "\
        "presence of String 'Proxy ARP is enabled' in show interface output "\

    if(exitVtysh(dut01) is False):
        return False

    # Disable Split interface.
    if (enterInterfaceContext(dut01, 53) is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="no split \n yes")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "no split failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False

    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.53-1.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.53-1.proxy_arp = 0' in proxy_arp_state, "Failed to "\
        "verify in kernel via sysctl that Proxy ARP is disabled on child "\
        "interface when parent interface is reset to no split."

    if(enterVtysh(dut01)) is False:
        return False

    cmdOut = dut01.cmdVtysh(command="show interface 53-1")
    assert 'Proxy ARP is enabled' not in cmdOut, "Failed to validate the "\
        "absence of String 'Proxy ARP is enabled' in show interface output "\

    if(exitVtysh(dut01) is False):
        return False

    return True


def proxyARPonVLANInterfaceTest(dut01, hosts):
    if (enterSWNameSpace(dut01) is False):
        return False

    devIntReturn = dut01.DeviceInteract(command="vtysh")
    devIntReturn = dut01.DeviceInteract(command="config t")
    devIntReturn = dut01.DeviceInteract(command="vlan 3")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    devIntReturn = dut01.DeviceInteract(command="exit")
    devIntReturn = dut01.DeviceInteract(command="interface 1")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    devIntReturn = dut01.DeviceInteract(command="no routing")
    devIntReturn = dut01.DeviceInteract(command="vlan acces 3")
    devIntReturn = dut01.DeviceInteract(command="exit")
    devIntReturn = dut01.DeviceInteract(command="interface vlan 3")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    cmd = "ip add " + str(DUT_SRC_HOST_IP) + "/" + str(IP_MASK)
    devIntReturn = dut01.DeviceInteract(command=cmd)
    devIntReturn = dut01.DeviceInteract(command="do show ru")
    devIntReturn = dut01.DeviceInteract(command="exit")
    devIntReturn = dut01.DeviceInteract(command="exit")

    print "ARP table verification on Vlan interface before enabling"
    if pingAndVerifyARPTable(dut01, hosts):
        assert 0, "Failed to verify that the Proxy ARP funtionality is "\
                  "disabled by default"

    # enable Proxy ARP on L3 VLAN interface
    if (enterInterfaceContext(dut01, "vlan 3") is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="ip proxy-arp")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Enabling Proxy ARP failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False
    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.vlan3.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.vlan3.proxy_arp = 1' in proxy_arp_state, "Failed to"\
        " verify Proxy ARP is enabled on vlan interface in kernel via sysctl"

    print "ARP table verification on VLAN interface after enabling"
    if(enterVtysh(dut01) is False):
        return False

    if pingAndVerifyARPTable(dut01, hosts):
        print "ARP verification on VLAN interface passed"
    else:
        assert 0, "Failed to verify that the Proxy ARP funtionality on "\
                  "VLAN interface"

    clearARPTable(hosts[0], 'lnk01')

    # Disable Proxy ARP on L3 vlan interface
    if (enterInterfaceContext(dut01, "vlan 3") is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="no ip proxy-arp")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Disabling Proxy ARP failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False
    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.vlan3.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.vlan3.proxy_arp = 0' in proxy_arp_state, "Failed to"\
        " verify Proxy ARP is disabled on vlan interface in kernel via sysctl"

    print "ARP table verification on VLAN interface after disable"

    if(enterVtysh(dut01) is False):
        return False

    clearARPTable(hosts[0], 'lnk01')

    if pingAndVerifyARPTable(dut01, hosts):
        assert 0, "Failed to verify that the Proxy ARP funtionality is "\
                  "disabled on VLAN interface"

    return True


def proxyARPOnBulkAdditionAndTrafficInBackgroungOnVLANInterface(dut01, hosts):
    # Function requires VLAN interface configurations to be present
    # and traffic running in background.
    if (enterSWNameSpace(dut01) is False):
        return False

    # Bulk Addition of Config.
    devIntReturn = dut01.DeviceInteract(command="vtysh")
    devIntReturn = dut01.DeviceInteract(command="config t")
    devIntReturn = dut01.DeviceInteract(command="no vlan 9")
    devIntReturn = dut01.DeviceInteract(command="vlan 9")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    devIntReturn = dut01.DeviceInteract(command="exit")
    devIntReturn = dut01.DeviceInteract(command="interface 2")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    devIntReturn = dut01.DeviceInteract(command="no routing")
    devIntReturn = dut01.DeviceInteract(command="vlan acces 9")
    devIntReturn = dut01.DeviceInteract(command="interface 3")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    devIntReturn = dut01.DeviceInteract(command="no routing")
    devIntReturn = dut01.DeviceInteract(command="vlan acces 9")
    devIntReturn = dut01.DeviceInteract(command="interface 4")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    devIntReturn = dut01.DeviceInteract(command="no routing")
    devIntReturn = dut01.DeviceInteract(command="vlan acces 9")
    devIntReturn = dut01.DeviceInteract(command="interface 5")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    devIntReturn = dut01.DeviceInteract(command="no routing")
    devIntReturn = dut01.DeviceInteract(command="vlan acces 9")
    devIntReturn = dut01.DeviceInteract(command="exit")
    devIntReturn = dut01.DeviceInteract(command="interface vlan 9")
    devIntReturn = dut01.DeviceInteract(command="no shutdown")
    cmd = "ip add " + str(DUT_DEST_HOST_IP) + "/" + str(IP_MASK)
    devIntReturn = dut01.DeviceInteract(command=cmd)
    devIntReturn = dut01.DeviceInteract(command="do show ru")
    devIntReturn = dut01.DeviceInteract(command="exit")
    devIntReturn = dut01.DeviceInteract(command="exit")

    # enable Proxy ARP on L3 VLAN interface
    if (enterInterfaceContext(dut01, "vlan 3") is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="ip proxy-arp")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Enabling Proxy ARP failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False
    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.vlan3.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.vlan3.proxy_arp = 1' in proxy_arp_state, "Failed to"\
        " verify Proxy ARP is enabled on vlan interface in kernel via sysctl"

    print "ARP table verification on Vlan interface after enabling"
    if(enterVtysh(dut01) is False):
        return False

    if pingAndVerifyARPTable(dut01, hosts):
        print "ARP verification on vlan interface passed"
    else:
        assert 0, "Failed to verify that the Proxy ARP funtionality on "\
                  "VLAN interface"

    clearARPTable(hosts[0], 'lnk01')
    if(enterBashShell(hosts[0]) is False):
        return False

    if (enterSWNameSpace(hosts[0]) is False):
        return False

    # Continuos ping, disable and enable proxy ARP.
    startBackgroundPingToOtherHosts(hosts[0])

    if(enterVtysh(hosts[0]) is False):
        return False

    if (verifyARPTable(dut01, hosts)):
        print "ARP verification on vlan interface passed"
    else:
        assert 0, "Failed to verify that the Proxy ARP funtionality on "\
                  "VLAN interface"

    # Disable Proxy ARP on L3 VLAN interface
    if (enterInterfaceContext(dut01, "vlan 3") is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="no ip proxy-arp")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Disabling Proxy ARP failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False
    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.vlan3.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.vlan3.proxy_arp = 0' in proxy_arp_state, "Failed to"\
        " verify Proxy ARP is disabled on vlan interface in kernel via sysctl"

    print "ARP table verification on Vlan interface after disabling"
    if(enterVtysh(dut01) is False):
        return False

    clearARPTable(hosts[0], 'lnk01')
    if(verifyARPTable(dut01, hosts)):
        assert 0, "Failed to verify that the Proxy ARP funtionality is "\
                  "disabled on VLAN interface"

    # enable Proxy ARP on L3 VLAN interface
    if (enterInterfaceContext(dut01, "vlan 3") is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="ip proxy-arp")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Enabling Proxy ARP failed"
    if (exitInterfaceContext(dut01) is False):
        return False

    if(enterBashShell(dut01) is False):
        return False
    out = dut01.DeviceInteract(command="sysctl net.ipv4.conf.vlan3.proxy_arp")
    proxy_arp_state = out.get('buffer')
    assert 'net.ipv4.conf.vlan3.proxy_arp = 1' in proxy_arp_state, "Failed to"\
        " verify Proxy ARP is enabled on vlan interface in kernel via sysctl"

    print "ARP table verification on Vlan interface after enabling"
    if(enterVtysh(dut01) is False):
        return False

    clearARPTable(hosts[0], 'lnk01')
    if(verifyARPTable(dut01, hosts)):
        print "ARP verification on vlan interface passed"
    else:
        assert 0, "Failed to verify that the Proxy ARP funtionality on "\
                  "VLAN interface"

    # Perform clear ARP with traffic running in background.
    clearARPTable(hosts[0], 'lnk01')
    if(verifyARPTable(dut01, hosts)):
        print "ARP verification on vlan interface passed"
    else:
        assert 0, "Failed to verify that the Proxy ARP funtionality on "\
                  "VLAN interface"

    clearARPTable(hosts[0], 'lnk01')
    if(verifyARPTable(dut01, hosts)):
        print "ARP verification on vlan interface passed"
    else:
        assert 0, "Failed to verify that the Proxy ARP funtionality on "\
               "VLAN interface"

    if (enterSWNameSpace(host[0]) is False):
        return False

    devIntRetStruct = hosts[0].DeviceInteract(command="killall -9 ping")

    if(enterVtysh(hosts[0]) is False):
        return False

    return True


def proxyARPonSubInterfaceTest(dut01):
    if (enterSWNameSpace(dut01) is False):
        return False

    # Try enable Proxy ARP on sub-interface
    if (enterInterfaceContext(dut01, "5.1") is False):
        return False
    devIntReturn = dut01.DeviceInteract(command="ip proxy-arp")
    if (exitInterfaceContext(dut01) is False):
        return False

    cmdOut = dut01.cmdVtysh(command="show interface 5.1")
    assert 'Proxy ARP is enabled' not in cmdOut, "Failed to validate the "\
        "absence of String 'Proxy ARP is enabled' in show interface output "\

    return True


@pytest.mark.skipif(True, reason="skipped test case due to gate job failures.")
class Test_proxyarp_feature:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        # Topology formation
        topoString = "dut01 "
        topoLinkString = ""
        topoFilterString = "dut01:system-category:switch, "

        for x in range(0, NO_OF_HOST):
            host_id = x + 1
            topoString += str("host0%d " % host_id)
            topoLinkString += str("lnk0%d:dut01:host0%d, "
                                  % (host_id, host_id))
            topoFilterString += str("host0%d:system-category:switch, "
                                    % host_id)

        # Removing the extra ', ' at the end of topoLink and topoFilter string.
        topoLinkString = topoLinkString[:-2]
        topoFilterString = topoFilterString[:-2]

        # Topology definition
        topoDict = {"topoExecution": 15000,
                    "topoTarget": topoString,
                    "topoDevices": topoString,
                    "topoLinks": topoLinkString,
                    "topoFilters": topoFilterString}

        Test_proxyarp_feature.testObj =\
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        # Get topology object
        Test_proxyarp_feature.topoObj = \
            Test_proxyarp_feature.testObj.topoObjGet()

    def teardown_class(cls):
        Test_proxyarp_feature.topoObj.terminate_nodes()

    def test_proxyARPOnL3Port(self):
        LogOutput('info', "\n### Test Proxy ARP on L3 port ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        hosts = []
        for x in range(0, NO_OF_HOST):
            host_id = x + 1
            host = str("host0%d" % host_id)
            hosts.append(self.topoObj.deviceObjGet(device=host))

        initial_configure(dut01Obj, hosts)
        retValue = proxyARPonL3PortTest(dut01Obj, hosts)
        if(retValue):
            LogOutput('info', "Proxy ARP on L3 port - passed")
        else:
            LogOutput('error', "Proxy ARP on L3 port - failed")

    def test_proxyARPOnIpChangeAndSecondaryIpConfiguredInterface(self):
        LogOutput('info', "\n### Test Proxy ARP on Ip Change And Secondary"
                  "IpConfiguredInterface ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        hosts = []
        for x in range(0, NO_OF_HOST):
            host_id = x + 1
            host = str("host0%d" % host_id)
            hosts.append(self.topoObj.deviceObjGet(device=host))

        retValue = proxyARPOnIpChangeAndSecondaryIpConfiguredInterfaceTest(
                                 dut01Obj, hosts)
        if(retValue):
            LogOutput('info', "Proxy ARP on Secondary IpConfigured "
                              "Interface - passed")
        else:
            LogOutput('info', "Proxy ARP on Secondary IpConfigured "
                              "Interface - failed")

    def test_proxyARPOnIpModificationIntfFlapWithTrafficInBackground(self):
        LogOutput('info', "\n### Test Proxy ARP on Ip Change With traffic in "
                  "background ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        hosts = []
        for x in range(0, NO_OF_HOST):
            host_id = x + 1
            host = str("host0%d" % host_id)
            hosts.append(self.topoObj.deviceObjGet(device=host))

        retValue = \
            proxyARPOnIpModificationAndInterfaceFlapWithTrafficInBackground(
                                 dut01Obj, hosts)
        if(retValue):
            LogOutput('info', "Proxy ARP on IP Modification with traffic in "
                              "Background - passed")
        else:
            LogOutput('info', "Proxy ARP on IP Modification with traffic in "
                              "Background - Failed")

    def test_proxyARPOnRoutingStatusModificationWithTrafficInBackground(self):
        LogOutput('info', "\n### Test Proxy ARP on Ip Change With traffic in "
                  "background ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        hosts = []
        for x in range(0, NO_OF_HOST):
            host_id = x + 1
            host = str("host0%d" % host_id)
            hosts.append(self.topoObj.deviceObjGet(device=host))

        retValue = proxyARPOnRoutingStatusModificationWithTrafficInBackground(
                                 dut01Obj, hosts)
        if(retValue):
            LogOutput('info', "Proxy ARP on Routing status Modification "
                              "with traffic in Background - passed")
        else:
            LogOutput('info', "Proxy ARP on Routing status Modification "
                              "with traffic in Background - Failed")

    def test_proxyARPOnMultipleReloadsWithTrafficInBackground(self):
        LogOutput('info', "\n### Test Proxy ARP on multiple reloads With "
                  "traffic in background ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        hosts = []
        for x in range(0, NO_OF_HOST):
            host_id = x + 1
            host = str("host0%d" % host_id)
            hosts.append(self.topoObj.deviceObjGet(device=host))

        retValue = proxyARPOnMultipleReloadsWithTrafficInBackground(
                                 dut01Obj, hosts)
        if(retValue):
            LogOutput('info', "Proxy ARP on  Multiple reloads "
                              "with traffic in Background - passed")
        else:
            LogOutput('info', "Proxy ARP on Multiple reloads "
                              "with traffic in Background - Failed")

    def test_proxyARPOnL2Port(self):
        LogOutput('info', "\n### Test Proxy ARP on L2 port ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")

        retValue = proxyARPonL2PortTest(dut01Obj)
        if(retValue):
            LogOutput('info', "Proxy ARP on L2 port - passed")
        else:
            LogOutput('error', "Proxy ARP on L2 port - failed")

    def test_proxyARPOnSplitParentPort(self):
        LogOutput('info', "\n### Test Proxy ARP on Split Parent port ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")

        retValue = proxyARPonSplitParentInterfaceTest(dut01Obj)
        if(retValue):
            LogOutput('info', "Proxy ARP on split parent interface - passed")
        else:
            LogOutput('error', "Proxy ARP on split parent interface - failed")

    def test_proxyARPOnSplitChildPort(self):
        LogOutput('info', "\n### Test Proxy ARP on Split child port ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")

        retValue = proxyARPonSplitChildInterfaceTest(dut01Obj)
        if(retValue):
            LogOutput('info', "Proxy ARP on split child interface - passed")
        else:
            LogOutput('error', "Proxy ARP on split child interface - failed")

    def test_proxyARPOnVLANInterface(self):
        LogOutput('info', "\n### Test Proxy ARP on VLAN Interface ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        hosts = []
        for x in range(0, NO_OF_HOST):
            host_id = x + 1
            host = str("host0%d" % host_id)
            hosts.append(self.topoObj.deviceObjGet(device=host))

        retValue = proxyARPonVLANInterfaceTest(dut01Obj, hosts)
        if(retValue):
            LogOutput('info', "Proxy ARP on VLAN interface - passed")
        else:
            LogOutput('error', "Proxy ARP on VLAN interface - failed")

    def test_proxyARPOnBulkAdditionAndTrafficInBackgroungOnVLANInterface(self):
        LogOutput('info', "\n### Test Proxy ARP on Bulk addition of VLAN "
                  "and Traffic in background ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        hosts = []
        for x in range(0, NO_OF_HOST):
            host_id = x + 1
            host = str("host0%d" % host_id)
            hosts.append(self.topoObj.deviceObjGet(device=host))

        retValue = proxyARPonVLANInterfaceTest(dut01Obj, hosts)
        if(retValue):
            LogOutput('info', "Proxy ARP on Bulk config addition for a "
                      "VLAN interface with traffic in background - passed")
        else:
            LogOutput('info', "Proxy ARP on Bulk config addition for a "
                      "VLAN interface with traffic in background - failed")

    def test_proxyARPOnSubInterface(self):
        LogOutput('info', "\n### Test Proxy ARP on sub-interface ###")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")

        retValue = proxyARPonSubInterfaceTest(dut01Obj)
        if(retValue):
            LogOutput('info', "Proxy ARP on Sub-interface - passed")
        else:
            LogOutput('error', "Proxy ARP on Sub-interface - failed")
