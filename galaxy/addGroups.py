#!/usr/bin/env python
import os.path
from subprocess

if os.path.exists("/export/groups.tsv"):
    f = open("/export/groups.tsv", "r")  # This has two columns: group, GID
    for line in f:
        cols = line.strip().split()
        subprocess.check_call(["groupadd", "-r", cols[0], "-g", cols[1]])
        subprocess.check_call(["gpasswd", "-a", "galaxy", cols[0]])
    f.close()
