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

from opsvsiutils.restutils.utils import get_switch_ip, execute_request, \
    rest_sanity_check, get_json, login
from opsvsiutils.restutils.utils import ACCOUNT_URI, DEFAULT_PASSWORD


NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

TEST_HEADER = "Self password change validation:"
TEST_START = "\n########## " + TEST_HEADER + " %s ##########\n"
TEST_END = "########## End " + TEST_HEADER + " %s ##########\n"

ROLE_NETOP = 'ops_netop'
READ_SWITCH_CONFIG = 'READ_SWITCH_CONFIG'
WRITE_SWITCH_CONFIG = 'WRITE_SWITCH_CONFIG'


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.addSwitch("s1")


class AccountTest(OpsVsiTest):
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
        self.cookie_header = None

    def change_password_bad_current_password(self):
        '''
        Assuming the user is logged in, attempt to change
        their password with an incorrect current password
        '''
        test_title = "attempt password change with wrong current password"
        info(TEST_START % test_title)

        # Attempt to change password
        data = {'configuration': {'password': 'wrongpassword',
                                  'new_password': 'newpassword'}}
        status_code, response_data = \
            execute_request(ACCOUNT_URI, "PUT", json.dumps(data),
                            self.SWITCH_IP, xtra_header=self.cookie_header)
        assert status_code == httplib.UNAUTHORIZED, \
            "Wrong status code %s " % status_code

        info(TEST_END % test_title)

    def change_password_missing_current_password(self):
        '''
        Assuming the user is logged in, attempt to change
        their password with a missing current password
        '''
        test_title = "attempt password change without current password"
        info(TEST_START % test_title)

        # Attempt to change password
        data = {'configuration': {'new_password': 'newpassword'}}
        status_code, response_data = \
            execute_request(ACCOUNT_URI, "PUT", json.dumps(data),
                            self.SWITCH_IP, xtra_header=self.cookie_header)
        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code

        info(TEST_END % test_title)

    def change_password_successful_change(self):
        '''
        Assuming the user is logged in, attempt to change
        their password with all correct data
        '''
        test_title = "attempt password change with correct data"
        info(TEST_START % test_title)

        # Initialize test data
        newpassword = 'newpassword'
        data = {'configuration': {'password': DEFAULT_PASSWORD,
                                  'new_password': newpassword}}

        # Attempt to change password
        status_code, response_data = \
            execute_request(ACCOUNT_URI, "PUT", json.dumps(data),
                            self.SWITCH_IP, xtra_header=self.cookie_header)
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        # Attempt a login with the new password
        self.cookie_header = login(self.SWITCH_IP, password=newpassword)

        # Change password back to default
        data['configuration']['password'] = newpassword
        data['configuration']['new_password'] = DEFAULT_PASSWORD
        status_code, response_data = \
            execute_request(ACCOUNT_URI, "PUT", json.dumps(data),
                            self.SWITCH_IP, xtra_header=self.cookie_header)
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        info(TEST_END % test_title)

    def change_password_missing_new_password(self):
        '''
        Assuming the user is logged in, attempt to change
        their password with a missing new password
        '''
        test_title = "attempt password change without new password"
        info(TEST_START % test_title)

        # Attempt to change password
        data = {'configuration': {'password': DEFAULT_PASSWORD}}
        status_code, response_data = \
            execute_request(ACCOUNT_URI, "PUT", json.dumps(data),
                            self.SWITCH_IP, xtra_header=self.cookie_header)
        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code

        info(TEST_END % test_title)

    def change_password_not_logged_in(self):
        '''
         Attempt changing password while not logged in
        '''
        test_title = "attempt password change not logged in"
        info(TEST_START % test_title)

        # Initialize test data
        newpassword = 'newpassword'
        data = {'configuration': {'password': DEFAULT_PASSWORD,
                                  'new_password': newpassword}}

        # Attempt to change password
        status_code, response_data = execute_request(ACCOUNT_URI, "PUT",
                                                     json.dumps(data),
                                                     self.SWITCH_IP)
        assert status_code == httplib.UNAUTHORIZED, \
            "Wrong status code %s " % status_code

        info(TEST_END % test_title)

    def query_account_information_logged_in(self):
        '''
        Query the user's account information (role and permissions)
        '''
        test_title = "Query user's account information"
        info(TEST_START % test_title)

        # Query user's information
        status_code, response_data = \
            execute_request(ACCOUNT_URI, "GET", None, self.SWITCH_IP,
                            xtra_header=self.cookie_header)
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        data = get_json(response_data)

        assert data, "Response data is empty"
        assert 'status' in data, "Response data does not contain status info"
        assert data['status'], "Status data is empty"
        assert 'role' in data['status'], "No role info found"
        assert 'permissions' in data['status'], "No permissions info found"

        role = data['status']['role']
        permissions = data['status']['permissions']

        assert role == ROLE_NETOP, \
            "Unexpected user role in response data"
        assert READ_SWITCH_CONFIG in permissions and \
            WRITE_SWITCH_CONFIG in permissions, \
            "Expected permissions not found in response data"

        info(TEST_END % test_title)

    def query_account_information_not_logged_in(self):
        '''
        Query the user's account information (role
        and permissions) while logged out
        '''
        test_title = "Query user's account information not logged in"
        info(TEST_START % test_title)

        # Query user's information
        status_code, response_data = execute_request(ACCOUNT_URI, "GET",
                                                     None, self.SWITCH_IP)
        assert status_code == httplib.UNAUTHORIZED, \
            "Wrong status code %s " % status_code

        info(TEST_END % test_title)


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class Test_Account:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        cls.test_var = AccountTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        cls.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_change_password_bad_current_password(self, netop_login):
        self.test_var.change_password_bad_current_password()

    def test_change_password_missing_current_password(self, netop_login):
        self.test_var.change_password_missing_current_password()

    def test_change_password_missing_new_password(self, netop_login):
        self.test_var.change_password_missing_new_password()

    def test_change_password_not_logged_in(self):
        self.test_var.change_password_not_logged_in()

    def test_change_password_successful_change(self, netop_login):
        self.test_var.change_password_successful_change()

    def test_query_account_information_logged_in(self, netop_login):
        self.test_var.query_account_information_logged_in()

    def test_query_account_information_not_logged_in(self):
        self.test_var.query_account_information_not_logged_in()
