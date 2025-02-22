#!/usr/bin/env python3

#
# check_df_output
#
# checks the output of `df -h` for a partition
# based on the % used
#
# author: Keobi Web Hosting
# website: https://github.com/keobi/nagios-plugin-df-output
#

import argparse
import subprocess
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("partition")
parser.add_argument("-c", dest="critical", type=int)
parser.add_argument("-w", dest="warning", type=int)
args = parser.parse_args()

results = subprocess.run("df -h", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

usage = None

for output in results.stdout.decode().split("\n"):
    if not output.strip().endswith(args.partition):
        continue

    if match := re.search(r"(\d+)%", output):
        usage = int(match.group(1))

    break

if not usage:
    print(f"UNKNOWN - '{args.partition}' not found in df output")
    sys.exit(3)

def output(exit_code):
    if exit_code == 0:
        status = "OK"
    elif exit_code == 1:
        status = "WARNING"
    elif exit_code == 2:
        status = "CRITICAL"
    else:
        status = "UNKNOWN"

    print(f"{status} - '{args.partition}' at {usage}%")
    sys.exit(exit_code)

if usage > args.critical:
    output(2)
elif usage > args.warning:
    output(1)
else:
    output(0)