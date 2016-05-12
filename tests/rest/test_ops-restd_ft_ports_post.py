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

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import subprocess

from opsvsiutils.restutils.utils import execute_request, login, \
    get_switch_ip, rest_sanity_check, get_container_id, PORT_DATA, \
    execute_port_operations
from copy import deepcopy
from opsvsiutils.restutils.swagger_test_utility import \
    swagger_model_verification

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        self.switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class CreatePortTest (OpsVsiTest):
    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=NUM_HOSTS_PER_SWITCH,
                                       sws=NUM_OF_SWITCHES,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch, host=None, link=None,
                           controller=None, build=True)

        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.PATH = "/rest/v1/system/ports"
        self.PORT_PATH = self.PATH + "/Port1"
        self.cookie_header = None

    def create_port_with_depth(self):
        info("\n########## Test to Validate Create "
             "Port with depth ##########\n")
        status_code, response_data = execute_request(
            self.PATH + "?depth=1", "POST", json.dumps(PORT_DATA),
            self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Unexpected status code. Received: %s Response data: %s " % \
            (status_code, response_data)
        info("### Port not created. Status code is 400 BAD REQUEST ###\n")

        info("\n########## End Test to Validate Create Port with depth "
             "##########\n")

    def create_port(self):
        info("\n########## Test to Validate Create Port ##########\n")
        status_code, response_data = execute_request(
            self.PATH, "POST", json.dumps(PORT_DATA), self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.CREATED, \
            "Error creating a Port. Status code: %s Response data: %s " % \
            (status_code, response_data)
        info("### Port Created. Status code is 201 CREATED  ###\n")

        # Verify data
        status_code, response_data = execute_request(
            self.PORT_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Failed to query added Port"
        json_data = {}
        try:
            json_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        assert json_data["configuration"] == PORT_DATA["configuration"], \
            "Configuration data is not equal that posted data"
        info("### Configuration data validated ###\n")

        info("\n########## End Test to Validate Create Port ##########\n")

    def create_same_port(self):
        info("\n########## Test create same port ##########\n")
        status_code, response_data = execute_request(
            self.PORT_PATH, "POST", json.dumps(PORT_DATA), self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Validation failed, is not sending Bad Request error. " + \
            "Status code: %s" % status_code
        info("### Port not modified. Status code is 400 Bad Request  ###\n")

        info("\n########## End Test create same Port ##########\n")

    def verify_attribute_type(self):

        info("\n########## Test to verify attribute types ##########\n")

        info("\nAttempting to create port with incorrect type in attributes\n")

        data = [("ip4_address", 192, httplib.BAD_REQUEST),
                ("ip4_address", "192.168.0.1", httplib.CREATED),
                ("tag", "675", httplib.BAD_REQUEST),
                ("tag", 675, httplib.CREATED),
                ("trunks", "654, 675", httplib.BAD_REQUEST),
                ("trunks", [654, 675], httplib.CREATED)]
        results = execute_port_operations(data, "PortTypeTest", "POST",
                                          self.PATH, self.SWITCH_IP,
                                          self.cookie_header)

        assert results, "Unable to execute requests in verify_attribute_type"

        for attribute in results:
            assert attribute[1], "%s code issued " % attribute[2] + \
                "instead of %s for type " % attribute[3] + \
                "test in field '%s'" % attribute[0]
            info("%s code received as expected for field %s!\n" %
                 (attribute[2], attribute[0]))

        info("\n########## End test to verify attribute types ##########\n")

    def verify_attribute_range(self):

        info("\n########## Test to verify attribute ranges ##########\n")

        info("\nAttempting to create a port with out of range values in "
             "attributes\n")

        interfaces_out_of_range = []
        for i in range(1, 10):
            interfaces_out_of_range.append("/rest/v1/system/interfaces/%s" % i)

        data = [("ip4_address", "175.167.134.123/248", httplib.BAD_REQUEST),
                ("ip4_address", "175.167.134.123/24", httplib.CREATED),
                ("tag", 4095, httplib.BAD_REQUEST),
                ("tag", 675, httplib.CREATED),
                ("interfaces", interfaces_out_of_range, httplib.BAD_REQUEST),
                ("interfaces", ["/rest/v1/system/interfaces/1"],
                 httplib.CREATED)]
        results = execute_port_operations(data, "PortRangesTest", "POST",
                                          self.PATH, self.SWITCH_IP,
                                          self.cookie_header)

        assert results, "Unable to execute requests in verify_attribute_range"

        for attribute in results:
            assert attribute[1], "%s code issued " % attribute[2] + \
                "instead of %s for value range " % attribute[3] + \
                "test in field '%s'" % attribute[0]
            info("%s code received as expected for field %s!\n" %
                 (attribute[2], attribute[0]))

        info("\n########## End test to verify attribute ranges ##########\n")

    def verify_attribute_value(self):

        info("\n########## Test to verify attribute valid value ##########\n")

        info("\nAttempting to create port with invalid value in attributes\n")

        data = [("vlan_mode", "invalid_value", httplib.BAD_REQUEST),
                ("vlan_mode", "access", httplib.CREATED)]

        results = execute_port_operations(data, "PortValidValueTest", "POST",
                                          self.PATH, self.SWITCH_IP,
                                          self.cookie_header)

        assert results, "Unable to execute requests in verify_attribute_value"

        for attribute in results:
            assert attribute[1], "%s code issued " % attribute[2] + \
                "instead of %s for attribute " % attribute[3] + \
                "valid value test in field '%s'" % attribute[0]
            info("%s code received as expected for field %s!\n" %
                 (attribute[2], attribute[0]))

        info("\n########## End test to verify attribute valid value "
             "##########\n")

    def verify_missing_attribute(self):

        info("\n########## Test to verify missing attribute ##########\n")

        request_data = deepcopy(PORT_DATA)

        # Try to POST a port with missing attribute in request data

        info("\nAttempting to create a port with missing attribute in request "
             "data\n")

        del request_data['configuration']['name']

        status_code, response_data = execute_request(
            self.PATH, "POST", json.dumps(request_data), self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "%s code issued instead of BAD_REQUEST for Port with missing " + \
            "attribute" % status_code

        info("BAD_REQUEST code received as expected!")

        # Try to POST a port with all attributes in request data

        info("\nAttempting to create port with all attributes in request " +
             "data\n")

        request_data['configuration']['name'] = 'PortAllAttributes'

        status_code, response_data = execute_request(
            self.PATH, "POST", json.dumps(request_data), self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.CREATED, \
            "Got %s code instead of CREATED for Port with all attributes" % \
            status_code

        info("CREATE code received as expected!\n")

        info("\n########## End test to verify missing attribute ##########\n")

    def verify_unknown_attribute(self):

        info("\n########## Test to verify unkown attribute ##########\n")

        info("\nAttempting to create a port with an unknown attribute\n")

        data = [("unknown_attribute", "unknown_value", httplib.BAD_REQUEST),
                ("vlan_mode", "access", httplib.CREATED)]

        results = execute_port_operations(data, "PortUnknownAttributeTest",
                                          "POST", self.PATH, self.SWITCH_IP,
                                          self.cookie_header)

        assert results, "Unable to execute request in verify_unknown_attribute"

        for attribute in results:
            assert attribute[1], "%s code issued " % attribute[2] + \
                "instead of %s for unknown " % attribute[3] + \
                "attribute test in field '%s'" % attribute[0]
            info("%s code received as expected for field %s!\n" %
                 (attribute[2], attribute[0]))

        info("\n########## End test to verify unkown attribute ##########\n")

    def verify_malformed_json(self):

        info("\n########## Test to verify malformed JSON ##########\n")

        request_data = deepcopy(PORT_DATA)

        # Try to POST a port with a malformed JSON in request data

        info("\nAttempting to create port with a malformed JSON in request " +
             "data\n")

        request_data['configuration']['name'] = 'PortMalformedJSON'
        json_string = json.dumps(request_data)
        json_string += ","

        status_code, response_data = execute_request(
            self.PATH, "POST", json_string, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "%s code issued instead of BAD_REQUEST for Port with " + \
            "malformed JSON in request data" % status_code

        # Try to POST a port with a correct JSON in request data

        info("\nAttempting to create port with a correct JSON in request"
             "data\n")

        request_data['configuration']['name'] = 'PortCorrectJSON'
        json_string = json.dumps(request_data)

        status_code, response_data = execute_request(
            self.PATH, "POST", json_string, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.CREATED, \
            "%s code issued instead of CREATED for Port with correct JSON " + \
            "in request data" % status_code

        info("\n########## End test to verify malformed JSON ##########\n")


class Test_CreatePort:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_CreatePort.test_var = CreatePortTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)
        cls.container_id = get_container_id(cls.test_var.net.switches[0])

    def teardown_class(cls):
        Test_CreatePort.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.create_port_with_depth()
        self.test_var.create_port()
        self.test_var.create_same_port()
        self.test_var.verify_attribute_type()
        self.test_var.verify_attribute_range()
        self.test_var.verify_attribute_value()
        self.test_var.verify_missing_attribute()
        self.test_var.verify_unknown_attribute()
        self.test_var.verify_malformed_json()
        info("container_id_test %s\n" % self.container_id)
        swagger_model_verification(self.container_id, "/system/ports", "POST",
                                   PORT_DATA)
