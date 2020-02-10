#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from Postgres import Database

SCHEMA = 'mimiciii'
DB_CONN = Database()
TABLES = DB_CONN.get_tables(SCHEMA)
DB_CONN.set_schema(SCHEMA)


# table_description = get_table_description()
# table_dict = format_tables_to_html(table_description)
# print(table_dict['admissions'])
# write_to_file(table_dict)


def get_table_description():
    """
    Get all the names of the tables and exclude the partitioned chartevents
    Once the names of the tables are defined, get a description of the table

    Returns an array of arrays with the table properties
    E.g.
    ['admissions', 1, 'row_id', 'integer', 'YES'],
    ['admissions', 2, 'subject_id', 'integer', 'YES'],
    ...
    """
    table_description = []
    for index, line in enumerate(TABLES):
        info = ''
        if not line[0].startswith("chartevents_"):
            info = DB_CONN.describe_tables(line[0])
        for indx, item in enumerate(info):
            info[indx] = list(item)
            info[indx].insert(0, line[0])
        if info != '':
            table_description.append(info)
    return table_description


def format_tables_to_html(description):
    """
    Format the table description into a tab and adds a 100 lines preview into
    another tab.

    This is added to a dictionary which the index is the name of the table.
    The deictionary is returned to be saved into a file.
    """
    table_to_save = {}
    for table in description:
        temp = ""
        temp += "<div id='{0}' class='tab-pane' style='overflow:auto;height:90vh;'>".format(table[0][0].upper())
        temp += """<ul class='nav nav-tabs'>
    <li class='nav-item active'><a class="nav-link active" data-toggle='tab' href='#{0}1'>Description</a></li>
    <li class='nav-item'><a class='nav-link' data-toggle='tab' href='#{1}2'>Preview (100) rows</a></li>
</ul>""".format(table[0][0].upper(), table[0][0].upper())
        temp += "<div class='tab-content'>"
        temp += "<div id='{0}1' class='tab-pane active' style='overflow:auto;height:85vh;'>".format(table[0][0].upper())
        temp += """<table class='table table-striped table-hover'><thead><tr>
    <th>ID</th><th>COLUMN_NAME</th><th>DATA_TYPE</th><th>NULLABLE</th>
</tr></thead><tbody>"""
        for column in table:
            temp += """<tr>
    <td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>
</tr>""".format(column[1], column[2], column[3], column[4])
        temp += """</tbody></table></div>
<div id='{0}2' class='tab-pane' style='overflow:auto;height:85vh;'>
    <table class='table table-striped table-hover'><thead>\n<tr>""".format(
            table[0][0].upper())
        desc, title, error = DB_CONN.get_table_preview(table[0][0])
        for item1 in title:
            temp += "<th>{0}</th>".format(item1)
        temp += "</tr>\n</thead><tbody>"
        for item2 in desc:
            temp += "\n<tr>"
            for line2 in item2:
                temp += "<td>{0}</td>".format(line2)
            temp += "</tr>\n"
        temp += "</tbody></table></div></div></div>"
        table_to_save[table[0][0]] = temp
    return table_to_save


def write_to_file(tables):
    """
    Write the description and preview of a table to a sample file.
    """
    for item in tables.keys():
        file = open('templates/tables/{}_table_desc.html'.format(item), 'w')
        file.write(tables[item])
        file.close()
