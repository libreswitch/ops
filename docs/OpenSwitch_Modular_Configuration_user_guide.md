# OpenSwitch Modular Configuration User Guide


## Contents

- [Integrating a feature](#integrating-a-feature)
    - [Update Kconfig files](#update-kconfig-files)
    - [Update the default configuration file](#update-the-default-configuration-file)
    - [Update recipe files](#update-recipe-files)
    - [Tag schema entries](#tag-schema-entries)
        - [Feature-tagging the JSON schema](#feature-tagging-the-json-schema)
            - [Feature-tagging a table](#feature-tagging-a-table)
            - [Feature-tagging a column](#feature-tagging-a-column)
            - [Feature-tagging an enum within a column](#feature-tagging-an-enum-within-a-column)
        - [Feature-tagging the XML schema](#feature-tagging-the-xml-schema)
            - [Feature-tagging a table](#feature-tagging-a-table)
            - [Feature-tagging a group](#feature-tagging-a-group)
            - [Feature-tagging a column within a group](#feature-tagging-a-column-within-a-group)
            - [Feature-tagging a column within a table](#feature-tagging-a-column-within-a-table)
    - [Embed decorators in test scripts](#embed-decorators-in-test-scripts)
        - [Skipping a test](#skipping-a-test)
    - [Modify package groups](#modify-package-groups)
- [Things to keep in mind](#things-to-keep-in-mind)
- [References](#references)

## Integrating a feature

Following are the high level steps one should follow to integrate a feature
into the OpenSwitch Modular Configuration:

1. [Update Kconfig files](#update-kconfig-files)
2. [Update the default configuration file](#update-the-default-configuration-file)
3. [Update recipe files](#update-recipe-files)
4. [Tag schema entries](#tag-schema-entries)
5. [Embed decorators in test scripts](#embed-decorators-in-test-scripts)
6. [Modify package groups](#modify-package-groups)

Detailed guidelines and steps are provided in each section.

### Update Kconfig files

Updating Kconfig files is accomplished through the UI. Typically this involves
adding two to four lines to an existing Kconfig file. Guidelines are as follows:

1. Identify an existing Kconfig file for the feature and use it, instead of
creating a new Kconfig file. A new platform creation always requires adding a
new platform specific Kconfig file. Refer to the "Kconfig files layout" section
of the OpenSwitch_Modular_Configuration_design.md document for details on
existing Kconfig files.

2. Adding a new feature into the Kconfig front-end typically involves adding
two to four constructs into a Kconfig file. Refer to the Kconfig language
syntax, which has a small set of constructs:
   https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt

   Example 1: NTP feature added to $(BUILD_ROOT)/yocto/openswitch/
   meta-distro-openswitch/recipes-ops/mgmt/Kconfig file.

```
   config OPS_NTPD
        bool "Network Time Protocol (NTP) Client"
        default y
        ---help---
          The NTP client feature provides the Network Time Protocol client
          functionality which synchronizes information from NTP servers.
          For more details, please visit:
            http://openswitch.net/documents/dev/ops-ntpd/design
```

   Example 2: Buffmon feature added to $(BUILD_ROOT)/yocto/openswitch/
   meta-distro-openswitch/recipes-ops/utils/Kconfig file.

```
   config OPS_BUFMOND
        bool "Buffer Monitor"
        default y
        ---help---
          Buffers Monitoring is a feature that provides OpenSwitch users the
          ability to monitor buffer space consumption inside the ASIC. It is
          useful for troubleshooting complex performance problems in the data
          center networking environment.
          For more details, please visit:
            http://openswitch.net/documents/dev/ops-bufmond/design
```

   Example 3: Broadview feature added to $(BUILD_ROOT)/tools/config/Kconfig.bcm
   file.

```
    config OPS_BROADVIEW
        bool "Broadview"
        depends on OPS_BUFMOND
        default y
        ---help---
          BroadView Instrumentation exposes various instrumentation
          capabilities in Broadcom silicon.
```

   Example 4: A dummy key-value pair example (number of physical ports) added to
   $(BUILD_ROOT)/yocto/openswitch/meta-distro-openswitch/recipes-ops/l2/Kconfig
   file.

```
    config KEY_VALUE_EXAMPLE_NUM_PORTS
        int "Example: Number of physical ports"
        default 64
        range 8 256
        ---help---
          This is to demonstrate how to make use of key-value pairs through
          through OpenSwitch Modular Configuration framework.
```

3. Kconfig symbol naming should adhere to the following rule if the symbol
being added is for a feature/sub-feature. This rule does not apply to
key-value pairs:
   - Use the feature repo name as the Kconfig symbol. Use uppercase letters and
     replace "-" with "_".
     For example, if the feature repo name is ops-<repo-name>, then
     OPS_<REPO_NAME> should be used as the Kconfig symbol.
   - Prepend the sub-feature directory name with "OPS_" and use as the Kconfig
     symbol. Use uppercase letters and replace "-" with "_".
     For example, if the sub-feature directory name is <sub-feature> (inside
     ops-<repo-name>), then use OPS_<SUB_FEATURE> as the Kconfig symbol
     dependent on OPS_<REPO_NAME>.

   Example 1: ops-dhcp-tftp will have OPS_DHCP_TFTP as the Kconfig symbol.

   Example 2: ops-quagga has bgpd and ospfd subfeatures. In this case add
   OPS_QUAGGA, OPS_BGPD and OPS_OSPFD as Kconfig symbols, and make OPS_BGPD and
   OPS_OSPFD dependent on OPS_QUAGGA. In addition to providing a parsing
   scripts clue about the feature package, this nicely groups and presents the
   quagga routing protocol suite to the user. The user can also disable the
   entire quagga routing protocol suite with a single selection.

4. Although the Kconfig language has limited set of constructs, many advanced
configuration options can be covered by using them. Refer to examples available
online or in a Linux kernel source.

### Update the default configuration file

The default configuration file (.ops-config) is used if the user decides to
skip `make menuconfig` and build the image. The default configuration file
should be updated with any changes to the Kconfig files. If this step is
skipped, then the feature will be disabled by default.

1. Run `make menuconfig` and set the default value for newly added feature.
Save and exit the configuration file. Commit the configuration file present at:

```
   yocto/openswitch/meta-platform-$(DISTRO)-$(CONFIGURED_PLATFORM)/.ops-config
```

2. Since the configuration file is platform specific, the above step should be
completed for all platforms. Run the `make switch-platform <platform>` command
followed by the `make menuconfig` command.

### Update recipe files

1. If the feature being added has a one-to-one mapping with the repository and
recipe being created, then the enable/disable of that feature is controlled by
including/excluding the corresponding Yocto package. Yocto internally can
include/exclude multiple dependent packages.

   Often there are requirements that need to pass certain buid-time flags to
   repo level makefiles. Some example scenarios, but not limited to, are as
   follows:
   - Key-value pair exposed to user.
   - A single repository consisting of multiple sub-features.
     Example: ops-quagga containing bgp and ospf.
   - Partial dependencies among features. A feature can continue to exist with
     reduced functionality if the other dependent feature is disabled. Such
     partial dependencies cannot be expressed using Kconfig files.
     Example: ops-cli has code specific to many other features that can be
     independently enabled/disabled.
     Example: Broadcom switchd plugin can have code specific to a broadview
     feature.

   The IMAGE_FEATURES data store variable of Yocto contains a list of enabled
   features (Kconfig symbols). All recipe files have access to this variable
   and the enabled feature list. Decisions can be based on the presence/absence
   of a Kconfig symbol in the IMAGE_FEATURES variable.

2. To pass a feature flag to repo level makefiles:

```
   <Yocto Flag> += "${@bb.utils.contains('IMAGE_FEATURES', '<Kconfig Symbol>', '-DENABLE_<Kconfig Symbol>=1', '', d)}"
   Where <Yocto Flag> can be EXTRA_OECMAKE, EXTRA_OECONF
   depending on type of build tool used (Autotools, CMake).
```

   Example: To pass information about whether broadview and bufmon features are
   enabled/disabled to the bcm switchd plugin, ops-switchd-opennsl-plugin.bb
   should include the following:

```
   # Pass required feature configuration flags to make process.
   # Syntax: -DENABLE_<Kconfig symbol>=1
   EXTRA_OECMAKE += "${@bb.utils.contains('IMAGE_FEATURES','OPS_BUFMOND','-DENABLE_OPS_BUFMON=1','',d)}"
   EXTRA_OECMAKE += "${@bb.utils.contains('IMAGE_FEATURES','OPS_BROADVIEW','-DENABLE_OPS_BROADVIEW=1','',d)}"
```

3. To pass a key-value pair to repo level makefiles:

```
   <Yocto Flag> += "-D<Kconfig Symbol>=${Kconfig Symbol}"
   Where <Yocto Flag> can be EXTRA_OECMAKE, EXTRA_OECONF
   depending on type of build tool used (Autotools, CMake).
```

   Example: To pass the number of available physical ports to the bcm switchd
   plugin, ops-switchd-opennsl-plugin.bb should include the following:

```
   # Pass required key value flags to make process.
   # Syntax: -D<Kconfig symbol>=${<Kconfig symbol>}
   EXTRA_OECMAKE += "-DKEY_VALUE_EXAMPLE_NUM_PORTS=${KEY_VALUE_EXAMPLE_NUM_PORTS}"
```

4. Recipe files may require more changes, in addition to passing flags to repo
level makefiles. One example is if each of the sub-features have their own set
of resources (daemons, files...). In such cases, all sub-feature related
content in the recipe file should be protected with a check to the sub-feature
specific Kconfig symbol in the IMAGE_FEATURES variable.

   Example: In do_install_append() task of ops-quagga.bb:

```
   if ${@bb.utils.contains('IMAGE_FEATURES','OPS_BGPD','true','false',d)}; then
   install -m 0644 ${WORKDIR}/ops-bgpd.service ${D}${systemd_unitdir}/system/
   fi

   if ${@bb.utils.contains('IMAGE_FEATURES','OPS_OSPFD','true','false',d)}; then
   install -m 0644 ${WORKDIR}/ops-ospfd.service ${D}${systemd_unitdir}/system/
   fi
```

### Tag schema entries

The schema is captured as part of the JSON format file (for example,
vswitch.extschema)and the corresponding XML format file (for example,
vswitch.xml). These schema-files are located within the ops repository
(ops/schema). We feature-tag the entries in both of these file formats.
The entries from both of these file formats need to be pruned whenever a
feature is not included in an image. The feature-name used for tagging
corresponds to the Kconfig symbol defined for that feature.

The general guidelines are as follows:
1. Features need to tag an entity (table/column/enum) only if they are using it
exclusively. If a certain entity is exclusively used by 2 features, then both
of these features need to tag the entity. Only when both features are not
included in the image will the entity be pruned out.

2. If an entity is untagged, it takes the tag of the immediate outer entity.
   For example, if all columns within a table are untagged, but the table
   itself is tagged as feature-1, then all columns are tagged as feature-1.

   If the table itself is untagged, then it represents a generic table (for
   example, "System") which is used by multiple features. Such untagged tables
   are always included in the schema.

3. The feature-tag at innermost granularity overrides the feature-tag at outer
   granularities.

   Example: Feature-1 is exclusively using Table-A which it has tagged. Later
   feature-2 is introduced and wants to add a column to Table-A. This column is
   exclusively used by feature-2. This new column is tagged with feature-2. This
   means feature-1 owns Table-A, except for the new column. Feature-2 owns the
   new column in Table-A.

   If feature-1 wants to use the new column, it must tag the new column. If
   Table-A is tagged with feature-1 as well as feature-2, then all columns
   within it are implicitly tagged as feature-1 and feature-2.

   To distinguish ownership, the columns can be explicitly tagged (which
   overrides any previous implicit tagging due to tags at the outer layers).

   **Note:** If a table is untagged, and a feature that wants to use it is
   unsure if the Table is being used by other features, then it should not
   exclusively tag the table.

#### Feature-tagging the JSON schema
The JSON schema can be feature-tagged at 3 levels: table, column, enum. The
feature-tag at the innermost granularity overrides the feature-tag at outer
granularities. This means the feature-tag of an enum within a column overrides
the feature-tag of the column, which in turn overrides the feature-tag of the
table.

The feature tag is defined as a list of features:
```
    "feature_list": ["feature-1", "feature-2", ..., "feature-N"],
```

##### Feature-tagging a table
```
{
    "name": "OpenSwitch",
    "tables": {
        ...
        "bufmon": {
            "feature_list": ["OPS_BUFMOND"],
            "columns": {
                ...
            }
        }
    },
    "version": "0.1.8"
}
```

##### Feature-tagging a column
```
{
    "name": "OpenSwitch",
    "tables": {
        ...
        "System": {
            "columns": {
                ...
                "bufmon_config": {
                    "feature_list": ["OPS_BUFMOND"],
                    "category": "configuration",
                    ...
                },
                "ntp_status": {
                    "feature_list": ["OPS_NTPD"],
                    "category": "status",
                    ...
                },
                ...
            }
        },
        ...
    },
    "version": "0.1.8"
}
```
##### Feature-tagging an enum within a column
In this case, instead of a regular string entry inside an enum-set, you need to
define a dictionary type containing "val" and "feature_list".
```
{
    "name": "OpenSwitch",
    "tables": {
        ...
        "Subsystem": {
            "columns": {
                ...
                "type": {
                    "category": "status",
                    "type": {
                        "key": {
                            "type": "string",
                            "enum": [
                                "set",
                                [
                                    {
                                         "val": "uninitialized",
                                         "feature_list": ["feature-1", "feature-2"]
                                    },
                                    "system",
                                    "chassis",
                                    {
                                        "val": "line_card",
                                        "feature_list": ["feature-1"]
                                    },
                                    "mezz_card"
                                ]
                            ]
                        },
                        "min": 0,
                        "max": 1
                    }
                },
            }
        },
        ...
    },
    "version": "0.1.8"
}
```

#### Feature-tagging the XML schema
The XML schema can be feature-tagged at three levels: table, group, and column.
The feature-tag at the innermost granularity overrides the feature-tag at outer
granularities. The feature-tag of a column within a group overrides the
feature-tag of the group, which in turn overrides the feature-tag of the table.
If a column within a table is not part of a group, then the feature-tag of the
column overrides the feature-tag of the table.

The feature tag is defined as a list of features:
```
    <feature_list>
        <feature>feature-1</feature>
        <feature>feature-2</feature>
        ...
        <feature>feature-N</feature>
    </feature_list>
```

##### Feature-tagging a table
```
<?xml version="1.0" encoding="utf-8"?>
<database title="OpenSwitch Configuration Database">
    ...
    <table name="bufmon">
        <p>
            Configuration and status of the counters per Capacity Monitoring feature
        </p>
        <feature_list>
            <feature>OPS_BUFMOND</feature>
        </feature_list>
        ...
    </table>
    ...
</database>
```

##### Feature-tagging a group
```
<?xml version="1.0" encoding="utf-8"?>
<database title="OpenSwitch Configuration Database">
    ...
    <table name="System">
        ...
        <group title="Bufmon configuration">
            <feature_list>
                <feature>OPS_BUFMOND</feature>
            </feature_list>
            <column name="bufmon_config" key="enabled"
                ...
            </column>
            ...
        </group>
        ...
    </table>
    ...
</database>
```

##### Feature-tagging a column within a group
```
<?xml version="1.0" encoding="utf-8"?>
<database title="OpenSwitch Configuration Database">
    ...
    <table name="System">
        ...
        <group title="NTP configuration">
            <p>
                Specifies the NTP global configuration.
            </p>
            <feature_list>
                <feature>OPS_NTPD</feature>
            </feature_list>
            <column key="authentication_enable" name="ntp_config" type="{&quot;type&quot;: &quot;boolean&quot;}">
                Determines whether NTP Authentication is enabled in the system.
                Default is false.

                <feature_list>
                    <feature>OPS_NTP_CLIENT</feature>
                </feature_list>
            </column>
        </group>
        ...
    </table>
    ...
</database>
```

##### Feature-tagging a column within a table
```
<?xml version="1.0" encoding="utf-8"?>
<database title="OpenSwitch Configuration Database">
    ...
    <table name="System">
        ...
        <column name="ntp_status" key="uptime">
            Time in hours since the system was last rebooted.
            <feature_list>
                <feature>OPS_NTPD</feature>
            </feature_list>
        </column>
        ...
    </table>
    ...
</database>
```

### Embed decorators in test scripts

**Note:** This is work-in-progress.
**Note:** This mechanism is available for the modular test framework alone. When
porting a feature to the ops_mod_config framework, the tests must be ported to
the modular framework as well.

The CIT framework deploys "pytest" to run the Python test-scripts that are
placed within the repos. As part of ops_mod_config, when a certain feature is
disabled, the tests corresponding to it should not be run (as they will fail).

A file (build/image_features) containing the list of features enabled by
ops_mod_config is generated as part of "make" and is also available as a
manifest file along with the released image bundle. This file (or the manifest
file) act as inputs to the Test framework to create a global set of enabled
features. The individual tests in the test-script need to be tagged with the
features it caters to. The test framework runs a test only when all features
marked for the test have been enabled. In case the test is not marked with any
feature, it will be run by the test-framework.

#### Skipping a test
If a test caters to feature-1, feature-2, ... feature-N, and the plan is to skip
running this test if any of the features are disabled, use the following:

```
from pytest import mark

@mark.feature-1
@mark.feature-2
...
@mark.feature-N
def <testname>(self):

For Example:

@mark.OPS_NTPD
def test_ct_ntp_config(topology, step):
	...
```

### Modify package groups

Before OpenSwitch Modular Configuration framework was in place, every package
associated with a new feature was added to Yocto PACKAGES (through
packagegroup-ops-base in packagegroup-openswitch.bb). This is no longer needed
with the OpenSwitch Modular Configuration framework.

Since it will take time to integrate all existing platforms and features with
the OpenSwitch Modular Configuration framework, follow the next steps to keep
backwards compatibility:

1. To add a new feature into OPS Mod Config framework:
   Include the package associated with the feature in packagegroup-ops-base

2. Porting an existing feature into OPS Mod Config framework:
   Remove the package associated with the feature from packagegroup-ops-config

3. Adding a new platform or porting an existing platform into OPS Mod Config
   framework:
   Include packagegroup-ops-config instead of packagegroup-ops-base in the
   platform specific configuration file

Eventually, packagegroup-ops-config will completely replace
packagegroup-ops-base.

## Things to keep in mind

The following items are covered elsewhere in OpenSwitch documentation, but are
good things of which to be aware.

1. Add new feature repository to the devenv.conf file. The devenv tools depend
on the devenv.conf file to display all available repos, and add them locally
for development. The OpenSwitch Modular Configuration framework also refers to
this file to identify main features and the associated packages.

2. Keep the repository name same as the recipe file name. This allows mapping a
feature repo name directly to the package name.

## References

* [Kconfig Language Syntax](https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt)
* [OpenSwitch Modular Configuration Design](http://git.openswitch.net/cgit/openswitch/ops/tree/docs/OpenSwitch_Modular_Configuration_design.md)
* [IRC Discussion](http://eavesdrop.openswitch.net/irclogs/%23openswitch/%23openswitch.2015-11-11.log.html)
* [Adding a new feature to OpenSwitch](http://openswitch.net/documents/dev/contribute-code#adding-a-new-feature)
