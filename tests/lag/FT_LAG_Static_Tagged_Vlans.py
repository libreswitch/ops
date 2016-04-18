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
import pytest
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.host import *

topoDict = {"topoExecution": 1500,
            "topoDevices": "dut01 dut02\
                            wrkston01 wrkston02 wrkston03 wrkston04",
            "topoLinks": "lnk01:dut01:wrkston01,\
                          lnk02:dut01:wrkston02,\
                          lnk03:dut01:dut02,\
                          lnk04:dut01:dut02,\
                          lnk05:dut02:wrkston03,\
                          lnk06:dut02:wrkston04",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation,\
                            wrkston03:system-category:workstation,\
                            wrkston04:system-category:workstation"}


def switch_reboot(dut01):
    # Reboot switch
    LogOutput('info', "Reboot switch")
    dut01.Reboot()
    rebootRetStruct = returnStruct(returnCode=0)
    return rebootRetStruct


def clean_up(dut01, dut02, wrkston01, wrkston02, wrkston03, wrkston04):

    listDut = [dut01, dut02]
    for currentDut in listDut:
        devRebootRetStruct = switch_reboot(currentDut)
        if devRebootRetStruct.returnCode() != 0:
            LogOutput('error', "Failed to reboot Switch")
            assert(False)
    else:
        LogOutput('info', "Passed Switch Reboot ")


class Test_ft_LAG_Static_tagged_vlans:

    listDut = None
    dut01Obj = None
    dut02Obj = None
    wrkston01Obj = None
    wrkston02Obj = None
    wrkston03Obj = None
    wrkston04Obj = None
    lagId = None
    l2IpAddress = None
    l2IpGateway = None
    l2IpNetwork = None
    l2IpNetmask = None
    vlanL2Id = None

    def setup_class(cls):

        # Create Topology object and connect to devices
        Test_ft_LAG_Static_tagged_vlans.testObj = testEnviron(
            topoDict=topoDict)
        Test_ft_LAG_Static_tagged_vlans.topoObj = \
            Test_ft_LAG_Static_tagged_vlans.testObj.topoObjGet()

        # Global definition
        global listDut
        global dut01Obj
        global dut02Obj
        global wrkston01Obj
        global wrkston02Obj
        global wrkston03Obj
        global wrkston04Obj
        global lagId
        global l2IpAddress
        global l2IpGateway
        global l2IpNetwork
        global l2IpNetmask
        global vlanL2Id

        # Var initiation
        lagId = 150
        l2IpAddress = ["10.2.2.100", "10.2.2.101", "10.2.2.102", "10.2.2.103"]
        l2IpGateway = "10.2.2.1"
        l2IpNetwork = "10.2.2.255"
        l2IpNetmask = "255.255.255.0"
        vlanL2Id = [900, 950]
        dut01Obj = cls.topoObj.deviceObjGet(device="dut01")
        dut02Obj = cls.topoObj.deviceObjGet(device="dut02")

        wrkston01Obj = cls.topoObj.deviceObjGet(device="wrkston01")
        wrkston02Obj = cls.topoObj.deviceObjGet(device="wrkston02")
        wrkston03Obj = cls.topoObj.deviceObjGet(device="wrkston03")
        wrkston04Obj = cls.topoObj.deviceObjGet(device="wrkston04")

        listDut = [dut01Obj, dut02Obj]

    def teardown_class(cls):
        # Terminate all nodes
        clean_up(dut01Obj,
                 dut02Obj,
                 wrkston01Obj,
                 wrkston02Obj,
                 wrkston03Obj,
                 wrkston04Obj)
        Test_ft_LAG_Static_tagged_vlans.topoObj.terminate_nodes()

    ##########################################################################
    # Step 1 - Reboot Switch
    ##########################################################################

    def test_reboot_switches(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 1 - Reboot the switches")
        LogOutput('info', "###############################################")

        for currentDut in listDut:
            devRebootRetStruct = switch_reboot(currentDut)
            if devRebootRetStruct.returnCode() != 0:
                LogOutput('error', "Failed to reboot Switch")
                assert(False)
            else:
                LogOutput('info', "Passed Switch Reboot ")

    ##########################################################################
    # Step 2 - Configured Lag
    ##########################################################################

    def test_configure_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 2 -Configure lag in the switch")
        LogOutput('info', "###############################################")

        devLagRetStruct1 = lagCreation(
            deviceObj=dut01Obj,
            lagId=lagId,
            configFlag=True)
        devLagRetStruct2 = lagCreation(
            deviceObj=dut02Obj,
            lagId=lagId,
            configFlag=True)

        if devLagRetStruct1.returnCode() != 0 \
                or devLagRetStruct2.returnCode() != 0:
            LogOutput('error', "Failed to configured lag in the switchs")
            assert(False)
        else:
            LogOutput('info', "Passed lag configured ")

    ##########################################################################
    # Step 3 - Configured vlan
    ##########################################################################

    def test_configure_vlan(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 3 - Configure vlan  in the switch")
        LogOutput('info', "###############################################")

        for currentVlan in vlanL2Id:
            devLagRetStruct1 = AddVlan(
                deviceObj=dut01Obj,
                vlanId=currentVlan,
                config=True)

            devLagRetStruct2 = AddVlan(
                deviceObj=dut02Obj,
                vlanId=currentVlan,
                config=True)

            if devLagRetStruct1.returnCode() != 0 \
                    or devLagRetStruct2.returnCode() != 0:
                LogOutput('error', "Failed to create vlan in the switchs")
                assert(False)
            else:
                LogOutput('info', "Vlan created")

        for currentVlan in vlanL2Id:
            devLagRetStruct1 = VlanStatus(
                deviceObj=dut01Obj,
                vlanId=currentVlan,
                status=True)
            devLagRetStruct2 = VlanStatus(
                deviceObj=dut02Obj,
                vlanId=currentVlan,
                status=True)

            if devLagRetStruct1.returnCode() != 0 \
                    or devLagRetStruct2.returnCode() != 0:
                LogOutput('error', "Failed to enable the vlan in the switchs")
                assert(False)
            else:
                LogOutput('info', "Passed vlan enable ")

    ##########################################################################
    # Step 4 - Add ports to vlan
    ##########################################################################

    def test_interface_vlan(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 4 - Configure vlan in  the interface")
        LogOutput('info', "###############################################")

        dut01Interface01 = dut01Obj.linkPortMapping['lnk01']
        dut01Interface02 = dut01Obj.linkPortMapping['lnk02']
        dut01Interface03 = "lag " + str(lagId)

        dut02Interface01 = dut02Obj.linkPortMapping['lnk05']
        dut02Interface02 = dut02Obj.linkPortMapping['lnk06']
        dut02Interface03 = "lag " + str(lagId)

        # Configured Vlan for device 1
        devIntLagRetStruct1 = AddPortToVlan(
            deviceObj=dut01Obj,
            vlanId=vlanL2Id[0],
            interface=dut01Interface01,
            access=True,
            config=True)

        devIntLagRetStruct2 = AddPortToVlan(
            deviceObj=dut01Obj,
            vlanId=vlanL2Id[1],
            interface=dut01Interface02,
            access=True,
            config=True)

        if devIntLagRetStruct1.returnCode() != 0 \
                or devIntLagRetStruct2.returnCode() != 0:
            LogOutput('error',
                      "Failed to configured vlan in the interface")
            assert(False)
        else:
            LogOutput('info', "Passed interface vlan configured")

        # Configured Vlan for device 2
        devIntLagRetStruct1 = AddPortToVlan(
            deviceObj=dut02Obj,
            vlanId=vlanL2Id[0],
            interface=dut02Interface01,
            access=True,
            config=True)

        devIntLagRetStruct2 = AddPortToVlan(
            deviceObj=dut02Obj,
            vlanId=vlanL2Id[1],
            interface=dut02Interface02,
            access=True,
            config=True)

        if devIntLagRetStruct1.returnCode() != 0 \
                or devIntLagRetStruct2.returnCode() != 0:
            LogOutput('error',
                      "Failed to configured vlan in the interface")
            assert(False)
        else:
            LogOutput('info', "Passed interface vlan configured")

        for currentVlan in vlanL2Id:
            devIntLagRetStruct1 = AddPortToVlan(
                deviceObj=dut01Obj,
                vlanId=currentVlan,
                interface=dut01Interface03,
                allowed=True,
                config=True)

            devIntLagRetStruct2 = AddPortToVlan(
                deviceObj=dut02Obj,
                vlanId=currentVlan,
                interface=dut02Interface03,
                allowed=True,
                config=True)

            if devIntLagRetStruct1.returnCode() != 0 \
                    or devIntLagRetStruct2.returnCode() != 0:
                LogOutput('error',
                          "Failed to configured vlan in the Lag")
                assert(False)
            else:
                LogOutput('info', "Passed Lag vlan configured")

    ##########################################################################
    # Step 5 - Add ports to lag
    ##########################################################################

    def test_configure_interface_lag(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 5 - Configure lag id in the interface")
        LogOutput('info', "###############################################")

        dut01Interface01 = dut01Obj.linkPortMapping['lnk03']
        dut01Interface02 = dut01Obj.linkPortMapping['lnk04']

        dut02Interface01 = dut02Obj.linkPortMapping['lnk03']
        dut02Interface02 = dut02Obj.linkPortMapping['lnk04']

        listInterfacesDut1 = [dut01Interface01, dut01Interface02]
        listInterfacesDut2 = [dut02Interface01, dut02Interface02]

        for interfaceDut in listInterfacesDut1:
            devIntLagRetStruct = InterfaceLagIdConfig(
                deviceObj=dut01Obj,
                interface=interfaceDut,
                lagId=lagId,
                enable=True)
            if devIntLagRetStruct.returnCode() != 0:
                LogOutput('error', "Failed to configured interface lag id")
                assert(False)
            else:
                LogOutput('info', "Passed interface lag id configured ")

        for interfaceDut in listInterfacesDut2:
            devIntLagRetStruct = InterfaceLagIdConfig(
                deviceObj=dut02Obj,
                interface=interfaceDut,
                lagId=lagId,
                enable=True)

            if devIntLagRetStruct.returnCode() != 0:
                LogOutput('error', "Failed to configured interface lag id")
                assert(False)
            else:
                LogOutput('info', "Passed interface lag id configured ")

    ##########################################################################
    # Step 6 - Configure Workstation
    ##########################################################################

    def test_configure_workstations(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 6 - Configure Workstations")
        LogOutput('info', "###############################################")

        # Client Side
        retStruct = wrkston01Obj.NetworkConfig(
            ipAddr=l2IpAddress[0],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston01Obj.linkPortMapping['lnk01'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)

        # Server side
        retStruct = wrkston02Obj.NetworkConfig(
            ipAddr=l2IpAddress[1],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston02Obj.linkPortMapping['lnk02'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)

        retStruct = wrkston03Obj.NetworkConfig(
            ipAddr=l2IpAddress[2],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston03Obj.linkPortMapping['lnk05'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)

        retStruct = wrkston04Obj.NetworkConfig(
            ipAddr=l2IpAddress[3],
            netMask=l2IpNetmask,
            broadcast=l2IpNetwork,
            interface=wrkston04Obj.linkPortMapping['lnk06'],
            config=True)
        if retStruct.returnCode() != 0:
            LogOutput('error', "Failed to configured Client station")
            assert(False)

        LogOutput('info', "Complete workstation configuration")

    ##########################################################################
    # Step 7 - Enable switch ports
    ##########################################################################

    def test_enable_switch_interfaces(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 7 - Enable all the switchs interfaces")
        LogOutput('info', "###############################################")

        switchInterface1 = dut01Obj.linkPortMapping['lnk01']
        switchInterface2 = dut01Obj.linkPortMapping['lnk02']
        switchInterface3 = dut01Obj.linkPortMapping['lnk03']
        switchInterface4 = dut01Obj.linkPortMapping['lnk04']

        listSwitchInterfacesDut1 = [
            switchInterface1,
            switchInterface2,
            switchInterface3,
            switchInterface4]

        switchInterface1 = dut02Obj.linkPortMapping['lnk03']
        switchInterface2 = dut02Obj.linkPortMapping['lnk04']
        switchInterface3 = dut02Obj.linkPortMapping['lnk05']
        switchInterface4 = dut02Obj.linkPortMapping['lnk06']

        listSwitchInterfacesDut2 = [
            switchInterface1,
            switchInterface2,
            switchInterface3,
            switchInterface4]

        # Enable ports from switch 1
        for currentInterface in listSwitchInterfacesDut1:
            retStruct = InterfaceEnable(
                deviceObj=dut01Obj,
                enable=True,
                interface=currentInterface)

            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable port on switch")
                assert(False)
        # Enable ports from switch 2
        for currentInterface in listSwitchInterfacesDut2:
            retStruct = InterfaceEnable(
                deviceObj=dut02Obj,
                enable=True,
                interface=currentInterface)

            if retStruct.returnCode() != 0:
                LogOutput('error', "Failed to enable port on switch")
                assert(False)

        LogOutput('info', "All ports in switches are enable")

    ##########################################################################
    # Step 8 - Send Traffic
    ##########################################################################

    def test_send_traffic(self):

        LogOutput('info', "\n###############################################")
        LogOutput('info', "# Step 8 - Send traffic betweem clients")
        LogOutput('info', "###############################################")

        # WorkStation 1 Ping other side
        retStructValid = wrkston01Obj.Ping(ipAddr=l2IpAddress[2])
        retStructInvalid = wrkston01Obj.Ping(ipAddr=l2IpAddress[3])
        if retStructValid.returnCode() != 0 \
                or retStructInvalid.returnCode() == 0:
            LogOutput('error',
                      "Failed to ping from workstation 1 to workstation2")
            # assert(False)
        else:
            packet_loss = retStructValid.valueGet(key='packet_loss')
            packets_sent = retStructValid.valueGet(key='packets_transmitted')
            packets_received = retStructValid.valueGet(key='packets_received')
            LogOutput('info', "Packets Sent:\t" + str(packets_sent))
            LogOutput('info', "Packets Recv:\t" + str(packets_received))
            LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
            if packet_loss != 0:
                LogOutput('error', "Packet Loss > 0%")
                # assert(False)

            packet_loss = retStructInvalid.valueGet(key='packet_loss')
            packets_sent = retStructInvalid.valueGet(
                key='packets_transmitted')
            packets_received = retStructInvalid.valueGet(
                key='packets_received')
            LogOutput('info', "Packets Sent:\t" + str(packets_sent))
            LogOutput('info', "Packets Recv:\t" + str(packets_received))
            LogOutput('info', "Packet Loss %:\t" + str(packet_loss))

        # Workstation 2 ping to other side
        retStructValid = wrkston02Obj.Ping(ipAddr=l2IpAddress[3])
        retStructInvalid = wrkston02Obj.Ping(ipAddr=l2IpAddress[2])
        if retStructValid.returnCode() != 0 \
                or retStructInvalid.returnCode() == 0:
            LogOutput('error',
                      "Failed to ping from workstation 2 to workstation1")
            assert(False)
        else:
            packet_loss = retStructValid.valueGet(key='packet_loss')
            packets_sent = retStructValid.valueGet(
                key='packets_transmitted')
            packets_received = retStructValid.valueGet(
                key='packets_received')
            LogOutput('info', "Packets Sent:\t" + str(packets_sent))
            LogOutput('info', "Packets Recv:\t" + str(packets_received))
            LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
            if packet_loss != 0:
                LogOutput('error', "Packet Loss > 0%")
                # assert(False)
            packet_loss = retStructInvalid.valueGet(key='packet_loss')
            packets_sent = retStructInvalid.valueGet(
                key='packets_transmitted')
            packets_received = retStructInvalid.valueGet(
                key='packets_received')
            LogOutput('info', "Packets Sent:\t" + str(packets_sent))
            LogOutput('info', "Packets Recv:\t" + str(packets_received))
            LogOutput('info', "Packet Loss %:\t" + str(packet_loss))
