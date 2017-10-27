#!/usr/bin/env python
# -*- coding: UTF-8 -*-
################################################################################
# Felipe Torres Fabregas 
# Last modified: October 27, 2017
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
# This is the file is used to create all the table preview information.
# The main variables are DB and path. 'DB' will have to be updated with the 
# other databases in order to display their information. The 'Path' variable
# should remain the samin, depending on the apache condiguration of the server
################################################################################
from datetime import datetime, timedelta
from sys import path, exit, stderr
from Cookie import SimpleCookie
from cgi import FieldStorage
from hashlib import sha256, md5
from cgitb import enable
from os import environ

path.insert(0, '../Python_QB/')
# from initial_testing import * # Here we insert all the functions crated for the user and queries
from initial_testing import * # Here we insert all the functions crated for the user and queries

###
DB = 'mimiciii'
Path = '/var/www/Tables/'
###

Query     = "" # We initialize the query variable as empty just in case there is no query.
data      = Database(DB) # Here the database model is initialized 
Tables    = data.GetTables(DB) # We call the function to get all the tables
Schema    = data.SetSchema(DB) # We call the function to set the schema and without the minute limit
TableDesc = [] # This will be the table 100 row preview and description
NewTables = [] # This will be the list of table names in the left side bar

# End of variable definition
for index in range(0, len(Tables)):
    if not Tables[index][0][:12] == "chartevents_": # If the table is not part of the chartevents, get the information.
        info = data.DescTables(Tables[index][0]) # Here the basic table information is searched.
        for item in range(0, len(info)):
            info[item] = list(info[item])
            info[item].insert(0, Tables[index][0])
        TableDesc.append(info)
        NewTables.append(Tables[index][0])

def Send_Email(Subject, Content):
    import smtplib
    server  = smtplib.SMTP("localhost")
    TO      = ["admin@querybuilder-lcp.mit.edu"]
    FROM    = "AWS@querybuilder-lcp.mit.edu"
    # server.set_debuglevel(1)
    server.sendmail(FROM, TO, """Subject: %s\n\n%s""" % (Subject, Content))
    server.quit()
    return True

To_File = {}
for table in TableDesc:
    temp = """"""
    temp += "<div id='{0}' class='tab-pane fade' style='overflow:auto;height:80%;'>".format(table[0][0].upper())
    temp += """<ul class='nav nav-tabs'>
      <li class='active'><a data-toggle='tab' href='#{0}1'>Description</a></li>
      <li><a data-toggle='tab' href='#{1}2'>Preview (100) rows</a></li>
    </ul>""".format(table[0][0].upper(), table[0][0].upper())
    temp += "<div class='tab-content'>"
    temp += "<div id='{0}1' class='result-pane fade in active' style='overflow:auto;height:80%;'>".format(table[0][0].upper())
    temp += """<table class='table table-hover'>
        <thead><tr class='header'><th>ID</th><th>COLUMN_NAME</th><th>DATA_TYPE</th><th>NULLABLE</th></tr></thead>
        <tbody>"""
    for column in table:
        temp += "<tr class='header'><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(column[1], column[2], column[3], column[4])
    temp += """</tbody></table></div>
    <div id='{0}2' class='result-pane fade' style='overflow:auto;height:80%;'>
    <table class='table table-hover'><thead><tr class='header'>""".format(table[0][0].upper())
    Desc1, Title1, Error1 = data.GetInfoFromDB(table[0][0])
    for item1 in Title1:
        temp += "<th>{0}</th>".format(item1)
    temp += "</tr></thead><tbody>"
    for item2 in Desc1:
        temp += "<tr class='header'>"
        for line2 in item2:
            temp += "<td>{0}</td>".format(line2)
        temp += "</tr>"
    temp += "</tbody></table></div></div></div>"
    To_File[table[0][0]] = temp

for item in To_File.keys():
    # if md5(open(Path + DB + '/' + item + '_table_desc.html','r').read()).hexdigest() != md5(To_File[item]).hexdigest():
    print "Writing table preview: " + item
    File = open(Path + DB + '/' + item + '_table_desc.html', 'w')
    File.write(To_File[item])
    File.close()
    if not Send_Email("Table changed in QueryBuilder", "The table {0}, with filename {1}_table_desc.html has been updated.".format(item, item)):
        File2 = open('ERROR.txt','a')
        File2.write("Table changed in QueryBuilder\n", "The table {0}, with filename {1}_table_desc.html has been updated.\n There was a error sending the email".format(item, item))
        File2.close()
