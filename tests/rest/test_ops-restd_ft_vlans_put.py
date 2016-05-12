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
from copy import deepcopy

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import urllib
import subprocess

from opsvsiutils.restutils.fakes import create_fake_vlan
from opsvsiutils.restutils.utils import get_switch_ip, execute_request, \
    rest_sanity_check, get_json, login, get_container_id
from opsvsiutils.restutils.swagger_test_utility import \
    swagger_model_verification

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

base_vlan_data = {
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}

test_vlan_data = {}
test_vlan_data["int"] = deepcopy(base_vlan_data)
test_vlan_data["string"] = deepcopy(base_vlan_data)
test_vlan_data["dict"] = deepcopy(base_vlan_data)
test_vlan_data["empty_array"] = deepcopy(base_vlan_data)
test_vlan_data["one_string"] = deepcopy(base_vlan_data)
test_vlan_data["multiple_string"] = deepcopy(base_vlan_data)
test_vlan_data["None"] = deepcopy(base_vlan_data)
test_vlan_data["boolean"] = deepcopy(base_vlan_data)

DEFAULT_BRIDGE = "bridge_normal"


###############################################################################
#                                                                             #
#   Common Tests topology                                                     #
#                                                                             #
###############################################################################
class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


###############################################################################
#                                                                             #
#   Basic update to existing VLAN                                             #
#                                                                             #
###############################################################################
@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class UpdateExistingVlan(OpsVsiTest):
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

        self.path = "/rest/v1/system/bridges"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.vlan_id = 1
        self.vlan_name = "fake_vlan"
        self.vlan_path = "%s/%s/vlans" % (self.path, DEFAULT_BRIDGE)
        self.vlan = "%s/%s/vlans/%s" % (self.path,
                                        DEFAULT_BRIDGE,
                                        self.vlan_name)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.cookie_header = None

    def test(self):
        data = deepcopy(base_vlan_data)
        data["configuration"]["name"] = self.vlan_name

        info("\n########## Executing PUT to %s ##########\n" % self.vlan_path)
        info("Testing Path: %s\n" % self.vlan_path)

        response_status, response_data = execute_request(
            self.vlan, "PUT", json.dumps(data), self.switch_ip,
            xtra_header=self.cookie_header)

        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing PUT to %s DONE "
             "##########\n" % self.vlan_path)


class TestPutExistingVlan:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPutExistingVlan.test_var = UpdateExistingVlan()
        rest_sanity_check(cls.test_var.switch_ip)
        create_fake_vlan(TestPutExistingVlan.test_var.vlan_path,
                         TestPutExistingVlan.test_var.switch_ip,
                         TestPutExistingVlan.test_var.vlan_name,
                         TestPutExistingVlan.test_var.vlan_id)

        cls.container_id = get_container_id(cls.test_var.net.switches[0])

    def teardown_class(cls):
        TestPutExistingVlan.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        info("container_id_test %s\n" % self.container_id)
        swagger_model_verification(self.container_id,
                                   "/system/bridges/{pid}/vlans/{id}",
                                   "PUT", base_vlan_data)
        self.test_var.test()


###############################################################################
#                                                                             #
#   Update VLAN name field with invalid values                                #
#                                                                             #
###############################################################################


class UpdateVlanInvalidName(OpsVsiTest):
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

        self.path = "/rest/v1/system/bridges"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.vlan_id = 1
        self.vlan_name = "fake_vlan"
        self.vlan_path = "%s/%s/vlans" % (self.path, DEFAULT_BRIDGE)
        self.vlan = "%s/%s/vlans/%s" % (self.path,
                                        DEFAULT_BRIDGE,
                                        self.vlan_name)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.cookie_header = None

    def test(self):
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("string")
        data.pop("one_string")

        data["int"]["configuration"]["name"] = 1
        data["dict"]["configuration"]["name"] = {}
        data["empty_array"]["configuration"]["name"] = []
        data["multiple_string"]["configuration"]["name"] = ["test_vlan_1",
                                                            "test_vlan_2"]
        data["None"]["configuration"]["name"] = None
        data["boolean"]["configuration"]["name"] = True

        info("\n########## Executing POST test with bad \"name\" value "
             "##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"name\" as [%s] with value: %s\n" % (field,
                                                                      value))

            response_status, response_data = execute_request(
                self.vlan, "PUT", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"name\" value DONE "
             "##########\n")


class TestPutVlanInvalidName:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPutVlanInvalidName.test_var = UpdateVlanInvalidName()
        rest_sanity_check(cls.test_var.switch_ip)
        create_fake_vlan(TestPutVlanInvalidName.test_var.vlan_path,
                         TestPutVlanInvalidName.test_var.switch_ip,
                         TestPutVlanInvalidName.test_var.vlan_name,
                         TestPutVlanInvalidName.test_var.vlan_id)

    def teardown_class(cls):
        TestPutVlanInvalidName.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()


###############################################################################
#                                                                             #
#   Update VLAN ID with invalid values                                        #
#                                                                             #
###############################################################################
class UpdateVlanInvalidId(OpsVsiTest):
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

        self.path = "/rest/v1/system/bridges"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.vlan_id = 1
        self.vlan_name = "fake_vlan"
        self.vlan_path = "%s/%s/vlans" % (self.path, DEFAULT_BRIDGE)
        self.vlan = "%s/%s/vlans/%s" % (self.path,
                                        DEFAULT_BRIDGE,
                                        self.vlan_name)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.cookie_header = None

    def test(self):
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("int")

        data["string"]["configuration"]["id"] = "id"
        data["dict"]["configuration"]["id"] = {}
        data["empty_array"]["configuration"]["id"] = []
        data["one_string"]["configuration"]["id"] = ["id"]
        data["multiple_string"]["configuration"]["id"] = ["test_vlan_1",
                                                          "test_vlan_2"]
        data["None"]["configuration"]["id"] = None
        data["boolean"]["configuration"]["id"] = True

        info("\n########## Executing POST test with bad \"id\" value "
             "##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"id\" as [%s] with value: %s\n" % (field,
                                                                    value))

            response_status, response_data = execute_request(
                self.vlan, "PUT", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"id\" value DONE "
             "##########\n")


class TestPutVlanInvalidId:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPutVlanInvalidId.test_var = UpdateVlanInvalidId()
        rest_sanity_check(cls.test_var.switch_ip)
        create_fake_vlan(TestPutVlanInvalidId.test_var.vlan_path,
                         TestPutVlanInvalidId.test_var.switch_ip,
                         TestPutVlanInvalidId.test_var.vlan_name,
                         TestPutVlanInvalidId.test_var.vlan_id)

    def teardown_class(cls):
        TestPutVlanInvalidId.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()


###############################################################################
#                                                                             #
#   Update VLAN description with invalid values                               #
#                                                                             #
###############################################################################
class UpdateVlanInvalidDescription(OpsVsiTest):
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

        self.path = "/rest/v1/system/bridges"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.vlan_id = 1
        self.vlan_name = "fake_vlan"
        self.vlan_path = "%s/%s/vlans" % (self.path, DEFAULT_BRIDGE)
        self.vlan = "%s/%s/vlans/%s" % (self.path,
                                        DEFAULT_BRIDGE,
                                        self.vlan_name)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.cookie_header = None

    def test(self):
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("string")
        data.pop("one_string")

        data["int"]["configuration"]["description"] = 1
        data["dict"]["configuration"]["description"] = {}
        data["empty_array"]["configuration"]["description"] = []
        data["multiple_string"]["configuration"]["description"] = \
            ["test_vlan_1", "test_vlan_2"]
        data["None"]["configuration"]["description"] = None
        data["boolean"]["configuration"]["description"] = True

        info("\n########## Executing PUT test with bad \"description\" "
             "value ##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"description\" as [%s] with value: "
                 "%s\n" % (field, value))

            response_status, response_data = execute_request(
                self.vlan, "PUT", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing PUT test with bad \"description\" value "
             "DONE ##########\n")


class TestPutVlanInvalidDescription:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPutVlanInvalidDescription.test_var = UpdateVlanInvalidDescription()
        rest_sanity_check(cls.test_var.switch_ip)
        create_fake_vlan(TestPutVlanInvalidDescription.test_var.vlan_path,
                         TestPutVlanInvalidDescription.test_var.switch_ip,
                         TestPutVlanInvalidDescription.test_var.vlan_name,
                         TestPutVlanInvalidDescription.test_var.vlan_id)

    def teardown_class(cls):
        TestPutVlanInvalidDescription.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()


###############################################################################
#                                                                             #
#   Update VLAN Admin with invalid values                                     #
#                                                                             #
###############################################################################
class UpdateVlanInvalidAdmin(OpsVsiTest):
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

        self.path = "/rest/v1/system/bridges"
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.vlan_id = 1
        self.vlan_name = "fake_vlan"
        self.vlan_path = "%s/%s/vlans" % (self.path, DEFAULT_BRIDGE)
        self.vlan = "%s/%s/vlans/%s" % (self.path,
                                        DEFAULT_BRIDGE,
                                        self.vlan_name)
        self.cookie_header = None

    def test(self):
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("dict")

        data["int"]["configuration"]["admin"] = 1
        data["string"]["configuration"]["admin"] = "admin"
        data["empty_array"]["configuration"]["admin"] = []
        data["one_string"]["configuration"]["admin"] = ["admin"]
        data["multiple_string"]["configuration"]["admin"] = ["test_vlan_1",
                                                             "test_vlan_2"]
        data["None"]["configuration"]["admin"] = None
        data["boolean"]["configuration"]["admin"] = True

        info("\n########## Executing PUT test with bad \"admin\" value "
             "##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"admin\" as %s with value: %s\n" % (field,
                                                                     value))

            response_status, response_data = execute_request(
                self.vlan, "PUT", json.dumps(value), self.SWITCH_IP,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing PUT test with bad \"admin\" value DONE "
             "##########\n")


class TestPutVlanInvalidAdmin:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPutVlanInvalidAdmin.test_var = UpdateVlanInvalidAdmin()
        rest_sanity_check(cls.test_var.SWITCH_IP)
        create_fake_vlan(TestPutVlanInvalidAdmin.test_var.vlan_path,
                         TestPutVlanInvalidAdmin.test_var.SWITCH_IP,
                         TestPutVlanInvalidAdmin.test_var.vlan_name,
                         TestPutVlanInvalidAdmin.test_var.vlan_id)

    def teardown_class(cls):
        TestPutVlanInvalidAdmin.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()


###############################################################################
#                                                                             #
#   Update VLAN Other_config with invalid values                              #
#                                                                             #
###############################################################################
class UpdateVlanInvalidOtherConfig(OpsVsiTest):
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

        self.path = "/rest/v1/system/bridges"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.vlan_id = 1
        self.vlan_name = "fake_vlan"
        self.vlan_path = "%s/%s/vlans" % (self.path, DEFAULT_BRIDGE)
        self.vlan = "%s/%s/vlans/%s" % (self.path,
                                        DEFAULT_BRIDGE,
                                        self.vlan_name)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.cookie_header = None

    def test(self):
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("dict")

        data["int"]["configuration"]["other_config"] = 1
        data["string"]["configuration"]["other_config"] = "other_config"
        data["empty_array"]["configuration"]["other_config"] = []
        data["one_string"]["configuration"]["other_config"] = ["other_config"]
        data["multiple_string"]["configuration"]["other_config"] = \
            ["test_vlan_1", "test_vlan_2"]
        data["None"]["configuration"]["other_config"] = None
        data["boolean"]["configuration"]["other_config"] = True

        info("\n########## Executing PUT test with bad \"other_config\" "
             "value ##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"other_config\" as [%s] with value: "
                 "%s\n" % (field, value))

            response_status, response_data = execute_request(
                self.vlan, "PUT", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing PUT test with bad \"other_config\" "
             "value DONE ##########\n")


class TestPutVlanInvalidOtherConfig:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPutVlanInvalidOtherConfig.test_var = UpdateVlanInvalidOtherConfig()
        rest_sanity_check(cls.test_var.switch_ip)
        create_fake_vlan(TestPutVlanInvalidOtherConfig.test_var.vlan_path,
                         TestPutVlanInvalidOtherConfig.test_var.switch_ip,
                         TestPutVlanInvalidOtherConfig.test_var.vlan_name,
                         TestPutVlanInvalidOtherConfig.test_var.vlan_id)

    def teardown_class(cls):
        TestPutVlanInvalidOtherConfig.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()


###############################################################################
#                                                                             #
#   Update VLAN External_ids with invalid values                              #
#                                                                             #
###############################################################################
class UpdateVlanInvalidExternalIds(OpsVsiTest):
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

        self.path = "/rest/v1/system/bridges"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.vlan_id = 1
        self.vlan_name = "fake_vlan"
        self.vlan_path = "%s/%s/vlans" % (self.path, DEFAULT_BRIDGE)
        self.vlan = "%s/%s/vlans/%s" % (self.path,
                                        DEFAULT_BRIDGE,
                                        self.vlan_name)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.cookie_header = None

    def test(self):
        data = deepcopy(test_vlan_data)

        # Remove same type keys
        data.pop("dict")

        data["int"]["configuration"]["external_ids"] = 1
        data["string"]["configuration"]["external_ids"] = "external_ids"
        data["empty_array"]["configuration"]["external_ids"] = []
        data["one_string"]["configuration"]["external_ids"] = ["external_ids"]
        data["multiple_string"]["configuration"]["external_ids"] = \
            ["test_vlan_1", "test_vlan_2"]
        data["None"]["configuration"]["external_ids"] = None
        data["boolean"]["configuration"]["external_ids"] = True

        info("\n########## Executing PUT test with bad \"external_ids\" "
             "value ##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"external_ids\" as %s with value: "
                 "%s\n" % (field, value))

            response_status, response_data = execute_request(
                self.vlan, "PUT", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing PUT test with bad \"external_ids\" value "
             "DONE ##########\n")


class TestPutVlanInvalidExternalIds:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPutVlanInvalidExternalIds.test_var = UpdateVlanInvalidExternalIds()
        rest_sanity_check(cls.test_var.switch_ip)
        create_fake_vlan(TestPutVlanInvalidExternalIds.test_var.vlan_path,
                         TestPutVlanInvalidExternalIds.test_var.switch_ip,
                         TestPutVlanInvalidExternalIds.test_var.vlan_name,
                         TestPutVlanInvalidExternalIds.test_var.vlan_id)

    def teardown_class(cls):
        TestPutVlanInvalidExternalIds.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()
