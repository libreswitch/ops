#!/usr/bin/env python
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

import pytest
from copy import deepcopy

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import urllib

import request_test_utils
import port_test_utils

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

base_vlan_data = { "configuration": { "name": "test", "id": 1, "description": "test vlan", "admin": ["up"], "other_config": {}, "external_ids": {} } }

test_vlan_data = {}
test_vlan_data["int"]               = deepcopy(base_vlan_data)
test_vlan_data["string"]            = deepcopy(base_vlan_data)
test_vlan_data["dict"]              = deepcopy(base_vlan_data)
test_vlan_data["empty_array"]       = deepcopy(base_vlan_data)
test_vlan_data["one_string"]        = deepcopy(base_vlan_data)
test_vlan_data["multiple_string"]   = deepcopy(base_vlan_data)
test_vlan_data["None"]              = deepcopy(base_vlan_data)
test_vlan_data["boolean"]           = deepcopy(base_vlan_data)

class myTopo(Topo):
    def build (self, hsts=0, sws=1, **_opts):

        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")

class configTest (OpsVsiTest):
    def setupNet (self):
        self.fake_bridge = "fake_bridge"
        self.path = "/rest/v1/system/bridges"
        self.switch_ip = ""
        self.switch_port = 8091
        self.test_path = "%s/%s/vlans" % (self.path, self.fake_bridge)

        self.net = Mininet(topo=myTopo(hsts = NUM_HOSTS_PER_SWITCH,
                                       sws = NUM_OF_SWITCHES,
                                       hopts = self.getHostOpts(),
                                       sopts = self.getSwitchOpts()),
                                       switch = VsiOpenSwitch,
                                       host = None,
                                       link = None,
                                       controller = None,
                                       build = True)

    ###########################################################################
    #                                                                         #
    #   Utils                                                                 #
    #                                                                         #
    ###########################################################################
    def setup_switch_ip(self):
        self.switch_ip = port_test_utils.get_switch_ip(self.net.switches[0])

    def create_fake_port(self, fake_port_name):
        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "interfaces": ["/rest/v1/system/interfaces/1"],
                        "trunks": [413],
                        "ip4_address_secondary": ["192.168.0.1"],
                        "lacp": ["active"],
                        "bond_mode": ["l2-src-dst-hash"],
                        "tag": 654,
                        "vlan_mode": "trunk",
                        "ip6_address": ["2001:0db8:85a3:0000:0000:8a2e:0370:7334"],
                        "external_ids": {"extid1key": "extid1value"},
                        "bond_options": {"key1": "value1"},
                        "mac": ["01:23:45:67:89:ab"],
                        "other_config": {"cfg-1key": "cfg1val"},
                        "bond_active_slave": "null",
                        "ip6_address_secondary": ["01:23:45:67:89:ab"],
                        "vlan_options": {"opt1key": "opt2val"},
                        "ip4_address": "192.168.0.1",
                        "admin": "up"
                    },
                    "referenced_by": [{"uri": "/rest/v1/system/bridges/bridge_normal"}]
                }
                """ % fake_port_name

        path = "/rest/v1/system/ports"

        info("\n---------- Creating fake port (%s) ----------\n" % fake_port_name)
        info("Testing path: %s\nTesting data: %s\n" % (path, data))

        response_status, response_data = request_test_utils.execute_request(path, "POST", data, self.switch_ip)

        assert response.status == httplib.OK, "Response status received: %s\n" % response_status
        info("Fake port \"%s\" created!\n" % fake_port_name)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data: %s)" % response_data)
        info("---------- Creating fake port (%s) DONE ----------\n" % fake_port_name)

    def create_fake_vlan(self, bridge_name, fake_vlan_name):
        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "id": 1,
                        "description": "test vlan",
                        "admin": ["up"],
                        "other_config": {},
                        "external_ids": {}
                    }
                }
                """ % fake_vlan_name

        path = "%s/%s/vlans" % (self.path, bridge_name)

        info("\n---------- Creating fake vlan (%s) ----------\n" % fake_vlan_name)
        info("Testing Path: %s\nTesting Data: %s\n" % (path, data))

        response_status, response_data = request_test_utils.execute_request(path, "POST", data, self.switch_ip)

        assert response_status == httplib.CREATED, "Response status received: %s\n" % response_status
        info("Fake VLAN \"%s\" created!\n" % fake_vlan_name)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)
        info("---------- Creating fake vlan (%s) DONE ----------\n" % fake_vlan_name)

    def create_fake_bridge(self, fake_bridge_name):
        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "ports": [],
                        "vlans": [],
                        "datapath_type": "",
                        "other_config": {
                            "hwaddr": "",
                            "mac-table-size": "16",
                            "mac-aging-time": "300"
                        },
                        "external_ids": {}
                     }
                }
                """ % fake_bridge_name

        path = self.path

        info("\n---------- Creating fake bridge (%s) ----------\n" % fake_bridge_name)
        info("Testing path: %s\nTesting data: %s\n" % (path, data))

        response_status, response_data = request_test_utils.execute_request(path, "POST", data, self.switch_ip)

        assert response_status == httplib.CREATED, "Response status: %s\n" % response_status
        info("Bridge \"%s\" created!\n" % fake_bridge_name)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("---------- Creating fake bridge (%s) DONE ----------\n" % fake_bridge_name)

    ###########################################################################
    #                                                                         #
    #   Basic validation                                                      #
    #                                                                         #
    ###########################################################################
    def test_post_vlan(self):
        fake_vlan = "fake_vlan_1"

        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "id": 1,
                        "description": "test vlan",
                        "admin": ["up"],
                        "other_config": {},
                        "external_ids": {}
                    }
                }
                """ % fake_vlan

        info("\n########## Executing POST to /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data, self.switch_ip)

        assert response_status == httplib.CREATED, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing POST to /system/bridges DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   Name validation                                                       #
    #                                                                         #
    ###########################################################################
    def test_post_vlan_bad_name(self):
        fake_vlan = "fake_vlan_2"
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("string")
        data.pop("one_string")

        data["int"]["configuration"]["name"]                = 1
        data["dict"]["configuration"]["name"]               = {}
        data["empty_array"]["configuration"]["name"]        = []
        data["multiple_string"]["configuration"]["name"]    = ["test_vlan_1", "test_vlan_2"]
        data["None"]["configuration"]["name"]               = None
        data["boolean"]["configuration"]["name"]            = True

        info("\n########## Executing POST test with bad \"name\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"name\" as [%s] with value: %s\n" % (field, value))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", json.dumps(value), self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"name\" value DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   Id validation                                                         #
    #                                                                         #
    ###########################################################################
    def test_post_vlan_bad_id(self):
        fake_vlan = "fake_vlan_3"
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("int")

        data["string"]["configuration"]["id"]             = "id"
        data["dict"]["configuration"]["id"]               = {}
        data["empty_array"]["configuration"]["id"]        = []
        data["one_string"]["configuration"]["id"]         = ["id"]
        data["multiple_string"]["configuration"]["id"]    = ["test_vlan_1", "test_vlan_2"]
        data["None"]["configuration"]["id"]               = None
        data["boolean"]["configuration"]["id"]            = True

        info("\n########## Executing POST test with bad \"id\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"id\" as [%s] with value: %s\n" % (field, value))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", json.dumps(value), self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"id\" value DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   Description validation                                                #
    #                                                                         #
    ###########################################################################
    def test_post_vlan_bad_description(self):
        fake_vlan = "fake_vlan_4"
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("string")
        data.pop("one_string")

        data["int"]["configuration"]["description"]                = 1
        data["dict"]["configuration"]["description"]               = {}
        data["empty_array"]["configuration"]["description"]        = []
        data["multiple_string"]["configuration"]["description"]    = ["test_vlan_1", "test_vlan_2"]
        data["None"]["configuration"]["description"]               = None
        data["boolean"]["configuration"]["description"]            = True

        info("\n########## Executing POST test with bad \"description\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"description\" as [%s] with value: %s\n" % (field, value))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", json.dumps(value), self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"description\" value DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   Admin validation                                                      #
    #                                                                         #
    ###########################################################################
    def test_post_vlan_bad_admin(self):
        fake_vlan = "fake_vlan_5"
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("dict")

        data["int"]["configuration"]["admin"]                = 1
        data["string"]["configuration"]["admin"]             = "admin"
        data["empty_array"]["configuration"]["admin"]        = []
        data["one_string"]["configuration"]["admin"]         = ["admin"]
        data["multiple_string"]["configuration"]["admin"]    = ["test_vlan_1", "test_vlan_2"]
        data["None"]["configuration"]["admin"]               = None
        data["boolean"]["configuration"]["admin"]            = True

        info("\n########## Executing POST test with bad \"admin\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"admin\" as %s with value: %s\n" % (field, value))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", json.dumps(value), self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"admin\" value DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   Other_Config validation                                               #
    #                                                                         #
    ###########################################################################
    def test_post_vlan_bad_other_config(self):
        fake_vlan = "fake_vlan_6"
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("dict")

        data["int"]["configuration"]["other_config"]                = 1
        data["string"]["configuration"]["other_config"]             = "other_config"
        data["empty_array"]["configuration"]["other_config"]        = []
        data["one_string"]["configuration"]["other_config"]         = ["other_config"]
        data["multiple_string"]["configuration"]["other_config"]    = ["test_vlan_1", "test_vlan_2"]
        data["None"]["configuration"]["other_config"]               = None
        data["boolean"]["configuration"]["other_config"]            = True

        info("\n########## Executing POST test with bad \"other_config\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"other_config\" as [%s] with value: %s\n" % (field, value))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", json.dumps(value), self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"other_config\" value DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   External_ids validation                                               #
    #                                                                         #
    ###########################################################################
    def test_post_vlan_bad_external_ids(self):
        fake_vlan = "fake_vlan_7"
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("dict")

        data["int"]["configuration"]["external_ids"]                = 1
        data["string"]["configuration"]["external_ids"]             = "external_ids"
        data["empty_array"]["configuration"]["external_ids"]        = []
        data["one_string"]["configuration"]["external_ids"]         = ["external_ids"]
        data["multiple_string"]["configuration"]["external_ids"]    = ["test_vlan_1", "test_vlan_2"]
        data["None"]["configuration"]["external_ids"]               = None
        data["boolean"]["configuration"]["external_ids"]            = True

        info("\n########## Executing POST test with bad \"external_ids\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"external_ids\" as %s with value: %s\n" % (field, value))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", json.dumps(value), self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"external_ids\" value DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   Missing fields validation                                             #
    #                                                                         #
    ###########################################################################
    def test_post_vlan_bad_missing_fields(self):
        fake_vlan = "fake_vlan_8"

        data = {}
        data["name"]         = deepcopy(base_vlan_data)
        data["id"]           = deepcopy(base_vlan_data)
        data["description"]  = deepcopy(base_vlan_data)
        data["admin"]        = deepcopy(base_vlan_data)
        data["other_config"] = deepcopy(base_vlan_data)
        data["external_ids"] = deepcopy(base_vlan_data)

        data["name"]["configuration"].pop("name")
        data["id"]["configuration"].pop("id")
        data["description"]["configuration"].pop("description")
        data["admin"]["configuration"].pop("admin")
        data["other_config"]["configuration"].pop("other_config")
        data["external_ids"]["configuration"].pop("external_ids")

        info("\n########## Executing POST test with missing fields ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing missing field \"%s\" with value: %s\n" % (field, value))

            response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", json.dumps(value), self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with missing fields DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   Duplicated VLAN validation                                            #
    #                                                                         #
    ###########################################################################
    def test_post_vlan_duplicated(self):
        fake_vlan = "fake_vlan_9"

        data =  """
                {
                    "configuration": {
                        "name": "%s",
                        "id": 1,
                        "description": "test vlan",
                        "admin": ["up"],
                        "other_config": {},
                        "external_ids": {}
                    }
                }
                """ % fake_vlan

        info("\n########## Executing POST to test duplicated VLAN ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data, self.switch_ip)

        assert response_status == httplib.CREATED, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        # Create duplicated
        info("Creating VLAN duplicate: %s\n" % fake_vlan)
        response_status, response_data = request_test_utils.execute_request(self.test_path, "POST", data, self.switch_ip)

        assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is not "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing POST to test duplicated VLAN DONE ##########\n")

    def run_all(self):
        info("\n########## Starting VLAN POST tests ##########\n")
        self.create_fake_bridge(self.fake_bridge)
        self.test_post_vlan()
        self.test_post_vlan_bad_name()
        self.test_post_vlan_bad_id()
        self.test_post_vlan_bad_description()
        self.test_post_vlan_bad_admin()
        self.test_post_vlan_bad_other_config()
        self.test_post_vlan_bad_external_ids()
        self.test_post_vlan_bad_missing_fields()
        self.test_post_vlan_duplicated()
        info("\n########## VLAN POST Tests DONE ##########\n\n")

class Test_config:
    def setup (self):
        pass

    def teardown (self):
        pass

    def setup_class (cls):
        Test_config.test_var = configTest()

    def teardown_class (cls):
        Test_config.test_var.net.stop()

    def setup_method (self, method):
        pass

    def teardown_method (self, method):
        pass

    def __del__ (self):
        del self.test_var

    def test_run (self):
        self.test_var.setup_switch_ip()
        self.test_var.run_all()
