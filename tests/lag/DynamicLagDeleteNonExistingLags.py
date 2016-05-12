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
###############################################################################
# Name:        DynamicLagDeleteNonExistingLags.py
#
# Description: Tests that a previously configured dynamic Link Aggregation does
#              not stop forwarding traffic when attempting to delete several
#              non-existent Link Aggregations with different names that may not
#              be supported
#
# Author:      Jose Hernandez
#
# Topology:  |Host| ----- |Switch| ---------------------- |Switch| ----- |Host|
#                                   (Dynamic LAG - 2 links)
#
# Success Criteria:  PASS -> Non-existent LAGs cannot be deleted and they
#                            don't affect the functioning LAG
#
#                    FAILED -> Functioning LAG configuration is changed or any
#                              of the non-existing LAGs don't produce errors
#                              when attempting to delete them
#
###############################################################################


import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *

topoDict = {"topoExecution": 3000,
            "topoDevices": "dut01 dut02 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:dut02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut02:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}

# Reboots switch


def switch_reboot(deviceObj):
    # Reboot switch
    LogOutput('info', "Reboot switch " + deviceObj.device)
    deviceObj.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct

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

# Enable/disable routing on interfaces so VLANs can be configured


def enableInterfaceRouting(deviceObj, int, enable):
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
    # enter interface
    command = "interface %s\r" % str(int)
    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])
    if retCode != 0:
        LogOutput('error', "Failed to configure interface " +
                  str(int) + " on device " + deviceObj.device)
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
        return returnCls
    else:
        LogOutput('debug', "Entered interface " +
                  str(int) + " on device " + deviceObj.device)
    if enable:
        # configure interface
        command = "routing"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to enable routing on interface " +
                      str(int) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Enabledrouting on interface " +
                      str(int) + " on device " + deviceObj.device)
    else:
        # configure interface
        command = "no routing"
        returnDevInt = deviceObj.DeviceInteract(command=command)
        retCode = returnDevInt['returnCode']
        overallBuffer.append(returnDevInt['buffer'])
        if retCode != 0:
            LogOutput('error', "Failed to disable routing on interface " +
                      str(int) + " on device " + deviceObj.device)
            bufferString = ""
            for curLine in overallBuffer:
                bufferString += str(curLine)
            returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
            return returnCls
        else:
            LogOutput('info', "Disabled routing on interface " +
                      str(int) + " on device " + deviceObj.device)
        # exit
    command = "exit"
    returnDevInt = deviceObj.DeviceInteract(command=command)
    retCode = returnDevInt['returnCode']
    overallBuffer.append(returnDevInt['buffer'])
    if retCode != 0:
        LogOutput('error', "Failed to exit configure interface " +
                  str(int) + " on device " + deviceObj.device)
        bufferString = ""
        for curLine in overallBuffer:
            bufferString += str(curLine)
        returnCls = returnStruct(returnCode=retCode, buffer=bufferString)
        return returnCls
    else:
        LogOutput('debug', "Exited configure interface " +
                  str(int) + " on device " + deviceObj.device)
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
    # Get out of vtysh
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
    # Return
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

# Function to try and delete a non-existent LAG. It assumes there is only
# 1 other LAG and then matches the information present in DUT to verify it
# wasn't modified


def deleteLAGNegative(
        deviceObj, lagId, goodLagId, goodLagMode, goodLagInterfaces,
        goodLagHash, goodLagFallback, goodLagFastFlag):
    retStruct = lagCreation(
        deviceObj=deviceObj, lagId=str(lagId), configFlag=False)
    if retStruct.returnCode() != 0:
        LogOutput('info', "Failed to delete LAG " + str(lagId) +
                  " as expected on " + deviceObj.device)
    else:
        LogOutput('error', "Deleted LAG " + str(lagId) +
                  " unexpectedly on " + deviceObj.device)
        return False
    retStruct = lacpAggregatesShow(deviceObj=deviceObj)
    if retStruct.returnCode() != 0:
        LogOutput('error', "Failed to verify if deleting LAG" +
                  str(lagId) + " procuded changes on device " +
                  deviceObj.device)
        return False
    if len(retStruct.dataKeys()) != 1:
        for i in retStruct.dataKeys():
            helperText += "\n" + i
        LogOutput(
            'error',
            "Expected to find only 1 LAG in configuration, found " +
            str(len(retStruct.dataKeys())) + " with the following IDs:\n" +
            helperText)
        return False
    if retStruct.dataKeys()[0] == lagId:
        LogOutput('error', "Found deleted LAG ID on device " +
                  deviceObj.device + " configuration")
        return False
    if retStruct.valueGet(key=goodLagId)['lacpMode'] != goodLagMode:
        LogOutput(
            'error',
            "Remaining LAG LACP mode altered. Expected: " + str(goodLagMode) +
            " - Found: " + str(retStruct.valueGet(key=goodLagId)['lacpMode']))
        return False
    if retStruct.valueGet(key=goodLagId)['hashType'] != goodLagHash:
        LogOutput(
            'error',
            "Remaining LAG hashing algorithm altered. Expected: " +
            str(goodLagHash) + " - Found: " +
            str(retStruct.valueGet(key=goodLagId)['hashType']))
        return False
    if retStruct.valueGet(key=goodLagId)['fallbackFlag'] != goodLagFallback:
        LogOutput(
            'error',
            "Remaining LAG fallback flag altered. Expected: " +
            str(goodLagFallback) + " - Found: " +
            str(retStruct.valueGet(key=goodLagId)['fallbackFlag']))
        return False
    if retStruct.valueGet(key=goodLagId)['lacpFastFlag'] != goodLagFastFlag:
        LogOutput(
            'error',
            "Remaining LAG fast speed setting altered. Expected: " +
            str(goodLagFastFlag) + " - Found: " +
            str(retStruct.valueGet(key=goodLagId)['lacpFastFlag']))
        return False
    if len(retStruct.valueGet(key=goodLagId)['interfaces']) !=\
            len(goodLagInterfaces):
        helperText1 = ''
        helperText2 = ''
        for i in retStruct.valueGet(key=goodLagId)['interfaces']:
            helperText1 += "\n" + i
        for i in goodLagInterfaces:
            helperText2 += "\n" + i
        LogOutput(
            'error',
            "Number of links in remaining LAG was modified. Expected: " +
            str(len(goodLagInterfaces)) + " with interfaces:\n" +
            helperText2 + "\n Found: " +
            str(len(retStruct.valueGet(key=goodLagId)['interfaces'])) +
            " with interfaces: \n" + helperText1)
        return False
    for i in goodLagInterfaces:
        found = False
        for k in retStruct.valueGet(key=goodLagId)['interfaces']:
            if i == k:
                found = True
                break
        if not found:
            LogOutput(
                'error', "Could not find interface " + i + "in remaining LAG")
            return False
    return True

# Add VLAN to interface


def addInterfaceVLAN(deviceObj, vlanId, enable, int):
    if enable:
        retStruct = enableInterfaceRouting(deviceObj, int, False)
        if retStruct.returnCode() != 0:
            return False
        retStruct = AddPortToVlan(
            deviceObj=deviceObj, vlanId=vlanId, interface=int, access=True)
        LogOutput('info', "Added VLAN " + str(vlanId) + " to interface " +
                  int)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to add VLAN " + str(vlanId) +
                " to interface " + int)
            return False
    else:
        retStruct = AddPortToVlan(
            deviceObj=deviceObj, vlanId=vlanId, interface=int, config=False,
            access=True)
        LogOutput(
            'info', "Delete VLAN " + str(vlanId) + " to interface " + int)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to delete VLAN " + str(vlanId) +
                " to interface " + int)
            return False
        retStruct = enableInterfaceRouting(deviceObj, int, True)
        if retStruct.returnCode() != 0:
            return False
    return True

# Configure/delete VLAN on switch


def configureVLAN(deviceObj, vlanId, enable):
    if enable:
        LogOutput('debug', "Configuring VLAN " + str(vlanId) +
                  " on device " + deviceObj.device)
        retStruct = AddVlan(deviceObj=deviceObj, vlanId=vlanId)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to create VLAN " +
                      str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Created VLAN " + str(vlanId) + " on device " +
                deviceObj.device)
        retStruct = VlanStatus(deviceObj=deviceObj, vlanId=vlanId,
                               status=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to enable VLAN " +
                      str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Enabled VLAN " + str(vlanId) + " on device " +
                deviceObj.device)
    else:
        LogOutput('debug', "Deleting VLAN " + str(vlanId) +
                  " on device " + deviceObj.device)
        retStruct = AddVlan(deviceObj=deviceObj, vlanId=vlanId,
                            config=False)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to delete VLAN " +
                      str(vlanId) + " on device " + deviceObj.device)
            return False
        else:
            LogOutput(
                'info', "Deleted VLAN " + str(vlanId) + " on device " +
                deviceObj.device)
    return True

# Configure/unconfigure the IP address of a workstation


def configureWorkstation(deviceObj, int, ipAddr, netMask, broadcast, enable):
    if enable:
        retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                            netMask=netMask,
                                            broadcast=broadcast,
                                            interface=int, configFlag=True)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to configure IP on workstation " +
                deviceObj.device)
            return False
        cmdOut = deviceObj.cmd("ifconfig " + int)
        LogOutput('info', "Ifconfig info for workstation " +
                  deviceObj.device + ":\n" + cmdOut)
    else:
        retStruct = deviceObj.NetworkConfig(ipAddr=ipAddr,
                                            netMask=netMask,
                                            broadcast=broadcast,
                                            interface=int, configFlag=False)
        if retStruct.returnCode() != 0:
            LogOutput(
                'error', "Failed to unconfigure IP on workstation " +
                deviceObj.device)
            return False
        cmdOut = deviceObj.cmd("ifconfig " + int)
        LogOutput('info', "Ifconfig info for workstation " +
                  deviceObj.device + ":\n" + cmdOut)
    return True

# Ping between workstation


def pingBetweenWorkstations(deviceObj1, deviceObj2, ipAddr, success):
    LogOutput('info', "Pinging between workstation " +
              deviceObj1.device + " and workstation " + deviceObj2.device)
    if success:
        retStruct = deviceObj1.Ping(ipAddr=ipAddr)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to ping from workstation " +
                      deviceObj1.device + ":\n" +
                      str(retStruct.retValueString()))
            return False
        else:
            LogOutput('info', "IPv4 Ping from workstation 1 to workstation 2 \
            return JSON:\n" +
                      str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('info', "Packets Sent:\t" + str(packets_sent))
            LogOutput('info', "Packets Recv:\t" + str(packets_received))
            LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
            LogOutput('info', "Passed ping test between workstation " +
                      deviceObj1.device + " and workstation " +
                      deviceObj2.device)
    else:
        retStruct = deviceObj1.Ping(ipAddr=ipAddr)
        if retStruct.returnCode() != 0:
            LogOutput(
                'debug', "Failed to ping workstation2 as expected:\n" +
                str(retStruct.retValueString()))
            LogOutput('info',
                      "Passed negative ping test between workstation " +
                      deviceObj1.device + " and workstation " +
                      deviceObj2.device)
        else:
            LogOutput('error', "IPv4 Ping from workstation 1 to workstation \
            2 return JSON:\n" +
                      str(retStruct.retValueString()))
            packet_loss = retStruct.valueGet(key='packet_loss')
            packets_sent = retStruct.valueGet(key='packets_transmitted')
            packets_received = retStruct.valueGet(key='packets_received')
            LogOutput('error', "Packets Sent:\t" + str(packets_sent))
            LogOutput('error', "Packets Recv:\t" + str(packets_received))
            LogOutput('error', "Packet Loss %:\t" + str(packet_loss))
            return False
    return True

# Clean up devices


def clean_up_devices(dut01Obj, dut02Obj, wrkston01Obj, wrkston02Obj):
    LogOutput('info', "\n############################################")
    LogOutput('info', "Device Cleanup - rolling back config")
    LogOutput('info', "############################################")
    finalResult = []

    LogOutput('info', "Unconfigure workstations")
    LogOutput('info', "Unconfiguring workstation 1")
    finalResult.append(configureWorkstation(
        wrkston01Obj, wrkston01Obj.linkPortMapping['lnk01'],
        "140.1.1.10", "255.255.255.0", "140.1.1.255", False))
    LogOutput('info', "Unconfiguring workstation 2")
    finalResult.append(configureWorkstation(
        wrkston02Obj, wrkston02Obj.linkPortMapping['lnk04'],
        "140.1.1.11", "255.255.255.0", "140.1.1.255", False))

    LogOutput('info', "Delete LAGs on DUTs")
    finalResult.append(createLAG(dut01Obj, '1', False, [], 'off'))
    finalResult.append(createLAG(dut02Obj, '1', False, [], 'off'))

    LogOutput('info', "Disable interfaces on DUTs")
    LogOutput('info', "Configuring switch dut01")
    finalResult.append(
        enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk01'],
                           False))
    finalResult.append(
        enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk02'],
                           False))
    finalResult.append(
        enableDutInterface(dut01Obj, dut01Obj.linkPortMapping['lnk03'],
                           False))

    LogOutput('info', "Configuring switch dut02")
    finalResult.append(
        enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                           False))
    finalResult.append(
        enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                           False))
    finalResult.append(
        enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
                           False))

    LogOutput('info', "Remove VLAN from DUTs")
    finalResult.append(configureVLAN(dut01Obj, 900, False))
    finalResult.append(configureVLAN(dut02Obj, 900, False))

    for i in finalResult:
        if not i:
            LogOutput('error', "Errors were detected while cleaning \
                    devices")
            return
    LogOutput('info', "Cleaned up devices")


class Test_ft_framework_basics:

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_ft_framework_basics.testObj = testEnviron(topoDict=topoDict)
        Test_ft_framework_basics.topoObj =\
            Test_ft_framework_basics.testObj.topoObjGet()

    def teardown_class(cls):
        # clean up devices
        clean_up_devices(
            cls.topoObj.deviceObjGet(device="dut01"),
            cls.topoObj.deviceObjGet(device="dut02"),
            cls.topoObj.deviceObjGet(device="wrkston01"),
            cls.topoObj.deviceObjGet(device="wrkston02"))
        # Terminate all nodes
        Test_ft_framework_basics.topoObj.terminate_nodes()

    def test_reboot_switch(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Reboot the switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        devRebootRetStruct = switch_reboot(dut01Obj)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch 1")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 1 Reboot piece")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        devRebootRetStruct = switch_reboot(dut02Obj)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch 2")
            assert(devRebootRetStruct.returnCode() == 0)
        else:
            LogOutput('info', "Passed Switch 2 Reboot piece")

    def test_createLAGs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Create LAGs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")

        assert(createLAG(dut01Obj, '1', True, [
               dut01Obj.linkPortMapping['lnk02'],
               dut01Obj.linkPortMapping['lnk03']], 'active'))
        assert(createLAG(dut02Obj, '1', True, [dut02Obj.linkPortMapping[
               'lnk02'], dut02Obj.linkPortMapping['lnk03']], 'passive'))

    def test_configureVLANs(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure VLANs on switches")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        # Switch 1
        LogOutput('info', "Configure VLAN on dut01")
        assert(configureVLAN(dut01Obj, 900, True))
        assert(
            addInterfaceVLAN(dut01Obj, 900, True,
                             dut01Obj.linkPortMapping['lnk01']))
        assert(addInterfaceVLAN(dut01Obj, 900, True, 'lag 1'))
        LogOutput('info', "Configure VLAN on dut02")
        assert(configureVLAN(dut02Obj, 900, True))
        assert(
            addInterfaceVLAN(dut02Obj, 900, True,
                             dut02Obj.linkPortMapping['lnk04']))
        assert(addInterfaceVLAN(dut02Obj, 900, True, 'lag 1'))

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

        LogOutput('info', "Configuring switch dut02")
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk02'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk03'],
                               True))
        assert(
            enableDutInterface(dut02Obj, dut02Obj.linkPortMapping['lnk04'],
                               True))

    def test_configureWorkstations(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Configure workstations")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        LogOutput('info', "Configuring workstation 1")
        assert(configureWorkstation(
            wrkston01Obj,
            wrkston01Obj.linkPortMapping[
                'lnk01'], "140.1.1.10", "255.255.255.0", "140.1.1.255", True))
        LogOutput('info', "Configuring workstation 2")
        assert(configureWorkstation(
            wrkston02Obj,
            wrkston02Obj.linkPortMapping[
                'lnk04'], "140.1.1.11", "255.255.255.0", "140.1.1.255", True))

    def test_pingBetweenClients1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test ping between clients work")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        assert(pingBetweenWorkstations(
            wrkston01Obj, wrkston02Obj, "140.1.1.11", True))

    def test_deleteLAGs1(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Delete non-existent LAGs on both DUTs")
        LogOutput('info', "############################################")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")

        LogOutput('info', 'Attemtpt to delete LAGs on dut01')
        LogOutput('info', 'With ID XX')
        assert(deleteLAGNegative(dut01Obj, 'XX', '1', 'active', [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 0')
        assert(deleteLAGNegative(dut01Obj, '0', '1', 'active', [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID -1')
        assert(deleteLAGNegative(dut01Obj, '-1', '1', 'active', [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 2000')
        assert(deleteLAGNegative(dut01Obj, '2000', '1', 'active', [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 2001')
        assert(deleteLAGNegative(dut01Obj, '2001', '1', 'active', [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID @%&$#()')
        assert(deleteLAGNegative(dut01Obj, '@%&$#()', '1', 'active', [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 60000')
        assert(deleteLAGNegative(dut01Obj, '60000', '1', 'active', [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 600')
        assert(deleteLAGNegative(dut01Obj, '600', '1', 'active', [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 2')
        assert(deleteLAGNegative(dut01Obj, '2', '1', 'active', [
            dut01Obj.linkPortMapping['lnk02'],
            dut01Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))

        LogOutput('info', 'Attemtpt to delete LAGs on dut01')
        LogOutput('info', 'With ID XX')
        assert(deleteLAGNegative(dut02Obj, 'XX', '1', 'passive', [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 0')
        assert(deleteLAGNegative(dut02Obj, '0', '1', 'passive', [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID -1')
        assert(deleteLAGNegative(dut02Obj, '-1', '1', 'passive', [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 2000')
        assert(deleteLAGNegative(dut02Obj, '2000', '1', 'passive', [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 2001')
        assert(deleteLAGNegative(dut02Obj, '2001', '1', 'passive', [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID @%&$#()')
        assert(deleteLAGNegative(dut02Obj, '@%&$#()', '1', 'passive', [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 60000')
        assert(deleteLAGNegative(dut02Obj, '60000', '1', 'passive', [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 600')
        assert(deleteLAGNegative(dut02Obj, '600', '1', 'passive', [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))
        LogOutput('info', 'With ID 2')
        assert(deleteLAGNegative(dut02Obj, '2', '1', 'passive', [
            dut02Obj.linkPortMapping['lnk02'],
            dut02Obj.linkPortMapping['lnk03']], 'l3-src-dst', False, False))

    def test_pingBetweenClients2(self):
        LogOutput('info', "\n############################################")
        LogOutput('info', "Test ping between clients work")
        LogOutput('info', "############################################")
        wrkston01Obj = self.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = self.topoObj.deviceObjGet(device="wrkston02")
        assert(pingBetweenWorkstations(
            wrkston01Obj, wrkston02Obj, "140.1.1.11", True))
