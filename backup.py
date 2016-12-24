import os
import subprocess
from datetime import datetime

class style:
   BOLD = '\033[1m'
   END = '\033[0m'

# Define some critica vars
backup = "wieting.tar.gz"
cwd = os.getcwd()
stick = "/Volumes/WIETING"
server = "wieting.dev"
user = "vagrant"
userAtServer = user + "@" + server
drush_alias = "@wieting"

# Get the current time and build a destination file name
timeStamp = datetime.now().strftime('%Y-%m-%d_%H:%M')
file = backup + "_" + str(timeStamp)
destination = "/tmp/" + file
local = cwd + "/" + file

# Define the 'drush ard' command and run it remotely via ssh.  check_call returns 0 if no error, or a traceback if there is
drush_ard = "drush " + drush_alias + " ard default --yes --no-core --destination=" + destination + " --overwrite"
print style.BOLD + "\nLaunching a remote 'drush ard' command via ssh..." + style.END
error = subprocess.check_call([ "ssh", userAtServer, drush_ard ]);

# No problem...rsync the file back to the host
args = [ "rsync", "-aruvi", userAtServer + ":" + destination, cwd ]
print style.BOLD + "\nRunning '" + ' '.join(args) + "' to copy the backup to your host..."  + style.END
error = subprocess.check_call(args)

# If stick is mounted, copy the backup there too
if os.path.isdir(stick):
    args = ["rsync", "-aruvi", local, stick]
    print style.BOLD + "\nRunning '" + ' '.join(args) + "' to copy the backup to your mounted " + stick + " volume..."  + style.END
    error = subprocess.check_call(args)
    files = filter(os.path.isfile, os.listdir(stick))
    print "\nContents of " + stick + " includes: "
    for f in files:
        print "  " + f
    print "\n\n"

else:
    print style.BOLD + "\nMount a portable drive at " + stick + " and use "
    print "  'rsync -aruvi " + local + " " + stick + "' to copy the backup there." + style.END

"""
# Use 'rootstalk_site_backup' from your HOST machine to backup a copy of the existing default database and files.
alias vm_create_backup="
  time=$(date '+%Y.%m.%d-%H-%M'); 
  dest=/tmp/${time}/rs.tar.gz;
  ssh dguser@rootstalk.grinnell.edu \"drush @drupalvm ard default --yes --no-core --destination=/tmp/${dest}/rs.tar.gz --overwritedrush @drupalvm ard default --yes --no-core --destination=/tmp/${dest}/rs.tar.gz --overwrite\" "  
alias rsync_file_message1="printf \"Transfering backup to the current directory on the host (your local machine)... \n\""
alias rsync_file_message2="printf \"Transfering backup to '/Volumes/ROOTSTALK' directory on your local machine... \n\""
alias no_ROOTSTALK_device="printf \"Attention: Mount a USB stick named ROOTSTALK and run 'save_backups_to_ROOTSTALK' if you wish to backup to a device. \n\""
alias backup_complete_message="printf \"File backup complete!!! The contents of the flash drive include: \n\""
alias vm_pull_to_host1="rsync_file_message1; rsync -aruvi dguser@rootstalk.grinnell.edu:/tmp/*/rs.tar.gz . "
alias save_backups_to_ROOTSTALK="
  rsync_file_message2; 
  rsync -aruvi */rs.tar.gz /Volumes/ROOTSTALK/; 
  backup_complete_message; 
  ls /Volumes/ROOTSTALK;"
alias rootstalk_site_backup="
  vm_create_backup; 
  vm_pull_to_host1; 
  if [ -d \"/Volumes/ROOTSTALK\" ]; then
    save_backups_to_ROOTSTALK
  else
    no_ROOTSTALK_device
  fi"
# Use rootstalk_vm_restore from your HOST machine to restore a copy fo the default database and files.
alias vm_push_to_vm="rsync -aruvi ./rootstalk.tar.gz dguser@dgdevx.grinnell.edu:/var/www/html/drupal/"
alias vm_restore_backup="ssh dguser@rootstalk.grinnell.edu \"cd /var/www/html/drupal; drush arr -v rootstalk.tar.gz default --overwrite --tar-options='vz'; cd web/sites/default; drush cr all\""
alias rootstalk_vm_restore="vm_push_to_vm; vm_restore_backup"
"""
