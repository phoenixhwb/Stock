import pymysql
import math
import time
import threading
import datetime
from Services.sqlService import SqlService
from Services.dayService import DayService
from Services.summaryService import SummaryService
from tqdm import tqdm

class AnalysisService():
    def __init__(self,dayNum):
        super().__init__()
    
    @staticmethod
    def _GetSingleDatas(stockId,dayNum):
        daysDatabase = SqlService('day')
        daysDatabaseCount = daysDatabase.GetData(stockId,'count(*)')[0][0]
        
        analysisDatabase = SqlService('analysis_%sdays' % dayNum)
        createDaysSen = ['day%s FLOAT' % i for i in range(1,dayNum)]
        createAnalysisTableSen = 'create table if not exists ana_%s (date Date, %s,dday FLOAT, primary key(date))' \
            % (stockId,','.join(createDaysSen))
        analysisDatabase.Execute(createAnalysisTableSen)
        analysisDatabaseCount = analysisDatabase.GetData(stockId,'count(*)')[0][0]

        expectAnalysisDatabaseCount = daysDatabaseCount-dayNum+1
        if expectAnalysisDatabaseCount == analysisDatabaseCount:
            pass
        elif expectAnalysisDatabaseCount > analysisDatabaseCount:
            newDateCount = expectAnalysisDatabaseCount-analysisDatabaseCount
            conditionSen = ''
            if analysisDatabaseCount > 0:
                conditionSen = 'order by date desc limit %s' % (newDateCount+dayNum-1)
            daysData = daysDatabase.GetData(stockId,'date,ratio',conditionSen)
            if analysisDatabaseCount > 0:
                daysData = list(daysData)
                daysData.reverse()
            insertAnalysisSenList = []
            for i in range(0,newDateCount):
                lastDate = daysData[i+dayNum-1][0]
                insertAnalysisDayDataList = [str(round(day[1])) for day in daysData[i:i+dayNum]]
                insertAnalysisDayDataListSen = ','.join(insertAnalysisDayDataList)
                insertAnalysisSen = '("%s",%s)' % (lastDate,insertAnalysisDayDataListSen)
                insertAnalysisSenList.append(insertAnalysisSen)
            insertAnalysisDaySen = ','.join(['day%s' % i for i in range(1,dayNum)])
            insertAnalysisSenListSen = ','.join(insertAnalysisSenList)
            insertSen = 'insert into ana_%s (date,%s,dday) values %s' % (stockId,insertAnalysisDaySen,insertAnalysisSenListSen) 
            analysisDatabase.Execute(insertSen)

        elif expectAnalysisDatabaseCount > 0:
            deleteAnalysisRowSen = 'delete from ana_%s' % stockId
            analysisDatabase.Execute(deleteAnalysisRowSen)            
        analysisDatabase.Close()
        daysDatabase.Close()
        
    @staticmethod
    def _insertAnalysisDateIntoClassByStockId(stockId,dayNum):
        classId = stockId[0:2]
        dayDataSens = []
        analysisDatabase = SqlService('analysis_%sdays' % dayNum)
        adata = analysisDatabase.GetData(stockId)
        for item in adata:
            trend = str(item[1:6]).strip('(').strip(')')
            d_date = item[0]
            d_day = item[6]
            dayDataSen = '(\"%s\",\"%s\",\"%s\",\"%s\",%s)' % (trend,classId,stockId,d_date,d_day)
            dayDataSens.append(dayDataSen)
        if not dayDataSens == []:
            dayDatasSen = ','.join(dayDataSens)
            insertSen = 'insert into ana_sum_%s (trend,class_id,stock_id,d_date,d_day) values %s' % (classId,dayDatasSen)
            analysisDatabase.Execute(insertSen)
        analysisDatabase.Close()

    @staticmethod
    def _updateAnalysisDataInStock(dayNum,classIds=[]):
        print('Initializing analysis database')
        if classIds == []: classIds = SummaryService.GetClassIds()
        anaDatabase = SqlService('analysis_%sdays' % dayNum)
        for classId in classIds:
            deleteSen = 'delete from ana_sum_%s' % classId
            createSen = 'create table if not exists ana_sum_%s(trend VARCHAR(200), class_id VARCHAR(5), stock_id VARCHAR(10),d_date date, d_day Float)' % classId
            anaDatabase.Execute(createSen)
            anaDatabase.Execute(deleteSen)
        stockIds = SummaryService.GetStockIds(classIds)
        threads = []
        for stockId in stockIds:
            thread = threading.Thread(target=AnalysisService._GetSingleDatas,args=(stockId,dayNum))
            threads.append(thread)
        for thread in tqdm(threads):
            while 1:
                if len(threading.enumerate())<32+8:
                    thread.start()
                    time.sleep(0.02)
                    break
        for thread in threads:
            thread.join()
        print('Initialize Done!')
            
    @staticmethod
    def Update(dayNum,classIds=[]):
        print('Updating analysis database')
        AnalysisService._updateAnalysisDataInStock(dayNum,classIds)
        if classIds == []: classIds = SummaryService.GetClassIds()
        stockIds = SummaryService.GetStockIds(classIds)
        threads = []
        for stockId in tqdm(stockIds):
            t = threading.Thread()
            threads.append(AnalysisService._insertAnalysisDateIntoClassByStockId,arg=(stockId,))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print('Update Done!')

