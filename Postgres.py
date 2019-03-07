#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################
# Felipe Torres Fabregas 
# Last modified: October 27, 2017
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# This is the file that contains all of the postgres database 
# functions.
###############################################################
from sys import stderr as http_logger
from psycopg2 import connect, Error
from io import StringIO
from config import *


class UserModel:

    def __init__(self):
        dbinfo = Config()
        try:
            self.con = connect("dbname={0} user={1} host=localhost password={2}".format(
                dbinfo.getDBName(), dbinfo.getUser(), dbinfo.getPassword()))
            self.cur = self.con.cursor()
        except Error as e:
            http_logger.write("Error connecting to the user DB: {0}".format(e))

    def __del__(self):
        try:
            self.con.close()
        except Error as e:
            http_logger.write("Error deleting connection of the user to the DB: {0}".format(e))

    def GetQueriesByEmail(self, email):
        try:
            self.cur.execute("""SELECT "Query" FROM "Builder"."Queries" WHERE "email" = '%s' order by "Date" desc limit 10""" %email)
            return self.cur.fetchall()
        except Error as e:
            http_logger.write("\t*** ERROR *** Error getting the last queriess,\nEmail: {0}\nError: {1}\n".format(email, e))
            return False

    def InsertQRow(self, email, Query):
        try:
            if "'" in Query:
                Query = Query.replace("'","''")
            self.cur.execute("""INSERT INTO "Builder"."Queries" ("email", "Query") VALUES ('%s', '%s')""" % (email, Query))
            self.con.commit()
            return True
        except Error as e:
            http_logger.write("\t*** ERROR *** Error inserting the query,\nEmail: {0}\nQuery: {1}\nError: {2}\n".format(email, Query, e))
            return False

class SessionModel:

    def __init__(self):
        dbinfo = Config()
        try:
            self.con = connect("dbname={0} user={1} host=localhost password={2}".format(
                dbinfo.getDBName(), dbinfo.getUser(), dbinfo.getPassword()))
            self.cur = self.con.cursor()
        except Error as e:
            if self.con:
                self.con.rollback()
            http_logger.write("Error connecting to the user DB: {0}".format(e))

    def __del__(self):
        try:
            self.con.close()
        except Error as e:
            http_logger.write("Error deleting connection of the user to the DB: {0}".format(e))

    def AddSession(self, email, SID):
        try:
            self.cur.execute("""INSERT INTO "Builder"."Sessions" ("email", "SID")"""+" VALUES ('%s', '%s')" % (email, SID))
            self.con.commit()
            return True
        except Error as e:
            http_logger.write("Error adding the session {0}".format(e))
            return False

    def GetSession(self, SID):
        try:
            self.cur.execute("""SELECT * FROM "Builder"."Sessions" WHERE "SID" = """+"%s" % (SID))
            return self.cur.fetchone()
        except Error as e:
            http_logger.write("Error aquiering the session {0}".format(e))
            return False

class Database():
    def __init__(self):
        dbinfo = DBConfig()

        try:
            self.con = connect("dbname={0} user={1} host=192.168.11.135 password={2} options='-c statement_timeout=15min'".format(
                dbinfo.getDBName(), dbinfo.getUser(), dbinfo.getPassword()))
            self.cur = self.con.cursor()
        except Error as e:
            if self.con:
                self.con.rollback()
            http_logger.write("Error connecting: {0}".format(e))

    def __del__(self):
        try:
            self.con.close()
        except Error as e:
            http_logger.write("Error disconnecting: {0}".format(e))

    def GetTables(self, DB):
        try:
            self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '%s' ORDER BY table_name" % DB)
            return self.cur.fetchall()
        except Error as e:
            http_logger.write("Error with tables: {0}".format(e))
            return False

    def DescTables(self, Table):
        try:
            self.cur.execute("SELECT ordinal_position, column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name ='%s'" %Table)
            return self.cur.fetchall()
        except Error as e:
            http_logger.write("Error describing tables: {0}".format(e))
            return False

    def RandomQ(self, Query):
        try:
            if "information_schema" in Query or "pg_" in Query:
                return [["Bad Query"],], ("Bad Query",), False
            try:
                self.cur.execute("%s" % Query)
            except Error as e:
                http_logger.write("Error describing tables: {0}".format(e))
                return False, False, e
            listing = []
            if self.cur.description != None:
                for item in self.cur.description:
                    listing.append(item[0])

            Result = self.cur.fetchmany(500)

            return Result, listing, False
        except Error as e:
            http_logger.write("Error describing tables: %s" % e)
            return False, False, e

    def GetInfoFromDB(self, Table):
        try:
            Query = "SELECT * FROM " + Table + " LIMIT 100"
            self.cur.execute("%s" %Query)
            listing = []
            if self.cur.description != None:
                for item in self.cur.description:
                    listing.append(item[0])
            return self.cur.fetchmany(100), listing, False
        except Error as e:
            http_logger.write("Error describing tables: %s" % e)
            return False, False, e

    def RandomQDown(self, Query):
        try:
            if "information_schema" in Query or "pg_" in Query:
                return [["Bad Query"],], ("Bad Query",), False
            text_stream = StringIO()
            if ';' == Query.rstrip()[-1]:
                Query = Query.rstrip()[:-1]
            copy_query = "COPY (" + Query + ") TO STDOUT WITH CSV HEADER DELIMITER ','"
            self.cur.copy_expert(copy_query,text_stream)
            tmp = 0
            temp = u''
            text_stream.seek(0)
            while tmp < 5000:
                try:
                    temp += next(text_stream)
                    tmp += 1
                except:
                    tmp = 5000
            #Output = text_stream.getvalue()
            return temp, False
        except Error as e:
            http_logger.write("\t*** ERROR *** Error executing a random query to download.\nQuery: {0}\nError: {1}".format(Query, e))
            return False, e

    def SetSchema(self, Schema):
        try:
            self.cur.execute("SET search_path TO " + Schema)
            self.cur.execute("SET statement_timeout = '15min'")
            self.con.commit()
            return Schema
        except Error as e:
            http_logger.write("Error setting schema: {0}".format(e))
            return False
