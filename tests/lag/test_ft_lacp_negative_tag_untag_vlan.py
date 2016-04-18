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
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *

topoDict = {"topoExecution": 1000,
            "topoDevices": "dut01",
            "topoFilters": "dut01:system-category:switch"}


def getInterfaceVlan(deviceObj, interface):

    # Recover vlan information from running config from specific VLAN
    # Variables
    overallBuffer = []
    bufferString = ""
    command = ""
    returnCode = 0

    if deviceObj is None:
        LogOutput('error', "Need to pass switch deviceObj to this routine")
        returnCls = returnStruct(returnCode=1)
        return returnCls

    # Get into vtyshelll
    returnStructure = deviceObj.VtyshShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

    ##########################################################################
    # Send Command
    ##########################################################################
    command = "show running-config"
    LogOutput('info', "Show running config.*****" + command)
    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])

    if retCode != 0:
        LogOutput('error', "Failed to get information ." + command)

    ###########################################################################
    # Get out of the Shell
    ###########################################################################
    # Get out of vtyshell
    returnStructure = deviceObj.VtyshShell(enter=False)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=1, buffer=bufferString)
        return returnCls

    ###########################################################################
    # Exit for context and validet buffer with information
    ###########################################################################

    for curLine in overallBuffer:
        bufferString += str(curLine)

    listVlans = dict()
    listVlansResult = list()
    dataInterfaceLag = re.split(r'' + str(interface), bufferString)[1]
    listVlans = re.findall(r'\s{4}(vlan.*)', dataInterfaceLag, re.MULTILINE)

    for currentVlan in listVlans:
        vlanPointer = dict()
        vlanDist = re.match("vlan\s*(\w*)", currentVlan)
        if vlanDist.group(1) == "access":
            vlanTemp = re.match("vlan\s*(\w*)\s*(\d*)", currentVlan)
            vlanPointer['type'] = vlanTemp.group(1)
            vlanPointer['id'] = vlanTemp.group(2)
        else:
            vlanTemp = re.match("vlan\s*(\w*)\s*(\w*)\s*(\d*)", currentVlan)
            vlanPointer['type'] = vlanTemp.group(1)
            vlanPointer['mode'] = vlanTemp.group(2)
            vlanPointer['id'] = vlanTemp.group(3)

        listVlansResult.append(vlanPointer)
    return listVlansResult


class Test_FT_LAG_dynamic_Negative_Tag_Untag_Vlan:

    # Global Var
    dut01Obj = None
    lagId = None
    vlanAccessId = None
    vlanTrunkId = None
    listInterfaces = None

    def setup_class(cls):

        # Create Topology object and connect to devices
        Test_FT_LAG_dynamic_Negative_Tag_Untag_Vlan.testObj = testEnviron(
            topoDict=topoDict)
        Test_FT_LAG_dynamic_Negative_Tag_Untag_Vlan.topoObj = \
            Test_FT_LAG_dynamic_Negative_Tag_Untag_Vlan.testObj.topoObjGet()

        # Global definition
        global dut01Obj
        global lagId
        global vlanTrunkId
        global vlanAccessId
        global listInterfaces
        # Var Initiation

        dut01Obj = cls.topoObj.deviceObjGet(device="dut01")
        lagId = 100
        vlanTrunkId = 950
        vlanAccessId = 900
        listInterfaces = ["1", "2", "3", "4"]  # Any interface to join the Lag

    def teardown_class(cls):
        # Terminate all nodes
        Test_FT_LAG_dynamic_Negative_Tag_Untag_Vlan.topoObj.terminate_nodes()

    ##########################################################################
    # Step 1 - Create Lag
    ##########################################################################

    def test_create_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 1 - Create Lag ")
        LogOutput('info', "###############################################")

        devLagRetStruct = lagCreation(
            deviceObj=dut01Obj,
            lagId=lagId,
            configFlag=True)

        if devLagRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to created a lag interface ")
            assert(False)
        else:
            LogOutput('info', "Passed lag creation")

    ##########################################################################
    # Step 2 - Enable dynamic Lag
    ##########################################################################

    def test_enable_dynamic_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 2 - Enable dynamic Lag ")
        LogOutput('info', "###############################################")

        devLagDinRetStruct = lagMode(
            deviceObj=dut01Obj,
            lagId=lagId,
            lacpMode="active")

        if devLagDinRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable dynamic lag")
            assert(False)
        else:
            LogOutput('info', "Enable dynamic lag")

    ##########################################################################
    # Step 3 - Create vlans
    ##########################################################################

    def test_create_vlan(self):

        LogOutput('info', "\n################################################")
        LogOutput('info', "# Step 3 - Create vlans ")
        LogOutput('info', "################################################")

        listVlan = [vlanAccessId, vlanTrunkId]

        for currentVlan in listVlan:
            devVlanRetStruct1 = AddVlan(
                deviceObj=dut01Obj,
                vlanId=currentVlan,
                config=True
            )

            devVlanRetStruct2 = VlanStatus(
                deviceObj=dut01Obj,
                vlanId=currentVlan,
                status=True)

            if devVlanRetStruct1.returnCode() != 0 \
                    or devVlanRetStruct2.returnCode() != 0:
                LogOutput('error', "Failed to created Vlan ")
                assert(False)
            else:
                LogOutput('info', "Vlan created")

    ##########################################################################
    # Step 4 - Add ports to the Lag
    ##########################################################################

    def test_add_ports_lag(self):

        LogOutput('info', "\n################################################")
        LogOutput('info', "# Step 4 - Add ports to the Lag ")
        LogOutput('info', "################################################")

        for currentInterface in listInterfaces:
            devIntLagRetStruct = InterfaceLagIdConfig(
                deviceObj=dut01Obj,
                interface=currentInterface,
                lagId=lagId,
                enable=True)
            if devIntLagRetStruct.returnCode() != 0:
                LogOutput('error', "Failed to tag the ports")
                assert(False)
            else:
                LogOutput('info', "Port tagged")

    #######################################################################
    # Step 5 - Enable Interfaces
    ##########################################################################

    def test_enable_interface(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 5 - Enable Interfaces ")
        LogOutput('info', "###############################################")

        for currentInterface in listInterfaces:
            returnStruct = InterfaceEnable(deviceObj=dut01Obj,
                                           enable=True,
                                           interface=currentInterface)

            if returnStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable interfaces")
                assert(False)
            else:
                LogOutput('info', "Interface enabled")

    ##########################################################################
    # Step 6 - Enable vlan access in Lag
    ##########################################################################

    def test_enable_vlan_trunk_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 6  - Enable vlan trunk in lag ")
        LogOutput('info', "###############################################")

        lagInterface = "lag " + str(lagId)

        devAccVlanRetStruct = AddPortToVlan(
            deviceObj=dut01Obj,
            vlanId=vlanTrunkId,
            interface=lagInterface,
            allowed=True,
            config="access")

        if devAccVlanRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable vlan access in lag")
            assert(False)
        else:
            LogOutput('info', "Passed to enable vlan access in lag")

    ##########################################################################
    # Step 7 - Validated access vlan show in lag
    ##########################################################################

    def test_validated_trunk_vlan_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 7 - Validated access vlan show in Lag ")
        LogOutput('info', "###############################################")

        lagInterface = "interface lag " + str(lagId)

        devRetStruct = getInterfaceVlan(dut01Obj, lagInterface)

        if devRetStruct is None:
            LogOutput('error', "No vlans assigned to the Lag")
        else:
            for currentVlan in devRetStruct:
                if currentVlan['type'] == "access":
                    LogOutput(
                        'error', "The vlan was misconfigured in the device")
                    assert(False)

            LogOutput('Info', "Vlan was corrected configured")

    ##########################################################################
    # Step 8 - Validated access vlan show in lag
    ##########################################################################

    def test_enable_vlan_access_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 8 - Enable vlan access in lag ")
        LogOutput('info', "###############################################")

        lagInterface = "lag " + str(lagId)

        devAccVlanRetStruct = AddPortToVlan(
            deviceObj=dut01Obj,
            vlanId=vlanAccessId,
            interface=lagInterface,
            access=True,
            config="access")

        if devAccVlanRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable vlan access in lag")
            assert(False)
        else:
            LogOutput('info', "Passed to enable vlan access in lag")

    #######################################################################
    # Step 9 - Validated access vlan show in lag
    ##########################################################################

    def test_validated_access_vlan_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 9 - Validated access vlan show in Lag ")
        LogOutput('info', "###############################################")

        lagInterface = "interface lag " + str(lagId)

        devRetStruct = getInterfaceVlan(dut01Obj, lagInterface)

        if devRetStruct is None:
            LogOutput('error', "No vlans assigned to the Lag")
        else:
            for currentVlan in devRetStruct:
                if currentVlan['type'] == "trunk" or len(devRetStruct) > 1:
                    LogOutput(
                        'error', "The vlan was misconfigured in the device")
                    assert(False)

            LogOutput('Info', "Vlan was corrected configured")
