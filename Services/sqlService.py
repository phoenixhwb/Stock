import pymysql

class SqlService():
    def __init__(self,id):
        self.database = pymysql.connect('localhost','fish','huang',charset='utf8')
        self.databaseCoursor = self.database.cursor()
        self._id = id
        try:
            self.databaseCoursor.execute('use stock_%s' % id)
        except:
            self.databaseCoursor.execute('create database if not exists stock_%s' % id)
            self.databaseCoursor.execute('use stock_%s' % id)

    def Execute(self,sen):
        try:
            self.databaseCoursor.execute(sen)
            self.database.commit()
        except pymysql.IntegrityError as a:
            pass

    def GetData(self,target,value='*',condition=''):
        sen = 'select %s from %s_%s %s' % (value,self._id[0:3],target,condition)
        try:
            self.databaseCoursor.execute(sen)
            return self.databaseCoursor.fetchall()   
        except:
            pass

    def RollBack(self):
        try:
            self.RollBack()
        except:
            pass

    def Close(self):
        try:
            self.database.close()
        except:
            pass
        