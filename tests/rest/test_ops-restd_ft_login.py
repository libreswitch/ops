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

# Testing framework imports
from opsvsi.docker import *
from opsvsi.opsvsitest import *
from opsvsiutils.systemutil import *

import time
import httplib
import urllib

from opsvsiutils.restutils.utils import get_switch_ip, rest_sanity_check, \
    execute_request, get_server_crt, remove_server_crt
from opsvsiutils.restutils.utils import LOGIN_URI, DEFAULT_USER, \
    DEFAULT_PASSWORD

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

TEST_HEADER = "/login validation:"
TEST_START = "\n########## " + TEST_HEADER + " %s ##########\n"
TEST_END = "########## End " + TEST_HEADER + " %s ##########\n"

HEADERS = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.addSwitch("s1")


class LoginTest (OpsVsiTest):
    def setupNet(self):

        mytopo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sws=NUM_OF_SWITCHES,
                        hopts=self.getHostOpts(), sopts=self.getSwitchOpts())
        self.net = Mininet(topo=mytopo, switch=VsiOpenSwitch, host=None,
                           link=None, controller=None, build=True)

        self.SWITCH_IP = get_switch_ip(self.net.switches[0])

    def query_not_logged_in(self):
        '''
        This function verifies the user can't query on /login if not logged in
        '''
        test_title = "query login while not logged in"
        info(TEST_START % test_title)

        info("Executing GET on /login while not logged in...")
        status_code, response_data = execute_request(LOGIN_URI, "GET", None,
                                                     self.SWITCH_IP, False)
        assert status_code == httplib.UNAUTHORIZED, "Wrong status code " + \
            "when querying /login while not logged in: %s" % status_code
        info(" All good.\n")

        info(TEST_END % test_title)

    def successful_login(self):
        '''
        This verifies Login is successful when using correct data
        '''
        test_title = "successful Login"
        info(TEST_START % test_title)

        data = {'username': DEFAULT_USER, 'password': DEFAULT_PASSWORD}

        # Attempt Login
        info("Attempting login with correct data...")
        response, response_data = execute_request(LOGIN_URI, "POST",
                                                  urllib.urlencode(data),
                                                  self.SWITCH_IP, True,
                                                  HEADERS)
        assert response.status == httplib.OK, ("Login POST not successful, " +
                                               "code: %s " % response.status)
        info(" All good.\n")

        # Get cookie header
        cookie_header = {'Cookie': response.getheader('set-cookie')}

        time.sleep(2)

        # Verify Login was successful
        info("Verifying Login was successful...")
        status_code, response_data = execute_request(LOGIN_URI, "GET", None,
                                                     self.SWITCH_IP, False,
                                                     cookie_header)
        assert status_code == httplib.OK, ("Login GET not successful, " +
                                           "code: %s " % status_code)
        info(" All good.\n")

        info(TEST_END % test_title)

    def unsuccessful_login_with_wrong_password(self):
        '''
        This verifies Login is unsuccessful for an
        existent user but using a wrong password
        '''
        test_title = "unsuccessful Login with wrong password"
        info(TEST_START % test_title)

        data = {'username': DEFAULT_USER, 'password': 'wrongpassword'}

        # Attempt Login
        info("Attempting login with wrong password...")
        response, response_data = execute_request(LOGIN_URI, "POST",
                                                  urllib.urlencode(data),
                                                  self.SWITCH_IP, True,
                                                  HEADERS)
        assert response.status == httplib.UNAUTHORIZED, "Wrong status code" + \
            " when login in with wrong password: %s " % response.status

        info(" All good.\n")

        info(TEST_END % test_title)

    def unsuccessful_login_with_non_existent_user(self):
        '''
        This verifies Login is unsuccessful for a non-existent user
        '''
        test_title = "unsuccessful Login with non-existent user"
        info(TEST_START % test_title)

        data = {'username': 'john', 'password': 'doe'}

        # Attempt Login
        info("Attempting login with non-existent user...")
        response, response_data = execute_request(LOGIN_URI, "POST",
                                                  urllib.urlencode(data),
                                                  self.SWITCH_IP, True,
                                                  HEADERS)
        assert response.status == httplib.UNAUTHORIZED, "Wrong status code" + \
            " when login in with non-existent user: %s " % response.status

        info(" All good.\n")

        info(TEST_END % test_title)

    def unauthorized_user_login_attempt(self):
        '''
        This verifies that you can't login with
        a user that has no REST login permissions.
        Current login permissions include
        READ_SWITCH_CONFIG and WRITE_SWITCH_CONFIG.
        Currently, the only users that do not have
        either of these permissions are any user from
        the ops_admin group
        '''
        test_title = "login attempt by unauthorized user"
        info(TEST_START % test_title)

        data = {'username': 'admin', 'password': 'admin'}

        # Attempt Login
        info("Attempting login with an unauthorized user...")
        status_code, response_data = execute_request(LOGIN_URI, "POST",
                                                     urllib.urlencode(data),
                                                     self.SWITCH_IP, False,
                                                     HEADERS)
        assert status_code == httplib.UNAUTHORIZED, "Wrong status code " + \
            "when attempting login by an unauthorized user: %s " % status_code
        info(" All good.\n")

        info(TEST_END % test_title)


class Test_login:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        cls.test_var = LoginTest()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        cls.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_query_login_while_not_logged_in(self):
        self.test_var.query_not_logged_in()

    def test_successful_login(self):
        self.test_var.successful_login()

    def test_login_with_wrong_password(self):
        self.test_var.unsuccessful_login_with_wrong_password()

    def test_login_with_non_existent_user(self):
        self.test_var.unsuccessful_login_with_non_existent_user()

    def test_unauthorized_user_login_attempt(self):
        self.test_var.unauthorized_user_login_attempt()
