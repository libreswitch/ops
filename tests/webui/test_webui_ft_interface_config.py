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
    get_json, rest_sanity_check, login, get_server_crt, \
    remove_server_crt
import copy

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

ADM_PATCH_PRT = [{"op": "add",
                  "path": "/admin",
                  "value": "up"}]
ADM_PATCH_INT = [{"op": "add",
                  "path": "/user_config",
                  "value": {"admin": "up"}}]
OTHER_PATCH = [{"op": "add",
                "path": "/user_config",
                "value": {"autoneg": "off",
                          "duplex": "half",
                          "pause": "rxtx"}}]
REMOVE_PATCH = [{"op": "remove",
                 "path": "/user_config"}]
PORT_DATA = {
    "configuration": {
        "name": "1",
        "interfaces": ["/rest/v1/system/interfaces/1"]
    },
    "referenced_by": [{"uri": "/rest/v1/system/bridges/bridge_normal"}]
}

INT_DATA = {
    "configuration": {
    }
}


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


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
        self.cookie_header = None

    def test_patch_port_int_admin(self):
        port_data = copy.deepcopy(PORT_DATA)
        int_data = copy.deepcopy(INT_DATA)
        self.PORT_PATH = self.PATH_PORTS + "/1"
        self.INT_PATH = self.PATH_INT + "/1"
        # Create port
        status_code, response_data = execute_request(
            self.PATH_PORTS, "POST", json.dumps(port_data), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.CREATED, "Error creating a Port. Status"\
            " code: %s Response data: %s " % (status_code, response_data)
        info("### Port Created. Status code is 201 CREATED  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PORT_PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query added Port"
        json_data = get_json(response_data)

        assert json_data["configuration"] == port_data["configuration"],\
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        info("\n########## Test to Validate Patch Port Int ##########\n")
        port_data["configuration"]["admin"] = "up"
        int_data["configuration"]["user_config"] = {}
        int_data["configuration"]["user_config"]["admin"] = "up"
        status_code, response_data = execute_request(
            self.PORT_PATH, "PATCH", json.dumps(ADM_PATCH_PRT), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching a Port "\
            "Status code: %s Response data: %s " % (status_code, response_data)
        info("### Port Patched. Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PORT_PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query patched Port"
        json_data = get_json(response_data)

        assert json_data["configuration"] == port_data["configuration"],\
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        status_code, response_data = execute_request(
            self.INT_PATH, "PATCH", json.dumps(ADM_PATCH_INT),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.INT_PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query patched Port"
        json_data = get_json(response_data)

        assert json_data["configuration"] == int_data["configuration"],\
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        info("\n########## End Test Create And Patch Port Int ##########\n")

    def test_patch_other(self):
        int_data = copy.deepcopy(INT_DATA)
        self.INT_PATH = self.PATH_INT + "/2"

        # Setup patch
        int_data["configuration"]["user_config"] = {}
        int_data["configuration"]["user_config"]["duplex"] = "half"
        int_data["configuration"]["user_config"]["autoneg"] = "off"
        int_data["configuration"]["user_config"]["pause"] = "rxtx"
        # Patch
        info("\n########## Test to Validate Patch Other ##########\n")
        status_code, response_data = execute_request(
            self.INT_PATH, "PATCH", json.dumps(OTHER_PATCH),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.INT_PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query patched Port"
        json_data = get_json(response_data)

        assert json_data["configuration"] == int_data["configuration"],\
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        # Remove data
        int_data = copy.deepcopy(INT_DATA)
        status_code, response_data = execute_request(
            self.INT_PATH, "PATCH", json.dumps(REMOVE_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.INT_PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query patched Port"
        json_data = get_json(response_data)

        assert json_data["configuration"] == int_data["configuration"],\
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
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_WebUIREST.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test_patch_port_int_admin()
        self.test_var.test_patch_other()
