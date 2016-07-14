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

DATA = {"configuration": {"name": "bridge_normal", "type": "internal",
                          "user_config":{"admin": "up"}}}


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QueryInterfacesId(OpsVsiTest):
    def setupNet(self):
        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sw=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.url = '/rest/v1/system/interfaces/bridge_normal'
        self.cookie_header = None

    def test_interfaces_id(self):
        status_code, response_data = execute_request(
            self.url, "PUT", json.dumps(DATA),
            self.SWITCH_IP, False, xtra_header=self.cookie_header)

        assert status_code == httplib.OK, ("Wrong status code %s " %
                                           status_code)
        info('### Success in executing the rest command "PUT" for url: ' +
             self.url + ' ###\n')
        info('### Success in Rest PUT Interfaces id ###\n')

        status_code, response_data = execute_request(
            self.url, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, ("Wrong status code %s " %
                                           status_code)
        d = get_json(response_data)
        assert d['configuration'] == DATA['configuration']

        info('### Success in executing the rest command "GET" for url: ' +
             self.url + ' ###\n')

        info('### Success in Rest GET Interfacesid ###\n')

        assert d['configuration']['name'] == 'bridge_normal', 'Failed in checking the \
            GET METHOD JSON response validation for Interface name'
        info('### Success in Rest GET system for Interface name ###\n')

        status_code, response_data = execute_request(
            self.url, "DELETE", json.dumps(DATA), self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.NO_CONTENT, ("Wrong status code %s " %
                                                   status_code)
        info('### Success in executing the rest command "DELETE" for url: ' +
             self.url + ' ###\n')

        info('### Success in executing the rest command \
        "DELETE for url=/rest/v1/system/interfaces/bridge_normal" ###\n')

        info('### Success in Rest DELETE Interfacesid ###\n')

        status_code, response_data = execute_request(
            self.url, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.NOT_FOUND, ("Wrong status code %s " %
                                                  status_code)

        info('### Success in executing the rest command" "GET" as not \
             expected for url: ' + self.url + ' ###\n')
        info('### Success in Rest Checking http code 404 for GET method \
             #once DELETED Interfacesid ###\n')


class Test_interfaces_id:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_interfaces_id.test_var = QueryInterfacesId()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_interfaces_id.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __def__(self):
        del self.test_var
    @pytest.mark.skipif(True, reason="disabling temporarily to enable custom validator change")
    def test_interfaces_id(self, netop_login):
        self.test_var.test_interfaces_id()
