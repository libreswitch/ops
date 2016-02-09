# Authentication, Authorization, and Accounting (AAA) feature

- [High level design of ops-aaa-utils](#high-level-design-of-ops-aaa-utils)
	- [Design choices](#design-choices)
	- [Participating modules](#participating-modules)
	- [OVSDB-Schema](#ovsdb-schema)
	- [References](#references)

#High level design of ops-aaa-utils
The Authentication, Authorization, and Accounting (AAA) feature leverages Linux PAM (Pluggable Authentication Modules) to provide authentication for user based login access to services (SSH,Console,REST)running on the switch. The `pam_unix.so `and `pam_radius_auth.so` are used for local and Radius based authentication respectively for users added on the device. Refer to `AAA_Component_Design.md `for more details on PAM.
REST service generates a secure cookie on an initial user login by the REST Client. Subsequent requests from the REST client are then authenticated based on the secure cookie contained in them until the cookie expires. The AAA feature provides either password or publicKey based SSH access to the switch by leveraging the openSSH daemon's file based configuration options.

##Design choices
When there is a choice between Linux PAM(http://www.linux-pam.org/) and `openPAM`(http://www.openpam.org/), Linux PAM is the better choice because it supports a larger number of modules.

##Participating modules
```ditaa
                                                    +-----------------+      +----------+
                                                    |                 |      |   SSHd    |
                                                    | AAA Daemon      +------>  Config  |
                                                    |                 |      |  file    |
                                                    +---------------+-+      +----------+
                                                                    |
                                                                    |
                                                                    |
+----------------+           +----------------------+             +-v------------------+
|   Applications +----------->                      +------------->  /etc/pam.d        |
|SSH,Console,REST|           |     Linux PAM        |             |  config files      |
|                <-----------+                      <-------------+ SSH,Console,REST   |
+----------------+           +-----+-------^--------+             |                    |
                                   |       |                      +--------------------+
                                   |       |
                                   |       |
                                   |       |
                                   |       |
                              +----v-------+--------+
                              |                     |
                              |     PAM Module      |
                              | pam_unix,           |
                              | pam_radius_auth,    |
                              | pam_radius_chap_auth|
                              +---------------------+

```

##OVSDB-Schema
For information about the OVSDB schema, refer [here](documents/dev/ops-aaa-utils/design).

##References

* Click [here](documents/dev/ops-aaa-utils/design) for AAA Design.
* Click [here](documents/user/aaa_user_guide) for AAA user guide.
* Click [here](documents/user/AAA_cli) for AAA CLI guide.
