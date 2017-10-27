#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################
# Felipe Torres Fabregas 
# Last modified: October 26, 2017
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# This file contains the user query history
###############################################################
from Cookie import SimpleCookie
from cgi import FieldStorage
from sys import path, exit
from cgitb import enable
from os import environ

path.insert(0, '../Python_QB/')
from initial_testing import *
enable(display=0, logdir="/var/www/html/tmp/")

print "Content-Type: text/html\n\r" # HTML is following

if environ.has_key('HTTP_COOKIE'):
  Co = ""
  for cookie in environ['HTTP_COOKIE'].split(';'):
    if "SID" in cookie or "Email" in cookie or "DB" in cookie:
      Co += cookie + ";"
  c=SimpleCookie()
  c.load(Co)
else:
  print "<script>alert('Please login.');</script>"
  print "<script language='javascript'>window.location.href = 'index.cgi'</script>"
  exit(0)
try:
  SModel = SessionModel()
  data = c['SID'].value
  if not (SModel.GetSession(int(data))):
    print "<script>alert('There was an error with the session'));});</script>"
    print "<script language='javascript'>window.location.href = 'index.cgi'</script>"
    exit(0)
except KeyError:
  print "<script>alert('There is a problem with your login information.');</script>"
  print "<script language='javascript'>window.location.href = 'index.cgi'</script>"
  exit(0)

email = c['Email'].value
Query_History = UserModel().GetQueriesByEmail(email)

def DocDashboard(email, Query_History):
  NumberOfRows = 100
  print "<html lang='en'><head>"
  print Header
  print """</head><body>
  <nav class="navbar navbar-default" role="navigation" style="margin-bottom: 0">
  <div class="navbar navbar-fixed-top navbar-header">
    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse"></button>
    <a class="navbar-brand" href="dashboard.cgi">Query Builder v1.1</a>
    <ul class="nav navbar-top-links navbar-right">
      <li class="dropdown">
        <a class="dropdown-toggle" data-toggle="dropdown" style="font-size:18px;" href="">%s
          <i class="fa fa-user fa-fw"></i>  <i class="fa fa-caret-down"></i>
        </a>
        <ul class="dropdown-menu dropdown-user">
          <li><a id="home" href="dashboard.cgi"><i class="fa fa-cog fa-fw"></i> Query Builder</a>
          <li><a id="create-user"  href="User.cgi"><i class="fa fa-user fa-fw"></i> User Profile</a>
          </li>
          <li class="divider"></li>
          <li><a href="/logout.cgi"><i class="fa fa-sign-out fa-fw"></i> Logout</a>
          </li></ul></li></ul></div></nav>""" % email
  print  """<div id="container">
     <div class="container-fluid box">
     <br>
      <div class="row">
<div class="col-sm-2"></div>

<div class="col-sm-4">
  <p class="text-muted" style="font-size:18px;">User information</p>
  <ul class="list-group">
    <li class="list-group-item" style="font-size:18px;">Email: %s </li>
  </ul>
</div>"""  % (email)
  print """<div class="col-sm-4"></div><div class="col-sm-2"></div></div>
  <div class="row">
<div class="col-sm-2"></div>
<div class="col-sm-8">
  <p class="text-muted" style="font-size:18px;">Last %s queries</p>
  <ul class="list-group">""" % len(Query_History)
  for item in Query_History:
    print """<li class="list-group-item list-group-item-action" style="font-size:18px;">%s</li>""" % item
  print """</ul></div><div class="col-sm-2"></div></div> 
  </div></body></html>"""

Header = """
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Query Builder</title>
    <link rel="shortcut icon" href="media/favicon.ico">
    <link rel='stylesheet' type='text/css' href="css/metisMenu.min.css" />
    <link rel='stylesheet' type='text/css' href="css/bootstrap.min.css" />
    <link rel='stylesheet' type='text/css' href="css/sb-admin-2.css" />
    <link rel='stylesheet' type='text/css' href="css/font-awesome.min.css" />


    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/sb-admin-2.js"></script>
    <script src="js/jquery-2.0.3.min.js" type="text/javascript"></script>
    <script type="text/javascript" src="js/bootstrap.min.js"></script>
    <script type="text/javascript" src="js/analytics.js"></script>
"""
DocDashboard(email, Query_History)

