#!/usr/bin/python
"""
Router rebooter

Reboots Netgear DG834 ADSL router

Copyright (C) 2011 Nick Craig-Wood <nick@craig-wood.com>. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY NICK CRAIG-WOOD ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL NICK CRAIG-WOOD OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import urllib
import urllib2
from subprocess import Popen, PIPE
import smtplib
from email.mime.text import MIMEText

# Change the config here and then comment out the line below
raise AssertionError("Unconfigured")
url = "http://1.2.3.4/setup.cgi" # replace 1.2.3.4 with the IP of your router
username = "admin"
password = "routerpassword"     # the password for your router
external_addr = "8.8.8.8"       # choose an external IP just at the other end of your ADSL connection
EMAIL = "you@your-email-account.com" # email address for notifications
mail_server = "localhost"            # address of SMTP server

def send_email(email, message):
    """
    Sends a simple message to email
    """
    print "Sending email %r to %r" % (message, email)
    msg = MIMEText(message)
    msg['Subject'] = message
    msg['From'] = email
    msg['To'] = email
    s = smtplib.SMTP(mail_server)
    s.sendmail(email, [email], msg.as_string())
    s.quit()
    print "Sent email"

def ping(host, wait=1, n=10):
    """
    Pings the host n times waiting for wait seconds for each ping

    Wait increases by 50% each time

    If any pings are returned then it returns True otherwise False
    """
    for i in range(1, n+1):
        print "Ping attempt %d: %s" % (i, host)
        prog = ["ping", "-n", "-c", "1", "-w", str(wait), host]
        p = Popen(prog, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate("")
        output = stdout + stderr
        rc = p.returncode
        #print "Ping returned %r: %r" % (rc, output)
        if rc == 0:
            print "Ping OK"
            return True
        wait *= 1.5
    print "Ping failed"
    return False

def reboot():
    """
    Reboot the router
    """
    print "Rebooting..."
    values = dict(next_file="diag.htm",
                  this_file="diag.htm",
                  todo="reboot",)
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    host = urllib.splithost(urllib.splittype(url)[1])[0]
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, host, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler).open
    response = opener(req)
    out = response.read()
    response.close()
    if "reboot_pg.htm" in out:
        print "Success"
    else:
        raise RunTimeError("Failed to reboot: %r" % out)

def main():
    """
    Ping the external addr and reboot router if it doesn't ping
    """
    if not ping(external_addr):
        reboot()
        send_email(EMAIL, "Rebooted router")
    
if __name__ == "__main__":
    main()
    #print ping(external_addr)
    #reboot()

