   CLI Developer Guide
=====

##Contents
- [Overview](#overview)
- [Adding CLI support for a new daemon](#adding-cli-support-for-a-new-daemon)
- [Installing a context](#installing-a-context)
 -  [install_node()](##install_node())
 -  [install_default()](##install_default()
 -  [exit/enter functions](##exit/enter-functions)
- [Installing a command](#installing-a-command)
 -   [Preparing the command spec (DEFUN)](#preparing-the-command-spec)
 -     [Terminal Tokens: ](#terminal-tokens:)
  -     [Multiple Tokens:](#multiple-tokens:)
  -     [Keyword Tokens: ](#keyword-tokens:)
  -     [Installing a command containing variables (.LINE) ](#installing-a-command-containing-variables-\(.LINE\))
  -     [Help strings ](#help-strings)
  -     [Installing a command with dynamic help string](#installing-a-command-with-dynamic-help-string)
  -     [Installing a command with integer range or comma separated list input](#installing-a-command-with-integer-range-or-comma-separated-list-input)
  -   ['No' form of configuration commands](#'no'-form-of-configuration-commands)
 -   [Hidden commands](#hidden-commands)
 -   [Disabled commands](#disabled-commands)
 -   [Show commands](#show-commands)
 -   [Example](#example)
- [Show running support for a command](#show-running-support-for-a-command)
- [User Interface Guidelines](#user-interface-guidelines)



##Overview
The command line interface (CLI) is equivalent to a command language interpreter. It has a parser which enables the developer to install a command in a desired format. The CLI parser parses this input and exposes relevant tokens to you through the command line. Your input is validated (primary validation – like range checks, valid numbers and so on ) and the your validated input is passed to the action routine handling the command execution.
OpenSwitch has a database-centric approach, where OVSDB acts as the data store also. All the daemons read the configurations from the OVSDB, and updates the OVSDB whenever there is a change in configurations, or states, or statistics. Similarly, the CLI also stores the user configuration in the OVSDB. When the data is queried, it has to read from the OVSDB and be displayed in the proper format.

This document covers the steps involved in adding CLI command support for your feature. The CLI infra code resides in the `ops-cli `repository. It has a lib folder, containing the parser logic implemented, and a 'vtysh' folder for CLI configurations (configuring the behavior of vtysh), and enhancements to the infra base code.


##Adding CLI support for a new daemon
This section covers using a CLI infra for a new daemon. If your daemon is already linked to the CLI infra and you have a few commands already installed, skip this section.

Every new daemon needs to register itself to the CLI infra to use the CLI parser functionality for its configuration. The command definitions, installations, show running-configuration logic and so on are kept inside the daemon repository. The callback functions with a predefined signature and function name have to be implemented inside the feature CLI code.
The following steps are required to deploy the CLI infra into a feature as part of build.

1. Add the  `ops-cli` dependencies to the feature specific recipe (.bb) file.	For  example, if you want to add the `ops-cli` dependencies to the `ops-mgmt-intf` feature, use the following command structure:

	DEPENDS = "ops-utils ops-ovsdb ops-cli"

2. Add the feature CLI libraries into the build package as follows:

	`FILES_${PN} += "/usr/lib/cli/plugins/"`

3. Create the `src/cli` directory under the `ops-featurename` directory. For example, use the following command structure if you want to add `src\cli` to the `ops-mgmt-intf` feature:

          `ops-mgmt-intf`
          ./src/cli
	      ./include

4. Create the  `<featurename>_vty.h` file under the `ops-featurename/include` directory. At a minimum, declare `void cli_pre_init(void)`. For example:

          #ifndef feature_VTY_H
          #define feature_VTY_H
          void cli_pre_init(void);
          #endif
5. Create the `<featurename>_vty.c` file under the `ops-featurename/src/cli` directory. At a minimum, implement `void cli_pre_init(void)`. For example:

         /* Install `<featurename>` related vty commands.*/
         void
         cli_pre_init(void)
         {
           return;
         }
a. Inside the `cli_pre_init` function, call the install_node, and the add_column/table related functions.
For example:
       void mgmt_ovsdb_init(void)
       {
           ovsdb_idl_add_column(idl, &ovsrec_system_col_mgmt_intf);
           ovsdb_idl_add_column(idl, &ovsrec_system_col_mgmt_intf_status);
       }
       void cli_pre_init(void)
       {
          install_node (&mgmt_interface_node, NULL);
          vtysh_install_default (MGMT_INTERFACE_NODE);
          mgmt_ovsdb_init();
       }
b. Call the installing element function from `cli_post_init`. For example:

        /* Initialize management interface cli element.*/
         void cli_post_init(void)
         {
             install_element (CONFIG_NODE, &vtysh_interface_mgmt_cmd);
             install_element (MGMT_INTERFACE_NODE, &vtysh_exit_mgmt_interface_cmd);
             install_element (MGMT_INTERFACE_NODE, &vtysh_end_all_cmd);
             .......
         }
6. Include the CLI dependencies header file in the feature source file as `vtysh/<dependencies file>.h`. For example:

       #include "vtysh/command.h"
       #include "vtysh/memory.h"
       #include "vtysh/vtysh.h"
       #include "vtysh/vtysh_user.h"
       #include "vtysh/vtysh_ovsdb_if.h"
       #include "vtysh/vtysh_ovsdb_config.h"
       #include "vtysh/vtysh_utils.h"

7. To include the CLI infra dependencies in the feature CLI library CMakefile/Makefile file, make the following changes:
        CMakeLists.txt file changes:
          add_definitions(-DHAVE_CONFIG_H -DHAVE_SOCKLEN_T)
		  # Rules to locate needed libraries
		  include(FindPkgConfig)
		  pkg_check_modules(OPSCLI REQUIRED ops-cli)
		  include_directories (${INCL_DIR}
	                           ${PROJECT_SOURCE_DIR}
		                       ${OPSCLI_INCLUDE_DIRS}
                               )
          # Installation
		  install(TARGETS ${LIBMGMTINTFCLI}
                  LIBRARY DESTINATION lib/cli/plugins
                  )

You are now ready to install a *command context* for your feature



##Installing a context

OpenSwitch groups the configuration commands based on the context. When you log into the CLI console, you enter the "enable" or "view" context where the **show** commands can be executed to display the current system configurations and parameters. Configuration commands are available on the"configure terminal" context. Further classification is possible as the "interface context" has physical and logical interface configurations, "router ospf" context has OSPF related configurations and so on.

If your daemon does not need a separate context and the commands can be installed in an existing context, or if the context is already implemented, skip this section.


A new context is added to the CLI parser when using the function `install_node()`; because it expects a command node structure which defines how the prompt looks when you are in that context. For example:

	static struct cmd_node ospf_node =
	{
		OSPF_NODE,
		"%s(config-router)# "
	};

#####Default commands in every context
There are few default commands that are supported in every context such as exit, end, help, list, and so on. These commands have to be installed once the context is created. Refer to "Entering a context" for information on how to install a command in a node.

#####Entering a context
The command to enter a child context has to be installed on its parent context. To enter the 'interface context', the "interface IFNAME" command is executed. This command is installed on the parent context, which is the 'configure context'.

##Installing a command

A command is the smallest entity that accepts a user configuration and updates the database or reads relevant information from the database and presents it in a properly formatted form.

To install a command, a command element structure has to be populated. This includes a token string (such as "show version"), the help strings for each token, and attributes such as hidden, disabled and so on. A callback function also needs to be defined which is executed when the getting installed command is issued.
There is a defined, **DEFUN** macro, which expands to the definition of the command element, and the definition of the action routine and so on.


#### Preparing the command spec

A command spec includes the following:
•Command string
•Command name
•Action routine name
•Help string

The DEFUN macro is used to install a command. This registers a command name and an action routine function. For more information, refer to the following syntax:

****DEFUN(funcname, cmdname, cmdstr, helpstr)****


**funcname:** Name of the action routine function that will be defined.

**cmdname:**  Name of the command element structure that will be defined for the command.

**cmdstr:**  The cmdstr defines the command syntax. It is used by the CLI parser to perform matching and completion in the CLI. Example: "show version", "show system temperature", "ospf enable".

A cmdstr is a sequence of tokens, separated by spaces.

There are three types of token - cmd_terminal, cmd_multiple and cmd_keyword.

Each cmd_terminal token can be of cmd_terminal_fixed or option token or vararg token.

cmd_terminal_fixed  can be fixed_string, variable, range, ipv4, ipv4_prefix, ipv6 or ipv6_prefix.

    fixed_string = (lowercase | digit) , { lowercase | digit | uppercase | "-" | "_" } ;

    variable = UPPERCASE Tokens , { UPPERCASE | "_" } ;

    range = "<" , number , "-" , number , ">" ;

    ipv4 = "A.B.C.D" ;

    ipv4_prefix = "A.B.C.D/M" ;

    ipv6 = "X:X::X:X" ;

    ipv6_prefix = "X:X::X:X/M" ;

    option = "[" , variable , "]" ;

    vararg = "." , variable ;


    lowercase = "a" | ... | "z" ;

    UPPERCASE = "A" | ... | "Z" ;

    digit = "0" | ... | "9" ;

    number = digit , { digit } ;


#### Terminal tokens:

An example of a simple command string is `show ip bgp`. It consists of three terminal tokens, each containing a fixed string. When this command is called, no arguments are passed to the action routine function handling the execution, as it only consists of fixed strings. There is no variable user input.

Apart from fixed strings, terminal tokens can also contain variables. An example of this would be `show ip bgp A.B.C.D`. This command expects an IPv4 as an argument. As this is a variable, the IP address entered is passed down as an argument.

A terminal token can contain an option token. This is a simple string variable that may be omitted. An example of this would be `show interface [brief]`. If this command is executed without the `brief` token, no arguments are passed to the function implementing the command. Otherwise, the keyword "brief" will be provided to the function as a regular argument.

#### Multiple tokens:

The multiple token type can be used if there are multiple arguments that may be used for a command, but it should map to the same function nonetheless. An example of this would be `ip route A.B.C.D/M (reject|blackhole)`. In this case both "reject" and "blackhole" are acceptable as last arguments. The words matched by multiple tokens are always added to the argument list, even if they are matched by fixed strings. A multiple token can contain almost any type of token that would also be acceptable for a terminal token. The exception to this are optional variables and varag.



#### Keyword tokens:

There are commands that take a lot of different and possibly optional arguments. An example from OSPF would be the `default-information originate` command. This command takes a lot of optional arguments that are provided in any order. To accommodate such commands, the keyword token has been implemented. Using the keyword token, the `default-information originate` command and all its possible options can be represented using this single command string.

    "default-information originate { always | metric <0-16777214> | metric-type (1|2)| route-map WORD }"

	How it appears?
		as5712(config-router)# default-information originate  ?
		  <cr>
		  always   Always advertise default route
		  metric   OSPF default metric
		  metric-type  OSPF metric type for default routes
		  route-mapRoute map reference
		as5712(config-router)# default-information originate  always ?
		  <cr>
		  metric   OSPF default metric
		  metric-type  OSPF metric type for default routes
		  route-mapRoute map reference
		as5712(config-router)# default-information originate  always metric ?
		  <0-16777214>  OSPF metric
		as5712(config-router)# default-information originate  always metric 1 ?
		  <cr>
		  metric-type  OSPF metric type for default routes
		  route-mapRoute map reference
		as5712(config-router)# default-information originate  always metric 1 metric-type  ?
		  1  Set OSPF External Type 1 metrics
		  2  Set OSPF External Type 2 metrics
		as5712(config-router)# default-information originate  always metric 1 metric-type
		  <cr>
		  route-map  Route map reference
		as5712(config-router)# default-information originate  always metric 1 metric-type 1 route-map router ?
		  WORD  Pointer to route-map entries

Keywords always start with a fixed string and may be followed by arguments. Except for optional variables and vararg, everything is permitted here.

For the special case of a keyword without arguments, either NULL or the keyword itself will be pushed as an argument, depending on whether the keyword is present.

For the other keywords, arguments are only pushed for variables or multiple tokens. If the keyword is not present, the arguments that would have been pushed are substituted by NULL. The following are a few examples of NULL:

      "default information originate metric-type 1 metric 1000" would yield the following arguments:
      { NULL, "1000", "1", NULL }

      "default information originate always route-map RMAP-DEFAULT" would yield the following arguments:
      { "always", NULL, NULL, "RMAP-DEFAULT" }



#####Installing a command containing variables (.LINE)

Also, a terminal token can contain a vararg. This vararg is used in the  `show ip bgp regexp .LINE` command. The last token is a variable argument match and consumes all the arguments inputted in the command line. Each word (separated by a space in the input) after the fixed command string is passed as an individual argument to the action routine. vararg  and must be the last token in the CLI. Any input after this token is consumed by this token.	For example:

show ip bgp regexp abc def ghi jkl  => action routine will receive argc = 4  and argv as
			       argv[0] = abc	288
			       argv[1] = def	289
			       argv[2] = ghi	290
			       argv[3] = jkl	291




#### Help strings

The help string is used to show a short explanation for the commands that are available when the question mark ("?") or Tab key is pressed in the CLI. Each help string must be separated by a linefeed ("\n"). There should be one help string for each token in the `cmdstr`. The individual help strings are expected to appear in the same order as their respective tokens in the `cmdstr`. The last help string should be terminated with a linefeed as well.



Care should also be taken to avoid having similar tokens with different help strings. For example, the commands `show ip ospf` and `show ip bgp` both contain a help string for "show", but only one will be displayed when "sh?" is entered. If those two help strings differ, an error string is displayed on the console instead of any of the help strings. The following show an example of the help strings:

    DEFUN (ipv6_address,
           ipv6_address_cmd,
           "ipv6 address X:X::X:X/M",
           "Interface IPv6 config commands\n"         => for "ipv6" token
           "Set the IP address of an interface\n"     => for "address" token
           "IPv6 address (e.g. 3ffe:506::1/48)\n")    => for "X:X::X:X/M" token
    {
           /* read the ipv6 address entered by user from arg[0],
		   check if it is in a valid address (no loopback/broadcast address etc.)
		   If user input is invalid, print a meaningful error message to the session
		   (use vty_out to print) and return success to the CLI infra.

           Update the corresponding configuration in ovs-db

           Return success */
    }

#####Installing a command with dynamic help string

Based on the system configuration, some commands may want to change help strings dynamically. For example, each interface supports different speeds. Dynamically, help strings should specify what speeds
are supported instead of displaying all possible speeds without specifying whether they are supported or not. The syntax for defining a **command** with dynamic help string is	:

    #define DEFUN_DYN_HELPSTR(funcname, cmdname, cmdstr, helpstr, dyn_cbstr)

The 'dyn\_cbstr' parameter of DEFUN\_DYN\_HELPSTR is the concatenation of the dynamic callback functions for all the tokens present in the `cmdstr` parameter separated by '\n'. The callback function name for each
token is specified in the same order as the tokens in the 'cmdstr' parameter. These callbacks are optional. Below is an example:

    DEFUN_DYN\_HELPSTR (cli_intf_speed,
                        cli_intf_speed_cmd,
                        "speed (auto|1000|10000|40000)",
                        "Configure the interface speed\n"      => "speed" token help-string
                        "Auto negotiate speed (Default)\n"     => "auto" token help-string
                        "1Gb/s\n"                              => "1000" token help-string
			            "10Gb/s\n"                             => "10000" token help-string
			            "40Gb/s",                              => "40000" token help-string
                        "\n"                                   => no dynamic help string for "speed"
			            "\n"                                   => no dynamic help string for "auto"
			            "dyncb_helpstr_1G\n"                   => dynamic help-string for "1000"
			            "dyncb_helpstr_10G\n"                  => dynamic help-string for "10000"
                             "dyncb_helpstr_40G")                   => dynamic help-string for "40000"
    {
	    /* your action routine here */
    }



The last argument is the string containing the callback function names for dynamic help strings separated by '\n'. If a particular token does not require a dynamic help string, then it can be left blank like '\n\n'. Here there is no dynamic help string for tokens 'speed' and 'auto'. So the callback function is not specified. The callback function definition is in the format specified below:

    void <callback_function_name>(struct cmd_token *token,
                                  struct vty *vty,
                                  char * const dyn_helpstr_ptr,
                                  int max_strlen);

These callback functions are mapped in the lookup table in the 'lib/dyn_helpstr.h' file as shown below:

    extern void dyncb_helpstr_speeds(struct cmd_token *token, struct vty *vty, char * const dyn_helpstr_ptr, int max_strlen);
    struct dyn_cb_func dyn_cb_lookup[] =
    {
    {"dyncb_helpstr_1G", dyncb_helpstr_speeds},
    {"dyncb_helpstr_10G", dyncb_helpstr_speeds},
    {"dyncb_helpstr_40G", dyncb_helpstr_speeds},
    };

The 'dyncb\_helpstr\_speeds' function is defined in the respective feature file with input parameters (struct cmd\_token \*token, struct vty \*vty, char \* const dyn\_helpstr\_ptr, int max\_strlen). 'The dyn\_helpstr\_ptr' help string is returned and displayed and is of maximum length 'max\_strlen'. For more details on implementation, refer to the dyncb\_helpstr\_speeds in the intf\_vty.c file.

###Installing a command with integer range or comma separated list input
The following sections display **DEFUN** integer templates for installing a command.

#### Installing single integer input command
Define the integer input in the format < `Start_value` - `End_value` > with the command string for a single integer input. For example:

         DEFUN (vtysh_command_demo,
                vtysh_command_demo_cmd,
                "command value <10-25>",
                "Demo Command \nDemo Value token Help\n Enter the value(Default 15)\n")
         {
                ....
                ....
         }

#### Installing range integer input command
Define the integer input in the format < `L:` `Start_value` - `End_value` > with the command string for a range integer input. For example:

        DEFUN (vtysh_command_demo,
               vtysh_command_demo_cmd,
               "command value <L:1-50>",
               "Demo Command \nDemo Value token Help\n Enter the value, Example:[1-15]\n")
        {
               ....
               ....
        }

#### Installing comma integer input command
Define the integer input in the format < `C:` `Start_value` - `End_value` > with a command string for a comma separated integer input. For example:


        DEFUN (vtysh_command_demo,
               vtysh_command_demo_cmd,
               "command value <C:1-50>",
               "Demo Command \nDemo Value token Help\n Enter the value, Example:[1,2,3 or 3,4,5,1 or 1,5,2,6,7]\n")
        {
               ....
               ....
        }

#### Installing a range and comma separated integer input command
Define the integer input in the format < `A:` `Start_value` - `End_value` > with the command string for a range and comma separated integer input. For example:


        DEFUN (vtysh_command_demo,
               vtysh_command_demo_cmd,
               "command value <A:1-50>",
               "Demo Command \nDemo Value token Help\n Enter the value, Example:[1,2,3 or 1-15 or 1,2,4-10,3]\n")
        {
               ....
               ....
        }

##### API used in command action routing to get/free list of user input integer value.
struct range_list \*cmd_free_memory_range_list(struct range_list \*list)
struct range_list \*cmd_get_list_from_range_str(const char \*str_ptr, int flag_intf)

Note: Do not use the interger range or comma-separated input for the context level.

    Example : Interface and vlan configuration command.
    switch(config)# interface <IFNAME>
    switch(config)# vlan <id>
Note : Example use case for range/comma seperated integer input.

    Example : configure vlan trunk in per interface.
              DEFUN(cli_intf_vlan_trunk_allowed,
                    cli_intf_vlan_trunk_allowed_cmd,
                    "vlan trunk allowed <A:1-4094>",
                    VLAN_STR
                    TRUNK_STR
                    "Allowed VLANs on the trunk port\n"
                    "VLAN identifier range. [2, 2-10 or 2,3,4 or 2,3-10]\n")

###'No' form of configuration commands
Every configuration command must support a reset command to revert the configuration. For more information see the guidelines at http://openswitch.net/documents/dev/ui-guidelines.

A configuration command accepting a user input must support two "no" commands - one with user input and one without the user input.

For example:  "hostname WORD"  must support "no hostname" and "no hostname WORD" as no commands.

To install a common action routine for both the configuration command and its “no” form of command, the macros are extended to return **vty_flags** as **CMD_FLAG_NO_CMD**. Read the `vty_flags` inside the action routine to take appropriate action.

For example:

    DEFUN (vtysh_command_demo,
       vtysh_command_demo_cmd,
       "command value <10-25>",
       "Demo Command \nDemo Value token Help\n Enter the value(Default 15)\n")
    {
		if(vty_flags & CMD_FLAG_NO_CMD)
			vty_out (vty, "No form, value to default\n");
			/* Here, assume value as 15, which is default and act appropriately */
		else
			vty_out (vty, "command value = %d\n", *(argv[0]));
			/* read the user input from *(arg[0]), and set db appropriately */
		return CMD_SUCCESS;
    }

    DEFUN_NO_FORM (vtysh_command_demo,
                   vtysh_command_demo_cmd,
                   "command value",                          /* Adding “no” to the command is taken care by macro */
                   "Demo Command \n"                         /* Adding “no” help string is taken care by macro */
                   "Demo Value token Help\n");

In the initialization path, install the `no` command along with the configuration command.

    install_element (CONFIG_NODE, &vtysh_command_demo_cmd);
    install_element (CONFIG_NODE, &no_vtysh_command_demo_cmd);


### Hidden commands

Functionality to hide a command runtime is also available . To do so, set the command structure attribute with the CMD\_ATTR\_HIDDEN macro.

    vtysh_command_demo_cmd.attr |= CMD_ATTR_HIDDEN;

To make it visible again, reset the bit.


### Disabled commands

For a few cases, we may have to block a command execution depending on system state or configuration download or active-standby sync etc. To achieve this, use attribute CMD\_ATTR\_NOT\_ENABLED.

    vtysh_command_demo_cmd.attr |= CMD_ATTR_NOT_ENABLED;

Resetting the above attribute bit will enable the execution of the command. This can be used to deny access to few configuration command for selected users depending on the role or privilege levels.



###Example
An example of installing a logging command in the `lldp` feature module is as follows:

Prepare the command elemnet using DEFUN macro.

    /* Logging commands. */
    DEFUN (vtysh_show_logging,   // this is your action routine function name
           vtysh_show_logging_cmd,   // this is your command element for this command
           "show logging",   // this is your command
           SHOW_STR  // a “\n” Separated help string that should be shown for each token in your command.
           "Show current logging configuration\n")
    {

        /*
			Here goes the action routine logic.
			User input if any, is passed as regular arguments (argc and argv[]).
			You may use vty_out for printing the values,
			e.g vty_out (vty, "I am in action routine, with %d arguments %s ",argc,  VTY_NEWLINE);
			You may use CMD_SUCCESS for a succesfull return
	    */

		/* Example code: */
		unsigned int i;
		char line[] = "show logging\n";
		for (i = 0; i < array_size(vtysh_client); i++)
		{
			if ( vtysh_client[i].fd >= 0 )
			{
				fprintf (stdout,"Logging configuration for %s:\n",
				vtysh_client[i].name);
				vtysh_client_execute (&vtysh_client[i], line, stdout);
				fprintf (stdout,"\n");
			}
		}
        return CMD_SUCCESS;
    }




Finally we call the install_element() as follows:

    install_element(CONFIG_NODE, vtysh_show_logging_cmd)



##Show running support for a command

Every configuration command that changes the switch configuration to a non-default value must be added to the `show running-configuration` infrastructure. This allows the administrator to save the output of the `show running-configuration` command from a switch, and replay it later on the switch configuration console to reconfigure it to the same configuration. The following steps add the `show running configuration` command for the feature context and sub-context.

1. Create the source `vtysh_ovsdb_<featurename>_context.c` file under the `<ops-featurename>/src/cli>` directory and the header file `vtysh_ovsdb_<featurename>_context.h` under the `<feature>/include` directory.

2. Include the source file into the feature CLI library CMakefile or Makefile file.
         # CLI libraries source files
         set (SOURCES_CLI ${PROJECT_SOURCE_DIR}/<featurename>_vty.c
              ${PROJECT_SOURCE_DIR}/vtysh_ovsdb_<featurename>_context.c
             )

3. Include the `vtysh_ovsdb_<featurename>_context.h` file in the `<featurename>_vty.c`.

4. Identify the right place for adding the configuration commands to the existing `show running-configuration` output. Ensure that the prerequisite configurations are appearing above in the output, so that on replaying the output on an unconfigured switch, the independent configuration gets configured first and then the dependent configuration. The new contexts enum should be added in the right order to context enum list `vtysh_context_idenum` which is maintained in the `ops-cli/vtysh/vtysh_ovsdb_config.h` file. This addition has to be sent to the CLI Infra for review and approval.

5. The `show running-configuration` infra provides for registering an init and an exit function for every callback routine registering. This allows the features to do one time operations that are required inside individual instances of callback routine calls or inside the sub-context callback functions. One example is implementing the `show running configuration` for the interface context involving multiple feature configurations. Also, the interface names must be sorted in the output. The steps involved to do this follow:
        a.   Sort the interface rows based on the interface name.
        b.   For each interface in the sorted list:
               i. Check the interface configurations, form command strings for non-default configurations and print it.
               ii. Call feature 1, which has some configurations inside the interface context.
               iii. Call feature 2, which has some configurations inside the interface context.
               iv. Do the above for every feature.
        c.   Free the sorted list created for printing.

To support all these functionalities, "show running-configuration" infra provides registering the below functions.

Define the callback init, the callback, and callback exit for the context in the below format in the `vtysh_ovsdb_<featurename>_context.c` file and respective declarations in the `vtysh_ovsdb_<featurename>_context.h` files.

	Step a:
         /* Context callback */
         vtysh_ret_val vtysh_<featurename>_context_clientcallback(void *p_private);
         E.g. vtysh_mgmt_intf_context_clientcallback /* mgmt_intf context */

	Step b:
         /* Sub-context callback */
         vtysh_ret_val vtysh_<contextname>_context_<featurename>_clientcallback(void *p_private);
         E.g. vtysh_config_context_led_clientcallback /* Sub-context led is added to global config context */

	Step c:
         struct feature_sorted_list * vtysh_<featurename>_context_init(void *p_private);
         void vtysh_<featurename>_context_exit(struct feature_sorted_list * row_list);

If any initialization is required before calling the callback function, `vtysh_<featurename>_context_init` is called. If any cleanup is required after the context callback, `vtysh_<featurename>_context_exit` is called. The `init` and `exit` functions are required when context acts on multiple OVSDB rows. Otherwise the rows can be initialized to NULL.

For the interface context, the CLI infra calls all the interfaces in a sequence. To achieve this, `vtysh_intf_context_init` is called and from that OVSREC\_INTERFACE\_FOR\_EACH is run to get the list of all interface rows and is then passed back to the CLI Infra. the interface list is created by malloc. The CLI loops through all the interfaces in the list and prints the data if any. To free the memory allocated in `vtysh_intf_context_init`, the `vtysh_intf_context_exit` context is called.

6. The context callback is registered with `ops-cli` from the `cli_pre_init` in `<featurename>_vty.c`.

       void install_show_run_config_context(vtysh_contextid index, /* Enum value of running-config context */
                                            vtysh_ret_val (*funcptr) (void* p_private), /* Context callback function pointer*/
                                            struct feature_sorted_list * (*init_funcptr) (void* p_private), /* Context callback init function pointer */
                                            void (*exit_funcptr) (struct feature_sorted_list * row_list));      /* Context callback exit function pointer */

       E.g.
         void cli_pre_init(void)
         {
           ...
	       install_show_run_config_context(e_vtysh_mgmt_interface_context,
                                           &vtysh_mgmt_intf_context_clientcallback,
                                           NULL, NULL);
         }

7. If the feature is a sub-context of any existing context, the sub-context callback is registered with `ops-cli` from the `cli\_post\_init` in the `<featurename>_vty.c`.

       void install_show_run_config_subcontext(vtysh_contextid index, /* Enum value of running-config context */
                                               vtysh_contextid subcontext_index,  /* Enum value of sub-context */
                                               vtysh_ret_val (*funcptr) (void* p_private), /* Context callback function pointer*/
                                               struct feature_sorted_list * (*init_funcptr) (void* p_private), /* Context callback init function pointer */
                                               void (*exit_funcptr) (struct feature_sorted_list* row_list));      /* Context callback exit function pointer */

For example: Led is a sub-context of the config context.

         void cli_post_init(void)
         {
           ...
           install_show_run_config_subcontext(e_vtysh_config_context,  /* Context index */
                                              e_vtysh_config_context_led, /* Sub-context index */
                                              &vtysh_config_context_led_clientcallback,
                                              NULL, NULL);
         }

For example:

The LLDP configurations are now added to the "configure context" callback routine as part of show running-configuration infra. To move it to an independent callback routine in the feature repository, and to register itself to be called at the right order in the show running-configuration output,

1. Enum for new context is added in the right place in the context enum list. This list is maintained in `ops-cli/vtysh/vtysh_ovsdb_config.h`
2. The context callback is registered with `ops-cli` from `cli_pre_init` in the `<featurename>_vty.c`.
3. The context, init, and exit callback are defined in `vtysh_ovsdb_<featurename>_context.c` and the respective declarations reside in the `vtysh_ovsdb_<featurename>_context.h` files.
4. If the feature is the sub-context to any existing context, register the sub-context in `cli_post_init` and define the respective callback functions in `vtysh_ovsdb_<featurename>_context.c`.
Add enum in the right order to sub-context the enum list.

##  Key combinations and its actions in vtysh
   1. **"ctrl + ]"** and **"ctrl + 5"** : Enter into telnet prompt.
   2. **"ctrl + 4"** and **"ctrl + \"** : Creates core dump for vtysh process and comes to bash prompt.
   3. **"ctrl + z"** : Exits any context in vtysh and comes to switch context (enable node).
   4. **"ctrl + c"** : Erases any typed input(if any) and remains in the same context.

##  User Interface Guidelines

Refer to the CLI guidelines at:
http://openswitch.net/documents/dev/ui-guidelines
https://github.com/openvswitch/ovs/blob/master/CodingStyle.md
