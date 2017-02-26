# -*- coding: utf-8 -*-
import codecs
import csv
import json
import sqlite3
import sys
import requests
import sys,time,re,json

from  api.AmapApi import Amap #高德

import xlrd

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Station:
    def __init__(self,dataPath):
        self.conn = sqlite3.connect(dataPath + '/model/chinaTrain.db')
        self.conn.text_factory = str

        self.stationNames = []
        self.gdmap = Amap()
        self.stationName2Id ={}
        self.errorStationNoLocation = []

        self.stationLocationA = {} #elcel中的 场站位置信息

        self.init()

    def init(self):
        Url_trainInfo = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        r = requests.get(Url_trainInfo, verify=False)
        if(r.status_code != 200):
            print "获取车站信息错误"
            return  False

        for s in r.text.split('@')[1:]:
            ss = s.split('|')
            stationName = ss[1].replace(' ','').strip()
            ss[1]=stationName
            if self.stationName2Id.has_key(ss[1].decode('utf-8')):
                continue
            else:
                self.stationNames.append(ss)
                self.stationName2Id[ss[1].decode('utf-8')] = ss[2]

        #从excel中初始化车站位置
        data = xlrd.open_workbook('/Users/yy/Documents/work2017/china_train/file/chinaTrainLocation.xlsx')
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(nrows - 2):
            self.stationLocationA[table.cell(i + 2, 2).value[0:-3].decode('utf-8')] = [table.cell(i + 2, 6).value, table.cell(i + 2, 7).value]

        print 'train init ok'


    def station2DB(self):
        cur = self.conn.cursor()
        cur.executemany("INSERT INTO station VALUES ( ?,?,?,?,?,?)",self.stationNames);
        self.conn.commit()
        cur.close()

    def stationLocation2DBByfile(self):

        cur = self.conn.cursor()
        cur.execute("SELECT l.name FROM station_location l ")

        keys = []
        for i in cur.fetchall():
            keys.append(i[0])

        staionL = []
        for i in self.stationNames:
            if self.stationLocationA.has_key(i[1]) and  i[1] not in keys:
                staionL.append([i[2],i[1],'',self.stationLocationA[i[1]][0],self.stationLocationA[i[1]][1],'','',''])

        cur.executemany("INSERT INTO station_location  VALUES ( ?,?,?,?,?,?,?,?)", staionL);
        self.conn.commit()
        cur.close()

        print 'has station',len(staionL)



    def stationLocation2DB(self):

        cur = self.conn.cursor()
        cur.execute(" SELECT  s.name,s.key ,s.no FROM station s WHERE s.key  NOT  IN (SELECT l.key FROM station_location l) ORDER BY s.no")

        stationkey =[]
        for i in cur.fetchall():
            stationkey.append([i[0],i[1]])

        location = []
        for i in stationkey:
            alistLocal = self.gdmap.getStationLocation(i[0]+ '站')
            if len(alistLocal) == 6:
                alistLocal.insert(0, i[0])
                alistLocal.insert(0, i[1])
                location.append(alistLocal)

                cur.execute("INSERT INTO station_location  VALUES ( ?,?,?,?,?,?,?,?)", alistLocal);
                self.conn.commit()
            else:
                self.errorStationNoLocation.append(alistLocal[0])

        print 'init station location is ok '


    def station_to_json(self,savePath):

        cur = self.conn.cursor()
        cur.execute(" SELECT s.key,s.name,s.lat,s.lng FROM station_location s ")

        stationkey =[]
        for i in cur.fetchall():
            try:
                stationkey.append({
                    'key':i[0],
                    'name':i[1],
                    'coordinates':[i[2],i[3]]
                })
            except Exception as e:
                print e
        self.conn.close()

        fp = open(savePath,'w')
        fp.write(json.dumps(stationkey))
        fp.close()

        print '保存channel json文件成功(',len(self.trainChannel),')'



if __name__ == '__main__':
    dbpath = 'D:\\work2017\\china_train'
    sn = Station(dbpath)
    print  '解析火车站：', len(sn.stationNames)

    sn.station2DB()
    sn.stationLocation2DB()











