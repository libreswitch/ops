#!/usr/bin/env python
# (c) Copyright 2015 - 2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os
import sys
import time
import re
from mininet.net import *
from mininet.topo import *
from mininet.node import *
from mininet.link import *
from mininet.cli import *
from mininet.log import *
from mininet.util import *
from subprocess import *
from opsvsi.docker import *
from opsvsi.opsvsitest import *
import select
import pytest


class mgmtIntfTests(OpsVsiTest):
    # This class member is used for retaining
    # IPv4 and it's subnet mask which is obtained from DHCP server.
    Dhcp_Ipv4_submask = ''

    # DHCP dhclient is currently not running on VSI image due to
    # dhclient_apparmor_profile [/etc/apparmor.d/sbin.dhclient] file,
    # which is present on running host machine[VM].
    # The Profile files will declare access rules to allow access to
    # linux system resources. Implicitly the access is denied
    # when there is no matching rule in the profile.
    # If we want to run docker instance with dhclient on such a
    # host machine, we have to disable the dhclient_apparmor_profile file
    # and enable it once testcase execution is finished.

    def disable_dhclient_profile(self):
        if os.path.isfile("/etc/apparmor.d/sbin.dhclient") is True:
            os.system("sudo ln -s /etc/apparmor.d/sbin.dhclient "
                      "  /etc/apparmor.d/disable/")
            os.system('sudo apparmor_parser -R /etc/apparmor.d/sbin.dhclient')

    def enable_dhclient_profile(self):
        if os.path.isfile("/etc/apparmor.d/sbin.dhclient") is True:
            os.system('sudo rm /etc/apparmor.d/disable/sbin.dhclient')
            os.system('sudo apparmor_parser -r /etc/apparmor.d/sbin.dhclient')

    # When we run this test file with multiple instance,there is a chance of
    # asynchronously enabling and disabling dhclient_profile file on the
    # running system.
    # To avoid asynchronous issue, the count variable is used to maintain
    # the number of mgmt-intf test file execution instance in a temp file.
    # whenever the count reaches zero, the profile file is enabled again.
    def file_read_for_mgmt_instance_count(self):
        file_fd = open('mgmt_sys_var', 'r')
        count = file_fd.read()
        count = re.search('\d+', count)
        num = int(count.group(0))
        file_fd.close()
        return num

    def file_write_for_mgmt_instance_count(self, count_number):
        file_fd = open('mgmt_sys_var', 'w+')
        file_fd.write(str(count_number))
        file_fd.close()

    def setupNet(self):
        if os.path.exists('mgmt_sys_var') is False:
            self.file_write_for_mgmt_instance_count(0)
        else:
            count = self.file_read_for_mgmt_instance_count()
            num = count + 1
            self.file_write_for_mgmt_instance_count(num)

        self.disable_dhclient_profile()

        # If you override this function, make sure to
        # either pass getNodeOpts() into hopts/sopts of the topology that
        # you build or into addHost/addSwitch calls.
        mgmt_topo = SingleSwitchTopo(k=0,
                                     hopts=self.getHostOpts(),
                                     sopts=self.getSwitchOpts())
        self.net = Mininet(topo=mgmt_topo,
                           switch=VsiOpenSwitch,
                           host=Host,
                           link=OpsVsiLink, controller=None,
                           build=True)

    def numToDottedQuad(self, n):
        d = 256 * 256 * 256
        q = []
        while d > 0:
            m, n = divmod(n, d)
            q.append(str(m))
            d = d/256
        return '.'.join(q)

    # DHCP client started on management interface.
    def dhclient_started_on_mgmt_intf_ipv4(self):
        s1 = self.net.switches[0]
        cnt = 15
        output_tmp = ''
        output = ''
        while cnt:
            output = s1.cmd("systemctl status dhclient@eth0.service -l")
            output_tmp = s1.cmd("ifconfig eth0")
            output_log = s1.cmd("cat /var/log/messages | grep \"dhclient\" ")
            if output in 'running':
                break
            else:
                cnt -= 1
                sleep(1)

        info("DHCLIENT status debug info : %s\n" % (output))
        info("Mgmt port status debug info : %s\n" % (output_tmp))
        info("SYSLOG output : %s\n" % (output_log))
        assert 'running' in output, "Test to verify dhcp client has"\
            " started failed"
        info('### Successfully verified dhcp client has started ###\n')

    # Mgmt Interface updated during bootup.
    def mgmt_intf_updated_during_bootup(self):
        s1 = self.net.switches[0]
        output = s1.ovscmd("ovs-vsctl list system")
        output += s1.cmd("echo")
        assert 'name=eth0' in output, "Test to mgmt interface has "\
            " updated from image.manifest file failed"
        info("### Successfully verified mgmt interface"
             " has updated from image.manifest file ###\n")

    # Set mode as DHCP.
    def dhcp_mode_set_on_mgmt_intf(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("end")
        s1.cmdCLI("configure terminal")
        s1.cmdCLI("interface mgmt")
        s1.cmdCLI("ip dhcp")
        output = s1.cmdCLI(" ")
        cnt = 15
        tmp = []
        while cnt:
            output = s1.cmdCLI("do show interface mgmt")
            output += s1.cmdCLI(" ")
            tmp = re.findall("IPv4 address/subnet-mask\s+: \d+.\d+.\d+."
                             "\d+/.\d+", output)
            if tmp:
                break
            else:
                sleep(1)
                cnt -= 1
        self.Dhcp_Ipv4_submask = re.findall("\d+.\d+.\d+.\d+/.\d+",
                                            tmp[0])[0].split("/")
        assert 'dhcp' in output, 'Test to set mode as DHCP failed'
        output = s1.cmd("systemctl status dhclient@eth0.service")
        assert 'running' in output, 'Test to set mode as DHCP failed'
        info('### Successfully configured DHCP mode ###\n')

    # Static IP config when mode is static.
    def config_ipv4_on_mgmt_intf_static_mode(self):
        s1 = self.net.switches[0]
        IPV4_static = re.sub('\d+$', '128', self.Dhcp_Ipv4_submask[0])
        s1.cmdCLI("ip static "+IPV4_static+"/"+self.Dhcp_Ipv4_submask[1])
        output = s1.cmdCLI(" ")
        cnt = 30
        while cnt:
            output = s1.cmdCLI("do show interface mgmt")
            output += s1.cmd("echo")
            output += s1.cmd("echo")
            if IPV4_static in output and self.Dhcp_Ipv4_submask[1] in output:
                cnt2 = 15
                while cnt2:
                    output = s1.cmd("ifconfig")
                    output += s1.cmd("echo")
                    if IPV4_static in output and\
                       self.Dhcp_Ipv4_submask[1] in output:
                        break
                    else:
                        cnt2 -= 1
                        sleep(1)
                break
            else:
                sleep(1)
                cnt -= 1
        assert IPV4_static in output,\
            'Test to add static IP address in static mode failed'
        subnet = (1 << 32) - (1 << 32 >> int(self.Dhcp_Ipv4_submask[1]))
        assert self.numToDottedQuad(subnet) in output,\
            'Test to add static IP address in static mode failed'
        info("### Successfully configured static"
             " IP address in static mode ###\n")

    # Add Default gateway in Static mode.
    def config_ipv4_default_gateway_static_mode(self):
        s1 = self.net.switches[0]
        IPV4_default = re.sub('\d+$', '130', self.Dhcp_Ipv4_submask[0])
        s1.cmdCLI("default-gateway "+IPV4_default)
        output = s1.cmdCLI(" ")
        cnt = 15
        while cnt:
            output = s1.cmdCLI("do show interface mgmt")
            output += s1.cmd("echo")
            output += s1.cmd("echo")
            if IPV4_default in output:
                cnt2 = 15
                while cnt2:
                    output = s1.cmd("ip route show")
                    output += s1.cmd("echo")
                    if IPV4_default in output:
                        break
                    else:
                        cnt2 -= 1
                        sleep(1)
                break
            else:
                sleep(1)
                cnt -= 1
        assert IPV4_default in output,\
            "Test to add Default gateway in static mode failed"
        info("### Successfully configured Default gateway"
             " in static mode ###\n")

    # Remove Default gateway in static mode.
    def unconfig_ipv4_default_gateway_static_mode(self):
        s1 = self.net.switches[0]
        IPV4_default = re.sub('\d+$', '130', self.Dhcp_Ipv4_submask[0])
        s1.cmdCLI("no default-gateway "+IPV4_default)
        output = s1.cmdCLI(" ")
        output = s1.cmdCLI("do show interface mgmt")
        output += s1.cmdCLI(" ")
        temp = re.findall("Default gateway\s+: "+IPV4_default, output)
        buf = ''
        if temp:
            buf = ' '
        assert buf in output, 'Test to remove default gateway failed'
        cnt2 = 15
        while cnt2:
            output = s1.cmd("ip route show")
            output += s1.cmd("echo")
            if IPV4_default not in output:
                break
            else:
                cnt2 -= 1
                sleep(1)
        assert IPV4_default not in output,\
            'Test to remove default gateway failed'
        info('### Successfully Removed Default gateway in static mode ###\n')

    # Configure Secondary DNS Server in static mode.
    def config_secondary_ipv4_dns_static_mode(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("nameserver 10.10.10.4 10.10.10.5")
        cnt = 15
        while cnt:
            output = s1.cmdCLI("do show interface mgmt")
            output += s1.cmd("echo")
            output += s1.cmd("echo")
            if re.findall("Primary Nameserver\s+: 10.10.10.4", output) and \
               re.findall("Secondary Nameserver\s+: 10.10.10.5", output):
                cnt2 = 15
                while cnt2:
                    output = s1.cmd("cat /etc/resolv.conf")
                    output += s1.cmd("echo")
                    if 'nameserver 10.10.10.5' in output\
                       and 'nameserver 10.10.10.4' in output:
                        break
                    else:
                        cnt2 -= 1
                        sleep(1)
                break
            else:
                sleep(1)
                cnt -= 1
        assert '10.10.10.5' in output, 'Test to add Secondary DNS failed'
        assert '10.10.10.4' in output, 'Test to add Secondary DNS failed'
        info('### Successfully Configured Secondary DNS in static mode ###\n')

    # Remove Secondary DNS ipv4 in static mode.
    def unconfig_secondary_ipv4_dns_static_mode(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("no nameserver  10.10.10.4 10.10.10.20")
        cnt = 15
        while cnt:
            output = s1.cmdCLI("do show interface mgmt")
            output += s1.cmd("echo")
            output += s1.cmd("echo")
            if '10.10.10.20' not in output:
                cnt2 = 15
                while cnt2:
                    output = s1.cmd("cat /etc/resolv.conf")
                    output += s1.cmd("echo")
                    if 'nameserver 10.10.10.20' not in output:
                        break
                    else:
                        cnt2 -= 1
                        sleep(1)
                break
            else:
                sleep(1)
                cnt -= 1
        assert '10.10.10.20' not in output,\
               'Test to Remove Secondary DNS failed'
        info('### Successfully Removed Secondary DNS in static mode ###\n')

    # Add Default gateway IPV6 in DHCP mode.
    def config_default_gateway_ipv6_dhcp_mode(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("end")
        s1.cmdCLI("configure terminal")
        s1.cmdCLI("interface mgmt")
        s1.cmdCLI("ip dhcp")
        s1.cmdCLI("default-gateway 2001:db8:0:1::128")
        output = s1.cmdCLI(" ")
        output = s1.cmdCLI("do show interface mgmt")
        assert '2001:db8:0:1::128' not in output,\
               "Test to add default gateway in DHCP mode failed"
        info("### Successfully verified "
             "configure of default gateway in DHCP mode ###\n")

    # Static IPV6 config when mode is static.
    def config_ipv6_on_mgmt_intf_static_mode(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("ip static 2001:db8:0:1::156/64")
        output = s1.cmdCLI(" ")
        cnt = 15
        while cnt:
            output = s1.cmdCLI("do show interface mgmt")
            output += s1.cmd("echo")
            output += s1.cmd("echo")
            if '2001:db8:0:1::156/64' in output:
                cnt2 = 15
                while cnt2:
                    output = s1.cmd("ip -6 addr show dev eth0")
                    output += s1.cmd("echo")
                    if '2001:db8:0:1::156/64' in output:
                        break
                    else:
                        cnt2 -= 1
                        sleep(1)
                break
            else:
                sleep(1)
                cnt -= 1
        assert '2001:db8:0:1::156/64' in output,\
               'Test to add static IP address failed'
        info('### Successfully verified configure of Static IP ###\n')

    # Default gateway should be reachable. Otherwise test case will fail.
    # Add Default gateway in Static mode.
    def config_ipv6_default_gateway_static_mode(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("default-gateway 2001:db8:0:1::128")
        output = s1.cmdCLI(" ")
        output = s1.cmdCLI("do show running-config")
        assert 'default-gateway 2001:db8:0:1::128' in output,\
               'Test to add default gateway in static mode failed'
        info("### Successfully verified configure of default"
             " gateway in static mode ###\n")

    # Remove Default gateway in static mode.
    def unconfig_ipv6_default_gateway_static_mode(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("no default-gateway 2001:db8:0:1::128")
        output = s1.cmdCLI(" ")
        output = s1.cmdCLI("do show running-config")
        assert 'default-gateway 2001:db8:0:1::128' not in output,\
               'Test to remove default gateway in static mode failed'
        info('### Successfully Removed Default gateway in static mode ###\n')

    # Add DNS Server 2 in static mode.
    def config_secondary_ipv6_dns_static_mode(self):
        s1 = self.net.switches[0]
        output = s1.cmdCLI("nameserver 2001:db8:0:1::150 2001:db8:0:1::156")
        cnt = 15
        while cnt:
            output_show = s1.cmdCLI("do show interface mgmt")
            output_show += s1.cmdCLI(" ")
            if re.findall("Primary Nameserver\s+: 2001:db8:0:1::150",
               output_show) and re.findall("Secondary Nameserver\s+: 2001:"
                                           "db8:0:1::156", output_show):
                cnt2 = 15
                while cnt2:
                    output = s1.cmd("cat /etc/resolv.conf")
                    output += s1.cmd("echo")
                    if 'nameserver 2001:db8:0:1::156' in output and \
                       'nameserver 2001:db8:0:1::150' in output:
                        break
                    else:
                        cnt2 -= 1
                        sleep(1)
                break
            else:
                sleep(1)
                cnt -= 1
        assert '2001:db8:0:1::156' in output,\
            'Test to add Secondary DNS in static mode failed'
        assert '2001:db8:0:1::150' in output,\
            'Test to add Secondary DNS in static mode failed'
        info('### Successfully Configured Secondary DNS in static mode ###\n')

    # Remove DNS server 2.
    def unconfig_secondary_ipv6_dns_static_mode(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("no nameserver  2001:db8:0:1::150 2001:db8:0:1::154")
        cnt = 15
        while cnt:
            output_show = s1.cmdCLI("do show interface mgmt")
            output_show += s1.cmdCLI(" ")
            if '2001:db8:0:1::154' not in output_show:
                cnt2 = 15
                while cnt2:
                    output = s1.cmd("cat /etc/resolv.conf")
                    output += s1.cmd("echo")
                    if 'nameserver 2001:db8:0:1::154' not in output:
                        break
                    else:
                        cnt2 -= 1
                        sleep(1)
                break
            else:
                sleep(1)
                cnt -= 1
        assert '2001:db8:0:1::154' not in output,\
            'Test to Remove Secondary DNS in static mode failed'
        info('### Successfully Removed Secondary DNS in static mode ###\n')

    # Change mode from static to dhcp.
    def change_mode_from_static_to_dhcp_ipv6(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("ip dhcp")
        output = s1.cmdCLI(" ")
        time.sleep(5)
        output = ''
        output = s1.cmdCLI("do show interface mgmt")
        output += s1.cmdCLI(" ")
        assert 'dhcp' in output,\
            'Test to change mode from static to dhcp failed'
        output = s1.ovscmd("ovs-vsctl list system")
        output += s1.cmd("echo")
        assert 'ipv6_linklocal' in output,\
            'Test to change mode from static to dhcp failed'
        assert 'dns-server-1' not in output,\
            'Test to change mode from static to dhcp failed'
        assert 'dns-server-2' not in output,\
            'Test to change mode from static to dhcp failed'
        info('### Successfully changed mode to DHCP from static ###\n')

    # Verify to configure system hostname through CLI
    def config_set_hostname_from_cli(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("config terminal")
        s1.cmdCLI("hostname cli")
        cnt = 15
        while cnt:
            cmd_output = s1.ovscmd("ovs-vsctl list system")
            hostname = s1.ovscmd("ovs-vsctl get system . "
                                 "hostname").rstrip('\r\n')
            output = s1.cmd("uname -n")
            if "hostname=cli" in cmd_output and \
               hostname == "cli" and \
               "cli" in output:
                break
            else:
                cnt -= 1
                sleep(1)
        assert 'hostname=cli' in cmd_output and \
               hostname == 'cli' and \
               'cli' in output,\
               "Test to set hostname through CLI"\
               " has failed"
        info("### Successfully verified configuring"
             " hostname using CLI ###\n")

    # Verify to set hostname through dhclient
    def set_hostname_by_dhclient(self):
        s1 = self.net.switches[0]
        s1.cmd("dhcp_options open-vswitch-new None None None")
        cnt = 15
        while cnt:
            cmd_output = s1.ovscmd("ovs-vsctl list system")
            output = s1.cmd("uname -n")
            if "dhcp_hostname=open-vswitch-new" in cmd_output:
                break
            else:
                cnt -= 1
                sleep(1)
        assert 'dhcp_hostname=open-vswitch-new' in cmd_output,\
            "Test to set system hostname through dhclient"\
            " has failed"
        info("### Successfully verified to set system hostname"
             " by dhclient ###\n")

    # Verify to configure system domainname through CLI
    def config_set_domainname_from_cli(self):
        s1 = self.net.switches[0]
        s1.cmdCLI("config terminal")
        s1.cmdCLI("domain-name cli")
        cnt = 15
        while cnt:
            cmd_output = s1.ovscmd("ovs-vsctl list system")
            domainname = s1.ovscmd("ovs-vsctl get system . "
                                   "domain_name").rstrip('\r\n')
            if "domain_name=cli" in cmd_output and \
               domainname == "cli":
                break
            else:
                cnt -= 1
                sleep(1)
        assert 'domain_name=cli' in cmd_output and \
               domainname == 'cli' and \
               "Test to set domainname through CLI"\
               " has failed"
        info("### Successfully verified configuring"
             " domainname using CLI ###\n")

    # Verify to set domainname through dhclient
    def set_domainname_by_dhclient(self):
        s1 = self.net.switches[0]
        s1.cmd("dhcp_options None None None dhcp_domain")
        cnt = 15
        while cnt:
            cmd_output = s1.ovscmd("ovs-vsctl list system")
            if "dhcp_domain_name=dhcp_domain" in cmd_output:
                break
            else:
                cnt -= 1
                sleep(1)
        assert 'dhcp_domain_name=dhcp_domain' in cmd_output,\
            "Test to set system domainname through dhclient"\
            " has failed"
        info("### Successfully verified to set system domainname"
             " by dhclient ###\n")

    #Extra cleanup if test fails in middle.
    def mgmt_intf_cleanup(self):
        s1 = self.net.switches[0]
        output = s1.cmd("ip netns exec swns ip addr show dev 1")
        if 'inet' in output:
            s1.cmd("ip netns exec swns ip address flush dev 1")


class Test_mgmt_intf:

    def setup_class(cls):
        # Create the Mininet topology based on mininet.
        Test_mgmt_intf.test = mgmtIntfTests()

    def teardown_class(cls):
        # Stop the Docker containers, and
        # mininet topology.
        Test_mgmt_intf.test.net.stop()
        Enable = False

        if os.path.exists('mgmt_sys_var') is True:
            num = Test_mgmt_intf.test.file_read_for_mgmt_instance_count()
            if num == 0:
                Enable = True
            else:
                num = num - 1
                Test_mgmt_intf.test.file_write_for_mgmt_instance_count(num)

        # Enabling dhclient.profile on VM.
        if Enable is True:
            Test_mgmt_intf.test.enable_dhclient_profile()
            os.system('rm mgmt_sys_var')

    def teardown_method(self, method):
        self.test.mgmt_intf_cleanup()

    def __del__(self):
        del self.test

    # mgmt intf tests.
    def test_dhclient_started_on_mgmt_intf_ipv4(self):
        info("\n########## Test to configure Management "
             "interface with DHCP IPV4 ##########\n")
        self.test.dhclient_started_on_mgmt_intf_ipv4()

    def test_mgmt_intf_updated_during_bootup(self):
        self.test.mgmt_intf_updated_during_bootup()

    def test_dhcp_mode_set_on_mgmt_intf(self):
        self.test.dhcp_mode_set_on_mgmt_intf()

    def test_config_ipv4_on_mgmt_intf_static_mode(self):
        info("\n########## Test to configure Management "
             "interface with static IPV4 ##########\n")
        self.test.config_ipv4_on_mgmt_intf_static_mode()

    def test_config_ipv4_default_gateway_static_mode(self):
        self.test.config_ipv4_default_gateway_static_mode()

    def test_unconfig_ipv4_default_gateway_static_mode(self):
        self.test.unconfig_ipv4_default_gateway_static_mode()

    def test_config_secondary_ipv4_dns_static_mode(self):
        self.test.config_secondary_ipv4_dns_static_mode()

    def test_unconfig_secondary_ipv4_dns_static_mode(self):
        self.test.unconfig_secondary_ipv4_dns_static_mode()

    def test_config_default_gateway_ipv6_dhcp_mode(self):
        info("\n########## Test to configure Management "
             "interface with Dhcp IPV6 ##########\n")
        self.test.config_default_gateway_ipv6_dhcp_mode()

    def test_change_mode_from_static_to_dhcp_ipv6(self):
        self.test.change_mode_from_static_to_dhcp_ipv6()

    def test_config_ipv6_on_mgmt_intf_static_mode(self):
        info("\n########## Test to configure Management "
             "interface with static IPV6 ##########\n")
        self.test.config_ipv6_on_mgmt_intf_static_mode()

    def test_config_ipv6_default_gateway_static_mode(self):
        self.test.config_ipv6_default_gateway_static_mode()

    def test_unconfig_ipv6_default_gateway_static_mode(self):
        self.test.unconfig_ipv6_default_gateway_static_mode()

    def test_config_secondary_ipv6_dns_static_mode(self):
        self.test.config_secondary_ipv6_dns_static_mode()

    def test_unconfig_secondary_ipv6_dns_static_mode(self):
        self.test.unconfig_secondary_ipv6_dns_static_mode()

    def test_config_set_hostname_from_cli(self):
        info("\n########## Test to configure System Hostname "
             " ##########\n")
        self.test.config_set_hostname_from_cli()

    def test_set_hostname_by_dhclient(self):
        self.test.set_hostname_by_dhclient()

    def test_config_set_domainname_from_cli(self):
        info("\n########## Test to configure System Domainname "
             " ##########\n")
        self.test.config_set_domainname_from_cli()

    def test_set_domainname_by_dhclient(self):
        self.test.set_domainname_by_dhclient()
