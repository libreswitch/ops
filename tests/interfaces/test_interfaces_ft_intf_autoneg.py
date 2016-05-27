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
# Test Plan for Interfaces:
#
# USER CONFIG
#
# autonegotiation
#
# dut01: vtysh cmd:     configure terminal
# dut01: vtysh cmd:     vlan 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     interface 2
# dut01: vtysh cmd:     no routing
# dut01: vtysh cmd:     vlan access 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     interface 1
# dut01: vtysh cmd:     no routing
# dut01: vtysh cmd:     vlan access 10
# dut01: vtysh cmd:     no shutdown
# dut01: shell cmd:     ovs-vsctl show interface 1
#      : verify   :     hw_intf_config:autoneg="on"
# wrkston01: shell cmd: ping <to wrkston022ip addr>
#      : verify   :     ping succeeds
# dut01: vtysh cmd:     autonegotiation off
# dut01: shell cmd:     ovs-vsctl show interface 1
#      : verify   :     admin_state="down"
#      : verify   :     error="autoneg_required"
# wrkston01: shell cmd: ping <to wrkston02 ip addr>
#      : verify   :     ping fails
# dut01: vtysh cmd:     autonegotiation on
# dut01: shell cmd:     ovs-vsctl show interface 1
#      : verify   :     admin_state="up"
#      : verify   :     hw_intf_config:autoneg="on"
# wrkston01: shell cmd: ping <to wrkston02 ip addr>
#      : verify   :     ping succeeds
# dut01: vtysh cmd:     no autonegotiation
# dut01: shell cmd:     ovs-vsctl show interface 1
#      : verify   :     admin_state="up"
#      : verify   :     hw_intf_config:autoneg="on"
# wrkston01: shell cmd: ping <to wrkston02 ip addr>
#      : verify   :     ping succeeds
#
# Speed
#
# Speed can't be tested until 10G interfaces exist in RTL
#
# Duplex
#
# Duplex is currently not supported
#
# MTU
#
# MTU requires additional support in RTL to effectively implement a test
#
#
# Interface Statistics
#
# Verify Interface Statistics
#
# dut01: vtysh cmd:     configure terminal
# dut01: vtysh cmd:     vlan 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     interface 2
# dut01: vtysh cmd:     no routing
# dut01: vtysh cmd:     vlan access 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     interface 1
# dut01: vtysh cmd:     no routing
# dut01: vtysh cmd:     vlan access 10
# dut01: vtysh cmd:     no shutdown
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     exit
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     <collect baseline for stats>
# wrkston01: shell cmd: ping <to wrkston02 ip addr>
#      : action   :     sleep(5)
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     stats updated correctly
# wrkston02: shell cmd: ping <to wrkston01 ip addr>
#      : action   :     sleep(5)
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     stats updated correctly
#      : action   :     sleep(10)
# dut01: vtysh cmd:     show interface 1
# dut01: vtysh cmd:     show interface 2
#      : verify   :     stats not updated


import pytest
from opstestfw import *
from opstestfw.switch.CLI import *

# Topology definition

topoDict = {"topoType" : "physical",
            "topoExecution": 4000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 wrkston01 wrkston02",
            "topoLinks": "lnk01:dut01:wrkston01, \
                          lnk02:dut01:wrkston02",
            "topoFilters": "dut01:system-category:switch,\
                            wrkston01:system-category:workstation,\
                            wrkston02:system-category:workstation"}

PING_BYTES = 128
PING_CNT = 10
RC_ERR_FMT = "vtysh exit code non-zero, %d"
NET_1 = "10.10.10"
WS1_IP = NET_1 + ".1"
WS2_IP = NET_1 + ".2"
NET1_MASK = "255.255.255.0"
NET1_BCAST = NET_1 + ".0"
PACKET_LOSS = 15

class Test_template:

    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        # Create Topology object and connect to devices
        Test_template.testObj = testEnviron(topoDict=topoDict)
        Test_template.topoObj = Test_template.testObj.topoObjGet()

    def teardown_class(cls):
        # Terminate all nodes
        Test_template.topoObj.terminate_nodes()
        LogOutput('info', "Tearing Down Topology")

    def init_intf(self, obj, type="w"):
        if (type == "s"):
            rc = obj.cmd("ifconfig " + obj._intf + " " + obj._ip)
            rc = obj.cmd("ifconfig " + obj._intf + " netmask " + obj._netm)
            rc = obj.cmd("ifconfig " + obj._intf + " broadcast " + obj._bcast)
        else:
            rc = obj.NetworkConfig(ipAddr=obj._ip, netMask=obj._netm, \
                                   interface=obj._intf, \
                                   broadcast=obj._bcast, config=True)

    def init_devices(self):
        # Switch 1
        self.s1 = self.topoObj.deviceObjGet(device="dut01")

        # Reboot the switch
        LogOutput('info', "Rebooting the switch")
        self.s1.Reboot()

        # Workstation 1
        self.w1 = self.topoObj.deviceObjGet(device="wrkston01")
        self.w1._ip = WS1_IP
        self.w1._netm = NET1_MASK
        self.w1._bcast = NET1_BCAST
        self.w1._intf = "eth1"
        # Workstation 2
        self.w2 = self.topoObj.deviceObjGet(device="wrkston02")
        self.w2._ip = WS2_IP
        self.w2._netm = NET1_MASK
        self.w2._bcast = NET1_BCAST
        self.w2._intf = "eth1"

        # Bring up the interfaces
        LogOutput('info', "Bringup up w1 eth1")
        self.init_intf(self.w1)
        LogOutput('info', "Bringup up w2 eth1")
        self.init_intf(self.w2)

        LogOutput('info', "Device init complete")

    def open_vtysh(self):
        self.vtyconn = self.s1
        rc = self.vtyconn.VtyshShell()

    def close_vtysh(self):
        rc = self.vtyconn.VtyshShell(configOption="exit")

    def startup_sequence(self):
        # Setup devices
        LogOutput('info', "Setting up devices")
        self.init_devices()

        # Start vtysh session
        LogOutput('info', "Opening up vtysh session")
        self.open_vtysh()

    def verify_intf_admin_state(self, obj, intf, expected):
        obj.cmd("do start-shell")
        admin_state =  obj.cmd("ovs-vsctl get interface " + str(intf) + " admin_state").splitlines()
        obj.cmd("exit")
        i  = len(admin_state)
        if i >= 2:
            assert admin_state[i-1] == expected, "Interface should be %s, is %s" % \
                                         (expected, admin_state)
        else:
            assert 1 == 0, "Invalid response from get admin_state, resp = %s" % admin_state

    def verify_intf_error(self, obj, intf, expected):
        obj.cmd("do start-shell")
        error =  obj.cmd("ovs-vsctl get interface " + str(intf) + " error").splitlines()
        obj.cmd("exit")
        i  = len(error)
        if i >= 2:
            assert error[i-1] == expected, "Interface error should be %s, is %s" % \
                                           (expected, error)
        else:
            assert 1 == 0, "Invalid response from get error, resp = %s" % error

    def verify_intf_autoneg(self, obj, intf, expected):
        obj.cmd("do start-shell")
        autoneg =  obj.cmd("ovs-vsctl get interface " + str(intf) + \
                           " hw_intf_config:autoneg").splitlines()
        obj.cmd("exit")
        i  = len(autoneg)
        if i >= 2:
            if expected is True:
                assert autoneg[i-1] == "on", "Autoneg should be on, is off"
            else:
                assert autoneg[i-1] <> "on", "Autoneg should be off, is %s" % autoneg
        else:
            assert 1 == 0, "Invalid response from get autoneg, resp = %s" % autoneg

    def verify_ping(self, src, dest, expected):
        out = src.Ping(ipAddr=dest._ip, interval=.2, errorCheck=False,
            packetCount=30)

        if out is None:
            assert 1 == 0, "ping command failed, no output"

        LogOutput("info", "%s" % out.data)
        success = False;
        if out.data['packet_loss'] <= PACKET_LOSS:
            success = True;

        assert success == expected, "ping was %s, expected %s" % (success, expected)

    def cmd_set_1(self, obj):

        interface_1 = self.s1.linkPortMapping['lnk01']
        interface_2 = self.s1.linkPortMapping['lnk02']
        # Issue "configure terminal" command
        LogOutput("info", "sending configure terminal")
        rc = obj.cmd("configure terminal")
        LogOutput("info", "sending vlan 10")
        rc = obj.cmd("vlan 10")
        LogOutput("info", "sending no shutdown")
        rc = obj.cmd("no shutdown")
        LogOutput("info", "sending exit")
        rc = obj.cmd("exit")
        LogOutput("info", "sending interface %s" %interface_2)
        rc = obj.cmd("interface %s" %interface_2)
        LogOutput("info", "sending no routing")
        rc = obj.cmd("no routing")
        LogOutput("info", "sending vlan access 10")
        rc = obj.cmd("vlan access 10")
        LogOutput("info", "sending no shutdown")
        rc = obj.cmd("no shutdown")
        LogOutput("info", "sending interface %s" % interface_1)
        rc = obj.cmd("interface %s" % interface_1)
        LogOutput("info", "sending no routing")
        rc = obj.cmd("no routing")
        LogOutput("info", "sending vlan access 10")
        rc = obj.cmd("vlan access 10")


    def test_autonegotiation(self):
        # Get everything initially configured
        LogOutput('info', "*****Testing autonegotiation*****")
        self.startup_sequence()

        interface_1 = self.s1.linkPortMapping['lnk01']
        interface_2 = self.s1.linkPortMapping['lnk02']

        # Configure interfaces 1 & 2 on vlan 10, with 1 down and 2 up.
        LogOutput('info', "Cfg intfs 1 & 2 on vlan 10, with 1 down and 2 up")
        self.cmd_set_1(self.vtyconn)

        # Bring up interface 1
        LogOutput('info', "Bring intf %s up" %interface_1)
        rc = self.vtyconn.cmd("no shutdown")

        # Verify autoneg is on
        sleep(1)
        LogOutput('info', "Verify autoneg is on")
        self.verify_intf_autoneg(self.vtyconn, interface_1, True)

        # Verify ping works
        LogOutput('info', "Verify that ping from ws1 to ws2 works")
        self.verify_ping(self.w1, self.w2, True)

        # Turn autonegotiation off
        LogOutput('info', "Turn autonegotiation off")
        rc = self.vtyconn.cmd("autonegotiation off")

        # Verify autoneg is off
        sleep(1)
        LogOutput('info', "Verify autoneg is off")
        self.verify_intf_autoneg(self.vtyconn, interface_1, False)

        # Verify interface 1 is down
        LogOutput('info', "Verify that intf %s is down"%interface_1)
        self.verify_intf_admin_state(self.vtyconn, interface_1, "down")
        LogOutput('info',
            "Verify that intf %s error is autoneg_required"%interface_1)
        self.verify_intf_error(self.vtyconn, interface_1, "autoneg_required")

        # Verify ping fails
        LogOutput('info', "Verify that ping from ws1 to ws2 fails")
        self.verify_ping(self.w1, self.w2, False)

        # Turn autonegotiation on
        LogOutput('info', "Turn autonegotiation on")
        rc = self.vtyconn.cmd("autonegotiation on")

        # Verify autoneg is on
        sleep(1)
        LogOutput('info', "Verify autoneg is on and admin_state is up")
        self.verify_intf_autoneg(self.vtyconn, interface_1, True)
        self.verify_intf_admin_state(self.vtyconn, interface_1, "up")

        # Verify ping works
        LogOutput('info', "Verify that ping from ws1 to ws2 works")
        self.verify_ping(self.w1, self.w2, True)

        # Set autonegotiation to default (on)
        LogOutput('info', "Set autonegotiation to default (on)")
        rc = self.vtyconn.cmd("no autonegotiation")

        # Verify autoneg is on
        LogOutput('info', "Verify autoneg is on and admin_state is up")
        self.verify_intf_autoneg(self.vtyconn, interface_1, True)
        self.verify_intf_admin_state(self.vtyconn, interface_1, "up")

        # Verify ping works
        LogOutput('info', "Verify that ping from ws1 to ws2 works")
        self.verify_ping(self.w1, self.w2, True)

        LogOutput('info', "succeeded!")
