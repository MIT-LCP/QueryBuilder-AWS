#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################
# Felipe Torres Fabregas 
# Last modified: October 27, 2017
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# This is the index page for the website Querybuilder.
# To authenticate, it will send a request to Physionet WITHOUT
# storying any passwords
###############################################################
from datetime import datetime, timedelta
from sys import path, exit, stderr
from Cookie import SimpleCookie
from random import random, seed
from cgi import FieldStorage
from cgitb import enable
from os import environ
from re import match
path.insert(0, '../Python_QB/')
from initial_testing import *
enable(display=0, logdir="/var/www/html/tmp/")

form = FieldStorage()
Error = False

if form.getvalue("email", None) and form.getvalue("Password", None) and form.getvalue("Database", None):
  email    = form.getvalue("email").lower()
  Password = form.getvalue("Password")
  DB       = form.getvalue("Database")
  resp = GetAuth2(email, Password, environ['SERVER_ADDR'])
  if GetAuth2(email, Password, environ['SERVER_ADDR']) == 200 and match(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', email):
    try:
      if not Database(DB).SetSchema(DB):
        print "Content-Type: text/html\n\r" # HTML is following
        print "<script> alert('There was a problem with the login information, please try again.'); window.location.href = 'index.cgi'</script>"
        stderr.write("*** ERROR *** . Invalid Schema: %s\n" % DB)
        exit(0)
    except Exception as e:
      print "Content-Type: text/html\n\r" # HTML is following
      stderr.write("*** ERROR *** . Invalid Schema: %s\n" % e)
      print "<script> alert('There was a problem with the login, please try again.'); window.location.href = 'index.cgi'</script>"
      exit(0)
    SID = str(random()).split(".")[1]
    if SessionModel().AddSession(email, SID):
      c = SimpleCookie()
      exp_date = datetime.utcnow() + timedelta(seconds=10800)
      c.load('DB=%s;       expires=%s; max-age=%s; ;' %(DB,    exp_date, exp_date))
      c.load('Email=%s;    expires=%s; max-age=%s; ;' %(email, exp_date, exp_date))
      c.load('SID=%s;      expires=%s; max-age=%s; ;' %(SID,   exp_date, exp_date))
      print c
      print "Content-Type: text/html\n\r" # HTML is following
      print "<script> window.location.href = 'dashboard.cgi'</script>"
      stderr.write("No ERROR. The user logging in is: %s\n" % email)
    else:
      Error = "Error Creating the model"
      print "Content-Type: text/html\n\r" # HTML is following
  else:
    Error = "Verify the information, if the error continues, raise a issue on the GitHub"
    print "Content-Type: text/html\n\r" # HTML is following
else:
  print "Content-Type: text/html\n\r" # HTML is following

def DocIndex(Error):
    print """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Query Builder</title>
    <link rel="icon" href="media/LCP-logo.png" type="image/x-icon" />

    <!-- Bootstrap Core CSS -->
    <link rel='stylesheet' type='text/css' href="css/bootstrap.min.css" />
    <link rel='stylesheet' type='text/css' href="css/sb-admin-2.css" />
    <link rel='stylesheet' type='text/css' href="css/font-awesome.min.css" />

    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/bootbox.min.js"></script>
    <script type="text/javascript" src="js/bootstrap.min.js"></script>
    <script type="text/javascript" src="js/analytics.js"></script>
    <script type="text/javascript" src="js/sb-admin-2.js"></script>
    </head>
    <body>
      <div id="wrapper">
        <div class="container">
          <div class="row">
            <div class="col-lg-12">
             <h1 class="header" style="text-align:center;">Query Builder v1.1</h1>
            </div>
          </div>
        </div>"""
    if Error:
        print """<script>bootbox.alert("%s", function() {console.log("%s");});</script>"""% (Error,Error)
    print """<div class="panel panel-default">
          <div class="panel-body">
            <div class="row">
              <div class="col-sm-3"></div>
              <div class="col-sm-6">
              <p style="font-size:130%;">Query Builder is a simple Postgres SQL client that allows you to do introductory searches 
              to our public databases.</p>
              <p style="font-size:130%;">This interface also provides the 
              ability for users to export the results of their queries for processing in their own statistical tools. </p><br>
                <form action='index.cgi' method='post' class="form-horizontal">
                  <div class="form-group">
                    <label for="email" class="col-sm-2 control-label">Email</label>
                    <div class="col-sm-10">
                      <input type="email" class="form-control" id="email" name="email" placeholder="Email">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="Password" class="col-sm-2 control-label">Password</label>
                    <div class="col-sm-10">
                      <input type="password" class="form-control" id="Password" name="Password" placeholder="Password">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="Database" class="col-sm-2 control-label">Database</label>
                    <div class="col-sm-10">
                      <select class="form-control" name="Database" id="Database">
                        <option value="mimiciii" selected="selected">MIMIC-III V1.4</option>
                      </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <div class="col-sm-offset-2 col-sm-10">
                      <button type="submit" class="btn btn-default">Sign in</button>
                    </div>
                  </div>
                </form>
              </div>
              <div class="col-sm-3"></div>
            </div>
            <hr>
            <div class="container" style="background-color:white;">
              <div class="row">
                <div class="col-sm-2"></div>
                <div class="col-sm-8">
                  <h1 id="Query-Builder-Issue-Tracker" style="text-align:center;">Issue Tracker</h1>
                  <p >If you are experiencing issues when using Query Builder or if you have a suggestion for improvement, please raise an issue on our issue tracker.</p>
                  <p >To raise an issue, first navigate to the Query Builder Repository on GitHub or click <a href='https://github.com/MIT-LCP/querybuilder-issue'>here</a>. After logging in to GitHub, click “New issue”, add a title and description of the problem, and then select the “Submit new issue” button.</p>
                </div>
                <div class="col-sm-2"></div>
              </div><hr>
              <div class="row">
                <div class="col-sm-8">
                  <h1 id="mimic-iii-critical-care-database" style="text-align:center;">MIMIC-III Critical Care Database</h1>
                  <p style="font-size:120%;">MIMIC-III (<strong>M</strong>edical <strong>I</strong>nformation <strong>M</strong>art for <strong>I</strong>ntensive <strong>C</strong>are III) is a large, freely-available database comprising deidentified health-related data associated with over forty thousand patients who stayed in critical care units of the Beth Israel Deaconess Medical Center between 2001 and 2012.</p>
                  <p style="font-size:120%;">The database includes information such as demographics, vital sign measurements made at the bedside (~1 data point per hour), laboratory test results, procedures, medications, caregiver notes, imaging reports, and mortality (both in and out of hospital).</p>
                  <p style="font-size:120%;">MIMIC supports a diverse range of analytic studies spanning epidemiology, clinical decision-rule improvement, and electronic tool development. It is notable for three factors:</p>
                  <ul>
                  <li style="font-size:100%;">it is freely available to researchers worldwide</li>
                  <li style="font-size:100%;">it encompasses a diverse and very large population of ICU patients</li>
                  <li style="font-size:100%;">it contains high temporal resolution data including lab results, electronic documentation, and bedside monitor trends and waveforms.</li>
                  </ul>
                </div>
                <div class="col-xs-4 col-sm-4 col-md-2 col-lg-2">
                  <img src="/media/mimic-III.png" alt="Mimic Flow Chart" class='image-full' style="height:250px;width:auto;margin-top: 2cm;"/>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </body>
    </html>
"""

DocIndex(Error)

