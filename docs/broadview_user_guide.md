# BroadView Daemon

## Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Basic configuration](#basic-configuration)


## Overview
The Broadcom [BroadView](https://github.com/Broadcom-Switch/BroadView-Instrumentation) software suite provides visibility into Broadcom switch silicon, exposing various instrumentation capabilities.

The software suite consists of an *agent* that runs on the switch, and an *application* that runs on a remote device. The application communicates with the agent using the Open REST API. The application analyzes and visualizes data provided by the agent, and enables administrators to fine-tune BST parameters.

In OpenSwitch, the agent is implemented by the BroadView daemon. The daemon provides instrumentation capability for OpenSwitch. In the current release, it obtains MMU buffer statistics from Broadcom silicon and exports them via the REST API. This allows applications (instrumentation collectors) to obtain MMU Buffer statistics, visualize buffer utilization patterns, and detect microbursts. This information provides administrators with visibility into the network and switch performance, and lets them fine-tune the network.

The BroadView daemon is recommended for use with OpenSwitch running on a hardware platform (such as the AS5712 from Accton). The daemon runs as a background process in OpenSwitch.

## Prerequisites
An application must be installed on a remote device to retrieve MMU buffer statistics from the agent on the switch via the REST API.

## Basic configuration
  1. Configure the IP address of the remote device running the application which will retrieve the statistics with the command:

   `broadview client ip <ip-address> port <port-num>`

  For example:

    `switch(config)# broadview client ip 10.130.168.30 port 8080`

  2. Configure the port on which the agent will communicate with the remote device with the command:

  `broadview agent-port <port-num>`

  For example:

    `switch(config)# broadview agent-port 8080`

  3. Verify the configuration with the command:

  `show broadview`

   For example:
   ```
   switch# show broadview
   BroadView client IP is 10.130.168.30
   BroadView client port is 8080
   BroadView agent port is 8080
   ```
