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


import json
import sys

from jsonschema import Draft4Validator, ValidationError
from argparse import ArgumentParser

import validators

from validators import (SchemaValidatorError, get_column_name, get_column_type,
                        get_error_msg, get_instance, get_instance_type,
                        get_table, get_table_name, get_warn_msg, valid_type)


# Schema Validators


def follows_validator(instance, schema, path_stack):
    table = get_table(schema, path_stack)
    columns = table['columns']
    if instance not in columns:
        msg = ('Invalid follows: Table "%s" does not have a column named "%s"'
               ) % (get_table_name(path_stack), instance)
        err_msg = get_error_msg(path_stack, instance, msg)
        raise SchemaValidatorError(err_msg)


def reftable_validator(instance, schema, path_stack):
    tables = schema['tables']
    groups = schema['groups']
    if instance not in tables and instance not in groups:
        print "Groups: %s" % groups
        msg = ('Invalid refTable: Table "%s" does not exist in the schema.'
               ) % (instance)
        err_msg = get_error_msg(path_stack, instance, msg)
        raise SchemaValidatorError(err_msg)


def pervalue_validator(instance, schema, path_stack):
    col_type = get_column_type(schema, path_stack)
    for cat in instance:
        if not valid_type(cat['value'], col_type):
            msg = ('Invalid value: "%s" is not the same type as column "%s"'
                   ) % (str(cat['value']), get_column_name(path_stack))
            err_msg = get_error_msg(path_stack, '', msg)
            raise SchemaValidatorError(err_msg)


def keyvalue_validator(instance, schema, path_stack):
    if 'minLength' in instance and 'maxLength' in instance:
        if instance['minLength'] > instance['maxLength']:
            msg = 'minLength is greater than maxLength.'
            err_msg = get_error_msg(path_stack, instance, msg)
            raise SchemaValidatorError(err_msg)
    if 'minInteger' in instance and 'maxInteger' in instance:
        if instance['minInteger'] > instance['maxInteger']:
            msg = 'minInteger is greater than maxInteger.'
            err_msg = get_error_msg(path_stack, instance, msg)
            raise SchemaValidatorError(err_msg)
    if 'minReal' in instance and 'maxReal' in instance:
        if instance['minReal'] > instance['maxReal']:
            msg = 'minReal is greater than maxReal.'
            err_msg = get_error_msg(path_stack, instance, msg)
            raise SchemaValidatorError(err_msg)


def type_validator(instance, schema, path_stack):
    if 'min' in instance and 'max' in instance:
        if (isinstance(instance['min'], int) and
           isinstance(instance['max'], int)):
            if instance['min'] > instance['max']:
                msg = 'min is greater than max.'
                err_msg = get_error_msg(path_stack, instance, msg)
                raise SchemaValidatorError(err_msg)
        if isinstance(instance['min'], (unicode, str)):
            msg = 'min can not be "unlimited".'
            err_msg = get_error_msg(path_stack, instance, msg)
            raise SchemaValidatorError(err_msg)
    if 'key' in instance and 'value' in instance:
        if 'valueMap' not in instance:
            column_name = get_column_name(path_stack)
            if column_name != 'other_config' and column_name != 'external_ids':
                msg = ('There are no keys defined for this map column ' +
                       '(there is no valueMap).')
                print get_warn_msg(path_stack[:len(path_stack)-1], '', msg)
    if 'valueMap' in instance:
        if 'max' not in instance:
            msg = 'There is a "valueMap", but no "max" limit defined.'
            print get_warn_msg(path_stack, '', msg)
        else:
            if instance['max'] == 'unlimited':
                msg = ('"max" is "unlimited", but should be bounded to the ' +
                       'number of keys defined in "valueMap".')
                print get_warn_msg(path_stack, '', msg)
            else:
                if instance['max'] != len(instance['valueMap']):
                    msg = ('"max" is not equal to the number of keys defined' +
                           ' in "valueMap".')
                    print get_warn_msg(path_stack, '', msg)


def emptyvalue_validator(instance, schema, path_stack):

    last = [path_stack.pop()]

    if 'valueMap' in path_stack:
        # emptyValue for a valueMap
        # Move up to the column definition to extract the valueType
        last.insert(0, path_stack.pop())
        last.insert(0, path_stack.pop())

    parent = get_instance(schema, path_stack)

    path_stack += last
    parent_type = get_instance_type(parent)
    if not valid_type(instance, parent_type):
        msg = 'emptyValue does not have the correct type.'
        err_msg = get_error_msg(path_stack, instance, msg)
        raise SchemaValidatorError(err_msg)


def indexes_validator(instance, schema, path_stack):
    table = get_table(schema, path_stack)
    columns = table['columns']
    for index in instance:
        for column in index:
            if column not in columns:
                msg = ('Bad index: table "%s" does not contain a column ' +
                       'named "%s".') % (get_table_name(path_stack), column)
                err_msg = get_error_msg(path_stack, instance, msg)
                raise SchemaValidatorError(err_msg)


def get_ref(line, pos):
    """Return the reference at given position.

    Reference is returned as a tuple (table, column, key).
    """
    i = line.find(')', pos + 2)
    ref = line[pos+2:i].split('.')
    if len(ref) == 3:
        return ref[0], ref[1], ref[2]
    elif len(ref) == 2:
        return ref[0], ref[1], None
    elif len(ref) == 1:
        return ref[0], None, None
    return None, None, None


def doc_validator(instance, schema, path_stack):
    ref_mark = ']('
    for line in instance:
        index = line.find(ref_mark)
        while index != -1:
            table, column, key = get_ref(line, index)
            index = line.find(ref_mark, index + len(ref_mark))
            if table is not None:
                tables = schema['tables']
                if table not in tables:
                    msg = ('Wrong reference: table "%s" does not exist in ' +
                           'the schema.') % table
                    err_msg = get_error_msg(path_stack, instance, msg)
                    raise SchemaValidatorError(err_msg)
            if column is not None:
                columns = tables[table]['columns']
                if column not in columns:
                    msg = ('Wrong reference: column "%s" does not exist in ' +
                           'table "%s" in the schema.') % (column, table)
                    err_msg = get_error_msg(path_stack, instance, msg)
                    raise SchemaValidatorError(err_msg)
            if key is not None:
                column_type = columns[column]['type']
                if 'valueMap' not in column_type:
                    msg = ('Wrong reference: column "%s" in table "%s" does' +
                           ' not contain a valueMap.') % (column, table)
                    err_msg = get_error_msg(path_stack, instance, msg)
                    raise SchemaValidatorError(err_msg)
                value_map = column_type['valueMap']
                if key not in value_map:
                    msg = ('Wrong reference: key "%s" is not present in ' +
                           'column "%s" in table "%s" in the schema.'
                           ) % (key, column, table)
                    err_msg = get_error_msg(path_stack, instance, msg)
                    raise SchemaValidatorError(err_msg)


def valuemap_validator(instance, schema, path_stack):
    column_name = get_column_name(path_stack)
    if column_name == 'other_config' or column_name == 'external_ids':
        return
    if len(instance) == 0:
        msg = 'This value map is empty.'
        print get_warn_msg(path_stack, '', msg)
    key_types = {}
    for key in instance:
        key_type = get_instance_type(instance[key])
        key_types[key_type] = 0
    if len(key_types) > 1:
        msg = ('Map combines several types: ' +
               str(key_types.keys()).replace("u'", "'"))
        print get_warn_msg(path_stack, '', msg)

schemaValidators = {
    'refTable': reftable_validator,
    'follows': follows_validator,
    'per-value': pervalue_validator,
    'key': keyvalue_validator,
    'value': keyvalue_validator,
    'type': type_validator,
    'emptyValue': emptyvalue_validator,
    'doc': doc_validator,
    'indexes': indexes_validator,
    'valueMap': valuemap_validator
}


def validation_error_to_str(error):
    msg = u""
    path = 'ERROR found in #'
    for bit in error.path:
        path += '/' + bit
    msg += path + ':\n'
    msg += error.message.replace("u'", "'") + '\n'
    msg += '\nFailed validation=\n'
    msg += (error.validator + '=' +
            str(error.validator_value).replace("u'", "'") + '\n')
    msg += '\nOne or several of the following may be the possible cause:\n'
    cause = 0
    for suberror in sorted(error.context, key=lambda e: e.schema_path):
        cause = cause + 1
        msg += ('\t[' + str(cause) + '] ' +
                suberror.message.replace("u'", "'") + '\n')
    return msg


def validate(metaschema, instance):

    # Use a metaschema to validate the JSON schema rules
    validator = Draft4Validator(metaschema)
    try:
        validator.validate(instance)
    except ValidationError as error:
        err_msg = validation_error_to_str(error)
        sys.exit(err_msg)

    # Validate what metaschema can't validate
    try:
        validators.validate(instance, schemaValidators)
    except SchemaValidatorError as error:
        sys.exit(error)


if __name__ == '__main__':

    # Setup and parse arguments
    args_parser = \
        ArgumentParser(description='Validate the unified schema according to ' +
                       'the rules in the metaschema and other non-standard ' +
                       'validation criteria')

    args_parser.add_argument('--instance', type=str,
                             help='the file containing the final extschema')

    args_parser.add_argument('--metaschema', type=str,
                             help='the file containing the JSON schema rules')

    args = args_parser.parse_args()

    if not args.metaschema or not args.instance:
        sys.exit("E: Both metaschema and instance are required")

    try:
        with open(args.metaschema, 'r') as fp:
            metaschema = json.load(fp)

        with open(args.instance, 'r') as fp:
            instance = json.load(fp)
    except:
        sys.exit("E: Unable to open the file")

    # Use the rules in the metaschema to validate the instance
    validate(metaschema, instance)
