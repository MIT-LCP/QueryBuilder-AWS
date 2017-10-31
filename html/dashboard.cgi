#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################
# Felipe Torres Fabregas 
# Last modified: October 27, 2017
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# This is the dashboard page for the website Querybuilder.
# Once a query has ben done the page will reload itself to show
# the query's result.
###############################################################
from datetime import datetime, timedelta
from sys import path, exit, stderr
from Cookie import SimpleCookie
from cgi import FieldStorage
from cgitb import enable
from os import environ

# This cgi build in function is to store the erros made by the page in the specified file
enable(display=0, logdir="/var/www/html/tmp/")
path.insert(0, '../Python_QB/')
from initial_testing import * # Here we insert all the functions crated for the user and queries

#Here we check ig there is a cookie for the session created for the user
if environ.has_key('HTTP_COOKIE'):
  c = SimpleCookie()
  c.load(environ['HTTP_COOKIE'])
  if "SID" and "Email" and "DB" in c:
    c['DB']['expires'] = c['Email']['expires'] = c['SID']['expires'] = datetime.utcnow() + timedelta(seconds=10800)
    print c
  else:
    print "Content-Type: text/html\n\r"
    print "<script>alert('There is a problem with your login information. Please login.'); window.location.href = 'index.cgi'; </script>"
    exit(0)
  print "Content-Type: text/html\n\r"
  try:
    if not (SessionModel().GetSession(int(c['SID'].value))):
      print "<script>alert('There was an error with the session'); window.location.href = 'index.cgi'; </script>"
      exit(0)
  except:
    print "<script>alert('There is a problem with your login information.'); window.location.href = 'index.cgi'; </script>"
    exit(0)
else:
  print "Content-Type: text/html\n\r"
  print "<script>alert('Please login.'); window.location.href = 'index.cgi';</script>"
  exit(0)

# Here we define the variables
form      = FieldStorage() #If there is a form, store all the variables in form
Query     = form.getvalue("Query", None) # We initialize the query variable as empty just in case there is no query.
data      = Database(c['DB'].value) # Here the database model is initialized 
Tables    = data.GetTables(c['DB'].value) # We call the function to get all the tables
Schema    = data.SetSchema(c['DB'].value) # We call the function to set the schema and without the minute limit
email     = c['Email'].value # Here we get the email from the cookie
NewTables = [] # This will be the list of table names in the left side bar
# End of variable definition
Path = '/var/www/Tables/' + c['DB'].value + '/'

# Here we get the table information, description and preview
for indx, item in enumerate(Tables):
  if not item[0][:12] == "chartevents_": 
    NewTables.append(item[0])

if form.getvalue("Query"):
  UserModel().InsertQRow(email, Query)

def DocDashboard(Schema, NewTables, email, Query, Path):
    NumberOfRows = 100
    print """<html lang="en"><head>""", Header, JS, """</head><body><div id="wrapper">
    <nav class="navbar navbar-default" style="margin-bottom: 0">
    <div class="navbar navbar-fixed-top navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse"></button>
    """
    #Set the header to MIMIC III if the schema is Mimic3 on TOP NAV BAR
    if Schema == "mimiciii":
      print """<a class="navbar-brand" href="dashboard.cgi">MIMIC-III Query Builder</a>"""

    #Dropdown for the user menu, here are the links for the user, logout and dashboard
    print """<ul class="nav navbar-top-links navbar-right">
      <li class="dropdown">
        <a class="dropdown-toggle" data-toggle="dropdown" style="font-size:18px;" href="">%s
          <i class="fa fa-user fa-fw"></i>  <i class="fa fa-caret-down"></i>
        </a>
        <ul class="dropdown-menu dropdown-user">
          <li><a id="home" href="dashboard.cgi"><i class="fa fa-cog fa-fw"></i> Query Builder</a></li>
          <li><a id="create-user"  href="User.cgi"><i class="fa fa-user fa-fw"></i> User Profile</a></li>
          <li class="divider"></li>
          <li><a href="/logout.cgi"><i class="fa fa-sign-out fa-fw"></i> Logout</a></li>
        </ul></li></ul></div>
  <div class="navbar-s navbar-default sidebar" role="navigation">
    <div class="sidebar-nav navbar-collapse">""" % email
    #Set the header to MIMIC III if the schema is Mimic3 on SIDE BAR
    if Schema == "mimiciii":
      print """<a href="#" class="list-group-item list-group-item-success" ID="table">MIMIC-III</a>"""
    else:
      print """<a href="#" class="list-group-item list-group-item-success" ID="table">""" + Schema + "</a>"
    TabManager = ""
    for table in range(len(NewTables)):
        TabManager += """<li id="%s" style="display: none;"><a data-toggle="tab" href="#%s" aria-expanded="false">%s  <i class="fa fa-lg fa-times-circle-o" onclick="Remove_Tab('%s', event);" aria-hidden="true"></i></a></li>""" % (NewTables[table].lower(), NewTables[table].upper(), NewTables[table].upper(),NewTables[table].lower())
        print """<a href="#" class="list-group-item tablinks" ID='Table"""+ str(table)+"""' onclick="addTab(event, '""" + NewTables[table].upper() + """')">""" + NewTables[table].upper() + """</a>"""
    print "</div></div></nav>"
    #END OF SIDEBAR AND NAVBAR
    print  """<div id="page-wrapper">
     <div class="container-fluid box">
      <div class="row">
        <ul class="nav nav-tabs" id="TabManager">
          <li id="Query_tab1"><a data-toggle="tab" href="#QUERY_TAB">Query</a></li>
          %s
        </ul>
        <div class="tab-content" id="TAB_Content">""" % TabManager

##Here we START the description of the table ##
    for table in NewTables: 
      File = open(Path+table+'_table_desc.html','r')
      print File.read()
      File.close()##Here we END the description of the table ##

    #END of print for the tables
    print """  <!-- ############################################ QUERY TAB ######################################## -->
          <div id="QUERY_TAB" class="tab-pane fade in active">
            <div class="row">
              <div class="col-lg-12">"""
    POST = """<form action="dashboard.cgi" method="POST">
               <textarea class="form-control" id="Query" name="Query" rows="10" placeholder="Query"></textarea><br>
               <button type="submit" class="btn btn-success">Execute Query</button>
               <span id="whoing"></span>
                <a id="Export" class="btn btn-success pull-right"  download="Result.csv">Export Results</a>
               </form>
               <div id='result-content'>"""
    if Query:
      POST = """<form action="dashboard.cgi" method="POST">
               <textarea class="form-control" id="Query" name="Query" rows="10" placeholder="Query">%s</textarea><br>
               <button type="submit" class="btn btn-success">Execute Query</button>
               <span id="whoing"></span>
                <a id="Export" class="btn btn-success pull-right"  download="Result.csv">Export Results</a>
               </form>
               <div id='result-content'>""" % Query
    
      try:
        Data = Database(c['DB'].value)
        Data.SetSchema(c['DB'].value)
        result, title, Error = Data.RandomQ(Query)
        stderr.write("No ERROR on query execution: %s\n" % Query)
      except Exception as e:
        stderr.write("*** ERROR *** on query execution: %s \n %s" % (e, Query))
        result = Error = title = Query = ''
    else: 
      result = Error = Query = title = ''
    print POST
    counter = 0
    if (Error == '' or Error == False) and title != '':
      head = "<thead><tr>"
      foot = "<tfoot><tr>"
      for item in title:
        head += "<th>" + item + "</th>"
        foot += "<th>" + item + "</th>"
      head += "</tr></thead>"
      foot += "</tr></tfoot>"
      body = "<tbody>"
      for idx, item in enumerate(result):
        body += "<tr>"
        for row in item:
          body += "<td>" + str(row) + "</td>"
        body += "</tr>"
        if ((idx + 1) % NumberOfRows == 0) or (idx + 1 == len(result)):
          counter+=1
          body += "</tbody>"
          if counter == 1:
            print """<div id='""" + str(counter) + """' class="result-pane fade in active" style="overflow:auto;height:50%;display:block;"><table id="QResult" class="table table-striped" >"""
            print head, foot, body, "</table></div>"
          else:
            print """<div id='""" + str(counter) + """' class="result-pane fade" style="overflow:auto;height:50%;display:none;"><table id="QResult" class="table table-striped" >"""
            print head, foot, body, "</table></div>"
          body = "<tbody>"
      if len(result) == 0:
        counter+=1
        print """<div id='""" + str(counter) + """' class="result-pane fade in active" style="overflow:auto;height:50%;display:block;"><table id="QResult" class="table table-striped" >"""
        print head, "<tbody></tbody></table></div>"
      Write = ''
      print """<center><ul id="pagination"></ul></center>"""
      if len(result) == 1:
        Write = "Showing only 1 result."
      elif len(result) == 5000:
        Write = "Showing only 5000 results. The rest were omitted"
      elif len(result) == 0:
        Write = "Showing 0 results."
      else:
        Write = "Showing only " + str(len(result)) + " results."
      print """ </div>
<script type="text/javascript"> $('#pagination').twbsPagination({
  totalPages: %i, visiblePages: 7, onPageClick: function (event, page) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("result-pane");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";}
    tablinks = document.getElementsByClassName("result-pane");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" in active", "");
        tablinks[i].style.display = "none";}
    document.getElementById(page).className += " in active";
    document.getElementById(page).style.display = "block";
    $("#whoing").text('%s');}});
</script>""" % (counter, Write)
    elif title == '' and (Error == False or Error == ''):
      pass
    elif (str(Error) == "False" or str(Error) == '' or str(Error) == False) and len(result) == 0:
            print """<div class="alert alert-danger" style="max-height:500px;overflow-y: auto;">
          <strong>Didn't found any results</strong><br>
          <p>Your query was:</p><p>%s</p><br>
        </div>""" % (Query.replace("\n", "</p><p>"))
    else:
      print """<div class="alert alert-danger" style="max-height:500px;overflow-y: auto;">
          <strong>An error was encountered from the query</strong><br>
          <p>Your query was:</p><p>%s</p><br>
          <p>The error was:</p> 
          <strong><ul> %s </ul></strong>
        </div>""" % (Query.replace("\n", "</p><p>"), str(Error))
    print """</div></div></div></div></div></div></div></div></div></body></html>"""

#################################################################################
# From here on its just the Header and JS, Also we will call the Main function  #
# that its defined above.                                                       #
#################################################################################
Header = """
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Query Builder</title>
    <link rel="shortcut icon" href="media/favicon.ico">
    <link rel='stylesheet' type='text/css' href="css/metisMenu.min.css">
    <link rel='stylesheet' type='text/css' href="css/bootstrap.min.css">
    <link rel='stylesheet' type='text/css' href="css/sb-admin-2.css">
    <link rel='stylesheet' type='text/css' href="css/font-awesome.min.css">

    <script type="text/javascript" src="js/FileSaver.js"></script>
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/sb-admin-2.js"></script>
    <script type="text/javascript" src="js/jquery-2.0.3.min.js"></script>
    <script type="text/javascript" src="js/bootstrap.min.js"></script>
    <script type="text/javascript" src="js/bootbox.js"></script>
    <script type="text/javascript" src="js/jquery.twbsPagination.js"></script>
    <script type="text/javascript" src="js/custom.js"></script>
    <script type="text/javascript" src="js/analytics.js"></script>

"""
JS = """<script type="text/javascript">
$(document).ready(function(){
  $("#Export").click(function(){
   x = document.getElementById("Query").value;
   $.ajax({
      url : "RandomQueryDownload.cgi",
      type : "POST", 
      data : {Query : x, DB : "%s"}, 
      success : function(File) {
        var NewFile = new Blob([File], {type: "text/csv;charset='utf-8'"});
        saveAs(NewFile, "Result.csv");
      }
    });
  });
});
</script>""" % (c['DB'].value)

DocDashboard(Schema, NewTables, email, Query, Path)
