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

# The test case verifies that the schema validations are able to
# detect invalid data in the PUT request for declarative configuration.
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
put_url = "/rest/v1/system/full-configuration?type=running"

put_data = {
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

    retStruct = returnStruct(returnCode=0)
    return retStruct


def restTestDcValidData(wrkston01):
    info("### Testing DC schema validations using VALID data ###\n")
    retStruct = wrkston01.RestCmd(switch_ip=switchMgmtAddr,
                                  url=put_url,
                                  method="PUT",
                                  data=put_data)

    assert retStruct.returnCode() == 0, "Failed to PUT for url=%s" % post_url
    info("### Successfully executed PUT for url=%s ###\n" % put_url)

    assert retStruct.data['http_retcode'].find('200') != -1, \
           'PUT request failed.\n' + retStruct.data['response_body']
    info("### Received successful HTTP status code ###\n")

    retStruct = returnStruct(returnCode=0)
    return retStruct


def restTestDcInvalidData(wrkston01):
    info("### Testing DC schema validations using INVALID data ###\n")
    erroneous_fields = []

    info("### Removing mandatory field hostname from System ###\n")
    field = "hostname"
    del put_data["System"][field]
    erroneous_fields.append(field)

    info("### Setting an invalid port reference for bridge_normal ###\n")
    field = "ports"
    put_data["System"]["bridges"]["bridge_normal"][field] = ["p2"]
    erroneous_fields.append(field)

    info("### Changing the type of Interface name to an incorrect type ###\n")
    field = "name"
    put_data["Interface"]["49"][field] = 1
    erroneous_fields.append(field)

    info("### Setting an out of range value for Port trunks ###\n")
    field = "trunks"
    put_data["Port"]["p1"][field] = [0]
    erroneous_fields.append(field)

    retStruct = wrkston01.RestCmd(switch_ip=switchMgmtAddr,
                                  url=put_url,
                                  method="PUT",
                                  data=put_data)

    assert retStruct.returnCode() == 0, "Failed to PUT for url=%s" % put_url
    info("### Successfully executed PUT for url=%s ###\n" % put_url)

    assert retStruct.data['http_retcode'].find('400') != -1, \
           'Expecting an error response.\n' + retStruct.data['response_body']
    info("### Received expected non-successful HTTP status code ###\n")

    info("### Verifying there was an error for each tampered field ###\n")
    response_body = json.loads(retStruct.data["response_body"].strip())

    assert len(response_body["error"]) >= len(erroneous_fields), \
           'The number of errors in the response does not match\n'
    info("### Received the expected number of errors ###\n")

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

    @pytest.mark.skipif(True, reason="new DC module does not have this feature.")
    def test_restTestDcSchemaValidations(self):
        info('##################################################\n')
        info('######   Testing REST DC Schema Validations   ####\n')
        info('##################################################\n')
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")

        retStruct = restTestDcValidData(wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to test DC valid data'

        retStruct = restTestDcInvalidData(wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to test DC invalid data'

        info('### Successful in testing DC Schema Validations ###\n')

    def test_clean_up_devices(self):
        info('#######################################################\n')
        info('######    Device Cleanup - rolling back config     ####\n')
        info('#######################################################\n')
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        retStruct = deviceCleanup(dut01Obj, wrkston01Obj)
        assert retStruct.returnCode() == 0, 'Failed to cleanup device'
        info('### Successfully Cleaned up devices ###\n')
