#!/usr/bin/python

# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
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


from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *
from opstestfw.switch.CLI.InterfaceIpConfig import InterfaceIpConfig
from opsvsiutils.vtyshutils import *

dict = {}


'''
TOPOLOGY 1
+------+             +------+             +---------+             +--------+
|      |   Area1     |      |   Area1     |         |   Area1     |        |
| SW1 1+------------+1 SW2 2+-------------+1  SW3  2+-------------+1  SW4  +
|      |             |      |             |         |             |        |
|      |             |      |             |         |             |        |
+------+             +------+             +---------+             +--------+

Switch 1 Configuration
IP ADDR is 10.10.10.1
Router Id is 1.1.1.1


Switch 2 Configuration
interface 1
IP ADDR is 10.10.10.2
Router Id is 2.2.2.2
interface 2
IP ADDR is 20.10.10.1


Switch 3 Configuration
IP ADDR is 20.10.10.2
Router Id is 3.3.3.3
interface 2
IP ADDR is 30.10.10.1

Switch 4 Configuration
IP ADDR is 30.10.10.2
Router Id is 4.4.4.4

TOPOLOGY 2
        (L2 Switch)
      _____dut04_______
     |       |         |
   dut01   dut02    dut03


Switch 1 Configuration
IP ADDR is 10.10.10.1
Router Id is 1.1.1.1


Switch 2 Configuration
IP ADDR is 10.10.10.2
Router Id is 2.2.2.2


Switch 3 Configuration
IP ADDR is 10.10.10.3
Router Id is 3.3.3.3

'''

OSPF_DUT_OBJ = 'dut_obj'
OSPF_ROUTER_KEY = 'router_id'
OSPF_IP_ADDR_KEY = 'ip'
OSPF_IP_MASK_KEY = "mask"
OSPF_NETWORK_KEY = "network"
OSPF_LINK_KEY = 'lnk'
OSPF_AREA_KEY = "area"

VTYSH_CR = '\r\n'
OSPF_DEAD_TIMER = 40


# Topology definition
# Topology 1
topoDict = {"topoExecution": 5000,
            "topoType": "virtual",
            "topoTarget": "dut01 dut02 dut03 dut04",
            "topoDevices": "dut01 dut02 dut03 dut04",
            "topoLinks": "lnk01:dut01:dut02, lnk02:dut02:dut03,\
                          lnk03:dut03:dut04",
            "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            dut04:system-category:switch"}

# Topology 2
topoDict1 = {"topoExecution": 5000,
             "topoType": "virtual",
             "topoTarget": "dut01 dut02 dut03 dut04",
             "topoDevices": "dut01 dut02 dut03 dut04",
             "topoLinks": "lnk01:dut01:dut04, lnk01:dut02:dut04,\
                          lnk01:dut03:dut04",
             "topoFilters": "dut01:system-category:switch,\
                            dut02:system-category:switch,\
                            dut03:system-category:switch,\
                            dut04:system-category:switch"}

# Topology 1 configs
dict01 = {OSPF_ROUTER_KEY: "1.1.1.1",
          OSPF_IP_ADDR_KEY: "10.10.10.1", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.1/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "1", }


dict02 = {OSPF_ROUTER_KEY: "2.2.2.2",
          OSPF_IP_ADDR_KEY: "10.10.10.2", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "10.10.10.2/24", OSPF_LINK_KEY: "lnk01",
          OSPF_AREA_KEY: "1", }

dict02_2 = {OSPF_IP_ADDR_KEY: "20.10.10.1", OSPF_IP_MASK_KEY: "24",
            OSPF_NETWORK_KEY: "20.10.10.1/24", OSPF_LINK_KEY: "lnk02",
            OSPF_AREA_KEY: "0", }

dict03 = {OSPF_ROUTER_KEY: "3.3.3.3",
          OSPF_IP_ADDR_KEY: "20.10.10.2", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "20.10.10.2/24", OSPF_LINK_KEY: "lnk02",
          OSPF_AREA_KEY: "0", }

dict03_2 = {OSPF_IP_ADDR_KEY: "30.10.10.1", OSPF_IP_MASK_KEY: "24",
            OSPF_NETWORK_KEY: "30.10.10.1/24", OSPF_LINK_KEY: "lnk03",
            OSPF_AREA_KEY: "2", }

dict04 = {OSPF_ROUTER_KEY: "4.4.4.4",
          OSPF_IP_ADDR_KEY: "30.10.10.2", OSPF_IP_MASK_KEY: "24",
          OSPF_NETWORK_KEY: "30.10.10.2/24", OSPF_LINK_KEY: "lnk03",
          OSPF_AREA_KEY: "2", }

# Topology 2 configs
dict1_01 = {OSPF_ROUTER_KEY: "1.1.1.1",
            OSPF_IP_ADDR_KEY: "10.10.10.1", OSPF_IP_MASK_KEY: "24",
            OSPF_NETWORK_KEY: "10.10.10.1/24", OSPF_LINK_KEY: "lnk01",
            OSPF_AREA_KEY: "0", }


dict1_02 = {OSPF_ROUTER_KEY: "2.2.2.2",
            OSPF_IP_ADDR_KEY: "10.10.10.2", OSPF_IP_MASK_KEY: "24",
            OSPF_NETWORK_KEY: "10.10.10.2/24", OSPF_LINK_KEY: "lnk01",
            OSPF_AREA_KEY: "0", }

dict1_03 = {OSPF_ROUTER_KEY: "3.3.3.3",
            OSPF_IP_ADDR_KEY: "10.10.10.3", OSPF_IP_MASK_KEY: "24",
            OSPF_NETWORK_KEY: "10.10.10.3/24", OSPF_LINK_KEY: "lnk01",
            OSPF_AREA_KEY: "0", }


# Function to enter into config mode
def enterConfigShell(dut01):
    retStruct = dut01.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    retStruct = dut01.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    return True


# If the context is not present already then it will be created
def enterRouterContext(dut01):
    if (enterConfigShell(dut01) is False):
        return False

    devIntReturn = dut01.DeviceInteract(command="router ospf")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter OSPF context"

    return True


# Function to delete router id
def delete_router_id(dut, router_id):
    if (enterRouterContext(dut) is False):
        return False

    LogOutput('info', "deleting OSPF router ID " + router_id)
    devIntReturn = dut.DeviceInteract(command="no router-id ")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set router-id failed"
    exitContext(dut)
    return True


# Function to enter into interface context
def enterInterfaceContext(dut01, interface, enable):
    if (enterConfigShell(dut01) is False):
        return False

    cmd = "interface " + str(interface)
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter Interface context"

    if (enable is True):
        dut01.DeviceInteract(command="no shutdown")
        dut01.DeviceInteract(command="no routing")

    return True


# Function to exit from context
def exitContext(dut01):
    devIntReturn = dut01.DeviceInteract(command="exit")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to exit current context"

    retStruct = dut01.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit config terminal"

    retStruct = dut01.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to exit vtysh prompt"

    return True


# Function to delete router instance
def deleteRouterInstanceTest(dut01):
    if (enterConfigShell(dut01) is False):
        return False

    devIntReturn = dut01.DeviceInteract(command="no router ospf")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to delete OSPF context failed"

    return True


# Function to configure router id
def configure_router_id(dut, router_id):
    if (enterRouterContext(dut) is False):
        return False

    LogOutput('info', "Configuring OSPF router ID " + router_id)
    devIntReturn = dut.DeviceInteract(command="router-id " + router_id)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set router-id failed"
    exitContext(dut)

    return True


# Function to configure network area for OSPF
def configure_network_area(dut01, network, area):
    if (enterRouterContext(dut01) is False):
        return False

    cmd = "network " + network + " area " + area
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Test to set network area id failed"
    exitContext(dut01)

    return True


# Function to verify if MTU was configured
def verify_mtu(switch_id, interface,  mtu):

    devIntReturn = switch_id.DeviceInteract(command="ip netns exec swns bash")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to execute command"
    cmd = "ifconfig " + interface
    devIntReturn = switch_id.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to execute command"
    matchObj = re.search(r'MTU:\d{1,4}', devIntReturn['buffer'], re.S)
    if matchObj:
        split_list = re.split(r':', matchObj.group())
        if split_list and len(split_list) > 1:
            if (str(split_list[1]) == str(mtu)):
                return True

    return False


# Function to configure MTU into the interface
def configure_mtu(dut01, interface, mtu_value):

    LogOutput('info', "Configuring mtu")
    if (enterConfigShell(dut01) is False):
        return False

    cmd = "interface " + str(interface)
    devIntReturn = dut01.DeviceInteract(command=cmd)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to enter Interface context"

    dut01.DeviceInteract(command="no shutdown")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to execute no shutdown"

    cmd1 = "mtu " + str(mtu_value)
    dut01.DeviceInteract(command=cmd1)
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to configure MTU"

    exitContext(dut01)
    return True


# This function will return buffer having tcpdump
def getTcpdump(switch_id):
    LogOutput('info', "Capturing packets through tcpdump")
    devIntReturn = switch_id.DeviceInteract(command="ip netns exec swns bash")
    retCode = devIntReturn.get('returnCode')
    assert retCode == 0, "Failed to execute command"

    devIntReturn = switch_id.DeviceInteract(command="timeout 70 tcpdump -i2\
                                            -v -XX ip proto 89")
    assert retCode == 0, "Failed to get tcpdump"
    return devIntReturn['buffer']


# Function will return neighbor list from tcpdump
def get_nbr_id_from_dump(switch_id, ip, dump_str):
    regex = ip + r' >.*Neighbor List:.*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matchObj = re.search(regex, dump_str, re.S)
    if matchObj:
        split_list = re.split(r'\s+', matchObj.group())
        if split_list:
            index = split_list.index("List:")
            return split_list[index + 1]
        else:
            return ""
    else:
        return ""


# Function to count number of router-id instance
def get_packet_count(switch_id, dump_str):
    reg_ex = r'switch\s>.*Router-ID\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matchObj = re.search(reg_ex, dump_str, re.S)
    if matchObj:
        split_list = re.split(r'\s+', matchObj.group())
        if split_list:
            count = split_list.count("Router-ID")
        else:
            count = 0
    else:
        count = 0

    return count


# Function to get Router-id of switch
def get_router_id(switch_id):
    LogOutput('info', "fetching router-id from show ip ospf")
    ospf_interface = SwitchVtyshUtils.vtysh_cmd(switch_id, "show ip ospf")
    matchObj = re.search(r'Router\sID:\s\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
                         ospf_interface)
    if matchObj:
        split_list = re.split(r'\s+', matchObj.group())
        if split_list and len(split_list) > 2:
            return split_list[2]

    return ""


# Function to get ospf states
def verify_ospf_states(dut):
    LogOutput('info', "fetching states of the router")
    ospf_interface = SwitchVtyshUtils.vtysh_cmd(dut, "show ip\
                                                    ospf interface")
    matchObj = re.search(r'State\s<.*>', ospf_interface)
    if matchObj:
        split_list = re.split(r'\s+', matchObj.group())
        if "Backup>" in split_list:
            return "DRBackup"
        elif "Other>" in split_list:
            return "DROther"
        elif "<DR>" in split_list:
            return "DR"

    return ""


# Test case to verify that the neighbors are discovered
def verify_ospf_adjacency(dut01, dut02_router_id, print_nbrs=False):
    neighbors = SwitchVtyshUtils.vtysh_cmd(dut01, "show ip ospf neighbor")

    if print_nbrs:
        info("%s\n" % neighbors)

    nbrs = neighbors.split(VTYSH_CR)
    nbr_id = dut02_router_id + " "
    for nbr in nbrs:
        if nbr_id in nbr:
            return True

    return False


# Function to get the dead interval and hello timer value
def getTimers(dut02, timer_type):
    ospf_interface = SwitchVtyshUtils.vtysh_cmd(dut02, "show\
                                                        ip ospf interface")

    if "Dead" in timer_type:
        matchObj = re.search(r'Dead\s\d+', ospf_interface)
    elif "Hello" in timer_type:
        matchObj = re.search(r'Hello\s\d+', ospf_interface)

    if matchObj:
        timers = re.split(r'\s+', matchObj.group())
        if timers and len(timers) > 1:
            timer = timers[1]
        else:
            timer = 0
    else:
        timer = 0

    return timer


# Function to get states of neighbor (down/init/
# 2-way, Exstart, Exchange, Loading and Full
def get_neighbor_state(dut):
    neighbors = SwitchVtyshUtils.vtysh_cmd(dut, "show ip ospf neighbor")
    split_list = re.split(r'\s+', neighbors)
    if split_list and len(split_list) > 20:
        state = split_list[20].split("/")
        return state[0]

    return False


# Function to wait until 2-Way or greater state
def wait_for_2way_state(dut):

    hello_time = getTimers(dut, "Hello")
    wait_time = int(hello_time) + 20
    for i in range(wait_time):
        state = get_neighbor_state(dut)
        if (state == "ExStart" or state == "Exchange" or state ==
                "Loading" or state == "Full"):
            return True
        else:
            sleep(1)

    info("### Condition not met after %s seconds ###\n" %
         wait_time)

    return False


# Function to wait for adjacency establishment
def wait_for_adjacency(dut01, dut02_router_id, condition=True,
                       print_nbrs=False):
    hello_time = getTimers(dut01, "Hello")
    wait_time = int(hello_time) + 50
    for i in range(wait_time):
        found = verify_ospf_adjacency(dut01, dut02_router_id, print_nbrs)
        if found == condition:
            return found

        sleep(1)

    info("### Condition not met after %s seconds ###\n" %
         wait_time)

    return found


# Function to configure OSPF
def configure(dict):

    # - Configures the IP address
    # - Creates router ospf instances
    # - Configures the router id
    # - Configures the network range and area

    # - Enable the link.
    # - Set IP for the switches.
    # Enabling interface

    if OSPF_DUT_OBJ in dict:
        switch = dict[OSPF_DUT_OBJ]
        if (not switch):
            assert "No Object to configure"
            return

    if OSPF_LINK_KEY in dict:
        link = dict[OSPF_LINK_KEY]
        info_str = "Enabling " + link + " on " + str(switch)
        LogOutput('info', info_str)
        interface_value = switch.linkPortMapping[str(link)]
        retStruct = InterfaceEnable(deviceObj=switch,
                                    enable=True,
                                    interface=interface_value)
        retCode = retStruct.returnCode()
        if retCode != 0:
            assert_msg = "Unable to enable " + interface_value
            " on " + str(switch)
            assert assert_msg

        # Assigning an IPv4 address on interface
        if OSPF_IP_ADDR_KEY and OSPF_IP_MASK_KEY in dict:
            ipAddr = dict[OSPF_IP_ADDR_KEY]
            ipMask = dict[OSPF_IP_MASK_KEY]
            interface_value = switch.linkPortMapping[str(link)]
            info_str = str(link) + " of " + str(switch)
            LogOutput('info', "Configuring ip adddress on " + info_str)
            retStruct = InterfaceIpConfig(deviceObj=switch,
                                          interface=interface_value,
                                          addr=ipAddr, mask=ipMask,
                                          config=True)
            retCode = retStruct.returnCode()
            if retCode != 0:
                assert "Failed to configure an IPv4 address on interface "

    # For all the switches
    # - Create the instance.
    # - Configure the router Id.
    # - Configure network area.

    if OSPF_ROUTER_KEY in dict:
        routerId = dict[OSPF_ROUTER_KEY]
        result = configure_router_id(switch, routerId)
        assert result is True, "OSPF router id set failed"

    if OSPF_NETWORK_KEY and OSPF_AREA_KEY in dict:
        network = dict[OSPF_NETWORK_KEY]
        area = dict[OSPF_AREA_KEY]
        info_str = "configuring network " + network + " for area " + area
        LogOutput('info', info_str)
        result = configure_network_area(switch, network, area)
        assert result is True, "OSPF network creation failed"


# Tcpdump is currently not running on VSI image due to
# tcpdump_apparmor_profile [/etc/apparmor.d/usr.sbin.tcpdump] file,
# which is present on running host machine[VM].
# The Profile files will declare access rules to allow access to
# linux system resources. Implicitly the access is denied
# when there is no matching rule in the profile.
# If we want to run docker instance with tcpdump on such a
# host machine, we have to disable the tcpdump_apparmor_profile file
# and enable it once testcase execution is finished.
def disable_tcpdump_profile():
    if os.path.isfile("/etc/apparmor.d/usr.sbin.tcpdump") is True and \
            not os.path.isfile("/etc/apparmor.d/disable/usr.sbin.tcpdump"):
        os.system("sudo ln -s /etc/apparmor.d/usr.sbin.tcpdump "
                  "  /etc/apparmor.d/disable/")
        os.system('sudo apparmor_parser -R '
                  '/etc/apparmor.d/usr.sbin.tcpdump')


def enable_tcpdump_profile():
    if os.path.isfile("/etc/apparmor.d/usr.sbin.tcpdump") is True and \
            os.path.isfile("/etc/apparmor.d/disable/usr.sbin.tcpdump"):
        os.system('sudo rm /etc/apparmor.d/disable/usr.sbin.tcpdump')
        os.system('sudo apparmor_parser -r '
                  '/etc/apparmor.d/usr.sbin.tcpdump')

        os.system('sudo rm /etc/apparmor.d/disable/usr.sbin.tcpdump')
        os.system('sudo apparmor_parser -r /etc/apparmor.d/usr.sbin.tcpdump')


# When we run this test file with multiple instance,there is a chance of
# asynchronously enabling and disabling tcpdump_profile file on the
# running system.
# To avoid asynchronous issue, the count variable is used to maintain
# the number of ospf test file execution instance in a temp file.
# whenever the count reaches zero, the profile file is enabled again.
def file_read_instance_count():
    file_fd = open('ospf_sys_var', 'r')
    count = file_fd.read()
    count = re.search('\d+', count)
    num = int(count.group(0))
    file_fd.close()
    return num


def file_write_instance_count(count_number):
    file_fd = open('ospf_sys_var', 'w+')
    file_fd.write(str(count_number))
    file_fd.close()


def setup_profile():
    if os.path.exists('ospf_sys_var') is False:
        file_write_instance_count(0)
    else:
        count = file_read_instance_count()
        num = count + 1
        file_write_instance_count(num)

    disable_tcpdump_profile()


def Revert_profile():
    Enable = False

    if os.path.exists('ospf_sys_var') is True:
        num = file_read_instance_count()
        if num == 0:
            Enable = True
        else:
            num = num - 1
            file_write_instance_count(num)

    # Enabling tcpdump.profile on VM.
    if Enable is True:
        enable_tcpdump_profile()
        os.system('rm ospf_sys_var')

@pytest.mark.skipif(True, reason="Skipping due to Taiga ID : 769")
class Test_ospf_configuration:

    # Global variables
    dut01Obj = None
    dut02Obj = None
    dut03Obj = None
    dut04Obj = None

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_ospf_configuration.testObj = testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_ospf_configuration.topoObj = \
            Test_ospf_configuration.testObj.topoObjGet()

        # Global variables
        global dut01Obj
        global dut02Obj
        global dut03Obj
        global dut04Obj
        dut01Obj = cls.topoObj.deviceObjGet(device="dut01")
        dut02Obj = cls.topoObj.deviceObjGet(device="dut02")
        dut03Obj = cls.topoObj.deviceObjGet(device="dut03")
        dut04Obj = cls.topoObj.deviceObjGet(device="dut04")

        # Setup the profile status
        setup_profile()

    def teardown_class(cls):
        Test_ospf_configuration.topoObj.terminate_nodes()
        # Revert back the changes made regarding the profiles
        Revert_profile()

    # Verifying that the dynamic router id is selected
    def test_dynamic_router_id(self):
        LogOutput('info', "****** Verifying that dynamic router "
                  "ID is selected*****")

        dict = {OSPF_DUT_OBJ: dut01Obj,
                OSPF_IP_ADDR_KEY: "10.10.10.1", OSPF_IP_MASK_KEY: "24",
                OSPF_NETWORK_KEY: "10.10.10.1/24", OSPF_LINK_KEY: "lnk01",
                OSPF_AREA_KEY: "1", }

        LogOutput('info', "Step 1 - Configure switch1 and switch2")
        configure(dict)
        OSPF_ROUTER_ID_DUT1 = "10.10.10.1"
        OSPF_ROUTER_ID_DUT2 = "10.10.10.2"

        dict = {OSPF_DUT_OBJ: dut02Obj,
                OSPF_IP_ADDR_KEY: "10.10.10.2", OSPF_IP_MASK_KEY: "24",
                OSPF_NETWORK_KEY: "10.10.10.2/24", OSPF_LINK_KEY: "lnk01",
                OSPF_AREA_KEY: "1"}
        configure(dict)

        LogOutput('info', "Step 2 - Waiting for adjacency")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        LogOutput('info', "Step 3 - verify hello packets are exchanged")
        dump_str = getTcpdump(dut01Obj)
        count = get_packet_count(dut01Obj, dump_str)
        if (count > 1):
            LogOutput('info', "Hello packets exchanged periodically")
        else:
            LogOutput('info', "**** Packet Captured **** %s" % dump_str)
            assert False, "Failed to exchange hello packets"

        LogOutput('info', "****** Verifying that dynamic router ID is "
                          "selected - Passed *****")

    # Verifying that the router id configured
    # in router context is selected
    def test_router_id_in_router_context_selected(self):
        LogOutput('info', "***** Verifying that the router id configured"
                  "in router context is selected ******")

        dict_01 = {OSPF_DUT_OBJ: dut01Obj, OSPF_ROUTER_KEY: "1.1.1.1", }
        dict_02 = {OSPF_DUT_OBJ: dut02Obj, OSPF_ROUTER_KEY: "2.2.2.2", }

        LogOutput('info', "Step 1 - Configure switch1 and switch2")

        configure(dict_01)
        configure(dict_02)

        LogOutput('info', "Step 2 - Waiting for adjacency")
        retVal = wait_for_adjacency(dut01Obj, dict_02[OSPF_ROUTER_KEY])
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % dict_02[OSPF_ROUTER_KEY])
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % dict_02[OSPF_ROUTER_KEY]

        LogOutput('info', "Step 3 - verify router ID"
                  " using show ip ospf command")
        router_id = get_router_id(dut01Obj)
        if dict_01[OSPF_ROUTER_KEY] in router_id:
            LogOutput('info', "Router-id is verfied for switch")
        else:
            LogOutput('info', "Router-id verification failed")
            assert "Router-id verification failed"

        dump_str = getTcpdump(dut01Obj)
        LogOutput('info', "Step 4 - verify router ID"
                  " using hello packets")
        neighbor_id = get_nbr_id_from_dump(dut01Obj,
                                           str(dict02[OSPF_IP_ADDR_KEY]),
                                           dump_str)
        if (neighbor_id == dict_01[OSPF_ROUTER_KEY]):
            LogOutput('info', "Router-id found in hello packet")
        else:
            LogOutput('info', "Router-id not seen in hello packet")
            LogOutput('info', "**** Packet Captured **** %s" % dump_str)
            assert "Router-id not seen in hello packet"

        LogOutput('info', "****** Passed ******")

    # Latest router-id  configured should be retained
    # when instance level router-id is removed
    def test_dynamic_router_selection(self):
        LogOutput('info', "***** Latest router-id  configured should be"
                  " retained when instance level router-id is removed*****")

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]

        LogOutput('info', "Step 1 - Removing instance level router-id in SW1")
        delete_router_id(dut01Obj, OSPF_ROUTER_ID_DUT1)

        LogOutput('info', "Step 2 - Waiting for adjacency")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        dump_str = getTcpdump(dut01Obj)
        neighbor_id = get_nbr_id_from_dump(dut01Obj,
                                           str(dict02[OSPF_IP_ADDR_KEY]),
                                           dump_str)

        LogOutput('info', "Step 3 - verify router ID"
                  " through hello packet in tcp-dump")
        if neighbor_id == OSPF_ROUTER_ID_DUT1:
            LogOutput('info', "Static Router-id found in hello packet")
        else:
            LogOutput('info', "**** Packet Captured **** %s" % dump_str)
            assert False, "Static router-id not found in hello packet"

        LogOutput('info', "****** Passed ******")

    # Test case to verify that the
    #  hello packets are exchanged periodically and neighbors are discovered
    def test_verify_hello_packets_exchanged(self):
        LogOutput('info', "***** Verifying that the hello packets are "
                  "exchanged periodically ******")

        dict02_2[OSPF_DUT_OBJ] = dut02Obj
        dict03[OSPF_DUT_OBJ] = dut03Obj
        dict03_2[OSPF_DUT_OBJ] = dut03Obj
        dict04[OSPF_DUT_OBJ] = dut04Obj

        LogOutput('info', "Step 1 - Configure switch1, switch2, switch3"
                  " and switch4")

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        configure(dict02_2)
        configure(dict03)
        configure(dict03_2)
        configure(dict04)

        LogOutput('info', "Step 2 - verify count of hello packets")
        dump_str = getTcpdump(dut01Obj)
        count = get_packet_count(dut01Obj, dump_str)
        if (count > 1):
            LogOutput('info', "Hello packets exchanged periodically")
        else:
            LogOutput('info', "Hello packets are not exchanged")
            LogOutput('info', "**** Packet Captured **** %s" % dump_str)
            assert "Hello packets are not exchanged"

        LogOutput('info', "Step 3 - verify router ID of switch1"
                  " in hello packet received from switch2")

        neighbor_id = get_nbr_id_from_dump(dut01Obj,
                                           str(dict02[OSPF_IP_ADDR_KEY]),
                                           dump_str)
        if (neighbor_id == OSPF_ROUTER_ID_DUT1):
            LogOutput('info', "Router-id found in hello packet")
        else:
            LogOutput('info', "Router-id not seen in hello packet")
            LogOutput('info', "**** Packet Captured **** %s" % dump_str)
            assert "Router-id not seen in hello packet"

        LogOutput('info', "Step 4 - verify adjacency is formed")
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]

        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut03Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW3 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW3 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        LogOutput('info', "****** Passed ******")

    # Test case to verify that neighbor adjacency
    # is torn when one of the neighbor goes down
    def test_adjacency_by_disabling_interface(self):

        LogOutput('info', "****** Verifying that neighbor adjacency "
                  "is torn when one of the neighbor goes down*****")

        LogOutput('info', "Step 1 - Configure switch1, switch2, switch3"
                  " and switch4")
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT3 = dict03[OSPF_ROUTER_KEY]

        LogOutput('info', "Step 2 - Wait for adjacency")
        # Give some time for the IFSM to establish states
        sleep(10)
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1)
        if retVal:
            LogOutput('info', "Adjacency formed in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
        else:
            assert False, "Adjacency not formed in SW2 with SW1(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT1

        retVal = wait_for_adjacency(dut03Obj, OSPF_ROUTER_ID_DUT2)
        if retVal:
            LogOutput('info', "Adjacency formed in SW3 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW3 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        LogOutput('info', "Step 3 - Disable interface between "
                  "switch2 and switch3 in switch2")
        interface_value = dut02Obj.linkPortMapping["lnk02"]
        info_str = interface_value + " on " + str(dut01Obj)
        LogOutput('info', "Disabling interface " + info_str)
        retStruct = InterfaceEnable(deviceObj=dut02Obj, enable=False,
                                    interface=interface_value)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Unable to disable %s" % interface_value

        LogOutput('info', "Step 4 - Check adjacency in switch1,"
                  " switch2 and switch3")
        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1)
        if retVal:
            LogOutput('info', "Adjacency formed in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
        else:
            assert False, "Adjacency not formed in SW2 with SW1(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT1

        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT3, False)
        if retVal is False:
            LogOutput('info', "Adjacency torn in SW2 with SW3 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT3)
        else:
            assert False, "Adjacency not torn in SW2 with SW3(Router-id % s)" \
                          % OSPF_ROUTER_ID_DUT3

        LogOutput('info', "****** Passed ******")

    # Test case to verify that neighbor adjacency
    # is torn when ospfv2 is disabled in one of the switches
    def test_adjacency_by_deleting_instance(self):
        LogOutput('info', "***** Verifying that neighbor adjacency"
                  " is torn when ospfv2 is disabled in one"
                  " of the switch*****")

        LogOutput('info', "Step 1 - Configure switch1, switch2, switch3"
                  " and switch4")

        interface_value = dut02Obj.linkPortMapping["lnk02"]
        retStruct = InterfaceEnable(deviceObj=dut02Obj, enable=True,
                                    interface=interface_value)
        retCode = retStruct.returnCode()
        assert retCode == 0, "Unable to enable %s" % interface_value

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT3 = dict03[OSPF_ROUTER_KEY]

        configure_router_id(dut01Obj, OSPF_ROUTER_ID_DUT1)

        LogOutput('info', "Step 2 - Wait for adjacency")
        retVal = wait_for_adjacency(dut03Obj, OSPF_ROUTER_ID_DUT2)
        if retVal:
            LogOutput('info', "Adjacency formed in SW3 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW3 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        retVal = wait_for_adjacency(dut04Obj, OSPF_ROUTER_ID_DUT3)
        if retVal:
            LogOutput('info', "Adjacency formed in SW4 with SW3 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT3)
        else:
            assert False, "Adjacency not formed in SW4 with SW3(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT3

        LogOutput('info', "Step 3 - Delete switch3 instance")
        retVal = deleteRouterInstanceTest(dut03Obj)
        assert retVal is True, "Failed to delete Router instance"

        LogOutput('info', "Step 4 - Check for adjacency in Switch 1,"
                  " switch 2 and switch 3")
        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT1)
        if retVal:
            LogOutput('info', "Adjacency torn in SW2 with SW1 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT1)
        else:
            assert False, "Adjacency not torn in SW1 with"
            " SW2(Router-id % s)" % OSPF_ROUTER_ID_DUT1

        retVal = wait_for_adjacency(dut02Obj, OSPF_ROUTER_ID_DUT3, False)
        if retVal is False:
            LogOutput('info', "Adjacency torn in SW2 with SW3 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT3)
        else:
            assert False, "Adjacency not torn in SW2 with"
            "SW3(Router-id % s)" % OSPF_ROUTER_ID_DUT3

        LogOutput('info', "****** Passed ******")

    # Test case to verify neighbor state is updated
    # when MTU mismatches
    def test_verify_mtu_mismatch(self):
        LogOutput('info', "***** Test case to verify that neighbor"
                  " state is changed when MTU mismatches")

        LogOutput('info', "Step 1 - Configure switch1, switch2 and switch3"
                  " switch4")

        OSPF_ROUTER_ID_DUT1 = dict01[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT2 = dict02[OSPF_ROUTER_KEY]
        OSPF_ROUTER_ID_DUT3 = dict03[OSPF_ROUTER_KEY]
        configure(dict03)
        configure(dict03_2)

        LogOutput('info', "Step 2 - Wait for adjacency")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        LogOutput('info', "Step 3 - Configuring MTU")

        link = dict01[OSPF_LINK_KEY]
        interface_value = dut01Obj.linkPortMapping[str(link)]
        retVal = configure_mtu(dut01Obj, interface_value, "1200")
        if retVal:
            LogOutput('info', "Step 4 - verifying MTU")
            retVal = verify_mtu(dut01Obj, interface_value, 1200)
            if retVal:
                LogOutput('info', "MTU verified")
            else:
                assert False, "Failed to set MTU"
        else:
            assert False, "Failed to set MTU"

        LogOutput('info', "Step 5 - Wait for state update")
        hello_time = getTimers(dut01Obj, "Hello")
        wait_time = int(hello_time) + 20
        for i in range(wait_time):
            state = get_neighbor_state(dut01Obj)
            if (state == "ExStart"):
                LogOutput('info', "Switch2 in correct state")
                break
            else:
                sleep(1)

        assert state == "ExStart", "Switch2 not in correct state"
        LogOutput('info', "****** Passed ******")


@pytest.mark.skipif(True, reason="Skipping due to Taiga ID : 769")
class Test_ospf_configuration_l2switch:

    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_ospf_configuration_l2switch.testObj = \
            testEnviron(topoDict=topoDict1)
        #    Get topology object
        Test_ospf_configuration_l2switch.topoObj = \
            Test_ospf_configuration_l2switch.testObj.topoObjGet()

    def teardown_class(cls):
        Test_ospf_configuration_l2switch.topoObj.terminate_nodes()

    def test_dr_bdr_selection(self):
        LogOutput('info', "***** Test case to verify "
                  "that the DR and BDR is selected")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut04Obj = self.topoObj.deviceObjGet(device="dut04")
        dict1_01[OSPF_DUT_OBJ] = dut01Obj
        dict1_02[OSPF_DUT_OBJ] = dut02Obj
        dict1_03[OSPF_DUT_OBJ] = dut03Obj

        LogOutput('info', "Step 1 - configuring SW1, SW2 and SW3")
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        configure(dict1_01)

        OSPF_ROUTER_ID_DUT2 = dict1_02[OSPF_ROUTER_KEY]
        configure(dict1_02)

        configure(dict1_03)

        # DUT04 is Layer 2 switch hence we are configuring
        # no routing on interfaces
        LogOutput('info', "****** Configure Switch4 interfaces"
                  " with (no routing)  *******")
        enterInterfaceContext(dut04Obj, 1, True)
        enterInterfaceContext(dut04Obj, 2, True)
        enterInterfaceContext(dut04Obj, 3, True)
        exitContext(dut04Obj)
        LogOutput('info', "****** Configure Switch4 interfaces"
                  " with (no routing) finished *******")

        LogOutput('info', "Step 2 - Waiting for adjacency")

        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        LogOutput('info', "Step 3 - Verifying states of switches")
        dr_present = False
        bdr_present = False
        dr_other_present = False
        retVal = wait_for_2way_state(dut02Obj)
        if retVal:
            state = verify_ospf_states(dut01Obj)
            if (state == "DRBackup"):
                LogOutput('info', "Switch1 in DRBackup state")
                bdr_present = True
            elif (state == "DR"):
                LogOutput('info', "Switch1 in DR state")
                dr_present = True
            elif (state == "DROther"):
                LogOutput('info', "Switch1 in DROther state")
                dr_other_present = True
            else:
                LogOutput('info', "Switch1 is not in correct state")
                assert False, "Switch1 is not in correct state"
        else:
            assert False, "Switch1 not in correct state"

        retVal = wait_for_2way_state(dut01Obj)
        if retVal:
            state = verify_ospf_states(dut02Obj)
            if (state == "DRBackup"):
                LogOutput('info', "Switch2 in DRBackup state")
                bdr_present = True
            elif (state == "DR"):
                LogOutput('info', "Switch2 in DR state")
                dr_present = True
            elif (state == "DROther"):
                LogOutput('info', "Switch2 in DROther state")
                dr_other_present = True
            else:
                LogOutput('info', "Switch2 is not in correct state")
                assert False, "Switch1 is not in correct state"
        else:
            assert False, "Switch2 not in correct state"

        retVal = wait_for_2way_state(dut02Obj)
        if retVal:
            state = verify_ospf_states(dut03Obj)
            if (state == "DRBackup"):
                LogOutput('info', "Switch3 in DRBackup state")
                bdr_present = True
            elif (state == "DR"):
                LogOutput('info', "Switch3 in DR state")
                dr_present = True
            elif (state == "DROther"):
                LogOutput('info', "Switch3 in DROther state")
                dr_other_present = True
            else:
                LogOutput('info', "Switch3 is not in correct state")
                assert False, "Switch1 is not in correct state"
        else:
            assert False, "Switch3 not in correct state"

        LogOutput('info', "Step 4 - Verifying dr, bdr and drother "
                          "were present in the topology")
        if (dr_present is False) and (bdr_present is False) and \
                (dr_other_present is False):
            assert False, "DR/BDR election failed"
        LogOutput('info', "****** Passed ******")

    def test_dr_bdr_change_with_routerid(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        dut02Obj = self.topoObj.deviceObjGet(device="dut02")
        dut03Obj = self.topoObj.deviceObjGet(device="dut03")
        dut04Obj = self.topoObj.deviceObjGet(device="dut04")
        dict1_01[OSPF_DUT_OBJ] = dut01Obj
        dict1_02[OSPF_DUT_OBJ] = dut02Obj
        dict1_03[OSPF_DUT_OBJ] = dut03Obj

        # changing router-id of dut01 to verify DR/BDR/DROther election
        LogOutput('info', "***** Test case to verify that the DR"
                  " election is triggered when router ids are changed.")

        LogOutput('info', "Step 1 - Changing router-id of SW1 from 1.1.1.1"
                  " to 5.5.5.5.")
        dict1_01[OSPF_ROUTER_KEY] = "5.5.5.5"

        configure(dict1_01)
        OSPF_ROUTER_ID_DUT2 = dict1_02[OSPF_ROUTER_KEY]

        LogOutput('info', "Step 2 - Waiting for adjacency")
        retVal = wait_for_adjacency(dut01Obj, OSPF_ROUTER_ID_DUT2, True)
        if retVal:
            LogOutput('info', "Adjacency formed in SW1 with SW2 (Router-id %s)"
                      % OSPF_ROUTER_ID_DUT2)
        else:
            assert False, "Adjacency not formed in SW1 with SW2(Router-id %s)"\
                % OSPF_ROUTER_ID_DUT2

        LogOutput('info', "Step 3 - Verfiying states of switches")
        retVal = wait_for_2way_state(dut02Obj)
        if retVal:
            state = verify_ospf_states(dut01Obj)
            if (state == "DR") or (state == "DRBackup") or \
                    (state == "DROther"):
                LogOutput('info', "Switch1 in %s state" % state)
            else:
                LogOutput('info', "Switch1 not in correct state, state = %s"
                          % state)
                assert False, "Switch1 not in correct state"
        else:
            assert False, "Switch1 not in correct state"

        retVal = wait_for_2way_state(dut01Obj)
        if retVal:
            state = verify_ospf_states(dut02Obj)
            if (state == "DR") or (state == "DRBackup") or \
                    (state == "DROther"):
                LogOutput('info', "Switch2 in %s state" % state)
            else:
                LogOutput('info', "Switch2 not in correct state")
                assert False, "Switch2 not in correct state, state = %s" \
                              % state
        else:
            assert False, "Switch2 not in correct state"

        retVal = wait_for_2way_state(dut02Obj)
        if retVal:
            state = verify_ospf_states(dut03Obj)
            if (state == "DR") or (state == "DRBackup") or \
                    (state == "DROther"):
                LogOutput('info', "Switch3 in %s state" % state)
            else:
                LogOutput('info', "Switch3 not in correct state")
                assert False, "Switch3 not in correct state, state = %s" \
                              % state
        else:
            assert False, "Switch3 not in correct state"

        LogOutput('info', "****** Passed ******")
