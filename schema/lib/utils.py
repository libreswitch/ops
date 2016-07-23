#!/usr/bin/env python
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import json

from os.path import abspath, basename
from collections import OrderedDict
from tempfile import NamedTemporaryFile
from pycksum import Cksum


class MyOrderedDict(OrderedDict):

    def prepend(self, key, value, dict_setitem=dict.__setitem__):

        root = self._OrderedDict__root
        first = root[1]

        if key in self:
            link = self._OrderedDict__map[key]
            link_prev, link_next, _ = link
            link_prev[1] = link_next
            link_next[0] = link_prev
            link[0] = root
            link[1] = first
            root[1] = first[0] = link
        else:
            root[1] = first[0] = self._OrderedDict__map[key] =\
                [root, first, key]
            dict_setitem(self, key, value)


def format_bool(string):
    if string in ['True', 'False']:
        string = string.lower()
    return string


def calculate_cksum(schema):
    '''
    Update the input schema with the corresponding
    dictionary value for the calculated cksum
    '''
    CKSUM_KEY = 'cksum'

    schema = MyOrderedDict(schema)

    if CKSUM_KEY in schema:
        schema.pop(CKSUM_KEY)

    formatted_schema = json.dumps(schema,
                                  indent=2,
                                  separators=(',', ': '))

    c = Cksum()
    c.add(formatted_schema)
    cksum_string = '%d %d' % (c.get_cksum(), c.get_size())

    schema.prepend(CKSUM_KEY, cksum_string)

    return schema


def convert_enums(dictionary):
    '''
    Looks for enums recursively in the dictionary and converts them to a list
    # of keywords, removing the 'set' entry. E.g. from
    # 'enum': ['set', [<keywords>]] to 'enum': [<keywords>]
    '''
    if 'enum' in dictionary:
        if len(dictionary['enum']) > 1 and \
                isinstance(dictionary['enum'][1], list):
            dictionary['enum'] = dictionary['enum'][1]
        else:
            dictionary['enum'] = dictionary['enum']
    else:
        for key in dictionary:
            if isinstance(dictionary[key], dict):
                convert_enums(dictionary[key])


def dump_json(json_obj, filename, unique_names=False):
    '''
    Dumps the given json object to a file with the given name
    '''

    try:
        final_name = filename
        if unique_names:
            dirname = abspath(filename)
            fn = basename(filename)
            fd = NamedTemporaryFile(dir=dirname,
                                    prefix=fn,
                                    delete=False)
        else:
            fd = open(final_name, 'w')
        json.dump(json_obj, fd, indent=2, separators=(',', ': '))
        print 'Created %s' % final_name
    except Exception as e:
        print 'E: Couldn\'t create or write %s: %s' % (final_name, e)
    finally:
        fd.close()

    return final_name


def load_json(filename, ordered=True):
    with open(filename, 'r') as f:
        if ordered:
            return json.load(f, object_pairs_hook=OrderedDict)
        else:
            return json.load(f)
