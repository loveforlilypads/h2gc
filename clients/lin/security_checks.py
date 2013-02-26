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

# Check the status of local system security
#
# modifies: security list
#
def check_security_status(security_list, config_p):
    md5item = security_checks.SecurityItem()
    md5item.currmd5 = security_checks.check_shadow_status()
    md5item.lastmd5 = config_p.get('Security', 'shadowmd5', 0)    
    security_list.append(md5item)

# Log analysis of security data to local log file
# modifies: status object, config file with new md5 if necesary
#
def log_security_data(security_list, status, config_p):
    
    for item in security_list:
        print item
        if item.currmd5.strip() != item.lastmd5.strip():
            status.overall += 50
            print "Security status +50 because: " + item.currmd5 + " is NOT the same as: " + item.lastmd5 + "\n"
            config_p.set("Security","shadowmd5",item.currmd5)
        else:
            print "Security status adds zero because: " + item.currmd5 + " is the same as: " + item.lastmd5 + "\n"

#################################
#
def main():
    check_security_status(security_list, config_p)
    log_security_data(security_list, config_p)

if __name__ == '__main__':
    main()
