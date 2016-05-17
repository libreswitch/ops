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

BGP1_POST_DATA = {
    "configuration": {
        "always_compare_med": True,
        "asn": 6001
    }
}

BGP2_POST_DATA = {
    "configuration": {
        "always_compare_med": True,
        "asn": 6002
    }
}

DC_PUT_DATA = {
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
        "aaa": {
            "fallback": "false",
            "radius": "false"
        },
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

DC_INVALID_BGP_CONFIGS = {
    "bgp_routers": {
        "6001": {
            "always_compare_med": True
        },
        "6002": {
            "always_compare_med": True
        }
    },
    "name": "vrf_default"
}


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QueryCustomValidatorsTest(OpsVsiTest):
    def setupNet(self):
        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sw=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])

        self.post_url = "/rest/v1/system/vrfs/vrf_default/bgp_routers"
        self.delete_url = self.post_url + "/6001"
        self.dc_put_url = "/rest/v1/system/full-configuration?type=running"
        self.cookie_header = None

    def test_custom_validator_valid_post(self):

        info("### Testing valid POST request ###\n")
        info("### Creating the first BGP should be successful ###\n")

        status_code, response_data = execute_request(
            self.post_url, "POST", json.dumps(BGP1_POST_DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)
        assert status_code == httplib.CREATED, ("Wrong status code %s " %
                                                status_code)

        status_code, response_data = execute_request(
            self.post_url, "GET", None,
            self.SWITCH_IP, False, xtra_header=self.cookie_header)
        assert status_code == httplib.OK, ("Wrong status code %s " %
                                                status_code)
        assert self.post_url + '/6001' in response_data

        info("### Successfully executed POST for url=%s ###\n" % self.post_url)
        info("### Received successful HTTP status code ###\n")

    def test_custom_validator_invalid_post(self):
        info("### Testing invalid POST request ###\n")
        info("### Creating another BGP is not allowed ###\n")

        status_code, response_data = execute_request(
            self.post_url, "POST", json.dumps(BGP2_POST_DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, ("Wrong status code %s " %
                                                    status_code)

        assert 'exceeded' in response_data, ('Error does not contain \
                                             resources exceeded error')

        d = get_json(response_data)
        info(d['message']['details'] + "\n")
        info("### Successfully retrieved validation error message ###\n")

    def test_delete_bgp_router(self):
        info("### Cleanup by deleting BGP router ###\n")

        status_code, response_data = execute_request(
            self.delete_url, "DELETE", None,
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, ("Wrong status code %s " %
                                                   status_code)
        info("### Successfully executed DELETE for url=%s ###\n" %
             self.delete_url)

        status_code, response_data = execute_request(
            self.delete_url, "GET", None,
            self.SWITCH_IP, False, xtra_header=self.cookie_header)
        assert status_code == httplib.NOT_FOUND, ("Wrong status code %s " %
                                                status_code)

        info("### Received successful HTTP status code ###\n")

    def dc_test_custom_validator_valid_put(self):
        info("### Testing valid DC PUT request ###\n")

        status_code, response_data = execute_request(
            self.dc_put_url, "PUT", json.dumps(DC_PUT_DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.OK, ("Wrong status code %s " %
                                           status_code)
        info("### Successfully executed PUT for url=%s ###\n" %
             self.dc_put_url)

        status_code, response_data = execute_request(
            self.dc_put_url, "GET", None,
            self.SWITCH_IP, False, xtra_header=self.cookie_header)
        assert status_code == httplib.OK, ("Wrong status code %s " %
                                                status_code)
        d = get_json(response_data)
        assert d['Interface']['49'] == DC_PUT_DATA['Interface']['49'], \
            'Failed in checking the GET METHOD JSON response validation for \
            Interface 49'
        assert d['Port']['p1'] == DC_PUT_DATA['Port']['p1'], \
            'Failed in checking the GET METHOD JSON response validation for \
            Port p1'
        assert d['System']['aaa'] == DC_PUT_DATA['System']['aaa'], \
            'Failed in checking the GET METHOD JSON response validation for \
            System aaa'

        info("### Received successful HTTP status code ###\n")

    def dc_test_custom_validator_invalid_put(self):
        info("### Testing invalid PUT request ###\n")
        info("### Adding invalid number of BGP routers ###\n")
        DC_PUT_DATA["System"]["vrfs"]["vrf_default"] = DC_INVALID_BGP_CONFIGS

        status_code, response_data = execute_request(
            self.dc_put_url, "PUT", json.dumps(DC_PUT_DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, ("Wrong status code %s " %
                                                    status_code)

        assert 'exceeded' in response_data, ('Error does not contain \
                                             resources exceeded error')
        info("### Successfully executed PUT for url=%s ###\n" %
             self.dc_put_url)

        info("### Received expected non-successful HTTP status code ###\n")
        d = get_json(response_data)
        info(d['error'][1]['details'] + "\n")
        info("### Successfully retrieved validation error message ###\n")

dc_disable = pytest.mark.skipif(True, reason="new DC module does not have this feature.")
class Test_custom_validators:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_custom_validators.test_var = QueryCustomValidatorsTest()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_custom_validators.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __def__(self):
        del self.test_var

    def test_valid_post(self, netop_login):
        self.test_var.test_custom_validator_valid_post()

    def test_invalid_post(self, netop_login):
        self.test_var.test_custom_validator_invalid_post()

    def test_delete(self, netop_login):
        self.test_var.test_delete_bgp_router()
    @dc_disable
    def test_put_dc(self, netop_login):
        self.test_var.dc_test_custom_validator_valid_put()
    @dc_disable
    def test_invalid_put_dc(self, netop_login):
        self.var_test.dc_test_custom_validators_invalid_put()
