#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################
# Felipe Torres Fabregas 
# Last modified: October 27, 2017
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# This is used to download the result of the query done.
###############################################################
from cgi import FieldStorage
import cgitb; cgitb.enable()
from sys import path
from datetime import datetime
path.insert(0, '../Python_QB/')
from initial_testing import *
import Cookie
from os import environ

print "Content-Type: text/html"
print

form = FieldStorage()
Query = form.getvalue("Query")
DB = form.getvalue("DB")
cookie_string=environ.get('HTTP_COOKIE')
c=Cookie.SimpleCookie()
c.load(cookie_string)
Data = Database(c['DB'].value)
schema = Data.SetSchema(DB)
if Query and schema != False: 
	RESULT, title, Error = Data.RandomQDown(Query)
	if Error == False: 
		LINE = []
		for item in RESULT:
			line = []
			for row in item:
				try: 
					row%1
					line.append(row)
				except:
					line.append(str(row))
			LINE.append(line)
		for item in LINE:
			print str(item)[1:-1]
	else:
		print "** ERROR **, There was an error with the Query."
		print "If the erro persist contact the administrator.\n Please send a email to admin@querybuilder-lcp.mit.edu"
		print "\n\n" + str(Error)
else:
	print "ERROR, There was a problem with the Query, please contact the administrator.\n Please send a email to admin@querybuilder-lcp.mit.edu"
