#!/usr/bin/env python

# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


class SchemaValidatorError(Exception):
    """ Class for errors from schema validations

    This class is used to diferentiate errors that come from schema
    validations.
    """
    pass


def path_to_str(path):
    """Convert path to a printable string."""
    return '/' + '/'.join(path)


def get_instance(schema, path):
    """Get the instance (value) for a given path."""
    instance = schema
    for key in path:
        if key in instance:
            instance = instance[key]
        else:
            return None
    return instance


def get_instance_type(instance):
    """Get the OVSDB type of instance."""
    if isinstance(instance, (unicode, str)):
        return instance
    if isinstance(instance, dict):
        if 'type' in instance:
            return get_instance_type(instance['type'])
        if 'key' in instance:
            return get_instance_type(instance['key'])
        if 'valueType' in instance:
            return get_instance_type(instance['valueType'])


def valid_type(instance, schema_type):
    """Return true if instance is of type schema_type.

    Valid schema types are 'integer', 'real', 'boolean', 'string' and 'uuid'.
    """
    valid_types = {
        u'integer': int,
        u'real': float,
        u'boolean': bool,
        u'string': (unicode, str),
        u'uuid': (unicode, str)
    }
    if schema_type in valid_types:
        return isinstance(instance, valid_types[schema_type])
    raise Exception('Unknown type: ' + type(instance) + ' is not of type ' +
                    schema_type)


def get_table_name(path):
    """Extract the table name from path.

    Return a string with the table's name, or an SchemaValidatorError exception
    if the path does not contain a valid table name.
    """
    if len(path) < 2:
        raise Exception('Path is too short to have a table name in it.')
    if path[0] != 'tables':
        raise Exception('Path does not contain a table name.')
    return path[1]


def get_table(schema, path):
    """If path constains a table, return such table.

    schema -- the full schema.
    path -- a path indicating the current place in the schema.

    Return a dict with the table indicated in path, or a SchemaValidatorError
    if the table does not exists in the schema.
    """
    if 'tables' not in schema:
        raise Exception('Schema does not have a "tables" property.')
    tables = schema['tables']
    table_name = get_table_name(path)
    if table_name not in tables:
        raise Exception('Table "' + table_name +
                        '" does not exists in the schema.')
    return tables[table_name]


def get_column_name(path):
    """Extract the column name from path.

    Return a string with the columns's name, or an SchemaValidatorError
    exception if the path does not contain a valid column name.
    """
    if len(path) < 4:
        raise Exception('Path is too short to have a column name in it.')
    if path[0] != 'tables':
        raise Exception('Path does not contain a table name.')
    if path[2] != 'columns':
        raise Exception('Path does not contain a column name.')
    return path[3]


def get_column(schema, path):
    """If path contains a column, return such column.

    schema -- the full schema.
    path -- a path indicating the current place in the schema.

    Return a dict with the column indicated in path, or a SchemaValidatorError
    if the column does not exists in the schema.
    """
    column_name = get_column_name(path)
    table = get_table(schema, path)
    columns = table['columns']
    if column_name not in columns:
        err_msg = ('Column "' + column_name + '" does not exists in table "' +
                   get_table_name(path) + '" in the schema.')
        raise Exception(err_msg)
    return columns[column_name]


def get_column_type(schema, path):
    """Return the OVSDB type for the column."""
    column = get_column(schema, path)
    return get_instance_type(column)


def _get_msg(path, instance, msg, pre_msg):
    return (pre_msg + path_to_str(path) + ': ' +
            str(instance).replace("u'", "'") + '\n- ' + msg)


def get_error_msg(path, instance, msg):
    """Return a standard error message for schema validation errors.

    path - a path indicating the current place in the schema.
    instance - instance of the schema where the error occurred.
    msg - string to be shown under the ERROR message.
    """
    return _get_msg(path, instance, msg, 'ERROR: ')


def get_warn_msg(path, instance, msg):
    """Return a standard warning message for schema validation errors.

    path - a path indicating the current place in the schema.
    instance - instance of the schema where the error occurred.
    msg - string to be shown under the WARN message.
    """
    return _get_msg(path, instance, msg, 'WARN: ')


def _validate_rec(instance, schema, path_stack, validators):
    if type(instance) is dict:
        for p in instance:
            path_stack.append(p)
            if p in validators:
                validators[p](instance[p], schema, path_stack)
            _validate_rec(instance[p], schema, path_stack, validators)
            path_stack.pop()


def validate(schema, validators):
    """Validate 'schema' using the schema validators specified in 'validators'

    schema - schema to be validated.
    validators - a dict with keys being the properties of the schema that must
                 to be validated, and values being functions that validate such
                 properties. As an example, if the property 'minLength' wants
                 to be validated as being always positive, the following code
                 can be used:

                 def minlength_validator(instance, schema, path_stack):
                     if instance < 0:
                         err_msg = get_error_msg(path_stack, instance,
                                                 "minLength is not positive.")
                         raise SchemaValidatorError(err_msg)

                 schema_validators = {
                    'minLength': minlength_validator
                 }

                 validate(schema, schema_validators)
    """
    path_stack = []
    _validate_rec(schema, schema, path_stack, validators)
