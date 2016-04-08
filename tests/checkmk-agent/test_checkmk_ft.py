#
# !/usr/bin/python
#
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

import os
import sys
import time
import pytest
import subprocess
import time
import re
import ast
from opsvsi.docker import *
from opsvsi.opsvsitest import *

NUM_OF_SWITCHES = 2
NUM_HOSTS_PER_SWITCH = 0

SWITCH = "s1"
OMD_SERVER = "s2"
OMD_IP = "9.0.0.1"
SWITCH_IP = "9.0.0.2"
NETMASK = "24"

INTERFACE = "1"
MAGICNO = "1234"

curlCmd = "curl -m 10"
viewURI = """\"http://127.0.0.1/default/check_mk/view.py?view_name=%s&_do_confirm=yes&_transid=-1&_do_actions=yes&output_format=JSON&_username=auto&_secret=secretpassword\""""
actionURI = """\"http://127.0.0.1/default/check_mk/webapi.py?action=%s&_username=auto&_secret=secretpassword&mode=%s\""""
svcInterfaceURI = """\"http://127.0.0.1/default/check_mk/view.py?view_name=service&service=Interface%201&host=%s\""""

CHECKMK_DEBUG = True
def checkmk_log(s):
    if CHECKMK_DEBUG:
        print s

OMD_DOCKER_IMAGE = 'openswitch/omd'

class OmdSwitch (DockerNode, Switch):
    def __init__(self, name, image=OMD_DOCKER_IMAGE, **kwargs):
        kwargs['nodetype'] = "OpsVsiHost"
        kwargs['init_cmd'] = DOCKER_DEFAULT_CMD
        super(OmdSwitch, self).__init__(name, image, **kwargs)
        self.inNamespace = True

    def start(self, controllers):
        pass

class myTopo(Topo):
    def build (self, hsts=0, sws=NUM_OF_SWITCHES, **_opts):

        self.hsts = hsts
        self.sws = sws

        self.addSwitch(SWITCH)
        self.addSwitch(name = OMD_SERVER, cls = OmdSwitch, **self.sopts)

class checkmkTest (OpsVsiTest):
    def setupNet (self):
        self.net = Mininet(topo=myTopo(hsts = NUM_HOSTS_PER_SWITCH,
                                       sws = NUM_OF_SWITCHES,
                                       hopts = self.getHostOpts(),
                                       sopts = self.getSwitchOpts()),
                                       switch = VsiOpenSwitch,
                                       host = OpsVsiHost,
                                       link = OpsVsiLink,
                                       controller = None,
                                       build = True)

    def configure (self):
        for switch in self.net.switches:
            if isinstance(switch, VsiOpenSwitch):
                switch.cmdCLI("configure terminal")
                switch.cmdCLI("interface %s" % INTERFACE)
                switch.cmdCLI("no shutdown")
                switch.cmdCLI("ip address %s/%s" % (SWITCH_IP, NETMASK)),
                switch.cmdCLI("exit")
                '''
                result = switch.cmd("ovs-vsctl list Interface %s" % INTERFACE)
                mac = re.findall('lnx_if\:sep\(58\)\>\>\>(.*)\<\<\<ovs_bonding', result, re.DOTALL)

                switch.cmdCLI("ovs-vsctl set interface %s statistics:tx_packets=%s", (INTERFACE, MAGICNO))
                switch.cmdCLI("ovs-vsctl set interface %s statistics:tx_bytes=%s", (INTERFACE, MAGICNO))
                switch.cmdCLI("ovs-vsctl set interface %s statistics:rx_packets=%s", (INTERFACE, MAGICNO))
                switch.cmdCLI("ovs-vsctl set interface %s statistics:rx_bytes=%s", (INTERFACE, MAGICNO))
                switch.cmdCLI("ovs-vsctl set interface %s statistics:rx_errors=%s", (INTERFACE, MAGICNO))
                switch.cmdCLI("ovs-vsctl set interface %s statistics:tx_errors=%s", (INTERFACE, MAGICNO))
                '''

    def checkmk_omdRunning(self):
        omd = False
        apache = False
        for switch in self.net.switches:
            if isinstance(switch, OmdSwitch):
                cmd = "service apache2 status"
                checkmk_log(cmd)
                result = switch.cmd(cmd)
                checkmk_log(result)
                match = re.search(r'running', result)
                if match is not None:
                    apache = True

                cmd = "netstat -plnt | grep ':80'"
                checkmk_log(cmd)
                result = switch.cmd(cmd)
                checkmk_log(result)
                match = re.search(r'LISTEN', result)
                if match is None:
                    apache = False

                cmd = "omd status"
                checkmk_log(cmd)
                result = switch.cmd(cmd)
                checkmk_log(result)
                for line in result.splitlines():
                    if "Overall state" in line:
                        checkmk_log(line)
                        match1 = re.search(r'running', line)
                        match2 = re.search(r'partially', line)
                        if match1 is not None and match2 is None:
                            omd = True

        return omd and apache

    def checkmk_omdRestart (self):
        for switch in self.net.switches:
            if isinstance(switch, OmdSwitch):
                cmd = "service apache2 stop"
                checkmk_log(cmd)
                result = switch.cmd(cmd)
                cmd = "killall -9 apache2"
                checkmk_log(cmd)
                result = switch.cmd(cmd)
                cmd = "service apache2 start"
                checkmk_log(cmd)
                result = switch.cmd(cmd)
                checkmk_log(result)
                cmd = "omd restart"
                checkmk_log(cmd)
                result = switch.cmd(cmd)
                checkmk_log(result)

    def checkmk_getIPs (self):
        for switch in self.net.switches:
            result = switch.cmd("ifconfig eth0")
            ipAddrs = re.findall(r'[0-9]+(?:\.[0-9]+){3}', result)
            for ipAddr in ipAddrs:
                if ipAddr != '0.0.0.0' and not re.match("255", ipAddr):
                    break
            if isinstance(switch, VsiOpenSwitch):
                self.switchIpAddr = ipAddr
            elif isinstance(switch, OmdSwitch):
                self.omdIpAddr = ipAddr

        checkmk_log("Switch Mgmt IP is %s, OMD Server IP is %s" % (self.switchIpAddr, self.omdIpAddr))

    def checkmk_addHost(self):
        for switch in self.net.switches:
            if isinstance(switch, OmdSwitch):
                args = [curlCmd, """-d 'request={"hostname": "%s", "folder": "os/linux"}'""" % self.switchIpAddr, actionURI % ("add_host", "none")]
                checkmk_log(args)
                result = switch.cmd(args)
                checkmk_log(result)
                match = re.search(r'Site Not Started', result)
                if match is not None:
                    return False
                else:
                    return True

    def checkmk_discover(self):
        for switch in self.net.switches:
            if isinstance(switch, OmdSwitch):
                args = [curlCmd, """-d 'request={"hostname": "%s"}'""" % self.switchIpAddr, actionURI % ("discover_services", "new")]
                checkmk_log(args)
                result = switch.cmd(args)
                checkmk_log(result)
                match = re.search(r'Service discovery successful', result)
                if match is None:
                    return False

                args = [curlCmd, actionURI % ("activate_changes", "all")]
                checkmk_log(args)
                result = switch.cmd(args)
                checkmk_log(result)
                match = re.search(r'Site Not Started', result)
                if match is not None:
                    return False

                ctr = 0
                up = False
                while not up and ctr < 10:
                    hosts = self.checkmk_getHosts()
                    checkmk_log(hosts)
                    for host in hosts:
                        checkmk_log(host)
                        if host["host"] == self.switchIpAddr \
                            and host["host_state"] == 'UP':
                            up = True
                            break
                    if not up:
                        ctr += 1
                        sleep(1)

                if up:
                    return True
                else:
                    return False

    def checkmk_getHosts(self):
        hosts = []
        for switch in self.net.switches:
            if isinstance(switch, OmdSwitch):
                args = [curlCmd, viewURI % "allhosts"]
                checkmk_log(args)
                resultStr = switch.cmd(args)
                checkmk_log(resultStr)
                match = re.search(r'Site Not Started', resultStr)
                if match is None:
                    result = ast.literal_eval(resultStr)
                    for row in result[1:]:
                        host = {}
                        host["host"] = row[1]
                        host["host_state"] = row[0]
                        hosts.append(host)
                return hosts
                '''
                for hostInfo in result:
                    if any(x == self.switchIpAddr for x in hostInfo):
                        checkmk_log(hostInfo)
                '''

    def checkmk_getSvcAll(self):
        for switch in self.net.switches:
            if isinstance(switch, OmdSwitch):
                args = [curlCmd, viewURI % "svcbyhgroups"]
                checkmk_log(args)
                resultStr = switch.cmd(args)
                result = ast.literal_eval(resultStr)
                return result

    def checkmk_verifyIfStats(self):
        for switch in self.net.switches:
            if isinstance(switch, OmdSwitch):
                ok = False
                cntr = 0
                while not ok and cntr < 300:
                    print "-----------------------------"
                    print cntr
                    svcs = self.checkmk_getSvcAll()
                    for svc in svcs:
                        print svc[0], svc[1], svc[2]
                        if svc[1] == self.switchIpAddr \
                            and svc[2] == 'Interface %s' % INTERFACE:
                            print svc
                            if svc[0] == 'OK' or svc[0] == 'PEND':
                                ok = True
                            break
                    sleep(1)
                    cntr += 1

@pytest.mark.skipif(True, reason="skipped test case due to random gate job failures.")
@pytest.mark.timeout(0)
class Test_checkmk_basic_setup:
    def setup (self):
        pass

    def teardown (self):
        pass

    def setup_class (cls):
        Test_checkmk_basic_setup.test_var = checkmkTest()

    def teardown_class (cls):
        Test_checkmk_basic_setup.test_var.net.stop()

    def setup_method (self, method):
        pass

    def teardown_method (self, method):
        pass

    def __del__ (self):
        del self.test_var

    def test_run (self):
        self.test_var.configure()
        self.test_var.checkmk_getIPs()
        run = 0
        while True:
            run += 1
            sleep(20)
            if self.test_var.checkmk_omdRunning():
                if self.test_var.checkmk_addHost():
                    if self.test_var.checkmk_discover():
                        self.test_var.checkmk_verifyIfStats()
                        break
            if run <= 3:
                checkmk_log("restart OMD")
                self.test_var.checkmk_omdRestart()
            else:
                assert(False)
