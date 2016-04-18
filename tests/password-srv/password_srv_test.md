# Password Server Test Cases

## Contents
- [Update password for netop](#Update-password-for-netop)
- [Update password with invalid old password] (#Invalid-old-password)

## Update password for netop
### Objective
The objective of the test case is to verify whether or not the update of the password for user netop is successfully performed via the CLI.

### Requirements
The requirements for this test case are:

- OpenSwitch
- Ubuntu Workstation

#### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```

### Description
Update the password via the CLI.

#### Steps

1. Connect user `netop` to the switch via SSH.
2. Run the `password` CLI command
3. Enter the old-password `netop` (netop is the default password for user netop).
4. Enter the new password `1111`.
5. Log out of SSH.
6. Reconnect user `netop` to the switch via SSH.
7. Verify that the password `1111` is required to log on to the switch.

### Test result criteria
#### Test pass criteria
- After Step 4, "Password update executed successfully." must be the CLI output.
- Logging on must be successful after using the new password `1111` in Step 6.

#### Test fail criteria
- After Step 4, "Password update executed successfully." is not displayed.
- Logging on cannot be done with the new password in Step 6.

## Invalid old password
### Objective
The objective of the test case is to verify that the password update fails when a user
does not provide the correct password.

### Requirements
The requirements for this test case are:

- OpenSwitch
- Ubuntu Workstation

#### Setup
#### Topology diagram
```ditaa
+---------------+                 +---------------+
|               |                 |    Ubuntu     |
|  OpenSwitch   |eth0---------eth1|               |
|               |      lnk01      |  Workstation  |
+---------------+                 +---------------+
```

### Description
User `netop` provides the invalid old password to update the password.

#### Steps

1. Connect user `netop` to the switch via SSH
2. Run the `password' CLI command
3. Enter the old-password as 'netop22' (Netop (all lowercase) is the default password for user netop).
4. Enter the new password '1111'
6. Verify that the "Old password did not match." message is displayed.
6. Log out of SSH.
7. Reconnect the user 'netop' to the switch via SSH.
8. Verify that the logon failed with a new password '1111'.

### Test result criteria
#### Test pass criteria
- After Step 4, the CLI must display the error "Old password did not match".
- Logon fails using the new password '1111' in Step 6.

#### Test fail criteria
- After Step 4, "Password update executed successfully." is not shown
- Logging on cannot be done with the new password in Step 6.