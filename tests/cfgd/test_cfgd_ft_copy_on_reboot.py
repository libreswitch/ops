#!/usr/bin/python
# (C) Copyright 2015 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
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

import os
import sys
import time
#import json
#import subprocess

if 'BUILD_ROOT' in os.environ:
    BUILD_ROOT = os.environ['BUILD_ROOT']
else:
    BUILD_ROOT = "../../.."

OPS_VSI_LIB = BUILD_ROOT + "/src/ops-vsi"
sys.path.append(OPS_VSI_LIB)

import mininet
from opsvsi.docker import *
from opsvsi.opsvsitest import *


#OVS_VSCTL = "/usr/bin/ovs-vsctl "

ALL_DAEMONS = "ops-sysd ops-pmd ops-tempd ops-powerd ops-ledd ops-fand"\
              " switchd ops-intfd ops-vland ops-lacpd"\
              " ops-lldpd ops-zebra ops-bgpd ovsdb-server"

PLATFORM_DAEMONS = "ops-sysd ops-pmd ops-tempd ops-powerd ops-ledd ops-fand"

CREATE_OVSDB_CMD = "/usr/bin/ovsdb-tool create /var/run/openvswitch/ovsdb.db"\
                   " /usr/share/openvswitch/vswitch.ovsschema"

CREATE_CONFIGDB_CMD = "/usr/bin/ovsdb-tool create /var/local/openvswitch/"\
                      "config.db /usr/share/openvswitch/configdb.ovsschema"

OVSDB_STARTUP_CMD_NORMAL = "/usr/sbin/ovsdb-server --remote=punix:/var/run/"\
                           "openvswitch/db.sock --detach --no-chdir --pidfile"\
                           " -vSYSLOG:INFO /var/run/openvswitch/ovsdb.db "\
                           "/var/local/openvswitch/config.db"

OVSDB_STARTUP_CMD_NO_CONFIGDB = "/usr/sbin/ovsdb-server --remote=punix:/var/"\
                                "run/openvswitch/db.sock --detach --no-chdir"\
                                " --pidfile -vSYSLOG:INFO "\
                                "/var/run/openvswitch/ovsdb.db"

OVSDB_STOP_CMD = "kill -9 `cat /var/run/openvswitch/ovsdb-server.pid`"
CFGD_CMD = "/usr/bin/ops_cfgd"
CFGD_DAEMON = "cfgd"
CFG_TBL_NOT_FOUND_MSG = "No rows found in the config table"
CFG_DATA_FOUND_MSG = "Config data found"
CUR_CFG_SET_MSG = "cur_cfg already set"
OVSDB = "/var/run/openvswitch/ovsdb.db"
CONFIGDB = "/var/local/openvswitch/config.db"
OVSDB_CLIENT_TRANSACT_CMD = "/usr/bin/ovsdb-client -v transact "
ADD_STARTUP_ROW_FILE = "./src/ops-cfgd/tests/add_startup_row"
ADD_TEST_ROW_FILE = "./src/ops-cfgd/tests/add_test_row"
GET_SYSTEM_TABLE_CMD = "ovs-vsctl list system"

'''
For now, only one function by the name of test is supported. To enable
multiple tests I wrote separate functions for each test and call them from the
main test function.
'''


class cfgdTest(OpsVsiTest):
    def setupNet(self):
        # if you override this function, make sure to
        # either pass getNodeOpts() into hopts/sopts of the topology that
        # you build or into addHost/addSwitch calls
        self.net = Mininet(topo=SingleSwitchTopo(
            k=1,
            hopts=self.getHostOpts(),
            sopts=self.getSwitchOpts()),
            switch=VsiOpenSwitch,
            host=Host,
            link=OpsVsiLink,
            controller=None,
            build=True)

    def stop_daemon(self, switch, daemon):
        out = switch.cmd("/bin/systemctl stop " + daemon)
        out += switch.cmd("echo")
        debug(out)

    def start_daemon(self, switch, daemon):
        out = switch.cmd("/bin/systemctl start " + daemon)
        out += switch.cmd("echo")
        debug(out)

    def status_daemon(self, switch, daemon):
        out = switch.cmd("/bin/systemctl status " + daemon + " -l")
        out += switch.cmd("echo")
        return out

    def remove_db(self, switch, db):
        debug(switch.cmd("/bin/rm -f " + db))

    def create_db(self, switch, db):
        debug(switch.cmd(db))

    def rebuild_dbs(self, switch):
        debug(self.remove_db(switch, OVSDB))
        debug(self.create_db(switch, CREATE_OVSDB_CMD))
        #debug(self.remove_db(switch, CONFIGDB))
        debug(self.create_db(switch, CREATE_CONFIGDB_CMD))

    def chk_cur_next_cfg(self, switch):
        table_out = switch.cmd(GET_SYSTEM_TABLE_CMD)
        table_out += switch.cmd("echo")
        mylines = table_out.splitlines()

        found_cur = False
        found_next = False
        for x in mylines:
            pair = x.split(':')
            if "cur_cfg" in pair[0]:
                if int(pair[1]) > 0:
                    found_cur = True
            elif "next_cfg" in pair[0]:
                if int(pair[1]) > 0:
                    found_next = True

        return found_cur and found_next

    def restart_system(self, switch, option):
        # Stop all daemons
        self.stop_daemon(switch, ALL_DAEMONS)

        # stop any manually started ovsdb-server
        debug(switch.cmd(OVSDB_STOP_CMD))

        # remove and recreate the dbs
        self.rebuild_dbs(switch)

        # start ovsdb-server with or without configdb
        if (option == "noconfig"):
            debug(switch.cmd(OVSDB_STARTUP_CMD_NO_CONFIGDB))
        else:
            debug(switch.cmd(OVSDB_STARTUP_CMD_NORMAL))
        time.sleep(0.2)

        # start the platform daemons
        self.start_daemon(switch, PLATFORM_DAEMONS)
        time.sleep(0.1)

    def copy_startup_to_running_on_bootup(self):
        info("\n########## Test to copying startup to "
             "running config on bootup #########")
        switch = self.net.switches[0]

        # Change hostname as CT-TEST in running db and copy the running
        # configuration to startup config. Now restart the system and
        # verify that the hostname is configured correctly during bootup

        switch.cmdCLI("configure terminal")
        switch.cmdCLI("hostname CT-TEST")
        switch.cmdCLI("exit")
        switch.cmdCLI("copy running-config startup-config")
        sleep(5)
        output = switch.cmdCLI("show running-config")
        output += switch.cmdCLI("end")
        debug(output)

        output = switch.cmdCLI("show startup-config")
        output += switch.cmdCLI("end")
        debug(output)

        self.restart_system(switch, "normal")
        sleep(10)

        # Run ops_cfgd
        out = self.start_daemon(switch, CFGD_DAEMON)
        debug(out)
        sleep(10)

        out = self.status_daemon(switch, CFGD_DAEMON)
        debug(out)

        output = switch.cmdCLI("show running-config")
        output += switch.cmdCLI("end")
        debug(output)

        if "hostname CT-TEST" in output:
            info("\n### Passed: copy running to startup"
                 " configuration on bootup ###")
        else:
            assert("hostname CT-TEST" in output), \
                "Failed: copy running to startup configuration on bootup"

        #info("\n########## Test to verify cur_cfg and "
        #    "next_cfg set > 0 #########")

        # Get the contents of the System table
        if not self.chk_cur_next_cfg(switch):
            assert(self.chk_cur_next_cfg(switch)), \
                "Failed:cur/next cfg not properly set"
        else:
            info("\n### Passed: cur_cfg, next_cfg properly set ###\n")

@pytest.mark.skipif(True, reason="Skipping temporarily due to defect #2084")
class Test_cfgdTest:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_cfgdTest.test = cfgdTest()
        pass

    def teardown_class(cls):
    # Stop the Docker containers, and
    # mininet topology
        Test_cfgdTest.test.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test

    def test_copy_startup_to_running_on_bootup(self):
        self.test.copy_startup_to_running_on_bootup()
