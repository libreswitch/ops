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

from opsvsiutils.restutils.fakes import create_fake_vlan
from opsvsiutils.restutils.utils import execute_request, login, \
    rest_sanity_check, get_switch_ip, get_server_crt, \
    remove_server_crt

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

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
#   Basic Delete for non-existent VLAN                                        #
#                                                                             #
###############################################################################
@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.switch_ip)


class DeleteNonExistentVlan(OpsVsiTest):
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
        delete_path = "%s/%s" % (self.vlan_path, self.vlan_name)
        info("\n########## Executing DELETE for %s ##########\n" %
             self.vlan_path)

        response_status, response_data = execute_request(
            delete_path, "DELETE", None, self.switch_ip,
            xtra_header=self.cookie_header)

        assert response_status == httplib.NOT_FOUND, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing DELETE for %s DONE "
             "##########\n" % self.vlan_path)


class TestDeleteNonExistentVlan:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestDeleteNonExistentVlan.test_var = DeleteNonExistentVlan()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        TestDeleteNonExistentVlan.test_var.net.stop()
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
#   Basic Delete for existent VLAN                                            #
#                                                                             #
###############################################################################
class DeleteExistentVlan(OpsVsiTest):
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
        delete_path = "%s/%s" % (self.vlan_path, self.vlan_name)

        #######################################################################
        # DELETE added VLAN
        #######################################################################
        info("\n########## Executing DELETE for %s ##########\n" % delete_path)

        response_status, response_data = execute_request(
            delete_path, "DELETE", None, self.switch_ip,
            xtra_header=self.cookie_header)

        assert response_status == httplib.NO_CONTENT, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        assert response_data is "", \
            "Response data received: %s\n" % response_data
        info("Response data received: %s\n" % response_data)

        info("########## Executing DELETE for %s DONE "
             "##########\n" % delete_path)

        #######################################################################
        # GET existing VLANs
        #######################################################################
        info("\n########## Executing GET for %s ##########\n" % self.vlan_path)
        info("Testing Path: %s\n" % self.vlan_path)

        response_status, response_data = execute_request(
            delete_path, "GET", None, self.switch_ip,
            xtra_header=self.cookie_header)

        assert response_status == httplib.NOT_FOUND, \
            "Response status received: %s\n" % response_status
        info("Response status received: \"%s\"\n" % response_status)

        info("########## Executing GET for %s DONE "
             "##########\n" % self.vlan_path)


class TestDeleteExistentVlan:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestDeleteExistentVlan.test_var = DeleteExistentVlan()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)
        create_fake_vlan(TestDeleteExistentVlan.test_var.vlan_path,
                         TestDeleteExistentVlan.test_var.switch_ip,
                         TestDeleteExistentVlan.test_var.vlan_name,
                         TestDeleteExistentVlan.test_var.vlan_id)

    def teardown_class(cls):
        TestDeleteExistentVlan.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()
