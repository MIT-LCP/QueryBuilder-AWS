# Querybuilder

This is the QueryBuilder build page. In order for this to work you must allow apache to run python cgi.

Once you do a git clone, you have to create the preview 100 rows for the databases you will be using. For that run the script `python Python_QB/MIMIC_Table_desc.py <schema>`

After first pull, you have to run the command: `git update-index --assume-unchanged Python_QB/config.py` in order to ignore the changes done in the config file for further pull requests.

Also the apache config was added as jupyter_rstudio_apache.conf.
