import requests
import re
import json

class WebService:
    def __init__(self):
        super().__init__()

    @staticmethod
    def _getData(url,params):
        defaultHeaders = {
        'User-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        'Referer':"http://quote.eastmoney.com/"
        }
        strHtml = requests.get(url=url,params=params,headers=defaultHeaders)
        if strHtml.status_code==200:
            reobj = re.search(r'\((.*?)\)',strHtml.text)
            if reobj :
                data = json.loads(reobj.group(1))['data']
        return data

    @staticmethod
    def QueryList():
        listUrl = 'http://57.push2.eastmoney.com/api/qt/clist/get'
        params = {
        'cb':"jQuery112409469838964850319_1606275622173",
        'pn':1,
        'pz':5000,
        'po':1,
        'np':1,
        'ut':"bd1d9ddb04089700cf9c27f6f7426281",
        'fltt':2,
        'invt':2,
        'fid':"f3",
        'fs':"m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",
        'fields':"f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        '_':"1606275622174"
        }
        return WebService._getData(url=listUrl,params=params)['diff']
    
    @staticmethod
    def QuerySingle(stockId):
        singleUrl = 'http://49.push2his.eastmoney.com/api/qt/stock/kline/get'
        params = {
        'secid':'0.000001',
        'lmt':10000,
        'fqt':0,
        'klt':101,
        'end':"20500101",
        'fields1':"f1,f2,f3,f4,f5,f6",
        'fields2':"f51,f52,f53,f54,f55,f56,f57,f58,f59,f60",
        'ut':"fa5fd1943c7b386f172d6893dbfba10b",
        'cb':"jQuery11240727171619796599_1606285650991",
        '_':"1606287810832"
        }
        class_code = 0
        if re.match('6',stockId):class_code = 1
        params['secid'] = '%s.%s' % (class_code,stockId)

        return WebService._getData(url=singleUrl,params=params)['klines']