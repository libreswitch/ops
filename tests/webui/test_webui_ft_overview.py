#!/usr/bin/env python
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
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

from opsvsiutils.restutils.utils import execute_request, get_switch_ip, \
    get_json, rest_sanity_check, login

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class myTopo(Topo):

    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class Test_OverviewData(OpsVsiTest):
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
        self.PATHBASE = "/rest/v1/system/subsystems/base"
        self.PATHSYS = "/rest/v1/system"
        self.cookie_header = None

    def test_overview_data(self):
        info("\n########## Test to Validate Base Info ##########\n")
        # Get data
        status_code, response_data = execute_request(
            self.PATHBASE, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to get base information"

        # Verify Data
        json_data = get_json(response_data)
        other_info = json_data["status"]["other_info"]

        required_keys = {'Product Name', 'part_number', 'onie_version',
                         'base_mac_address', 'serial_number', 'vendor',
                         'max_interface_speed', 'max_transmission_unit',
                         'interface_count'}

        for key in required_keys:
            assert key in other_info, "Missing key %s" % key

        info("\n########## Base Data Validated ##########\n")

        info("\n########## Test to Validate System Info ##########\n")
        # Get data
        status_code, response_data = execute_request(
            self.PATHSYS, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)
        assert status_code == httplib.OK, "Failed to get base information"

        # Verify Data
        json_data = get_json(response_data)
        system_config = json_data["configuration"]
        system_status = json_data["status"]

        assert 'hostname' in system_config, "Missing key %s" % key
        assert 'switch_version' in system_status, "Missing key %s" % key

        info("\n########## System Data Validated ##########\n")


class Test_OverviewPage:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_OverviewPage.test_var = Test_OverviewData()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_OverviewPage.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test_overview_data()
