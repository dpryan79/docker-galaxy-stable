#!/usr/bin/env python3
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
    os.makedirs("/etc/automount", exist_ok=True)
    for f in glob.glob("/export/automount/*"):
        try:
            if os.path.basename(f) in ["auto.master", "yp.conf", "nsswitch.conf"]:
                shutil.copy(f, "/etc/{}".format(os.path.basename(f)))
            else:
                shutil.copy(f, "/etc/automount/{}".format(os.path.basename(f)))
        except:
            pass
    subprocess.check_call(["/usr/sbin/rsyslogd"])
    subprocess.check_call(["domainname", "solsys1.immunbio.mpg.de"])
    subprocess.check_call(["/sbin/rpcbind"])
    subprocess.check_call(["/usr/sbin/ypbind"])
    subprocess.check_call(["/usr/sbin/automount"])
    subprocess.check_call(["sleep", "15"])

if not os.path.exists("/etc/galaxy/tool_data_table_conf.xml"):
    subprocess.check_call(["sleep", "15"])
    if os.path.exists("/export/galaxy-central/config/tool_data_table_conf.xml"):
        os.symlink("/export/galaxy-central/config/tool_data_table_conf.xml", "/etc/galaxy/tool_data_table_conf.xml")
    else:
        os.symlink("/export/galaxy-central/config/tool_data_table_conf.xml.sample", "/etc/galaxy/tool_data_table_conf.xml")

subprocess.check_call(['sed', '-i', 's/ 22/ 8022/', '/etc/proftpd/proftpd.conf'])
subprocess.check_call(['sed', '-i', 's:/tmp/nginx_upload_store:/export/nginx_upload_store:', '/ansible/roles/galaxyprojectdotorg.galaxyextras/defaults/main.yml'])
