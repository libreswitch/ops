# REST API

## Contents

- [Overview](#overview)
- [How to use this feature](#how-to-use-this-feature)
  - [Setting up the basic configuration](#setting-up-the-basic-configuration)
  - [Troubleshooting the configuration](#troubleshooting-the-configuration)
    - [Condition](#condition)
    - [Cause](#cause)
    - [Remedy](#remedy)
  - [Entry point](#entry-point)
- [CLI](#cli)
- [Related features](#related-features)
- [Notifications](#notifications)
  - [Subscribing](#subscribing)
  - [Notification message](#notification-message)
  - [Notifications over WebSockets](#notifications-over-websockets)

## Overview
The REST_API provides a management interface to interact with a switch. You can utilize the API to retrieve status and statistics information of the switch, as well as to set and change the configuration of the switch.

This feature provides two major functionalities:

- REST API service engine -- Processes REST API operation requests.

- REST API documentation rendering engine -- Presents a web interface documenting the supported REST API. You can interact with the REST API service engine running on the same switch through this web interface.

## How to use this feature

### Setting up the basic configuration

This feature is included in the switch image build and is enabled by default. This feature cannot be turned off through CLI. You do not need to do anything other than basic network connectivity to the switch to use this feature.

### Troubleshooting the configuration

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

## CLI
This feature is an alternative to the CLI mechanism as a management interface. It has no CLIs of its own.

## Related features
The configuration daemon and API modules utilize configuration read and write capabilities provided by this feature in the form of Python libraries.

## Notifications
Resources can be subscribed to for monitoring resource additions, changes, and deletions that trigger notifications to the client. The client can subscribe to specific resources or a collection of resources. For example, the client can subscribe to changes for a BGP router with ASN `6001`, or to a collection of BGP routers that belong to a VRF with the name `vrf_default`.

When a client subscribes to a specific resource, the client will be notified of its initial values, its updated values when the resource is modified, or notified when the resource is deleted. When a client subscribes to a collection of resources, the client will be notified of its initial values, and when other resources within the same collection subscription is added or deleted. Clients can have multiple subscriptions.

### Subscribing
The subscribing mechanism is through REST APIs. To create a new subscription, the client must send a POST request to the URI of the subscriber. For example, if the subscriber name is "subscriber_1", the URI to send a POST request to is:
`https://ip_address/rest/v1/system/notification_subscriber/subscriber_1/notification_subscription`

The data for the POST request contains the `name` of the subscription that is unique to the subscriber and a `resource` URI that may be for a specific resource or for a collection.

For a specific resource, the `resource` may look like the following: `/rest/v1/system/vrfs/vrf_default/bgp_routers/6001`.

For a collection, the `resource` may look like the following: `/rest/v1/system/vrfs/vrf_default/bgp_routers`

### Notification message
When a monitored resource change is detected, a notification is sent to the client in a JSON formatted message, which includes the resources `added`, `modified`, or `deleted`. Each notification includes the values, subscription URI, and resource URI, except for a deleted resource that excludes the resource's values.

The notification message may look like the following:
```
{
    "notifications": {
        "added": [{
            "subscription": "/rest/v1/system/notification_subscribers/3562910982/notification_subscriptions/subscription_1",
            "resource": "/rest/v1/system/vrfs/vrf_default/bgp_routers/1/bgp_neighbors/2.2.2.2",
            "values": {
                "remote_as": 2
            }
        }],
        "modified": [{
            "subscription": "/rest/v1/system/notification_subscribers/3562910982/notification_subscriptions/subscription_2",
            "resource": "/rest/v1/system/vrfs/vrf_default/bgp_routers/1",
            "new_values": {
                "router_id": "1.1.1.1",
                "maximum_paths": 5,
            }
        }],
        "deleted": [{
            "subscription": "/rest/v1/system/notification_subscribers/3562910982/notification_subscriptions/subscription_3",
            "resource": "/rest/v1/system/vrfs/vrf_default/bgp_routers/1/bgp_neighbors/3.3.3.3"
        }]
    }
}
```

### Notifications over WebSockets
Notifications are currently only supported over WebSockets. When a client connects to the server through WebSockets at the `wss://ip_address/rest/v1/ws/notifications` URI, a notification subscriber resource with a random generated subscriber name is automatically created. The subscriber name can be used for creating subscriptions through REST. When changes are detected, notifications are sent to the client through the WebSocket.
