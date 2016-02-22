#!/usr/bin/env python

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
import re
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

#
# The purpose of this test is to test
# SFTP functionality
#
# For this test, we need below topology
#
#       +---+----+        +--------+
#       |        |        |        |
#       +switch1 +--------|switch2 |
#       |(Client)|        |(Server)|
#       |        |        |        |
#       +---+----+        +--------+
#


# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01 dut02",
            "topoDevices": "dut01 dut02",
            "topoLinks":  "lnk01:dut01:dut02",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch",
            "topoLinkFilter": "lnk01:dut01:interface:eth0,\
                              lnk01:dut02:interface:eth0"}


# Enter VTYSH
def enterVtyshShell(dut01):
    retStruct = dut01.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    return True


# Enable/Disable SFTP server
# Description : Enable/Disable SFTP server based on the
#               condition and verify the status of server
#               using show command
def sftpServerConfigTest(**kwargs):

    dut01 = kwargs.get('switchObj', None)
    condition = kwargs.get('cond', None)
    # opsuccess = False

    retStruct = dut01.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    dut01.DeviceInteract(command="configure terminal")

    if condition is True:
        # Enable SFTP server
        devIntReturn = dut01.DeviceInteract(command="sftp server enable")
        dut01.DeviceInteract(command="end")
        devIntReturn = dut01.DeviceInteract(command="show running-config")
        output = devIntReturn.get('buffer')
        if 'enable' not in output:
            assert "Enable SFTP server - FAIL"
        else:
            LogOutput('info', "Enable SFTP server - SUCCESS")
            returnCls = returnStruct(returnCode=0)
    else:
        # Disable SFTP server
        devIntReturn = dut01.DeviceInteract(command="no sftp server enable")
        dut01.DeviceInteract(command="end")
        devIntReturn = dut01.DeviceInteract(command="show running-config")
        output = devIntReturn.get('buffer')
        if 'enable' in output:
            assert "Disable SFTP server - FAIL"
        else:
            LogOutput('info', "Disable SFTP server - SUCCESS")
            returnCls = returnStruct(returnCode=0)

    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enable/disable SFTP server"

    dut01.DeviceInteract(command="end")
    returnCls = returnStruct(returnCode=0)
    return returnCls


# Support funtion to configure an IP on mgmt interface
def interfaceMgmtConfig(**kwargs):

    dut01 = kwargs.get('switchObj', None)
    ipAddr = kwargs.get('ipAddr', None)

    if(enterVtyshShell(dut01) is False):
        return False

    static = "ip static"
    dut01.DeviceInteract(command="configure terminal")
    devIntReturn = dut01.DeviceInteract(command="interface mgmt")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the mgmt interface"
    cmd = static+" "+ipAddr
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to assign the ip static address"
    dut01.DeviceInteract(command="end")

    returnCls = returnStruct(returnCode=0)
    return returnCls


# Test to verify SFTP client get
# Description : Use one switch as SFTP server and download a
#               file from server using a get command and
#               verify this operation by looking for the
#               downloaded file in the client and if found,
#               delete this downloaded file
def sftpClientGet(**kwargs):
    LogOutput('info', "\n############################################\n")
    LogOutput('info', "Verify SFTP client get")
    LogOutput('info', "\n############################################\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    opsuccess = False
    copy = "copy sftp"
    username = "root"
    srcpath = "/etc/ssh/sshd_config"
    destpath = "/home/admin/"
    destfile = "trial_file"

    # Enable interface mgmt on SW1
    retStruct = interfaceMgmtConfig(switchObj=switch1, ipAddr="10.1.1.1/24")
    if retStruct.returnCode() != 0:
        assert "Unable to config mgmt interface on switch1"
    LogOutput('info', "Enable interface mgmt on switch1 - SUCCESS")

    # Enable interface mgmt on SW2
    retStruct = interfaceMgmtConfig(switchObj=switch2, ipAddr="10.1.1.2/24")
    if retStruct.returnCode() != 0:
        assert "Unable to config mgmt interface on switch2"
    LogOutput('info', "Enable interface mgmt on switch2 - SUCCESS")

    # Enable SFTP server on SW2
    LogOutput('info', "Enabling SFTP server on switch2")
    retStruct = sftpServerConfigTest(switchObj=switch2, cond=True)
    if retStruct.returnCode() != 0:
        assert "switch2 SFTP server is disabled."

    # SFTP get operation
    if(enterVtyshShell(switch1) is False):
        return False

    hostip = "10.1.1.2"
    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+destpath+destfile
    devIntReturn = switch1.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')

    # Verify the downloaded file
    devIntReturn = switch1.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Downloaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch1.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the downloaded file"
        LogOutput('info', "Downloaded file clean up - SUCCESS")
        LogOutput('info', "Verification of SFTP get operation - SUCCESS")

    switch1.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP get operation failed"

    if opsuccess is True:
        LogOutput('info', "\n SFTP client get - PASSED\n")
    else:
        LogOutput('info', "\n SFTP client get - FAILED\n")

    return True


# Test the SFTP client interactive mode
# Description : Use one switch as SFTP server and download a
#               file from server using a interactive get command
#               and verify this operation by looking for the
#               downloaded file in the client and if found,
#               delete this downloaded file. Upload a file
#               from client to the server using interactive put
#               verify this operation by looking for the uploaded
#               file and if found, delete this uploaded file
def sftpClientInt(**kwargs):
    LogOutput('info', "\n############################################\n")
    LogOutput('info', "Verify SFTP interactive client")
    LogOutput('info', "\n############################################\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    opsuccess = False
    copy = "copy sftp"
    username = "root"
    srcpath = "/etc/ssh/sshd_config"
    destpath = "/home/admin/"
    destfile = "trial_file"
    hostip = "10.1.1.2"

    # Interactive mode - get operation
    cmd = copy+" "+username+" "+hostip
    switch1.expectHndl.send(cmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)


    # Perform get operation
    getcmd = "get"+" "+srcpath+" "+destpath+destfile
    switch1.expectHndl.send(getcmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    switch1.DeviceInteract(command="quit")

    # Verify the interactive get operation
    devIntReturn = switch1.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Downloaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch1.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the downloaded file"
        LogOutput('info', "Downloaded file clean up - SUCCESS")
        LogOutput('info', "Verification of interactive SFTP "
                          "get operation - SUCCESS")

    switch1.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP get operation failed"

    if opsuccess is True:
        LogOutput('info', "\n SFTP client interactive get - PASSED\n")
    else:
        LogOutput('info', "\n SFTP client interactive get - FAILED\n")

    # Interactive mode - put operation
    opsuccess = False
    cmd = copy+" "+username+" "+hostip
    switch1.expectHndl.send(cmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    # Perform put operation
    putcmd = "put"+" "+srcpath+" "+destpath+destfile
    switch1.expectHndl.send(putcmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)


    switch1.DeviceInteract(command="quit")

    # Verify the interactive put operation
    if(enterVtyshShell(switch2) is False):
        return False

    devIntReturn = switch2.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch2.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Uploaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch2.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the uploaded file"
        LogOutput('info', "Uploaded file clean up - SUCCESS")
        LogOutput('info', "Verification of interactive SFTP "
                          "put operation - SUCCESS")

    switch2.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP put operation failed"

    if opsuccess is True:
        LogOutput('info', "\n SFTP client interactive put - PASSED\n")
    else:
        LogOutput('info', "\n SFTP client interactive put - FAILED\n")

    return True


# Test to verify SFTP functionality post server disable
# Description : This is a neagative test scenario disable SFTP server
#               and download a file from server using a get command
#               this copy should not be possible
def sftpPostServerDisable(**kwargs):
    LogOutput('info', "\n############################################\n")
    LogOutput('info', "Verify SFTP functionality post server disable")
    LogOutput('info', "\n############################################\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    copy = "copy sftp"
    username = "root"
    hostip = "10.1.1.2"
    srcpath = "/etc/ssh/sshd_config"
    destpath = "/home/admin/"
    destfile = "trial_file"
    failMsg = "Connection reset by peer"

    # Disable SFTP server on SW2
    LogOutput('info', "Disable SFTP server on switch2")
    retStruct = sftpServerConfigTest(switchObj=switch2, cond=False)
    if retStruct.returnCode() != 0:
        assert "switch2 disable SFTP server - FAILED."

    # Perform SFTP operation on SW1
    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd)

    if failMsg in out.get('buffer'):
        LogOutput('info', "Verify SFTP get after SFTP "
                          "server disable - SUCCESS")
    else:
        LogOutput('error', "Verify SFTP get after SFTP "
                           "server disable - FAILED")
        assert "Verification of SFTP get post SFTP " \
               "server disable failed"

    return True


# Test to verify negative scenarios
# Description : Verify the negative scenarios when user source
#               path of the file is invalid and when destination
#               path is invalid
def sftpFailCases(**kwargs):
    LogOutput('info', "\n############################################\n")
    LogOutput('info', "Verify SFTP negative test cases")
    LogOutput('info', "\n############################################\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    # opsuccess = False
    copy = "copy sftp"
    username = "root"
    hostip = "10.1.1.2"
    srcpath = "/etc/ssh/sshd_config"
    destpath = "/home/admin/"
    destfile = "trial_file"
    invalidSrcPath = "/invalid/src_path"
    srcFailMsg = "not found"
    invalidDestPath = "/invalid/dest_file"
    destFailMsg = "No such file or directory"

    # Enable SFTP server on SW2
    LogOutput('info', "Enable SFTP server on switch2")
    retStruct = sftpServerConfigTest(switchObj=switch2, cond=True)
    if retStruct.returnCode() != 0:
        assert "switch2 enable SFTP server - FAILED"

    # Invalid source path test
    cmd = copy+" "+username+" "+hostip+" "+invalidSrcPath+" "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd)

    if srcFailMsg in out.get('buffer'):
        LogOutput('info', "Verify invalid source path test - SUCCESS")
    else:
        LogOutput('error', "Verify invalid source path test - FAILED")
        assert "Verification of SFTP get with invalid source path failed"

    # Invalid destination path test
    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+invalidDestPath
    out = switch1.DeviceInteract(command=cmd)

    if destFailMsg in out.get('buffer'):
        LogOutput('info', "Verify invalid destination path test - SUCCESS")
    else:
        LogOutput('error', "Verify invalid destination path test - FAILED")
        assert "Verification of SFTP get with invalid destination path failed"

    return True


# Support function to reboot the switch
def switch_reboot(deviceObj):
    LogOutput('info', "Reboot switch " + deviceObj.device)
    deviceObj.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct


# Test to check SFTP post reboot
# Description : Enable SFTP server on a switch, perform a copy
#               from a client and verify this action. Now save the
#               configs on the server and reboot it, so even after
#               reboot the configs should be available and respective
#               operation should be allowed
def sftpRebootTest(**kwargs):
    LogOutput('info', "\n############################################\n")
    LogOutput('info', "Verify SFTP post reboot")
    LogOutput('info', "\n############################################\n")

    switch1 = kwargs.get('switch1', None)
    switch2 = kwargs.get('switch2', None)

    opsuccess = False
    copy = "copy sftp"
    username = "root"
    hostip = "10.1.1.2"
    srcpath = "/etc/ssh/sshd_config"
    destpath = "/home/admin/"
    destfile = "trial_file"

    # SFTP operations before reboot
    if(enterVtyshShell(switch1) is False):
        return False

    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+destpath+destfile
    devIntReturn = switch1.DeviceInteract(command=cmd)
    switch1.expectHndl.send(cmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    # Verify the downloaded file
    devIntReturn = switch1.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Downloaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch1.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the downloaded file"
        LogOutput('info', "Downloaded file clean up - SUCCESS")
        LogOutput('info', "Verification of SFTP before reboot - SUCCESS")

    switch1.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP before reboot failed"

    # Save the configuration on SW2.
    if(enterVtyshShell(switch2) is False):
        return False

    runCfg = "copy running-config startup-config"
    devIntReturn = switch2.DeviceInteract(command=runCfg)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to save the running configuration"

    # Perform reboot of SW2.
    devRebootRetStruct = switch_reboot(switch2)
    if devRebootRetStruct.returnCode() != 0:
        LogOutput('error', "Switch2 reboot - FAILED")
        assert(devRebootRetStruct.returnCode() == 0)
    else:
        LogOutput('info', "Switch2 reboot - SUCCESS")

    # SFTP get after reboot.
    opsuccess = False
    cmd = copy+" "+username+" "+hostip+" "+srcpath+" "+destpath+destfile
    switch1.expectHndl.send(cmd)
    switch1.expectHndl.send('\r')
    time.sleep(1)

    # Verify the downloaded file
    devIntReturn = switch1.DeviceInteract(command="start-shell")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter the bash shell"

    cmd1 = "ls "+destpath+destfile
    out = switch1.DeviceInteract(command=cmd1)

    if destpath+destfile in out.get('buffer') and \
       "No such file" not in out.get('buffer'):
        opsuccess = True
        LogOutput('info', "Downloaded file found")
        cmd2 = "rm -rf "+destpath+destfile
        devIntReturn = switch1.DeviceInteract(command=cmd2)
        retCode = devIntReturn.get('returnCode')
        assert retCode == 0, "Failed to erase the downloaded file"
        LogOutput('info', "Downloaded file clean up - SUCCESS")
        LogOutput('info', "Verification of SFTP after reboot - SUCCESS")

    switch1.DeviceInteract(command="exit")
    assert opsuccess is True, "Verification of SFTP after reboot failed"

    if opsuccess is True:
        LogOutput('info', "\n SFTP feature post reboot - PASSED\n")
    else:
        LogOutput('info', "\n SFTP feature post reboot - FAILED\n")
        assert "SFTP feature post reboot"

    return True


# Test class to verify SFTP
class Test_sftp:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_sftp.testObj =\
            testEnviron(topoDict=topoDict, defSwitchContext="vtyShell")
        # Get topology object
        Test_sftp.topoObj = \
            Test_sftp.testObj.topoObjGet()
        # Defect Note:  Waiting for Taiga ID 682 to get fixed to
        if Test_sftp.topoObj.topoType == "physical":
            LogOutput('info',
                      "Skipping  test physical run due to defect #682")
            pytest.skip("Skipping  test physical run due defect #682")

    def teardown_class(cls):
        Test_sftp.topoObj.terminate_nodes()

    def test_sftp_complete(self):
        # GEt Device objects
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")

        LogOutput('info', "### SFTP server enable/disable test ###")
        # SFTP server enable test
        sftpServerConfigTest(switchObj=dut02Obj, cond=True)
        # SFTP server disable test
        sftpServerConfigTest(switchObj=dut02Obj, cond=False)

        LogOutput('info', "### SFTP client get test ###")
        sftpClientGet(switch1=dut01Obj, switch2=dut02Obj)

        LogOutput('info', "### SFTP client interactive mode test ###")
        sftpClientInt(switch1=dut01Obj, switch2=dut02Obj)

        LogOutput('info', "### SFTP post server disable test ###")
        sftpPostServerDisable(switch1=dut01Obj, switch2=dut02Obj)

        LogOutput('info', "### SFTP negative test cases ###")
        sftpFailCases(switch1=dut01Obj, switch2=dut02Obj)

        LogOutput('info', "### SFTP reboot test ###")
        sftpRebootTest(switch1=dut01Obj, switch2=dut02Obj)
