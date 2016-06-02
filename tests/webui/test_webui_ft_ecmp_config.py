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


from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib

from pytest import mark

from opsvsiutils.restutils.utils import login, execute_request, \
    rest_sanity_check, get_switch_ip, get_json
NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

TRUE = "true"
FALSE = "false"

ECMP_PATCH = [{"op": "add", "path": "/ecmp_config", "value": {"key": "val"}}]


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class myTopo(Topo):

    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.addSwitch("s1")


class Test_EcmpConfig(OpsVsiTest):

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
        info("\n########## Test to Validate initial ecmp config ##########\n")

    def test_initial_config(self):
        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config "
        json_data = get_json(response_data)
        assert "ecmp" not in json_data["configuration"].keys(),\
            "Default ECMP configuration data is non blank"
        info("### ECMP default configuration data validated ###\n")

    def test_ecmp_enable(self):

        # enable ecmp
        ECMP_PATCH[0]["value"]["enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["enabled"] = TRUE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching a ecmp " \
            "enable Status code: %s Response data: %s " % (status_code,
                                                           response_data)
        info("### Enable ECMP Patched. Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert json_data["configuration"]["ecmp_config"]["enabled"] == TRUE,\
            "ECMP enable failed"
        info("### ECMP enable validated ###\n")

    def test_ecmp_disable(self):

        # disable ecmp
        ECMP_PATCH[0]["value"]["enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["enabled"] = FALSE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, \
            "Error patching a ecmp disable Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Disable ECMP Patched. Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert json_data["configuration"]["ecmp_config"]["enabled"] == FALSE,\
            "ECMP disable failed"
        info("### ECMP disable validated ###\n")

    def test_ecmp_dstip_enable(self):

        # enable ecmp dest ip

        ECMP_PATCH[0]["value"]["hash_dstip_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["hash_dstip_enabled"] = TRUE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, \
            "Error patching ecmp dest ip enable Status code: " \
            "%s Response data: %s " % (status_code, response_data)
        info("### Enable Dest IP ECMP Patched. "
             "Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert json_data["configuration"]["ecmp_config"]["hash_dstip_enabled"]\
            == TRUE, "ECMP dest IP enable failed"
        info("### ECMP dest IP enable validated ###\n")

    def test_ecmp_dstip_disable(self):

        # disable ecmp dest ip

        ECMP_PATCH[0]["value"]["hash_dstip_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["hash_dstip_enabled"] = FALSE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, \
            "Error patching ecmp dest ip disable Status code:" \
            "%s Response data: %s " % (status_code, response_data)
        info("### Disable Dest IP ECMP Patched. "
             "Status code is 204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert json_data["configuration"]["ecmp_config"]["hash_dstip_enabled"]\
            == FALSE, "ECMP dest IP disable failed"
        info("### ECMP dest IP disable validated ###\n")

    def test_ecmp_srcip_enable(self):

        # enable ecmp source ip

        ECMP_PATCH[0]["value"]["hash_srcip_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["hash_srcip_enabled"] = TRUE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, \
            "Error patching ecmp source ip enable Status code: "\
            "%s Response data: %s " % (status_code, response_data)
        info("### Enable Source IP ECMP Patched. Status code is "
             "204 NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert json_data["configuration"]["ecmp_config"]["hash_srcip_enabled"]\
            == TRUE, "ECMP source IP enable failed"
        info("### ECMP source IP enable validated ###\n")

    def test_ecmp_srcip_disable(self):

        # disable ecmp source ip

        ECMP_PATCH[0]["value"]["hash_srcip_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["hash_srcip_enabled"] = FALSE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, \
            "Error patching ecmp source ip disable Status code: %s Response "\
            "data: %s " % (status_code, response_data)
        info("### Disable Source IP ECMP Patched. Status code is 204 "
             "NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert json_data["configuration"]["ecmp_config"]["hash_srcip_enabled"]\
            == FALSE, "ECMP source IP disable failed"
        info("### ECMP source IP disable validated ###\n")

    def test_ecmp_dstport_enable(self):

        # enable ecmp dest port

        ECMP_PATCH[0]["value"]["hash_dstport_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["hash_dstport_enabled"] = TRUE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching ecmp dest "\
            "port enable Status code: %s Response data: %s " \
            % (status_code, response_data)
        info("### Enable Dest port ECMP Patched. Status code is 204 "
             "NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert \
            json_data["configuration"]["ecmp_config"]["hash_dstport_enabled"] \
            == TRUE, "ECMP dest port enable failed"
        info("### ECMP dest port enable validated ###\n")

    def test_ecmp_dstport_disable(self):

        # disable ecmp dest port

        ECMP_PATCH[0]["value"]["hash_dstport_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["hash_dstport_enabled"] = FALSE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)
        assert status_code == httplib.NO_CONTENT, "Error patching ecmp dest "\
            "ecmp dest port enable Status code: %s Response data: %s " \
            % (status_code, response_data)
        info("### Disable Dest port ECMP Patched. Status code is 204 "
             "NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert \
            json_data["configuration"]["ecmp_config"]["hash_dstport_enabled"] \
            == FALSE, "ECMP dest port disable failed"
        info("### ECMP dest port disable validated ###\n")

    def test_ecmp_srcport_enable(self):

        # enable ecmp source port

        ECMP_PATCH[0]["value"]["hash_srcport_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["hash_srcport_enabled"] = TRUE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching ecmp src "\
            "ecmp source port enable Status code: %s Response data: %s " \
            % (status_code, response_data)
        info("Enable Source Port ECMP Patched. Status code is 204 "
             "NO CONTENT\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert \
            json_data["configuration"]["ecmp_config"]["hash_srcport_enabled"] \
            == TRUE, "ECMP source port enable failed"
        info("### ECMP source port enable validated ###\n")

    def test_ecmp_srcport_disable(self):

        # disable ecmp source port

        ECMP_PATCH[0]["value"]["hash_srcport_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["hash_srcport_enabled"] = FALSE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching ecmp src "\
            "ecmp source port disable Status code: %s Response data: %s " \
            % (status_code, response_data)
        info("Disable Source Port ECMP Patched. Status code is 204 "
             "NO CONTENT\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert \
            json_data["configuration"]["ecmp_config"]["hash_srcport_enabled"] \
            == FALSE, "ECMP source port disable failed"
        info("### ECMP source port disable validated ###\n")

    def test_ecmp_reshash_enable(self):

        # enable ecmp resilient hash

        ECMP_PATCH[0]["value"]["resilient_hash_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["resilient_hash_enabled"] = TRUE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, "Error patching ecmp "\
            "resilient hash enable Status code: %s Response data: %s " \
            % (status_code, response_data)
        info("### Enable Resilient Hash ECMP Patched. Status code is 204 "
             "NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert json_data[
            "configuration"]["ecmp_config"]["resilient_hash_enabled"]\
            == TRUE, "ECMP resilient hash enable failed"
        info("### ECMP resilient hash enable validated ###\n")

    def test_ecmp_reshash_disable(self):
        # disable ecmp resilient hash
        ECMP_PATCH[0]["value"]["resilient_hash_enabled"] = \
            ECMP_PATCH[0]["value"].pop(ECMP_PATCH[0]["value"].keys()[0])
        ECMP_PATCH[0]["value"]["resilient_hash_enabled"] = FALSE

        status_code, response_data = execute_request(
            self.PATH, "PATCH", json.dumps(ECMP_PATCH), self.SWITCH_IP,
            False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, \
            "Error patching ecmp resilient hash disable Status code: \
            %s Response data: %s " % (status_code, response_data)
        info("### Disable Resilient Hash ECMP Patched. Status code is 204 "
             "NO CONTENT  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query ecmp config"
        json_data = get_json(response_data)
        assert json_data[
            "configuration"]["ecmp_config"]["resilient_hash_enabled"]\
            == FALSE, "ECMP resilient hash disable failed"
        info("### ECMP resilient hash disable validated ###\n")


@mark.skipif(True, reason="Test ported to modular framework")
class Test_WebUI_ECMP:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_WebUI_ECMP.test_var = Test_EcmpConfig()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_WebUI_ECMP.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run_initial_config(self, netop_login):
        self.test_var.test_initial_config()

    def test_run_iecmp_enable(self, netop_login):
        self.test_var.test_ecmp_enable()

    def test_run_ecmp_dstip_enable(self, netop_login):
        self.test_var.test_ecmp_dstip_enable()

    def test_run_ecmp_srcip_enable(self, netop_login):
        self.test_var.test_ecmp_srcip_enable()

    def test_run_ecmp_dstport_enable(self, netop_login):
        self.test_var.test_ecmp_dstport_enable()

    def test_run_ecmp_srcport_enable(self, netop_login):
        self.test_var.test_ecmp_srcport_enable()

    def test_run_ecmp_reshash_enable(self, netop_login):
        self.test_var.test_ecmp_reshash_enable()

    # perform disable operations now

    def test_run_ecmp_dstip_disable(self, netop_login):
        self.test_var.test_ecmp_dstip_disable()

    def test_run_ecmp_srcip_disable(self, netop_login):
        self.test_var.test_ecmp_srcip_disable()

    def test_run_ecmp_dstport_disable(self, netop_login):
        self.test_var.test_ecmp_dstport_disable()

    def test_run_ecmp_srcport_disable(self, netop_login):
        self.test_var.test_ecmp_srcport_disable()

    def test_run_ecmp_reshash_disable(self, netop_login):
        self.test_var.test_ecmp_reshash_disable()

    def test_run_ecmp_disable(self, netop_login):
        self.test_var.test_ecmp_disable()
