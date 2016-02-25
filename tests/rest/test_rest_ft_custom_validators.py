# (C) Copyright 2015 Hewlett Packard Enterprise Development LP
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
import json
from opstestfw.switch.CLI import *
from opstestfw import *

# The test case verifies that the custom validation framework is able to
# invoke a BGP create custom validator upon a REST/DC request and return
# an error response upon an invalid request.
#
# The following topology is used:
#
# +----------------+         +----------------+
# |                |         |                |
# |                |         |                |
# |      Host      +---------+     Switch     |
# |                |         |                |
# |                |         |                |
# +----------------+         +----------------+

topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 wrkston01",
            "topoLinks": "lnk01:dut01:wrkston01",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston01:docker-image:host/freeradius-ubuntu",
            "topoLinkFilter": "lnk01:dut01:interface:eth0"}
switchMgmtAddr = "10.10.10.2"
restClientAddr = "10.10.10.3"
broadcast = "10.10.10.255"
netmask = "255.255.255.0"
subnetMaskBits = 24
post_url = "/rest/v1/system/vrfs/vrf_default/bgp_routers"
dc_put_url = "/rest/v1/system/full-configuration?type=running"

bgp1_post_data = {
    "configuration": {
        "always_compare_med": True,
        "asn": 6001
    }
}

bgp2_post_data = {
    "configuration": {
        "always_compare_med": True,
        "asn": 6002
    }
}

dc_put_data = {
    "Interface": {
        "49": {
            "name": "49",
            "type": "system"
        }
    },
    "Port": {
        "p1": {
            "admin": "up",
            "name": "p1",
            "vlan_mode": "trunk",
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

dc_invalid_bgp_configs = {
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


def switch_reboot(dut01):
    # Reboot switch
    info('###  Reboot switch  ###\n')
    dut01.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct


def config_rest_environment(dut01, wrkston01):
    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface="mgmt",
                                  addr=switchMgmtAddr,
                                  mask=subnetMaskBits,
                                  config=True)

    assert retStruct.returnCode() == 0, 'Failed to configure IP on switchport'
    info('### Successfully configured ip on switch port ###\n')

    cmdOut = dut01.cmdVtysh(command="show run")
    info('### Running config of the switch: ###\n' + cmdOut)

    info('### Configuring workstations ###\n')
    retStruct = wrkston01.NetworkConfig(
                                ipAddr=restClientAddr,
                                netMask=netmask,
                                broadcast=broadcast,
                                interface=wrkston01.linkPortMapping['lnk01'],
                                config=True)

    assert retStruct.returnCode() == 0, 'Failed to configure IP on workstation'
    info('### Successfully configured IP on the workstation ###\n')

    cmdOut = wrkston01.cmd("ifconfig " + wrkston01.linkPortMapping['lnk01'])
    info('### Ifconfig info for the workstation: ###\n' + cmdOut)

    retStruct = GetLinuxInterfaceIp(deviceObj=wrkston01)
    assert retStruct.returnCode() == 0, 'Failed to get interface ip on switch'
    info("### Successful in getting linux interface "
         "ip on the workstation ###\n")

    retStruct = returnStruct(returnCode=0)
    return retStruct


def deviceCleanup(dut01, wrkston01):
    retStruct = wrkston01.NetworkConfig(
                                ipAddr=restClientAddr,
                                netMask=netmask,
                                broadcast=broadcast,
                                interface=wrkston01.linkPortMapping['lnk01'],
                                config=False)

    assert retStruct.returnCode() == 0, 'Failed to clean on the workstation'
    info('### Successfully unconfigured ip on the workstation ###\n')

    cmdOut = wrkston01.cmd("ifconfig " + wrkston01.linkPortMapping['lnk01'])
    info('### Ifconfig info for the workstation: ###\n' + cmdOut)

    retStruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface="mgmt",
                                  addr=switchMgmtAddr,
                                  mask=subnetMaskBits,
                                  config=False)

    assert retStruct.returnCode() == 0, 'Failed to clean on dut01 port'
    info('### Unconfigured IP address on dut01 port ###\n')

    cmdOut = dut01.cmdVtysh(command="show run")
    info('### Running config of the switch: ###\n' + cmdOut)

    retStruct = returnStruct(returnCode=0)
    return retStruct


def restTestCustomValidatorValidPost(wrkston01):
    info("### Testing valid POST request ###\n")
    info("### Creating the first BGP should be successful ###\n")
    retStruct = wrkston01.RestCmd(switch_ip=switchMgmtAddr,
                                  url=post_url,
                                  method="POST",
                                  data=bgp1_post_data)

    assert retStruct.returnCode() == 0, "Failed to POST for url=%s" % post_url
    info("### Successfully executed POST for url=%s ###\n" % post_url)

    assert retStruct.data['http_retcode'].find('201') != -1, \
        'REST POST failed.\n' + retStruct.data['response_body']
    info("### Received successful HTTP status code ###\n")

    retStruct = returnStruct(returnCode=0)
    return retStruct


def restTestCustomValidatorInvalidPost(wrkston01):
    info("### Testing invalid POST request ###\n")
    info("### Creating another BGP is not allowed ###\n")
    retStruct = wrkston01.RestCmd(switch_ip=switchMgmtAddr,
                                  url=post_url,
                                  method="POST",
                                  data=bgp2_post_data)

    assert retStruct.returnCode() == 0, "Failed to POST for url=%s" % post_url
    info("### Successfully executed POST for url=%s ###\n" % post_url)

    assert retStruct.data['http_retcode'].find('201') == -1, \
        'REST POST unexpectedly passed.\n' + retStruct.data['response_body']
    info("### Received expected non-successful HTTP status code ###\n")

    assert "exceeded" in retStruct.data["response_body"], \
        'Error does not contain resources exceeded error\n'
    info("### Successfully retrieved validation error message ###\n")

    retStruct = returnStruct(returnCode=0)
    return retStruct


def restDeleteBgpRouter(wrkston01):
    delete_url = post_url + "/6001"
    info("### Cleanup by deleting BGP router ###\n")
    retStruct = wrkston01.RestCmd(switch_ip=switchMgmtAddr,
                                  url=delete_url,
                                  method="DELETE")

    assert retStruct.returnCode() == 0, \
        "Failed to DELETE for url=%s" % delete_url
    info("### Successfully executed DELETE for url=%s ###\n" % delete_url)

    assert retStruct.data['http_retcode'].find('204') != -1, \
        'REST DELETE failed.\n' + retStruct.data['response_body']
    info("### Received successful HTTP status code ###\n")

    retStruct = returnStruct(returnCode=0)
    return retStruct


def dcTestCustomValidatorValidPut(wrkston01):
    info("### Testing valid DC PUT request ###\n")
    retStruct = wrkston01.RestCmd(switch_ip=switchMgmtAddr,
                                  url=dc_put_url,
                                  method="PUT",
                                  data=dc_put_data)

    assert retStruct.returnCode() == 0, "Failed to PUT for url=%s" % dc_put_url
    info("### Successfully executed PUT for url=%s ###\n" % dc_put_url)

    assert retStruct.data['http_retcode'].find('200') != -1, \
        'REST PUT passed.\n' + retStruct.data['response_body']
    info("### Received successful HTTP status code ###\n")

    retStruct = returnStruct(returnCode=0)
    return retStruct


def dcTestCustomValidatorInvalidPut(wrkston01):
    info("### Testing invalid PUT request ###\n")
    info("### Adding invalid number of BGP routers ###\n")
    dc_put_data["System"]["vrfs"]["vrf_default"] = dc_invalid_bgp_configs

    retStruct = wrkston01.RestCmd(switch_ip=switchMgmtAddr,
                                  url=dc_put_url,
                                  method="PUT",
                                  data=dc_put_data)

    assert retStruct.returnCode() == 0, "Failed to PUT for url=%s" % dc_put_url
    info("### Successfully executed PUT for url=%s ###\n" % dc_put_url)

    assert retStruct.data['http_retcode'].find('200') == -1, \
        'REST PUT unexpectedly passed.\n' + retStruct.data['response_body']
    info("### Received expected non-successful HTTP status code ###\n")

    response_body = json.loads(retStruct.data["response_body"])
    response_error = response_body["error"][0]

    assert "exceeded" in retStruct.data["response_body"], \
        'Error does not contain resources exceeded error\n'
    info("### Successfully retrieved validation error message ###\n")

    retStruct = returnStruct(returnCode=0)
    return retStruct


class Test_ft_framework_rest:
    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_framework_rest.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_rest.topoObj = \
            Test_ft_framework_rest.testObj.topoObjGet()
        wrkston01Obj = Test_ft_framework_rest.topoObj.deviceObjGet(
            device="wrkston01")
        wrkston01Obj.CreateRestEnviron()

    def teardown_class(cls):
        # Terminate all nodes
        Test_ft_framework_rest.topoObj.terminate_nodes()

    def test_reboot_switch(self):
        info('########################################################\n')
        info('############       Reboot the switch          ##########\n')
        info('########################################################\n')
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        retStruct = switch_reboot(dut01Obj)
        assert retStruct.returnCode() == 0, 'Failed to reboot Switch'
        info('### Successful in Switch Reboot piece ###\n')

    def test_config_rest_environment(self):
        info('#######################################################\n')
        info('######        Configure REST environment           ####\n')
        info('#######################################################\n')
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retStruct = config_rest_environment(dut01Obj, wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to config REST environment'
        info('### Successful in config REST environment test ###\n')

    def test_restTestCustomValidators(self):
        info('########################################################\n')
        info('######   Testing REST Custom Validators Framework   ####\n')
        info('########################################################\n')
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")

        retStruct = restTestCustomValidatorValidPost(wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to test REST valid post'

        retStruct = restTestCustomValidatorInvalidPost(wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to test REST invalid post'

        retStruct = restDeleteBgpRouter(wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to delete BGP resource'

        info('### Successful in testing REST custom validators ###\n')

    def test_declarativeConfigTestCustomValidators(self):
        info('########################################################\n')
        info('######   Testing DC Custom Validators Framework   ######\n')
        info('########################################################\n')
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")

        retStruct = dcTestCustomValidatorValidPut(wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to test DC valid post'

        retStruct = dcTestCustomValidatorInvalidPut(wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to test DC invalid post'

        info('### Successful in testing DC custom validators ###\n')

    def test_clean_up_devices(self):
        info('#######################################################\n')
        info('######    Device Cleanup - rolling back config     ####\n')
        info('#######################################################\n')
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retStruct = deviceCleanup(dut01Obj, wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to cleanup device'
        info('### Successfully Cleaned up devices ###\n')
