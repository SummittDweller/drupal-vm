""" vars.py

This Python script defines variables for use by backup.py and restore.py.
Define some critical vars.  These need to be modified for each project!  Use 'drush status' to determine some values.

"""

backup = "wieting.tar.gz"                                         # name the backup file
stick = "/Volumes/WIETING"                                        # name of a mounted drive to accept a copy of the backup
server = "wieting.dev"                                            # the remote server name
user = "vagrant"                                                  # admin user on the remote server
drush_alias = "@wieting.wieting.dev"                              # drush alias for the remote site
site_path = "/var/www/drupalvm/drupal/web/sites/default"          # path to the Drupal site on the remote server
drush = "/var/www/drupalvm/drupal/vendor/drush/drush/drush.php"   # remote server path to drush
