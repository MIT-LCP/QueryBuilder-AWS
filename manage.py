#!/var/www/vhosts/querybuilder-lcp.mit.edu/python_env/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, session, request, jsonify, Response, current_app
from datetime import datetime, timedelta
import urllib.request
from re import search
from Postgres import *

app = Flask(__name__)
app.debug = True

# FOLDER = '/var/www/vhosts/querybuilder-lcp.mit.edu/Flask'


def Auth(User, Pass):
    """
    This authentication works for the current 2008-2019 physionet authentication
    version. It will NOT work for the NEW version of physionet that is being developed.
    """
    url='https://physionet.org/works/MIMICIIIClinicalDatabase/files/'
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='PhysioNetWorks', uri=url, user=User, passwd=Pass)
    opener = urllib.request.build_opener(auth_handler)
    try:
        return opener.open(url).getcode()
    except:
        return 400

@app.route("/",           methods=['POST','GET'])
@app.route("/index.html", methods=['POST','GET'])
@app.route("/index.cgi",  methods=['POST','GET'])
@app.route("/index",      methods=['POST','GET'])
@app.route("/login.html", methods=['POST','GET'])
@app.route("/login.cgi",  methods=['POST','GET'])
@app.route("/login",      methods=['POST','GET'])
def login():
    if request.method == 'POST':
        Email = request.form.get('Email', None)
        app.logger.info('{0}: {1} is trying to log into querybuilder.'.format(datetime.now(), Email))
        if Email != None and request.form.get('Password', None) != None:
            Code = Auth(Email, request.form.get('Password', None))
            if Code == 200 or Code == '200':
                app.logger.info('{0}: Generating session for - {1}.'.format(datetime.now(), Email))
                session["Email"] = Email
                session["Database"] = request.form.get('Database', 'mimiciii')  
                session["Date"] = datetime.now()
                session['URL'] = "https://querybuilder-lcp.mit.edu"
                app.logger.info(session)
                return redirect('dashboard')
            else:
                app.logger.error('Incorrect password or username: {0} Error: {1}'.format(Email, Code))
                return render_template('login.html', Error='Wrong username and password, please try again.')
        else:
            app.logger.info('{0}: There was an error in the login for the following account: {1}'.format(datetime.now(), Email))
            return render_template('login.html', Error='There was an error, please try again, or contact the administraror')
    else:
        return render_template('login.html')


@app.route("/dashboard.cgi")#, methods=['POST','GET'])
@app.route("/dashboard")#,     methods=['POST','GET'])
def dashboard():
    if 'Email' not in session and 'URL' not in session:
        return redirect('login')
    Email = session['Email']

    Tablenames = ['ADMISSIONS', 'CALLOUT', 'CAREGIVERS', 'CHARTEVENTS', 'CPTEVENTS', 'D_CPT', 'D_ICD_DIAGNOSES', 
    'D_ICD_PROCEDURES', 'D_ITEMS', 'D_LABITEMS', 'DATETIMEEVENTS', 'DIAGNOSES_ICD', 'DRGCODES', 'ICUSTAYS', 
    'INPUTEVENTS_CV', 'INPUTEVENTS_MV', 'LABEVENTS', 'MICROBIOLOGYEVENTS', 'NOTEEVENTS', 'OUTPUTEVENTS', 'PATIENTS', 
    'PRESCRIPTIONS', 'PROCEDUREEVENTS_MV', 'PROCEDURES_ICD', 'SERVICES', 'TRANSFERS']
    Files = ['admissions_table_desc.html', 'callout_table_desc.html', 'caregivers_table_desc.html', 'chartevents_table_desc.html', 
    'cptevents_table_desc.html', 'd_cpt_table_desc.html', 'd_icd_diagnoses_table_desc.html', 'd_icd_procedures_table_desc.html', 
    'd_items_table_desc.html', 'd_labitems_table_desc.html', 'datetimeevents_table_desc.html', 'diagnoses_icd_table_desc.html', 
    'drgcodes_table_desc.html', 'icustays_table_desc.html', 'inputevents_cv_table_desc.html', 'inputevents_mv_table_desc.html', 
    'labevents_table_desc.html', 'microbiologyevents_table_desc.html', 'noteevents_table_desc.html', 'outputevents_table_desc.html', 
    'patients_table_desc.html', 'prescriptions_table_desc.html', 'procedureevents_mv_table_desc.html', 'procedures_icd_table_desc.html',
    'services_table_desc.html', 'transfers_table_desc.html']

    # if request.method == 'POST':
    #     pass
    # else:
    #     return render_template('dashboard.html', Tables = Tablenames, User = Email, Files = Files)
    app.logger.info('{0}: User - {1} is in the dashboard.'.format(datetime.now(), Email))
    return render_template('dashboard.html', Tables = Tablenames, User = Email, Files = Files)

@app.route("/get_file", methods=['POST','GET'])
def get_file():
    if 'Email' not in session and 'URL' not in session:
        return redirect('login')
    import os
    app.logger.info(os.getcwd())
    Filename = request.form.get('Filename', None)
    content = current_app.open_resource('templates/tables/'+Filename).read()
    #content = open('templates/tables/'+Filename).read()
    return content

@app.route("/User")
def User():
    if 'Email' not in session and 'URL' not in session:
        return redirect('login')

    Email = session['Email']
    Query = []
    Query_History = UserModel().GetQueriesByEmail(Email)
    for item in Query_History:
        Query.append(item[0])

    app.logger.info('{0}: User - {1} is in the user history page.'.format(datetime.now(), Email))

    return render_template('user.html', Query_History=Query, User = Email)

@app.route("/random_query", methods=['POST','GET'])
def random_query():
    if 'Email' not in session and 'URL' not in session:
        return redirect('login')

    Query = request.form.get('Query', None)

    app.logger.info('{0}: User - {1} ran this query:\n {2}\n'.format(datetime.now(), session['Email'], Query))

    Data = Database()
    Data.SetSchema('mimiciii')
    result, title, Error = Data.RandomQ(Query)

    if Error:
        app.logger.error('{0}: There was an error in the query:\n{1}\n'.format(datetime.now(), Error))
        QError = """<div class="card text-dark" style="color: #a94442; background-color: #f2dede; border-color: #ebccd1;">
            <div class="card-body">
                <strong>An error was encountered from the query</strong><br>
                  <strong><p>Your query was:</p></strong><p>{0}</p>
                  <strong><p>The error is:</p></strong>""".format(Query.rstrip())
        for line in str(Error).split("\n"):
            QError += "<p>{0}</p>".format(line)
        QError += """    </div>
          </div>"""

        return jsonify(result=[QError])    

    NumberOfRows = 50
    content = ""
    counter = 0

    head = "<thead><tr>"
    foot = "<tfoot><tr>"
    for item in title:
        head += "<th>{0}</th>".format(item)
        foot += "<th>{0}</th>".format(item)
    head += "</tr></thead>"
    foot += "</tr></tfoot>"
    body = "<tbody>"
    for idx, item in enumerate(result):
        body += "<tr>"
        for row in item:
            body += "<td>{0}</td>".format(row)
        body += "</tr>"
        if ((idx + 1) % NumberOfRows == 0) or (idx + 1 == len(result)):
            counter+=1
            body += "</tbody>"
            if counter == 1:
                content += "<div id='{0}' class='result-pane active' style='overflow:auto;height:50vh;display:block;'><table id='QResult' class='table table-striped'>{1}{2}{3}</table></div>".format(counter, head, foot, body)
            else:
                content +=  "<div id='{0}' class='result-pane' style='overflow:auto;height:50vh;display:none;'><table id='QResult' class='table table-striped'>{1}{2}{3}</table></div>".format(counter, head, foot, body)
            body = "<tbody>"
    if len(result) == 0:
        counter+=1
        content += "<div id='{0}' class='result-pane active' style='overflow:auto;height:50%;display:block;'><table id='QResult' class='table table-striped'>{1}<tbody></tbody></table></div>".format(counter, head)

    Write = ""
    if len(result) == 1:
      Write = "Showing only 1 result."
    elif len(result) == 500:
      Write = "Showing only 500 results. The rest were omitted"
    elif len(result) == 0:
      Write = "Showing 0 results."
    else:
      Write = "Showing only {0} results.".format(len(result))

    content2 = """<ul id='pagination' style="display: flex; justify-content: center; padding-top:2em;"></ul>
        <script type='text/javascript'> 
        $('#pagination').twbsPagination({
          totalPages: """ + str(counter) + """, visiblePages: 5, onPageClick: function (event, page) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName('result-pane');
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = 'none';
                }
            tablinks = document.getElementsByClassName('result-pane');
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(' active', '');
                tablinks[i].style.display = 'none';
                }
            document.getElementById(page).className += ' active';
            document.getElementById(page).style.display = 'block';
            } 
        });
        </script>"""

    return jsonify(result=[content, content2, Write])    

@app.route("/download_random_query", methods=['POST','GET'])
def download_random_query():
    Query = request.form.get('Query', None)
    Data = Database()
    Data.SetSchema('mimiciii')
    result, Error = Data.RandomQDown(Query.rstrip())
    app.logger.info('{0}: User - {1} ran this query to download:\n {2}\n'.format(datetime.now(), session['Email'], Query))
    if Error:
        app.logger.error('{0}: There was an error in the query:\n{1}\n'.format(datetime.now(), Error))
        return Error
    return result

@app.route("/logout")
@app.route("/logout.cgi")
def logout():
    session.clear()
    return redirect('login')

app.secret_key = 'mf}7WwDxTmpULrYgSWzfxutj|zDo1n(h+abvEa&$aM)?O$8R>qUtE)?CyOQ)*6YwADN!IHLy+TE^K1>>8^riVxe**JBH!+N'

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.run(host='0.0.0.0', port=8083, threaded=True, debug=True)


