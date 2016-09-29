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

DATA = {
    "configuration": {
        "bridges": ["/rest/v1/system/bridge_normal"],
        "lacp_config": {},
        "dns_servers": [],
        "logrotate_config": {},
        "hostname": "openswitch",
        "manager_options": [],
        "subsystems": ["/rest/v1/system/base"],
        "asset_tag_number": "",
        "ssl": [],
        "mgmt_intf": {
            "ip": "10.10.10.2",
            "subnet-mask": '24',
            "mode": "static",
            "name": "eth0",
            "default-gateway": ""},
        "radius_servers": [],
        "management_vrf": [],
        "other_config": {
            "enable-statistics": "true"},
        "daemons": [
            "/rest/v1/system/fan",
            "/rest/v1/system/power",
            "/rest/v1/system/sys",
            "/rest/v1/system/led",
            "/rest/v1/system/pm",
            "/rest/v1/system/temp"],
        "bufmon_config": {},
        "external_ids": {},
        "ecmp_config": {},
        "vrfs": ["/rest/v1/system/vrf"]}}
PUT_DATA = {
    "configuration": {
        "split_parent": ["/rest/v1/system/interfaces/1"],
        "name": "1",
        "other_config": {},
        "user_config": {},
        "split_children": [],
        "external_ids": {},
        "type": "integer",
        "options": {}}}


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QueryInvalidPut(OpsVsiTest):
    def setupNet(self):
        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sw=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.url_system = "/rest/v1/system/"
        self.url_interfaces = "/rest/v1/system/interfaces/1"

    def test_invalid_put_method(self):
        status_code, response_data = execute_request(
            self.url_system, "PUT", json.dumps(DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, ("Wrong status code %s " %
                                                    status_code)
        info('### PASSED in Execute rest command "PUT" as expected for: ' +
             'url: ' + self.url_system + '  ###\n')
        info('### Success in INVALID Rest PUT for system ###\n')

        status_code, response_data = execute_request(
            self.url_system, "PUT", json.dumps(PUT_DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.BAD_REQUEST, ("Wrong status code %s " %
                                                    status_code)

        info('### PASSED in Execute rest command "PUT" as expected for: ' +
             'url: ' + self.url_interfaces + '  ###\n')

        info('### Success in INVALID Rest PUT for Interfaces id ###\n')


class Test_invalid_put:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_invalid_put.test_var = QueryInvalidPut()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_invalid_put.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __def__(self):
        del self.test_var

    def test_invalid_put_method(self, netop_login):
        self.test_var.test_invalid_put_method()
