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
###############################################################################
# Name:        DynamicLagModifyMaxNumberOfMembers.py
#
# Description: Tests that a previously configured dynamic Link Aggregation can
#              be modified to have between 7 and 8 members
#
# Author:      Jose Hernandez
#
# Topology:    |Switch| ---------------------- |Switch|
#                       (Dynamic LAG - 8 links)
#
# Success Criteria:  PASS -> LAGs are modified to support 7 or 8 members
#                            and pass traffic
#
#                    FAILED -> LAGs cannot be modified to 7 or 8 members or
#                              traffic cannot pass after any of these
#                              modifications
#
###############################################################################

from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *

topoDict = {"topoExecution": 3000,
            "topoType":"virtual",
            "topoDevices": "dut01 dut02",
            "topoLinks": "lnk01:dut01:dut02,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut01:dut02,\
                          lnk05:dut01:dut02,\
                          lnk06:dut01:dut02,\
                          lnk07:dut01:dut02,\
                          lnk08:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch"}

# Adds interfaces to LAG

def addInterfacesToLAG(deviceObj, lagId, intArray):
    overallBuffer = []
    returnStructure = deviceObj.VtyshShell(enter=True)
    overallBuffer.append(returnStructure.buffer())
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls

    # Get into config context
    returnStructure = deviceObj.ConfigVtyShell(enter=True)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to get vtysh config prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls

    # Add interfaces
    for i in intArray:
        command = "interface %s\r" % str(i)
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to configure interface " +
                      str(i) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput(
                'debug', "Entered interface " + str(i) + " on device " +
                deviceObj.device)

        command = "lag %s" % str(lagId)
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to add interface " + str(i) +
                      " to LAG" + str(lagId) + " on device " +
                      deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode,
                                     buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Added interface " + str(i) +
                      " to LAG" + str(lagId) + " on device " +
                      deviceObj.device)

        command = "exit"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to exit configuration of interface " +
                      str(i) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('debug', "Exited configuration of interface " +
                      str(i) + " on device " + deviceObj.device)

    # Get out of config context
    returnStructure = deviceObj.ConfigVtyShell(enter=False)
    returnCode = returnStructure.returnCode()
    overallBuffer.append(returnStructure.buffer())
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh config prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls
    # Exit vtysh
    returnStructure = deviceObj.VtyshShell(enter=False)
    overallBuffer.append(returnStructure.buffer())
    returnCode = returnStructure.returnCode()
    if returnCode != 0:
        LogOutput('error', "Failed to exit vtysh prompt")
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
        return returnCls
    bufferString = ""
    for curLine in overallBuffer:
        bufferString += str(curLine)
    returnCls = returnStruct(returnCode=returnCode, buffer=bufferString)
    return returnCls

# Enable/disable interface on DUT

def enableDutInterface(deviceObj, int, enable):
    if enable:
        retStruct = InterfaceEnable(
            deviceObj=deviceObj, enable=enable, interface=int)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to enable " + deviceObj.device +
                " interface " + int)
            return False
        else:
            LogOutput(
                'info', "Enabled " + deviceObj.device + " interface " + int)
    else:
        retStruct = InterfaceEnable(
            deviceObj=deviceObj, enable=enable, interface=int)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to disable " + deviceObj.device +
                " interface " + int)
            return False
        else:
            LogOutput(
                'info', "Disabled " + deviceObj.device + " interface " + int)
    return True

# Add/remove a single interface from a LAG

def addInterfaceToLAG(deviceObj, lagId, int, config, expectedIntArray):
    if config:
        LogOutput('info', "Adding interface " + str(int) +
                  " to LAG" + lagId + " on device " + deviceObj.device)
    else:
        LogOutput('info', "Removing interface " + str(int) +
                  " to LAG" + lagId + " on device " + deviceObj.device)
    returnStruct = InterfaceLagIdConfig(
        deviceObj=deviceObj, interface=int, lagId=lagId, enable=config)
    if returnStruct.returnCode() != 0:
        return False
    if config:
        LogOutput(
            'info', "Verifying if interface " + str(int) +
            " was added to LAG")
    else:
        LogOutput(
            'info', "Verifying if interface " + str(int) +
            " was removed from LAG")
    # verify if device is added/removed from LAG
    returnStruct = InterfaceLagShow(deviceObj=deviceObj, interface=int)
    if returnStruct.returnCode() != 0:
        LogOutput('info', "Unable to verify change in interface " + str(int))
        return False
    if config:
        helper = False
        for i in returnStruct.valueGet(key='localPort').keys():
            if i == 'lagId':
                helper = True
                break
        if not helper:
            LogOutput(
                'error', "The interface " + str(int) +
                " was verified to not be in a LAG")
            return False
        if returnStruct.valueGet(key='localPort')['lagId'] != str(lagId):
            LogOutput('error', "The interface " + str(int) +
                      " was verified to not be added to LAG " + str(lagId))
            return False
        else:
            LogOutput('info', "The interface " + str(int) +
                      " was verified to be added to LAG " + str(lagId))
    else:
        for i in returnStruct.valueGet(key='localPort').keys():
            if i == 'lagId':
                LogOutput('error', "The interface " + str(int) +
                          " was verified to still be in a LAG with ID: " +
                          returnStruct.valueGet(key='localPort')['lagId'])
                return False
        LogOutput('info', "The interface " + str(int) +
                  " was verified to not be in a LAG")
    returnStruct = lacpAggregatesShow(deviceObj=deviceObj, lagId=lagId)
    if returnStruct.returnCode() != 0:
        LogOutput('error', "Unable to verify integrity of resulting LAG")
        return False
    if len(returnStruct.valueGet(key=lagId)['interfaces']) !=\
            len(expectedIntArray):
        LogOutput(
            'error',
            "The resulting number of interfaces in LAG is different \
            than expected")
        return False
    for i in expectedIntArray:
        compareResult = False
        for k in returnStruct.valueGet(key=lagId)['interfaces']:
            if i == k:
                compareResult = True
                break
        if not compareResult:
            LogOutput(
                'error', 'Could not find interface ' + i + ' on resulting LAG')
            return False
    return True

# Create/delete a LAG and add interfaces

def createLAG(deviceObj, lagId, configure, intArray, mode):
    if configure:
        retStruct = lagCreation(
            deviceObj=deviceObj, lagId=str(lagId), configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to create LAG1 on " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Created LAG" + str(lagId) + " on " +
                deviceObj.device)
        retStruct = addInterfacesToLAG(deviceObj, 1, intArray)
        if retStruct.returnCode() != 0:
            return False
        if mode != 'off':
            retStruct = lagMode(
                lagId=str(lagId), deviceObj=deviceObj, lacpMode=mode)
            if retStruct.returnCode() != 0:
                return False
        retStruct = lacpAggregatesShow(deviceObj=deviceObj)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to verify if LAG was created on " +
                deviceObj.device)
            return False
        if len(retStruct.dataKeys()) == 0:
            print "----"
            print retStruct.buffer()
            print "----"
            LogOutput('error', "No LAGs were configured on device")
            return False
        if retStruct.valueGet(key=str(lagId)) is None:
            LogOutput('error', "Configured LAG is not present on device")
            return False
        if len(retStruct.valueGet(key=str(lagId))['interfaces']) !=\
                len(intArray):
            LogOutput('error', "The number of interfaces in the LAG (" +
                      len(retStruct.valueGet(key=str(lagId))['interfaces']) +
                      ") does not match the configured number of " +
                      len(intArray))
            return False
        if retStruct.valueGet(key=str(lagId))['lacpMode'] != mode:
            LogOutput('error', "The LAG have been configured in LACP mode " +
                      mode + " but instead it is in LACP mode " +
                      retStruct.valueGet(key=str(lagId))['lacpMode'])
            return False
    else:
        retStruct = lagCreation(
            deviceObj=deviceObj, lagId=str(lagId), configFlag=False)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to delete LAG1 on " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Deleted LAG" + str(lagId) + " on " + deviceObj.device)
        retStruct = lacpAggregatesShow(deviceObj=deviceObj)
        if len(retStruct.dataKeys()) != 0:
            if retStruct.valueGet(key=str(lagId)) is not None:
                LogOutput(
                    'error', "The LAG was not deleted from configuration")
                return False
    return True

class Test_ft_framework_basics:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_framework_basics.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_basics.topoObj =\
            Test_ft_framework_basics.testObj.topoObjGet()

    def teardown_class(cls):
       # Terminate all nodes
        Test_ft_framework_basics.topoObj.terminate_nodes()

    def test_createLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        assert(createLAG(dut01Obj, '1', True, [
            dut01Obj.linkPortMapping['lnk01'],
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03'],
            dut01Obj.linkPortMapping['lnk04'],
            dut01Obj.linkPortMapping['lnk05'],
            dut01Obj.linkPortMapping['lnk06'],
            dut01Obj.linkPortMapping['lnk07'],
            dut01Obj.linkPortMapping['lnk08']], 'active'))
        assert(createLAG(dut02Obj, '1', True, [
            dut02Obj.linkPortMapping['lnk01'],
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03'],
            dut02Obj.linkPortMapping['lnk04'],
            dut02Obj.linkPortMapping['lnk05'],
            dut02Obj.linkPortMapping['lnk06'],
            dut02Obj.linkPortMapping['lnk07'],
            dut02Obj.linkPortMapping['lnk08']], 'passive'))

    def test_enableDUTsInterfaces(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Enable switches interfaces")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "Configuring switch dut01")
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk04'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk05'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk06'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk07'],
                               True))
        assert(
            enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk08'],
                               True))

        LogOutput('info', "Configuring switch dut02")
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk01'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk05'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk06'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk07'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk08'],
                               True))

    def test_modifyLAGs1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Delete 1 member from LAG")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "Delete 1 LAG member from dut01")
        assert(
            addInterfaceToLAG(
                dut01Obj, '1', dut01Obj.linkPortMapping['lnk01'],
                False, [
                    dut01Obj.linkPortMapping['lnk02'],
                    dut01Obj.linkPortMapping['lnk03'],
                    dut01Obj.linkPortMapping['lnk04'],
                    dut01Obj.linkPortMapping['lnk05'],
                    dut01Obj.linkPortMapping['lnk06'],
                    dut01Obj.linkPortMapping['lnk07'],
                    dut01Obj.linkPortMapping['lnk08']]))
        LogOutput('info', "Delete 1 LAG member from dut02")
        assert(
            addInterfaceToLAG(
                dut02Obj, '1', dut02Obj.linkPortMapping['lnk01'],
                False, [
                    dut02Obj.linkPortMapping['lnk02'],
                    dut02Obj.linkPortMapping['lnk03'],
                    dut02Obj.linkPortMapping['lnk04'],
                    dut02Obj.linkPortMapping['lnk05'],
                    dut02Obj.linkPortMapping['lnk06'],
                    dut02Obj.linkPortMapping['lnk07'],
                    dut02Obj.linkPortMapping['lnk08']]))

    def test_modifyLAGs2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Add 1 member to LAG")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        LogOutput('info', "Add 1 LAG member to dut01")
        assert(
            addInterfaceToLAG(
                dut01Obj, '1', dut01Obj.linkPortMapping['lnk01'],
                True, [
                    dut01Obj.linkPortMapping['lnk01'],
                    dut01Obj.linkPortMapping['lnk02'],
                    dut01Obj.linkPortMapping['lnk03'],
                    dut01Obj.linkPortMapping['lnk04'],
                    dut01Obj.linkPortMapping['lnk05'],
                    dut01Obj.linkPortMapping['lnk06'],
                    dut01Obj.linkPortMapping['lnk07'],
                    dut01Obj.linkPortMapping['lnk08']]))
        LogOutput('info', "Add 1 LAG member to dut02")
        assert(
            addInterfaceToLAG(
                dut02Obj, '1', dut02Obj.linkPortMapping['lnk01'],
                True, [
                    dut02Obj.linkPortMapping['lnk01'],
                    dut02Obj.linkPortMapping['lnk02'],
                    dut02Obj.linkPortMapping['lnk03'],
                    dut02Obj.linkPortMapping['lnk04'],
                    dut02Obj.linkPortMapping['lnk05'],
                    dut02Obj.linkPortMapping['lnk06'],
                    dut02Obj.linkPortMapping['lnk07'],
                    dut02Obj.linkPortMapping['lnk08']]))
