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

import os
import sys
import time
import pytest
import subprocess
import shutil

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import urllib

import request_test_utils
import port_test_utils

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

path = "/rest/v1/system/ports"
port_path = path + "/Port1"

class myTopo(Topo):
    def build (self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class DeletePortTest (OpsVsiTest):
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

    def delete_port (self):
        info("\n########## Test delete Port ##########\n")
        status_code, response_data = request_test_utils.execute_request(self.PORT_PATH, "DELETE", None, self.SWITCH_IP)
        assert status_code == httplib.NO_CONTENT, "Is not sending No Content status code. Status code: %s" % status_code
        info("### Status code is 204 No Content  ###\n")

        info("\n########## End Test delete Port ##########\n")

    def verify_deleted_port_from_port_list(self):
        info("\n########## Test Verify if Port is been deleted from port list ##########\n")
        # Verify if port has been deleted from the list
        status_code, response_data = request_test_utils.execute_request(self.PATH, "GET", None, self.SWITCH_IP)
        json_data = []
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert port_path not in json_data, "Port has not been deleted from port list"
        info("### Port not in list  ###\n")

        info("\n########## End Test Verify if Port is been deleted from port list ##########\n")

    def verify_deleted_port(self):
        info("\n########## Test Verify if Port is found ##########\n")
        # Verify deleted port
        status_code, response_data = request_test_utils.execute_request(self.PORT_PATH, "GET", None, self.SWITCH_IP)
        assert status_code == httplib.NOT_FOUND, "Port has not be deleted"
        info("### Port not found  ###\n")

        info("\n########## End Test Verify if Port is found ##########\n")

    def delete_non_existent_port(self):
        info("\n########## Test delete non-existent Port ##########\n")
        new_path = self.PATH + "/Port2"
        status_code, response_data = request_test_utils.execute_request(new_path, "DELETE", None, self.SWITCH_IP)

        assert status_code == httplib.NOT_FOUND, "Validation failed, is not sending Not Found error. Status code: %s" % status_code
        info("### Status code is 404 Not Found  ###\n")

        info("\n########## End Test delete non-existent Port  ##########\n")

class Test_DeletePort:
    def setup (self):
        pass

    def teardown (self):
        pass

    def setup_class (cls):
        Test_DeletePort.test_var = DeletePortTest()
        Test_DeletePort.test_var.setup_switch_ip()
        # Add a test port
        port_test_utils.create_test_port(Test_DeletePort.test_var.SWITCH_IP)

    def teardown_class (cls):
        Test_DeletePort.test_var.net.stop()

    def setup_method (self, method):
        pass

    def teardown_method (self, method):
        pass

    def __del__ (self):
        del self.test_var

    def test_run (self):
        self.test_var.delete_port()
        self.test_var.verify_deleted_port_from_port_list()
        self.test_var.verify_deleted_port()
        self.test_var.delete_non_existent_port()
