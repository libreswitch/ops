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


from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib

from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, create_test_port
NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

path = "/rest/v1/system/ports"
port_path = path + "/Port1"


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class DeletePortTest (OpsVsiTest):
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
        self.PATH = "/rest/v1/system/ports"
        self.PORT_PATH = self.PATH + "/Port1"
        self.cookie_header = None

    def delete_port_with_depth(self):
        info("\n########## Test delete Port with depth ##########\n")
        status_code, response_data = execute_request(
            self.PORT_PATH + "?depth=1", "DELETE", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Is not sending No Content status code. Status code: %s" % \
            status_code
        info("### Status code is 400 BAD REQUEST  ###\n")

        info("\n########## End Test delete Port with depth ##########\n")

    def delete_port(self):
        info("\n########## Test delete Port ##########\n")
        status_code, response_data = execute_request(
            self.PORT_PATH, "DELETE", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, \
            "Is not sending No Content status code. Status code: %s" % \
            status_code
        info("### Status code is 204 No Content  ###\n")

        info("\n########## End Test delete Port ##########\n")

    def verify_deleted_port_from_port_list(self):
        info("\n########## Test Verify if Port is deleted from port list "
             "##########\n")
        # Verify if port has been deleted from the list
        status_code, response_data = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        json_data = []
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert port_path not in json_data, \
            "Port has not been deleted from port list"
        info("### Port not in list  ###\n")

        info("\n########## End Test Verify if Port is deleted from port list"
             "##########\n")

    def verify_deleted_port(self):
        info("\n########## Test Verify if Port is found ##########\n")
        # Verify deleted port
        status_code, response_data = execute_request(
            self.PORT_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.NOT_FOUND, "Port has not be deleted"
        info("### Port not found  ###\n")

        info("\n########## End Test Verify if Port is found ##########\n")

    def delete_non_existent_port(self):
        info("\n########## Test delete non-existent Port ##########\n")
        new_path = self.PATH + "/Port2"
        status_code, response_data = execute_request(
            new_path, "DELETE", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.NOT_FOUND, \
            "Validation failed, is not sending Not Found error. " + \
            "Status code: %s" % status_code
        info("### Status code is 404 Not Found  ###\n")

        info("\n########## End Test delete non-existent Port  ##########\n")


class Test_DeletePort:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_DeletePort.test_var = DeletePortTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)
        # Add a test port
        info("\n########## Creating Test Port  ##########\n")
        status_code, response = create_test_port(cls.test_var.SWITCH_IP)
        assert status_code == httplib.CREATED, "Port not created."\
            "Response %s" % response
        info("### Test Port Created  ###\n")

    def teardown_class(cls):
        Test_DeletePort.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.delete_port_with_depth()
        self.test_var.delete_port()
        self.test_var.verify_deleted_port_from_port_list()
        self.test_var.verify_deleted_port()
        self.test_var.delete_non_existent_port()
