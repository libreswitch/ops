#!/usr/bin/env python

# LIBRARY IMPORT
from collections import OrderedDict

GENERATION_WARNING = ' AUTOMATICALLY GENERATED CODE; DO NOT MODIFY '

# LineType definition
LT_DOC = 0
LT_COMMENT = 1
LT_DEF = 2

# Schema keys
EMPTY_VALUE_KEY = 'emptyValue'
VALUE_MAP_KEY = 'valueMap'
TYPE_KEY = 'type'
COLUMNS_KEY = 'columns'
TABLES_KEY = 'tables'


def dump_string(line_type, string, value=None):
    dump_str = ''
    if line_type == LT_COMMENT:
        dump_str += '\n\n// %s' % string
    elif line_type == LT_DEF:
        c_value = value
        if isinstance(value, str) or isinstance(value, unicode):
            c_value = '"' + str(value) + '"'
        elif isinstance(value, bool):
            c_value = str(value).lower()
        dump_str += '\n#define {:<80} {}'.format(string.upper(), c_value)
    elif line_type == LT_DOC:
        dump_str += '\n/* %s */\n' % string
    return dump_str


def generate_header_text(dbname):
    '''
    Dump the license and main messages in the header of the file
    '''
    header_str = '''/*
 * Copyright (C) 2015-2016 Hewlett-Packard Development Company, L.P.
 * All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *
 * Purpose: This file contains automatically generated constant definitions and
 *          enums to represent valid values for maps of string-string pairs in
 *          the OVSDB schema.
 */
'''
    dbname = dbname.upper()
    header_str +=\
        ('\n#ifndef %s_EMPTY_VALUES_HEADER' +\
         '\n#define %s_EMPTY_VALUES_HEADER') % (dbname, dbname)

    # This global definitions are only required for OpenSwitch database
    if dbname == 'OPENSWITCH':
        header_str += dump_string(LT_COMMENT,
                                  '{:*^100}'.format(' GLOBAL DEFINITIONS '))
        header_str += dump_string(LT_COMMENT,
                                  'Default VRF name used during system bootup')
        header_str += dump_string(LT_DEF,
                                  'DEFAULT_VRF_NAME', 'vrf_default')
        header_str += dump_string(LT_COMMENT,
                                  'Default bridge name used during system bootup')
        header_str += dump_string(LT_DEF,
                                  'DEFAULT_BRIDGE_NAME', 'bridge_normal')
    return header_str


def generate_footer_text(dbname):
    return "\n\n#endif /* %s_EMPTY_VALUES_HEADER */" % dbname.upper()


def dump_empty_values(schema, name):
    empty_value_str = ''
    if EMPTY_VALUE_KEY in schema:
        name = name.replace('-', '_').replace(' ', '_')
        name += '_EMPTY_VALUE'
        empty_value_str = dump_string(LT_DEF, name, schema[EMPTY_VALUE_KEY])
    return empty_value_str


def empty_values_generator(schema):
    tables = schema[TABLES_KEY]
    definitions_str = ''
    for tbl_name, tbl_schema in tables.iteritems():
        for col_name, col_schema in tbl_schema[COLUMNS_KEY].iteritems():

            # Extract the column's empty values
            name = '_'.join(['OVSREC', tbl_name, col_name])
            col_ev = dump_empty_values(col_schema, name)

            # Extract the map's empty values
            if 'type' in col_schema and VALUE_MAP_KEY in col_schema[TYPE_KEY]:
                for map_key, map_schema in\
                        col_schema[TYPE_KEY][VALUE_MAP_KEY].iteritems():
                    name = '_'.join(['OVSMAP', tbl_name, col_name, map_key])
                    col_ev += dump_empty_values(map_schema, name)

            if col_ev:
                header_str = 'Empty values for column ' + col_name
                definitions_str += dump_string(LT_COMMENT, header_str)
                definitions_str += col_ev

    if not definitions_str:
        definitions_str = '\n\n// No empty values for this database'
    else:
        warning_str = '{:*^100}'.format(GENERATION_WARNING)
        definitions_str = dump_string(LT_COMMENT, warning_str) + definitions_str

    return definitions_str


def dump_strings_to_file(output_filename, strings):
    try:
        with open(output_filename, 'w') as fd:
            fd.truncate()
            fd.write(strings)
    except:
        print "E: Unable to write the output file"
        raise

def generate_empty_values(schema, output_filename):
    '''
    Generate a file containing the C header definitions with the
    empty values extracted out of the schema
    '''

    header = generate_header_text(schema['name'])
    empty_values = empty_values_generator(schema)
    footer = generate_footer_text(schema['name'])
    definitions = header + empty_values + footer
    dump_strings_to_file(output_filename, definitions)


if __name__ == "__main__":

    import json

    EXTSCHEMA_FILE = "vswitch.extschema.new"

    with open(EXTSCHEMA_FILE, 'r') as f:
        schema = json.load(f, object_pairs_hook=OrderedDict)
        generate_empty_values(schema, '/ops-empty-values.h')
