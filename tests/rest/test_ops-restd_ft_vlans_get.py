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

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import urllib

from utils.fakes import *
from utils.utils import *

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class configTest(OpsVsiTest):
    def setupNet(self):
        self.fake_bridge = "fake_bridge"

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
        self.switch_port = 8091

    ###########################################################################
    #                                                                         #
    #   Basic validation                                                      #
    #                                                                         #
    ###########################################################################
    def test_get_system_bridges(self):
        expected_data = ["/rest/v1/system/bridges/bridge_normal"]
        path = self.path

        info("\n########## Executing GET for /system/bridges ##########\n")
        info("Testing Path: %s\n" % path)

        response_status, response_data = execute_request(path,
                                                         "GET",
                                                         None,
                                                         self.switch_ip)
        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received: %s\n" % response_status)

        assert json.loads(response_data) == expected_data, \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing GET for /system/bridges DONE ##########\n")

    ###########################################################################
    #                                                                         #
    #   VLAN Tests                                                            #
    #                                                                         #
    ###########################################################################
    def test_get_system_bridges_id_no_vlans(self):
        path = "%s/%s/vlans" % (self.path, self.fake_bridge)

        info("\n########## Executing GET for /system/bridges/{id}/vlans "
             "(No VLANs added) ##########\n")
        info("Testing path: %s\n" % path)

        response_status, response_data = execute_request(path,
                                                         "GET",
                                                         None,
                                                         self.switch_ip)

        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received: %s\n" % response_status)

        assert json.loads(response_data) == []
        info("Response data received: %s\n" % response_data)

        info("########## Executing GET for /system/bridges/{id}/vlans "
             "(No VLANs added) DONE ##########\n")

    def test_get_system_bridges_id_with_vlans(self):
        fake_vlan = "fake_vlan_2"
        expected_data = \
            ["/rest/v1/system/bridges/%s/vlans/%s" % (self.fake_bridge,
                                                      fake_vlan)]
        path = "%s/%s/vlans" % (self.path, self.fake_bridge)

        create_fake_vlan(path, self.switch_ip, fake_vlan)

        info("\n########## Executing GET for /system/bridges/{id}/vlans "
             "(VLAN added) ##########\n")
        info("Testing path: %s\n" % path)

        response_status, response_data = execute_request(path,
                                                         "GET",
                                                         None,
                                                         self.switch_ip)

        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received: %s\n" % response_status)

        assert json.loads(response_data) == expected_data, \
            "Response data received: %s\n" % response_data
        info("Response data received: %s" % response_data)

        info("########## Executing GET for /system/bridges/{id}/vlans "
             "(VLAN added) DONE ##########\n")

    def test_get_system_bridges_id_vlans_id(self):
        fake_vlan = "fake_vlan_3"
        path = "%s/%s/vlans/%s" % (self.path, self.fake_bridge, fake_vlan)

        expected_configuration_data = {}
        expected_configuration_data["name"] = "%s" % fake_vlan
        expected_configuration_data["id"] = 1
        expected_configuration_data["description"] = "test_vlan"
        expected_configuration_data["admin"] = "up"
        expected_configuration_data["other_config"] = {}
        expected_configuration_data["external_ids"] = {}

        create_fake_vlan("%s/%s/vlans" % (self.path, self.fake_bridge),
                         self.switch_ip,
                         fake_vlan)

        info("\n########## Executing GET for /system/bridges/{id}/vlans/ "
             "{id} ##########\n")
        info("Testing path: %s\n" % path)

        response_status, response_data = execute_request(path,
                                                         "GET",
                                                         None,
                                                         self.switch_ip)
        expected_response = json.loads(response_data)

        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received %s" % response_status)

        assert compare_dict(expected_response["configuration"],
                            expected_configuration_data), \
            "Response data received: %s\n" % response_data

        info("########## Executing GET for /system/bridges/{id}/vlans/{id} "
             "DONE ##########\n")

    def test_get_system_bridges_id_vlans_id_not_found(self):
        fake_vlan = "fake_vlan_4"
        path = "%s/%s/vlans/not_found" % (self.path, self.fake_bridge)

        create_fake_vlan("%s/%s/vlans" % (self.path, self.fake_bridge),
                         self.switch_ip,
                         fake_vlan)

        info("\n########## Executing GET for /system/bridges/{id}/vlans/{id} "
             "##########\n")
        info("Testing path: %s\n" % path)

        response_status, response_data = execute_request(path,
                                                         "GET",
                                                         None,
                                                         self.switch_ip)

        assert response_status == httplib.NOT_FOUND, \
            "Response status received: %s\n" % response_status
        info("Response status received: %s\n" % response_status)

        assert response_data == "", \
            "Response data received: %s" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing GET for /system/bridges/{id}/vlans/{id} "
             "DONE ##########\n")

    def run_all(self):
        info("\n########## Starting VLAN POST tests ##########\n")
        self.test_get_system_bridges()

        create_fake_bridge(self.path, self.switch_ip, self.fake_bridge)

        self.test_get_system_bridges_id_no_vlans()
        self.test_get_system_bridges_id_with_vlans()
        self.test_get_system_bridges_id_vlans_id()
        self.test_get_system_bridges_id_vlans_id_not_found()
        info("\n########## VLAN POST Tests DONE ##########\n\n")


class Test_config:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_config.test_var = configTest()

    def teardown_class(cls):
        Test_config.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self):
        self.test_var.run_all()
