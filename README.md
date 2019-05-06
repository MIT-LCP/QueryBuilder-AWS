# Querybuilder

This is the QueryBuilder build page. In order for this to work you must allow apache or NGINX to use a sucket with uwsgi.

First one has to install and activate the python virtual enviroment.
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt 
```

Once you do a git clone, you have to create the preview 100 rows for the databases you will be using. For that run the script `python MIMIC_Table_desc.py`.

You need to set the credentials on the config.py, and create the database for the query history using the `database.dump` file.

You can also run this as a stand alone flask application with `python manage.py`.

