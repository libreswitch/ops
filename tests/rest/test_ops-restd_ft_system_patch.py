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
from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, get_server_crt, \
    remove_server_crt


NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

TEST_HEADER = "Test to validate PATCH"
TEST_START = "\n########## " + TEST_HEADER + " %s ##########\n"
TEST_END = "########## End " + TEST_HEADER + " %s ##########\n"


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.switch_ip)


class PatchSystemTest(OpsVsiTest):
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

        self.path = "/rest/v1/system?selector=configuration"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.cookie_header = None

    def check_malformed_json(self, response_data):
        try:
            data = json.loads(response_data)
            return data
        except:
            assert False, "Malformed JSON"

    def test_patch_add_new_value(self):
        # Test Setup
        test_title = "using \"op\": \"add\" with a new value"
        info(TEST_START % test_title)
        data = ["1.1.1.1"]
        patch = [{"op": "add", "path": "/dns_servers", "value": data}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)
        post_patch_data = post_patch_data['configuration']['dns_servers']

        assert post_patch_data == data, "Configuration data is not "\
            "equal that posted data"
        post_patch_etag = response.getheader("Etag")
        assert etag != post_patch_etag, "Etag should not be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/dns_servers"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code

        info(TEST_END % test_title)

    def test_patch_add_new_value_with_invalid_etag(self):
        # Test Setup
        test_title = "using \"op\": \"add\" with a new value and invalid etag"
        info(TEST_START % test_title)
        data = ["1.1.1.1"]
        patch = [{"op": "add", "path": "/dns_servers", "value": data}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        before_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": "abcdefghijklmnopqrstuvwxyz12345678901234"}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.PRECONDITION_FAILED, \
            "Wrong status code %s " % status_code
        info("### System data remains the same. "
             "Status code 412 PRECONDITION FAILED  ###\n")

        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        after_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        info("Before patch etag: %s\n" % before_patch_etag)
        info("After  patch etag: %s\n" % after_patch_etag)
        assert before_patch_etag == after_patch_etag, "The etag should be " \
                                                      "the same"
        info(TEST_END % test_title)

    def test_patch_add_replace_existing_field(self):
        # Test Setup
        test_title = "using \"op\": \"add\" replace existing field"
        info(TEST_START % test_title)
        # 1 - Query Resource
        data = ["1.2.3.4"]
        patch = [{"op": "add", "path": "/dns_servers", "value": ["1.1.1.1"]},
                 {"op": "add", "path": "/dns_servers", "value": data}]
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)
        post_patch_data = post_patch_data['configuration']['dns_servers']

        assert post_patch_data == data, "Configuration data is not "\
            "equal that posted data"
        post_patch_etag = response.getheader("Etag")
        assert etag != post_patch_etag, "Etag should not be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/dns_servers"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info(TEST_END % test_title)

    def test_patch_add_an_array_element(self):
        # Test Setup
        test_title = "using \"op\": \"add\" adding an Array Element"
        info(TEST_START % test_title)
        # 1 - Query Resource
        data = ["1.1.1.1", "1.2.3.4"]
        patch = [{"op": "add", "path": "/dns_servers", "value": ["1.1.1.1"]},
                 {"op": "add", "path": "/dns_servers/1", "value": "1.2.3.4"}]
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)
        post_patch_data = post_patch_data['configuration']['dns_servers']

        assert post_patch_data == data, "Configuration data is not "\
            "equal that posted data"
        post_patch_etag = response.getheader("Etag")
        assert etag != post_patch_etag, "Etag should not be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/dns_servers"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code

        info(TEST_END % test_title)

    def test_patch_add_an_object_member(self):
        # Test Setup
        test_title = "using \"op\": \"add\" an Object Member"
        info(TEST_START % test_title)
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)
        # 1.1- Modify the Data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)

        data = {"baz": "qux"}
        patch = [{"op": "add", "path": "/other_config", "value": {}},
                 {"op": "add", "path": "/other_config/foo", "value": "bar"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 1.2 Query the resource again
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data: Add a new object member
        patch2 = [{"op": "add", "path": "/other_config/baz", "value": "qux"}]
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch2),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)
        post_patch_data = post_patch_data['configuration']['other_config']

        assert data["baz"] == post_patch_data["baz"], \
            "Configuration data is not equal that posted data"
        post_patch_etag = response.getheader("Etag")
        assert etag != post_patch_etag, "Etag should not be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/other_config/foo"},
                 {"op": "remove", "path": "/other_config/baz"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code

        info(TEST_END % test_title)

    def test_patch_add_an_empty_optional_member(self):
        # Test Setup
        test_title = "using \"op\": \"add\" empty optional member"
        info(TEST_START % test_title)
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data: Add a new object member
        data = {"maxsize": "20"}
        patch2 = [{"op": "add", "path": "/logrotate_config/maxsize",
                   "value": "20"}]
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch2),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)
        post_patch_data = post_patch_data['configuration']['logrotate_config']

        assert data["maxsize"] == post_patch_data["maxsize"], \
            "Configuration data is not equal that posted data"
        post_patch_etag = response.getheader("Etag")
        assert etag != post_patch_etag, "Etag should not be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/logrotate_config/maxsize"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code

        info(TEST_END % test_title)

    def test_patch_add_value_with_malformed_patch(self):
        # Test Setup
        test_title = "using \"op\": \"add\" field value with malformed patch"
        info(TEST_START % test_title)
        data = ["1.1.1.1"]
        patch = [{"op": "remove", "path": "/dns_servers"},
                 {"path": "/dns_servers", "value": data}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)

        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " \
            % status_code
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        post_patch_etag = response.getheader("Etag")
        assert etag == post_patch_etag, "Etag should be the same"
        info("### System remains the same. Status code 400 BAD REQUEST  ###\n")
        info(TEST_END % test_title)

    def test_patch_add_new_value_for_boolean_field(self):
        # Test Setup
        test_title = "using \"op\": \"add\" with a new value for boolean field"
        info(TEST_START % test_title)
        data = "true"
        patch = [{"op": "add", "path": "/other_config", "value": {}},
                 {"op": "add", "path": "/other_config/enable-statistics",
                  "value": data}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)
        post_patch_data = post_patch_data['configuration']['other_config']

        assert post_patch_data["enable-statistics"] == data,\
            "Configuration data is not equal that posted data"
        post_patch_etag = response.getheader("Etag")
        assert etag != post_patch_etag, "Etag should not be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/other_config/enable-statistics"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code

        info(TEST_END % test_title)

    def test_patch_add_multiple_fields(self):
        # Test Setup
        test_title = "using \"op\": \"add\" multiple fields"
        info(TEST_START % test_title)
        data = ["true", ["1.1.1.1"], "bar"]
        patch = [{"op": "add", "path": "/other_config", "value": {}},
                 {"op": "add", "path": "/other_config/enable-statistics",
                  "value": data[0]},
                 {"op": "add", "path": "/dns_servers", "value": data[1]},
                 {"op": "add", "path": "/other_config/foo", "value": data[2]}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)
        post_patch_data = post_patch_data['configuration']

        assert post_patch_data["other_config"]["enable-statistics"] == \
            data[0], "Configuration data is not equal that posted data"
        assert post_patch_data["dns_servers"] == data[1],\
            "Configuration data is not equal that posted data"
        assert post_patch_data["other_config"]["foo"] == data[2],\
            "Configuration data is not equal that posted data"
        post_patch_etag = response.getheader("Etag")
        assert etag != post_patch_etag, "Etag should not be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/other_config/foo"},
                 {"op": "remove", "path": "/other_config/enable-statistics"},
                 {"op": "remove", "path": "/dns_servers"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code

        info(TEST_END % test_title)

    def test_patch_test_operation_nonexistent_value(self):
        # Test Setup
        test_title = "using \"op\": \"test\" a nonexistent value"
        info(TEST_START % test_title)
        data = "bar"
        patch = [{"op": "test", "path": "/other_config/foo", "value": data}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " \
            % status_code
        info("### System remains the same. Status code 400 BAD REQUEST  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)

        assert etag == post_patch_etag, "Etag should be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)
        info(TEST_END % test_title)

    def test_patch_test_with_malformed_value(self):
        # Test Setup
        test_title = "using \"op\": \"test\" with a malformed path value"
        info(TEST_START % test_title)
        data = "test data"
        eval_list = ['a/b', '/ab', 'ab/', 'a//b', 'a///b', 'a\\/b']

        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)
        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        for i in range(len(eval_list)):
            patch = [{"op": "add", "path": "/other_config", "value": {}},
                     {"op": "add", "path": "/other_config/" + eval_list[i],
                      "value": data},
                     {"op": "test", "path": "/other_config/" + eval_list[i],
                      "value": data}]
            info("%s\n" % patch)
            status_code, response_data = execute_request(self.path, "PATCH",
                                                         json.dumps(patch),
                                                         self.switch_ip, False,
                                                         headers)
            info("REST API response after evaluate the patch with "
                 "string %s in path: %s\n" % (eval_list[i], response_data))
            assert status_code == httplib.BAD_REQUEST, \
                "Wrong status code %s " % status_code

        info("### Configuration data validated ###\n")
        info(TEST_END % test_title)

    def test_patch_test_operation_for_existent_value(self):
        # Test Setup
        test_title = "using \"op\": \"test\" for existent value"
        info(TEST_START % test_title)
        data = ["1.1.1.1"]
        patch = [{"op": "add", "path": "/dns_servers", "value": data}]
        patch_test = [{"op": "test", "path": "/dns_servers", "value": data}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 2.1 - Test data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch_test), self.switch_ip, False,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System remains the same. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)

        assert etag == post_patch_etag, "Etag should be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/dns_servers"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info(TEST_END % test_title)

    def test_patch_copy_existing_value(self):
        # Test Setup
        test_title = "using \"op\": \"copy\" for existent value"
        info(TEST_START % test_title)
        data = "this is a test"
        patch = [{"op": "add", "path": "/other_config", "value": {}},
                 {"op": "add", "path": "/other_config/foo", "value": data}]
        patch_test = [{"op": "copy", "from": "/other_config/foo",
                       "path": "/other_config/copy_of_foo"}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 2.1 - Test data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch_test), self.switch_ip, False,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)

        assert etag != post_patch_etag, "Etag should not be the same"

        post_patch_data = post_patch_data['configuration']['other_config']
        assert post_patch_data['copy_of_foo'] == post_patch_data['foo'],\
            "Configuration data is not equal that copied data"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/other_config/foo"},
                 {"op": "remove", "path": "/other_config/copy_of_foo"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info(TEST_END % test_title)

    def test_patch_copy_nonexistent_value(self):
        # Test Setup
        test_title = "using \"op\": \"copy\" for nonexistent value"
        info(TEST_START % test_title)
        patch_test = [{"op": "copy", "from": "/other_config/foo",
                       "path": "/other_config/copy_of_foo"}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch_test),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " \
            % status_code
        info("### System remains the same. Status code 400 BAD REQUEST  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)

        assert etag == post_patch_etag, "Etag should be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)
        info(TEST_END % test_title)

    def test_patch_move_existent_value(self):
        # Test Setup
        test_title = "using \"op\": \"move\" for existent value"
        info(TEST_START % test_title)
        data = "1.1.1.1"
        patch = [{"op": "add", "path": "/other_config", "value": {}},
                 {"op": "add", "path": "/other_config/servers", "value": data}]
        patch_test = [{"op": "move", "from": "/other_config/servers",
                       "path": "/other_config/dns_servers"}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 2.1 - Test data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch_test),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)

        assert etag != post_patch_etag, "Etag should not be the same"

        post_patch_data = post_patch_data["configuration"]
        assert data == post_patch_data["other_config"]["dns_servers"],\
            "Configuration data is not equal that copied data"

        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/other_config/dns_servers"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info(TEST_END % test_title)

    def test_patch_move_nonexistent_value(self):
        # Test Setup
        test_title = "using \"op\": \"move\" a nonexistent value"
        info(TEST_START % test_title)
        patch_test = [{"op": "move", "from": "/other_config/servers",
                       "path": "/other_config/dns_servers"}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch_test),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " \
            % status_code
        info("### System remains the same. Status code 400 BAD REQUEST  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        assert etag == post_patch_etag, "Etag should be the same"
        info(TEST_END % test_title)

    def test_patch_move_value_to_invalid_path(self):
        # Test Setup
        test_title = "using \"op\": \"move\" value to invalid path"
        info(TEST_START % test_title)
        data = "this is a test"
        patch = [{"op": "add", "path": "/other_config", "value": {}},
                 {"op": "add", "path": "/other_config/abc", "value": data}]
        patch_test = [{"op": "move", "from": "/other_config/abc",
                       "path": "/other_config/abc/def"}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 2.1 - Test data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch_test),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " \
            % status_code
        info("### System remains the same. Status code 400 BAD REQUEST  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)

        assert etag == post_patch_etag, "Etag should be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/other_config/abc"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info(TEST_END % test_title)

    def test_patch_replace_existent_value(self):
        # Test Setup
        test_title = "using \"op\": \"replace\" for existent value"
        info(TEST_START % test_title)
        data = "foo"
        patch_data = "bar"
        patch = [{"op": "add", "path": "/other_config", "value": {}},
                 {"op": "add", "path": "/other_config/test", "value": data}]
        patch_test = [{"op": "replace", "path": "/other_config/test",
                       "value": patch_data}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 2.1 - Test data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch_test),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)

        assert etag != post_patch_etag, "Etag should not be the same"

        post_patch_data = post_patch_data["configuration"]
        assert patch_data == post_patch_data["other_config"]["test"],\
            "Configuration data is not equal that copied data"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/other_config/test"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info(TEST_END % test_title)

    def test_patch_replace_nonexistent_value(self):
        # Test Setup
        test_title = "using \"op\": \"replace\" for nonexistent value"
        info(TEST_START % test_title)
        data = "foo"
        patch_data = "bar"
        patch = [{"op": "add", "path": "/other_config", "value": {}},
                 {"op": "add", "path": "/other_config/test", "value": data}]
        patch_test = [{"op": "replace",
                       "path": "/other_config/non_existent_field",
                       "value": patch_data}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 2.1 - Test data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch_test),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.BAD_REQUEST, "Wrong status code %s " \
            % status_code
        info("### System remains the same. Status code 400 BAD REQUEST  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)

        assert etag == post_patch_etag, "Etag should be the same"
        info("### Configuration data validated %s ###\n" % post_patch_data)

        # Test Teardown
        headers = {"If-Match": post_patch_etag}
        headers.update(self.cookie_header)
        patch = [{"op": "remove", "path": "/other_config/test"}]
        status_code, response_data = execute_request(
            self.path, "PATCH", json.dumps(patch), self.switch_ip,
            xtra_header=headers)

        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info(TEST_END % test_title)

    def test_patch_remove_existent_value(self):
        # Test Setup
        test_title = "using \"op\": \"remove\" for existent value"
        info(TEST_START % test_title)
        data = "foo"
        patch = [{"op": "add", "path": "/other_config", "value": {}},
                 {"op": "add", "path": "/other_config/test", "value": data}]
        patch_test = [{"op": "remove", "path": "/other_config/test"}]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        self.check_malformed_json(response_data)

        # Test
        # 2 - Modify data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        etag = response.getheader("Etag")
        status_code = response.status
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 2.1 - Test data
        headers = {"If-Match": etag}
        headers.update(self.cookie_header)
        status_code, response_data = execute_request(self.path, "PATCH",
                                                     json.dumps(patch_test),
                                                     self.switch_ip, False,
                                                     headers)
        assert status_code == httplib.NO_CONTENT, "Wrong status code %s " \
            % status_code
        info("### System Modified. Status code 204 NO CONTENT  ###\n")

        # 3 - Verify Modified data
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        post_patch_etag = response.getheader("Etag")
        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code

        post_patch_data = self.check_malformed_json(response_data)

        assert etag != post_patch_etag, "Etag should not be the same"

        # If "test" was the last value in other_config,
        # GET will not return the column at all if removed
        if "other_config" in post_patch_data["configuration"]:
            assert "test" not in \
                post_patch_data["configuration"]["other_config"], \
                "Something went wrong when removing the data"

        info("### Configuration data validated %s ###\n" % post_patch_data)
        info(TEST_END % test_title)


class Test_PatchSystem:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_PatchSystem.test_var = PatchSystemTest()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        Test_PatchSystem.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_call_patch_add_new_value(self, netop_login):
        self.test_var.test_patch_add_new_value()

    def test_call_patch_add_replace_existing_field(self, netop_login):
        self.test_var.test_patch_add_replace_existing_field()

    def test_call_patch_add_an_array_element(self, netop_login):
        self.test_var.test_patch_add_an_array_element()

    def test_call_patch_add_an_object_member(self, netop_login):
        self.test_var.test_patch_add_an_object_member()

    def test_call_patch_add_an_empty_optional_member(self, netop_login):
        self.test_var.test_patch_add_an_empty_optional_member()

    def test_call_patch_add_value_with_malformed_patch(self, netop_login):
        self.test_var.test_patch_add_value_with_malformed_patch()

    def test_call_patch_add_new_value_for_boolean_field(self, netop_login):
        self.test_var.test_patch_add_new_value_for_boolean_field()

    def test_call_patch_add_multiple_fields(self, netop_login):
        self.test_var.test_patch_add_multiple_fields()

    def test_call_patch_test_operation_nonexistent_value(self, netop_login):
        self.test_var.test_patch_test_operation_nonexistent_value()

    def test_call_patch_test_with_malformed_value(self, netop_login):
        self.test_var.test_patch_test_with_malformed_value()

    def test_call_patch_test_operation_for_existent_value(self, netop_login):
        self.test_var.test_patch_test_operation_for_existent_value()

    def test_call_patch_copy_existing_value(self, netop_login):
        self.test_var.test_patch_copy_existing_value()

    def test_call_patch_copy_nonexistent_value(self, netop_login):
        self.test_var.test_patch_copy_nonexistent_value()

    def test_call_patch_move_existent_value(self, netop_login):
        self.test_var.test_patch_move_existent_value()

    def test_call_patch_move_nonexistent_value(self, netop_login):
        self.test_var.test_patch_move_nonexistent_value()

    def test_call_patch_move_value_to_invalid_path(self, netop_login):
        self.test_var.test_patch_move_value_to_invalid_path()

    def test_call_patch_replace_existent_value(self, netop_login):
        self.test_var.test_patch_replace_existent_value()

    def test_call_patch_replace_nonexistent_value(self, netop_login):
        self.test_var.test_patch_replace_nonexistent_value()

    def test_call_patch_remove_existent_value(self, netop_login):
        self.test_var.test_patch_remove_existent_value()

    def test_run_call_test_patch_add_new_value_with_invalid_etag(self,
                                                                 netop_login):
        self.test_var.test_patch_add_new_value_with_invalid_etag()
