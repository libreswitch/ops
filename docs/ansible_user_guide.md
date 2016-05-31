# Ansible User Guide

## Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Ansible installation](#ansible-installation)
	- [Setting up the basic configuration on a control machine](#setting-up-the-basic-configuration-on-a-control-machine)
		- [Default configuration for Ansible](#default-configuration-for-ansible)
		- [Declaring an inventory/hosts file](#declaring-inventory/hosts-file)
	- [Verifying Ansible installation](#verifying-ansible-installation)
- [Playbooks](#playbooks)
- [Roles](#roles)
	- [Ansible galaxy](#ansible-galaxy)
- [Communicating with Openswitch](#communicating-with-openswitch)
	- [SSH communication with Openswitch](#ssh-communiation-with-openswitch)
- [How to write Ansible role for OpenSwitch VLAN](#how-to-write-ansible-role-for-openswitch-vlan)
	- [Create and initialize VLAN role](#create-and-initialize-vlan-role)
	- [Create templates based on schema](#create-templates-based-on-schema)
	- [Simple playbook to create VLAN](#simple-playbook-to-create-vlan)
- [References](#references)

## Overview
This guide provides details about installing Ansible, basic information about Ansible, and communicating with the Openswitch using Ansible playbooks and modules. Ansible is an IT automation tool that is lightweight and has the following characteristics:

- Ansible does not need a master server; you only need a control machine to run the playbooks and roles on the hosts.
- No need to install anything on the hosts.
- Ansible works through SSH keys.
- We only need IP reach-ability to the servers to run the scripts/playbooks.
- Managing the automation code is by writing yaml files, which is equivalent to writing human readable ordered commands.

## Prerequisites
The basic requirement to use Ansible is to have a Linux/BSD/mac/centos OS based control machine in the infrastructure. Windows machines can not be used as a control machine at this time.
It is recommended on the Ansible website to use 'pip', the Python package manager, to install Ansible.

## Installing Ansible

As per the flavor of the operating system, there are different ways to install Ansible.

Recommended by Ansible official documentation for linux:
```
$sudo pip install Ansible
```
on mac OS:
```
$brew install Ansible
```
on centos OS:
```
$yum install Ansible
```
Ansible can also be installed using apt-get provided all the package requirements are taken care of:
```
$sudo apt-get install Ansible
```

A working Ansible control machine Docker image is uploaded on the Docker hub and is used for running the tests.

The command to pull the Ansible control machine is:
```
docker pull openswitch/ansiblecm
```
Then you can access the Ansible control machine:
```
docker run -it openswitch/ansiblecm /bin/bash
```

For more information about installing Ansible on different operating systems refer to:

http://docs.ansible.com/ansible/intro_installation.html#getting-ansible

### Setting up the basic configuration on a control machine

#### Default configuration for Ansible
Settings in Ansible can be adjusted through the ansible.cfg file. If you use pip to install Ansible, the ansible.cfg file is present by default in the /etc/ansible/ directory. Changes can be made by creating the ansible.cfg file either in the home directory or in the current directory.

Here is a sample ansible.cfg file:
```
[defaults]
inventory=/etc/ansible/hosts
# disable SSH key host checking
host_key_checking = False
# make ansible use scp for ssh connection
# (default method is sftp)
scp_if_ssh = True

```

For more information about the Ansible.cfg file, refer to:

http://docs.ansible.com/ansible/intro_configuration.html

#### Declaring an inventory/hosts file

Managing the list of servers or hosts that need to be automated is done by creating  an inventory file. The inventory file is by default present in the /etc/ansible/hosts directory. The location of the inventory file can be changed by providing a specific location in the ansible.cfg file. Similar to the configuration file, the inventory file can also be created in the current directory or the home directory to overwrite the default file under /etc/ansible/hosts.

For more information about managing the inventory and options associated with the inventory, refer to:

http://docs.ansible.com/ansible/intro_inventory.html

Sample inventory:

```
[OpenSwitch]
ops ansible_host=192.168.1.10 ansible_port=22

```

#### Verifying the Ansible installation

To make sure Ansible is properly installed and all requirements are met, use the Ansible modules on the localhost.
For example:
```
$ ansible localhost -m ping
$ ansible localhost -m setup
```

## Playbooks

Playbook are used to automate, configure, and orchestrate the infrastructure. As the official documentation explains, playbooks are the design plans and modules are the tools. Playbooks contain plays, and plays contain tasks.

Sample playbook with a single play:

```
---
  #hosts to run the playbook on
- hosts: OpenSwitch
  #User that will be logged in with
  remote_user: root
  tasks:
      #Name/Caption for the task
    - name: ping the OpenSwitch
      #Ansible module to be used
      ping:
```

To run the playbook use the following command:
```
$ansible-playbook ping.yml
```

For more information on writing playbboks, refer to:

http://docs.ansible.com/ansible/playbooks_intro.html


## Roles

For a larger and more diverse architecture, the best way to manage the orchesteration is to create and use roles.
A role is an easy way to share the variables, default configuration, and host specific configuration in a structured file which is familiar to Ansible.
A role saves the duplication of playbooks and variables.

A typical structure of a role is as follows:

```
site.yml
roles/
   switch/
     files/
     templates/
     tasks/
     handlers/
     vars/
     defaults/
     meta/
```

This role can be executed on the host by running the site.yml file, which is shown below:

```
---
- hosts: OpenSwitch
  roles:
    - switch
```

For more detailed information about writing roles, refer to:

http://docs.ansible.com/ansible/playbooks_roles.html


### Ansible-galaxy

Ansible-galaxy is a website to manage the Ansible roles, and also a command line tool to create and manage roles.
Use the following command to create a role using Ansible-galaxy command:
```
$ ansible-galaxy init switch
```
**Note:** "switch" is an example role name.

For more information about Ansible-galaxy, refer to:

http://docs.ansible.com/ansible/galaxy.html


## Communicating with OpenSwitch

To communicate with the host, you need to have IP reachability. If you can ping the server, and initiate the SSH communication, you can automate the configuration on the host. Communicating with Openswitch is the same. Ansible connects to the host, in this case OpenSwitch, and pushes small programs called Ansible modules. Communication, deployment, and automation with OpenSwitch can be  achieved by using three Ansible modules that are specifically developed for OpenSwitch. For more information about these modules, refer to the respective links provided beneath each module.

- ops_template: Push the configuration to OpenSwitch

https://docs.ansible.com/ansible/ops_template_module.html

- ops_command: Run arbitrary commands on OpenSwitch devices

https://docs.ansible.com/ansible/ops_command_module.html

- ops_config: Manage the OpenSwitch configuration using CLI

https://docs.ansible.com/ansible/ops_config_module.html


These modules are used in the playbooks to be run on OpenSwitch. After execution of the modules, they are removed by Ansible. No packages or applications are installed on OpenSwitch.

### SSH communication with OpenSwitch

Passwords can be used to communicate, but SSH keys with SSH-agents are a better way to communicate. Ansible's "authorized_keys" module can be used to copy the public key from the Ansible control machine to OpenSwitch.
It is required to have an access to the management port of the OpenSwitch in order to initiate the SSH communication and run Ansible playbooks. SSH communication can not be established using any other port on the OpenSwitch.

For an example playbook written for the initial communication with the OpenSwitch, refer to:

http://git.openswitch.net/cgit/openswitch/ops-ansible/tree/examples/utility

Use the following commands to confirm the test:
```
$ git clone https://git.openswitch.net/openswitch/ops-build  ops-sim
$ cd ops-sim
$ make configure genericx86-64
$ make devenv_init
$ make devenv_add ops-ansible
$ make testenv_init
$ make testenv_run component ops-ansible

```
## How to write Ansible role for OpenSwitch VLAN

This section provides information on how to create an Ansible role for OpenSwitch VLAN configuration and testing.

### Create and initialize VLAN role
First initialize the vlan role under the <b>/etc/ansible/roles</b> folder with the ansible-galaxy API:
```
ansible-galaxy init vlan
```
Create the default file for the vlan role as <b>defaults/main.yml</b>:
```
---
# defaults/main.yml
# default remote user on the switch
remote_user: admin

# default host variable, which is required by ops_*.py modules.
ops_host: "{{ ansible_host }}"

# Enable debugging on ops_*.py modules.
ops_debug: false
```
Create the task file to configure vlan and debug configuration transaction as <b>tasks/main.yml</b>:
```
---
- name: print JSON input for this play
  debug: >
    msg="{{ lookup('template', 'main.j2') }}"
  when: ops_debug

- name: configure the bgp role
  become: yes
  ops_template:
    src: main.j2
    host: "{{ ops_host }}"
  register: ops_result

- name: result from the switch
  debug: var=ops_result
  when: ops_debug
```


### Create templates based on schema
Create <b>templates/main.j2</b> file based on schema:
```
{# OpenSwitch JSON main template file #}

{
  {%- include ['ops_system.j2'] -%}
}

```
Refer to <b>schema/vswitch.ovsschema</b> in the ops repository. The main table for ops is named <i>System</i>, and it contains the column <i>bridges</i>.
```
...
  "tables": {
    "System": {
      "columns": {
        ...
        "bridges": {
          "type": {
            "key": {
              "type": "uuid",
              "refTable": "Bridge"
            },
            "min": 0,
            "max": "unlimited"
          }
        }
  ...
```
Create a template (<b>templates/ops_system.j2</b>) to iterate through the <i>System</i> table:
```
{# OpenSwitch System table JSON template file #}

"System": {
  {# System.bridges column #}
  {%- if ops_bridges is defined -%}
    {%- include ['ops_system_bridges.j2'] -%}
  {%- endif -%}
}

```
**Note**: In the schema sample, <i>bridges</i> is referred to as <i>Bridges</i> table.
```
"refTable": "Bridge"
```
In the <i>Bridge</i> table, there is a <i>vlan</i> column that refers to the <i>VLAN</i> table.
```
"vlans": {
          "type": {
            "key": {
              "type": "uuid",
              "refTable": "VLAN"
            },
            "min": 0,
            "max": 4094
          }
         },

```
Based on this, create a template (<b>templates/ops_system_bridges.j2</b>) to iterate through the <i>bridges</i> column:
```
{# OpenSwitch System.bridges column JSON template file #}

"bridges": {
  {%- for bridge in ops_bridges -%}
    "{{- bridge.name -}}": {

      {# System.bridges.vlans column #}
      {%- if bridge.vlans is defined -%}
        {%- include ['ops_system_vlans.j2'] -%},
      {%- endif -%}

      "name": "{{- bridge.name -}}"
    } {%- if not loop.last -%} , {%- endif -%}
  {%- endfor -%}
}
```
Create the vlan template <b>templates/ops_system_vlans.j2</b>:
```
{# OpenSwitch System.bridges.vlans column JSON template file #}

"vlans": {
  {%- for vlan in bridge.vlans -%}
    "{{- vlan.name -}}": {
      {%- if vlan.admin is defined -%}
        "admin": "{{- vlan.admin -}}"
      {%- endif -%}
    } {%- if not loop.last -%} , {%- endif -%}
  {%- endfor -%}
}
```
###Simple playbook to create VLAN
Following is a simple playbook to create two vlans under the default bridge (<b>tests/create_vlan.yml</b>):

```
---
- name: create two vlans through vlan role
  hosts: ops
  gather_facts: no
  vars:
    ansible_user: admin
    ops_debug: yes
    ops_cli_provider:
      transport: cli
      username: netop
      password: netop
      host: "{{ ansible_host }}"
      port: "{{ ansible_port }}"
    ops_rest_provider:
      transport: rest
      username: netop
      password: netop
      host: "{{ ansible_host }}"
      port: "{{ ops_rest_port }}"
      use_ssl: true
      validate_certs: no

  roles:
    - role: vlan
      ops_bridges:
        - name: bridge_normal
          vlans:
            - name: "VLAN2"
              admin: "up"
            - name: "VLAN3"
              admin: "down"
```

## References
- http://www.ansible.com
- http://docs.ansible.com
