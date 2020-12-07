from Services.dayService import DayService
from Services.summaryService import SummaryService
from Services.analysisService import AnalysisService
from Services.sqlService import SqlService
from Services.caculationService import CaculationService
from tqdm import tqdm
import datetime
import re
import threading
import pandas as pd
import numpy as np

def FindNumber(startDate,endDate,count):
    return "select trend, count(*) as count, avg(d_day) as avg from ana_sum_60 where d_date between '%s' and '%s' group by trend having count > %s order by avg desc limit 50" % (startDate,endDate,count) ;

if __name__ == "__main__":
    # SummaryService.Update()
    #DayService.Update()
    # for dayNum in range(6,10):
    #     AnalysisService.Update(dayNum)
        # for year in range(2000,2021):
        #     CaculationService.UpdateYearData(dayNum,year)

    for dayNum in range(6,10):
        anaDatabase = SqlService('analysis','%sdays'%dayNum)
        dates = anaDatabase.GetDataBySen('select d_date from ana_sum_60 group by d_date order by d_date desc')
        for dayDate in dates:
            dayDateEnd = dayDate[0]
            dayDateStart = dayDateEnd + datetime.timedelta(days=-365)
            findNumberSen = FindNumber(dayDateStart,dayDateEnd,50)
            numbers = anaDatabase.GetData(findNumberSen)


    print("")
