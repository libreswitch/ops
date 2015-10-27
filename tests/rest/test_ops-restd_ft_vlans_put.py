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

from utils.fakes import *
from utils.utils import *

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
        self.fake_vlan = "fake_vlan"

        self.net = Mininet(topo=myTopo(hsts = NUM_HOSTS_PER_SWITCH,
                                       sws = NUM_OF_SWITCHES,
                                       hopts = self.getHostOpts(),
                                       sopts = self.getSwitchOpts()),
                                       switch = VsiOpenSwitch,
                                       host = None,
                                       link = None,
                                       controller = None,
                                       build = True)

        self.path = "/rest/v1/system/bridges"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.switch_port = 8091
        self.test_path = "%s/%s/vlans/%s" % (self.path, self.fake_bridge, self.fake_vlan)

    ###########################################################################
    #                                                                         #
    #   Basic validation                                                      #
    #                                                                         #
    ###########################################################################
    def test_put_vlan(self):
        data = deepcopy(base_vlan_data)
        data["configuration"]["name"] = self.fake_vlan

        info("\n########## Executing PUT to %s ##########\n" % self.test_path)
        info("Testing Path: %s\n" % self.test_path)

        response_status, response_data = execute_request(self.test_path,
                                                                            "PUT",
                                                                            json.dumps(data),
                                                                            self.switch_ip)

        assert response_status == httplib.OK, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing PUT to %s DONE ##########\n" % self.test_path)

    ###########################################################################
    #                                                                         #
    #   Name validation                                                       #
    #                                                                         #
    ###########################################################################
    def test_put_vlan_bad_name(self):
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

            response_status, response_data = execute_request(self.test_path,
                                                                                "PUT",
                                                                                json.dumps(value),
                                                                                self.switch_ip)

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
    def test_put_vlan_bad_id(self):
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

            response_status, response_data = execute_request(self.test_path,
                                                                                "PUT",
                                                                                json.dumps(value),
                                                                                self.switch_ip)

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
    def test_put_vlan_bad_description(self):
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

        info("\n########## Executing PUT test with bad \"description\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"description\" as [%s] with value: %s\n" % (field, value))

            response_status, response_data = execute_request(self.test_path,
                                                                                "PUT",
                                                                                json.dumps(value),
                                                                                self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing PUT test with bad \"description\" value DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   Admin validation                                                      #
    #                                                                         #
    ###########################################################################
    def test_put_vlan_bad_admin(self):
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

        info("\n########## Executing PUT test with bad \"admin\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"admin\" as %s with value: %s\n" % (field, value))

            response_status, response_data = execute_request(self.test_path,
                                                                                "PUT",
                                                                                json.dumps(value),
                                                                                self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing PUT test with bad \"admin\" value DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   Other_Config validation                                               #
    #                                                                         #
    ###########################################################################
    def test_put_vlan_bad_other_config(self):
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

        info("\n########## Executing PUT test with bad \"other_config\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"other_config\" as [%s] with value: %s\n" % (field, value))

            response_status, response_data = execute_request(self.test_path,
                                                                                "POST",
                                                                                json.dumps(value),
                                                                                self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing PUT test with bad \"other_config\" value DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   External_ids validation                                               #
    #                                                                         #
    ###########################################################################
    def test_put_vlan_bad_external_ids(self):
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

        info("\n########## Executing PUT test with bad \"external_ids\" value ##########\n")
        info("Testing Path: %s\n" % self.test_path)

        for field, value in data.iteritems():
            info("Testing field \"external_ids\" as %s with value: %s\n" % (field, value))

            response_status, response_data = execute_request(self.test_path,
                                                                                "PUT",
                                                                                json.dumps(value),
                                                                                self.switch_ip)

            assert response_status == httplib.BAD_REQUEST, "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing PUT test with bad \"external_ids\" value DONE ##########\n")


    ###########################################################################
    #                                                                         #
    #   Tests Configuration                                                   #
    #                                                                         #
    ###########################################################################
    def run_all(self):
        info("\n########## Starting VLAN PUT tests ##########\n")
        create_fake_bridge(self.path, self.switch_ip, self.fake_bridge)
        create_fake_vlan("%s/%s/vlans" % (self.path, self.fake_bridge),
                         self.switch_ip,
                         self.fake_bridge,
                         self.fake_vlan)

        self.test_put_vlan()
        self.test_put_vlan_bad_name()
        self.test_put_vlan_bad_id()
        self.test_put_vlan_bad_description()
        self.test_put_vlan_bad_admin()
        self.test_put_vlan_bad_other_config()
        self.test_put_vlan_bad_external_ids()
        info("\n########## VLAN PUT Tests DONE ##########\n\n")

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
        self.test_var.run_all()
