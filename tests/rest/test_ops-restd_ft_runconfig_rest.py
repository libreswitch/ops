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

import os
import sys
import time
import pytest
import subprocess
import shutil
import json
import httplib
from opsvsi.docker import *
from opsvsi.opsvsitest import *
from opsvsiutils.systemutil import *
from opsvsiutils.restutils.utils import execute_request, login, \
    rest_sanity_check, get_switch_ip, get_server_crt, \
    remove_server_crt

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):

        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


@pytest.fixture
def netop_login(request):
    request.cls.test_var.cookie_header = login(request.cls.test_var.SWITCH_IP)


class configTest(OpsVsiTest):
    def setupNet(self):

        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sws=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)
        self.cookie_header = None
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])

    def verify_startup_config(self):
        info('''"\n########## Verify startup config writes and reads the
             config to startup config db ##########\n"''')
        src_path = os.path.dirname(os.path.realpath(__file__))
        src_file = os.path.join(src_path, 'json.data')

        path = '/rest/v1/system' + '/full-configuration?type=startup'
        with open(src_file) as data_file:
                _data = json.loads(data_file.read())

        status_code, response_data = execute_request(
            path, "PUT", json.dumps(_data), self.SWITCH_IP,
            xtra_header=self.cookie_header)

        assert status_code == httplib.OK

        status_code, response_data = execute_request(
            path, "GET", None, self.SWITCH_IP, xtra_header=self.cookie_header)
        content = json.loads(response_data)

        assert status_code == httplib.OK

        assert ordered(content) == ordered(_data)

        info("\n### Startup config write & read were successful ###\n")


class Test_config:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_config.test_var = configTest()
        get_server_crt(cls.test_var.net.switches[0])

    def teardown_class(cls):
        Test_config.test_var.net.stop()
        remove_server_crt()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self, netop_login):
        self.test_var.verify_startup_config()
