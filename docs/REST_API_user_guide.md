# REST API

## Overview ##
The REST_API provides a management interface to interact with a switch. You can utilize the API to retrieve status and statistics information of the switch, as well as to set and change the configuration of the switch.

This feature provides two major functionalities:

- REST API service engine -- Processes REST API operation requests.

- REST API documentation rendering engine -- Presents a web interface documenting the supported REST API. You can interact with the REST API service engine running on the same switch through this web interface.

## How to use this feature ##

###Setting up the basic configuration

This feature is included in the switch image build and is enabled by default. This feature cannot be turned off through CLI. You do not need to do anything other than basic network connectivity to the switch to use this feature.

###Troubleshooting the configuration

#### Condition
Error in accessing the URIs supported by the REST API.
#### Cause
- Switch network connectivity issue
- REST daemon fails to start or has crashed
#### Remedy
- Ping the switch at the given IP address after making sure that the IP address is configured for the management interface of the switch.
- Make sure that the REST daemon is running.

### Entry point

The URL for accessing REST API documentation rendered on the switch is:
```ditaa
    https://management_interface_ip_address-or-switch_name/api/index.html
```

The default HTTPS port is 443. When http is used (port 80), requests get redirected to https (port 443).

To access details about the supported REST API without running a switch image, see the following website for information:
```ditaa
    http://api.openswitch.net/rest/dist/index.html
```

## CLI ##
This feature is an alternative to the CLI mechanism as a management interface. It has no CLIs of its own.

## Related features ##
The configuration daemon and API modules utilize configuration read and write capabilities provided by this feature in the form of Python libraries.
