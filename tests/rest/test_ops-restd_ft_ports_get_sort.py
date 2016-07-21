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

from opsvsiutils.restutils.fakes import create_fake_port
from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, update_test_field, \
    fill_with_function, random_mac, random_ip6_address, \
    get_server_crt, remove_server_crt

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0
NUM_FAKE_PORTS = 10


class myTopo(Topo):

    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class QuerySortPortTest (OpsVsiTest):

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

        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.PATH = "/rest/v1/system/ports"
        self.PORT_PATH = self.PATH + "/Port-1"
        self.cookie_header = None

    """
    **********************************************************************
    * Sort utilities                                                     *
    **********************************************************************
    """

    def execute_sort_by_request(self, attributes, expected_code, desc=False,
                                limit=None, offset=None, depth=1,
                                filters=None):
        """
        Common function to send a sort request
        :param attributes
        :param expected_code
        :param desc
        :param limit:
        :param offset:
        :param depth:
        :param filters
        """
        path = self.PATH + "?"
        if depth is not None:
            path += "depth=" + str(depth) + ";"
        if limit is not None:
            path += "limit=" + str(limit) + ";"
        if offset is not None:
            path += "offset=" + str(offset) + ";"

        if filters is not None:
            if isinstance(filters, dict):
                for key in filters.viewkeys():
                    path += key + "=" + filters[key]
                path += ";"
            else:
                path += filters[key] + ";"

        path += "sort="

        if desc:
            path += "-"
        if isinstance(attributes, list):
            for attr in attributes:
                path += attr
                if attr != attributes[-1]:
                    path += ","
        else:
            path += attributes

        info("### Request to %s ###\n" % path)
        status_code, response_data = execute_request(
            path, "GET", None, self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == expected_code, "Wrong status code %s " % \
                                             status_code
        info("### Status code is %s ###\n" % status_code)
        assert response_data is not "", \
            "Response data received: %s\n" % response_data
        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        # In order to no affect the tests the bridge_normal is removed
        if expected_code == httplib.OK:
            self.remove_bridge_from_data(json_data)
        return json_data

    def remove_bridge_from_data(self, json_data):
        """
        Function used to remove the bridge_normal from test data
        """
        index = None
        for i in range(0, len(json_data)):
            if json_data[i]["configuration"]["name"] == "bridge_normal":
                index = i
                break
        if index is not None:
            json_data.pop(index)

    def check_sort_expectations(self, expected_values, json_data, field):
        """
        Common function to check order expectations
        """
        for i in range(0, len(expected_values)):
            # Expected values
            expected_value = expected_values[i]
            # Returned values
            returned_value = json_data[i]["configuration"][field]
            if (isinstance(returned_value, list) and
                    not isinstance(expected_value, list)):
                expected_value = [expected_value]

            assert expected_value == returned_value, "Wrong order. \
                    Expected: %s Returned: %s" % (expected_value,
                                                  returned_value)

    def sort_value_to_lower(self, value):
        """
        Used to sort a value to lower case, depending of the type
        """
        if isinstance(value, str):
            return value.lower()
        else:
            return value

    """
    **********************************************************************
    * Sort by tests                                                      *
    **********************************************************************
    """

    def non_null_col(self, json_data, column):
        flag = True
        column_list = []
        if type(column) is list:
            column_list = column
        else:
            column_list.append(column)

        for col in column_list:
            for data in json_data:
                if col not in data['configuration']:
                    flag = False
                break
        return flag

    def test_port_sort_by_name(self, desc=False):
        info("\n########## Test to sort port by name##########\n")

        expected_values = []

        for i in range(1, NUM_FAKE_PORTS + 1):
            port_name = "Port-%s" % i
            expected_values.append(port_name)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("name", httplib.OK, desc)
        assert len(json_data) is (
            NUM_FAKE_PORTS), "Retrieved more expected ports!"

        if self.non_null_col(json_data, "name"):
            self.check_sort_expectations(expected_values, json_data, "name")

        info("########## End Test to sort ports by name##########\n")

    def test_port_sort_by_interfaces(self, desc=False):
        info("\n########## Test to sort port by interfaces##########\n")

        expected_values = []
        for i in range(1, NUM_FAKE_PORTS + 1):
            interfaces = []
            if not desc:
                interfaces = ["/rest/v1/system/interfaces/%s" %
                              (NUM_FAKE_PORTS + 1 - i)]
            else:
                interfaces = ["/rest/v1/system/interfaces/%s" % i]

            update_test_field(self.SWITCH_IP, self.PATH + "/Port-%s" % i,
                              "interfaces", interfaces, self.cookie_header)
            expected_values.append(interfaces)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)
        json_data = self.execute_sort_by_request("interfaces", httplib.OK,
                                                 desc)
        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "interfaces"):
            self.check_sort_expectations(expected_values, json_data,
                                         "interfaces")

        info("########## End Test to sort ports by interfaces ##########\n")

    def test_port_sort_by_trunks(self, desc=False):
        info("\n########## Test to sort port by trunks ##########\n")

        expected_values = []
        for i in range(1, NUM_FAKE_PORTS + 1):
            trunks = []
            if not desc:
                trunks = [NUM_FAKE_PORTS + 1 - i]
            else:
                trunks = [i]
            update_test_field(
                self.SWITCH_IP, self.PATH + "/Port-%s" % i, "trunks", trunks,
                self.cookie_header)
            expected_values.append(trunks)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("trunks", httplib.OK, desc)
        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "trunks"):
            self.check_sort_expectations(expected_values, json_data, "trunks")
        info("\n########## End to sort port by trunks ##########\n")

    def test_port_sort_by_ip4_address(self, desc=False):
        info("\n########## Test to sort port by ip4 address ##########\n")

        json_data = self.execute_sort_by_request("ip4_address", httplib.OK,
                                                 desc)

        assert len(json_data) is (
            NUM_FAKE_PORTS), "Retrieved more expected ports!"

        expected_values = []
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = "192.168.0.%(index)s/24" % {"index": i}
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)
        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "ip4_address"):
            self.check_sort_expectations(expected_values, json_data,
                                         "ip4_address")

        info("########## End Test to sort ports by ip4 address ##########\n")

    def test_port_sort_by_ip4_address_secondary(self, desc=False):
        info("\n########## Test to sort port by ip4_address_secondary "
             "##########\n")

        json_data = self.execute_sort_by_request("ip4_address_secondary",
                                                 httplib.OK, desc)

        assert len(json_data) is (
            NUM_FAKE_PORTS), "Retrieved more expected ports!"

        expected_values = []
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = "192.168.1.%(index)s/24" % {"index": i}
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)
        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "ip4_address_secondary"):
            self.check_sort_expectations(
                expected_values, json_data, "ip4_address_secondary")

        info("\n########## End Test to sort port by ip4_address_secondary "
             "##########\n")

    def test_port_sort_by_lacp(self, desc=False):
        info("\n########## Test to sort port by lacp ##########\n")

        expected_values = []
        values = ["active", "passive", "off"]
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = values[(i - 1) % len(values)]
            update_test_field(
                self.SWITCH_IP, self.PATH + "/Port-%s" % i, "lacp", value,
                self.cookie_header)
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("lacp", httplib.OK, desc)

        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "lacp"):
            self.check_sort_expectations(expected_values, json_data, "lacp")

        info("\n########## End Test to sort port by lacp ##########\n")

    def test_port_sort_by_bond_mode(self, desc=False):
        info("\n########## Test to sort port by bond_mode ##########\n")

        expected_values = []
        values = ["l2-src-dst-hash", "l3-src-dst-hash"]
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = values[(i - 1) % len(values)]
            update_test_field(
                self.SWITCH_IP, self.PATH + "/Port-%s" % i, "bond_mode", value,
                self.cookie_header)
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("bond_mode", httplib.OK, desc)

        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "bond_mode"):
            self.check_sort_expectations(expected_values, json_data,
                                         "bond_mode")

        info("\n########## End Test to sort port by bond_mode ##########\n")

    def test_port_sort_by_tag(self, desc=False):
        info("\n########## Test to sort port by tag ##########\n")

        expected_values = []
        values = fill_with_function(random.randint(1, 4094), NUM_FAKE_PORTS)
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = values[(i - 1)]
            update_test_field(
                self.SWITCH_IP, self.PATH + "/Port-%s" % i, "tag", value,
                self.cookie_header)
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("tag", httplib.OK, desc)

        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "tag"):
            self.check_sort_expectations(expected_values, json_data, "tag")

        info("\n########## End Test to sort port by tag ##########\n")

    def test_port_sort_by_vlan_mode(self, desc=False):
        info("\n########## Test to sort port by vlan_mode ##########\n")

        expected_values = []
        values = ["trunk", "access", "native-tagged", "native-untagged"]
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = values[(i - 1) % len(values)]
            update_test_field(
                self.SWITCH_IP, self.PATH + "/Port-%s" % i, "vlan_mode", value,
                self.cookie_header)
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("vlan_mode", httplib.OK, desc)

        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "vlan_mode"):
            self.check_sort_expectations(expected_values, json_data,
                                         "vlan_mode")

        info("\n########## End Test to sort port by vlan_mode ##########\n")

    def test_port_sort_by_mac(self, desc=False):
        info("\n########## Test to sort port by mac ##########\n")

        expected_values = []
        values = fill_with_function(random_mac(), NUM_FAKE_PORTS)

        for i in range(1, NUM_FAKE_PORTS + 1):
            value = values[i - 1]
            update_test_field(
                self.SWITCH_IP, self.PATH + "/Port-%s" % i, "mac", value,
                self.cookie_header)
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("mac", httplib.OK, desc)

        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "mac"):
            self.check_sort_expectations(expected_values, json_data, "mac")

        info("\n########## End Test to sort port by mac ##########\n")

    def test_port_sort_by_bond_active_slave(self, desc=False):
        info("\n########## Test to sort port by bond_active_slave "
             "##########\n")

        expected_values = []
        values = fill_with_function(random_mac(), NUM_FAKE_PORTS)
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = values[i - 1]
            update_test_field(self.SWITCH_IP, self.PATH + "/Port-%s" % i,
                              "bond_active_slave", value,
                              self.cookie_header)
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("bond_active_slave",
                                                 httplib.OK, desc)

        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "bond_active_slave"):
            self.check_sort_expectations(
                expected_values, json_data, "bond_active_slave")

        info("\n########## End Test to sort port by bond_active_slave "
             "##########\n")

    def test_port_sort_by_ip6_address(self, desc=False):
        info("\n########## Test to sort port by ip6_address ##########\n")

        expected_values = []
        values = fill_with_function(random_ip6_address() + '/64',
                                    NUM_FAKE_PORTS)
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = values[i - 1]
            update_test_field(self.SWITCH_IP, self.PATH + "/Port-%s" % i,
                              "ip6_address", value, self.cookie_header)
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("ip6_address", httplib.OK,
                                                 desc)

        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "ip6_address"):
            self.check_sort_expectations(expected_values, json_data,
                                         "ip6_address")

        info("\n########## End Test to sort port by ip6_address ##########\n")

    def test_port_sort_by_ip6_address_secondary(self, desc=False):
        info("\n########## Test to sort port by ip6_address_secondary "
             "##########\n")

        expected_values = []
        values = fill_with_function(random_ip6_address() + '/64',
                                    NUM_FAKE_PORTS)
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = values[i - 1]
            update_test_field(self.SWITCH_IP, self.PATH + "/Port-%s" % i,
                              "ip6_address_secondary", [value],
                              self.cookie_header)
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("ip6_address_secondary",
                                                 httplib.OK, desc)

        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "ip6_address_secondary"):
            self.check_sort_expectations(
                expected_values, json_data, "ip6_address_secondary")

        info("\n########## End Test to sort port by ip6_address_secondary "
             "##########\n")

    def test_port_sort_by_admin(self, desc=False):
        info("\n########## Test to sort port by admin ##########\n")

        expected_values = []
        values = ["up", "down"]
        for i in range(1, NUM_FAKE_PORTS + 1):
            value = values[(i - 1) % len(values)]
            update_test_field(
                self.SWITCH_IP, self.PATH + "/Port-%s" % i, "admin", value,
                self.cookie_header)
            expected_values.append(value)

        expected_values.sort(key=lambda val: self.sort_value_to_lower(val),
                             reverse=desc)

        json_data = self.execute_sort_by_request("admin", httplib.OK, desc)

        assert len(json_data) is (NUM_FAKE_PORTS), \
            "Retrieved more expected ports!"

        if self.non_null_col(json_data, "admin"):
            self.check_sort_expectations(expected_values, json_data, "admin")

        info("\n########## End Test to sort port by admin ##########\n")

    def test_port_sort_by_admin_name(self, desc=False):
        info("\n########## Test to sort port by (admin,name) ##########\n")

        expected_values = []
        admin_values = ["up", "down"]
        random.seed()
        for i in range(1, NUM_FAKE_PORTS + 1):
            port = "Port-%s" % i
            admin_value = admin_values[(i - 1) % len(admin_values)]
            update_test_field(
                self.SWITCH_IP, self.PATH + "/" + port, "admin", admin_value,
                self.cookie_header)
            expected_dict = {"admin": admin_value, "name": port}
            expected_values.append(expected_dict)

        columns = ["admin", "name"]

        compare_function = lambda item: tuple(self.sort_value_to_lower(item[k])
                                              for k in columns)
        expected_values = sorted(expected_values, key=compare_function,
                                 reverse=desc)

        json_data = self.execute_sort_by_request(columns, httplib.OK, desc)

        assert len(json_data) is (
            NUM_FAKE_PORTS), "Retrieved more expected ports!"

        for i in range(0, len(expected_values)):
            expected_name = expected_values[i]["name"]
            expected_admin = expected_values[i]["admin"]
            returned_name = json_data[i]["configuration"]["name"]
            returned_admin = json_data[i]["configuration"]["admin"]

            if self.non_null_col(json_data, columns):
                assert returned_name == expected_name and \
                    expected_admin == returned_admin, \
                    "Wrong order. Expected: %s Returned: %s" \
                    % (expected_name, returned_name)

        info("\n########## End Test to sort port by (admin,name) ##########\n")

    def test_port_sort_by_invalid_column(self, desc=False):
        test_title = "Test to sort port by invalid column"
        info("\n########## " + test_title + " ##########\n")
        json_data = self.execute_sort_by_request("invalid_column",
                                                 httplib.BAD_REQUEST, desc)
        info("Request response: %s\n" % json_data)
        info("########## End " + test_title + " ##########\n")

    def test_port_sort_without_depth_parameter(self, desc=False):
        test_title = "Test to sort port without depth parameter"
        info("\n########## " + test_title + " ##########\n")
        json_data = self.execute_sort_by_request("name", httplib.BAD_REQUEST,
                                                 desc, depth=None)
        info("Request response: %s\n" % json_data)
        info("########## End " + test_title + " ##########\n")

    def test_port_sort_with_invalid_pagination_parameter(self, desc=False):
        test_title = "Test to sort port with invalid pagination parameter"
        info("\n########## " + test_title + " ##########\n")
        json_data = self.execute_sort_by_request("name", httplib.BAD_REQUEST,
                                                 desc, offset="one")
        info("Request response: %s\n" % json_data)
        info("########## End " + test_title + " ##########\n")

    def test_port_sort_with_offset_equals_zero(self, desc=False):
        test_title = "Test to sort port with offset equals zero"
        info("\n########## " + test_title + " ##########\n")
        json_data = self.execute_sort_by_request("name", httplib.OK, desc,
                                                 offset=0)
        assert len(json_data) == NUM_FAKE_PORTS,\
            "Retrieved a different amount of ports than expected!"
        info("########## End " + test_title + " ##########\n")

    def test_port_sort_with_limit_equals_zero(self, desc=False):
        test_title = "Test to sort port with limit equals zero"
        info("\n########## " + test_title + " ##########\n")
        json_data = self.execute_sort_by_request("name", httplib.BAD_REQUEST,
                                                 desc, limit=0)
        info("Request response: %s\n" % json_data)
        info("########## End " + test_title + " ##########\n")

    def test_port_sort_shows_last_result(self, desc=False):
        test_title = "Test to sort port shows last result"
        info("\n########## " + test_title + " ##########\n")
        filtered_ports = ""
        for i in range(1, NUM_FAKE_PORTS + 1):
            filtered_ports += "Port-%s," % i
        filtered_ports = filtered_ports.rstrip(",")
        json_data = \
            self.execute_sort_by_request("name", httplib.OK, desc,
                                         limit=2,
                                         offset=NUM_FAKE_PORTS - 1,
                                         filters={
                                             "name": filtered_ports})
        assert len(json_data) == 1, \
            "Retrieved a different amount of ports than expected!"
        info("########## End " + test_title + " ##########\n")

    def test_port_sort_with_negative_limit(self, desc=False):
        test_title = "Test to sort port with negative limit"
        info("\n########## " + test_title + " ##########\n")
        json_data = self.execute_sort_by_request("name", httplib.BAD_REQUEST,
                                                 desc, limit=-1)
        info("Request response: %s\n" % json_data)
        info("########## End " + test_title + " ##########\n")

    def test_port_sort_with_limit_equals_all_elements_in_db(self, desc=False):
        """
        Test all available ports with the limit parameter equal to the same
        amount of filtered ports requested
        """
        test_title = "Test to sort port with limit == all elements in db"
        info("\n########## " + test_title + " ##########\n")
        filtered_ports = ""
        for i in range(1, NUM_FAKE_PORTS + 1):
            filtered_ports += "Port-%s," % i
        filtered_ports = filtered_ports.rstrip(",")
        json_data = \
            self.execute_sort_by_request("name", httplib.OK, desc,
                                         filters={
                                             "name": filtered_ports})
        assert len(json_data) == NUM_FAKE_PORTS, \
            "Retrieved a different amount of ports than expected!"
        info("########## End " + test_title + " ##########\n")

    def test_port_sort_with_limit_higher_all_elements_in_db(self, desc=False):
        """
        Test all available ports with the limit parameter higher to the amount
        of filtered ports requested
        """
        test_title = "Test to sort port with limit > all elements in db"
        info("\n########## " + test_title + " ##########\n")
        filtered_ports = ""
        for i in range(1, NUM_FAKE_PORTS + 1):
            filtered_ports += "Port-%s," % i
        filtered_ports = filtered_ports.rstrip(",")
        json_data = \
            self.execute_sort_by_request("name", httplib.OK, desc,
                                         filters={
                                             "name": filtered_ports})
        assert len(json_data) == NUM_FAKE_PORTS, \
            "Retrieved a different amount of ports than expected!"
        info("########## End " + test_title + " ##########\n")

    def test_port_sort_with_all_available_keys(self, desc=False):
        """
        Test ports resource by sorting with all the available keys
        """
        test_title = "Test to sort port with all available keys"
        info("\n########## " + test_title + " ##########\n")

        expected_values = []
        admin_values = ["up", "down"]
        random.seed()
        for i in range(1, NUM_FAKE_PORTS + 1):
            port = "Port-%s" % i
            admin_value = admin_values[(i - 1) % len(admin_values)]
            update_test_field(
                self.SWITCH_IP, self.PATH + "/" + port, "admin", admin_value,
                self.cookie_header)
            status_code, response_data = execute_request(
                self.PATH + "/" + port, "GET", None, self.SWITCH_IP,
                xtra_header=self.cookie_header)
            assert status_code == httplib.OK, "Wrong status code %s " % \
                                              status_code
            json_data = json.loads(response_data)
            expected_dict = json_data['configuration']
            expected_values.append(expected_dict)

        columns = []
        for key in expected_values[0].viewkeys():
            columns.append(key)

        compare_function = lambda item: tuple(self.sort_value_to_lower(item[k])
                                              for k in columns)
        expected_values = sorted(expected_values, key=compare_function,
                                 reverse=desc)

        json_data = self.execute_sort_by_request(columns, httplib.OK, desc)

        assert len(json_data) is (
            NUM_FAKE_PORTS), "Retrieved more expected ports!"

        if self.non_null_col(json_data, columns):
            for i in range(0, len(json_data)):
                for column in columns:
                    assert json_data[i]["configuration"][column] == \
                           expected_values[i][column], \
                           "Wrong order. Expected: %s Returned: %s" \
                           % (expected_values[i][column],
                              json_data[i]["configuration"][column])
        info("########## End " + test_title + " ##########\n")

    def setup_switch_ports(self, total):
        for i in range(0, total):
            create_fake_port(self.PATH, self.SWITCH_IP, (i + 1))

    def run_tests(self):
        """
        This method will inspect itself to retrieve all existing methodS.
        Only methods that begin with "test_" will be executed.
        """
        methodlist = [n for n, v in inspect.getmembers(
            self, inspect.ismethod) if isinstance(v, types.MethodType)]

        info("\n########## Start Port Sort Tests Ascending Order ##########\n")
        for name in methodlist:
            if name.startswith("test_"):
                # Ascending Order Test
                getattr(self, "%s" % name)()
        info("\n########## End Port Sort Tests Ascending Order ##########\n")

        info("\n########## Start Port Sort Tests Descending Order "
             "##########\n")
        for name in methodlist:
            if name.startswith("test_"):
                # Descending Order Test
                getattr(self, "%s" % name)(desc=True)
        info("\n########## End Port Sort Tests Descending Order ##########\n")


class Test_QuerySortPort:

    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_QuerySortPort.test_var = QuerySortPortTest()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.SWITCH_IP)
        Test_QuerySortPort.test_var.setup_switch_ports(NUM_FAKE_PORTS)

    def teardown_class(cls):
        Test_QuerySortPort.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.run_tests()
