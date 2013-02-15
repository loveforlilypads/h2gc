# security_checks.py - module to contain security checks for linux clients
# Status: this is mostly a placeholder for security checks, so I can continue development
#

import os
import subprocess
import re
import ConfigParser
import StringIO

class SecurityItem:
    def __init__(self):
        self.lastmd5 = ''
        self.currmd5 = ''
    def __str__(self):        
        return ("Security Item Object\n"
                "Last shadow file md5sum: " + str(self.lastmd5) + "\n"
                "Current shadow file md5sum: " + str(self.currmd5) + "\n")

# Check to see if any user accounts have changed
# Depends on GNU coreutils 8.13
# returns the md5 hash of /etc/shadow
#
def check_shadow_status():
    # REFACTOR - error checking - valid md5 hash string check
    out = '\n'.join(subprocess.check_output(["sudo", "md5sum", "/etc/shadow"]).splitlines())
    md5sum_shadow = StringIO.StringIO(out).readline()
    #print "Shadow md5: " + md5sum_shadow
    try:
        md5hash_only = re.search('(.+)\s+.+', md5sum_shadow).group(1)
    except:
        print "Looks like we don't have a valid md5sum string here here."
    #print "Hash md5: " + md5hash_only
    return md5hash_only
