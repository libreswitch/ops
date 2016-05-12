# Copyright 2015-2016 Hewlett Packard Enterprise Development LP
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
    get_json, rest_sanity_check, login
import json
import httplib

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QuerySystem(OpsVsiTest):
    def setupNet(self):
        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sw=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.url = "/rest/v1/system"
        self.cookie_header = None
        self.DATA = {
            "configuration": {
                "bridges": ["/rest/v1/system/bridges/bridge_normal"],
                "aaa": {
                    "fallback": "true",
                    "radius": "false"},
                "hostname": "openswitch",
                "asset_tag_number": "",
                "mgmt_intf": {
                    "ip": self.SWITCH_IP,
                    "subnet_mask": '24',
                    "mode": "static",
                    "name": "eth0"},
                "other_config": {
                    "enable-statistics": "true"},
                "vrfs": ["/rest/v1/system/vrfs/vrf_default"]}}

    def test_system(self):
        status_code, response_data = execute_request(
            self.url, "PUT", json.dumps(self.DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)
        assert status_code == httplib.OK, ("Wrong status code %s " %
                                           status_code)

        info('### Success in executing the rest command "PUT" for url: ' +
             self.url + ' ###\n')
        info('### Success in Rest PUT system ###\n')

        status_code, response_data = execute_request(
            self.url, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)
        assert status_code == httplib.OK, ("Wrong status code %s " %
                                           status_code)
        d = get_json(response_data)

        info('### Success in executing the rest command "GET" for url: ' +
             self.url + ' ###\n')

        info('### Success in Rest GET system ###\n')

        assert d['configuration']['hostname'] == \
            self.DATA['configuration']['hostname'], 'Failed in checking '\
            'the GET  METHOD JSON response validation for hostname'

        assert d['configuration']['other_config']['enable-statistics'] == \
            self.DATA['configuration']['other_config']['enable-statistics'], \
            'Failed in checking the GET METHOD JSON response validation for ' \
            'enable-statistics'

        assert d['configuration']['mgmt_intf']['mode'] == \
            self.DATA['configuration']['mgmt_intf']['mode'], \
            'Failed in checking the GET METHOD JSON response validation ' \
            'for management interface mode'

        assert d['configuration']['mgmt_intf']['name'] == \
            self.DATA['configuration']['mgmt_intf']['name'], 'Failed ' \
            'in checking the GET METHOD JSON response validation for ' \
            'management interface name'


class Test_system:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_system.test_var = QuerySystem()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_system.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __def__(self):
        del self.test_var

    def test_system(self, netop_login):
        self.test_var.test_system()
