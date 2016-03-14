# Audit Log How-to Guide for OpenSwitch Developers

## Contents

- [Trusted applications](#trusted-applications)
- [Supplying the user for a configuration change](#supplying-the-user-for-a-configuration-change)
- [The audit log library](#the-audit-log-library)
	- [Common audit log function parameters](#common-audit-log-function-parameters)
		- [int audit\_fd](#int-auditfd)
		- [int type](#int-type)
		- [const char \*hostname](#const-char-hostname)
		- [const char \*addr](#const-char-addr)
		- [const char \*tty](#const-char-tty)
		- [int result](#int-result)
	- [Audit log functions](#audit-log-functions)
		- [Connect to the audit framework](#connect-to-the-audit-framework)
		- [Encode user supplied data](#encode-user-supplied-data)
		- [Generate a general configuration change audit event](#generate-a-general-configuration-change-audit-event)
		- [Generate a configuration change using a scheduled program audit event](#generate-a-configuration-change-using-a-scheduled-program-audit-event)
		- [Manipulate user account audit events](#manipulate-user-account-audit-events)
		- [Execute a script](#execute-a-script)
- [Python code example for RESTD](#python-code-example-for-restd)
	- [RESTD audit log wrapper function](#restd-audit-log-wrapper-function)
- [C code example](#c-code-example)
	- [Building with and linking in the audit library](#building-with-and-linking-in-the-audit-library)
- [Interpreting and displaying audit log events](#interpreting-and-displaying-audit-log-events)
- [Additional references](#additional-references)

The goal of an audit log/trace feature is to track who did what. This guide documents how to use the Linux audit framework to create audit events for tracking configuration changes made by users to OpenSwitch. It describes the audit log functions and their parameters. It provides examples of their usage in both C and Python code.

## Trusted applications

The Audit Framework only allows trusted applications to create audit events. A trusted application is defined as any process running as root, or a non-root process that has the CAP_AUDIT_WRITE capability set. The *restd* process is an example of a process that runs as the root user. The *vtysh* process is an example of a non-root process (as long as a non-root user is logged in). In order to turn a non-root process into a trusted application, the *setcap* utility must be used. Use the following command to turn the *vtysh* process into a trusted application by the audit framework:

	setcap cap_audit_write+eip /usr/bin/vtysh

This command needs to be issued after *vtysh* is built, but before the OpenSwitch image is created. If you issue this on a running switch, you may need to reboot for the capability to take effect. One caution about Python programs since they are not native executables, but are interpreted, the CAP_AUDIT_WRITE capability must be set on the Python interpreter itself.

## Supplying the user for a configuration change

When creating an audit event, the end user associated with the configuration change must always be noted. There are some implementation issues of which you need to be aware. If the process that calls the audit log library function is running as the actual end user, the audit framework automatically injects the correct user ID into the audit event record. For example, if *vtysh* runs with the actual UID/GID of the user that logged in, then no special provision is needed to supply the user in the audit log call.

However, if the process is running as root on behalf of one or more end users, the audit framework  always injects the root user into the audit event record. In this case, the audit log function caller **MUST** supply the user that is responsible for the configuration change, as noted below.

## The audit log library

The Audit Framework provides a library of functions used to create audit event records. There are bindings for *C/C++*, *Python*, and *Go*. A summary of the calls are as follows:

- audit_open() - Initiate a connection to the audit framework for subsequent audit calls.
- audit_encode_nv_string(…) – Used to encode user supplied data to prevent injection attacks.
- audit_log_user_message(…) – Log a general configuration change to the switch.
- audit_log_user_command(…) – Log a user command.  Only needed if you schedule a program that modifies the switch configuration.
- audit_log_acct_message(…) – Log changes to user accounts (add/delete/role change/etc).
- audit_log_comm_message(…) – Log a console app message while executing a script. Probably will not be used.

Each of these functions have an associated main page. You can look them up in your browser, or install them on your local VM using the following command:

	sudo apt-get install auditd

Many of the parameters used in the *audit_log...()* function calls are common. These parameters are described in the next section, followed by a detailed description of each audit log function.

### Common audit log function parameters

#### int audit\_fd

This parameter is returned by a call to *audit_open()* and must be passed unaltered as the first parameter in all audit_log...() calls.

#### int type

This parameter is the audit event type. A large number of different event types are available, whose use depend on the type of audit event data being logged. In most cases only a couple of these event types are used. The full list can be found in */usr/include/libaudit.h*. In addition, a more complete description of each event type can be found in Appendix B.2 of the [Red Hat Enterprise Linux Security Guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Security_Guide/sec-Audit_Record_Types.html). The following event types are the ones primarily used:

	AUDIT_USYS_CONFIG - Used when a user-space system configuration change is detected.
    AUDIT_TRUSTED_APP - Used when system configuration change is made and the message parameter uses free-form text (rare).

Daemons and services that create audit events should also use the following events:

	AUDIT_SERVICE_START - Used to indicate the service/daemon has started.
    AUDIT_SERVICE_STOP - Used to indicate the service/daemon has stopped.

#### const char \*hostname

This parameter contains the local hostname of the switch if known, or NULL (None in Python) if unknown. This parameter is especially important when a customer redirects the audit events to a central remote system.  During analysis, it allows one to determine with which system a given event is associated. It is recommended that a valid hostname is always supplied.

#### const char \*addr

This parameter contains the remote network address of the user if known, or NULL (None in Python) if unknown. The http REST server code should supply this parameter, as it is available in every REST request.

#### const char \*tty

This parameter is the *tty* of the user if known, or NULL (None in Python) if unknown. When NULL is supplied, the audit function attempts to automatically figure out the user's tty. This parameter normally only has a value for CLI based code.

#### int result

The result of the configuration operation. The value 1 is used for success, and the value 0 is used for failure. This implies that the audit log call must be made after the configuration action has taken place.

### Audit log functions

This section supplements the standard audit log man pages. Consult the audit log man page for the details on each function and its parameters. This section provides OpenSwitch specific usage context and critical usage information missing from the standard man pages.

#### Connect to the audit framework
```
int audit_open()
```

This function opens a Netlink socket connection to the audit framework and returns its file descriptor. This file descriptor must be passed to all subsequent audit_log...() calls. This function should only be called once in a program.

#### Encode user supplied data
```
char audit_encode_nv_string(const char name, const char value, unsigned int vlen)
```

Audit event records are made up of a set of name/value pairs. The name parameter is one of the standard predefined audit field names. The value parameter is the data associated with that field, which can be supplied by a user. The primary purpose of this function is to encode user supplied data to prevent log injection attacks where malicious values could cause parsing errors in the aureport and ausearch audit utilities or other analysis utilities. A secondary use is to encode any field's value data that contains a space, double-quote, or control character. Only field names that expect encoded data should be used, as these are the only fields that will be decoded when displaying the event data. This function returns a pointer to a malloc'ed string. C programs must free this string after use.

The vlen parameter must be set to zero (0) unless the data contains an embedded null, in which case it is set to the actual length of the data.

The full list of field names and their expected formats can be found in the "How to write good events" white paper on the Audit Framework web site at [http://people.redhat.com/sgrubb/audit/audit-events.txt](http://people.redhat.com/sgrubb/audit/audit-events.txt).

#### Generate a general configuration change audit event
```
int audit_log_user_message(int audit_fd, int type, const char *message,
						   const char *hostname, const char *addr, const char *tty, int result)
```

This is the main function developers use to generate a general configuration change audit event. The message parameter should contain a set of field name/value pairs, each separated by a space. The general form is`<field name>=<value>`. The primary field names that most calls will use are *op*, *data*, and *user*. However, additional fields may be needed depending on the nature of the event and its data. The previous section has a link to the full list of field names. A description of the field names can also be found in Appendix B.1 of the [Red Hat Enterprise Linux Security Guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Security_Guide/app-Audit_Reference.html).

The **op** field should contain a description of the configuration operation being performed. It must not contain a space, double-quote, or control character. If the operation normally contains multiple words, replace each space with a dash or underscore character. It is recommended a short prefix representing the module creating the audit event is added. For example:

```
op=RESTD:Set-hostname
op=CLI:Disable-Port
```

The **data** field is expected to be in an encoded format (using *audit_encode_nv_string*), and should contain the data associated with the configuration change. If there is no data, it can be omitted. For example, if the operation was to disable port A2, the call `audit_encode_nv_string("data", port_name, 0)` returns the following string:

```
data="A2"
```

The **user** field is only used in programs that run as root (or a user different from the end user making the change). In the context of OpenSwitch, this is the restd daemon. The Audit Framework normally automatically supplies the user id and login UID (AUID field) of the executing process. In the case of the restd daemon, the user id would always be 0 (root) and the login UID would be unset. The restd code handles REST requests from a previously authenticated user. The user field **MUST** always be supplied in all audit events created by the restd daemon or other similar programs. For example:

```
user=fredflintstone
```

The following two examples are what a message string might look like for the CLI (vtysh) and restd code:

```
op=CLI:Disable-Port data="A2"
op=RESTD:Set-hostname data="MyHostname" user=fredflintstone
```


#### Generate a configuration change using a scheduled program audit event
```
int audit_log_user_command(int audit_fd, int type, const char \*command, const char *tty, int result)
```

This function is used when a program is scheduled to change the OpenSwitch configuration. The command parameter is the full text of the command being issued.  For example, if a command to change the hostname was issued, this parameter might look like:
```
/bin/hostname my-new-hostname
```

#### Manipulate user account audit events
```
int audit_log_acct_message(int audit_fd, int type, const char *pgname, const char *op, const char *name,
                           unsigned int id, const char *hostname, const char *addr, const char *tty, int result)
```

This function is used for all user account manipulation operations. This includes adding and deleting users, changing user roles, user login and authentication, etc. The OpenSwitch code uses PAM and the useradd and userdel utilities for operations that have already implemented the correct audit log calls. Therefore, it is not anticipated that any OpenSwitch code will need to call this function.

However, if in the future, a custom/sophisticated Role Based Access Control function is implemented, this call may be needed to log various "role" events.

#### Execute a script
```
int audit_log_user_comm_message(int audit_fd, int type, const char *message, const char *command,
						        const char *hostname, const char *addr, const char *tty, int result)
```

This function is used for commands executing a script. For example, *crond* wanting to say what they are executing. This function probably will not be used by any OpenSwitch code. Note the command and message parameters were documented above.

## Python code example for RESTD

Python code should be able to directly use the audit library without any changes to your recipe files. In the example, the variables are assumed to contain the following:

- op 		- The text indicating the operation that was performed (mandatory).
- cfgdata	- The optional configuration data associated with the operation.
- user_name  - The name of the user (for example, linux user name) issuing the REST request (mandatory).
- hostname   - The local host name of the system (or None).
- addr       - The remote IP address of the user issuing the REST request.
- result     - The value 1 or 0 indicating success or failure of the operation.
- self 	  - The Tornado web.RequestHandler instance (see basy.py BaseHandler class).

```
import audit
import socket

audit_fd = audit.audit_open()

cfg = ""
if (cfgdata != None):
    cfg = audit.audit_encode_nv_string("data", str(cfgdata), 0)
    if (cfg == None):
        cfg = ""		# You may want to throw a MemoryError exception

addr = self.request.remote_ip;
hostname = socket.getfqdn()
user_name = self.get_secure_cookie("user")
msg = str("op=RESTD:%s %s  user=%s" % (op, cfg, user_name))
audit.audit_log_user_message(audit_fd, audit.AUDIT_USYS_CONFIG,
                             msg, hostname, addr, None, result)
```

### RESTD audit log wrapper function

If your audit log events are substantially of the same form, it is highly recommended that you implement a wrapper function to ensure that required parameters and field values are supplied and follow a consistent format. An example wrapper function has been implemented in the ops-restd code that can be used as is or modified to meet your needs. Other repos (for example, ops-cli) should use this as the example pattern for creating their own wrapper functions. This function is located in *opsrest/utils/auditlog_utils.py*.  The name of the function is *audit_log_user_msg*.

	audit_log_user_msg(op, cfgdata, user, hostname, addr, result)

Where:

* **op** is text representing the operation being performed.  Note that a "RESTD:" prefix is automatically added.
* **cfgdata** is the configuration data associated with the operation, or None if there is no data.
* **user** is the name of the user that issued the REST request.
* **hostname** is the local host name of the system or the value None.
* **addr** is the remote user's IP address or None if unknown.
* **result** is 1 if the configuration operation succeeded, otherwise it is 0 if the operation failed.


## C code example

In order to use the audit log library, you need to change your repo recipe to link in libaudit.a (static) or libaudit.so (shared).  The build system also needs a dependency on the audit framework.  Like the Python example, this example assumes the same variables (and their contents).  This example is appropriate for creating an audit event in the vtysh (CLI) code.

```
#include <libaudit.h>

int audit_fd;
char *cfg;          /* Ptr to the encoded data field/value string. */
char aubuf[160];	/* Buffer to hold the message string. */
char hostname[HOST_NAME_MAX+1];

audit_fd = audit_open();

gethostname(hostname, HOST_NAME_MAX);
strcpy(aubuf, "op=CLI:Disable-Port ");
if (cfgdata != NULL) {
    cfg = audit_encode_nv_string("data", cfgdata, 0);
    if (cfg == NULL) {
        /* Handle fatal out-of-memory condition. */
    } else {
        strncat(aubuf, cfg, 130);
        free(cfg);
    }
}

audit_log_user_message(audit_fd, AUDIT_USYS_CONFIG, aubuf, hostname, NULL, NULL, result);
```

### Building with and linking in the audit library

In order to successfully compile your module and link in the audit library, you will need to modify your repo's recipe file and CMake file.  We will use the ops-cli repo as an example.  The following are changes needed to use the audit library in the VTYSH code, which is in the ops-cli repo.  First you need to make changes to the repo's recipe file which is normally located at yocto/openswitch/meta-distro-openswitch/recipes-ops/mgmt/ops-cli.bb.  You need to edit the recipe and add "audit" to the DEPENDS and RDEPENDS_${PN} lines.  For example:

	DEPENDS = "ops-utils ops-ovsdb audit"
    RDEPENDS_${PN} = "audit"

If your recipe does not have a DEPENDS or RDEPENDS_${PN} statement, add them.  Next you need to go to the repo's source code directory and make a change to the CMakeLists.txt file.  For the ops-cli repo, this is located in the "src/ops-cli/vtysh" directory.  Edit the CMakeLists.txt file and find the target_link_libraries line.  Add "audit" to the end of the list.  For example:

	target_link_libraries(vtysh PUBLIC
	  ${OVSCOMMON_LIBRARIES}
	  ${OVSDB_LIBRARIES}
	  ${OPSCLI_LIBRARIES}
	  crypt pthread readline ops-cli audit)


## Interpreting and displaying audit log events

**WARNING**:  Currently the Audit Framework does not write audit events to the audit log file when running inside a docker container.  This means a physical switch is needed to see the audit events.  The default audit log file is located at /var/log/audit/audit.log.  A typical raw log record appears as follows:

	type=USYS_CONFIG msg=audit(1446776250.787:91): pid=540 uid=1002 auid=4294967295 ses=4294967295 msg='op=CLI:Set-Hostname data="newHostName" exe="/usr/bin/vtysh" hostname=? addr=? terminal=pts/1 res=success

This particular record was generated by prototype code calling the audit_log_user_message() function in vtysh. Most fields are self-explanatory. Several fields match the parameters supplied in the audit_log_user_message() function. Explanations for some fields are as follows:

- **msg=audit(1446776250.787:91)** is the time stamp and event number. The time stamp value is 1446776250.787 and the event number is 91.

- **pid=540** is the process ID of the program that made the audit log call.

- **uid=1002** is the user ID of the program that made the audit log call.

- **auid=4294967295** is the login user ID. This specific value represents -1 for a "C" int and indicates the value is not set.

- **ses=4294967295** is the session ID, if any. In this case, it is not set.

- **op=CLI:Set-Hostname data="newHostName"** is the content of the message parameter passed to audit_log_user_message().

The *ausearch* utility is used to display audit log events. Note that all audit utilities are restricted to the root user. To get easier to read output, use the "-i" or "--interpret" option. Consult the man page for more infromation about the many options available for this utility. If *"ausearch -i -a 91"* was issued to display event number 91, it would output the following:

```
type=USYS_CONFIG msg=audit(11/06/15 02:17:30.787:91) : pid=540 uid=fredf auid=unset ses=unset msg='op=CLI:Set-Hostname data="newHostName"exe=/usr/bin/vtysh hostname=? addr=? terminal=pts/1 res=success'
```

The other main audit utility is *aureport*, which is used to get a variety of summary reports. Read the man page for additional details. Running *aureport* without any options displays the following summary:

	Summary Report
	======================
	Range of time in logs: 01/08/01 07:11:42.847 - 11/06/15 03:01:02.171
	Selected time for report: 01/08/01 07:11:42 - 11/06/15 03:01:02.171
	Number of changes in configuration: 2
	Number of changes to accounts, groups, or roles: 5
	Number of logins: 0
	Number of failed logins: 0
	Number of authentications: 3
	Number of failed authentications: 5
	Number of users: 1
	Number of terminals: 5
	Number of host names: 3
	Number of executables: 8
	Number of commands: 3
	Number of files: 0
	Number of AVC's: 0
	Number of MAC events: 0
	Number of failed syscalls: 0
	Number of anomaly events: 0
	Number of responses to anomaly events: 0
	Number of crypto events: 0
	Number of integrity events: 0
	Number of virt events: 0
	Number of keys: 0
	Number of process IDs: 14
	Number of events: 92

A typical report for OpenSwitch is a configuration report using *aureport -c*, which displays the following:

	Config Change Report
	===================================
	# date time type auid success event
	===================================
	1. 11/06/15 02:17:30 USYS_CONFIG -1 yes 91
	2. 11/06/15 02:17:30 USYS_CONFIG -1 yes 93

## Additional references

* [Linux Audit Framework web site](http://people.redhat.com/sgrubb/audit/)
* ["Guide to writing well formed audit events" white paper](http://people.redhat.com/sgrubb/audit/audit-events.txt)
* [Linux Audit Quick Start](https://www.suse.com/documentation/sles11/singlehtml/audit_quickstart/audit_quickstart.html)
* [Red Hat Enterprise Linux 7 Security Guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Security_Guide/index.html)
* [SUSE Linux Enterprise Desktop 11 Security Guide](https://www.suse.com/documentation/sled11/book_security/data/book_security.html)
