#!/usr/bin/env python

from __future__ import print_function

import json
import subprocess
import sys
from os.path import isfile


urls_to_transfer = json.loads("""
{urls}
""")

# format of urls_to_transfer
#
# [
#   {{
#      u: "url",
#      o: "output path",
#      c: [
#            ["command", "args", ...],
#            ...
#         ]
#   }},
#   ...
# ]
#

for u in urls_to_transfer:
    url = u["u"]
    output_path = u["o"]
    transfer_commands = u["c"]

    print("Downloading %s..." % url, file=sys.stderr)
    if isfile(output_path):
        print("File from %s already exists at %s" % (url, output_path), file=sys.stderr)
        continue

    for command in u["c"]:
        try:
            print(" ".join(command), file=sys.stderr)
            subprocess.check_call(command)
            print("%s saved to %s" % (url, output_path), file=sys.stderr)
            break
        except subprocess.CalledProcessError:
            print("Failed to transfer. Trying next command...", file=sys.stderr)
