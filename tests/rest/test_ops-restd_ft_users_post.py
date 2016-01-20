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

# Third party imports
import pytest
import json
import httplib
import inspect
import string

# Local imports
from opsvsi.docker import *
from opsvsi.opsvsitest import *
from utils.utils import *
from utils.user_utils import SHADOW_CMD

NUM_OF_SWITCHES = 1
NUM_HOST_PER_SWITCH = 0

switch_ip = ""

MAX_USERNAME = 32

users_post_disable = pytest.mark.skipif(True,
                                        reason="Disabling until fix 205 for "
                                        "users resource is merged")


class myTopo(Topo):

    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.addSwitch("s1")


class CreateUserTest(OpsVsiTest):

    def setupNet(self):
        global switch_ip
        self.net = Mininet(topo=myTopo(hsts=NUM_HOST_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch,
                           host=None,
                           link=None,
                           controller=None,
                           build=True)

        switch_ip = get_switch_ip(self.net.switches[0])
        self.PATH = "/rest/v1/system/users"

    def get_user_data(self, username, password):
        user_data = {}
        user_data["configuration"] = {"username": username,
                                      "password": password}
        return user_data

    def check_user_exists(self, user_list_json, username):
        for user in user_list_json:
            if user["configuration"]["username"] == username:
                return True
        return False

    def get_not_allowed_usernames(self):
        # Not Allowed usernames
        empty_username = ''
        space_username = ' '
        long_username = ''.join("a" for _ in range(MAX_USERNAME+1))
        # $ is only allowed at the end of the username
        special_characters = list("#(){}[]?\~/+-*=|^$%`.;,:")
        special_characters_usernames = [c + "user" + str(i)
                                        for i,
                                        c in enumerate(special_characters)]
        # Add usernames to a list
        not_allowed_usernames = []
        not_allowed_usernames.append(empty_username)
        not_allowed_usernames.append(space_username)
        not_allowed_usernames.append(long_username)
        not_allowed_usernames.extend(special_characters_usernames)
        return not_allowed_usernames

    def test_create_user_valid_username_and_password(self):
        info("\n########## Test Create user: valid username and password "
             "##########\n")
        # Test Setup
        expected_data = self.get_user_data("test_user", "test_password")
        username = expected_data["configuration"]["username"]

        # Test
        info("### Try to create user: \"%s\" ###\n" %
             json.dumps(expected_data))
        status_code, response_data = execute_request(self.PATH, "POST",
                                                     json.dumps(expected_data),
                                                     switch_ip)

        assert status_code == httplib.CREATED, "Validation failed, request " \
            "didn't return Created status code. Status code: %s" % status_code

        info("### Status code is CREATED ###")

        info("### Check if user is created ###")
        query_path = self.PATH + "?depth=1"
        status_code, response_data = execute_request(query_path, "GET",
                                                     None, switch_ip)

        assert status_code == httplib.OK, "Validation failed, " \
            "didn't return OK status code. Status code: %s" % status_code

        info("### Status code is OK ###")

        query_data = {}
        try:
            query_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        username = expected_data["configuration"]["username"]

        assert self.check_user_exists(query_data, username), \
            "Wrong expected data. Expected data: %s Returned data: %s" \
            % (expected_data["configuration"], query_data["configuration"])

        info("\n########## End Test Create user: valid username and password "
             "##########\n")

    def test_create_user_invalid_username(self):
        info("\n########## Test Create user: invalid name and valid password "
             "##########\n")
        # Test Setup
        not_allowed_usernames = self.get_not_allowed_usernames()

        # Test
        for wrong_username in not_allowed_usernames:
            user_data = self.get_user_data(wrong_username, "test_password")
            info("### Try to create user \"%s\" ###\n" % wrong_username)
            status_code, response_data = execute_request(self.PATH,
                                                         "POST",
                                                         json.dumps(user_data),
                                                         switch_ip)

            assert status_code == httplib.BAD_REQUEST, "Validation failed, " \
                "didn't return BAD REQUEST status code. Status code: %s" \
                % status_code

            info("### Status code is BAD REQUEST, response: %s ###\n"
                 % response_data)

        info("\n########## End Test Create user: invalid username "
             "##########\n")

    def test_create_user_max_username(self):
        info("\n########## Test Create user: max username "
             "##########\n")
        # Test Setup
        max_username = ''.join(random.choice(string.ascii_lowercase)
                               for _ in range(MAX_USERNAME))

        # Test
        expected_data = self.get_user_data(max_username, "password")

        info("### Try to create user: \"%s\" ###\n" %
             json.dumps(expected_data))

        status_code, response_data = execute_request(self.PATH,
                                                     "POST",
                                                     json.dumps(expected_data),
                                                     switch_ip)

        assert status_code == httplib.CREATED, "Validation failed, request " \
            "didn't return Created status code. Status code: %s" % status_code

        info("### Status code is CREATED ###")

        info("### Check if user is created ###")
        query_path = self.PATH + "?depth=1"
        status_code, response_data = execute_request(query_path, "GET",
                                                     None, switch_ip)

        assert status_code == httplib.OK, "Validation failed, " \
            "didn't return OK status code. Status code: %s" % status_code

        info("### Status code is OK ###")

        query_data = {}
        try:
            query_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        username = expected_data["configuration"]["username"]
        assert self.check_user_exists(query_data, username), \
            "Wrong expected data. Expected data: %s Returned data: %s" \
            % (expected_data["configuration"], query_data["configuration"])

        info("\n########## End Test Create user: max username "
             "##########\n")

    def test_create_user_long_password(self):
        info("\n########## Test Create user: long password "
             "##########\n")
        # Test Setup
        long_password = ''.join("a" for _ in range(128))

        # Test
        expected_data = self.get_user_data("test_user_long_password",
                                           long_password)

        info("### Try to create user: \"%s\" ###\n" %
             json.dumps(expected_data))

        status_code, response_data = execute_request(self.PATH,
                                                     "POST",
                                                     json.dumps(expected_data),
                                                     switch_ip)

        assert status_code == httplib.CREATED, "Validation failed, request " \
            "didn't return Created status code. Status code: %s" % status_code

        info("### Status code is CREATED ###")

        info("### Check if user is created ###")
        query_path = self.PATH + "?depth=1"
        status_code, response_data = execute_request(query_path, "GET",
                                                     None, switch_ip)

        assert status_code == httplib.OK, "Validation failed, " \
            "didn't return OK status code. Status code: %s" % status_code

        info("### Status code is OK ###")

        query_data = {}
        try:
            query_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        username = expected_data["configuration"]["username"]
        assert self.check_user_exists(query_data, username), \
            "Wrong expected data. Expected data: %s Returned data: %s" \
            % (expected_data["configuration"], query_data["configuration"])

        info("\n########## End Test Create user: long password "
             "##########\n")

    def test_create_user_empty_username_and_password(self):
        info("\n########## Test Create user: empty username and "
             "empty password ##########\n")
        # Test Setup
        user_data = self.get_user_data("", "")
        info("### Try to create user \"%s\" ###\n" % json.dumps(user_data))
        status_code, response_data = execute_request(self.PATH,
                                                     "POST",
                                                     json.dumps(user_data),
                                                     switch_ip)

        assert status_code == httplib.BAD_REQUEST, "Validation failed, " \
            "didn't return BAD REQUEST status code. Status code: %s" \
            % status_code

        info("### Status code is BAD REQUEST, response: %s ###\n"
             % response_data)

        info("\n########## End Test Create user: empty username "
             "and empty password ##########\n")

    def test_create_user_empty_password(self):
        info("\n########## Test Create user: empty password "
             "##########\n")
        # Test Setup
        user_data = self.get_user_data("user_empty_password", "")
        info("### Try to create user \"%s\" ###\n" % json.dumps(user_data))
        status_code, response_data = execute_request(self.PATH,
                                                     "POST",
                                                     json.dumps(user_data),
                                                     switch_ip)

        assert status_code == httplib.BAD_REQUEST, "Validation failed, " \
            "didn't return BAD REQUEST status code. Status code: %s" \
            % status_code

        info("### Status code is BAD REQUEST, response: %s ###\n"
             % response_data)
        info("\n########## End Test Create user: empty password "
             "##########\n")

    def test_create_existent_user(self):
        info("\n########## Test Create user: existent user "
             "##########\n")
        # Test Setup
        user_data = self.get_user_data("existent_user", "password")
        info("### Try to create user \"%s\" ###\n" % json.dumps(user_data))
        status_code, response_data = execute_request(self.PATH,
                                                     "POST",
                                                     json.dumps(user_data),
                                                     switch_ip)

        assert status_code == httplib.CREATED, "Validation failed, " \
            "didn't return CREATED status code. Status code: %s" \
            % status_code

        info("### Status code is CREATED, response: %s ###\n"
             % response_data)

        info("### Try to create user again \"%s\" ###\n" %
             json.dumps(user_data))
        status_code, response_data = execute_request(self.PATH,
                                                     "POST",
                                                     json.dumps(user_data),
                                                     switch_ip)

        assert status_code == httplib.BAD_REQUEST, "Validation failed, " \
            "didn't return BAD_REQUEST status code. Status code: %s" \
            % status_code

        info("### Status code is BAD_REQUEST, response: %s ###\n"
             % response_data)

        info("\n########## End Test Create user: existent user "
             "##########\n")

    def test_create_two_user_with_same_password(self):
        info("\n########## Test Create user: two user with the same password "
             "##########\n")
        # Test Setup
        password = "same_password"
        user_data_1 = self.get_user_data("test_user_pass_1", password)
        user_data_2 = self.get_user_data("test_user_pass_2", password)

        # Test
        info("### Try to create user: \"%s\" ###\n" % json.dumps(user_data_1))

        status_code, response_data = execute_request(self.PATH,
                                                     "POST",
                                                     json.dumps(user_data_1),
                                                     switch_ip)
        assert status_code == httplib.CREATED, "Validation failed, request " \
            "didn't return Created status code. Status code: %s" % status_code
        info("### Status code is CREATED ###")

        info("### Try to create user: \"%s\" ###\n" % json.dumps(user_data_2))
        status_code, response_data = execute_request(self.PATH,
                                                     "POST",
                                                     json.dumps(user_data_2),
                                                     switch_ip)
        assert status_code == httplib.CREATED, "Validation failed, request " \
            "didn't return Created status code. Status code: %s" % status_code
        info("### Status code is CREATED ###\n")

        info("### Check if user are created ###\n")
        query_path = self.PATH + "?depth=1"
        status_code, response_data = execute_request(query_path, "GET",
                                                     None, switch_ip)

        assert status_code == httplib.OK, "Validation failed, " \
            "didn't return OK status code. Status code: %s" % status_code

        info("### Status code is OK ###")

        query_data = {}
        try:
            query_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        username_1 = user_data_1["configuration"]["username"]
        username_2 = user_data_2["configuration"]["username"]

        assert self.check_user_exists(query_data, username_1), \
            "Wrong expected data. Expected data: %s Returned data: %s" \
            % (user_data_1["configuration"], query_data["configuration"])
        assert self.check_user_exists(query_data, username_2), \
            "Wrong expected data. Expected data: %s Returned data: %s" \
            % (user_data_2["configuration"], query_data["configuration"])
        info("### Users are created ###\n")

        info("### Check if password/salt are different ###\n")
        switch = self.net.switches[0]
        password_enc_user1 = switch.cmd(SHADOW_CMD % username_1).rstrip("\r\n")
        password_enc_user2 = switch.cmd(SHADOW_CMD % username_2).rstrip("\r\n")
        info("### Password Encrypted User %s: %s  ###\n" %
             (username_1, password_enc_user1))
        info("### Password Encrypted User %s: %s  ###\n" %
             (username_2, password_enc_user2))

        assert password_enc_user1 != password_enc_user2, "Error encrypted " \
            "password are equal"

        info("\n########## End Test Create user: two user with the "
             "same password ##########\n")


@users_post_disable
class Test_CreateUser:

    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_CreateUser.test_var = CreateUserTest()

    def teardown_class(cls):
        Test_CreateUser.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def _del_(self):
        del selt.test_var

    def test_run_call_create_user_valid_username_and_password(self):
        self.test_var.test_create_user_valid_username_and_password()

    def test_run_call_create_user_invalid_username(self):
        self.test_var.test_create_user_invalid_username()

    def test_run_call_create_user_max_username(self):
        self.test_var.test_create_user_max_username()

    def test_run_call_create_user_long_password(self):
        self.test_var.test_create_user_long_password()

    def test_run_call_create_user_empty_username_and_password(self):
        self.test_var.test_create_user_empty_username_and_password()

    def test_run_call_create_user_empty_password(self):
        self.test_var.test_create_user_empty_password()

    def test_run_call_create_existent_user(self):
        self.test_var.test_create_existent_user()

    def test_run_call_create_two_user_with_same_password(self):
        self.test_var.test_create_two_user_with_same_password()
