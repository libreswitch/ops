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


import pytest

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
from opsvsiutils.restutils.fakes import create_fake_vlan, FAKE_VLAN_DATA
from opsvsiutils.restutils.utils import execute_request, login, \
    rest_sanity_check, get_switch_ip, compare_dict, \
    get_server_crt, remove_server_crt
from copy import deepcopy

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

base_vlan_data = {
    "configuration": {
        "name": "test",
        "id": 1,
        "description": "test vlan",
        "admin": ["up"],
        "other_config": {},
        "external_ids": {}
    }
}

test_vlan_data = {}
test_vlan_data["int"] = deepcopy(base_vlan_data)
test_vlan_data["string"] = deepcopy(base_vlan_data)
test_vlan_data["dict"] = deepcopy(base_vlan_data)
test_vlan_data["empty_array"] = deepcopy(base_vlan_data)
test_vlan_data["one_string"] = deepcopy(base_vlan_data)
test_vlan_data["multiple_string"] = deepcopy(base_vlan_data)
test_vlan_data["None"] = deepcopy(base_vlan_data)
test_vlan_data["boolean"] = deepcopy(base_vlan_data)
DEFAULT_BRIDGE = "bridge_normal"

TEST_HEADER = "Test to validate If-Match"
TEST_START = "\n########## " + TEST_HEADER + " %s ##########\n"
TEST_END = "\n########## End " + TEST_HEADER + " %s ##########\n"


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.switch_ip)


class IfMatchVlanTest(OpsVsiTest):
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

        self.path = "/rest/v1/system/bridges"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.vlan_id = 2
        self.vlan_name = "fake_vlan"
        self.vlan_path = "%s/%s/vlans" % (self.path, DEFAULT_BRIDGE)
        self.vlan = "%s/%s/vlans/%s" % (self.path,
                                        DEFAULT_BRIDGE,
                                        self.vlan_name)
        self.config_selector = "?selector=configuration"
        self.cookie_header = None

    def test_put_vlan_with_star_etag(self):
        info(TEST_START % "PUT VLAN with star Etag")
        # 1 - Query Resource
        cond_path = self.vlan + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)

        # 2 - Modify data
        put_data = pre_put_get_data["configuration"]
        put_data["description"] = "Star Etag"

        # Add If-Match: '"*"' to the request
        config_data = {'configuration': put_data}
        headers = {"If-Match": '"*"'}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "PUT", json.dumps(config_data), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.OK, "Error modifying a VLAN using "\
            "if-match option. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### VLAN Modified. Status code 200 OK  ###\n")

        # 3 - Verify Modified data
        status_code, response_data = execute_request(
            cond_path, "GET", None, self.switch_ip,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "VLAN %s doesn't exists" % cond_path
        post_put_data = {}
        try:
            post_put_get_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        post_put_data = post_put_get_data["configuration"]

        assert compare_dict(post_put_data, put_data), "Configuration data is "\
            "not equal that posted data"
        info("### Configuration data validated %s ###\n" % response_data)

        info(TEST_END % "PUT VLAN with star Etag")

    def test_put_vlan_etag_match(self):
        info(TEST_START % "PUT VLAN with matching Etag")
        # 1 - Query Resource
        cond_path = self.vlan + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)

        # 2 - Modify data
        put_data = pre_put_get_data["configuration"]
        put_data["description"] = "Etag match"

        config_data = {'configuration': put_data}
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "PUT", json.dumps(config_data), self.switch_ip,
            False, headers)

        assert status_code == httplib.OK, "Error modifying "\
            "a VLAN using if-match(precondition failed) option. "\
            "Status code: %s Response data: %s " % (status_code, response_data)

        # 3 - Verify Modified data
        status_code, response_data = execute_request(
            cond_path, "GET", None, self.switch_ip,
            xtra_header=self.cookie_header)
        assert status_code == httplib.OK, "VLAN %s doesn't exists" % cond_path

        post_put_data = {}
        try:
            post_put_get_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        post_put_data = post_put_get_data["configuration"]

        assert compare_dict(post_put_data, put_data), "Configuration data is "\
            "not equal that posted data"
        info("### Configuration data validated %s ###\n" % response_data)

        info(TEST_END % "PUT VLAN with matching Etag")

    def test_put_vlan_same_state_not_matching_etag(self):
        info(TEST_START % "PUT VLAN with not matching Etag "
             "and not state change")
        # 1 - Query Resource
        cond_path = self.vlan + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)

        # 2 - Set not matching etag
        put_data = pre_put_get_data["configuration"]
        if etag:
            etag = etag[::-1]
        else:
            etag = '"abcdef"'

        # 2 - Set same unchanged data
        config_data = {'configuration': put_data}
        headers = {'If-Match': etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "PUT", json.dumps(config_data), self.switch_ip,
            False, headers)

        assert status_code == httplib.OK, "Error modifying a VLAN using "\
            "if-match option. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### VLAN Modified. Status code 200 OK  ###\n")

        # 3 - Verify Modified data
        status_code, response_data = execute_request(
            cond_path, "GET", None, self.switch_ip,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "VLAN %s doesn't exists" % cond_path
        post_put_data = {}
        try:
            post_put_get_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        post_put_data = post_put_get_data["configuration"]

        assert compare_dict(post_put_data, put_data), "Configuration data "\
            "is not equal that posted data"
        info("### Configuration data validated %s ###\n" % response_data)

        info(TEST_END % "PUT VLAN with not matching Etag and not state change")

    def test_put_vlan_etag_not_match(self):
        info(TEST_START % "PUT VLAN with not matching Etag")
        # 1 - Query Resource
        cond_path = self.vlan + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)

        # 2 - Modify data
        put_data = pre_put_get_data["configuration"]
        put_data["description"] = "Etag not match"
        if etag:
            etag = etag[::-1]
        else:
            etag = '"abcdef"'

        config_data = {'configuration': put_data}
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "PUT", json.dumps(config_data), self.switch_ip,
            False, headers)

        assert status_code == httplib.PRECONDITION_FAILED, "Error modifying "\
            "a VLAN using if-match(precondition failed) option. "\
            "Status code: %s Response data: %s " % (status_code, response_data)
        info("### VLAN no Modified. Status code 412 OK  ###\n")

        info(TEST_END % "PUT VLAN with not matching Etag")

    def test_post_vlan_etag_match(self):
        info(TEST_START % "POST VLAN with matching Etag")
        # 1 - Query Resource
        cond_path = self.vlan_path + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)

        # Fill Vlan data
        fake_vlan_name = "VLAN3"
        vlan_id = 3
        data = FAKE_VLAN_DATA % {"name": fake_vlan_name, "id": vlan_id}

        # Try to create the resource using a valid etag
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "POST", data, self.switch_ip, False, headers)

        assert status_code == httplib.CREATED, "Error creating a VLAN using "\
            "if-match option. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### VLAN Created. Status code 201 CREATED  ###\n")

        # Delete created VLAN
        self.delete_fake_vlan_if_exists(fake_vlan_name)

        info(TEST_END % "POST VLAN with matching Etag")

    def test_post_vlan_etag_not_match(self):
        info(TEST_START % "POST VLAN with not matching Etag")
        # 1 - Query Resource
        cond_path = self.vlan_path + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)
        # Set wrong etag
        if etag:
            etag = etag[::-1]
        else:
            etag = '"abcdef"'

        # Fill Vlan data
        fake_vlan_name = "VLAN3"
        vlan_id = 3
        data = FAKE_VLAN_DATA % {"name": fake_vlan_name, "id": vlan_id}

        # Try to create the resource using a invalid etag
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "POST", data, self.switch_ip, False, headers)

        assert status_code == httplib.PRECONDITION_FAILED, "Error creating "\
            "using if-match using invalid etag. Status code: %s "\
            "Response data: %s " % (status_code, response_data)
        info("### VLAN No Created. Status code 412 Precondition Failed  ###\n")

        info(TEST_END % "POST VLAN with not matching Etag")

    def test_get_all_vlan_etag_match(self):
        info(TEST_START % "GET all VLANs with matching Etag")
        # 1 - Query Resource
        cond_path = self.vlan_path + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)

        # Try to retrieve the resource using a valid etag
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "GET", None, self.switch_ip, False, headers)
        assert status_code == httplib.OK, "Error retrieving VLANs using " \
            "valid etag Status code: %s Response data: %s " % \
            (status_code, response_data)
        info("### VLANs retrieved. Status code 200 OK  ###\n")

        info(TEST_END % "GET all VLANs with  matching Etag")

    def test_get_all_vlan_etag_not_match(self):
        info(TEST_START % "GET all VLANs with not matching Etag")
        # 1 - Query Resource
        cond_path = self.vlan_path + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)
        # Set wrong etag
        if etag:
            etag = etag[::-1]
        else:
            etag = '"abcdef"'

        # Try to retrieve the resource using a invalid etag
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "GET", None, self.switch_ip, False, headers)

        assert status_code == httplib.PRECONDITION_FAILED,\
            "Error retrieving VLANs using invalid etag. Status code: %s" \
            "Response data: %s " % (status_code, response_data)
        info("### VLANs not retrieved. Status code 412 "
             "Precondition Failed  ###\n")

        info(TEST_END % "GET all VLANs with not matching Etag")

    def test_get_vlan_etag_match(self):
        info(TEST_START % "GET VLAN with matching Etag")
        # 1 - Query Resource
        cond_path = self.vlan + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)

        # Try to retrieve the resource using a valid etag
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "GET", None, self.switch_ip, False, headers)

        assert status_code == httplib.OK, "Error retrieving VLAN using "\
            "valid etag Status code: %s Response data: %s " % \
            (status_code, response_data)
        info("### VLANs retrieved. Status code 200 OK  ###\n")

        info(TEST_END % "GET VLAN with matching Etag")

    def test_get_vlan_etag_not_match(self):
        info(TEST_START % "GET VLAN with not matching Etag")
        # 1 - Query Resource
        cond_path = self.vlan + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)
        # Set wrong etag
        if etag:
            etag = etag[::-1]
        else:
            etag = '"abcdef"'

        # Try to retrieve the resource using a invalid etag
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "GET", None, self.switch_ip, False, headers)

        assert status_code == httplib.PRECONDITION_FAILED,\
            "Error retrieving VLAN using invalid etag. "\
            "Status code: %s Response data: %s " % (status_code, response_data)
        info("### VLANs not retrieved. Status code 412 "
             "Precondition Failed ###\n")

        info(TEST_END % "GET VLAN with not matching Etag")

    def test_delete_vlan_etag_match(self):
        info(TEST_START % "DELETE VLAN with matching Etag")
        # 1- Create Fake VLAN
        fake_vlan_name = "VLAN3"
        vlan_id = 3
        create_fake_vlan(Test_IfMatchVlan.test_var.vlan_path,
                         Test_IfMatchVlan.test_var.switch_ip,
                         fake_vlan_name, vlan_id)

        # 2- Query Resource
        cond_path = self.vlan_path + "/" + fake_vlan_name\
            + self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)

        # 3- Delete the vlan using the matching etag
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "DELETE", None, self.switch_ip, False, headers)

        assert status_code == httplib.NO_CONTENT, "Error deleting VLAN using "\
            "valid etag Status code: %s Response data: %s " % \
            (status_code, response_data)
        info("### VLAN deleted. Status code NOT CONTENT 204  ###\n")

        info(TEST_END % "DELETE VLAN with matching Etag")

    def test_delete_vlan_etag_not_match(self):
        info(TEST_START % "DELETE VLAN with not matching Etag")
        # 1- Create Fake VLAN
        fake_vlan_name = "VLAN3"
        vlan_id = 3
        create_fake_vlan(Test_IfMatchVlan.test_var.vlan_path,
                         Test_IfMatchVlan.test_var.switch_ip,
                         fake_vlan_name, vlan_id)

        # 2- Query Resource
        cond_path = self.vlan_path + "/" + fake_vlan_name +\
            self.config_selector
        etag, pre_put_get_data = self.get_etag_and_data(cond_path)

        # Set wrong etag
        if etag:
            etag = etag[::-1]
        else:
            etag = '"abcdef"'

        # 3- Try to delete the resource using a invalid etag
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            cond_path, "GET", None, self.switch_ip, False, headers)

        assert status_code == httplib.PRECONDITION_FAILED, "Error deleting "\
            "VLAN using invalid etag. Status code: %s Response data: %s "\
            % (status_code, response_data)
        info("### VLANs not deleted. Status code 412 "
             "Precondition Failed ###\n")

        # Delete created VLAN
        self.delete_fake_vlan_if_exists(fake_vlan_name)

        info(TEST_END % "DELETE VLAN with not matching Etag")

    def get_etag_and_data(self, cond_path):
        response, response_data = execute_request(
            cond_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        etag = response.getheader("Etag")
        assert status_code == httplib.OK, "VLAN %s doesn't exists" % cond_path
        info("Etag = %s" % etag)
        pre_put_get_data = {}
        try:
            pre_put_get_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"
        info("\n### Query Resource %s  ###\n" % response_data)
        return etag, pre_put_get_data

    def delete_fake_vlan_if_exists(self, vlan_name):
        info("\n### Deleting VLAN %s  ###\n" % vlan_name)
        path = self.vlan_path + "/" + vlan_name
        status_code, response_data = execute_request(
            path, "GET", None, self.switch_ip, xtra_header=self.cookie_header)

        if status_code == httplib.OK:
            status_code, response_data = execute_request(
                path, "DELETE", None, self.switch_ip,
                xtra_header=self.cookie_header)

            assert status_code == httplib.NO_CONTENT, "VLAN deleted" % path


class Test_IfMatchVlan:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_IfMatchVlan.test_var = IfMatchVlanTest()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)
        create_fake_vlan(Test_IfMatchVlan.test_var.vlan_path,
                         Test_IfMatchVlan.test_var.switch_ip,
                         Test_IfMatchVlan.test_var.vlan_name,
                         Test_IfMatchVlan.test_var.vlan_id)

    def teardown_class(cls):
        Test_IfMatchVlan.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run_call_put_vlan_with_star_etag(self, netop_login):
        self.test_var.test_put_vlan_with_star_etag()

    def test_run_call_put_vlan_etag_match(self, netop_login):
        self.test_var.test_put_vlan_etag_match()

    def test_run_call_put_vlan_same_state_not_matching_etag(self, netop_login):
        self.test_var.test_put_vlan_same_state_not_matching_etag()

    def test_run_call_put_vlan_etag_not_match(self, netop_login):
        self.test_var.test_put_vlan_etag_not_match()

    def test_run_call_post_vlan_etag_match(self, netop_login):
        self.test_var.test_post_vlan_etag_match()

    def test_run_call_post_vlan_etag_not_match(self, netop_login):
        self.test_var.test_post_vlan_etag_not_match()

    def test_run_call_get_all_vlan_etag_match(self, netop_login):
        self.test_var.test_get_all_vlan_etag_match()

    def test_run_call_get_all_vlan_etag_not_match(self, netop_login):
        self.test_var.test_get_all_vlan_etag_not_match()

    def test_run_call_get_vlan_etag_match(self, netop_login):
        self.test_var.test_get_vlan_etag_match()

    def test_run_call_get_vlan_etag_not_match(self, netop_login):
        self.test_var.test_get_vlan_etag_not_match()

    def test_run_call_delete_vlan_etag_match(self, netop_login):
        self.test_var.test_delete_vlan_etag_match()

    def test_run_call_delete_vlan_etag_not_match(self, netop_login):
        self.test_var.test_delete_vlan_etag_not_match()
