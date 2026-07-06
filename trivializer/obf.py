#!/usr/bin/env python3

#
# obf.py: obfuscate fr-min.py.
#

import base64 as b, gzip as z, os, sys

path = os.path.join(os.path.dirname(__file__), 'fr-min.py')
s = b.z85encode(z.compress(open(path).read().strip().encode())).decode()

print(f'''
import base64 as b,gzip as z
exec(z.decompress(b.z85decode('{s}')))
'''.strip())
