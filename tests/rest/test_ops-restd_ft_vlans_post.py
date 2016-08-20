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

from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, get_container_id, \
    get_server_crt, remove_server_crt
from opsvsiutils.restutils.swagger_test_utility import \
    swagger_model_verification

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

base_vlan_data = {
    "configuration": {
        "name": "test",
        "id": 2,
        "description": "test_vlan",
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

default_bridge = "bridge_normal"


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
#   Create a fake vlan to bridge_normal                                       #
#                                                                             #
###############################################################################
@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.switch_ip)


class CreateBasicVlan(OpsVsiTest):
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
        self.vlan_path = "%s/%s/vlans" % (self.path, default_bridge)
        self.cookie_header = None

    def test(self):
        data = """
               {
                   "configuration": {
                       "name": "fake_vlan_1",
                       "id": 2,
                       "description": "test vlan",
                       "admin": ["up"],
                       "other_config": {},
                       "external_ids": {}
                   }
               }
               """

        info("\n########## Executing POST to /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        response_status, response_data = execute_request(
            self.vlan_path, "POST", data, self.switch_ip,
            xtra_header=self.cookie_header)

        assert response_status == httplib.CREATED, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing POST to /system/bridges DONE ##########\n")


class TestPostBasicVlan:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPostBasicVlan.test_var = CreateBasicVlan()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)
        cls.container_id = get_container_id(cls.test_var.net.switches[0])

    def teardown_class(cls):
        TestPostBasicVlan.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        info("container_id_test %s\n" % self.container_id)
        swagger_model_verification(self.container_id,
                                   "/system/bridges/{pid}/vlans",
                                   "POST", base_vlan_data)
        self.test_var.test()


###############################################################################
#                                                                             #
#   Create a VLAN to bridge_normal using an invalid name                      #
#                                                                             #
###############################################################################
class CreateVlanInvalidName(OpsVsiTest):
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
        self.vlan_path = "%s/%s/vlans" % (self.path, default_bridge)
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

        info("\n########## Executing POST test with bad \"name\" "
             "value ##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"name\" as [%s] with value: %s\n" % (field,
                                                                      value))

            response_status, response_data = execute_request(
                self.vlan_path, "POST", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"name\" value "
             "DONE ##########\n")


class TestPostVlanInvalidName:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPostVlanInvalidName.test_var = CreateVlanInvalidName()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestPostVlanInvalidName.test_var.net.stop()
        remove_server_crt()

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
#   Create a VLAN to bridge_normal using an invalid ID                        #
#                                                                             #
###############################################################################
class CreateVlanInvalidId(OpsVsiTest):
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
        self.vlan_path = "%s/%s/vlans" % (self.path, default_bridge)
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
                self.vlan_path, "POST", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"id\" value DONE "
             "##########\n")


class TestPostVlanInvalidId:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPostVlanInvalidId.test_var = CreateVlanInvalidId()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestPostVlanInvalidId.test_var.net.stop()
        remove_server_crt()

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
#   Create a VLAN to bridge_normal using an invalid description               #
#                                                                             #
###############################################################################
class CreateVlanInvalidDescription(OpsVsiTest):
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
        self.vlan_path = "%s/%s/vlans" % (self.path, default_bridge)
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
            ["test_vlan_1", "test_vlan_3"]
        data["None"]["configuration"]["description"] = None
        data["boolean"]["configuration"]["description"] = True

        info("\n########## Executing POST test with bad \"description\" "
             "value ##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"description\" as [%s] with value: "
                 "%s\n" % (field, value))

            response_status, response_data = execute_request(
                self.vlan_path, "POST", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"description\" value "
             "DONE ##########\n")


class TestPostVlanInvalidDescription:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPostVlanInvalidDescription.test_var = \
            CreateVlanInvalidDescription()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestPostVlanInvalidDescription.test_var.net.stop()
        remove_server_crt()

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
#   Create a VLAN to bridge_normal using an invalid admin                     #
#                                                                             #
###############################################################################
class CreateVlanInvalidAdmin(OpsVsiTest):
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
        self.vlan_path = "%s/%s/vlans" % (self.path, default_bridge)
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

        info("\n########## Executing POST test with bad \"admin\" value "
             "##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"admin\" as %s with value: %s\n" % (field,
                                                                     value))

            response_status, response_data = execute_request(
                self.vlan_path, "POST", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"admin\" value "
             "DONE ##########\n")


class TestPostVlanInvalidAdmin:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPostVlanInvalidAdmin.test_var = CreateVlanInvalidAdmin()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestPostVlanInvalidAdmin.test_var.net.stop()
        remove_server_crt()

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
#   Create a VLAN to bridge_normal using an invalid other_config              #
#                                                                             #
###############################################################################
class CreateVlanInvalidOtherConfig(OpsVsiTest):
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
        self.vlan_path = "%s/%s/vlans" % (self.path, default_bridge)
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

        info("\n########## Executing POST test with bad \"other_config\" "
             "value ##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"other_config\" as [%s] with value: "
                 "%s\n" % (field, value))

            response_status, response_data = execute_request(
                self.vlan_path, "POST", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"other_config\" value "
             "DONE ##########\n")


class TestPostVlanInvalidOtherConfig:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPostVlanInvalidOtherConfig.test_var = \
            CreateVlanInvalidOtherConfig()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestPostVlanInvalidOtherConfig.test_var.net.stop()
        remove_server_crt()

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
#   Create a VLAN to bridge_normal using an invalid external_ids              #
#                                                                             #
###############################################################################
class CreateVlanInvalidExternalIds(OpsVsiTest):
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
        self.vlan_path = "%s/%s/vlans" % (self.path, default_bridge)
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

        info("\n########## Executing POST test with bad \"external_ids\" "
             "value ##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing field \"external_ids\" as %s with value: "
                 "%s\n" % (field, value))

            response_status, response_data = execute_request(
                self.vlan_path, "POST", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with bad \"external_ids\" value "
             "DONE ##########\n")


class TestPostVlanInvalidExternalIds:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPostVlanInvalidExternalIds.test_var = \
            CreateVlanInvalidExternalIds()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestPostVlanInvalidExternalIds.test_var.net.stop()
        remove_server_crt()

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
#   Create a VLAN to bridge_normal with missing fields                        #
#                                                                             #
###############################################################################
class CreateVlanMissingFields(OpsVsiTest):
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
        self.vlan_path = "%s/%s/vlans" % (self.path, default_bridge)
        self.cookie_header = None

    def test(self):
        data = {}
        data["name"] = deepcopy(base_vlan_data)
        data["id"] = deepcopy(base_vlan_data)

        data["name"]["configuration"].pop("name")
        data["id"]["configuration"].pop("id")

        info("\n########## Executing POST test with missing fields "
             "##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        for field, value in data.iteritems():
            info("Testing missing field \"%s\" with value: %s\n" % (field,
                                                                    value))

            response_status, response_data = execute_request(
                self.vlan_path, "POST", json.dumps(value), self.switch_ip,
                xtra_header=self.cookie_header)

            assert response_status == httplib.BAD_REQUEST, \
                "Response status received: %s\n" % response_status
            info("Response status received: \"%s\"\n" % response_status)

            assert response_data is not "", \
                "Response data received: %s\n" % response_data
            info("Response data received: %s\n" % response_data)

        info("########## Executing POST test with missing fields DONE "
             "##########\n")


class TestPostVlanMissingFields:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPostVlanMissingFields.test_var = CreateVlanMissingFields()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestPostVlanMissingFields.test_var.net.stop()
        remove_server_crt()

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
#   Create a VLAN that already exits to bridge_normal                         #
#                                                                             #
###############################################################################
class CreateVlanDuplicated(OpsVsiTest):
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
        self.vlan_path = "%s/%s/vlans" % (self.path, default_bridge)
        self.cookie_header = None

    def test(self):
        data = """
               {
                   "configuration": {
                       "name": "fake_vlan_1",
                       "id": 2,
                       "description": "test vlan",
                       "admin": ["up"],
                       "other_config": {},
                       "external_ids": {}
                   }
               }
               """

        info("\n########## Executing POST to /system/bridges ##########\n")
        info("Testing Path: %s\n" % self.vlan_path)

        response_status, response_data = execute_request(
            self.vlan_path, "POST", data, self.switch_ip,
            xtra_header=self.cookie_header)

        assert response_status == httplib.CREATED, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        # Create duplicated
        response_status, response_data = execute_request(
            self.vlan_path, "POST", data, self.switch_ip,
            xtra_header=self.cookie_header)

        assert response_status == httplib.BAD_REQUEST, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is not "", \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing POST to test duplicated VLAN DONE "
             "##########\n")


class TestPostDuplicated:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestPostDuplicated.test_var = CreateVlanDuplicated()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestPostDuplicated.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()
