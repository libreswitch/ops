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
from opsvsiutils.systemutil import *

import json
import httplib
import urllib

from webui.utils.utils import *
import copy

NUM_OF_SWITCHES = 2
NUM_HOSTS = 2

ADM_PATCH_PRT = [{"op": "add",
                  "path": "/admin",
                  "value": "up"}]
ADM_PATCH_INT = [{"op": "add",
                  "path": "/user_config",
                  "value": {"admin": "up"}}]

LACP_KEY_PATCH_INT = {"op": "add",
                      "path": "/other_config",
                      "value": {"lacp-aggregation-key": "1"}}

LACP_KEY_DELETE_PATCH_INT = {"op": "remove",
                             "path": "/other_config/lacp-aggregation-key"}

SWITCH_PREFIX = "s"
HOST_PREFIX = "h"
PORT_1 = "1"
PORT_2 = "2"
PORT_3 = "3"

LAG_ID = "12"
INTERFACES = {"1", "2"}

LACP_AGGREGATION_KEY = "lacp-aggregation-key"

# The host IPs are based on 10.0.0.0/8

PING_ATTEMPTS = 3
CREATION_SLEEP_SECS = 30
DELETION_SLEEP_SECS = 30


class myTopo(Topo):

    def build(self, hsts=0, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.addSwitch("%s1" % SWITCH_PREFIX)
        self.addSwitch("%s2" % SWITCH_PREFIX)

        # Add the hosts. One per switch.
        for i in irange(1, hsts):
            hostName = "%s%s" % (HOST_PREFIX, i)
            self.addHost(hostName)
        # Connect the hosts to the switches
        for i in irange(1, sws):
            self.addLink("%s%s" % (SWITCH_PREFIX, i),
                         "%s%s" % (HOST_PREFIX, i), int(PORT_3), int(PORT_3))
        # Connect the switches
        for i in irange(2, sws):
            self.addLink("%s%s" % (SWITCH_PREFIX, i-1),
                         "%s%s" % (SWITCH_PREFIX, i), int(PORT_1), int(PORT_1))
            self.addLink("%s%s" % (SWITCH_PREFIX, i-1),
                         "%s%s" % (SWITCH_PREFIX, i), int(PORT_2), int(PORT_2))


class Test_CreateLag(OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS,
                           sws=NUM_OF_SWITCHES,
                           hopts=self.getHostOpts(),
                           sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch,
                           host=OpsVsiHost,
                           link=OpsVsiLink,
                           ipBase="10.0.0.0/8",
                           controller=None,
                           build=True)

        self.SWITCH_IP1 = get_switch_ip(self.net.switches[0])
        self.SWITCH_IP2 = get_switch_ip(self.net.switches[1])
        self.PATH = "/rest/v1/system"
        self.PATH_PORTS = self.PATH + "/ports"
        self.PATH_INT = self.PATH + "/interfaces"

    def create_topo_no_lag(self):
        # set up port 1, 2 and 3 on switch 1
        self.create_port(self.SWITCH_IP1, PORT_1)
        self.port_int_admin(self.SWITCH_IP1, PORT_1)
        self.create_port(self.SWITCH_IP1, PORT_2)
        self.port_int_admin(self.SWITCH_IP1, PORT_2)
        self.create_port(self.SWITCH_IP1, PORT_3)
        self.port_int_admin(self.SWITCH_IP1, PORT_3)
        # set up port 1, 2 and 3 on switch 2
        self.create_port(self.SWITCH_IP2, PORT_1)
        self.port_int_admin(self.SWITCH_IP2, PORT_1)
        self.create_port(self.SWITCH_IP2, PORT_2)
        self.port_int_admin(self.SWITCH_IP2, PORT_2)
        self.create_port(self.SWITCH_IP2, PORT_3)
        self.port_int_admin(self.SWITCH_IP2, PORT_3)

    def test_create_lag(self):
        self.create_topo_no_lag()
        self.create_lag(self.SWITCH_IP1, LAG_ID, INTERFACES, "active")
        self.create_lag(self.SWITCH_IP2, LAG_ID, INTERFACES, "passive")
        time.sleep(CREATION_SLEEP_SECS)
        self.verify_lag_ok("lag" + LAG_ID)

    def test_delete_lag(self):
        # called after test_create_lag()
        self.delete_lag(self.SWITCH_IP1, LAG_ID, INTERFACES)
        self.delete_lag(self.SWITCH_IP2, LAG_ID, INTERFACES)
        time.sleep(DELETION_SLEEP_SECS)
        self.verify_lag_deleted("lag" + LAG_ID)

    def create_lag(self, switch, lagId, interfaces, mode="active"):
        self.PORT_PATH = self.PATH_PORTS + "/" + lagId
        port_data = copy.deepcopy(PORT_DATA)
        port_data["configuration"]["name"] = "lag" + lagId
        port_data["configuration"]["admin"] = "up"
        port_data["configuration"]["lacp"] = mode
        port_data["configuration"]["vlan_mode"] = "trunk"

        # build array of interfaces
        ints = []
        for interface in interfaces:
            ints.append("/rest/v1/system/interfaces/" + interface)
        port_data["configuration"]["interfaces"] = ints
        info("\n########## Switch " + switch + ": Create LAG " +
             lagId + " ##########\n")
        status_code, response_data = execute_request(self.PATH_PORTS, "POST",
                                                     json.dumps(port_data),
                                                     switch)
        assert status_code == httplib.CREATED, "Error creating a Port.Status" \
            + " code: %s Response data: %s " % (status_code, response_data)
        info("### Port Created. Status code is 201 CREATED  ###\n")
        self.assign_lacp_aggregation_key_ints(switch, lagId, interfaces)

    def delete_lag(self, switch, lagId, interfaces):
        self.PORT_PATH = self.PATH_PORTS + "/lag" + lagId
        info("\n########## Switch " + switch + ": Delete LAG " +
             lagId + " ##########\n")
        status_code, response_data = execute_request(self.PORT_PATH, "DELETE",
                                                     None, switch)
        assert status_code == httplib.NO_CONTENT,\
            "Error deleting a Port.Status" \
            + " code: %s Response data: %s " % (status_code, response_data)
        info("### Port Deleted. Status code is 201 DELETED  ###\n")
        self.remove_lacp_aggregation_key_ints(switch, lagId, interfaces)

    def assign_lacp_aggregation_key_ints(self, switch, lagId, interfaces):
        for interface in interfaces:
            self.assign_lacp_aggregation_key_int(switch, lagId, interface)

    def assign_lacp_aggregation_key_int(self, switch, lagId, interface):
        self.INT_PATH = self.PATH_INT + "/" + interface
        int_data = copy.deepcopy(LACP_KEY_PATCH_INT)
        int_data["value"][LACP_AGGREGATION_KEY] = lagId
        status_code, response_data = execute_request(
            self.INT_PATH,
            "PATCH",
            json.dumps([int_data]),
            switch,
            False)
        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")

    def remove_lacp_aggregation_key_ints(self, switch, lagId, interfaces):
        for interface in interfaces:
            self.remove_lacp_aggregation_key_int(switch, lagId, interface)

    def remove_lacp_aggregation_key_int(self, switch, lagId, interface):
        self.INT_PATH = self.PATH_INT + "/" + interface
        int_data = copy.deepcopy(LACP_KEY_DELETE_PATCH_INT)
        status_code, response_data = execute_request(
            self.INT_PATH,
            "PATCH",
            json.dumps([int_data]),
            switch,
            False)
        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")

    def verify_lag_ok(self, lagName, mode="active"):
        # assert status bond_hw_handle has value for static lag
        # assert status lacp_status bond_status ok for dynamic lag
        # Verify data
        self.PORT_PATH = self.PATH_PORTS + "/" + lagName
        for switch in [self.SWITCH_IP1, self.SWITCH_IP2]:
            info("### Checking switch " + switch + "###\n")
            status_code, response_data = execute_request(
                self.PORT_PATH, "GET",
                None,
                switch)
            assert status_code == httplib.OK,\
                "Failed to query LAG " + lagName
            json_data = get_json(response_data)
            if mode != "off":
                assert json_data["status"]["lacp_status"]["bond_status"] \
                    == "ok"
                info("### Switch " + switch + " lag status is ok ###\n")

    def verify_lag_deleted(self, lagName):
        # assert status bond_hw_handle has value for static lag
        # assert status lacp_status bond_status ok for dynamic lag
        # Verify data
        self.PORT_PATH = self.PATH_PORTS + "/" + lagName
        for switch in [self.SWITCH_IP1, self.SWITCH_IP2]:
            info("### Checking switch " + switch + "###\n")
            status_code, response_data = execute_request(
                self.PORT_PATH, "GET",
                None,
                switch)
            assert status_code == 404,\
                "Switch: " + switch + " - LAG " + lagName + " must not exist."
            info("### Switch " + switch + " lag deletion is ok ###\n")

    def create_port(self, switch, port):
        self.PORT_PATH = self.PATH_PORTS + "/" + port
        port_data = copy.deepcopy(PORT_DATA)
        port_data["configuration"]["name"] = port
        port_data["configuration"]["interfaces"] = \
            ["/rest/v1/system/interfaces/" + port]
        info("\n########## Switch " + switch + ": Create Port " +
             port + " ##########\n")
        status_code, response_data = execute_request(self.PATH_PORTS, "POST",
                                                     json.dumps(port_data),
                                                     switch)
        assert status_code == httplib.CREATED, "Error creating a Port.Status" \
            + " code: %s Response data: %s " % (status_code, response_data)
        info("### Port Created. Status code is 201 CREATED  ###\n")

    def port_int_admin(self, switch, port):
        self.PORT_PATH = self.PATH_PORTS + "/" + port
        self.INT_PATH = self.PATH_INT + "/" + port
        status_code, response_data = execute_request(self.PORT_PATH, "PATCH",
                                                     json.dumps(ADM_PATCH_PRT),
                                                     switch,
                                                     False)
        assert status_code == httplib.NO_CONTENT, "Error patching a Port "\
            "Status code: %s Response data: %s " % (status_code, response_data)
        info("### Port Patched. Status code is 204 NO CONTENT  ###\n")

        status_code, response_data = execute_request(self.INT_PATH,
                                                     "PATCH",
                                                     json.dumps(ADM_PATCH_INT),
                                                     switch,
                                                     False)
        assert status_code == httplib.NO_CONTENT, "Error patching an "\
            "Interface. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### Interface Patched. Status code is 204 NO CONTENT  ###\n")


class Test_WebUIREST:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_WebUIREST.test_var = Test_CreateLag()
        rest_sanity_check(cls.test_var.SWITCH_IP1)
        rest_sanity_check(cls.test_var.SWITCH_IP2)

    def teardown_class(cls):
        Test_WebUIREST.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run_create_lag(self):
        self.test_var.test_create_lag()

    def test_run_delete_lag(self):
        self.test_var.test_delete_lag()
