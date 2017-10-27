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

enable(display=0, logdir="/var/www/html/tmp/")

c = SimpleCookie()
exp_date = datetime.utcnow() + timedelta(seconds=10800)
c.load('DB='';    expires=-31104000; ;'
c.load('Email=''; expires=-31104000; ;' 
c.load('SID='';   expires=-31104000; ;'

print "Content-Type: text/html\n\r" # HTML is following

print "<script language='javascript'>window.location.href = 'index.cgi'</script>"
