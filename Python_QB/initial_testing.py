#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################
# Felipe Torres Fabregas 
# Last modified: October 27, 2017
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# This is the file that contains all of the postgres database 
# functions.
###############################################################
from psycopg2 import connect, Error
from datetime import datetime
from sys import stderr as http_logger
from config import *

class UserModel:
    """
    In this model, we ONLY store all the past queries to mantain a history for the user
    """
    def __init__(self):
        dbinfo = User_Config()
        try:
            self.con = connect("dbname={0} user={1} host={2} password={3}".format(dbinfo.getDBName(), dbinfo.getUser(), dbinfo.getHost(), dbinfo.getPassword()))
            self.cur = self.con.cursor()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error connecting to the Database\t")

    def __del__(self):
        try:
            self.con.close()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error closing the connection to the Database\t")

    def InsertQRow(self, email, Query):
        try:
            if "'" in Query:
                Query = Query.replace("'","''")
            self.cur.execute("""INSERT INTO "QueryBuilder"."Queries" ("email", "Query") VALUES ('%s', '%s')""" % (email, Query))
            self.con.commit()
            return True
        except Error, e:
            http_logger.write("\t*** ERROR *** Error inserting the query,\nEmail: {0}\nQuery: {1}\nError: {2}\n".format(email, Query, e))
            return False

    def GetQueriesByEmail(self, email):
        try:
            self.cur.execute("""SELECT "Query" FROM "QueryBuilder"."Queries" WHERE "email" = '%s' order by "Date" desc limit 10""" %email)
            return self.cur.fetchall()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error getting the last queriess,\nEmail: {0}\nError: {1}\n".format(email, e))
            return False

class SessionModel:
    """
    In this model, we ONLY store a session, to make sure authorized users are logged.
    """
    def __init__(self):
        dbinfo = User_Config()
        try:
            self.con = connect("dbname={0} user={1} host={2} password={3}".format(dbinfo.getDBName(), dbinfo.getUser(), dbinfo.getHost(), dbinfo.getPassword()))
            self.cur = self.con.cursor()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error connecting to the Database\t")

    def __del__(self):
        try:
            self.con.close()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error closing the connection to the Database\t")

    def AddSession(self, email, SID):
        try:
            self.cur.execute("INSERT INTO \"QueryBuilder\".\"Sessions\" (\"email\", \"SID\") VALUES ('%s', '%s')" % (email, SID))
            self.con.commit()
            return True
        except Error, e:
            http_logger.write("\t*** ERROR *** Error adding the session,\nEmail: {0}\nSID: {1}\nError: {2}\n".format(email, SID, e))
            return False

    def GetSession(self, SID):
        try:
            self.cur.execute("SELECT * FROM \"QueryBuilder\".\"Sessions\" WHERE \"SID\" = %s" % (SID))
            return self.cur.fetchone()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error getting the session,\nSID: {1}\nError: {2}\n".format(email, SID, e))
            return False

class Database():
    """
    This is the main class, here all the queries done by a user are executed.
    We disallow access to the information_schema and any pg_* tables.
    """
    def __init__(self, DB_NAME):
        dbinfo = ReadOnly_DB()
        try:
            self.con = connect("dbname={0} user={1} host={2} password={3}".format(dbinfo.getDBName(), dbinfo.getUser(), dbinfo.getHost(), dbinfo.getPassword()))
            self.cur = self.con.cursor()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error connecting to the Database\t")

    def __del__(self):
        try:
            self.con.close()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error closing the connection to the Database\t")

    def GetTables(self, DB):
        try:
            self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '%s' ORDER BY table_name" % DB)
            return self.cur.fetchall()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error getting information from the Database.\nDatabase: {0}\nError: {1}".format(DB, e))
            return False

    def DescTables(self, Table):
        try:
            self.cur.execute("SELECT ordinal_position, column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name ='%s'" %Table)
            return self.cur.fetchall()
        except Error, e:
            http_logger.write("\t*** ERROR *** Error getting information from the tables.\nDatabase: {0}\nError: {1}".format(Table, e))
            return False

    def RandomQ(self, Query):
        try:
            if "information_schema" in Query or "pg_" in Query:
                return [["Bad Query"],], ("Bad Query",), False
            self.cur.execute(Query)
            listing = []
            if self.cur.description != None:
                for item in self.cur.description:
                    listing.append(item[0])
            Result = self.cur.fetchmany(1000)
            return Result, listing, False
        except Error, e:
            http_logger.write("\t*** ERROR *** Error executing a random query.\nQuery: {0}\nError: {1}".format(Query, e))
            return False, '', e

    def GetInfoFromDB(self, Table):
        try:
            Query = "SELECT * FROM " + Table + " LIMIT 100"
            self.cur.execute("%s" %Query)
            listing = []
            if self.cur.description != None:
                for item in self.cur.description:
                    listing.append(item[0])
            return self.cur.fetchmany(100), listing, False
        except Error, e:
            http_logger.write("\t*** ERROR *** Error getting the 100 rows for preview.\nTable: {0}\nError: {1}".format(Table, e))
            return False, False, e

    def RandomQDown(self, Query):
        try:
            if "information_schema" in Query or "pg_" in Query:
                return [["Bad Query"],], ("Bad Query",), False
            text_stream = StringIO()
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
            return temp, False
        except Error, e:
            http_logger.write("\t*** ERROR *** Error executing a random query to download.\nQuery: {0}\nError: {1}".format(Query, e))
            return False, e
    # def RandomQDown(self, Query):
    #     try:
    #         if "information_schema" in Query or "pg_" in Query:
    #             return [["Bad Query"],], ("Bad Query",), False
    #         self.cur.execute("%s" %Query)
    #         listing = []
    #         if self.cur.description != None:
    #             for item in self.cur.description:
    #                 listing.append(item[0])
    #         Down = self.cur.fetchmany(5000)
    #         Down.insert(0, listing)
    #         return Down, listing, False
    #     except Error, e:
    #         http_logger.write("\t*** ERROR *** Error executing a random query to download.\nQuery: {0}\nError: {1}".format(Query, e))
    #         return False, False, e

    def SetSchema(self, Schema):
        from urllib import urlopen
        url = "https://querybuilder-lcp.mit.edu/json"
        response = urlopen(url)
        data = response.read().split('\n')
        for item in data:
            if item == Schema:
                try:
                    self.cur.execute("SET search_path TO " + Schema)
                    self.con.commit()
                    return Schema
                except Error, e:
                    http_logger.write("\t*** ERROR *** Error setting the schema.\nSchema: {0}\nError: {1}".format(Schema, e))
                    return False
        http_logger.write("\t*** INFO *** NO SCHEMA found.\nSchema: {0}\n".format(Schema))
        return False

def GetAuth2(User, Pass, IP):
    from requests import get
    url = 'https://physionet.org/works/MIMICIIIClinicalDatabase/files/'
    response = get(url, auth=(User, Pass))
    return response.status_code

