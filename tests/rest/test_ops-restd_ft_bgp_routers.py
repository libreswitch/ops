#!/usr/bin/env python
#
# Copyright (C) 2015 Hewlett Packard Enterprise Developmen
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "Lic
# not use this file except in compliance with the License.
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writin
# distributed under the License is distributed on an "AS I
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# License for the specific language governing permissions
# under the License.


import pytest

from opsvsi.docker import *
from opsvsi.opsvsitest import *

import json
import httplib
import urllib
import os
import sys
import time
import subprocess
import shutil

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class QueryBGPRoutersTest (OpsVsiTest):

    def setupNet(self):
        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sw=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)

    def verify_bgp_routers(self):

        _data_file = {"configuration": {"asn": 6004, "router_id": "10.10.0.4",
                      "redistribute": [], "deterministic_med": False,
                      "bgp_neighbors": [], "always_compare_med": False,
                      "other_config": {}, "networks": [],
                      "gr_stale_timer": 1, "timers": {},
                      "external_ids": {}, "maximum_paths": 1}}

        info('\n######### Test to validate GET, POST, PUT, and DELETE'
             ' for all BGP_Routers request ##########\n')

        src_path = os.path.dirname(os.path.realpath(__file__))
        src_file = os.path.join(src_path, 'json_bgp_routers.data')
        s1 = self.net.switches[0]
        ip_addr = s1.cmd("python -c \"import socket; print\
                socket.gethostbyname(socket.gethostname())\"")

        ip_addr = ip_addr.replace('\r\n', "")

        path_bgp = '/rest/v1/system/vrfs/vrf_default/bgp_routers'

        info("\n######### Testing GET without any entry #########\n")
        # GET without any entry
        path = '/rest/v1/system/vrfs/vrf_default/bgp_routers/6004'
        _headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("GET", path, json.dumps(""), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 404
        info('Successful')

        info("\n######### POST bgp router ########\n")
        # POST bgp_router
        _headers = {"Content-type": "application/x-form-urlencoded",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("POST", path_bgp, json.dumps(_data_file), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 201
        info('Successful')

        info("\n######## GET to check for POST data #########\n")
        # GET the bgp_router
        path = '/rest/v1/system/vrfs/vrf_default/bgp_routers/6004'
        _headers = {"Content-type": "application/json",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("GET", path, json.dumps(""), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 200

        d = json.loads(content)
        # GET returns all the fields except the asn,
        # so it needs to get removed.
        _data_file['configuration'].pop('asn', None)
        assert d['configuration'] == _data_file['configuration']
        info('Successful')
        # PUT for the bgp_router
        info('\n######### Testing PUT ########\n')
        _data_file['configuration']['networks'] = ["10.10.1.0/24"]
        _headers = {"Content-type": "application/json", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("PUT", path, json.dumps(_data_file), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 200
        info('Successful')
        # GET after doing PUT
        info('\n######## Testing GET after PUT operation ########\n')
        path = '/rest/v1/system/vrfs/vrf_default/bgp_routers/6004'
        _headers = {"Content-type": "application/json",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("GET", path, json.dumps(""), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 200

        d = json.loads(content)
        assert d['configuration'] == _data_file['configuration']
        info('Successful')
        # DELETE the bgp_router
        info('\n######### Testing DELETE #########\n')
        _headers = {"Content-type": "application/x-form-urlencoded",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("DELETE", path, json.dumps(""), _headers)
        response = conn.getresponse()
        assert response.status == 204
        info('Successful')
        # GET after deleting the bgp_router
        info('\n######## Testing GET after DELETE operation ########\n')
        path = '/rest/v1/system/vrfs/vrf_default/bgp_routers/6004'
        _headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("GET", path, json.dumps(""), _headers)
        response = conn.getresponse()
        assert response.status == 404
        info('Successful')

    def verify_bgp_neighbors(self):
        _data_file = {"configuration": {"asn": 6004, "router_id": "10.10.0.4",
                      "redistribute": [], "deterministic_med": False,
                      "bgp_neighbors": [], "always_compare_med": False,
                      "other_config": {}, "networks": [],
                      "gr_stale_timer": 1, "timers": {},
                      "external_ids": {}, "maximum_paths": 1}}

        info("\n######### Test to validate GET and POST for all" +
             "BGP_Neigbors request ##########\n")

        src_path = os.path.dirname(os.path.realpath(__file__))
        src_file = os.path.join(src_path, 'json_bgp_routers.data')
        s1 = self.net.switches[0]
        ip_addr = s1.cmd("python -c \"import socket; print\
                socket.gethostbyname(socket.gethostname())\"")

        ip_addr = ip_addr.replace('\r\n', "")

        path_bgp = '/rest/v1/system/vrfs/vrf_default/bgp_routers'

        info("\n######### POST bgp router ########\n")
        #POST bgp_router
        _headers = {"Content-type": "application/x-form-urlencoded",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("POST", path_bgp, json.dumps(_data_file), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 201
        info('Successful')

        _data_file_bgp_neighbor = {"configuration": {
            "ip_or_group_name": "172.17.0.3",
            "inbound_soft_reconfiguration": False,
            "passive": False, "bgp_peer_group": [], "allow_as_in": 1,
            "remote_as": 6008, "override_capability": False,
            "weight": 0, "is_peer_group": False, "other_config": {},
            "local_as": 6007, "advertisement_interval": 0, "timers": {},
            "shutdown": False, "route_maps": [], "external_ids": {},
            "strict_capability_match": False, "remove_private_as": False,
            "password": "", "maximum_prefix_limit": 1, "description": ""}}

        info("\n######### POST BGP_Neighbor ########\n")
        # POST bgp_neighbor
        path_bgp = ('/rest/v1/system/vrfs/vrf_default/'
                    'bgp_routers/6004/bgp_neighbors')
        _headers = {"Content-type": "application/json",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("POST", path_bgp,
                     json.dumps(_data_file_bgp_neighbor), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 201
        info("Successful")
        # GET after POST bgp_neighbor
        info('\n######## Testing GET after POST operation ########\n')
        path = ('/rest/v1/system/vrfs/vrf_default/'
                'bgp_routers/6004/bgp_neighbors/172.17.0.3')
        _headers = {"Content-type": "application/json",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("GET", path, json.dumps(""), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 200

        d = json.loads(content)
        # GET returns all the fields except ip_or_group_name,
        # so it needs to be removed
        _data_file_bgp_neighbor['configuration'].pop('ip_or_group_name', None)
        # capability is not suported now, so it can be removed
        d['configuration'].pop('capability', None)
        assert d['configuration'] == _data_file_bgp_neighbor['configuration']
        info('Successful')
        # PUT for bgp_neighbor
        info('\n######### Testing PUT ########\n')
        _data_file['configuration']['description'] = ["BGP_Neighbor"]
        _headers = {"Content-type": "application/json", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("PUT", path,
                     json.dumps(_data_file_bgp_neighbor), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 200
        info('Successful')
        # GET after PUT bgp_neighbor
        info('\n######## Testing GET after PUT operation ########\n')
        path = ('/rest/v1/system/vrfs/vrf_default/'
                'bgp_routers/6004/bgp_neighbors/172.17.0.3')
        _headers = {"Content-type": "application/json",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("GET", path, json.dumps(""), _headers)
        response = conn.getresponse()
        content = response.read()
        assert response.status == 200

        d = json.loads(content)
        _data_file_bgp_neighbor['configuration'].pop('ip_or_group_name', None)
        d['configuration'].pop('capability', None)
        assert d['configuration'] == _data_file_bgp_neighbor['configuration']
        info('Successful')
        # DELETE bgp_neighbor
        info('\n######### Testing DELETE #########\n')
        _headers = {"Content-type": "application/x-form-urlencoded",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("DELETE", path, json.dumps(""), _headers)
        response = conn.getresponse()
        assert response.status == 204
        info('Successful')
        # GET after deleting the bgp_nieghbor
        info('\n######## Testing GET after DELETE operation ########\n')
        _headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"}
        conn = httplib.HTTPConnection(ip_addr, 8091)
        conn.request("GET", path, json.dumps(""), _headers)
        response = conn.getresponse()
        assert response.status == 404
        info('Successful')


class Test_config:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_config.test_var = QueryBGPRoutersTest()

    def teardown_class(cls):
        Test_config.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __def__(self):
        del self.test_var

    def test_run(self):
        self.test_var.verify_bgp_routers()
        self.test_var.verify_bgp_neighbors()
