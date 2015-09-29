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

import request_test_utils
import port_test_utils


NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

class myTopo(Topo):
    def build (self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QueryPortTest (OpsVsiTest):
    def setupNet (self):
        self.SWITCH_IP = ""
        self.PATH = "/rest/v1/system/ports"
        self.PORT_PATH = self.PATH + "/Port1"

        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                                       switch=VsiOpenSwitch,
                                       host=None,
                                       link=None,
                                       controller=None,
                                       build=True)

    def setup_switch_ip(self):
        s1 = self.net.switches[0]
        self.SWITCH_IP = port_test_utils.get_switch_ip(s1)

    def query_all_ports (self):
        info("\n########## Test to Validate first GET all Ports request ##########\n")

        status_code, response_data = request_test_utils.execute_request(self.PATH, "GET", None, self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"
        info("### Response data returned: %s ###\n" % response_data)

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert len(json_data) > 0, "Wrong ports size %s " % len(json_data)
        info("### There is at least one port  ###\n")

        assert self.PORT_PATH in json_data, "Port is not in data. Data returned is: %s" % response_data[0]
        info("### Port is in list  ###\n")

        info("\n########## End Test to Validate first GET all Ports request ##########\n")

    def query_port (self):
        info("\n########## Test to Validate first GET single Port request ##########\n")

        status_code, response_data = request_test_utils.execute_request(self.PORT_PATH, "GET", None, self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        assert response_data is not None, "Response data is empty"
        info("### Response data returned: %s ###\n" % response_data)

        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert json_data["configuration"] is not None, "configuration key is not present"
        assert json_data["statistics"] is not None, "statistics key is not present"
        assert json_data["status"] is not None, "status key is not present"
        info("### Configuration, statistics and status keys present ###\n")

        assert json_data["configuration"] == port_test_utils.test_data["configuration"], "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        info("\n########## End Test to Validate first GET single Port request ##########\n")

    def query_non_existent_port(self):
        info("\n########## Test to Validate first GET Non-existent Port request ##########\n")

        new_path = self.PATH + "/Port2"
        status_code, response_data = request_test_utils.execute_request(new_path, "GET", None, self.SWITCH_IP)

        assert status_code == httplib.NOT_FOUND, "Wrong status code %s " % status_code
        info("### Status code is NOT FOUND ###\n")

        info("\n########## End Test to Validate first GET Non-existent Port request ##########\n")

class Test_QueryPort:
    def setup (self):
        pass

    def teardown (self):
        pass

    def setup_class (cls):
        Test_QueryPort.test_var = QueryPortTest()
        Test_QueryPort.test_var.setup_switch_ip()
        # Add a test port
        port_test_utils.create_test_port(Test_QueryPort.test_var.SWITCH_IP)

    def teardown_class (cls):
        Test_QueryPort.test_var.net.stop()

    def setup_method (self, method):
        pass

    def teardown_method (self, method):
        pass

    def __del__ (self):
        del self.test_var

    def test_run (self):
        self.test_var.query_all_ports()
        self.test_var.query_port()
        self.test_var.query_non_existent_port()
