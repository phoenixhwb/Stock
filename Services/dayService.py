from Services.sqlService import SqlService
from Services.webService import WebService
from Services.summaryService import SummaryService
from tqdm import tqdm
import datetime
import threading
import time
import re
import rx  

class DayService():
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def _toInsertDayInfoSen(stockId,data):
        li = []
        for dayData in data:
            cdata = re.split(",",dayData,1)
            dayLine = '(\"%s\",%s)' % (cdata[0],cdata[1])
            li.append(dayLine) 
        dataSen = ",".join(li)
        insertSen = 'insert into day_%s (date,start,end,high,low,volume_portion,volume_value,exchange,ratio,value) values %s' % (stockId,dataSen)
        return insertSen

    @staticmethod
    def _createStockDayInfoTable(stockId):
        daysDatabase = SqlService('day')
        sen = 'create table if not exists day_%s(date DATE,start FLOAT,end FLOAT,high FLOAT,low FLOAT,volume_portion BIGINT,volume_value BIGINT,\
            exchange FLOAT,ratio FLOAT,value FLOAT,primary key (date))' % (stockId)
        daysDatabase.Execute(sen)
        runTimes = 0
        while(runTimes<3):
            dbDataCount = daysDatabase.GetData(stockId,'count(*)')[0][0]

            webData = WebService.QuerySingle(stockId)
            webDataCount = len(webData)
            if dbDataCount==webDataCount:
                break
            elif dbDataCount<webDataCount:
                insertSen = DayService._toInsertDayInfoSen(stockId,webData[dbDataCount:webDataCount])
                daysDatabase.Execute(insertSen)
                runTimes += 1
            else:
                deleteTableSen = 'delete from day_%s' % (stockId)
                daysDatabase.Execute(deleteTableSen)

            time.sleep(1)
        daysDatabase.Close()

    @staticmethod
    def Update(classIds=[]):
        print('Updating day database')
        if classIds == []: classIds = SummaryService.GetClassIds()
        stockIds = SummaryService.GetStockIds(classIds)
        threads = []
        for stockId in stockIds:
            p = threading.Thread(target=DayService._createStockDayInfoTable,args=(stockId,))
            threads.append(p)
        for thread in tqdm(threads):
            while 1 :
                if len(threading.enumerate()) < 32+8:
                    thread.start()
                    time.sleep(0.01)
                    break
        for thread in threads:
            thread.join()
        print('Update done!')
