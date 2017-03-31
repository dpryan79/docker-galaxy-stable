#!/usr/bin/env python
import os
import os.path
import shutil
import subprocess
import glob

if os.path.exists("/export/groups.tsv"):
    f = open("/export/groups.tsv", "r")  # This has two columns: group, GID
    for line in f:
        cols = line.strip().split()
        subprocess.check_call(["groupadd", "-r", cols[0], "-g", cols[1]])
        subprocess.check_call(["gpasswd", "-a", "galaxy", cols[0]])
    f.close()

# Handle automounting
if os.path.exists("/export/automount"):
    os.mkdir("/etc/automount")
    for f in glob.glob("/export/automount/*"):
        if os.path.basename(f) in ["auto.master", "yp.conf", "nsswitch.conf"]:
            shutil.copy(f, "/etc/{}".format(os.path.basename(f)))
        else:
            shutil.copy(f, "/etc/automount/{}".format(os.path.basename(f)))
    subprocess.check_call(["/usr/sbin/rsyslogd"])
    subprocess.check_call(["domainname", "solsys1.immunbio.mpg.de"])
    subprocess.check_call(["/sbin/rpcbind"])
    subprocess.check_call(["/sbin/rpc.statd", "--no-notify"])
    subprocess.check_call(["/usr/sbin/ypbind"])
    subprocess.check_call(["/usr/sbin/automount"])
    subprocess.check_call(["sleep", "15"])
    #subprocess.check_call(["killall", "automount"])
    #subprocess.check_call(["/usr/sbin/automount"])

