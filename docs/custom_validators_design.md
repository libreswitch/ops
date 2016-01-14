# Custom Validators Framework Design

## Contents

- [Overview](#overview)
- [High level design](#high-level-design)
	- [Validator](#validator)
	- [Base](#base)
	- [Plugins](#plugins)
	- [Errors](#errors)
- [Custom validator framework](#custom-validator-framework)
	- [Location of custom validators](#location-of-custom-validators)
	- [Installation of custom validators](#installation-of-custom-validators)
	- [Discovery of custom validators](#discovery-of-custom-validators)
	- [Invocation of custom validators](#invocation-of-custom-validators)
	- [Validation errors](#validation-errors)
- [Implementing a custom validator](#implementing-a-custom-validator)
	- [BitBake recipe modifications](#bitbake-recipe-modifications)
	- [Custom validator location](#custom-validator-location)
	- [Derived custom validator class](#derived-custom-validator-class)
		- [Filename](#filename)
		- [Imports and usages](#imports-and-usages)
		- [Class name](#class-name)
		- [Defining the resource name](#defining-the-resource-name)
		- [Overriding validation methods](#overriding-validation-methods)
		- [Using the validation arguments](#using-the-validation-arguments)
- [Examples](#examples)
	- [Example of BitBake recipe modifications](#example-of-bitbake-recipe-modifications)
	- [Example of a custom validator](#example-of-a-custom-validator)
- [References](#references)

## Overview

Custom validators are Python modules that perform feature specific validations for resource creating, updating, and deleting. Beyond the generic validations, for example, checking if a resource exists. Some features require specific checks, such as whether a resource is already referenced by another resource. Custom validators are used by REST APIs and Declarative Configuration (DC) for validation prior to committing a transaction to the database.

## High level design

The custom validator framework is responsible for the installation, discovery, registration, and invocation of the custom validators. The framework consists of the following components:

From the `opsvalidator` package:

- Validator - Implemented in the `validator.py` module.
- Base - Implemented in the `base.py` module.
- Plugins/custom validators - Implemented in each feature's repository for each table.
- Errors - Implemented in the `error.py` module.

The validator, base, and error modules are implemented as a part of the `opsvalidator` Python package. The `opsvalidator` is used by REST and DC to perform validations to prevent invalid configurations from the database. The diagram, below, highlights how the main components are interfaced.

```ditaa
	+--------------+
	|              |
	|              |       +---------------+    +---------------+
	|     REST     |       |               |    |               |
	|              +-------+               |    |  +------------+--+
	|              |       |               |    |  |               |
	+--------------+       |               |    |  |  +------------+--+
	                       |   Validator   +----|  |  |               |
	+--------------+       |               |    |  |  |               |
	|              |       |               |    +--+  |    Plugins    |
	|              +-------+               |       |  |               |
	|      DC      |       |               |       +--+               |
	|              |       |               |          |               |
	|              |       +---------------+          +---------------+
	+--------------+

```

### Validator
The validator discovers, loads, and registers all plugins/custom validators upon `restd` start-up. The validator is the interface for invoking custom validators for REST/DC requests. The plugins are invoked based upon the resource/table name contained within the REST/DC request. The validator manages all of the custom validators, and is responsible for invoking the correct validators. The validator module provides the custom validators with the necessary data for validations. The caller of the validator must handle errors returned from the validator.

### Base
The base module is used as the super class of the derived custom validators. The base module declares methods that the validator invokes as hooks to the derived plugins. The base module also serves the role of allowing the validator module to discover all derived classes. Default definitions of the validation methods are defined in the base module.

### Plugins
Plugins/custom validators are derived from the base module, and are implemented for each resource/table. Custom validators override the inherited base module methods in order for the validator module to be invoked upon receiving a REST/DC request. Custom validators are used for performing feature-specific validations, and raise any errors to the validator caller, if any validations fail.

### Errors
The error module defines the error codes, error messages, and exceptions that are returned from the custom validators upon validation failure. The error module is the central module for defining additional error codes and messages for use by custom validators. The exception raised includes the error code, message, and any additional details the custom validators include.

## Custom validator framework

### Location of custom validators

Custom validators are distributed across repositories. Custom validators are located in a directory named `opsplugins`. During build time, **BitBake** recipes for each repository locate validators using the specific directory name `opsplugins`.

### Installation of custom validators

Custom validators are utilized during run-time. All custom validators are consolidated and installed as a part of the OpenSwitch image. **BitBake** recipes must be modified to consolidate the custom validators into the target `/usr/share/opsplugins` directory.

### Discovery of custom validators

The `validator.py` module iterates through the directory `/usr/share/opsplugins` for any Python modules and are loaded and registered as custom validators.

All custom validators derive from the `BaseValidator` class from `opsvalidator/base.py`. Deriving from `BaseValidator` allows the `validator.py` module to discover subclasses of the `BaseValidator` when the custom validator module is loaded. All custom validators register with a resource name. During initialization of the custom validator framework, all validators are loaded from the `/usr/share/opsplugins` directory. When the custom validators are discovered and loaded, the validator is mapped to the value of the class variable `resource`. The value of the `resource` is stored as the key in a dictionary for retrieving the custom validator. If more than one custom validator is registered using the same resource name, the custom validators are added to the list of validators for that `resource`.

For example, a custom validator for the table **BGP Router** is derived from `BaseValidator` with `resource` initialized:

```
resource = "bgp_router"
```

When a custom validator is discovered and loaded in `validators.py`, an instance of the plugin is stored and mapped in a dictionary:

```
g_validators[resource] = plugin_instance
```

### Invocation of custom validators

Upon reception of a request to create or modify a resource, the `validator.py` module is used for invoking the associated custom validators based on the resource's table name. The `validator.py` module can be utilized in the following way:

```
from opsvalidator import validator
from opsvalidator.error import ValidationError

try:
    validator.exec_validators(idl, schema, table_name,
                              row, request_type, p_table_name, p_row)
except ValidationError as e:
    # e.error contains error code, message, and details
```

The following arguments are passed to the API:

* `idl`: The Interface Definition Language (IDL) object is the in-memory replica of the database. It is an object from the `ovs.db.idl` Python module.
* `schema`: The parsed schema of the database as described in `vswitch.extschema`.
* `table_name`: The name of the current resource's table.
* `row`: The IDL row data for the current resource.
* `p_table_name`: The name of the parent resource's table.
* `p_row`: The IDL row data for the parent resource.
* `request_type`: Type of the incoming request, which can be `"POST"`, `"PUT"`, or `"DELETE"`.
* `data`: JSON format of the incoming data for the resource.

All custom validators are loaded upon `restd` start-up and stored by their associated resource names. The `validator.py` module uses the `resource` name to perform a custom validator dictionary look-up. If a custom validator is not found for the `resource`, then a message is logged and the validation is skipped. If the name exists in the dictionary, then all custom validators registered under the `resource` name are invoked. If any custom validators fail, when more than one validators is registered to the same resource, the validation immediately returns an error. If a validator should only be executed for specific types of the resource, that custom validator should include a check to enforce skipping or proceeding with the validation.

The `validator.py` module invokes the custom validator's corresponding `validate_modification` or `validate_deletion` method, based upon the value of the `request_type`, which can be `"POST"`, `"PUT"`, or `"DELETE"`. If the value is `"POST"` or `"PUT"`, then the `validation_modification` method is invoked. The `ValidationArgs` object is passed as an argument to the custom validators. The `ValidationArgs` object stores the IDL, schema, creation flag, and child and parent specific information, including table name, schema table, IDL table data, and IDL row data, for the custom validators to use for validations. If any of the validation methods are not overridden in the custom validators, the activity is logged and validation is skipped.

The `validator` module performs the look-up and invocation of custom validators with the following logic:

```
if resource_name in g_validators:
    resource_validators = g_validators[resource_name]
    validation_args = ValidationArgs(idl, schema, table_name, row,
                                     p_table_name, p_row, is_new)

    for validator in resource_validators:
        res = validator.validate(validation_args)
        ...
```

### Validation errors

The error codes, error messages, and exceptions are defined in the `error.py` module in `opsvalidators`. Custom validators raise a `ValidationError` upon encountering a validation error. The `ValidationError` exception accepts an error code, plus any additional plugin-specific details, and stores the information for the caller of the validator in an `error` variable that includes the `code`, `message`, and `details`. Clients of the validator import `ValidationError` from `opsvalidators.error` to catch exceptions raised from the custom validators.

The `ValidationError` exception utilizes the `code` argument to look-up the predefined error message for the error `code`. If a predefined message for the error code is not found, the default error is utilized as a part of the error response to the caller of the validator. Any additional error codes and messages must be added in the `error.py` module. The error codes and messages are common for all validators. New error codes and messages should be defined generically. When raising the `ValidationError` exception, custom validators can provide additional information in the `details` parameter.


## Implementing a custom validator

### BitBake recipe modifications

The **BitBake** recipe for each repository implementing custom validators must be modified to copy the custom validators into the target standard path `/usr/share/opsplugins`. The modified code for copying must be added in the `do_install_append` function of the corresponding recipe file. Modification of the **BitBake** recipe only needs to occur once for the repository.

The following is an example of modifying the recipe file for `ops-quagga`, located at `yocto/openswitch/meta-distro-openswitch/recipes-ops/l3/ops-quagga.bb` under the `ops-build` repository:

```
# Added for files to be picked up as a part of the installation.
FILES_${PN} += "/usr/share/opsplugins"

do_install_append() {
   # Any existing logic...

	# Code for copying to /usr/share/opsplugins. This assumes
	# the opsplugins for ops-quagga is under the ops folder.
	install -d ${D}/usr/share/opsplugins
	for plugin in $(find ${S}/ops/opsplugins -name "*.py"); do \
		install -m 0644 ${plugin} ${D}/usr/share/opsplugins
	done
}
```

If the `do_install_append` function does not exist in the recipe file, then it must be added. If it does exist, then the code should be added at the end of the function.

### Custom validator location

Custom validators must be implemented in the `opsplugins` directory of the repository for each resource. The correct location of the custom validators is important for the validators to be successfully discovered by the custom validator framework.

### Derived custom validator class

#### Filename

The custom validator file should be named using the resource/table name in lowercase. If the resource/table name contains more than one word, then the words of the custom validator file name should be separated by `_`. For example, the custom validator file name for the table `BGP Router` should be named `bgp_router.py`, following the `resource_name.py` convention. If a validator is created for a table that already has a custom validator, then the type should be appended at the end, such as `resource_name_type.py`. If the selected file name for the custom validator exists, an error occurs during build time, and the name must be changed to avoid a conflict.

#### Imports and usages

Custom validators typically import the following:

```
from opsvalidator.base import *
from opsvalidator import error
from opsvalidator.error import ValidationError
from opsrest.utils import *
from tornado.log import app_log
```

- `opsvalidator.base`: Module that includes the base class used for registration and invocation of derived custom validators.
- `opsvalidator.error`: Module that includes the predefined error codes and messages. Error codes can be accessed, for example: `error.VERIFICATION_FAILED`
- `opsvalidator.error.ValidationError`: The exception to indicate there was an error during validation.

	Exceptions are raised, for example, in the following way:

	```
	code = error.VERIFICATION_FAILED
	details = ['invalid asn', 'invalid type']

	raise ValidationError(code, details)
	```

- `opsrest.utils`: Contains utility functions that custom validators can use, such as `get_column_data_from_row`, to retrieve the value of a column for a given OVS row.
- `tornado.log.app_log`: Part of the **Tornado** web framework for logging. Custom validators can log information or debug messages with the following APIs:

	```
	app_log.info("")
	app_log.debug("")
	```


#### Class name

The name of the custom validator should be in upper camel-casing. The class name includes the name of the resource and type, and is appended by the string "Validator". The type should be included if there is more than one validator for the same table name. For example, the custom validator class name for the table `BGP Router` should be `BgpRouterValidator`, following the `ResourceNameValidator` convention. If a validator already exists for the table, then the class name should be `ResourceNameTypeValidator`.

#### Defining the resource name

A custom validator is registered to a table/resource name by assigning the name to the `resource` class variable:

```
class BgpRouterValidator(BaseValidator):
    resource = "bgp_router"

    ...
```

The value of the resource should be in the format of `resource_name`. Correct naming of the resource is crucial for successful registering and look-up of the custom validator.

#### Overriding validation methods

The `BaseValidator` class declares the `validate_modification` and `validate_deletion` methods. The methods should be overridden in the custom validators, as shown below. If the method is not overridden, the default behavior is logging the unimplemented method and skipping validation.

```
class BgpRouterValidator(BaseValidator):
    resource = "bgp_router"

    def validate_modification(self, validation_args):
        # Validation logic

    def validate_deletion(self, validation_args):
        # Validation logic
```

#### Using the validation arguments

The `validation_args` argument is passed to the custom validator to perform validations. The `validation_args` is an object of the `ValidationArgs` from `opsvalidator.base`, which includes the IDL, schema, creation flag, and child and parent specific information, including table name, schema table, IDL table data, and IDL row data. The arguments can be accessed via:

```
# General arguments
idl = validation_args.idl
schema = validation_args.schema
is_new = validation_args.is_new

# Parent specific arguments
parent_table = validation_args.p_resource_table
parent_schema = validation_args.p_resource_schema
parent_idl_table = validation_args.p_resource_idl_table
parent_row = validation_args.p_resource_row

# Child specific arguments
child_table = validation_args.resource_table
child_schema = validation_args.resource_schema
child_idl_table = validation_args.resource_idl_table
child_row = validation_args.resource_row
```

The `idl` argument is an `Idl` object from the `ovs.db.idl` module. The IDL includes all tables, rows, and columns information. For example, the following code snippet obtains the rows from a table:

```
idl = validation_args.idl

table_name = "some_table_name"

for row in idl.tables[table_name].rows.itervalues():
```

The `schema` argument is a `RESTSchema` object, from the `opslib.restparser` module, and is a result of parsing the schema from `vswitch.extschema`. The schema of the tables, configurations, status, statistics, and etc, can be found from the `schema` argument.

For example, the tables from the schema can be obtained from the following code snippet:

```
for table_name, table in schema.ovs_tables.iteritems():
```

The configurations defined for a table can be accessed via:

```
for column_name, column in table.config.iteritems():
```
The `is_new` argument contains a flag that denotes if the modification is for a new row. If `is_new` is true, then it indicates a row is being created, otherwise, it is a row update.

The `p_resource_table` and `resource_table` are the parent and child resources' table names.

The `p_resource_schema` and `resource_schema` are the parent and child resources' parsed schemas. From the parsed schema, the configuration, statistics, statuses, and references can be accessed in the following way:

```
parent_schema = validation_args.p_resource_schema

parent_config_keys = parent_schema.config
parent_stats_keys = parent_schema.stats
parent_status_keys = parent_schema.status
parent_references = parent_schema.references
parent_reference_keys = parent_references.keys()

# Access each key in the parent table's schema
for key in parent_config_keys:
	# Do something with key
```

The `p_resource_idl_table` and `resource_idl_table` arguments are resource specific `Idl` objects containing the table from the `ovs.db.idl` module. The IDL includes the resource's specific table, rows, and columns information. For example, the following code snippet obtains the rows from a table:

```
parent_idl_table = validation_args.p_resource_idl_table

column_key = "some_column_key"

for row in parent_idl_table.rows.itervalues():
	# Do something with a value from the row's column
	value_of_column = utils.get_column_data_from_row(row, column_key)

	# Value can also be obtained if the column is known and exists
	value_of_column = row.some_column_key
```

The `p_resource_row` and `resource_row` arguments are `Row` objects from the `ovs.db.idl` module. The object contains the resource's row data from the IDL. Specific data from the row can be obtained by the column name if it exists. For example, getting the ASN value for a BGP router resource's row can be accessed by `row.key`. If the column key is dynamically generated or retrieved, then it is recommended to access the column data by using the `utils.get_column_data_from_row`.

For more information of the `ovs.db.idl` module, refer to the comments in the original [source](https://github.com/osrg/openvswitch/blob/master/python/ovs/db/idl.py).


## Examples

### Example of BitBake recipe modifications

```
# Added for files to be picked up as a part of the installation.
FILES_${PN} += "/usr/share/opsplugins"

do_install_append() {
   # Any existing logic...

	# Code for copying to /usr/share/opsplugins. This assumes
	# the opsplugins for ops-quagga is under the ops folder.
	install -d ${D}/usr/share/opsplugins
	for plugin in $(find ${S}/ops/opsplugins -name "*.py"); do \
		install -m 0644 ${plugin} ${D}/usr/share/opsplugins
	done
}
```

### Example of a custom validator

```
from opsvalidator.base import *
from opsvalidator import error
from opsvalidator.error import ValidationError
from opsrest.utils import *
from tornado.log import app_log


class BgpRouterValidator(BaseValidator):
    resource = "bgp_router"

    def validate_modification(self, validation_args):
        is_new = validation_args.is_new
        vrf_row = validation_args.p_resource_row

        if is_new:
            bgp_routers = utils.get_column_data_from_row(vrf_row,
                                                         "bgp_routers")

            # Since working on the IDL that already has the reflective change,
            # the total number of bgp_routers in parent table can be used
            # to validate allowed bgp_routers.
            if bgp_routers is not None:
                if len(bgp_routers) > 1:
                    details = "Only one BGP router can be created"
                    raise ValidationError(error.RESOURCES_EXCEEDED, details)

        app_log.debug('Validation Successful')
		# No exception raised indicates successful validation
```

## References

- [Yocto - BitBake](http://www.yoctoproject.org/docs/1.8/bitbake-user-manual/bitbake-user-manual.html#bitbake-user-manual)
- [Open vSwitch - OVS Python APIs](https://github.com/osrg/openvswitch/tree/master/python/ovs)
