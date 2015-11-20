#!/usr/bin/env python
'''
Strips all keys in DROP_KEYS from input-schema and writes the resulting
OpenvSwitch-ready schema to output-schema.
'''

import sys
from subprocess import Popen, PIPE
from collections import OrderedDict
import json

DROP_KEYS = ('category', 'relationship')

def delete_keys(objname):
    for key in DROP_KEYS:
        objname.pop(key, None)
    for key, value in objname.iteritems():
        if type(value) == OrderedDict:
            delete_keys(value)

#
# main
#
if len(sys.argv) < 3:
    print("Usage: sanitize.py input-schema output-schema")
    sys.exit(1)

orig_schema, ovs_schema = sys.argv[1:3]

f = open(orig_schema).read()
schema = json.loads(f, object_pairs_hook=OrderedDict)

delete_keys(schema)
# Remove any top-level "cksum" present in the input
schema.pop("cksum", None)

# Calculate new checksum.
schema_text = json.dumps(schema, indent=2, separators=(',', ': ')) + '\n'
cksum_pipe = Popen('cksum', stdin=PIPE, stdout=PIPE)
output, err = cksum_pipe.communicate(input=schema_text)

# Keep the 'cksum' key at the top of the OrderedDict so that the JSON
# output will have it at the start, and the broken validation code in
# openvswitch still works.
cksum = ' '.join(output.split()[:2])
schema_cksum = OrderedDict([('cksum', cksum)])
schema_cksum.update(schema)

# Rewrite with cksum field added.
with open(ovs_schema, 'w') as fp:
    json.dump(schema_cksum, fp, indent=2, separators=(',', ': '))
    fp.write('\n')
