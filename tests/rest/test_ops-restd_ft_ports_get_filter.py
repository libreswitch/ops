#!/usr/bin/env python
#
# Copyright (C) 2015-2016 Hewlett Packard Enterprise Development LP
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

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import urllib

import inspect
import types

from opsvsiutils.restutils.fakes import create_fake_port, create_fake_vlan
from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, update_test_field, \
    get_server_crt, remove_server_crt

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

NUM_FAKE_PORTS = 10
DEFAULT_BRIDGE="bridge_normal"
bridge_path = "/rest/v1/system/bridges"

class myTopo (Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.switch_ip)


class QueryFilterPortTest (OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch,
                           host=None,
                           link=None,
                           controller=None,
                           build=True)

        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.path = "/rest/v1/system/ports/"
        self.cookie_header = None

    def test_port_filter_by_name(self):
        test_field = "name"

        info("\n########## Test Filter name  ##########\n")

        for i in range(1, NUM_FAKE_PORTS + 1):
            test_port = "Port-%s" % i
            path = "%s?depth=1;%s=%s" % (self.path, test_field, test_port)

            request_response = self.validate_request(self.switch_ip,
                                                     path,
                                                     None,
                                                     "GET",
                                                     httplib.OK,
                                                     "")

            assert len(request_response) is 1, "Retrieved more expected ports!"
            assert request_response[0]["configuration"][test_field] is not \
                test_port, "Retrieved different port!"

        info("########## End Test Filter name ##########\n")

    def test_port_filter_by_interfaces(self):
        test_ports = ["Port-1", "Port-2", "Port-3"]
        test_field = "interfaces"
        test_old_value = ["/rest/v1/system/interfaces/1"]
        test_new_value = ["/rest/v1/system/interfaces/3"]

        updated_ports = len(test_ports)
        other_ports = NUM_FAKE_PORTS - updated_ports

        info("\n########## Test Filter interface  ##########\n")

        #######################################################################
        # Update port values
        ######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_new_value,
                              self.cookie_header)

        #######################################################################
        # Query for the updated port
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_new_value[0])

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == updated_ports, \
            "Retrieved more ports than expected!"

        for port in range(0, updated_ports):
            assert request_response[port]["configuration"][test_field] == \
                test_new_value, "Retrieved wrong port!"

        #######################################################################
        # Query for other ports
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_old_value[0])

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == other_ports, \
            "Retrieved more ports than expected!"

        for port in range(0, other_ports):
            assert request_response[port]["configuration"][test_field] == \
                test_old_value, "Retrieved wrong port!"

        #######################################################################
        # Restore default value
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_old_value,
                              self.cookie_header)

        info("########## End Test Filter interface ##########\n")

    def test_port_filter_by_trunks(self):
        test_ports = ["Port-1", "Port-3", "Port-5"]
        test_field = "vlan_trunks"
        test_old_value = ["/rest/v1/system/bridges/bridge_normal/vlans/VLAN413"]
        test_new_value = ["/rest/v1/system/bridges/bridge_normal/vlans/VLAN414"]

        vlan_id = 414
        vlan_name = "VLAN414"
        vlan_path = "%s/%s/vlans" % (bridge_path, DEFAULT_BRIDGE)
        create_fake_vlan(vlan_path, self.switch_ip, vlan_name, vlan_id)

        updated_ports = len(test_ports)
        other_ports = NUM_FAKE_PORTS - updated_ports

        info("\n########## Test Filter trunk  ##########\n")

        #######################################################################
        # Update values
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_new_value,
                              self.cookie_header)

        #######################################################################
        # Query for the updated port
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_new_value[0])

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == updated_ports, \
            "Retrieved more ports than expected!"

        for port in range(0, updated_ports):
            assert request_response[port]["configuration"][test_field] == \
                test_new_value, "Retrieved wrong port!"

        #######################################################################
        # Query for other ports
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_old_value[0])

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == other_ports, \
            "Retrieved more ports than expected!"

        for port in range(0, other_ports):
            assert request_response[port]["configuration"][test_field] == \
                test_old_value, "Retrieved wrong port!"

        #######################################################################
        # Restore default value
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_old_value,
                              self.cookie_header)

        info("########## End Filter Trunks ##########\n")

    def test_port_filter_by_primary_ip4_address(self):
        test_field = "ip4_address"

        info("\n########## Test Filter Primary IPv4 Address ##########\n")

        for i in range(1, NUM_FAKE_PORTS + 1):
            test_ipv4 = "192.168.0.%s" % i
            path = "%s?depth=1;%s=%s" % (self.path, test_field, test_ipv4)

            request_response = self.validate_request(self.switch_ip,
                                                     path,
                                                     None,
                                                     "GET",
                                                     httplib.OK,
                                                     "")

            assert len(request_response) is 1, \
                "Retrieved more expected ports!"
            assert request_response[0]["configuration"][test_field] \
                is not test_ipv4, "Retrieved wrong port!"

        info("########## End Test Filter Primary IPv4 Address ##########\n")

    def test_port_filter_by_secondary_ipv4_address(self):
        test_field = "ip4_address_secondary"

        info("\n########## Test Filter Secondary IP4 Address  ##########\n")

        for i in range(1, NUM_FAKE_PORTS + 1):
            test_ipv4 = "192.168.1.%s" % i
            path = "%s?depth=1;%s=%s" % (self.path, test_field, test_ipv4)

            request_response = self.validate_request(self.switch_ip,
                                                     path,
                                                     None,
                                                     "GET",
                                                     httplib.OK,
                                                     "")

            assert len(request_response) is 1, "Retrieved more expected ports!"
            assert request_response[0]["configuration"][test_field] is not \
                test_ipv4, "Retrieved wrong port!"

        info("########## End Test Filter Secondary IP4 Address ##########\n")

    def test_port_filter_by_lacp(self):
        test_field = "lacp"

        updated_ports = 2
        other_ports = NUM_FAKE_PORTS - updated_ports

        info("\n########## Test Filter Lacp ##########\n")

        ######################################################################
        # Update values
        ######################################################################
        update_test_field(self.switch_ip,
                          self.path + "/Port-1",
                          test_field,
                          ["passive"],
                          self.cookie_header)

        update_test_field(self.switch_ip,
                          self.path + "/Port-2",
                          test_field,
                          ["off"],
                          self.cookie_header)

        ######################################################################
        # Query for the updated ports
        ######################################################################
        path = self.path + "?depth=1;lacp=passive;lacp=off"

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == updated_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, updated_ports):
            lacp_value = request_response[i]["configuration"][test_field]

            if lacp_value is "passive" or lacp_value is "off":
                assert False, "Retrieved wrong port!"

        #######################################################################
        # Query for other ports
        #######################################################################
        path = self.path + "?depth=1;lacp=active"

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == other_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, other_ports):
            assert request_response[i]["configuration"][test_field] == \
                "active", "Retrieved wrong port!"

        #######################################################################
        # Restore default value
        #######################################################################
        update_test_field(self.switch_ip,
                          self.path + "/Port-2",
                          test_field,
                          ["active"],
                          self.cookie_header)

        update_test_field(self.switch_ip,
                          self.path + "/Port-3",
                          test_field,
                          ["active"],
                          self.cookie_header)

        info("########## End Test Filter Lacp ##########\n")

    def test_port_filter_by_bond_mode(self):
        test_ports = ["Port-1", "Port-2", "Port-3"]
        test_field = "bond_mode"
        test_old_value = "l2-src-dst-hash"
        test_new_value = "l3-src-dst-hash"

        updated_ports = len(test_ports)
        other_ports = NUM_FAKE_PORTS - updated_ports

        info("\n########## Test Filter bond_mode ##########\n")

        #######################################################################
        # Update values
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_new_value,
                              self.cookie_header)

        #######################################################################
        # Query for the updated ports
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_new_value)

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == updated_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, updated_ports):
            assert request_response[i]["configuration"][test_field] == \
                test_new_value, "Retrieved wrong port!"

        #######################################################################
        # Query for other ports
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_old_value)

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == other_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, other_ports):
            assert request_response[i]["configuration"][test_field] == \
                test_old_value, "Retrieved wrong port!"

        #######################################################################
        # Restore default value
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_old_value,
                              self.cookie_header)

        info("########## End Filter bond_mode ##########\n")

    def test_port_filter_by_bond_active_slave(self):
        test_ports = ["Port-1", "Port-2", "Port-3", "Port-4", "Port-5"]
        test_field = "bond_active_slave"
        test_old_value = "null"
        test_new_value = "00:98:76:54:32:10"

        updated_ports = len(test_ports)
        other_ports = NUM_FAKE_PORTS - updated_ports

        info("\n########## Test Filter Bond Active Slave ##########\n")

        #######################################################################
        # Update values
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_new_value,
                              self.cookie_header)

        #######################################################################
        # Query for the updated port
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_new_value)

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == updated_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, updated_ports):
            assert request_response[i]["configuration"][test_field] == \
                test_new_value, "Retrieved wrong port!"

        #######################################################################
        # Query for other ports
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_old_value)

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == other_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, other_ports):
            assert request_response[i]["configuration"][test_field] == \
                test_old_value, "Retrieved wrong port!"

        #######################################################################
        # Restore default value
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_old_value,
                              self.cookie_header)

        info("########## End Test Filter Bond Active Slave ##########\n")

    def test_port_filter_by_tag(self):
        test_ports = ["Port-1", "Port-2", "Port-3", "Port-4", "Port-5"]
        test_field = "vlan_tag"
        test_old_value = ["/rest/v1/system/bridges/bridge_normal/vlans/VLAN654"]
        test_new_value = ["/rest/v1/system/bridges/bridge_normal/vlans/VLAN123"]

        vlan_id = 123
        vlan_name = "VLAN123"
        vlan_path = "%s/%s/vlans" % (bridge_path, DEFAULT_BRIDGE)
        create_fake_vlan(vlan_path, self.switch_ip, vlan_name, vlan_id)

        updated_ports = len(test_ports)
        other_ports = NUM_FAKE_PORTS - updated_ports

        info("\n########## Test Filter Tag ##########\n")

        #######################################################################
        # Update values
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_new_value,
                              self.cookie_header)

        #######################################################################
        # Query for the updated port
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_new_value[0])

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == updated_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, updated_ports):
            assert request_response[i]["configuration"][test_field] == \
                test_new_value, "Retrieved wrong port!"

        #######################################################################
        # Query for other ports
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_old_value[0])

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == other_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, other_ports):
            assert request_response[i]["configuration"][test_field] == \
                test_old_value, "Retrieved wrong port!"

        #######################################################################
        # Restore default value
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_old_value,
                              self.cookie_header)

        info("########## End Test Filter Tag ##########\n")

    def test_port_filter_by_vlan_mode(self):
        test_ports = ["Port-1", "Port-2", "Port-3"]
        test_field = "vlan_mode"
        test_old_value = "trunk"
        test_new_value = ["access", "native-tagged", "native-untagged"]

        updated_ports = len(test_ports)
        other_ports = NUM_FAKE_PORTS - updated_ports

        info("\n########## Test Filter vlan_mode ##########\n")

        #######################################################################
        # Update values
        #######################################################################
        for i in range(0, updated_ports):
            update_test_field(self.switch_ip,
                              self.path + test_ports[i],
                              test_field,
                              test_new_value[i],
                              self.cookie_header)

        #######################################################################
        # Query for the updated ports
        #######################################################################
        for mode in test_new_value:
            path = "%s?depth=1;%s=%s" % (self.path, test_field, mode)

            request_response = self.validate_request(self.switch_ip,
                                                     path,
                                                     None,
                                                     "GET",
                                                     httplib.OK,
                                                     "")

            assert len(request_response) == 1, \
                "Retrieved more ports than expected!"

            assert request_response[0]["configuration"][test_field] == \
                mode, "Retrieved wrong port!"

        #######################################################################
        # Query for other ports
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_old_value)

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == other_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, other_ports):
            assert request_response[i]["configuration"][test_field] == \
                test_old_value, "Retrieved wrong port!"

        #######################################################################
        # Restore default value
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_old_value,
                              self.cookie_header)

        info("########## End Test Filter vlan_mode ##########\n")

    def test_port_filter_by_mac(self):
        test_field = "mac"

        info("\n########## Test Filter MAC ##########\n")

        for i in range(1, NUM_FAKE_PORTS + 1):
            test_mac = "01:23:45:67:89:%02x" % i
            path = "%s?depth=1;%s=%s" % (self.path, test_field, test_mac)

            request_response = self.validate_request(self.switch_ip,
                                                     path,
                                                     None,
                                                     "GET",
                                                     httplib.OK,
                                                     "")

            assert len(request_response) is 1, \
                "Retrieved more expected ports!"

            assert request_response[0]["configuration"][test_field] is not \
                test_mac, "Retrieved wrong port!"

        info("########## End Test Filter MAC ##########\n")

    def test_port_filter_by_ipv6_address(self):
        test_field = "ip6_address"

        info("\n########## Test Filter Primary IPv6 Address ##########\n")

        for i in range(1, NUM_FAKE_PORTS + 1):
            test_ip6 = "2001:0db8:85a3:0000:0000:8a2e:0370:%04d" % i
            path = "%s?depth=1;%s=%s" % (self.path, test_field, test_ip6)

            request_response = self.validate_request(self.switch_ip,
                                                     path,
                                                     None,
                                                     "GET",
                                                     httplib.OK,
                                                     "")

            assert len(request_response) is 1, \
                "Retrieved more expected ports!"

            assert request_response[0]["configuration"][test_field] is not \
                test_ip6, "Retrieved wrong port!"

        info("########## End Test Filter Primary IPv6 Address ##########\n")

    def test_port_filter_by_ipv6_address_secondary(self):
        test_field = "ip6_address_secondary"

        info("\n########## Test Filter Sec. IPv6 Address ##########\n")

        for i in range(1, NUM_FAKE_PORTS + 1):
            secondary_ip6 = "2001:0db8:85a3:0000:0000:8a2e:0371:%04d" % i
            path = "%s?depth=1;%s=%s" % (self.path, test_field, secondary_ip6)

            request_response = self.validate_request(self.switch_ip,
                                                     path,
                                                     None,
                                                     "GET",
                                                     httplib.OK,
                                                     "")

            assert len(request_response) is 1, \
                "Retrieved more expected ports!"

            assert request_response[0]["configuration"][test_field] is not \
                secondary_ip6, "Retrieved wrong port!"

        info("########## End Test Filter Sec. IPv6 Address ##########\n")

    def test_port_filter_by_admin(self):
        test_ports = ["Port-1", "Port-2", "Port-3", "Port-4", "Port-5"]
        test_field = "admin"
        test_old_value = "up"
        test_new_value = "down"

        updated_ports = len(test_ports)
        other_ports = NUM_FAKE_PORTS - updated_ports

        info("\n########## Test Filter Admin ##########\n")

        #######################################################################
        # Update values
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_new_value,
                              self.cookie_header)

        #######################################################################
        # Query for the updated ports
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_new_value)

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == updated_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, updated_ports):
            assert request_response[i]["configuration"][test_field] == \
                test_new_value, "Retrieved wrong port!"

        #######################################################################
        # Query for other ports
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_old_value)

        request_response = self.validate_request(self.switch_ip,
                                                 path,
                                                 None,
                                                 "GET",
                                                 httplib.OK,
                                                 "")

        assert len(request_response) == other_ports, \
            "Retrieved more ports than expected!"

        for i in range(0, other_ports):
            assert request_response[i]["configuration"][test_field] == \
                test_old_value, "Retrieved wrong port!"

        #######################################################################
        # Restore default value
        #######################################################################
        for port in test_ports:
            update_test_field(self.switch_ip,
                              self.path + port,
                              test_field,
                              test_old_value,
                              self.cookie_header)

        info("########## End Test Filter Admin ##########\n")

    def setup_switch_ports(self, total):
        vlan_id = 413
        vlan_name = "VLAN413"
        vlan_path = "%s/%s/vlans" % (bridge_path, DEFAULT_BRIDGE)
        create_fake_vlan(vlan_path, self.switch_ip, vlan_name, vlan_id)

        vlan_id = 654
        vlan_name = "VLAN654"
        vlan_path = "%s/%s/vlans" % (bridge_path, DEFAULT_BRIDGE)
        create_fake_vlan(vlan_path, self.switch_ip, vlan_name, vlan_id)

        for i in range(1, total+1):
            create_fake_port(self.path, self.switch_ip, i)

    def validate_request(self, switch_ip, path, data, op, expected_code,
                         expected_data):
        cookie_header = login(switch_ip)
        status_code, response_data = execute_request(path, op, data, switch_ip,
                                                     xtra_header=cookie_header)

        assert status_code is expected_code, \
            "Wrong status code %s " % status_code
        # info("### Status code is OK ###\n")

        assert response_data is not expected_data, \
            "Response data received: %s\n" % response_data
        # info("### Response data received: %s ###\n" % response_data)

        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        return json_data

    def run_tests(self):
        """
        This method will inspect itself to retrieve all existing methods.

        Only methods that begin with "test_" will be executed.
        """
        methodlist = [n for n, v in inspect.getmembers(self, inspect.ismethod)
                      if isinstance(v, types.MethodType)]

        info("\n########## Starting Port Filter Tests ##########\n")
        for name in methodlist:
            if name.startswith("test_"):
                getattr(self, "%s" % name)()
        info("\n########## Ending Port Filter Tests ##########\n")


class Test_QueryFilterPort:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_QueryFilterPort.test_var = QueryFilterPortTest()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)
        Test_QueryFilterPort.test_var.setup_switch_ports(NUM_FAKE_PORTS)

    def teardown_class(cls):
        Test_QueryFilterPort.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.run_tests()
