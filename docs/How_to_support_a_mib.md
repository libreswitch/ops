How to support a MIB for a feature
====
Contents
---
- [Location of SNMP infrastructure and MIB files](#location-of-snmp-infrastructure-and-mib-files)
- [Feature developer workflow](#feature-developer-workflow)
- [References](#references)

Location of SNMP infrastructure and MIB files
---------------------------------------------
This document explains how to support a MIB database for a feature using the SNMP infrastructure available in OPS. The infrastructure resides in the **ops-snmpd** repository.
The MIB feature resides in the feature repository under the *src/snmp/* directory, and includes the dependency MIBs. Some commonly used MIBs are included in the *ops-snmpd* repository under the *netsnmp/mibs* directory. In the case of a new MIB or a modified MIB, smilint is run to check for semantics and syntax errors.
MIBs can be compiled at any place provided the right path to a MIB is mentioned. The file is generated under the users directory at `/users/`*`user-name`*`/pysnmp/mibs/`. The *libsmi* package provides smilint.
```
wget https://www.ibr.cs.tu-bs.de/projects/libsmi/download/libsmi-0.4.8.tar.gz
tar -evf libsmi-0.4.8.tar.gz
smilint -l 6 MIB file
```
Feature developer workflow
--------------------------
An MIB represents a certain data format. The objects in the OVSDB represent a different data format. To support read operations on a given MIB, it is necessary to map the MIB objects to specific schema objects. The SNMP infrastructure requires a "mapping file" which in its simplest form could be thought of as a two column table where the first column would be a MIB object and the second column is its corresponding OVSDB schema object. The feature owner or developer is required to provide this mapping. Every feature implementing SNMP using this infra needs the *python Lex-Yacc (Ply)* package.
To install the *python Lex-Yacc (Ply)* package:
```
pip install ply
```
1. Understand the one to one (1:1) mapping between the MIB feature and the schema,  and write a JSON file.
The JSON file format follows:
	- **MIBtype**--The MIB object type (scalar/tabular/trap)
	- **OvsTable**--Corresponding schema table for the MIB object. It is *null* if there is no one to one (1:1) mapping for the MIB object.
	- **OvsColumn**--Column in the schema table. It is *null* if there is no one to one (1:1) mapping for the MIB object.
	- **Key**--MIB object schema key. It is *null* if the MIB object is the value of a column and not a key-value pair,  or if there is no one to one (1:1) mapping for the MIB object.
	- **CustomFunction**--Specifies a function name which the developer may need to define in case of a mismatch between the MIB data type and the corresponding schema data type. This function can also be modified to return a default value for an MIB object in case there is no schema equivalent for that MIB object.
To illustrate this better, consider the following MIB object which is a scalar:
```
LLDP-MIB::lldpMessageTxInterval
"lldpMessageTxInterval": {
"MibType": "Scalar",
"OvsTable": "system",
"OvsColumn": "other_config",
"Type": {
           "Key": "lldp_tx_interval"
        },
"CustomFunction": "lldpMessageTxInterval_custom_function"
},
```
When **lldp_tx_interval** is read using `smap_get` from the OVSDB, a *char* is returned. However, the MIB object expects an integer type. Therefore, the supplied custom convert function does the following:
```
void lldpMessageTxInterval_custom_function(const struct ovsdb_idl *idl, const struct ovsrec_system * system_row, long *lldpMessageTxInterval_val_ptr)
{
    char *temp = (char*)smap_get(&system_row->other_config, "lldp_tx_interval");
    smap_to_long(temp, lldpMessageTxInterval_val_ptr);
}
```
Consider another example, which is a tabular object in LLDP-MIB:
```
 "lldpPortConfigTable": {
            "MibType": "Table",
            "RootOvsTable": "interface",
            "CacheTimeout": 30,
            "SkipFunction": "lldpPortConfigTable_skip_function",
            "Indexes": {
                "lldpPortConfigPortNum": {
                    "OvsTable": "interface",
                    "OvsColumn": "name",
                    "Type": {
                        "Key": null
                    },
                    "CustomFunction": "lldpPortConfigPortNum_custom_function"
                }
            },
            "Columns": {
                "lldpPortConfigAdminStatus": {
                    "OvsTable": "interface",
                    "OvsColumn": "other_config",
                    "Type": {
                        "Key": "lldp_status"
                    },
                    "CustomFunction": "lldpPortConfigAdminStatus_custom_function"
                },
                "lldpPortConfigNotificationEnable": {
                    "OvsTable": null,
                    "OvsColumn": null,
                    "Type": {
                        "Key": null
                    },
                    "CustomFunction": null
                },
                "lldpPortConfigTLVsTxEnable": {
                    "OvsTable": "system",
                    "OvsColumn": "other_config",
                    "Type": {
                        "Key": "lldp_tlv_sys_name_enable"
                    },
                    "CustomFunction": "lldpPortConfigTLVsTxEnable_custom_function"
                }
            }
        },
```
In the above case, additional mapping parameters may be needed as described below:
  - **RootOvsTable**--Specifically defined for tabular MIB type which indicates the table to loop through in the schema to populate the MIB table.
  - **CacheTimeout**--Maximum time for which tabular data is cached in the Net-SNMP container. By default the timeout value is *30 seconds*. This value may be changed according the frequency of the cache refresh needed for a particular table. A value of *-1 never will cache the data* in a container.
 - **SkipFunction**--Specifies a function to implement skip logic. Some row entries in the OVSDB tables may need to be skipped while populating the MIB table.
For example, when dealing with physical interfaces, a logical interface such as 'Bridge_normal' may need to be skipped. Such skip logic may be defined in this function.
This mapping file will be located in feature repository under /src/snmp/*feature*_mapping.json.
2. Generate all the files for the MIB.
The SNMP infrastructure provides a python script **ops-snmpgen.py**. Executing this script with necessary options generates all the files for a given feature MIB.
Usage:
```
python ops-snmpgen.py --mapping-file=[PATH to mapping file] --mib-source='file: [PATH to MIB file]
```
The files are generated in the **/users/*user-name*/.pysnmp/mibs** directory.
The files that get generated when supporting the standard LLDP MIB are:
*LLDP_MIB_custom.c*  -> An empty file which is modified with all the custom functions.
*LLDP_MIB_custom.h*
*LLDP_MIB_plugins.c*-> A plugin file to use init/plugin destroy calls to the SNMP plugins.
*LLDP_MIB_plugins.h*
*LLDP_MIB_scalars.c* -> File containing register/handler/destroy function calls for all the scalars.
*LLDP_MIB_scalars.h*
*LLDP_MIB_scalars_ovsdb_get.c* -> File containing functions to get the data from the OVSDB, which will be a call to the custom convert function. In the custom convert function the developer defines a logic to return the appropriate value.
*LLDP_MIB_scalars_ovsdb_get.h*
For every table in the MIB, the following set of files are generated:
*lldpPortConfigTable.c* -> This file contains init or destroy calls to the table.
*lldpPortConfigTable_data_access.c* -> This file contains the container init, load, or cleanup calls.
*lldpPortConfigTable_data_access.h*
*lldpPortConfigTable_data_get.c* -> This file contains handlers for the read operation table.
*lldpPortConfigTable_data_get.h*
*lldpPortConfigTable_data_set.c*
*lldpPortConfigTable_data_set.h*
*lldpPortConfigTable_enums.h*
*lldpPortConfigTable.h*
*lldpPortConfigTable_interface.c*
*lldpPortConfigTable_interface.h*
*lldpPortConfigTable_oids.h*
*lldpPortConfigTable_ovsdb_get.c* -> File containing functions to get the data from OVSDB which will be a call to custom convert function. In the custom convert function the developer will define a logic to return the appropriate value.
*lldpPortConfigTable_ovsdb_get.h*
3. Cut and paste the generated files into the *feature/src/snmp* directory in the feature repository.
4.  Modify the custom.c file to return default values and to resolve any type of mismatch between the MIB and the schema.
5.  Write a makefile to generate a .so file of all the SNMP src files and install the .so at */usr/lib/snmp/plugins*.
  a. Write a makefile under the `src/snmp` directory. Override the default library directory path to  */usr/lib/snmp/plugins/*. For example:
 `libdir =/usr/lib/snmp/plugins`
  b. Avoid generating a static library by adding LDFLAGS = -module -shared -avoid-version.
  c. Include this library path in the *FILES-{PN}* of the feature .bb file.
6.  Add a net-snmp dependency to the feature repository by adding DEPENDS += 'net-snmp'.
```
DEPENDS = "net-snmp ops-utils ops-config-yaml ops-ovsdb libevent openssl ops-supportability"
```

SNMP traps
-------
The file for SNMP traps is automatically generated, when you run `ops-snmpgen.py` script, with code for all the traps in the given MIB File(The file is named `<MIB NAME>_traps.c`). Add this file to your repository and call the respective functions for sending the traps in your repository at the appropriate locations. The design for SNMP traps is documented in the SNMP Design.md (See References). For a sample you can look at the code(`LLDP_MIB_traps.c`) described in ops-lldpd.
```
/* In ops-lldpd lldpd.c file calls the generated functions */
lldpd_send_lldpRemTablesChange_trap(stuct lldpd_hardware *hardware) {
    /* This is the auto generated function for lldpRemTablesChange trap
     * This function is present in LLDP_MIB_traps.c*/
    send_lldpRemTablesChange();
}
```

References
------
Click [here](documents/user/snmp_design) for the SNMP design.md.
Click [here](http://lists.openswitch.net/pipermail/ops-dev/2016-January/001395.html) for the ops-dev email archive.
