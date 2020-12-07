import pymysql

class SqlService():
    def __init__(self,db,arg=None):
        self.database = pymysql.connect('192.168.116.131','fish','huang',charset='utf8')
        self.databaseCoursor = self.database.cursor()
        self._db = db
        if arg:
             self._db = '%s_%s' % (db,arg)
        try:
            self.databaseCoursor.execute('use stock_%s' % self._db)
        except:
            self.databaseCoursor.execute('create database if not exists stock_%s' % self._db)
            self.databaseCoursor.execute('use stock_%s' % self._db)

    def Execute(self,sen):
        try:
            self.databaseCoursor.execute(sen)
            self.database.commit()
        except pymysql.IntegrityError as a:
            pass

    def GetData(self,target,value='*',condition=''):
        sen = 'select %s from %s_%s %s' % (value,self._db[0:3],target,condition)
        try:
            self.databaseCoursor.execute(sen)
            return self.databaseCoursor.fetchall()   
        except:
            pass
    
    def GetDataBySen(self,sen):
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
        