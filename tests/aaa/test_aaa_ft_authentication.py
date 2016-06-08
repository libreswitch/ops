#!/usr/bin/env python
# Copyright (C) 2015-2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from smart import Error, _
from smart.util import pexpect

from time import sleep
import pytest

from opsvsi.docker import *
from opsvsi.opsvsitest import *

SSHCLIENT = "/usr/bin/ssh -q -o UserKnownHostsFile=/dev/null \
             -o StrictHostKeyChecking=no"

# Purpose of this test is to test switch authentication
# with local credentials and RADIUS credentials.

class myTopo(Topo):
    """Custom Topology Example
    H1[h1-eth0]<--->[1]S1
    """

    def build(self, hsts=1, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws

        "add list of hosts"
        for h in irange(1, hsts):
            host = self.addHost('h%s' % h)

        "add list of switches"
        for s in irange(1, sws):
            switch = self.addSwitch('s%s' % s)
        "Add links between nodes based on custom topo"
        self.addLink('h1', 's1')

class aaaFeatureTest(OpsVsiTest):
    def setupRadiusserver(self):
        ''' This function is to setup radius server in the ops-host image
        '''
        h1 = self.net.hosts[0]
        switchIP = self.getSwitchIP()
        print "SwitchIP:" + switchIP
        out = h1.cmd("sed -i '76s/steve/netop/' /etc/freeradius/users")
        out = h1.cmd("sed -i '76s/#netop/netop/' /etc/freeradius/users")
        out = h1.cmd("sed -i '196s/192.168.0.0/"+switchIP+"/' "
                     "/etc/freeradius/clients.conf")
        out = h1.cmd("sed -i '196,199s/#//' /etc/freeradius/clients.conf")

        h1.cmd("service freeradius stop")
        sleep(1)
        out = h1.cmd("service freeradius start")
        assert ('fail') not in out, \
            "Failed to start freeradius on host"

        info('Configured radius server on host\n')

    def setupRadiusclient(self):
        ''' This function is to setup radius client in the switch
        '''
        s1 = self.net.switches[0]
        host_1_IpAddress = self.getHostIP_1()
        print "Radius Server:" + host_1_IpAddress
        s1.cmd("mkdir /etc/raddb/")
        s1.cmd("touch /etc/raddb/server")
        sleep(1)
        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out), \
            "Failed to enter configuration terminal"

        sleep(1)
        s1.cmdCLI("radius-server host " + host_1_IpAddress)
        s1.cmdCLI("radius-server timeout 1")
        s1.cmdCLI("radius-server retries 0")
        s1.cmdCLI("exit")
        info('Configured radius client on switch\n')

    def setupNet(self):
        # Create a topology with single Openswitch and
        # host.

        # Select ops-host image from docker hub, which has freeradius
        # installed.
        self.setHostImageOpts("host/freeradius-ubuntu")

        topo = myTopo(hsts=1, sws=1, hopts=self.getHostOpts(),
                      sopts=self.getSwitchOpts(), switch=VsiOpenSwitch,
                      host=OpsVsiHost, link=OpsVsiLink, controller=None,
                      build=True)

        self.net = Mininet(topo, switch=VsiOpenSwitch, host=OpsVsiHost,
                           link=OpsVsiLink, controller=None, build=True)
        self.setupRadiusserver()
        self.setupRadiusclient()

    def getSwitchIP(self):
        ''' This function is to get switch IP addess
        '''
        s1 = self.net.switches[0]
        out = s1.cmd("ifconfig eth0")
        switchIpAddress = out.split("\n")[1].split()[1][5:]
        return switchIpAddress

    def getHostIP_1(self):
        ''' This function is to get host IP addess
        '''
        h1 = self.net.hosts[0]
        out = h1.cmd("ifconfig eth0")
        host_1_IpAddress = out.split("\n")[1].split()[1][5:]
        return host_1_IpAddress

    def localAuthEnable(self):
        ''' This function is to enable local authentication in DB
        with CLI command'''
        s1 = self.net.switches[0]
        out = ""
        out += s1.cmd("echo ")
        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out), \
            "Failed to enter configuration terminal"

        out += s1.cmd("echo ")
        out = s1.cmdCLI("aaa authentication login local")
        assert ('Unknown command' not in out), "Failed to enable local" \
                                               " authentication"
        out += s1.cmd("echo ")
        s1.cmdCLI("exit")
        return True

    def radiusAuthEnable(self, chap=False):
        ''' This function is to enable radius authentication in DB
        with CLI command'''
        s1 = self.net.switches[0]

        out = ""
        out += s1.cmd("echo ")
        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out),  \
            "Failed to enter configuration terminal"

        if chap:
            out += s1.cmd("echo ")
            out = s1.cmdCLI("aaa authentication login radius radius-auth chap")
            assert ('Unknown command' not in out), "Failed to set chap" \
                                               " for radius"
        else:
            out += s1.cmd("echo ")
            out = s1.cmdCLI("aaa authentication login radius")
            assert ('Unknown command' not in out), "Failed to enable radius" \
                                                   " authentication"

        out += s1.cmd("echo ")
        s1.cmdCLI("exit")
        return True

    def noFallbackEnable(self):
        ''' This function is to disable fallback to local in DB
        with CLI command'''
        s1 = self.net.switches[0]

        out = ""
        out += s1.cmd("echo ")
        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out), \
            "Failed to enter configuration terminal"

        out += s1.cmd("echo ")
        out = s1.cmdCLI("no aaa authentication login fallback error local")
        assert ('Unknown command' not in out),  \
            "Failed to disable fallback to local authentication"

        out += s1.cmd("echo ")
        s1.cmdCLI("exit")
        return True

    def FallbackEnable(self):
        ''' This function is to enable fallback to local in DB
        with CLI command'''
        s1 = self.net.switches[0]

        out = ""
        out += s1.cmd("echo ")
        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out),  \
            "Failed to enter configuration terminal"

        out += s1.cmd("echo ")
        out = s1.cmdCLI("aaa authentication login fallback error local")
        assert ('Unknown command' not in out), "Failed to enable fallback to" \
                                               " local authentication"

        s1.cmdCLI("exit")
        return True

    def loginSSHlocal(self):
        '''This function is to verify local authentication is successful when
        radius is false and fallback is true'''
        info('########## Test to verify SSH login with local authenication '
             'enabled ##########\n')
        s1 = self.net.switches[0]
        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        info(".### switchIpAddress: " + switchIpAddress + " ###\n")
        info(".### Running configuration ###\n")
        run = s1.cmdCLI("show running-config")
        print run
        out = ""
        out += s1.cmd("echo ")
        myssh = SSHCLIENT + " netop@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('netop')
            j = p.expect(['#', 'password:'])
            if j == 0:
                p.sendline('exit')
                p.kill(0)
                info(".### Passed SSH login with local credenticals ###\n")
                return True
            if j == 1:
                p.sendline('dummypassword')
                p.expect('password:')
                p.sendline('dummypasswordagain')
                p.kill(0)
                assert j != 1, "Failed to authenticate with local password"
        elif i == 2:
            assert i != 2, "Failed with SSH command"

    def loginSSHradius(self, chap=False):
        '''This function is to verify radius authentication is successful when
        radius is true and fallback is false'''
        info('########## Test to verify SSH login with radius authentication '
             'enabled and fallback disabled ##########\n')
        s1 = self.net.switches[0]
        self.noFallbackEnable()
        sleep(5)
        self.radiusAuthEnable(chap)
        sleep(5)
        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        info(".###switchIpAddress: " + switchIpAddress + " ###\n")
        info(".### Running configuration ###\n")
        run = s1.cmdCLI("show running-config")
        print run

        out = ""
        out += s1.cmd("echo ")
        myssh = SSHCLIENT + " netop@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('testing')
        elif i == 2:
            assert i != 2, "Failed with SSH command"
        loginpass = p.expect(['password:', '#'])
        if loginpass == 0:
            p.sendline('dummypassword')
            p.expect('password:')
            p.sendline('dummypasswordagain')
            p.kill(0)
            assert loginpass != 0, "Failed to login via radius authentication"
        if loginpass == 1:
            p.sendline('exit')
            p.kill(0)
            if chap:
                info(".### Passed SSH login with radius authentication and"
                     " chap ###\n")
            else:
                info(".### Passed SSH login with radius authentication ###\n")
            return True

    def loginSSHradiusWithFallback(self):
        ''' This function is to verify radius authentication when fallback is
        enabled. Login with local password should work when raddius server is
        un reachable'''
        info('########## Test to verify SSH login with radius authenication'
             ' enabled and fallback Enabled ##########\n')
        s1 = self.net.switches[0]
        h1 = self.net.hosts[0]
        self.FallbackEnable()
        # self.checkAccessFiles()
        h1.cmd("service freeradius stop")

        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        info(".###switchIpAddress: " + switchIpAddress + " ###\n")
        info(".### Running configuration ###\n")
        run = s1.cmdCLI("show running-config")
        print run
        out = ""
        out += s1.cmd("echo ")
        myssh = SSHCLIENT + " netop@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('Testing')
        elif i == 2:
            assert i != 2, "Failed with SSH command"
        loginpass = p.expect(['password:', '#'])
        if loginpass == 0:
            p.sendline('netop')
            p.expect('#')
            p.sendline('exit')
            p.kill(0)
            info(".### Passed authentication with local password when radius"
                 " server not reachable and fallback enabled ###\n")
            return True
        if loginpass == 1:
            p.sendline('exit')
            p.kill(0)
            assert loginpass != 1, "Failed to validate radius authetication" \
                                   " when server is not reachable"

class Test_aaafeature:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_aaafeature.test = aaaFeatureTest()
        pass

    def teardown_class(cls):
    # Stop the Docker containers, and
    # mininet topology
        Test_aaafeature.test.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test

    def test_loginSSHlocal(self):
        self.test.loginSSHlocal()

    def test_loginSSHradius(self):
        self.test.loginSSHradius()
        self.test.loginSSHradius(chap=True)

    def test_loginSSHradiusWithFallback(self):
        self.test.loginSSHradiusWithFallback()
