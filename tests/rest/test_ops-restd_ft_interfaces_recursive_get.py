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

from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, get_json, rest_sanity_check

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class QueryInterfaceDepthTest(OpsVsiTest):
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
        self.PATH = "/rest/v1/system/interfaces"
        self.cookie_header = None

    def get_json(self, response_data):
        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        return json_data

    def validate_keys_complete_object(self, json_data):
        assert json_data["configuration"] is not None, \
            "configuration key is not present"
        assert json_data["statistics"] is not None, \
            "statistics key is not present"
        assert json_data["status"] is not None, "status key is not present"
        info("### Configuration, statistics and status keys present ###\n")

        return True

    def validate_keys_inner_object(self, json_data, json_expected_data):
        assert json_data["split_parent"] is not None, \
            "split_parent key is not present"
        info("### split_parent, split_children keys present ###\n")
        assert json_data == json_expected_data, \
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        assert json_data["split_parent"][0] == \
            json_expected_data["split_parent"][0], "URI is not received\n"
        info("### URI present in second level received ###\n")

        return True

    def test_recursive_get_depth_first_level(self):
        specific_interface_path = self.PATH + "/50-1"
        depth_interface_path = self.PATH + "?depth=1;name=50-1"
        status_code, expected_data = execute_request(
            specific_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        json_expected_data = self.get_json(expected_data)
        json_data = self.get_json(response_data)[0]

        info("\n########## Test to Validate recursive GET Interface 50-1 "
             "depth=1 request ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert self.validate_keys_complete_object(json_data)
        info("### Validated first level of depth ###\n")

        json_expected_data = json_expected_data["configuration"]
        json_data = json_data["configuration"]

        assert self.validate_keys_inner_object(json_data, json_expected_data)
        info("########## End Test to Validate recursive GET Interface 50-1 "
             "depth=1 request ##########\n")

    def test_recursive_get_depth_second_level(self):
        specific_interface_path = self.PATH + "/50"
        depth_interface_path = self.PATH + "?depth=2;name=50-1"
        status_code, expected_data = execute_request(
            specific_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        json_expected_data = self.get_json(expected_data)
        json_data = self.get_json(response_data)[0]

        info("\n########## Test to Validate recursive GET Interface 50-1 "
             "depth=2 request ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert self.validate_keys_complete_object(json_data)
        info("### Validated first level of depth ###\n")

        json_data = json_data["configuration"]["split_parent"][0]

        assert self.validate_keys_complete_object(json_data)
        info("### Validated second level of depth###\n")

        assert len(set(json_data["configuration"]) &
                   set(json_expected_data["configuration"])) > 0, \
            "Configuration data is not equal that posted data\n"
        assert json_data["configuration"]["split_children"].sort() == \
            json_expected_data["configuration"]["split_children"].sort(), \
            "Response data is not equal that expected data\n"
        info("### Data for the third level received ###\n")

        info("########## End Test to Validate recursive GET Interface 50-1 "
             "depth=2 request ##########\n")

    def test_recursive_get_validate_negative_depth_value(self):
        depth_interface_path = self.PATH + "?depth=-1"
        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        info("\n########## Test to Validate recursive GET Interface 50-1 "
             "depth=<negative value> request ##########\n")

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST for URI: %s ###\n" %
             depth_interface_path)

        info("########## End Test to Validate recursive GET Interface 50-1 "
             "depth=<negative value> request ##########\n")

    def test_recursive_get_validate_string_depth_value(self):
        depth_interface_path = self.PATH + "?depth=a"
        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        info("\n########## Test to Validate recursive GET Interface 50-1 "
             "depth=<string> request ##########\n")

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST for URI: %s ###\n" %
             depth_interface_path)

        info("########## End Test to Validate recursive GET Interface 50-1 "
             "depth=<string> request ##########\n")

    def test_recursive_get_validate_with_depth_zero(self):
        expected_data = self.PATH + "/50"
        depth_interface_path = self.PATH + "?depth=0"
        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        json_data = self.get_json(response_data)

        info("\n########## Test to Validate recursive GET interfaces "
             "with depth=0 request ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        assert len(json_data) > 0, "Wrong interfaces size %s " % len(json_data)
        assert expected_data in json_data, \
            "Expected URI not present in response data"
        info("### There is at least one interface  ###\n")

        info("########## End Test to Validate recursive GET interfaces "
             "with depth=0 request ##########\n")

    def test_all_interfaces_no_depth_parameter(self):
        expected_data = self.PATH + "/50"
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        json_data = self.get_json(response_data)

        info("\n########## Test to Validate first GET all Interfaces "
             "no depth parameter request ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        assert len(json_data) > 0, "Wrong interfaces size %s " % len(json_data)
        assert expected_data in json_data, \
            "Expected URI not present in response data"
        info("### There is at least one interface  ###\n")

        info("########## End Test to Validate first GET all Interfaces "
             "no depth parameter request ##########\n")

    def test_recursive_get_depth_first_level_specific_uri(self):
        specific_interface_path = self.PATH + "?depth=1;name=50-1"
        depth_interface_path = self.PATH + "/50-1?depth=1"
        status_code, expected_data = execute_request(
            specific_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        json_expected_data = self.get_json(expected_data)[0]
        json_data = self.get_json(response_data)

        info("\n########## Test to Validate recursive GET Interface 50-1 "
             "depth=1 specific uri request ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert self.validate_keys_complete_object(json_data)
        info("### Validated first level of depth ###\n")

        json_expected_data = json_expected_data["configuration"]
        json_data = json_data["configuration"]

        assert self.validate_keys_inner_object(json_data, json_expected_data)
        info("########## End Test to Validate recursive GET Interface 50-1 "
             "depth=1 specific uri request ##########\n")

    def test_recursive_get_depth_second_level_specific_uri(self):
        specific_interface_path = self.PATH + "?depth=2;name=50-1"
        depth_interface_path = self.PATH + "/50-1?depth=2"
        status_code, expected_data = execute_request(
            specific_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        json_expected_data = self.get_json(expected_data)[0]
        json_data = self.get_json(response_data)

        info("\n########## Test to Validate recursive GET Interface 50-1 "
             "depth=2 specific uri request ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert self.validate_keys_complete_object(json_data)
        info("### Validated first level of depth###\n")

        json_data = json_data["configuration"]["split_parent"][0]
        json_expected_data = \
            json_expected_data["configuration"]["split_parent"][0]

        assert self.validate_keys_complete_object(json_data)
        info("### Validated second level of depth###\n")

        assert len(set(json_data["configuration"]) &
                   set(json_expected_data["configuration"])) > 0, \
            "Configuration data is  not equal that posted data\n"

        assert json_data == json_expected_data, \
            "Response data is not equal that expected data\n"
        info("### Data for the third level received ###\n")

        info("########## End Test to Validate recursive GET Interface 50-1 "
             "depth=2 specific uri request ##########\n")

    def test_recursive_get_with_negative_depth_value_specific_uri(self):
        depth_interface_path = self.PATH + "/50-1?depth=-1"
        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        info("\n########## Test to Validate recursive GET Interface 50-1 "
             "depth=<negative value> specific uri request\n")

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST for URI: %s ###\n" %
             depth_interface_path)

        info("########## End Test to Validate recursive GET Interface 50-1 "
             "depth=<negative value> specific uri request\n")

    def test_recursive_get_with_string_depth_value_specific_uri(self):
        depth_interface_path = self.PATH + "/50-1?depth=a"
        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        info("\n########## Test to Validate recursive GET Interface 50-1 "
             "depth=<string> specific uri request\n")

        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Status code is BAD_REQUEST for URI: %s ###\n" %
             depth_interface_path)

        info("########## End Test to Validate recursive GET Interface 50-1 "
             "depth=<string> specific uri request\n")

    def test_recursive_get_specific_uri_with_depth_zero(self):
        specific_interface_path = self.PATH + "?depth=1;name=50-1"
        depth_interface_path = self.PATH + "/50-1?depth=0"
        status_code, expected_data = execute_request(
            specific_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)
        json_expected_data = self.get_json(expected_data)[0]
        json_data = self.get_json(response_data)

        info("\n########## Test to Validate GET specific Interface with "
             "depth=0 request ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        assert self.validate_keys_complete_object(json_data)
        info("### Validated first level of depth ###\n")

        json_data = json_data["configuration"]
        json_expected_data = json_expected_data["configuration"]

        assert self.validate_keys_inner_object(json_data, json_expected_data)
        info("########## End Test to Validate GET specific Interface with "
             "depth=0 request ##########\n")

    def test_recursive_get_specific_uri_no_depth_parameter(self):
        specific_interface_path = self.PATH + "?depth=1;name=50-1"
        depth_interface_path = self.PATH + "/50-1"
        status_code, expected_data = execute_request(
            specific_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        status_code, response_data = execute_request(
            depth_interface_path, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        json_expected_data = self.get_json(expected_data)[0]
        json_data = self.get_json(response_data)

        info("\n########## Test to Validate GET specific Interface with "
             "no depth request ##########\n")

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"

        assert self.validate_keys_complete_object(json_data)
        info("### Validated first level of depth ###\n")

        json_data = json_data["configuration"]
        json_expected_data = json_expected_data["configuration"]

        assert self.validate_keys_inner_object(json_data, json_expected_data)
        info("########## End Test to Validate GET specific Interface with "
             "no depth request ##########\n")

    def run_tests(self):
        """
        This method will inspect itself to retrieve all existing methods.

        Only methods that begin with "test_" will be executed.
        """
        methodlist = [n for n, v in inspect.getmembers(self,
                                                       inspect.ismethod)
                      if isinstance(v, types.MethodType)]

        info("\n########## Starting Recursive Get Tests ##########\n")
        for name in methodlist:
            if name.startswith("test_"):
                getattr(self, "%s" % name)()
        info("\n########## Ending Recursive Get Tests ##########\n")


class Test_QueryInterfaceDepth:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_QueryInterfaceDepth.test_var = QueryInterfaceDepthTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_QueryInterfaceDepth.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def _del_(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.run_tests()
