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

from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, create_test_ports

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0
NUM_PORTS = 100


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class QueryPortPaginationTest(OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch, host=None, link=None,
                           controller=None, build=True)

        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.PATH = "/rest/v1/system/ports"
        self.cookie_header = None

    def test_pagination_empty_offset(self, path):
        info("### Attempting to fetch first 5 ports in the list with" +
             " no offset set ###\n")

        status_code, response_data = execute_request(
            path + ";limit=5", "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        json_data_len = len(json_data)

        assert json_data_len == 5, "Wrong request size %s " % json_data_len
        info("### Correct number of ports returned: %s  ###\n" % json_data_len)

        assert json_data[0]["configuration"]["name"] == "bridge_normal", \
            "Wrong initial port: %s" % json_data[0]["configuration"]["name"]
        info("### Correct offset was set by default ###\n")

    def test_pagination_empty_limit(self, path):
        info("### Attempting to fetch last 10 ports in the list with" +
             " no limit set ###\n")

        status_code, response_data = execute_request(
            path + ";offset=91", "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        json_data_len = len(json_data)

        assert json_data_len == 10, "Wrong request size %s " % json_data_len
        info("### Correct number of ports returned: %s  ###\n" % json_data_len)

        assert json_data[0]["configuration"]["name"] == "Port90", \
            "Wrong initial port: %s" % json_data[0]["configuration"]["name"]
        assert json_data[9]["configuration"]["name"] == "Port99", \
            "Wrong final port: %s" % json_data[9]["configuration"]["name"]
        info("### Correct limit was set by default ###\n")

    def test_pagination_no_offset_limit(self, path):
        info("### Attempting to fetch ports with no offset or limit set ###\n")

        status_code, response_data = execute_request(
            path, "GET", None, self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        json_data_len = len(json_data)

        # There a total fo NUM_PORTS + 1 (counting the default port)
        assert json_data_len == NUM_PORTS + 1, \
            "Wrong request size %s " % json_data_len
        info("### Correct number of ports returned: %s  ###\n" % json_data_len)

    def test_pagination_negative_offset(self, path):
        info("### Attempting to fetch ports with negative offset ###\n")

        status_code, response_data = execute_request(
            path + ";offset=-1;limit=10", "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST ###\n")

    def test_pagination_negative_limit(self, path):
        info("### Attempting to fetch ports with negative limit ###\n")

        status_code, response_data = execute_request(
            path + ";offset=5;limit=-1", "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST ###\n")

    def test_pagination_offset_greater_than_data(self, path):
        info("### Attempting to fetch ports with offset larger than" +
             " data size ###\n")

        status_code, response_data = execute_request(
            path + ";offset=200", "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST ###\n")

    def test_pagination_offset_remainder(self, path):
        info("### Attempting to fetch remainder 10 ports in the list using " +
             "large limit ###\n")

        status_code, response_data = execute_request(
            path + ";offset=91;limit=20", "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        json_data_len = len(json_data)

        assert json_data_len == 10, "Wrong request size %s " % json_data_len
        info("### Correct number of ports returned: %s  ###\n" % json_data_len)

        assert json_data[0]["configuration"]["name"] == "Port90", \
            "Wrong initial port: %s" % json_data[0]["configuration"]["name"]
        assert json_data[9]["configuration"]["name"] == "Port99", \
            "Wrong final port: %s" % json_data[9]["configuration"]["name"]
        info("### Expected remainder ports are returned " +
             "using large limit ###\n")

    def test_pagination_offset_limit_non_plural(self):
        info("### Attempting to fetch single port with offset and limit " +
             "present ###\n")

        status_code, response_data = execute_request(
            self.PATH + "/bridge_normal?depth=1" + ";offset=0;limit=10",
            "GET", None, self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST ###\n")

    def test_pagination_offset_only_non_plural(self):
        info("### Attempting to fetch single port with offset " +
             "present ###\n")

        status_code, response_data = execute_request(
            self.PATH + "/bridge_normal?depth=1" + ";offset=5",
            "GET", None, self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST ###\n")

    def test_pagination_limit_only_non_plural(self):
        info("### Attempting to fetch single port with offset " +
             "present ###\n")

        status_code, response_data = execute_request(
            self.PATH + "/bridge_normal?depth=1" + ";limit=5",
            "GET", None, self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST ###\n")

    def test_pagination_indexes(self):
        info("\n########## Test to validate pagination indexes of GET" +
             " request results ##########\n")

        path = self.PATH + "?depth=1;sort=name"

        # Test empty offset, it should default to 0
        self.test_pagination_empty_offset(path)

        # Test empty limit with offset set to 91,
        # it should return the last 10 ports
        self.test_pagination_empty_limit(path)

        # Test GET with no offset or limit set,
        # the entire port list should be returned
        self.test_pagination_no_offset_limit(path)

        # Test negative offset
        self.test_pagination_negative_offset(path)

        # Test negative limit
        self.test_pagination_negative_limit(path)

        # Test an offset greater than total data size
        self.test_pagination_offset_greater_than_data(path)

        # Test (offset + limit) > total ports
        # Ports from offset to the end should be returned
        self.test_pagination_offset_remainder(path)

        # Test offset and limit present for non-plural resource
        self.test_pagination_offset_limit_non_plural()

        # Test offset present for non-plural resource
        self.test_pagination_offset_only_non_plural()

        # Test limit present for non-plural resource
        self.test_pagination_limit_only_non_plural()

        info("\n########## End test to validate pagination indexes of GET" +
             " request results ##########\n")

    def test_query_ports_paginated(self):
        info("\n########## Test to Validate pagination of GET request" +
             " results ##########\n")

        # Request will be of depth = 1, with ports sorted by name
        path = self.PATH + "?depth=1;sort=name"

        # Request first 10 Ports

        info("### Attempting to fetch first 10 ports in the list ###\n")

        status_code, response_data = execute_request(
            path + ";offset=0;limit=10", "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        json_data_len = len(json_data)

        assert json_data_len == 10, "Wrong request size %s " % json_data_len
        info("### Correct number of ports returned: %s  ###\n" % json_data_len)

        # Ports are sorted alphabetically by name
        # Test ports are named Port0-Port100, when
        # sorted alphabetically: Port0, Port1, Port11, Port12...

        assert json_data[0]["configuration"]["name"] == "bridge_normal", \
            "Wrong initial port: %s" % json_data[0]["configuration"]["name"]
        assert json_data[9]["configuration"]["name"] == "Port16", \
            "Wrong final port: %s" % json_data[9]["configuration"]["name"]
        info("### Correct set of ports returned ###\n")

        # Request 10 ports from the list end

        info("### Attempting to fetch last 10 ports in the list ###\n")

        status_code, response_data = execute_request(
            path + ";offset=91;limit=10", "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        json_data_len = len(json_data)

        assert json_data_len == 10, "Wrong request size %s " % json_data_len
        info("### Correct number of ports returned: %s  ###\n" % json_data_len)

        assert json_data[0]["configuration"]["name"] == "Port90", \
            "Wrong initial port: %s" % json_data[0]["configuration"]["name"]
        assert json_data[9]["configuration"]["name"] == "Port99", \
            "Wrong final port: %s" % json_data[9]["configuration"]["name"]
        info("### Correct set of ports returned ###\n")

        info("\n########## End Test to Validate pagination of GET request" +
             " results ##########\n")


class Test_QueryPortPagination:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_QueryPortPagination.test_var = QueryPortPaginationTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)
        # Create NUM_PORTS test ports
        status_code = \
            create_test_ports(Test_QueryPortPagination.test_var.SWITCH_IP,
                              NUM_PORTS)
        assert status_code == httplib.CREATED, "Failed to create test ports"

    def teardown_class(cls):
        Test_QueryPortPagination.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test_pagination_indexes()
        self.test_var.test_query_ports_paginated()
