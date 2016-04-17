# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
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

from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

# Topology definition
topoDict = {"topoExecution": 120,
            "topoTarget": "dut01",
            "topoDevices": "dut01",
            "topoFilters": "dut01:system-category:switch"}


def check_show_version_detail_cli_ft(dut01):
    cmdOut = dut01.cmdVtysh(command="show version detail")
    assert 'ops-sysd' in cmdOut, "show version detail failed"
    return True

class TestShowVersionDetail:

    def setup_class(cls):
        # Create Topology object and connect to devices
        TestShowVersionDetail.testObj = testEnviron(
            topoDict=topoDict, defSwitchContext="vtyShell")
        TestShowVersionDetail.topoObj = \
            TestShowVersionDetail.testObj.topoObjGet()

    def teardown_class(cls):
        # Terminate all nodes
        TestShowVersionDetail.topoObj.terminate_nodes()

    def testShowVersionDetail(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        retValue = check_show_version_detail_cli_ft(dut01Obj)
        if(retValue):
            LogOutput('info', "Show version detail - passed")
        else:
            LogOutput('info', "Show version detail - failed")
