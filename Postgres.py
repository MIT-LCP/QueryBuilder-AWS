#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from sys import stderr as http_logger
from psycopg2 import connect, Error
from io import StringIO
from config import DatabaseConfig, Config


class UserModel:
    """
    Store a user query history
    """
    def __init__(self):
        db_info = Config()
        try:
            self.con = connect("dbname={0} user={1} host={2} password={3}\
                ".format(db_info.get_db(), db_info.get_user(),
                         db_info.get_host(), db_info.get_password()))
            self.cur = self.con.cursor()
        except Error as error:
            http_logger.write("Error connecting to the user database: {0}\
                              ".format(error))

    def __del__(self):
        try:
            self.con.close()
        except Error as error:
            http_logger.write("Error deleting connection of the user to the \
                DB: {0}".format(error))

    def get_queries_from_email(self, email):
        """
        Return the user querie history
        """
        try:
            self.cur.execute("""SELECT "Query" FROM "Builder"."Queries" WHERE
                "email" = '%s' order by "Date" desc limit 10""" % email)
            return self.cur.fetchall()
        except Error as error:
            http_logger.write("\t*** ERROR *** Error getting the last \
                              queriess,\nEmail: {0}\nError: {1}\n".format(
                                  email, error))
            return False

    def record_query(self, email, query):
        """
        Record the query used by the user
        """
        try:
            if "'" in query:
                query = query.replace("'", "''")
            self.cur.execute("""INSERT INTO "Builder"."Queries" ("email",
                             "Query") VALUES ('%s', '%s')""" % (email, query))
            self.con.commit()
            return True
        except Error as error:
            http_logger.write("\t*** ERROR *** Error inserting the query,\n\
                Email: {0}\nQuery: {1}\nError: {2}\n".format(email, query,
                                                             error))
            return False


class Database():
    """
    MIMIC database
    """
    def __init__(self):
        db_info = DatabaseConfig()
        try:
            self.con = connect("dbname={0} user={1} host={2} password={3} \
                               options='-c statement_timeout=15min'".format(
                                   db_info.get_db(), db_info.get_user(),
                                   db_info.get_host(), db_info.get_password()))
            self.cur = self.con.cursor()
        except Error as error:
            if self.con:
                self.con.rollback()
            http_logger.write("Error connecting: {0}".format(error))

    def __del__(self):
        try:
            self.con.close()
        except Error as error:
            http_logger.write("Error disconnecting: {0}".format(error))

    def get_tables(self, db_name):
        """
        Get table names from postgres using a schema
        """
        try:
            self.cur.execute("SELECT table_name FROM \
                information_schema.tables WHERE table_schema = '%s' ORDER BY \
                table_name" % db_name)
            return self.cur.fetchall()
        except Error as error:
            http_logger.write("Error with tables: {0}".format(error))
            return False

    def describe_tables(self, table):
        """
        Get table's information
        """
        try:
            self.cur.execute("SELECT ordinal_position, column_name, \
                data_type, is_nullable FROM information_schema.columns WHERE \
                table_name ='%s'" % table)
            return self.cur.fetchall()
        except Error as error:
            http_logger.write("Error describing tables: {0}".format(error))
            return False

    def random_query(self, query):
        """
        Execute a random query done by a user
        """
        try:
            http_logger.write("Query -- : {0}".format(query))
            if "information_schema" in query or "pg_" in query:
                return [["Bad Query"], ], ("Bad Query",), False
            try:
                self.cur.execute("%s" % query)
            except Error as error:
                http_logger.write("Error describing tables: {0}".format(error))
                return False, False, error
            listing = []
            if self.cur.description is not None:
                for item in self.cur.description:
                    listing.append(item[0])

            result = self.cur.fetchmany(500)

            return result, listing, False
        except Error as error:
            http_logger.write("Error describing tables: %s" % error)
            return False, False, error

    def get_table_preview(self, table):
        """
        Get 100 lines of preview from DB
        """
        try:
            query = "SELECT * FROM " + table + " LIMIT 100"
            self.cur.execute(query)
            listing = []
            if self.cur.description is not None:
                for item in self.cur.description:
                    listing.append(item[0])
            return self.cur.fetchmany(100), listing, False
        except Error as error:
            http_logger.write("Error describing tables: %s" % error)
            return False, False, error

    def random_query_download(self, query):
        """
        Execute a random query done by a user to download
        """
        try:
            if "information_schema" in query or "pg_" in query:
                return [["Bad Query"], ], ("Bad Query",), False
            text_stream = StringIO()
            if query.rstrip()[-1] == ';':
                query = query.rstrip()[:-1]
            copy_query = "COPY ({}) TO STDOUT WITH CSV HEADER DELIMITER ','\
                         ".format(query)
            self.cur.copy_expert(copy_query, text_stream)
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
        except Error as error:
            http_logger.write("\t*** ERROR *** Error executing a random query \
                              to download.\nQuery: {0}\nError: {1}".format(
                                  query, error))
            return False, error

    def set_schema(self, schema):
        """
        Set the database schema
        """
        try:
            self.cur.execute("SET search_path TO " + schema)
            self.cur.execute("SET statement_timeout = '15min'")
            self.con.commit()
        except Error as error:
            http_logger.write("Error setting schema: {0}".format(error))
