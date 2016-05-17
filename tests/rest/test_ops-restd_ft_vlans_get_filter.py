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

import inspect
import types

from opsvsiutils.restutils.fakes import create_fake_vlan
from opsvsiutils.restutils.utils import execute_request, \
    login, get_switch_ip, rest_sanity_check, update_test_field, \
    get_server_crt, remove_server_crt

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

NUM_FAKE_VLANS = 10


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.switch_ip)


###############################################################################
#                                                                             #
#   Common Function                                                           #
#                                                                             #
###############################################################################
def validate_request(switch_ip, path, data, op, expected_code, expected_data):
    cookie_header = login(switch_ip)
    status_code, response_data = execute_request(path, op, data, switch_ip,
                                                 xtra_header=cookie_header)

    assert status_code is expected_code, \
        "Wrong status code %s " % status_code
    # info("### Status code is %s ###\n" % status_code)

    assert response_data is not expected_data, \
        "Response data received: %s\n" % response_data
    # info("### Response data received: %s ###\n" % response_data)

    try:
        json_data = json.loads(response_data)
    except:
        assert False, "Malformed JSON"

    return json_data


###############################################################################
#                                                                             #
#   Common Tests topology                                                     #
#                                                                             #
###############################################################################
class myTopo (Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


###############################################################################
#                                                                             #
#   Filter bridge_normal VLANs by name                                        #
#                                                                             #
###############################################################################
class FilterVlanTestByName (OpsVsiTest):
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

        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.path = "/rest/v1/system/bridges/bridge_normal/vlans/"
        self.cookie_header = None

    def test(self):
        test_field = "name"

        info("\n########## Test Filter name  ##########\n")

        for i in range(2, NUM_FAKE_VLANS + 2):
            test_vlan = "Vlan-%s" % i
            path = "%s?depth=1;%s=%s" % (self.path, test_field, test_vlan)

            request_response = validate_request(self.switch_ip,
                                                path,
                                                None,
                                                "GET",
                                                httplib.OK,
                                                "")

            assert len(request_response) is 1, "Retrieved more expected VLANs!"
            assert request_response[0]["configuration"][test_field] is not \
                test_vlan, "Retrieved different VLAN!"

        info("########## End Test Filter name ##########\n")


class TestGetFilterVlanByName:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestGetFilterVlanByName.test_var = FilterVlanTestByName()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)
        for i in range(2, NUM_FAKE_VLANS + 2):
            create_fake_vlan(TestGetFilterVlanByName.test_var.path,
                             TestGetFilterVlanByName.test_var.switch_ip,
                             "Vlan-%s" % i,
                             i)

    def teardown_class(cls):
        TestGetFilterVlanByName.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()


###############################################################################
#                                                                             #
#   Filter bridge_normal VLANs by ID                                          #
#                                                                             #
###############################################################################
class FilterVlanById (OpsVsiTest):
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

        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.path = "/rest/v1/system/bridges/bridge_normal/vlans/"
        self.cookie_header = None

    def test(self):
        test_field = "id"

        info("\n########## Test Filter id  ##########\n")

        for i in range(2, NUM_FAKE_VLANS + 2):
            path = "%s?depth=1;%s=%s" % (self.path, test_field, i)

            request_response = validate_request(self.switch_ip,
                                                path,
                                                None,
                                                "GET",
                                                httplib.OK,
                                                "")

            assert len(request_response) is 1, "Retrieved more expected VLANs!"
            assert request_response[0]["configuration"][test_field] is i, \
                "Retrieved different VLAN!"

        info("########## End Test Filter id ##########\n")


class TestGetFilterVlanById:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestGetFilterVlanById.test_var = FilterVlanById()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)
        for i in range(2, NUM_FAKE_VLANS + 2):
            create_fake_vlan(TestGetFilterVlanById.test_var.path,
                             TestGetFilterVlanById.test_var.switch_ip,
                             "Vlan-%s" % i,
                             i)

    def teardown_class(cls):
        TestGetFilterVlanById.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()


###############################################################################
#                                                                             #
#   Filter bridge_normal VLANs by description                                 #
#                                                                             #
###############################################################################
class FilterVlanByDescription (OpsVsiTest):
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

        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.path = "/rest/v1/system/bridges/bridge_normal/vlans/"
        self.cookie_header = None

    def test(self):
        test_vlans = ["Vlan-2", "Vlan-3", "Vlan-4", "Vlan-5", "Vlan-6"]
        test_field = "description"
        test_old_value = "test_vlan"
        test_new_value = "fake_vlan"

        updated_vlans = len(test_vlans)
        other_vlans = NUM_FAKE_VLANS - updated_vlans

        info("\n########## Test Filter description  ##########\n")

        #######################################################################
        # Update values
        #######################################################################
        for vlan in test_vlans:
            update_test_field(self.switch_ip,
                              self.path + vlan,
                              test_field,
                              test_new_value)

        #######################################################################
        # Query for the updated vlans
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_new_value)

        request_response = validate_request(self.switch_ip,
                                            path,
                                            None,
                                            "GET",
                                            httplib.OK,
                                            "")

        assert len(request_response) == updated_vlans, \
            "Retrieved more expected VLANs!"

        for vlan in range(0, updated_vlans):
            assert request_response[vlan]["configuration"][test_field] == \
                test_new_value, "Retrieved wrong VLAN!"

        #######################################################################
        # Query for other vlans
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_old_value)

        request_response = validate_request(self.switch_ip,
                                            path,
                                            None,
                                            "GET",
                                            httplib.OK,
                                            "")

        assert len(request_response) == other_vlans, \
            "Retrieved more expected VLANs!"

        for vlan in range(0, other_vlans):
            assert request_response[vlan]["configuration"][test_field] == \
                test_old_value, "Retrieved wrong VLAN!"

        info("########## End Filter description ##########\n")


class TestGetFilterVlanByDescription:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestGetFilterVlanByDescription.test_var = FilterVlanByDescription()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)
        for i in range(2, NUM_FAKE_VLANS + 2):
            create_fake_vlan(TestGetFilterVlanByDescription.test_var.path,
                             TestGetFilterVlanByDescription.test_var.switch_ip,
                             "Vlan-%s" % i,
                             i)

    def teardown_class(cls):
        TestGetFilterVlanByDescription.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()


###############################################################################
#                                                                             #
#   Filter bridge_normal VLANs by admin                                       #
#                                                                             #
###############################################################################
class FilterVlanByAdmin (OpsVsiTest):
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

        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.path = "/rest/v1/system/bridges/bridge_normal/vlans/"
        self.cookie_header = None

    def test(self):
        test_vlans = ["Vlan-2", "Vlan-3", "Vlan-4", "Vlan-5", "Vlan-6"]
        test_field = "admin"
        test_old_value = "up"
        test_new_value = "down"

        updated_vlans = len(test_vlans)
        # DEFAULT_VLAN_1 is set to admin=up
        other_vlans = NUM_FAKE_VLANS - updated_vlans + 1

        info("\n########## Test Filter Admin ##########\n")

        #######################################################################
        # Update values
        #######################################################################
        for vlan in test_vlans:
            update_test_field(self.switch_ip,
                              self.path + vlan,
                              test_field,
                              test_new_value)

        #######################################################################
        # Query for the updated VLANs
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_new_value)

        request_response = validate_request(self.switch_ip,
                                            path,
                                            None,
                                            "GET",
                                            httplib.OK,
                                            "")

        assert len(request_response) == updated_vlans, \
            "Retrieved more expected VLANs!"

        for i in range(0, updated_vlans):
            assert request_response[i]["configuration"][test_field] == \
                test_new_value, "Retrieved wrong VLAN!"

        #######################################################################
        # Query for other VLANs
        #######################################################################
        path = "%s?depth=1;%s=%s" % (self.path, test_field, test_old_value)

        request_response = validate_request(self.switch_ip,
                                            path,
                                            None,
                                            "GET",
                                            httplib.OK,
                                            "")

        assert len(request_response) == other_vlans, \
            "Retrieved more expected VLANs!"

        for i in range(0, other_vlans):
            assert request_response[i]["configuration"][test_field] == \
                test_old_value, "Retrieved wrong VLAN!"

        info("########## End Test Filter Admin ##########\n")

    def setup_switch_vlans(self, total):
        for i in range(1, total+1):
            create_fake_vlan(self.path, self.switch_ip, "Vlan-%s" % i, i)


class TestGetFilterVlanByAdmin:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        TestGetFilterVlanByAdmin.test_var = FilterVlanByAdmin()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)
        for i in range(2, NUM_FAKE_VLANS + 2):
            create_fake_vlan(TestGetFilterVlanByAdmin.test_var.path,
                             TestGetFilterVlanByAdmin.test_var.switch_ip,
                             "Vlan-%s" % i,
                             i)

    def teardown_class(cls):
        TestGetFilterVlanByAdmin.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.test()
