# Versioning Infrastructure

## Contents

- [Show version](#show-version)
  - [Description](#description)
- [Show version detail](#show-version-detail)
  - [Description](#description)
  - [Use cases](#use-cases)
  - [Internal workings](#internal-workings)
  - [Block diagram](#block-diagram)
  - [Version detail yaml file](#version-detail-yaml-file)
  - [Source code debugging](#source-code-debugging)
  - [Limitations](#limitations)

## Show version
### Description
This command shows the current switch version information.
The switch version captures the project-name, platform, git-branch, and timestamp.

For example:

| Switch Image Build Type                                                 | Show version                                                                |
|-------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Developer build of OpenSwitch from the master branch for genericx86-64. | OpenSwitch 0.4.0 (Build: genericx86-64-ops-0.4.0-master-20160419204046-dev) |
| Periodic build of OpenSwitch from the master branch for genericx86-64.  | OpenSwitch 0.4.0 (Build: genericx86-64-ops-0.4.0-master+2016042606          |
| Developer build of OpenSwitch from the master branch for AS5712.        | OpenSwitch 0.4.0 (Build: as5712-ops-0.4.0-master-20160419204046-dev)        |
| Periodic build of OpenSwitch from the master branch for AS5712.         | OpenSwitch 0.4.0 (Build: as5712-ops-0.4.0-master+2016042606)                |
| Periodic build of OpenSwitch from the release branch for AS5712.        | OpenSwitch 0.3.0 (Build: as5712-ops-0.3.0-rc0-release+2016042606)                |

For detailed explanation of every field, refer to the [CLI Guide](/documents/user/system_cli).

## Show version detail
### Description
The `show version detail` command is supported, and lists some key information for all packages included in the image.

### Use cases
1. To provide all users of the image a list of all the packages within the image and their versions.
2. To provide the source code location of every package, which allows inspection/debugging of the relevant package.

### Internal workings
Yocto is used to build the images.
The runtime "package manager" functionality of Yocto uses the package*.bbclass to maintain per package metadata.
However, the runtime "package manager" is not included with our image.
Because the runtime "package manager" is not included, the metadata maintained per package is not present in the image.
The metadata is gathered during build time in order to display the desired information.
Functionality from the "package.bbclass" is leveraged, and is used by the package manager as well.
On the build machine, the metadata per package is gathered and stored in files (also called dictionaries) at - ${PKGDATA_DIR}.
During the packaging process, the "do_packagedata" task packages data for each recipe and installs it in a temporary, shared area. This directory defaults to the following: ${STAGING_DIR_HOST}/pkgdata
This resource is used to generate a "Version Detail" yaml file that contains the desired information per package.
This file is packaged along with the image.
When ops-sysd comes up, it reads this file and fills the information therein into the OVSDB "Package_Info" table.
This OVSDB information is then accessed by management entities like CLI and REST to display the package information.
The implementation of the "show version detail" CLI displays the package information.

### Block diagram
```ditaa
+------------+         +-------+         +----------------+
|            |  init   |       |   CLI   |     ops-cli    |
|  ops-sysd  +-------->| OVSDB +-------->| (vtysh Daemon) |
|            |         |       |         |                |
+------------+         +-------+         +----------------+
          ^
          |
          |
          |
  +-------+--------+
  | version detail |
  | file (YAML)    |
  | /var/lib/      |
  +----------------+

```

###  Version detail yaml file
The version detail file is generated during build time after the rootfs is created, and before the image is generated.
For every package present in the image, it lists the version number and the source-code path.
Based on the source-code path, the "source-type" for the package can be https, http, ftp, git, svn, or cvs.
If the source-type is a git repository, the version corresponds to the git hash (SRCREV).
Otherwise, the version corresponds to a version string (PV).
On the build server, this file is generated at - ${DEPLOY_DIR_IMAGE}/${IMAGE_NAME}.version_detail.
It is then copied to the image at - /var/lib/version_detail.yaml.

Sample contents of this file are shown below:

```ditaa
PKG: ops-switchd
PV: gitAUTOINC+107ce4f327
SRCREV: 107ce4f327facf7fa634a57cacf659f99d44967d
SRC_URL: https://git.openswitch.net/openswitch/ops-switchd
TYPE: git
---
PKG: sed
PV: 4.2.2
SRCREV: INVALID
SRC_URL: http://ftp.gnu.org/gnu/sed/sed-4.2.2.tar.gz
TYPE: http
```
**Note:** A few entries in this file will contain just the "PKG", and may or may not contain "PV".
For example:
```ditaa
PKG: packagegroup-base-ipv6
PV: '1.0'
SRCREV: INVALID
SRC_URL: NA
TYPE: other
```
These entries correspond to "metapackages". They exist as packages, but do not install any files. They are used to pull in other packages through dependencies. The PKGSIZE value for such metapackages is usually zero.

### Source code debugging
As the "show version detail" output displays the source-code path (src_url), one is able to fetch the exact codebase corresponding to the package. In case of git repositories, one is able to fetch the exact codebase corresponding to the git-hash printed.
For example:
```ditaa
git clone <src_url>
cd <repo>/
git fetch origin <git-hash>
git reset --hard FETCH_HEAD
```

### Limitations
Since the runtime "package manager" is not part of the image, static information gathered during build time is used.
This information is fed to the OVSDB by ops-sysd during init time.
If there are hot patches, or a new version of a package is installed on the running image, the OVSDB still points to stale information present in the database. This limitation will be address when our images begin supporting the runtime package manager.
