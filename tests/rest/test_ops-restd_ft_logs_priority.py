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
from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, get_json, rest_sanity_check

import json
import httplib
import urllib
import subprocess

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0
OFFSET_TEST = 0
LIMIT_TEST = 10
PRIORITY_TEST = 6


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class LogsPriorityTest (OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch, host=None, link=None,
                           controller=None, build=True)

        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.PATH = "/rest/v1/logs"
        self.LOGS_PATH = self.PATH
        self.cookie_header = None

    def logs_with_priority_filter(self):
        info("\n########## Test to Validate logs with priority parameter \
              ##########\n")

        self.LOGS_PATH = self.PATH + "?priority=%s&offset=%s&limit=%s" % \
            (PRIORITY_TEST, OFFSET_TEST, LIMIT_TEST)
        status_code, response_data = execute_request(
            self.LOGS_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"
        info("### Response data returned for logs with priority filter  ###\n")

        json_data = get_json(response_data)
        info("### JSON data is in good shape ###\n")

        assert len(json_data) <= LIMIT_TEST, "Pagination limit failed %s " \
            % len(json_data)
        info("### Pagination for logs works fine ###\n")

        flag = True
        for d in json_data:
            if int(d["PRIORITY"]) > PRIORITY_TEST:
                flag = False

        assert flag, "Logs for incorrect priority level displayed"
        info("### Priority filter for logs is working fine ###\n")

        info("\n########## End Test to Validate logs with priority \
             parameters ##########\n")

    def logs_with_priority_negative(self):
        info("\n########## Test to Validate logs with negative priority \
             parameter ##########\n")

        self.LOGS_PATH = self.PATH + "?priority=-1&offset=%s&limit=%s" % \
            (OFFSET_TEST, LIMIT_TEST)
        status_code, response_data = execute_request(
            self.LOGS_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " \
            % status_code
        info("### Status code is okay ###\n")

        info("\n########## End Test to Validate logs with negative priority \
             parameters ##########\n")


class Test_LogsPriority:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_LogsPriority.test_var = LogsPriorityTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_LogsPriority.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_logs_with_priority_filter(self, netop_login):
        self.test_var.logs_with_priority_filter()

    def test_logs_with_priority_negative(self, netop_login):
        self.test_var.logs_with_priority_negative()
