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

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import urllib
import subprocess

from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, get_container_id
from opsvsiutils.restutils.swagger_test_utility import \
    swagger_model_verification

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0
response_global = ""


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws

        switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class systemTest(OpsVsiTest):

    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch, host=None, link=None,
                           controller=None, build=True)

        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.PATH = "/rest/v1/system"
        self.cookie_header = None

    def test_call_system_get(self):
        global response_global
        info("\n########## Executing GET request on %s ##########\n"
             % self.PATH)

        # # Execute GET

        response, json_string = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, True,
            xtra_header=self.cookie_header)

        assert response.status == httplib.OK, "GET request failed: {0} \
            {1}".format(response.status, response.reason)

        get_data = {}

        try:
            # A malformed json should throw an exception here
            get_data = json.loads(json_string)
        except:
            assert False, "GET: Malformed JSON in response body"

        # # Check data was received

        assert get_data, "GET: Empty response"
        assert type(get_data) is dict, "GET: Malformed response"
        assert len(get_data) > 0, "GET: No data in response"

        info("\n########## Finished executing GET request on %s ##########\n"
             % self.PATH)

    def test_call_system_options(self):
        info("\n########## Executing OPTIONS request on %s ##########\n"
             % self.PATH)

        # # Execute OPTIONS

        response, json_string = execute_request(
            self.PATH, "OPTIONS", None, self.SWITCH_IP, True,
            xtra_header=self.cookie_header)

        assert response.status == httplib.OK, "OPTIONS request failed: {0} \
            {1}".format(response.status, response.reason)

        # # Check expected options are correct

        # TODO change these to propper expected values after correct OPTIONS
        # is implemented
        expected_allow = ["DELETE", "GET", "OPTIONS", "POST", "PUT", "PATCH"]
        response_allow = response.getheader("allow").split(", ")

        assert expected_allow == response_allow, "OPTIONS: unexpected 'allow'\
            options"

        info("\n########## Finished executing OPTIONS request on %s \
            ##########\n" % self.PATH)

    def test_call_system_put(self):
        info("\n########## Executing PUT request on %s ##########\n"
             % self.PATH)

        # # Get initial data
        response, pre_put_json_string = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, True,
            xtra_header=self.cookie_header)

        assert response.status == httplib.OK, "PUT: initial GET request \
            failed: {0} {1}".format(response.status, response.reason)
        pre_put_get_data = {}

        try:
            # A malformed json should throw an exception here
            pre_put_get_data = json.loads(pre_put_json_string)
        except:
            assert False, "PUT: Malformed JSON in response body for initial \
                GET request"

        # # Execute PUT request

        put_data = pre_put_get_data['configuration']

        # Modify config keys
        put_data['hostname'] = 'switch'

        dns_servers = ["8.8.8.8"]
        if 'dns_servers' in put_data:
            put_data['dns_servers'].extend(dns_servers)
        else:
            put_data['dns_servers'] = dns_servers

        put_data['asset_tag_number'] = "1"

        other_config = {
            'stats-update-interval': "5001",
            'min_internal_vlan': "1024",
            'internal_vlan_policy': 'ascending',
            'max_internal_vlan': "4094",
            'enable-statistics': "false"
        }
        if 'other_config' in put_data:
            put_data['other_config'].update(other_config)
        else:
            put_data['other_config'] = other_config

        put_data['external_ids'] = {"id1": "value1"}

        ecmp_config = {
            'hash_srcip_enabled': "false",
            'hash_srcport_enabled': "false",
            'hash_dstip_enabled': "false",
            'enabled': "false",
            'hash_dstport_enabled': "false"
        }
        if 'ecmp_config' in put_data:
            put_data['ecmp_config'].update(ecmp_config)
        else:
            put_data['ecmp_config'] = ecmp_config

        bufmon_config = {
            'collection_period': "5",
            'threshold_trigger_rate_limit': "60",
            'periodic_collection_enabled': "false",
            'counters_mode': 'current',
            'enabled': "false",
            'snapshot_on_threshold_trigger': "false",
            'threshold_trigger_collection_enabled': "false"
        }
        if 'bufmon_config' in put_data:
            put_data['bufmon_config'].update(bufmon_config)
        else:
            put_data['bufmon_config'] = bufmon_config

        logrotate_config = {
            'maxsize': "10",
            'period': 'daily',
            'target': ''
        }
        if 'logrotate_config' in put_data:
            put_data['logrotate_config'].update(logrotate_config)
        else:
            put_data['logrotate_config'] = logrotate_config

        response_global = {"configuration": put_data}
        response, json_string = \
            execute_request(self.PATH, "PUT",
                            json.dumps({'configuration': put_data}),
                            self.SWITCH_IP, True,
                            xtra_header=self.cookie_header)

        assert response.status == httplib.OK, "PUT request failed: {0} \
            {1}".format(response.status, response.reason)

        # # Get post-PUT data

        response, post_put_json_string = execute_request(
            self.PATH, "GET", None, self.SWITCH_IP, True,
            xtra_header=self.cookie_header)

        assert response.status == httplib.OK, "PUT: Post-PUT GET request \
            failed: {0} {1}".format(response.status, response.reason)

        post_put_get_data = {}

        try:
            # A malformed json should throw an exception here
            post_put_get_data = json.loads(post_put_json_string)
        except:
            assert False, "PUT: Malformed JSON in post-PUT GET request body"

        # post-PUT data should be the same as pre-PUT data
        post_put_data = post_put_get_data['configuration']

        assert put_data == post_put_data, "PUT: Mismatch between PUT request\
            data and post-PUT GET response"

        # # Perform bad PUT request

        json_string = json.dumps({'configuration': put_data})
        json_string += ","

        response, json_string = execute_request(
            self.PATH, "PUT", json_string, self.SWITCH_IP, True,
            xtra_header=self.cookie_header)

        assert response.status == httplib.BAD_REQUEST, "PUT: Malformed JSON \
            did not yield BAD_REQUEST: {0} {1}".format(response.status,
                                                       response.reason)

        info("\n########## Finished executing PUT request on %s ##########\n"
             % self.PATH)


class Test_system:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_system.test_var = systemTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)
        cls.container_id = get_container_id(cls.test_var.net.switches[0])

    def teardown_class(cls):
        Test_system.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run_call_sytem_get(self, netop_login):
        self.test_var.test_call_system_get()
        info("container_id_test_get_id %s\n" % self.container_id)
        swagger_model_verification(self.container_id, "/system", "GET_ID",
                                   response_global)

    def test_run_call_sytem_options(self, netop_login):
        self.test_var.test_call_system_options()

    def test_run_call_sytem_put(self, netop_login):
        self.test_var.test_call_system_put()
