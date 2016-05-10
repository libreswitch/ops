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


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QueryTestInterfaces(OpsVsiTest):
    def setupNet(self):
        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sw=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.url = "/rest/v1/system/interfaces/"
        self.url_one = self.url + '19'
        self.url_two = self.url + '10'
        self.url_three = self.url + '49-2'
        self.cookie_header = None

    def test_interfaces(self):
        status_code, response_data = execute_request(
            self.url, "GET", None, self.SWITCH_IP, False,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK, ("Wrong status code %s " %
                                           status_code)

        info('### Success in executing the rest command "GET" for url: ' +
             self.url + ' ###\n')
        info('### Success in Rest GET interfaces ###\n')

        d = get_json(response_data)

        assert self.url_one in d, 'Failed in checking the GET METHOD \
            JSON response validation for Interface 19'
        info('### Success in Rest GET for Interface 19 ###\n')
        assert self.url_two in d, 'Failed in checking the GET METHOD \
            JSON response validation for Interface 10'
        info('### Success in Rest GET for Interface 10 ###\n')
        assert self.url_three in d, 'Failed in checking the GET METHOD \
            JSON response validation for Interface 49-2'
        info('### Success in Rest GET for Interface 49-2 ###\n')


class Test_interfaces:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_interfaces.test_var = QueryTestInterfaces()
        get_server_crt(cls.test_var.net.switches[0])
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_interfaces.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __def__(self):
        del self.test_var

    def test_interfaces(self, netop_login):
        self.test_var.test_interfaces()
