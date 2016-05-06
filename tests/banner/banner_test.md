# Banner feature test cases

- [Test Cases](#test-cases)
    - [Test case 1a - Restore default pre-login banner](#test-case-1a-restore-default-pre-login-banner)
    - [Test case 1b - Restore default post-login banner](#test-case-1b-restore-default-post-login-banner)
    - [Test case 1c - Restore default pre-login banner as invalid user](#test-case-1c-restore-default-pre-login-banner-as-invalid-user)
    - [Test case 1d - Restore default post-login banner as invalid user](#test-case-1d-restore-default-post-login-banner-as-invalid-user)
    - [Test case 2a - Customize the pre-login banner](#test-case-2a-customize-the-pre-login-banner)
    - [Test case 2b - Customize the post-login banner](#test-case-2b-customize-the-post-login-banner)
    - [Test case 2c - Customize the pre-login banner as invalid user](#test-case-2c-customize-the-pre-login-banner-as-invalid-user)
    - [Test case 2d - Customize the post-login banner as invalid user](#test-case-2d-customize-the-post-login-banner-as-invalid-user)
    - [Test case 3a - Disable the pre-login banner](#test-case-3a-disable-the-pre-login-banner)
    - [Test case 3b - Disable the post-login banner](#test-case-3b-disable-the-post-login-banner)
    - [Test case 3c - Disable the pre-login banner as invalid user](#test-case-3c-disable-the-pre-login-banner-as-invalid-user)
    - [Test case 3d - Disable the post-login banner as invalid user](#test-case-3d-disable-the-post-login-banner-as-invalid-user)
    - [Test case 4a - Display the pre-login banner](#test-case-4a-display-the-pre-login-banner)
    - [Test case 4b - Display the post-login banner](#test-case-4b-display-the-post-login-banner)

#Test cases
##  Verify the custom login banners feature
### Objective
Verify the custom login banners feature.
### Requirements
The requirement for this test case is Docker version 1.10 or above.

### Setup
#### Topology

```ditaa
              +------------------------+
              |                        |
              |  Openswitch container  |
              |                        |
              +------------------------+
```
#### Test setup
None.

### Test case 1a - Restore default pre-login banner
### Description
Restore the default pre-login banner and confirm that the expected string is
displayed in a new SSH session.
### Test result criteria
#### Test pass criteria
The banner string matches the default pre-login banner string.
#### Test fail criteria
The banner string does not match the default pre-login banner string.

### Test case 1b - Restore default post-login banner
### Description
Restore the default post-login banner and confirm that the expected string is
displayed in a new SSH session.
### Test result criteria
#### Test pass criteria
The banner string matches the default post-login banner string.
#### Test fail criteria
The banner string does not match the default post-login banner string.

### Test case 1c - Restore default pre-login banner as invalid user
### Description
Issue a command to restore the default pre-login banner as an invalid user and confirm
that the change is not accepted.
### Test result criteria
#### Test pass criteria
The banner string is unchanged.
#### Test fail criteria
The banner string is changed.

### Test case 1d - Restore default post-login banner as invalid user
### Description
Issue the command to restore default the post-login banner as an invalid user and
confirm that the change is not accepted.
### Test result criteria
#### Test pass criteria
The banner string is unchanged.
#### Test fail criteria
The banner string is changed.

### Test case 2a - Customize the pre-login banner
### Description
Modify the pre-login banner with a known string and confirm the expected string
is displayed in a new SSH session.
### Test result criteria
#### Test pass criteria
The banner string matches the known string.
#### Test fail criteria
The banner string does not match the known string.

### Test case 2b - Customize the post-login banner
### Description
Modify the post-login banner with a known string and confirm that the expected
is displayed in a new SSH session.
### Test result criteria
#### Test pass criteria
The banner string matches the known string.
#### Test fail criteria
The banner string does not match the known string.

### Test case 2c - Customize the pre-login banner as invalid user
### Description
Modify the pre-login banner as an invalid user and confirm that the banner
remains unchanged.
### Test result criteria
#### Test pass criteria
The banner string is unchanged.
#### Test fail criteria
The banner string is changed.

### Test case 2d - Customize the post-login banner as invalid user
### Description
Modify the post-login banner as an invalid user and confirm that the banner
remains unchanged.
### Test result criteria
#### Test pass criteria
The banner string is unchanged.
#### Test fail criteria
The banner string is changed.

### Test case 3a - Disable the pre-login banner
### Description
Disable the pre-login banner and confirm that no text is displayed before the
login prompt in a new SSH session.
### Test result criteria
#### Test pass criteria
No text is displayed before the login prompt.
#### Test fail criteria
Unexpected non-whitespace characters are displayed before the login prompt.

### Test case 3b - Disable the post-login banner
### Description
Disable the post-login banner and confirm that no text is displayed after the
login prompt and before the shell prompt in a new SSH session.
### Test result criteria
#### Test pass criteria
No unexpected text is displayed after the login prompt and before the shell
prompt.
#### Test fail criteria
Unexpected non-whitespace characters are displayed after the login prompt and
before the shell prompt.

### Test case 3c - Disable the pre-login banner as invalid user
### Description
Disable the pre-login banner as an invalid user and confirm that no change is
made to the banner.
### Test result criteria
#### Test pass criteria
No change is made to the banner.
#### Test fail criteria
The banner is disabled.

### Test case 3d - Disable the post-login banner as invalid user
### Description
Disable the post-login banner as an invalid user and confirm that no change is
made to the banner.
### Test result criteria
#### Test pass criteria
No change is made to the banner.
#### Test fail criteria
The banner is disabled.

### Test case 4a - Display the pre-login banner
### Description
Use the show command to display the pre-login banner and confirm that it matches
an expected value.
### Test result criteria
#### Test pass criteria
Displayed banner matches an expected value.
#### Test fail criteria
Displayed banner does not match an expected value.

### Test case 4b - Display the post-login banner
### Description
Use the show command to display the post-login banner and confirm that it
matches an expected value.
### Test result criteria
#### Test pass criteria
Displayed banner matches an expected value.
#### Test fail criteria
Displayed banner does not match an expected value.
