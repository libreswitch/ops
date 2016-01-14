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

import inspect

from utils.utils import *
from utils.user_utils import *

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class UpdateUserTest(OpsVsiTest):
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

        self.switch = self.net.switches[0]
        self.SWITCH_IP = get_switch_ip(self.switch)
        self.PATH = "/rest/v1/system/users"
        self.HEADERS = None

    def test_update_valid_user(self):
        # Test Setup
        data = {}
        prompt = CLI_PROMPT
        new_path = self.PATH + "/test_user_0"
        create_user(self, "test", "test", DEFAULT_USER_GRP,
                    prompt, 1)

        # Test
        info("\n########## Test to Validate UPDATE Valid User ##########\n")

        new_password = "test_password"
        data = {"configuration": {"password": new_password}}

        status_code, response_data = execute_request(new_path, "PUT",
                                                     json.dumps(data),
                                                     self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### User password updated successfully ###\n")

        assert login(self, "test_user_0", new_password), "User not logged in"
        info("### User logged in successfully with the new password ###\n")

        # Test Teardown
        delete_user(self, "test", 1)

        info("########## End Test to Validate UPDATE Valid User ##########\n")

    def test_update_user_with_empty_password(self):
        # Test Setup
        data = {}
        prompt = CLI_PROMPT
        new_path = self.PATH + "/test_user_0"
        create_user(self, "test", "test", DEFAULT_USER_GRP,
                    prompt, 1)

        # Test
        info("\n########## Test to Validate UPDATE User with empty password"
             " ##########\n")

        new_password = ""
        data = {"configuration": {"password": new_password}}

        status_code, response_data = execute_request(new_path, "PUT",
                                                     json.dumps(data),
                                                     self.SWITCH_IP)

        assert status_code == httplib.BAD_REQUEST, "Validation failed, is " +\
            "not sending Bad Request error. Status code: %s" % status_code
        info("### Status code is 400 Bad Request ###\n")

        assert login(self, "test_user_0", "test"), "User not logged in"
        info("### User password unchanged ###\n")

        # Test Teardown
        delete_user(self, "test", 1)

        info("########## End Test to Validate UPDATE User with empty password"
             " ##########\n")

    def test_update_nonexistent_user(self):
        # Test Setup
        data = {}
        prompt = CLI_PROMPT
        new_path = self.PATH + "/nonexistentuser"

        # Test
        info("\n########## Test to Validate UPDATE nonexistent user password"
             " ##########\n")

        new_password = "test_password"
        data = {"configuration": {"password": new_password}}

        status_code, response_data = execute_request(new_path, "PUT",
                                                     json.dumps(data),
                                                     self.SWITCH_IP)

        assert status_code == httplib.BAD_REQUEST, "Validation failed, is " +\
            "not sending Bad Request error. Status code: %s" % status_code
        info("### Status code is 400 Bad Request ###\n")

        info("########## End Test to Validate UPDATE nonexistent user"
             " password ##########\n")

    def test_update_password_for_user_not_in_ovsdb_group(self):
        # Test Setup
        data = {}
        prompt = CLI_PROMPT
        new_path = self.PATH + "/test_user_0"
        create_user(self, "test", "test", "nogroup",
                    prompt, 1)

        # Test
        info("\n########## Test to Validate UPDATE User not in ovsdb group"
             " ##########\n")

        new_password = "test_password"
        data = {"configuration": {"password": new_password}}

        status_code, response_data = execute_request(new_path, "PUT",
                                                     json.dumps(data),
                                                     self.SWITCH_IP)

        assert status_code == httplib.BAD_REQUEST, "Validation failed, is " +\
            "not sending Bad Request error. Status code: %s" % status_code
        info("### Status code is 400 Bad Request ###\n")

        # Test Teardown
        delete_user(self, "test", 1)

        info("########## End Test to Validate UPDATE User not in ovsdb group"
             " ##########\n")

    def test_update_valid_user_and_login_with_old_password(self):
        # Test Setup
        data = {}
        prompt = CLI_PROMPT
        new_path = self.PATH + "/test_user_0"
        create_user(self, "test", "test", DEFAULT_USER_GRP,
                    prompt, 1)

        # Test
        info("\n########## Test to Validate UPDATE Valid User and login with"
             " old password ##########\n")

        new_password = "test_password"
        data = {"configuration": {"password": new_password}}

        status_code, response_data = execute_request(new_path, "PUT",
                                                     json.dumps(data),
                                                     self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### User password updated successfully ###\n")

        assert not login(self, "test_user_0", "test"), "User logged in"
        info("### User not logged in with the old password ###\n")

        # Test Teardown
        delete_user(self, "test", 1)

        info("########## End Test to Validate UPDATE Valid User and login with"
             " old password ##########\n")

    def run_tests(self):
        """
        This method will inspect itself to retrieve all existing methods.

        Only methods that begin with "test_" will be executed.
        """
        methodlist = [n for n, v in inspect.getmembers(self,
                                                       inspect.ismethod)
                      if isinstance(v, types.MethodType)]

        info("\n########## Starting Users Delete Tests ##########\n")
        for name in methodlist:
            if name.startswith("test_"):
                getattr(self, "%s" % name)()
        info("\n########## Ending Users Delete Tests ##########\n")


class Test_UpdateUser:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_UpdateUser.test_var = UpdateUserTest()

    def teardown_class(cls):
        Test_UpdateUser.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def _del_(self):
        del self.test_var

    def test_run(self):
        self.test_var.run_tests()
