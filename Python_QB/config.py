#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################
# Felipe Torres Fabregas 
# Last modified: October 27, 2017
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# This is the file that contains all of the postgres database 
# user authentication information.
###############################################################
class User_Config:
    """
    The User_Config class is used to store the history of the queries done by 
    the users.
    """
    def __init__(self, name = None, user = None, passwd = None):
        self.user   = "Username"
        self.passwd = "Password"
        self.name   = "DB_Name"
        self.host   = "localhost"

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.passwd

    def getDBName(self):
        return self.name

    def getHost(self):
        return self.host

class ReadOnly_DB:
    def __init__(self, name = None, user = None, passwd = None):
        self.user   = "Username"
        self.passwd = "Password"
        self.name   = "DB_Name"
        self.host   = "localhost"

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.passwd

    def getDBName(self):
        return self.name

    def getHost(self):
        return self.host
