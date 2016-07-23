#!/usr/bin/env python

import xml.etree.ElementTree as ET
import xml.dom.minidom as xmlPrint

# CONSTANTS
TITLE = 'OpenSwitch Configuration Database'


def set_empty_value(node, schema_value):
    if 'emptyValue' in schema_value:
        value = schema_value['emptyValue']
    node_value = str(value).lower() if isinstance(value, bool) else str(value)
    node.set('empty_value', node_value)


def generate_xml(json, xml_filename):
    tables = json['tables']

    root = ET.Element('database', title=TITLE)
    xmlschema = ET.ElementTree()
    xmlschema._setroot(root)
    for table, tableschema in tables.iteritems():
        table_node = ET.SubElement(root, 'table')
        table_node.set('name', table)
        for column, columnschema in tableschema['columns'].iteritems():
            if isinstance(columnschema['type'], dict) and\
                    'valueMap' in columnschema['type']:
                for key, keyschema in\
                        columnschema['type']['valueMap'].iteritems():
                    column_node = ET.SubElement(table_node, 'column')
                    column_node.set('key', key)
                    column_node.set('name', column)
                    if 'emptyValue' in keyschema:
                        set_empty_value(column_node, keyschema)
                    if isinstance(keyschema['type'], dict):
                        column_node.set('type',
                                        '%s' % keyschema['type']['type'])
                    else:
                        column_node.set('type',
                                        '%s' % keyschema['type'])
            else:
                column_node = ET.SubElement(table_node, 'column')
                column_node.set('name', column)
                if 'emptyValue' in columnschema:
                    set_empty_value(column_node, columnschema)
                if 'keyname' in columnschema:
                    column_node.set('keyname', columnschema['keyname'])
                if isinstance(columnschema['type'], dict):
                    key = columnschema['type']['key']
                    column_type = key['type'] if isinstance(key, dict) else key
                    column_node.set('type', '%s' % column_type)
                else:
                    column_node.set('type',
                                    '%s' % columnschema['type'])

    xmlschema.write(xml_filename)
    xml = xmlPrint.parse(xml_filename)
    with open(xml_filename, 'w+') as output:
        output.write(xml.toprettyxml())
