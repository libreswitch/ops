# Banner CLI Commands

## Contents

- [Default banner commands](#default-banner-commands)
    - [Restore default pre-login banner](#restore-default-pre-login-banner)
    - [Restore default post-login banner](#restore-default-post-login-banner)
- [Custom banner commands](#custom-banner-commands)
    - [Customize the pre-login banner](#customize-the-pre-login-banner)
    - [Customize the post-login banner](#customize-the-post-login-banner)
- [Disable banner commands](#disable-banner-commands)
    - [Disable the pre-login banner](#disable-the-pre-login-banner)
    - [Disable the post-login banner](#disable-the-post-login-banner)
- [Display banner commands](#display-banner-commands)
    - [Show the pre-login banner](#show-the-pre-login-banner)
    - [Show the post-login banner](#show-the-post-login-banner)

## Default banner commands
### Restore default pre-login banner
#### Syntax
`banner default`
#### Description
This command enables the pre-login banner feature and sets the string to be
displayed to a predefined default. This default is non-customizable.
#### Authority
Users in group ops\_netop may execute this command.
#### Parameters
No parameters.
#### Examples
```
switch# configure terminal
switch(config)# banner default
Banner updated successfully!
```
### Restore default post-login banner
#### Syntax
`banner exec default`
#### Description
This command enables the post-login banner feature and sets the string to be
displayed to a predefined default. This default is non-customizable.
#### Authority
Users in group ops\_netop may execute this command.
#### Parameters
No parameters.
#### Examples
```
switch# configure terminal
switch(config)# banner exec default
Banner updated successfully!

```

## Custom banner commands
### Customize the pre-login banner
#### Syntax
`banner <delimeter>`
#### Description
This command allows you to specify a custom string that is displayed
to users attempting to connect to management interfaces on a switch.
#### Authority
Only users in group ops\_netop may execute this command.
#### Parameters
| Parameter | Status   | Syntax | Description                         |
|-----------|----------|--------|-------------------------------------|
| delimeter | Required | string | Specifies the end of the user input |
#### Examples
```
switch# configure terminal
switch(config)# banner $
Enter a new banner, when you are done enter a new line containing only your
chosen delimeter.
>> This is an example of a custom login banner
>> that spans multiple lines.
>> $
Banner updated succesfully!

```

### Customize the post-login banner
#### Syntax
`banner exec <delimeter>`
#### Description
This command allows the user to specify a custom string that will be displayed
to users who have connected to a management interface on the switch and
authenticated.
#### Authority
Only users in group ops\_netop may execute this command.
#### Parameters
| Parameter | Status   | Syntax | Description                         |
|-----------|----------|--------|-------------------------------------|
| delimeter | Required | string | Specifies the end of the user input |
#### Examples
```
switch# configure terminal
switch(config)# banner $
Enter a new banner, when you are done enter a new line containing only your
chosen delimeter.
>> This is a post-login banner.
>> $
Banner updated succesfully!
```

## Disable banner commands
### Disable the pre-login banner
#### Syntax
`no banner`
#### Description
This command replaces the pre-login banner string with an empty string, which
functionally disables the banner.
#### Authority
Only users in group ops\_netop may execute this command.
#### Parameters
No parameters.
#### Examples
```
switch# configure terminal
switch(config)# no banner
Banner updated succesfully!
switch(config)#

```

### Disable the post-login banner
#### Syntax
`no banner exec`
#### Description
This command replaces the post-login banner string with an empty string, which
functionally disables the banner.
#### Authority
Only users in group ops\_netop may execute this command.
#### Parameters
No parameters.
#### Examples
```
switch# configure terminal
switch(config)# no banner exec
Banner updated succesfully!
switch(config)#
```
## Display banner commands

### Show the pre-login banner
#### Syntax
`show banner`
#### Description
This command displays the pre-login banner.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
switch# show banner

Welcome to OpenSwitch
```

### Show the post-login banner
#### Syntax
`show banner exec`
#### Description
This command displays the post-login banner.
#### Authority
All users.
#### Parameters
No parameters.
#### Examples
```
switch# show banner exec

Please be responsible
```
