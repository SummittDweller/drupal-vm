""" backup.py

Use this Python script from the command line (terminal) in combination with restore.py.  This script will create a
 *.tar.gz containing an SQL dump and a tar of vars.site_path files.

This script depends on vars.py, and you must define your site and user parameters in vars.py before performing
  a backup/restore operation.

"""

from colorama import init
from colorama import Style, Fore, Back
import vars
import os
import subprocess
import sys
from datetime import datetime

init()

# Get the current time and build a destination file name
timeStamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
file = vars.backup + "_" + str(timeStamp)
destination = "/home/" + vars.user + "/" + file
userAtServer = vars.user + "@" + vars.server

cwd = os.getcwd()
local = cwd + "/" + file

# Cleanup the remote server before beginning
command = "rm -f /home/" + vars.user + "/" + vars.server + ".sql /home/" + vars.user + "/" + vars.backup
args = [ "ssh", userAtServer, command ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET + " to clean up... " + Style.RESET_ALL
error = subprocess.check_call(args);

# Try 'drush sql-dump' instead of 'drush ard', it's easier to control
command = "sql-dump --result-file=" + vars.site_path + "/files/" + vars.server + ".sql --skip-tables-key=common"
args = [ "ssh", userAtServer, vars.drush, vars.drush_alias, command ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET +" to dump the database... " + Style.RESET_ALL
error = subprocess.check_call(args);

# Follow up with a 'tar' command under better control
skip = [ "config_*", "*/css/*", "*/js/*", "*/php/*", "*services.yml", "*settings.php" ]
exclude = " --exclude=".join(skip)
command = "tar -czvf " + destination + " -C " + vars.site_path + " . /home/" + vars.user + "/*.sql --exclude=" + exclude
command = "tar -czvf " + destination + " -C " + vars.site_path + " . --exclude=" + exclude
args = [ "ssh", userAtServer, command ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET + " to create a backup... " + Style.RESET_ALL
error = subprocess.check_call(args);

# No problems thus far?...rsync the file back to the host
args = [ "rsync", "-aruvi", userAtServer + ":" + destination, cwd ]
print Style.BRIGHT + "\nRunning " + Fore.GREEN + ' '.join(args) + Fore.RESET + " to copy the backup to your host..."  + Style.RESET_ALL
error = subprocess.check_call(args)

# If stick is mounted, copy the backup there too
if os.path.isdir(vars.stick):
    args = ["rsync", "-aruvi", local, vars.stick]
    print Style.BRIGHT + "\nRunning " + Fore.GREEN + ' '.join(args) + Fore.RESET + " to copy the backup to your mounted " + vars.stick + " volume..."  + Style.RESET_ALL
    error = subprocess.check_call(args)
    files = filter(os.path.isfile, os.listdir(vars.stick))
    print "\nContents of " + vars.stick + " includes: "
    for f in files:
        print "  " + f
    print "\n\n"

else:
    print Style.BRIGHT + "\nMount a portable drive at " + vars.stick + " and use "
    print Fore.GREEN + "  'rsync -aruvi " + local + " " + vars.stick + "' " + Fore.RESET + "to copy the backup there.\n\n" + Style.RESET_ALL
