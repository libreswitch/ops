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

import pytest

from opsvsi.opsvsitest import *

from utils import *

def create_fake_port(path, switch_ip, fake_port_name):
    data =  """
            {
                "configuration": {
                    "name": "%s",
                    "interfaces": ["/rest/v1/system/interfaces/1"],
                    "trunks": [413],
                    "ip4_address_secondary": ["192.168.0.1"],
                    "lacp": ["active"],
                    "bond_mode": ["l2-src-dst-hash"],
                    "tag": 654,
                    "vlan_mode": "trunk",
                    "ip6_address": ["2001:0db8:85a3:0000:0000:8a2e:0370:7334"],
                    "external_ids": {"extid1key": "extid1value"},
                    "bond_options": {"key1": "value1"},
                    "mac": ["01:23:45:67:89:ab"],
                    "other_config": {"cfg-1key": "cfg1val"},
                    "bond_active_slave": "null",
                    "ip6_address_secondary": ["01:23:45:67:89:ab"],
                    "vlan_options": {"opt1key": "opt2val"},
                    "ip4_address": "192.168.0.1",
                    "admin": "up"
                },
                "referenced_by": [{"uri": "/rest/v1/system/bridges/bridge_normal"}]
            }
            """ % fake_port_name

    info("\n---------- Creating fake port (%s) ----------\n" % fake_port_name)
    info("Testing path: %s\nTesting data: %s\n" % (path, data))

    response_status, response_data = execute_request(path, "POST", data, switch_ip)

    assert response.status == httplib.OK, "Response status received: %s\n" % response_status
    info("Fake port \"%s\" created!\n" % fake_port_name)

    assert response_data is "", "Response data received: %s\n" % response_data
    info("Response data: %s)" % response_data)
    info("---------- Creating fake port (%s) DONE ----------\n" % fake_port_name)

def create_fake_vlan(path, switch_ip, bridge_name, fake_vlan_name):
    info("\n---------- Creating fake vlan (%s) ----------\n" % fake_vlan_name)

    data =  """
            {
                "configuration": {
                    "name": "%s",
                    "id": 1,
                    "description": "test vlan",
                    "admin": ["up"],
                    "other_config": {},
                    "external_ids": {}
                }
            }
            """ % fake_vlan_name

    info("Testing Path: %s\nTesting Data: %s\n" % (path, data))

    response_status, response_data = execute_request(path, "POST", data, switch_ip)

    assert response_status == httplib.CREATED, "Response status received: %s\n" % response_status
    info("Fake VLAN \"%s\" created!\n" % fake_vlan_name)

    assert response_data is "", "Response data received: %s\n" % response_data
    info("Response data received: %s\n" % response_data)
    info("---------- Creating fake vlan (%s) DONE ----------\n" % fake_vlan_name)

def create_fake_bridge(path, switch_ip, fake_bridge_name):
    info("\n---------- Creating fake bridge (%s) ----------\n" % fake_bridge_name)
    data =  """
            {
                "configuration": {
                    "name": "%s",
                    "ports": [],
                    "vlans": [],
                    "datapath_type": "",
                    "other_config": {
                        "hwaddr": "",
                        "mac-table-size": "16",
                        "mac-aging-time": "300"
                    },
                    "external_ids": {}
                 }
            }
            """ % fake_bridge_name

    info("Testing path: %s\nTesting data: %s\n" % (path, data))

    response_status, response_data = execute_request(path, "POST", data, switch_ip)

    assert response_status == httplib.CREATED, "Response status: %s\n" % response_status
    info("Bridge \"%s\" created!\n" % fake_bridge_name)

    assert response_data is "", "Response data received: %s\n" % response_data
    info("Response data received: %s\n" % response_data)
    info("---------- Creating fake bridge (%s) DONE ----------\n" % fake_bridge_name)
