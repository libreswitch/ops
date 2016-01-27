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
        self.addSwitch("s1")


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
        query_path = self.PATH + "?depth=1"
        expected_data = create_user(self, "test", "test", DEFAULT_USER_GRP,
                                    prompt, 100)
        status_code, response_data = execute_request(query_path, "GET", None,
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

    def test_get_all_users_uri(self):
        # Test Setup
        users_list = []
        prompt = CLI_PROMPT
        query_path = self.PATH + "?depth=1"

        user_data = create_user(self, "test", "test", DEFAULT_USER_GRP,
                                prompt, 100)
        expected_uris = [self.PATH + "/admin", self.PATH + "/test"]

        # Test
        status_code, response_data = execute_request(query_path, "GET", None,
                                                     self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        info("\n########## Test to Validate GET All Users ##########\n")

        info("### Configuration, statistics and status keys present ###\n")

        for data in json_data:
            assert data in expected_uris, "Wrong expected data\n"

        info("### Data returned as expected ###\n")

        # Test Teardown
        delete_user(self, "test", 100)
        info("########## End Test to Validate GET All Users ##########\n")

    def test_get_only_ovsdb_group_users(self):
        # Test Setup
        users_list = []
        prompt = CLI_PROMPT
        query_path = self.PATH + "?depth=1"
        expected_data = create_user(self, "test", "test", DEFAULT_USER_GRP,
                                    prompt, 10)
        create_user(self, "user_not_in_ovsdb_group", "test", "nobody",
                    prompt, 1)
        status_code, response_data = execute_request(query_path, "GET", None,
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
        query_path = self.PATH + "?depth=1"
        expected_data = create_user(self, "test", "test", DEFAULT_USER_GRP,
                                    prompt, 10)
        status_code, response_data = execute_request(query_path, "GET", None,
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
        query_path = self.PATH + "?depth=1"
        status_code, response_data = execute_request(query_path, "GET", None,
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

    def test_get_specific_user(self):
        # Test Setup
        query_path = self.PATH + "/admin"
        expected_data = {'username': 'admin'}
        # Test
        status_code, response_data = execute_request(query_path, "GET", None,
                                                     self.SWITCH_IP)

        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        info("### Status code is OK ###\n")

        json_data = get_json(response_data)

        info("\n########## Test to Validate GET Specific User ##########\n")

        assert validate_keys_complete_object(json_data)
        info("### Configuration, statistics and status keys present ###\n")

        assert expected_data == json_data['configuration'], \
            "Wrong expected data\n"
        info("### Data returned as expected ###\n")

        # Test Teardown
        delete_user(self, "test", 100)
        info("########## End Test to Validate GET Specific User ##########\n")

    def test_get_non_existent_user(self):
        query_path = self.PATH + "/test"
        # Test
        info("\n########## Test to Validate GET Non existent "
             "User ##########\n")
        status_code, response_data = execute_request(query_path, "GET", None,
                                                     self.SWITCH_IP)

        assert status_code == httplib.NOT_FOUND, "Wrong status code %s " \
            % status_code
        info("### Status code is NOT FOUND ###\n")

        info("########## End Test to Validate GET Non existent "
             "User ##########\n")


class Test_QueryUser:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_QueryUser.test_var = QueryUserTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_QueryUser.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def _del_(self):
        del self.test_var

    def test_run_call_get_all_users(self):
        self.test_var.test_get_all_users()

    def test_run_call_get_only_ovsdb_group_users(self):
        self.test_var.test_get_only_ovsdb_group_users()

    def test_run_call_get_users_with_not_relevant_argument(self):
        self.test_var.test_get_users_with_not_relevant_argument

    def test_run_call_get_default_users(self):
        self.test_var.test_get_default_users()

    def test_run_call_get_specific_user(self):
        self.test_var.test_get_specific_user()

    def test_run_call_get_non_existent_user(self):
        self.test_var.test_get_non_existent_user()
