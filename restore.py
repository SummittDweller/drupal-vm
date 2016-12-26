""" restore.py

Use this Python script from the command line (terminal) in combination with backup.py.  You should first cd to
  a directory holding one or more *.tar.gz backups prepared using backup.py.  This script will always select
  the most recent copy of *.tar.gz.

This script depends on vars.py, and you must define your site and user parameters in vars.py before performing
  a backup/restore operation.

"""

from colorama import init
from colorama import Style, Fore, Back
import vars
import os
import glob
import subprocess

init()

cwd = os.getcwd()
userAtServer = vars.user + "@" + vars.server
path = "/home/" + vars.user + "/" + vars.backup

# Find the latest file matching the backup* filename pattern
file_path = max(glob.iglob(vars.backup + '*'), key=os.path.getctime)

# rsync (push) the file to the remote from this host
args = [ "rsync", "-aruvi", file_path, userAtServer + ":" + path ]
print Style.BRIGHT + "\nRunning '" + Fore.GREEN + ' '.join(args) + Fore.RESET + "' to copy the backup to the server..."  + Style.RESET_ALL
error = subprocess.check_call(args)

# Extract everything from the tar file
command = "tar -xzvf " + path + " -C " + vars.site_path
args = [ "ssh", userAtServer, command ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET + " to extract files from the backup... " + Style.RESET_ALL
error = subprocess.check_call(args);

# Define a drush sql-cli command to restore the database
command = "sql-cli < " + vars.site_path + "/files/" + vars.server + ".sql"
args = [ "ssh", userAtServer, vars.drush, vars.drush_alias, command ]
print Style.BRIGHT + "\nLaunching remote " + Fore.GREEN + " ".join(args) + Fore.RESET + " to restore the database from backup..." + Style.RESET_ALL
error = subprocess.check_call(args);

# Cleanup the remote sever
args = [ "ssh", userAtServer, "rm -f", path + "* ", vars.site_path + "/files/*.sql" ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET + " to cleanup the remote server... " + Style.RESET_ALL
error = subprocess.check_call(args)

print "\n\n"
