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


class DeleteUserTest(OpsVsiTest):
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

    def test_delete_new_user(self):
        # Test Setup
        users_list = []
        prompt = CLI_PROMPT
        new_path = self.PATH + "/test_user_0"
        expected_data = create_user(self, "test", "test", DEFAULT_USER_GRP,
                                    prompt, 1)
        # Removing the last user created from the expected data list
        expected_data.pop()

        # Test
        assert login(self, "admin", "admin"), "User not logged in"

        info("\n########## Test to Validate DELETE New User ##########\n")
        status_code, response_data = execute_request(new_path, "DELETE", None,
                                                     self.SWITCH_IP)

        assert status_code == httplib.NO_CONTENT, "Validation failed, is " +\
            "not sending No Content successful status code"

        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        for data in json_data:
            assert validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        # Test Teardown
        delete_user(self, "test", 1)

        info("########## End Test to Validate GET All Users ##########\n")

    def test_delete_new_logged_in_user(self):
        # Test Setup
        users_list = []
        prompt = CLI_PROMPT
        new_path = self.PATH + "/test_user_0"
        expected_data = create_user(self, "test", "test", DEFAULT_USER_GRP,
                                    prompt, 1)

        # Test
        assert login(self, "test_user_0", "test"), "User not logged in"

        info("\n########## Test to Validate DELETE New Logged in User "
             "##########\n")
        status_code, response_data = execute_request(new_path, "DELETE", None,
                                                     self.SWITCH_IP, False,
                                                     self.HEADERS)
        assert status_code == httplib.BAD_REQUEST, "Validation failed, is " +\
            "not sending Bad Request error. Status code: %s" % status_code
        info("### Status code is 400 Bad Request ###\n")
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        for data in json_data:
            assert validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        # Test Teardown
        delete_user(self, "test", 1)
        info("########## End Test to Validate DELETE New Logged in User "
             "##########\n")

    def test_delete_current_logged_in_user(self):
        # Test Setup
        users_list = []
        prompt = CLI_PROMPT
        new_path = self.PATH + "/admin"
        expected_data = [{'username': "admin"}]

        # Test
        assert login(self, "admin", "admin"), "User not logged in"

        info("\n########## Test to Validate DELETE Current Logged in User "
             "##########\n")
        status_code, response_data = execute_request(new_path, "DELETE", None,
                                                     self.SWITCH_IP, False,
                                                     self.HEADERS)
        assert status_code == httplib.BAD_REQUEST, "Validation failed, is " +\
            "not sending Bad Request error. Status code: %s" % status_code
        info("### Status code is 400 Bad Request ###\n")
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        for data in json_data:
            assert validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")
        info("########## End Test to Validate DELETE Current Logged in User "
             "##########\n")

    def test_delete_nonexistent_user(self):
        # Test Setup
        users_list = []
        prompt = CLI_PROMPT
        new_path = self.PATH + "/noexistentuser"
        expected_data = [{'username': "admin"}]

        # Test
        assert login(self, "admin", "admin"), "User not logged in"

        info("\n########## Test to Validate DELETE Nonexistent User "
             "##########\n")
        status_code, response_data = execute_request(new_path, "DELETE", None,
                                                     self.SWITCH_IP, False,
                                                     self.HEADERS)
        assert status_code == httplib.BAD_REQUEST, "Validation failed, is " +\
            "not sending Bad Request error. Status code: %s" % status_code
        info("### Status code is 400 Bad Request ###\n")

        info("########## End Test to Validate DELETE Nonexistent User "
             "##########\n")

    def test_delete_user_not_in_ovsdb_group(self):
        # Test Setup
        users_list = []
        prompt = CLI_PROMPT
        new_path = self.PATH + "/test_user_0"
        create_user(self, "test", "test", "nobody", prompt, 1)
        expected_data = [{'username': 'admin'}]

        # Test
        assert login(self, "admin",  "admin"), "User not logged in"

        info("\n########## Test to Validate DELETE New User not in OVSDB "
             "Group ##########\n")
        status_code, response_data = execute_request(new_path, "DELETE", None,
                                                     self.SWITCH_IP, False,
                                                     self.HEADERS)
        assert status_code == httplib.BAD_REQUEST, "Validation failed, is " +\
            "not sending Bad Request error. Status code: %s" % status_code
        info("### Status code is 400 Bad Request ###\n")

        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        for data in json_data:
            assert validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        # Test Teardown
        delete_user(self, "test", 1)
        info("########## End Test to Validate DELETE New User not in OVSDB "
             "Group ##########\n")

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


class Test_DeleteUser:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_DeleteUser.test_var = DeleteUserTest()

    def teardown_class(cls):
        Test_DeleteUser.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def _del_(self):
        del self.test_var

    def test_run(self):
        self.test_var.run_tests()
