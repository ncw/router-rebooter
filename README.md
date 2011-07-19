Router Rebooter
===============

Reboot your Netgear DG834 ADSL router when your ADSL connection drops.

I wrote this because my router seems to lock up once a week or so, and requires a reboot.  This annoyed the rest of the family a lot so I automated the reboot process.

Installation
------------

Check out this project (say in your home directory)

Edit the top of the file which looks like this

    # Change the config here and then comment out the line below
    raise AssertionError("Unconfigured")
    url = "http://1.2.3.4/setup.cgi" # replace 1.2.3.4 with the IP of your router
    username = "admin"
    password = "routerpassword"     # the password for your router
    external_addr = "8.8.8.8"       # choose an external IP just at the other end of your ADSL connection
    EMAIL = "you@your-email-account.com" # email address for notifications

Find the external_addr with traceroute

Crontab
-------

Now add the script onto your crontab (it can run as a user not root) something like this.  Edit your crontab by typing "crontab -e" and add lines like this

    # Reboot the router if it has gone wrong
    */5 * * * * /home/user/router-rebooter/router_rebooter.py >>/tmp/router_rebooter.log 2>&1

Change the path as appropriate.

In Use
------

This will check your ADSL line is up every 5 minutes and if it isn't it will reboot your router.

Testing
-------

To test the script, change external_addr to something which definitely isn't reachable eg "1.1.1.1" (test first with ping!)

License (Simplified BSD)
------------------------

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

Author
------

Nick Craig-Wood
nick@craig-wood.com
http://www.craig-wood.com/nick/
https://github.com/ncw/router-rebooter
