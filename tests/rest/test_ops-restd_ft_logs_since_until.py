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
import subprocess
import time
import datetime

from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, get_json

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0
OFFSET_TEST = 0
LIMIT_TEST = 10


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class LogsSinceUntilTest (OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch, host=None, link=None,
                           controller=None, build=True)

        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.PATH = "/rest/v1/logs"
        self.cookie_header = None

    def verify_timestamp(self, json_data):
        for t in json_data:
            if t["__REALTIME_TIMESTAMP"] < (time.time() - 60):
                return False
        return True

    def logs_with_since_relative_filter(self):
        info("\n########## Test to Validate logs with since relative filter" +
             " ##########\n")

        bug_flag = True
        since_test = "1%20minute%20ago"

        self.LOGS_PATH = self.PATH + "?since=%s&offset=%s&limit=%s" % \
            (since_test, OFFSET_TEST, LIMIT_TEST)

        info("logs path %s" % self.LOGS_PATH)
        status_code, response_data = execute_request(
            self.LOGS_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"
        info("### Response data returned for logs with since filter  ###\n")

        json_data = get_json(response_data)
        info("### JSON data is in good shape ###\n")

        assert len(json_data) <= LIMIT_TEST, "Pagination limit failed %s " \
            % len(json_data)
        info("### Pagination for logs works fine ###\n")

        assert self.verify_timestamp(json_data), "Logs for incorrect \
            timestamp also displayed"
        info("### Since filter for logs is working fine ###\n")

        info("\n########## End Test to Validate logs with since relative" +
             " filter ##########\n")

    def logs_with_since_timestamp_filter(self):
        info("\n########## Test to Validate logs with since timestamp" +
             "##########\n")

        since_test = str(datetime.datetime.now()).split('.')[0]
        since_test = since_test.replace(" ", "%20")

        self.LOGS_PATH = self.PATH + "?since=%s&offset=%s&limit=%s" % \
            (since_test, OFFSET_TEST, LIMIT_TEST)
        status_code, response_data = execute_request(
            self.LOGS_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"
        info("### Response data returned for logs with since timestamp" +
             "filter ###\n")

        json_data = get_json(response_data)
        info("### JSON data is in good shape ###\n")

        assert len(json_data) <= LIMIT_TEST, "Pagination limit failed %s " \
            % len(json_data)
        info("### Pagination for logs works fine ###\n")

        assert self.verify_timestamp(json_data), "Logs for incorrect \
            timestamp also displayed"
        info("### Since filter for logs is working fine ###\n")

        info("\n########## End Test to Validate logs with since timestamp" +
             "##########\n")

    def logs_with_since_negative_test_cases(self):
        info("\n########## Test to Validate negative test cases for logs" +
             " with since timestamp ##########\n")

        since_test = "0000-00-00%2000:00:00"
        self.LOGS_PATH = self.PATH + "?since=%s&offset=%s&limit=%s" \
            % (since_test, OFFSET_TEST, LIMIT_TEST)
        status_code, response_data = execute_request(
            self.LOGS_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " \
            % status_code
        info("### Status code for since 0000-00-00 00:00:00 "
             "case is okay ###\n")

        since_test = "2050-01-01%2001:00:00"
        self.LOGS_PATH = self.PATH + "?since=%s&offset=%s&limit=%s" \
            % (since_test, OFFSET_TEST, LIMIT_TEST)
        status_code, response_data = execute_request(
            self.LOGS_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s "\
            % status_code
        info("### Status code for since 2050-01-01 01:00:00 case is OK ###\n")

        assert "Empty logs" in response_data, "Response data is empty"
        info("### Response data returned for empty logs returned fine  ###\n")

        since_test = "-1%20hour%20ago"
        self.LOGS_PATH = self.PATH + "?since=%s&offset=%s&limit=%s" \
            % (since_test, OFFSET_TEST, LIMIT_TEST)
        status_code, response_data = execute_request(
            self.LOGS_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s "\
            % status_code
        info("### Status code for since parameter with negative "
             "value is okay ###\n")

        info("\n########## End Test to Validate negative test case for logs" +
             " with since timestamp ##########\n")

    def logs_with_until_relative_filter(self):
        info("\n########## Test to Validate logs with until relative filter" +
             "##########\n")

        bug_flag = True
        until_test = "now"

        self.LOGS_PATH = self.PATH + "?until=%s&offset=%s&limit=%s" % \
            (until_test, OFFSET_TEST, LIMIT_TEST)

        info("logs path %s" % self.LOGS_PATH)
        status_code, response_data = execute_request(
            self.LOGS_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"
        info("### Response data returned for logs with until filter  ###\n")

        json_data = get_json(response_data)
        info("### JSON data is in good shape ###\n")

        assert len(json_data) <= LIMIT_TEST, "Pagination limit failed %s " \
            % len(json_data)
        info("### Pagination for logs works fine ###\n")

        assert self.verify_timestamp(json_data), "Logs for incorrect \
            timestamp also displayed"
        info("### Until filter for logs is working fine ###\n")

        info("\n########## End Test to Validate logs with until relative" +
             " filter ##########\n")

    def logs_with_until_timestamp_filter(self):
        info("\n########## Test to Validate logs with until timestamp" +
             "##########\n")

        until_test = str(datetime.datetime.utcnow()).split('.')[0]
        until_test = until_test.replace(" ", "%20")

        self.LOGS_PATH = self.PATH + "?until=%s&offset=%s&limit=%s" % \
            (until_test, OFFSET_TEST, LIMIT_TEST)
        status_code, response_data = execute_request(
            self.LOGS_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Wrong status code %s " \
            % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"
        info("### Response data returned for logs with until timestamp" +
             "filter ###\n")

        json_data = get_json(response_data)
        info("### JSON data is in good shape ###\n")

        assert len(json_data) <= LIMIT_TEST, "Pagination limit failed %s " \
            % len(json_data)
        info("### Pagination for logs works fine ###\n")

        assert self.verify_timestamp(json_data), "Logs for incorrect \
            timestamp also displayed"
        info("### Until filter for logs is working fine ###\n")

        info("\n########## End Test to Validate logs with until timestamp" +
             "##########\n")


class Test_LogsSinceUntil:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_LogsSinceUntil.test_var = LogsSinceUntilTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_LogsSinceUntil.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_logs_with_since_relative_filter(self, netop_login):
        self.test_var.logs_with_since_relative_filter()

    def test_logs_with_since_timestamp_filter(self, netop_login):
        self.test_var.logs_with_since_timestamp_filter()

    def test_logs_with_since_negative_test_cases(self, netop_login):
        self.test_var.logs_with_since_negative_test_cases()

    def test_logs_with_until_relative_filter(self, netop_login):
        self.test_var.logs_with_until_relative_filter()

    def test_logs_with_until_timestamp_filter(self, netop_login):
        self.test_var.logs_with_until_timestamp_filter()
