# from hashlib import sha256
from Postgres import * # Here we insert all the functions crated for the user and queries
DB = 'mimiciii'

data      = Database() # Here the database model is initialized 
Tables    = data.GetTables(DB)# We call the function to get all the tables
TableDesc = [] # This will be the table 100 row preview and description
Schema    = data.SetSchema(DB) # We call the function to set the schema and without the minute limit

# End of variable definition
for index in range(0, len(Tables)):
    info = ''
    if not Tables[index][0].startswith("chartevents_"): # If the table is not part of the chartevents, get the information.
        info = data.DescTables(Tables[index][0]) # Here the basic table information is searched.
    for item in range(0, len(info)):
        info[item] = list(info[item])
        info[item].insert(0, Tables[index][0])
    if info != '':
        TableDesc.append(info)

To_File = {}
for table in TableDesc:
    temp = ""
    temp += "<div id='{0}' class='tab-pane' style='overflow:auto;height:90vh;'>".format(table[0][0].upper())
    temp += """<ul class='nav nav-tabs'>
      <li class='nav-item active'><a class="nav-link active" data-toggle='tab' href='#{0}1'>Description</a></li>
      <li class='nav-item'><a class='nav-link' data-toggle='tab' href='#{1}2'>Preview (100) rows</a></li>
    </ul>""".format(table[0][0].upper(), table[0][0].upper())
    temp += "<div class='tab-content'>"
    temp += "<div id='{0}1' class='tab-pane active' style='overflow:auto;height:85vh;'>".format(table[0][0].upper())
    temp += """<table class='table table-striped table-hover'>
        <thead><tr><th>ID</th><th>COLUMN_NAME</th><th>DATA_TYPE</th><th>NULLABLE</th></tr></thead>
        <tbody>"""
    for column in table:
        temp += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(column[1], column[2], column[3], column[4])
    temp += """</tbody></table></div>
    <div id='{0}2' class='tab-pane' style='overflow:auto;height:85vh;'>
    <table class='table table-striped table-hover'><thead><tr >""".format(table[0][0].upper())
    Desc1, Title1, Error1 = data.GetInfoFromDB(table[0][0])
    for item1 in Title1:
        temp += "<th>{0}</th>".format(item1)
    temp += "</tr></thead><tbody>"
    for item2 in Desc1:
        temp += "<tr>"
        for line2 in item2:
            temp += "<td>{0}</td>".format(line2)
        temp += "</tr>"
    temp += "</tbody></table></div></div></div>"
    To_File[table[0][0]] = temp

for item in To_File.keys():
    File = open('templates/tables/'+item+'_table_desc.html', 'w')
    File.write(To_File[item])
    File.close()
