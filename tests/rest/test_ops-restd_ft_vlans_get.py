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
import subprocess

from opsvsiutils.restutils.fakes import create_fake_vlan
from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, get_container_id, \
    compare_dict
from opsvsiutils.restutils.swagger_test_utility import \
    swagger_model_verification

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

DEFAULT_BRIDGE = "bridge_normal"


###############################################################################
#                                                                             #
#   Common Tests topology                                                     #
#                                                                             #
###############################################################################
class myTopo(Topo):
    """
    Default network configuration for these tests
    """
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


###############################################################################
#                                                                             #
#   Query for Bridge Normal                                                   #
#                                                                             #
###############################################################################
@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.switch_ip)


class QueryDefaultBridgeNormal(OpsVsiTest):
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
        self.cookie_header = None

    def test(self):
        expected_data = ["/rest/v1/system/bridges/%s" % DEFAULT_BRIDGE]
        path = "/rest/v1/system/bridges"

        info("\n########## Executing GET to /system/bridges ##########\n")
        info("Testing Path: %s\n" % path)

        response_status, response_data = execute_request(
            path, "GET", None, self.switch_ip, xtra_header=self.cookie_header)

        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received: %s\n" % response_status)

        assert json.loads(response_data) == expected_data, \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing GET to /system/bridges DONE ##########\n")


class TestGetDefaultBridgeNormal:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestGetDefaultBridgeNormal.test_var = QueryDefaultBridgeNormal()
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestGetDefaultBridgeNormal.test_var.net.stop()

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
#   Retrieve VLANs Associated from bridge_normal                              #
#                                                                             #
###############################################################################
class QueryVlansAssociated(OpsVsiTest):
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
        self.cookie_header = None

    def test(self):
        expected_data = "%s/%s" % (self.vlan_path, self.vlan_name)
        path = self.vlan_path

        info("\n########## Executing GET to /system/bridges/{id}/vlans "
             "(VLAN added) ##########\n")
        info("Testing path: %s\n" % path)

        response_status, response_data = execute_request(
            path, "GET", None, self.switch_ip, xtra_header=self.cookie_header)

        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received: %s\n" % response_status)

        assert expected_data in json.loads(response_data), \
            "Response data received: %s\n" % response_data
        info("Response data received: %s" % response_data)

        info("########## Executing GET to /system/bridges/{id}/vlans "
             "(VLAN added) DONE ##########\n")


class TestGetVlansAssociated:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestGetVlansAssociated.test_var = QueryVlansAssociated()
        rest_sanity_check(cls.test_var.switch_ip)
        create_fake_vlan(TestGetVlansAssociated.test_var.vlan_path,
                         TestGetVlansAssociated.test_var.switch_ip,
                         TestGetVlansAssociated.test_var.vlan_name,
                         TestGetVlansAssociated.test_var.vlan_id)

    def teardown_class(cls):
        TestGetVlansAssociated.test_var.net.stop()

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
#   Retrieve VLAN by name from bridge_normal                                  #
#                                                                             #
###############################################################################
class QueryVlanByName(OpsVsiTest):
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
        self.cookie_header = None

    def test(self):
        path = "%s/%s" % (self.vlan_path, self.vlan_name)

        expected_configuration_data = {}
        expected_configuration_data["name"] = "%s" % self.vlan_name
        expected_configuration_data["id"] = 1
        expected_configuration_data["description"] = "test_vlan"
        expected_configuration_data["admin"] = "up"
        #expected_configuration_data["other_config"] = {}
        #expected_configuration_data["external_ids"] = {}

        info("\n########## Executing GET to /system/bridges/{id}/vlans/ "
             "{id} ##########\n")
        info("Testing path: %s\n" % path)

        response_status, response_data = execute_request(
            path, "GET", None, self.switch_ip, xtra_header=self.cookie_header)

        expected_response = json.loads(response_data)

        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received %s" % response_status)

        assert compare_dict(expected_response["configuration"],
                            expected_configuration_data), \
            "Response data received: %s\n" % response_data

        info("########## Executing GET to /system/bridges/{id}/vlans/{id} "
             "DONE ##########\n")


class TestGetVlanByName:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestGetVlanByName.test_var = QueryVlanByName()
        rest_sanity_check(cls.test_var.switch_ip)
        cls.fake_data = create_fake_vlan(TestGetVlanByName.test_var.vlan_path,
                                         TestGetVlanByName.test_var.switch_ip,
                                         TestGetVlanByName.test_var.vlan_name,
                                         TestGetVlanByName.test_var.vlan_id)

        cls.container_id = get_container_id(cls.test_var.net.switches[0])

    def teardown_class(cls):
        TestGetVlanByName.test_var.net.stop()

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
                                   "GET_ID", self.fake_data)
        self.test_var.test()


###############################################################################
#                                                                             #
#   Retrieve VLAN by name not associated from bridge_normal                   #
#                                                                             #
###############################################################################
class QueryNonExistentVlanByName(OpsVsiTest):
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
        self.vlan_name = "not_found"
        self.vlan_path = "%s/%s/vlans" % (self.path, DEFAULT_BRIDGE)
        self.cookie_header = None

    def test(self):
        path = "%s/%s" % (self.vlan_path, self.vlan_name)

        info("\n########## Executing GET to /system/bridges/{id}/vlans/{id} "
             "##########\n")
        info("Testing path: %s\n" % path)

        response_status, response_data = execute_request(
            path, "GET", None, self.switch_ip, xtra_header=self.cookie_header)

        assert response_status == httplib.NOT_FOUND, \
            "Response status received: %s\n" % response_status
        info("Response status received: %s\n" % response_status)

        assert response_data == "", \
            "Response data received: %s" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing GET to /system/bridges/{id}/vlans/{id} "
             "DONE ##########\n")


class TestGetNonExistentVlan:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestGetNonExistentVlan.test_var = QueryNonExistentVlanByName()
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestGetNonExistentVlan.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()
