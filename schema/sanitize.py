import json
from types import *
import sys
import subprocess

def delete_keys(objname, keys):
    if type(objname) is not DictType:
        return

    for key in keys:
        objname.pop(key, None)
    for key, value in objname.iteritems():
        delete_keys(value, keys)

if __name__ == '__main__':

    exit
    # read the json ovs schema
    with open(sys.argv[1]) as x: f = x.read()
    ovsschema =  json.loads(f)

    # delete the keys
    delete_keys(ovsschema, ['category', 'relationship'])

    if 'cksum' in ovsschema:
        ovsschema.pop('cksum')
    if len(sys.argv) < 3:
        print("Error: Script needs 2 argument (input-schema output-schema)")
    else:
        with open(sys.argv[2], 'w') as fp:
            json.dump(ovsschema, fp, sort_keys = True, indent=4, separators=(',', ': '))
            fp.write('\n')

        # calculates the new check sum
        cksum =  subprocess.Popen(['cksum', sys.argv[2]], stdout=subprocess.PIPE)
        output, err = cksum.communicate()
        csa = output.split(' ')
        csa.pop()
        str1 = " "
        ovsschema['cksum'] = str1.join(csa)
        print(output)

        # dump the json, give the option to sort it and save it to a new file
        with open(sys.argv[2], 'w') as fp:
            json.dump(ovsschema, fp, sort_keys = True, indent=4, separators=(',', ': '))
            fp.write('\n')
