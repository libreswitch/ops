<!--  See the https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet for additional information about markdown text.
Here are a few suggestions in regards to style and grammar:
* Use active voice. With active voice, the subject is the doer of the action. Tell the reader what
to do by using the imperative mood, for example, Press Enter to view the next screen. See https://en.wikipedia.org/wiki/Active_voice for more information about the active voice.
* Use present tense. See https://en.wikipedia.org/wiki/Present_tense for more information about using the present tense.
* Avoid the use of I or third person. Address your instructions to the user. In text, refer to the reader as you (second person) rather than as the user (third person). The exception to not using the third-person is when the documentation is for an administrator. In that case, *the user* is someone the reader interacts with, for example, teach your users how to back up their laptop.
* See https://en.wikipedia.org/wiki/Wikipedia%3aManual_of_Style for an online style guide.
Note regarding anchors:
--StackEdit automatically creates an anchor tag based off of each heading.  Spaces and other nonconforming characters are substituted by other characters in the anchor when the file is converted to HTML.
 -->

#Log-rotate
<!--Provide the title of the feature-->

- [Overview](#overview)
- [How to use the feature](#how-to-use-the-feature)
- [Changing the default threshold values for log rotation](#changing-the-default-threshold-values-for-log-rotation)
- [Setting up the optional configuration](#setting-up-the-optional-configuration)
- [Verifying the configuration](#verifying-the-configuration)
- [Troubleshooting the configuration](#troubleshooting-the-configuration)


## Overview ##
 <!--Provide an overview here. This overview should give the reader an introduction of when, where and why they would use the feature. -->

Logrotate rotates and compresses the log files either based on period or based on size or based on both period and size (whichever condition triggers first). Rotated log files are stored locally or transferred to the remote destination.

## How to use the feature ##

With no initial configuration , logrotate runs as an hourly cron job from the `/etc/cron.hourly` path with the following default configuration,
```bash
    h1# show logrotate
    Logrotate configurations :
    Period            : daily
    Maxsize           : 10MB
```
All rotated logs are stored locally.

As per this configuration, the default behavior is that the log rotation feature rotates the log files daily. Log rotation is also triggered if the maximum file size exceeds 10 MB. Out of the period and size, whichever condition occurs first, triggers the log rotation.

###Changing the default threshold values for log rotation

Use the `logrotate` CLI command to change the default threshold values for period and file size.

```bash
 logrotate period (hourly| daily| weekly | monthly )
 logrotate maxsize <1-200>
```

###Setting up the optional configuration

Identify a remote host for receiving rotated log file by using the following CLI command:
```bash
 logrotate target  { tftp://A.B.C.D | tftp://X:X::X:X }
```

 Only the TFTP protocol is supported for remote transfer.
 Both IPv4 and IPv6 host addresses are supported.

###Verifying the configuration

- Verify log rotation parameters by running the following command:
```bash
    h1# show logrotate
    Logrotate configurations :
    Period            : weekly
    Maxsize           : 20MB
    Target            : tftp://2001:db8:0:1::128
```

- Verify Log-rotate configuration CLIs  with the *show running-config* command.

### Troubleshooting the configuration

#### Condition 1
<!-- Type the symptoms for the issue. -->

#### Log-rotation is not happening regardless of 'period' value.

##### Cause
<!-- Type the cause for the issue. -->

Log-rotate does not happen for empty files (i.e if file size is zero)

##### Remedy
<!--Type the solution. -->

Log-rotate happens when file size is greater than zero
#### Condition 2
<!-- Type the symptoms for the issue. -->

##### Rotated log files are not transferred to remote host

##### Cause
<!-- Type the cause for the issue. -->

1. The remote host might not be reachable
2. The Tftp server on the remote host might not have sufficient privileges for file creation

##### Remedy
<!--Type the solution. -->

1. Verify that the remote host is reachable.
2. Ensure that the TFTP server is configured with the required file creation permissions.
	1. For example, in tftpd-hpa server, change the configuration file in `/etc/default/tftpd-hpa` to include `-c` in TFTP_OPTIONS. (for example, `TFTP_OPTIONS="--secure -c"`).

#### Condition 3
<!-- Type the symptoms for the issue. -->

#### Log rotation does not occur immediately after the maximum file size for the log file is reached.

##### Cause
<!-- Type the cause for the issue. -->

The log rotation checks the size of the file on the first minute of every hour. If the maximum file size is reached in the meantime, the log rotation does not occur until the next hourly check of the file size.

##### Remedy
<!--Type the solution. -->

Log rotation is working as designed. The log rotation feature is designed to check the file size on an hourly basis.

## CLI ##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](http://www.openswitch.net/documents/user/Logrotate_cli) for the CLI commands related to the logrotate feature.
