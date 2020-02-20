#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from functools import wraps
from os import getcwd
from re import search

from requests.auth import HTTPBasicAuth
from requests import get, codes
from flask import (Flask, render_template, redirect, session, request, jsonify,
                   current_app, url_for)

from Postgres import UserModel, Database

app = Flask(__name__)
app.debug = True
app.secret_key = 'mf}7WwDxTmpULrYgSWzfxutj|zDo1n(h+abvEa&$aM)?O$8R>qUtE)?CyOQ)*6YwADN!IHLy+TE^K1>>8^riVxe**JBH!+N'


def login_required(function):
    """
    Wrapper function to force login
    """
    @wraps(function)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        if ('Email' not in session) or ('URL' not in session):
            return redirect(url_for('login'))
        return function(*args, **kwargs)
    return wrap


def auth(email, passwd):
    """
    Authentication function against mimiciii
    """
    url = 'https://physionet.org/files/mimiciii/1.4/'
    headers = {'User-Agent': 'Wget/1.18', 'Application': 'QueryBuilder'}
    response = get(url, auth=HTTPBasicAuth(email, passwd), headers=headers)

    if response.status_code == codes.ok:
        app.logger.info("User {} loggin complete".format(email))
    elif response.status_code == codes.forbidden:
        app.logger.info("User {} does not have access to MIMIC".format(email))
    elif response.status_code == codes.unauthorized:
        app.logger.info("Invalid credentials for {}".format(email))
    else:
        app.logger.info("Error logging in user {0}\nReason {0}\n {1}".format(
            email, response.reason, response.status_code))
        response.raise_for_status()
    return response.status_code


@app.route("/", methods=['POST', 'GET'])
@app.route("/index.html", methods=['POST', 'GET'])
@app.route("/index.cgi", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
@app.route("/login.html", methods=['POST', 'GET'])
@app.route("/login.cgi", methods=['POST', 'GET'])
@app.route("/login", methods=['POST', 'GET'])
def login():
    """
    Login view
    """
    if request.method == 'POST':
        email = request.form.get('Email', None).lower()
        passwd = request.form.get('Password', None)
        now = datetime.now()
        if email and passwd and valid_email(email):
            app.logger.info('{} is trying to log into querybuilder.'.format(
                email))
            code = auth(email, passwd)
            if code in ['200', 200]:
                app.logger.info('Generating session for - {}.'.format(email))
                session["Email"] = email
                session["Date"] = now
                session['URL'] = "https://querybuilder-lcp.mit.edu"
                return redirect('dashboard')
            app.logger.info('{1}: Incorrect password or username: {0}'.format(
                email, code))
            return render_template('login.html', Error='Incorrect username or password, please try again.')
        elif not valid_email(email):
            app.logger.info('Invalid email {}'.format(email))
            return render_template('login.html', Error='Invalid email')
    return render_template('login.html')


@app.route("/dashboard.cgi")
@app.route("/dashboard")
@login_required
def dashboard():
    """
    Querybuilder dashboard
    """
    email = session['Email']

    table_names = ['ADMISSIONS', 'CALLOUT', 'CAREGIVERS', 'CHARTEVENTS',
                   'CPTEVENTS', 'D_CPT', 'D_ICD_DIAGNOSES', 'D_ICD_PROCEDURES',
                   'D_ITEMS', 'D_LABITEMS', 'DATETIMEEVENTS', 'DIAGNOSES_ICD',
                   'DRGCODES', 'ICUSTAYS', 'INPUTEVENTS_CV', 'INPUTEVENTS_MV',
                   'LABEVENTS', 'MICROBIOLOGYEVENTS', 'NOTEEVENTS',
                   'OUTPUTEVENTS', 'PATIENTS', 'PRESCRIPTIONS',
                   'PROCEDUREEVENTS_MV', 'PROCEDURES_ICD', 'SERVICES',
                   'TRANSFERS']
    files = ['admissions_table_desc.html', 'callout_table_desc.html',
             'caregivers_table_desc.html', 'chartevents_table_desc.html',
             'cptevents_table_desc.html', 'd_cpt_table_desc.html',
             'd_icd_diagnoses_table_desc.html',
             'd_icd_procedures_table_desc.html', 'd_items_table_desc.html',
             'd_labitems_table_desc.html', 'datetimeevents_table_desc.html',
             'diagnoses_icd_table_desc.html', 'drgcodes_table_desc.html',
             'icustays_table_desc.html', 'inputevents_cv_table_desc.html',
             'inputevents_mv_table_desc.html', 'labevents_table_desc.html',
             'microbiologyevents_table_desc.html',
             'noteevents_table_desc.html', 'outputevents_table_desc.html',
             'patients_table_desc.html', 'prescriptions_table_desc.html',
             'procedureevents_mv_table_desc.html',
             'procedures_icd_table_desc.html', 'services_table_desc.html',
             'transfers_table_desc.html']

    app.logger.info('User - {} is in the dashboard.'.format(email))
    return render_template('dashboard.html', Tables=table_names, User=email,
                           Files=files)


@app.route("/get_file", methods=['POST', 'GET'])
@login_required
def get_file():
    """
    Render table description file
    """
    if 'Email' not in session and 'URL' not in session:
        return redirect('login')

    app.logger.info(getcwd())
    filename = request.form.get('Filename', None)
    return current_app.open_resource('templates/tables/'+filename).read()


@app.route("/User")
@login_required
def user():
    """
    User query history page
    """
    email = session['Email']
    query = []
    query_history = UserModel().get_queries_from_email(email)
    for item in query_history:
        query.append(item[0])
    return render_template('user.html', Query_History=query, User=email)


@app.route("/random_query", methods=['POST', 'GET'])
@login_required
def random_query():
    """
    Run a random query
    """
    query = request.form.get('Query', None)
    app.logger.info('User: {0} ran this query:\n{1}\n'.format(
        session['Email'], query))

    data = Database()
    data.set_schema('mimiciii')
    UserModel().record_query(session['Email'], query)
    result, title, error = data.random_query(query)
    if error:
        app.logger.info('There was an error in the query:\n{}\n'.format(
            error))
        query_error = """<div class="card text-dark" style="color: #a94442; background-color: #f2dede; border-color: #ebccd1;">
            <div class="card-body">
                <strong>An error was encountered from the query</strong><br>
                  <strong><p>Your query was:</p></strong><p>{}</p>
                  <strong><p>The error is:</p></strong>""".format(
                      query.rstrip())
        for line in str(error).split("\n"):
            query_error += "<p>{}</p>".format(line)
        query_error += """    </div>
          </div>"""
        return jsonify(result=[query_error])

    max_rows = 50
    content = ""
    counter = 0
    head = "<thead><tr>"
    foot = "<tfoot><tr>"
    for item in title:
        head += "<th>{}</th>".format(item)
        foot += "<th>{}</th>".format(item)
    head += "</tr></thead>"
    foot += "</tr></tfoot>"
    body = "<tbody>"
    for idx, item in enumerate(result):
        body += "<tr>"
        for row in item:
            body += "<td>{}</td>".format(row)
        body += "</tr>"
        if ((idx + 1) % max_rows == 0) or (idx + 1 == len(result)):
            counter+=1
            body += "</tbody>"
            if counter == 1:
                content += "<div id='{0}' class='result-pane active' style='overflow:auto;height:50vh;display:block;'>\
                <table id='QResult' class='table table-striped'>{1}{2}{3}</table></div>".format(counter, head, foot, body)
            else:
                content += "<div id='{0}' class='result-pane' style='overflow:auto;height:50vh;display:none;'>\
                <table id='QResult' class='table table-striped'>{1}{2}{3}</table></div>".format(counter, head, foot, body)
            body = "<tbody>"
    if len(result) == 0:
        counter += 1
        content += "<div id='{0}' class='result-pane active' style='overflow:auto;height:50%;display:block;'>\
        <table id='QResult' class='table table-striped'>{1}<tbody></tbody></table></div>".format(counter, head)

    write = ""
    if len(result) == 1:
        write = "Showing only 1 result."
    elif len(result) == 500:
        write = "Showing only 500 results. The rest were omitted"
    elif len(result) == 0:
        write = "Showing 0 results."
    else:
        write = "Showing only {} results.".format(len(result))

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
    return jsonify(result=[content, content2, write])


@app.route("/download_random_query", methods=['POST', 'GET'])
@login_required
def download_random_query():
    """
    Download a random query
    """
    query = request.form.get('Query', None)
    db_connection = Database()
    db_connection.set_schema('mimiciii')
    result, error = db_connection.random_query_download(query.rstrip())
    app.logger.info('User - {0} ran this query to download:\n{1}\n'.format(
        session['Email'], query))
    if error:
        app.logger.info('There was an error in the query:\n{}\n'.format(
            error))
        return error
    return result


@app.route("/logout")
@app.route("/logout.cgi")
def logout():
    """
    Logout function
    """
    session.clear()
    return redirect('login')


def valid_email(email):
    """
    Validates emails
    """
    regex = r'\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if not search(regex, email):
        app.logger.info("Invalid email: {}".format(email))
        return False
    return True


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.run(host='0.0.0.0', port=8084, threaded=True, debug=True)
