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
from copy import deepcopy

from opsvsiutils.restutils.utils import execute_request, login, \
    rest_sanity_check, get_switch_ip, create_test_port, \
    get_container_id, compare_dict, execute_port_operations, \
    PORT_DATA
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


class ModifyPortTest (OpsVsiTest):
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

    def modify_port_with_depth(self):
        info("\n########## Test to Validate Modify Port with depth "
             "##########\n")

        # 1 - Query port
        status_code, response_data = execute_request(
            self.PORT_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Port %s doesn't exists" % \
            self.PORT_PATH

        pre_put_get_data = {}
        try:
            pre_put_get_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"
        info("### Query Port %s  ###\n" % response_data)

        # 2 - Modify data
        put_data = pre_put_get_data["configuration"]
        put_data["ip4_address"] = "192.168.1.2"

        status_code, response_data = execute_request(
            self.PORT_PATH + "?depth=1", "PUT",
            json.dumps({'configuration':put_data}), self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "Unexpected status code. Received: %s Response data: %s " % \
            (status_code, response_data)
        info("### Port Not Modified. Status code is 400 BAD REQUEST  ###\n")

        info("\n########## End Test to Validate Modify Port ##########\n")

    def modify_port(self):
        info("\n########## Test to Validate Modify Port ##########\n")

        # 1 - Query port
        status_code, response_data = execute_request(
            self.PORT_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Port %s doesn't exists" % \
            self.PORT_PATH

        pre_put_get_data = {}
        try:
            pre_put_get_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"
        info("### Query Port %s  ###\n" % response_data)

        # 2 - Modify data
        put_data = pre_put_get_data["configuration"]
        put_data["interfaces"] = ["/rest/v1/system/interfaces/1",
                                  "/rest/v1/system/interfaces/2"]
        put_data["trunks"] = [400]
        put_data["ip4_address_secondary"] = ["192.168.0.2"]
        put_data["lacp"] = "passive"
        put_data["bond_mode"] = "l3-src-dst-hash"
        put_data["tag"] = 600
        put_data["vlan_mode"] = "access"
        put_data["ip6_address"] = "2001:0db8:85a3:0000:0000:8a2e:0370:8225"
        put_data["external_ids"] = {"extid2key": "extid2value"}
        put_data["mac"] = "01:23:45:63:90:ab"
        put_data["other_config"] = {"cfg-2key": "cfg2val"}
        put_data["bond_active_slave"] = "slave1"
        put_data["ip6_address_secondary"] = \
            ["2001:0db8:85a3:0000:0000:8a2e:0370:7224"]
        put_data["ip4_address"] = "192.168.1.2"

        status_code, response_data = execute_request(
            self.PORT_PATH, "PUT", json.dumps({'configuration':put_data}),
            self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Error modifying a Port. Status \
            code: %s Response data: %s " % (status_code, response_data)
        info("### Port Modified. Status code 200 OK  ###\n")

        # 3 - Verify Modified data
        status_code, response_data = execute_request(
            self.PORT_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Port %s doesn't exists" % \
            self.PORT_PATH
        post_put_data = {}
        try:
            post_put_get_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        post_put_data = post_put_get_data["configuration"]

        assert compare_dict(post_put_data, put_data), \
            "Configuration data is not equal that posted data"
        info("### Configuration data validated %s ###\n" % response_data)

        info("\n########## End Test to Validate Modify Port ##########\n")

    def verify_port_name_modification_not_applied(self):
        info("\n########## Test to Validate: Port name modification not \
            applied ##########\n")

        # 1 - Query port
        status_code, response_data = execute_request(
            self.PORT_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Port %s doesn't exists" \
            % self.PORT_PATH

        pre_put_get_data = {}
        try:
            pre_put_get_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"
        info("### Query Port %s  ###\n" % response_data)

        # 2 - Modify data
        put_data = pre_put_get_data["configuration"]
        expected_value = put_data["name"]
        put_data["name"] = "Port2"

        status_code, response_data = execute_request(
            self.PORT_PATH, "PUT", json.dumps({'configuration':put_data}),
            self.SWITCH_IP, xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Error modifying a Port. Status \
            code: %s Response data: %s " % (status_code, response_data)
        info("### Port Modified. Status code 200 OK  ###\n")

        # 3 - Verify Port name is not modified
        status_code, response_data = execute_request(
            self.PORT_PATH, "GET", None, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "Port %s doesn't exists" \
            % self.PORT_PATH
        post_put_get_data = {}
        try:
            post_put_get_data = json.loads(response_data)
        except:
            assert False, "Malformed JSON"

        post_put_data = post_put_get_data["configuration"]

        assert expected_value == post_put_data["name"], \
            "Port name was modified"
        info("### Configuration data validated %s ###\n" % response_data)

        info("\n########## End Test to Validate: Port name modification not \
            applied ##########\n")

    def verify_attribute_type(self):

        info("\n########## Test to verify attribute types ##########\n")

        info("\nAttempting to modify a port with incorrect types in \
            attributes\n")

        data = [("ip4_address", 192, httplib.BAD_REQUEST),
                ("ip4_address", "192.168.0.1", httplib.OK),
                ("tag", "675", httplib.BAD_REQUEST),
                ("tag", 675, httplib.OK),
                ("trunks", "654, 675", httplib.BAD_REQUEST),
                ("trunks", [654, 675], httplib.OK)]
        results = execute_port_operations(data, "PortTypeTest", "PUT",
                                          self.PATH, self.SWITCH_IP,
                                          self.cookie_header)

        assert results, "Unable to execute requests in verify_attribute_type"

        for attribute in results:
            assert attribute[1], "%s code issued " % attribute[2] + \
                "instead of %s for type " % attribute[3] + \
                "test in field '%s'" % attribute[0]
            info("%s code received as expected for field %s!\n" %
                 (attribute[2], attribute[0]))
            assert attribute[1], "{0} code issued instead of {2} for type \
                test in field '{1}'".format(attribute[2], attribute[0],
                                            attribute[3])
            info("{0} code received as expected for field {1}!\n".format
                 (attribute[2], attribute[0]))

        info("\n########## End test to verify attribute types ##########\n")

    def verify_attribute_range(self):

        info("\n########## Test to verify attribute ranges ##########\n")

        info("\nAttempting to modify a port with out of range values in \
            attributes\n")

        interfaces_out_of_range = []
        for i in range(1, 10):
            interfaces_out_of_range.append("/rest/v1/system/interfaces/%s" % i)

        data = [("ip4_address", "175.167.134.123/248", httplib.BAD_REQUEST),
                ("ip4_address", "175.167.134.123/24", httplib.OK),
                ("tag", 4095, httplib.BAD_REQUEST),
                ("tag", 675, httplib.OK),
                ("interfaces", interfaces_out_of_range, httplib.BAD_REQUEST),
                ("interfaces", ["/rest/v1/system/interfaces/1"], httplib.OK)]
        results = execute_port_operations(data, "PortRangesTest", "PUT",
                                          self.PATH, self.SWITCH_IP,
                                          self.cookie_header)

        assert results, "Unable to execute requests in verify_attribute_range"

        for attribute in results:
            assert attribute[1], "%s code issued " % attribute[2] + \
                "instead of %s for value " % attribute[3] + \
                "range test in field '%s'" % attribute[0]
            info("%s code received as expected for field %s!\n" %
                 (attribute[2], attribute[0]))

        info("\n########## End test to verify attribute ranges ##########\n")

    def verify_attribute_value(self):

        info("\n########## Test to verify attribute valid value ##########\n")

        info("\nAttempting to modify port with invalid value in attributes\n")

        data = [
            ("vlan_mode", "invalid_value", httplib.BAD_REQUEST),
            ("vlan_mode", "access", httplib.OK)
        ]
        results = execute_port_operations(data, "PortValidValueTest", "PUT",
                                          self.PATH, self.SWITCH_IP,
                                          self.cookie_header)

        assert results, "Unable to execute requests in verify_attribute_value"

        for attribute in results:
            assert attribute[1], "%s code issued " % attribute[2] + \
                "instead of %s for attribute valid " % attribute[3] + \
                "value test in field '%s'" % attribute[0]
            info("%s code received as expected for field %s!\n" %
                 (attribute[2], attribute[0]))

        info("\n########## End test to verify attribute valid value \
            ##########\n")

    def verify_unknown_attribute(self):

        info("\n########## Test to verify unkown attribute ##########\n")

        info("\nAttempting to modify a port with an unknown attribute\n")

        data = [
            ("unknown_attribute", "unknown_value", httplib.BAD_REQUEST),
            ("vlan_mode", "access", httplib.OK)
        ]
        results = execute_port_operations(data, "PortUnknownAttributeTest",
                                          "PUT", self.PATH, self.SWITCH_IP,
                                          self.cookie_header)

        assert results, \
            "Unable to execute requests in verify_unknown_attribute"

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

        # Delete reference_by from PUT
        del request_data['referenced_by']

        # Try to POST a port with a malformed JSON in request data

        info("\nAttempting to modify port with a malformed JSON in request \
            data\n")

        json_string = json.dumps(request_data)
        json_string += ","

        status_code, response_data = execute_request(
            self.PORT_PATH, "PUT", json_string, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, \
            "%s code issued instead of BAD_REQUEST for Port with malformed" + \
            " JSON in request data" % status_code

        # Try to POST a port with a correct JSON in request data

        info("\nAttempting to modify port with a correct JSON in request " +
             "data\n")

        json_string = json.dumps(request_data)

        status_code, response_data = execute_request(
            self.PORT_PATH, "PUT", json_string, self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, "%s code issued instead of OK " + \
            "for Port with correct JSON in request data" % status_code

        info("\n########## End test to verify malformed JSON ##########\n")


class Test_ModifyPort:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_ModifyPort.test_var = ModifyPortTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)
        # Add a test port
        info("\n########## Creating Test Port  ##########\n")
        status_code, response = create_test_port(cls.test_var.SWITCH_IP)
        assert status_code == httplib.CREATED, "Port not created."\
            "Response %s" % response
        info("### Test Port Created  ###\n")
        cls.container_id = get_container_id(cls.test_var.net.switches[0])

    def teardown_class(cls):
        Test_ModifyPort.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.modify_port_with_depth()
        self.test_var.modify_port()
        self.test_var.verify_port_name_modification_not_applied()
        # Verification Tests
        self.test_var.verify_attribute_type()
        self.test_var.verify_attribute_range()
        self.test_var.verify_attribute_value()
        self.test_var.verify_unknown_attribute()
        self.test_var.verify_malformed_json()
        info("container_id_test %s\n" % self.container_id)
        swagger_model_verification(self.container_id, "/system/ports/{id}",
                                   "PUT", PORT_DATA)
