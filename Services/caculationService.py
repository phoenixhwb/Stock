import re
from Services.sqlService import SqlService

class CaculationService():
    def __init__(self):
        super().__init__()

    @staticmethod
    def FilterYearData(dayNum,year):
        db = SqlService('analysis','%sdays' % dayNum)
        data = db.GetData(
            'sum_60',"trend, count(*) as count,\
            avg(d_day) as avg",\
            "where d_date < \"%s-01-01\" group by trend having count > 100 order by avg desc limit 50" % year)
        
        trendSens = []

        for i in data:
            trendSen = i[0]
            trendList = re.split(',',trendSen)
            trendList = [float(item.strip()) for item in trendList]
            if not ((10.0 in trendList) or (5.0 in trendList) or (-10.0 in trendList) or (-5.0 in trendList)):
                if len(trendSens)>5:
                    break
                else:
                    trendSen = 'trend = \"%s\"' % trendSen
                    trendSens.append(trendSen)
        finalSen = ' or '.join(trendSens)
        d = db.GetData(target='sum_60',condition="where (%s) and d_date between \"%s-01-01\" and \"%s-01-01\"" % (finalSen,year,year+1))

    @staticmethod
    def UpdateYearData(dayNum,year):
        database = SqlService('caculation','%sdays' % dayNum)
        data = CaculationService.FilterYearData(dayNum,year)
        ds = []
        for item in data:
            ds.append(item)
        print('')