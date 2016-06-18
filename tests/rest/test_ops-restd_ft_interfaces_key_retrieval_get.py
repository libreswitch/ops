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
    get_switch_ip, get_json, rest_sanity_check, get_server_crt, \
    remove_server_crt


NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

TEST_HEADER = "Test to validate Specific Column Retrieval"
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


class ColretrieveInterfaceTest(OpsVsiTest):
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

        self.path = "/rest/v1/system/interfaces" \
                    "?selector=status;depth=1;sort=name;"
        self.switch_ip = get_switch_ip(self.net.switches[0])
        self.cookie_header = None

    def get_keys_to_retrieve(self, keys):
        appended_keys = ""
        if keys:
            appended_keys = ','.join(keys)
        return appended_keys

    def validate_retrieved_data_by_keys(self, complete_data_rows, data_rows,
                                        keys):
        if (len(complete_data_rows) == len(data_rows) and len(keys) > 0 and
           len(complete_data_rows) > 0 and len(data_rows) > 0):
            for i in range(len(data_rows)):
                assert (not len(data_rows[i]['status']) or
                        len(data_rows[i]['status']) == len(keys)), \
                    "The amount of keys are different to %s." % len(keys)
                for key in data_rows[i]["status"]:
                    assert data_rows[i]["status"][key] is not None, \
                        "The value is empty for key %s" % key
                    assert data_rows[i]["status"][key] == \
                        complete_data_rows[i]["status"][key], \
                        "The values is different to the original row"
            return True

        return False

    def test_single_column_retrieval(self):
        # Test Setup
        test_title = "- Single column retrieval in GET request"
        info(TEST_START % test_title)
        keys = ["name"]
        appended_keys = self.get_keys_to_retrieve(keys)
        new_path = self.path + "keys=" + appended_keys
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        complete_data_rows = get_json(response_data)

        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        data_rows = get_json(response_data)
        info("### Data successfully retrieved. Status code 200 OK ###\n")
        # Test
        # 2 - Validate that data exist in rows by keys retrieval
        result = \
            self.validate_retrieved_data_by_keys(complete_data_rows,
                                                 data_rows, keys)
        assert result is True, "Wrong data length: %s <--> %s\n" \
            % (len(complete_data_rows), len(data_rows))
        info("### Retrieved data validated ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_multiple_column_retrieval(self):
        # Test Setup
        test_title = "- Multiple column retrieval in GET request"
        info(TEST_START % test_title)
        keys = ["name", "type"]
        appended_keys = self.get_keys_to_retrieve(keys)
        new_path = self.path + "keys=" + appended_keys
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        complete_data_rows = get_json(response_data)

        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        data_rows = get_json(response_data)
        info("### Data successfully retrieved. Status code 200 OK ###\n")
        # Test
        # 2 - Validate that data exist in rows by keys retrieval
        result = \
            self.validate_retrieved_data_by_keys(complete_data_rows,
                                                 data_rows, keys)
        assert result is True, "Wrong data length: %s <--> %s\n" \
            % (len(complete_data_rows), len(data_rows))
        info("### Retrieved data validated ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_column_retrieval_without_depth_argument(self):
        # Test Setup
        test_title = "- Column retrieval without depth argument in GET request"
        info(TEST_START % test_title)
        keys = ["name"]
        appended_keys = self.get_keys_to_retrieve(keys)
        fixed_path = "/rest/v1/system/interfaces" \
                     "?selector=configuration;sort=name;"
        new_path = fixed_path + "keys=" + appended_keys
        # 1 - Query Resource
        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("Response: %s\n" % response_data)
        info("### Expected Bad Request. Status code 400 BAD_REQUEST ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_column_retrieval_with_empty_keys_argument(self):
        # Test Setup
        test_title = "- Column retrieval with empty keys argument in " \
                     "GET request"
        info(TEST_START % test_title)
        keys = []
        appended_keys = self.get_keys_to_retrieve(keys)
        new_path = self.path + "keys=" + appended_keys
        # 1 - Query Resource
        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Expected Bad Request. Status code 400 BAD_REQUEST ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_column_retrieval_with_nonexistent_column_key(self):
        # Test Setup
        test_title = "- Column retrieval with invalid column key in " \
                     "GET request"
        info(TEST_START % test_title)
        keys = ["foo"]
        appended_keys = self.get_keys_to_retrieve(keys)
        new_path = self.path + "keys=" + appended_keys
        # 1 - Query Resource
        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.BAD_REQUEST, \
            "Wrong status code %s " % status_code
        info("### Expected Bad Request. Status code 400 BAD_REQUEST ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_column_retrieval_with_filter(self):
        # Test Setup
        test_title = "- Column retrieval in GET request by specifying filter"
        info(TEST_START % test_title)
        keys = ["name", "type"]
        appended_keys = self.get_keys_to_retrieve(keys)
        fixed_path = self.path + ";name=10"
        new_path = self.path + "keys=" + appended_keys + ";name=10"
        # 1 - Query Resource
        response, response_data = execute_request(
            fixed_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        complete_data_rows = get_json(response_data)

        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        data_rows = get_json(response_data)
        info("### Data successfully retrieved. Status code 200 OK ###\n")
        # Test
        # 2 - Validate that data exist in rows by keys retrieval
        result = \
            self.validate_retrieved_data_by_keys(complete_data_rows,
                                                 data_rows, keys)
        assert result is True, "Wrong data length: %s <--> %s\n" \
            % (len(complete_data_rows), len(data_rows))
        info("### Retrieved data validated ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_column_retrieval_with_pagination(self):
        # Test Setup
        test_title = "- Column retrieval in GET request with pagination"
        info(TEST_START % test_title)
        keys = ["name", "type"]
        appended_keys = self.get_keys_to_retrieve(keys)
        fixed_path = self.path + ";limit=10;offset=10;"
        new_path = fixed_path + "keys=" + appended_keys
        # 1 - Query Resource
        response, response_data = execute_request(
            fixed_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        complete_data_rows = get_json(response_data)

        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        data_rows = get_json(response_data)
        info("### Data successfully retrieved. Status code 200 OK ###\n")
        # Test
        # 2 - Validate that data exist in rows by keys retrieval
        result = \
            self.validate_retrieved_data_by_keys(complete_data_rows,
                                                 data_rows, keys)
        assert result is True, "Wrong data length: %s <--> %s\n" \
            % (len(complete_data_rows), len(data_rows))
        info("### Retrieved data validated ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_column_retrieval_with_depth_greater_than_one(self):
        # Test Setup
        test_title = "- Column retrieval in GET request with depth > 1"
        info(TEST_START % test_title)
        keys = ["name", "type"]
        appended_keys = self.get_keys_to_retrieve(keys)
        fixed_path = "/rest/v1/system/interfaces?depth=2;sort=name;"
        new_path = fixed_path + "keys=" + appended_keys
        # 1 - Query Resource
        response, response_data = execute_request(
            fixed_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        complete_data_rows = get_json(response_data)

        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        data_rows = get_json(response_data)
        info("### Data successfully retrieved. Status code 200 OK ###\n")
        # Test
        # 2 - Validate that data exist in rows by keys retrieval
        result = \
            self.validate_retrieved_data_by_keys(complete_data_rows,
                                                 data_rows, keys)
        assert result is True, "Wrong data length: %s <--> %s\n" \
            % (len(complete_data_rows), len(data_rows))
        info("### Retrieved data validated ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_column_retrieval_in_requests_other_than_GET(self):
        # Test Setup
        test_title = "- Column retrieval in requests other than GET"
        info(TEST_START % test_title)
        keys = ["name"]
        appended_keys = self.get_keys_to_retrieve(keys)
        fixed_path = "/rest/v1/system/interfaces?"
        new_path = fixed_path + "keys=" + appended_keys
        # 1 - Query Resource
        requests = ["POST", "PUT", "DELETE"]
        for request in requests:
            response, response_data = execute_request(
                new_path, request, None, self.switch_ip, True,
                xtra_header=self.cookie_header)

            status_code = response.status
            assert status_code == httplib.BAD_REQUEST, \
                "Wrong status code %s " % status_code
            info("Response("+request+"): %s\n" % response_data)
        info("### Expected Bad Request. Status code 400 BAD_REQUEST ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_column_retrieval_with_applicable_arguments(self):
        # Test Setup
        test_title = "- Column retrieval in GET request with all applicable "
        "arguments"
        info(TEST_START % test_title)
        keys = ["name"]
        appended_keys = self.get_keys_to_retrieve(keys)
        fixed_path = self.path + "name=10;limit=1;"
        new_path = fixed_path + "keys=" + appended_keys
        # 1 - Query Resource
        response, response_data = execute_request(
            fixed_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        complete_data_rows = get_json(response_data)

        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        data_rows = get_json(response_data)
        info("### Data successfully retrieved. Status code 200 OK ###\n")
        # Test
        # 2 - Validate that data exist in rows by keys retrieval
        result = \
            self.validate_retrieved_data_by_keys(complete_data_rows,
                                                 data_rows, keys)
        assert result is True, "Wrong data length: %s <--> %s\n" \
            % (len(complete_data_rows), len(data_rows))
        info("### Retrieved data validated ###\n")
        # Test Teardown
        info(TEST_END % test_title)

    def test_column_retrieval_separate_keys_argument(self):
        # Test Setup
        test_title = "- Column retrieval in GET request with keys "
        "arguments added separately"
        info(TEST_START % test_title)
        keys = ["name", "type"]
        appended_keys = self.get_keys_to_retrieve(keys)
        new_path = self.path + "keys=" + keys[0] + ";keys=" + \
            keys[1]
        # 1 - Query Resource
        response, response_data = execute_request(
            self.path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        complete_data_rows = get_json(response_data)

        response, response_data = execute_request(
            new_path, "GET", None, self.switch_ip, True,
            xtra_header=self.cookie_header)

        status_code = response.status
        assert status_code == httplib.OK, "Wrong status code %s " % status_code
        data_rows = get_json(response_data)
        info("### Data successfully retrieved. Status code 200 OK ###\n")
        # Test
        # 2 - Validate that data exist in rows by keys retrieval
        result = \
            self.validate_retrieved_data_by_keys(complete_data_rows,
                                                 data_rows, keys)
        assert result is True, "Wrong data length: %s <--> %s\n" \
            % (len(complete_data_rows), len(data_rows))
        info("### Retrieved data validated ###\n")
        # Test Teardown
        info(TEST_END % test_title)


class Test_ColretrieveInterface:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_ColretrieveInterface.test_var = ColretrieveInterfaceTest()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.switch_ip)

    def teardown_class(cls):
        Test_ColretrieveInterface.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run_call_test_single_column_retrieval(self, netop_login):
        self.test_var.test_single_column_retrieval()

    def test_run_call_test_multiple_column_retrieval(self, netop_login):
        self.test_var.test_multiple_column_retrieval()

    def test_run_call_test_column_retrieval_without_depth_argument(self, netop_login):
        self.test_var.test_column_retrieval_without_depth_argument()

    def test_run_call_test_column_retrieval_with_empty_keys_argument(self, netop_login):
        self.test_var.test_column_retrieval_with_empty_keys_argument()

    def test_run_call_test_column_retrieval_with_nonexistent_column_key(self, netop_login):
        self.test_var.test_column_retrieval_with_nonexistent_column_key()

    def test_run_call_test_column_retrieval_with_filter(self, netop_login):
        self.test_var.test_column_retrieval_with_filter()

    def test_run_call_test_column_retrieval_with_pagination(self, netop_login):
        self.test_var.test_column_retrieval_with_pagination()

    def test_run_call_test_column_retrieval_with_depth_greater_than_one(self, netop_login):
        self.test_var.test_column_retrieval_with_depth_greater_than_one()

    def test_run_call_test_column_retrieval_in_requests_other_than_GET(self, netop_login):
        self.test_var.test_column_retrieval_in_requests_other_than_GET()

    def test_run_call_test_column_retrieval_with_applicable_arguments(self, netop_login):
        self.test_var.test_column_retrieval_with_applicable_arguments()

    def test_run_call_test_column_retrieval_separate_keys_argument(self, netop_login):
        self.test_var.test_column_retrieval_separate_keys_argument()
