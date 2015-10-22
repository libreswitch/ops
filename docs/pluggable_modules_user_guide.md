# Pluggable modules

- [Overview](#overview)
- [How to setup and configure pluggable modules](#how-to-setup-and-configure-pluggable-modules)
	- [Setting up the basic configuration](#setting-up-the-basic-configuration)
	- [Configuring split interfaces](#configuring-split-interfaces)
	- [Verifying the configuration](#verifying-the-configuration)
	- [Troubleshooting](#troubleshooting)
- [CLI](#cli)
- [Related features](#related-features)
- [External references](#external-references)

## Overview
Pluggable modules, including SFP, SFP+, and QSFP+ transceiver modules, allow a network designer to select from several physical transports instead of having fixed copper or optical transceivers. Direct Attach Copper cables (DACs) may be used to connect two SFP+ (or QSFP+) ports without dedicated transceivers over relatively short distances (typically 1 to 7 meters for passive cables), while optical transceivers may support distances of multiple kilometers.

SFP modules support speeds up to 1 Gb, while SFP+ modules support 10-Gb line rate.

QSFP+ modules include 40-Gb DAC modules, 40-Gb optical transceivers, and 10-Gb 4X transceivers (which split the four lanes of a QSFP+ module into individual interfaces).

## How to setup and configure pluggable modules

### Setting up the basic configuration

Refer to the switch manufacturer's documentation to determine available receptacle types and supported module variants.
 1. Insert the modules in the receptacles, and attach cables between modules in switch and modules in server, switch, or other network device.
 1. Configure interfaces for operation as described in [Interface User Guide](/documents/user/interface_user_guide).

### Configuring split interfaces
**Note**: For QSFP modules that split a connector into multiple separate interfaces, additional configuration is required. There is no industry standard defined for detecting split QSFP modules, so you must configure the interface to identify the QSFP as split. See the [split](/documents/user/interface_cli#intfsplit) CLI interface command.

1. Enter configuration mode.
```bash
ops-xxxx# configure terminal
```
2. Select interface to be configured for split operation.
```bash
ops-xxxx(config)# interface 49
```
3. Configure split operation.
```bash
ops-xxxx(config-if)# split
```

Once an interface is configured for split operation, the individual 10-Gb interfaces (e.g., 49-1, 49-2, 49-3, and 49-4) can be configured and used.

To disable split operation for an interface use the `no split` CLI interface command.

1. Enter configuration mode.
```bash
ops-xxxx# configure terminal
```
2. Select interface to be configured for non-split operation.
```bash
ops-xxxx(config)# interface 49
```
3. Configure non-split operation.
```bash
ops-xxxx(config-if)# no split
```

## Verifying the configuration

Display the pluggable module information using the `show interface transceiver` command. See the [show interface transceiver](/documents/user/interface_cli#showalltransintf) command reference for more information.

Display the split operation configuration (and other configuration) for an interface using the `show running-config interface` command.

## Troubleshooting

### The SFP, SFP+, or QSFP+ is not detected.
#### The module may not be properly seated in the receptacle.
##### Remedy
Check that the module is inserted with the correct orientation and has established good mechanical interlock with the receptacle.
#### The module is not inserted in the correct slot.
##### Remedy
Verify that the module is inserted in the correct receptacle.
### The interface does not establish link.
#### The interface is not configured properly.
##### Remedy
Refer to interface documentation.
#### The module is not present or is not fully inserted.
##### Remedy
Verify that the module is present and properly inserted in the receptacle.
#### The cable (optical or copper) is not attached to the module.
##### Remedy
Attach the cable.
#### The remote end of the cable or module is not properly connected to the remote device.
##### Remedy
Attach the cable and the module to the remote device.
#### The remote device is not configured to establish link.
##### Remedy
Configure the remote device to enable an interface.
#### The remote module is not the same variant (incompatible technologies).
##### Remedy
Only use compatible module types at either end of a network connection.

## CLI
Click [here](/documents/user/interface_cli) for the CLI commands related to interfaces and pluggable modules.

## Related features
See also the [Interface User Guide](/documents/user/interface_user_guide) for information on configuring physical interfaces.

## External references
[Small Formfactor Pluggable](https://en.wikipedia.org/wiki/Small_form-factor_pluggable_transceiver "Wikipedia")
[Direct Attach](https://en.wikipedia.org/wiki/10_Gigabit_Ethernet#SFP.2B_Direct_Attach "Wikipedia")
[Quad Small Formfactor Pluggable](https://en.wikipedia.org/wiki/QSFP "Wikipedia")
