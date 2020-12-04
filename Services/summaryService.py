from Services.sqlService import SqlService
from Services.webService import WebService
from tqdm import tqdm
import datetime

class SummaryService():
    def __init__(self):
        super().__init__()

    @staticmethod
    def GetClassIds():
        return ['00','30','60','68'];

    @staticmethod
    def _insertStockBasicInfoToSummary(data):
        stid = data['f12']
        name = data['f14']
        classId = stid[0:2]
        return 'insert into sum_%s (id,name) values ("%s","%s")' % (classId,stid,name)

    @staticmethod
    def _getStockIdsByClassId(classId):
        database = SqlService('summary')
        sen = 'select id from sum_%s' % classId
        stockIds = database.GetData(classId,'id')
        database.Close()
        return stockIds
    
    @staticmethod
    def GetStockIds(classIds=[]):
        if classIds == []: classIds = SummaryService.GetClassIds()
        stockIds = []
        for classId in classIds:
            for stockId in SummaryService._getStockIdsByClassId(classId):
                stockIds.append(stockId[0])
        return stockIds

    @staticmethod
    def Update(classIds=[]):
        print('')
        print('%s:Updating summary database....' % datetime.datetime.now())
        if classIds == []: classIds = SummaryService.GetClassIds()
        database = SqlService('summary')
        for classId in classIds:
            createSummarySen = 'create table if not exists sum_%s(id VARCHAR(10),name VARCHAR(10),primary key (id))' % (classId)
            database.Execute(createSummarySen)
        data = WebService.QueryList()
        for item in tqdm(data):
            insertStockBasicInfoToSummarySen=SummaryService._insertStockBasicInfoToSummary(item)
            database.Execute(insertStockBasicInfoToSummarySen)
        print('Update done!')