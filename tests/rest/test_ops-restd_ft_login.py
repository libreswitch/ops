#!/usr/bin/env python
#
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
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
import urllib
from opsvsi.docker import *
from opsvsi.opsvsitest import *
from opsvsiutils.systemutil import *

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


class configTest (OpsVsiTest):
    def setupNet(self):

        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sws=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)

    def verify_login(self):

        s1 = self.net.switches[0]
        ip_addr = s1.cmd("python -c \"import socket;print\
                         socket.gethostbyname(socket.gethostname())\"")
        conn = httplib.HTTPConnection(ip_addr, 8091)
        url = '/login'

        # POST to fetch cookie
        print("\n######### Running POST to fetch the cookie ##########\n")
        body = {'username': 'root', 'password': ''}
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn.request('POST', url, urllib.urlencode(body), headers)
        response = conn.getresponse()
        print(response)

        headers = {'Cookie': response.getheader('set-cookie')}

        time.sleep(2)

        print ('''"\n######### Running GET to fetch the system
        info from the DB ##########\n"''')

        # GET to fetch system info from the DB
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request('GET', url, headers=headers)
        response = conn.getresponse()
        print(response)

        assert response.status == 200
        time.sleep(2)

        print ('''"\n######### Running GET to fetch the system info
                from the DB after removing the cookie ##########\n"''')

        headers = {'Cookie': response.getheader('set-cookie')}

        # GET to fetch system info from the DB
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request('GET', url, headers=headers)
        response = conn.getresponse()
        print(response)

        assert response.status == 401

    def verify_fail_login(self):
        s1 = self.net.switches[0]
        ip_addr = s1.cmd("python -c \"import socket;print\
                         socket.gethostbyname(socket.gethostname())\"")
        conn = httplib.HTTPConnection(ip_addr, 8091)
        url = '/login'

        # POST to fetch cookie
        print ('''"\n######### Running POST to fetch the cookie
                with wrong username and password #1 ##########\n"''')
        url = '/login'
        body = {'username': 'john', 'password': 'doe'}
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request('POST', url, urllib.urlencode(body), headers)
        response = conn.getresponse()
        print(response)

        headers = {'Cookie': response.getheader('set-cookie')}

        time.sleep(2)

        print ('''"\n######### Running GET to fetch the system info
               from the DB ##########\n"''')

        # GET to fetch system info from the DB
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request('GET', url, headers=headers)
        response = conn.getresponse()
        print(response)

        assert response.status == 401
        time.sleep(2)

        # POST to fetch cookie
        print ('''"\n######### Running POST to fetch the cookie with
                wrong username and password #2 ##########\n"''')
        url = '/login'
        body = {'username': 'error', 'password': ''}
        headers = {"Content-type": "application/x-www-form-rlencoded",
                   "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request('POST', url, urllib.urlencode(body), headers)
        response = conn.getresponse()
        print(response)

        headers = {'Cookie': response.getheader('set-cookie')}

        time.sleep(2)

        print ('''"\n######### Running GET to fetch the system info
                from the DB ##########\n"''')
        # GET to fetch system info from the DB
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request('GET', url, headers=headers)
        response = conn.getresponse()
        print(response)

        assert response.status == 401


class Test_config:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_config.test_var = configTest()

    def teardown_class(cls):
        Test_config.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self):
        self.test_var.verify_login()
        self.test_var.verify_fail_login()
