#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################
# Felipe Torres Fabregas 
# Last modified: October 26, 2017
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# This is the logout page, it logs you out by expiring the cookie
###############################################################
from Cookie import SimpleCookie
from cgi import FieldStorage
from cgitb import enable
from datetime import datetime, timedelta

enable(display=0, logdir="/var/www/html/tmp/")

c = SimpleCookie()
c.load("DB=;    expires='Thu, 01 Jan 1970 00:00:00 GMT';;")
c.load("Email=;    expires='Thu, 01 Jan 1970 00:00:00 GMT';;")
c.load("SID=;    expires='Thu, 01 Jan 1970 00:00:00 GMT';;")

print c
print "Content-Type: text/html\n\r" # HTML is following

print "<script language='javascript'>window.location.href = 'index.cgi'</script>"
