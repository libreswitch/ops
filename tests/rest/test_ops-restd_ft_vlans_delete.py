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
        self.test_path = "%s/%s/vlans" % (self.path, self.fake_bridge)

    ###########################################################################
    #                                                                         #
    #   Basic validation                                                      #
    #                                                                         #
    ###########################################################################
    def test_delete_vlan(self):
        fake_vlan = "fake_vlan_1"
        delete_path = "%s/%s" % (self.test_path, fake_vlan)
        expected_data = \
            ["/rest/v1/system/bridges/%s/vlans/%s" % (self.fake_bridge,
                                                      fake_vlan)]

        #######################################################################
        # POST bridge and VLAN
        #######################################################################
        create_fake_bridge(self.path,
                           self.switch_ip,
                           self.fake_bridge)

        create_fake_vlan("%s/%s/vlans" % (self.path, self.fake_bridge),
                         self.switch_ip,
                         fake_vlan)

        #######################################################################
        # GET added VLAN
        #######################################################################
        info("\n########## Executing GET to %s ##########\n" % self.test_path)
        info("Testing Path: %s\n" % self.test_path)

        response_status, response_data = execute_request(self.test_path,
                                                         "GET",
                                                         None,
                                                         self.switch_ip)

        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert json.loads(response_data) == expected_data, \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing GET to %s DONE "
             "##########\n" % self.test_path)

        #######################################################################
        # DELETE added VLAN
        #######################################################################
        info("\n########## Executing DELETE to %s ##########\n" % delete_path)

        response_status, response_data = execute_request(delete_path,
                                                         "DELETE",
                                                         None,
                                                         self.switch_ip)

        assert response_status == httplib.NO_CONTENT, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing DELETE to %s DONE "
             "##########\n" % delete_path)

        #######################################################################
        # GET existing VLANs
        #######################################################################
        info("\n########## Executing GET to %s ##########\n" % self.test_path)
        info("Testing Path: %s\n" % self.test_path)

        response_status, response_data = execute_request(self.test_path,
                                                         "GET",
                                                         None,
                                                         self.switch_ip)

        assert response_status == httplib.OK, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert json.loads(response_data) == [], \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing GET to %s DONE "
             "##########\n" % self.test_path)

    def run_all(self):
        info("\n########## Starting VLAN DELETE tests ##########\n")
        self.test_delete_vlan()
        info("\n########## VLAN DELETE Tests DONE ##########\n\n")


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
