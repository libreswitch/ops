# (C) Copyright 2015-2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import pytest

from opsvsi.docker import *
from opsvsi.opsvsitest import *
from opsvsiutils.restutils.utils import execute_request, get_switch_ip, \
    get_json, rest_sanity_check, login, get_server_crt, \
    remove_server_crt
import json
import httplib

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0

PUT_DATA = {
    "Interface": {
        "49": {
            "name": "49",
            "type": "system"
        }
    },
    "Port": {
        "p1": {
            "admin": ["up"],
            "name": "p1",
            "vlan_mode": ["trunk"],
            "trunks": [1]
        }
    },
    "System": {
        "asset_tag_number": "",
        "bridges": {
            "bridge_normal": {
                "datapath_type": "",
                "name": "bridge_normal",
                "ports": [
                    "p1"
                ]
            }
        },
        "hostname": "ops",
        "vrfs": {
            "vrf_default": {
                "name": "vrf_default"
            }
        }
    }
}


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QueryDcSchemaValidations(OpsVsiTest):
    def setupNet(self):
        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sw=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.put_url = "/rest/v1/system/full-configuration?type=running"

    def test_dc_valid_data(self):
        info("### Testing DC schema validations using VALID data ###\n")

        status_code, response_data = execute_request(
            self.put_url, "PUT", json.dumps(PUT_DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.OK, ("Wrong status code %s " %
                                           status_code)

        status_code, response_data = execute_request(
            self.put_url, "GET", None,
            self.SWITCH_IP, False, xtra_header=self.cookie_header)
        assert status_code == httplib.OK, ("Wrong status code %s " %
                                                status_code)

        d = get_json(response_data)
        info(d['Interface']['49'])
        assert d['Interface']['49'] == PUT_DATA['Interface']['49'], \
            'Failed in checking the GET METHOD JSON response validation for \
            Interface 49'
        assert d['Port']['p1'] == PUT_DATA['Port']['p1'], \
            'Failed in checking the GET METHOD JSON response validation for \
            Port p1'

        info("### Successfully executed PUT for url=%s ###\n" % self.put_url)
        info("### Received successful HTTP status code ###\n")

    def test_dc_invalid_data(self):
        info("### Testing DC schema validations using INVALID data ###\n")
        erroneous_fields = []

        info("### Removing mandatory field hostname from System ###\n")
        field = "hostname"
        del PUT_DATA["System"][field]
        erroneous_fields.append(field)

        info("### Setting an invalid port reference for bridge_normal ###\n")
        field = "ports"
        PUT_DATA["System"]["bridges"]["bridge_normal"][field] = ["p2"]
        erroneous_fields.append(field)

        info("### Changing the type of Interface name to an incorrect \
             type ###\n")
        field = "name"
        PUT_DATA["Interface"]["49"][field] = 1
        erroneous_fields.append(field)

        info("### Setting an out of range value for Port trunks ###\n")
        field = "trunks"
        PUT_DATA["Port"]["p1"][field] = [0]
        erroneous_fields.append(field)

        status_code, response_data = execute_request(
            self.put_url, "PUT", json.dumps(PUT_DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)
        assert status_code == httplib.BAD_REQUEST, ("Wrong status code %s " %
                                                    status_code)

        info("### Successfully executed PUT for url=%s ###\n" % self.put_url)
        info("### Received expected non-successful HTTP status code ###\n")
        info("### Verifying there was an error for each tampered field ###\n")

        d = get_json(response_data)

        assert len(d['error']) >= len(erroneous_fields), 'The number of \
                errors in the response does not match\n'

        info("### Received the expected number of errors ###\n")

@pytest.mark.skipif(True, reason="new DC module does not have this feature.")
class Test_dc_schema_validations:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_dc_schema_validations.test_var = QueryDcSchemaValidations()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_dc_schema_validations.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __def__(self):
        del self.test_var

    def test_valid_data(self, netop_login):
        self.test_var.test_dc_valid_data()

    def test_invalid_data(self, netop_login):
        self.test_var.test_dc_invalid_data()
