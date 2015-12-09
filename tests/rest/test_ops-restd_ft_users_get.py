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
import json
import httplib
import urllib
import inspect

from opsvsi.docker import *
from opsvsi.opsvsitest import *
from utils.utils import *
from utils.user_utils import *

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QueryUserTest(OpsVsiTest):
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

    def test_get_all_users(self):
        # Test Setup
        users_list = []
        prompt = CLI_PROMPT
        expected_data = create_user(self, "test", "test", DEFAULT_USER_GRP,
                                    prompt, 100)
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        # Test
        info("\n########## Test to Validate GET All Users ##########\n")

        for data in json_data:
            assert validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        # Test Teardown
        delete_user(self, "test", 100)
        info("########## End Test to Validate GET All Users ##########\n")

    def test_get_only_ovsdb_group_users(self):
        # Test Setup
        users_list = []
        prompt = CLI_PROMPT
        expected_data = create_user(self, "test", "test", DEFAULT_USER_GRP,
                                    prompt, 10)
        create_user(self, "user_not_in_ovsdb_group", "test", "nobody",
                    prompt, 1)
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)


        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        # Test
        info("\n########## Test to Validate GET only OVSDB_GROUP "
             "Users ##########\n")

        for data in json_data:
            assert validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        # Test Teardown
        delete_user(self, "test", 10)
        delete_user(self, "user_not_in_ovsdb_group", 1)
        info("########## End Test to Validate GET only OVSDB_GROUP "
             "Users ##########\n")

    def test_get_users_with_not_relevant_argument(self):
        # Test Setup
        users_list = []
        prompt = BASH_PROMPT
        expected_data = create_user(self, "test", "test", DEFAULT_USER_GRP,
                                    prompt, 10)
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        # Test
        info("\n########## Test to Validate GET All Users in OVSDB_GROUP "
             "with not relevant argument ##########\n")

        for data in json_data:
            assert validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        # Test Teardown
        delete_user(self, "test", 10)
        info("########## End Test to Validate GET All Users in OVSDB_GROUP "
             "With not relevant argument ##########\n")

    def test_get_default_users(self):
        # Test Setup
        users_list = []
        expected_data = [{'username': 'admin'}]
        status_code, response_data = execute_request(self.PATH, "GET", None,
                                                     self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        # Test
        info("\n########## Test to Validate GET Default User ##########\n")

        for data in json_data:
            assert validate_keys_complete_object(data)
            users_list.append(data['configuration'])
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == users_list, "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        info("########## End Test to Validate GET Default User ##########\n")

    def run_tests(self):
        """
        This method will inspect itself to retrieve all existing methods.

        Only methods that begin with "test_" will be executed.
        """
        methodlist = [n for n, v in inspect.getmembers(self,
                                                       inspect.ismethod)
                      if isinstance(v, types.MethodType)]

        info("\n########## Starting Retrieve Users Get Tests ##########\n")
        for name in methodlist:
            if name.startswith("test_"):
                getattr(self, "%s" % name)()
        info("\n########## Ending Retrieve Users Get Tests ##########\n")


class Test_QueryUser:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_QueryUser.test_var = QueryUserTest()

    def teardown_class(cls):
        Test_QueryUser.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def _del_(self):
        del self.test_var

    def test_run(self):
        self.test_var.run_tests()
