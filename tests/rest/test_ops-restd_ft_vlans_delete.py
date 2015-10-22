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
                        "other_config": {},
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
    def test_delete_vlan(self):
        fake_vlan = "fake_vlan_1"
        delete_path = "%s/%s" % (self.test_path, fake_vlan)
        expected_data = ["/rest/v1/system/bridges/%s/vlans/%s" % (self.fake_bridge, fake_vlan)]

        #######################################################################
        # POST bridge and VLAN
        #######################################################################
        self.create_fake_bridge(self.fake_bridge)
        self.create_fake_vlan(self.fake_bridge, fake_vlan)

        #######################################################################
        # GET added VLAN
        #######################################################################
        info("\n########## Executing GET to %s ##########\n" % self.test_path)
        info("Testing Path: %s\n" % self.test_path)

        response_status, response_data = request_test_utils.execute_request(self.test_path, "GET", None, self.switch_ip)

        assert response_status == httplib.OK, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert json.loads(response_data) == expected_data, "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing GET to %s DONE ##########\n" % self.test_path)

        #######################################################################
        # DELETE added VLAN
        #######################################################################
        info("\n########## Executing DELETE to %s ##########\n" % delete_path)

        response_status, response_data = request_test_utils.execute_request(delete_path, "DELETE", None, self.switch_ip)

        assert response_status == httplib.NO_CONTENT, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing DELETE to %s DONE ##########\n" % delete_path)

        #######################################################################
        # GET existing VLANs
        #######################################################################
        info("\n########## Executing GET to %s ##########\n" % self.test_path)
        info("Testing Path: %s\n" % self.test_path)

        response_status, response_data = request_test_utils.execute_request(self.test_path, "GET", None, self.switch_ip)

        assert response_status == httplib.OK, "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert json.loads(response_data) == [], "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing GET to %s DONE ##########\n" % self.test_path)

    def run_all(self):
        info("\n########## Starting VLAN DELETE tests ##########\n")
        self.test_delete_vlan()
        info("\n########## VLAN DELETE Tests DONE ##########\n\n")

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
