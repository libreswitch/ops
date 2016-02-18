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

from webui.utils.utils import *
import copy

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

ADMIN_PATCH_PORT = [{"op": "add",
                    "path": "/admin",
                    "value": "up"}]
ADMIN_PATCH_INT = [{"op": "add",
                    "path": "/user_config",
                    "value": {"admin": "up"}}]
basic_port_data = copy.deepcopy(BASIC_PORT_DATA)
basic_int_data = copy.deepcopy(BASIC_INT_DATA)


class myTopo(Topo):

    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class Test_CreatePatch(OpsVsiTest):
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
        self.PATH = "/rest/v1/system"
        self.PATH_PORTS = self.PATH + "/ports"
        self.PATH_INT = self.PATH + "/interfaces"

    def test_create_port(self):
        self.PORT_PATH = self.PATH_PORTS + "/1"
        info("\n########## Test to Validate Create Port ##########\n")
        status_code, response_data = execute_request(self.PATH_PORTS, "POST",
                                                     json.dumps(BASIC_PORT_DATA),
                                                     self.SWITCH_IP)
        assert status_code == httplib.CREATED, "Error creating a Port.Status" \
            + " code: %s Response data: %s " % (status_code, response_data)
        info("### Port Created. Status code is 201 CREATED  ###\n")

        # Verify data
        status_code, response_data = execute_request(self.PORT_PATH,
                                                     "GET",
                                                     None,
                                                     self.SWITCH_IP)
        assert status_code == httplib.OK, "Failed to query added Port"
        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert json_data["configuration"] == BASIC_PORT_DATA["configuration"],\
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        info("\n########## End Test to Validate Create Port ##########\n")

    def test_patch_port_int_admin(self):
        self.PORT_PATH = self.PATH_PORTS + "/2"
        self.INT_PATH = self.PATH_INT + "/2"
        basic_port_data["configuration"]["name"] = "2"
        basic_port_data["configuration"]["interfaces"] = \
            ["/rest/v1/system/interfaces/2"]
        basic_int_data["configuration"]["name"] = "2"
        # Create port
        status_code, response_data = execute_request(self.PATH_PORTS,
                                                     "POST",
                                                     json.dumps(basic_port_data),
                                                     self.SWITCH_IP)
        assert status_code == httplib.CREATED, "Error creating a Port. Status"\
            " code: %s Response data: %s " % (status_code, response_data)
        info("### Port Created. Status code is 201 CREATED  ###\n")

        # Verify data
        status_code, response_data = execute_request(self.PORT_PATH, "GET",
                                                     None,
                                                     self.SWITCH_IP)
        assert status_code == httplib.OK, "Failed to query added Port"
        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert json_data["configuration"] == basic_port_data["configuration"],\
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        info("\n########## Test to Validate Patch Port Int ##########\n")
        basic_port_data["configuration"]["admin"] = "up"
        basic_int_data["configuration"]["user_config"] = {}
        basic_int_data["configuration"]["user_config"]["admin"] = "up"
        status_code, response_data = execute_request(self.PORT_PATH, "PATCH",
                                                     json.dumps(ADMIN_PATCH_PORT),
                                                     self.SWITCH_IP,
                                                     False)
        assert status_code == httplib.NO_CONTENT, "Error patching a Port "\
            "Status code: %s Response data: %s " % (status_code, response_data)
        info("### Port Patched. Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(self.PORT_PATH, "GET",
                                                     None,
                                                     self.SWITCH_IP)
        assert status_code == httplib.OK, "Failed to query patched Port"
        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"
        assert json_data["configuration"] == basic_port_data["configuration"],\
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        status_code, response_data = execute_request(self.INT_PATH,
                                                     "PATCH",
                                                     json.dumps(ADMIN_PATCH_INT),
                                                     self.SWITCH_IP,
                                                     False)
        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(self.INT_PATH, "GET",
                                                     None,
                                                     self.SWITCH_IP)
        assert status_code == httplib.OK, "Failed to query patched Port"
        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"
        assert json_data["configuration"] == basic_int_data["configuration"],\
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        info("\n########## End Test Create And Patch Port Int ##########\n")


class Test_WebUIREST:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_WebUIREST.test_var = Test_CreatePatch()

    def teardown_class(cls):
        Test_WebUIREST.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self):
        self.test_var.test_create_port()
        self.test_var.test_patch_port_int_admin()
