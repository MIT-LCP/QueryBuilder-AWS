class Config:
    def __init__(self, name = None, user = None, passwd = None):
        self.user   = "username"
        self.passwd = "password"
        self.name   = "QueryBuilder"

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.passwd

    def getDBName(self):
        return self.name

class DBConfig:
    def __init__(self, name = None, user = None, passwd = None):
        self.user   = "mimicusername"
        self.passwd = "mimicpassword"
        self.name   = "mimic"

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.passwd

    def getDBName(self):
        return self.name
