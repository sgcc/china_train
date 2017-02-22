# -*- coding: utf-8 -*-
import codecs
import csv
import json
import sqlite3
import sys
import requests
import sys,time,re,json

from  api.AmapApi import Amap #高德

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Station:
    def __init__(self,dataPath):
        self.conn = sqlite3.connect(dataPath + '//model//chinaTrain.db')
        self.conn.text_factory = str

        self.stationNames = []
        self.gdmap = Amap()
        self.stationName2Id ={}
        self.errorStationNoLocation = []

        self.init()

    def init(self):
        Url_trainInfo = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8997'
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


    def station2DB(self):
        cur = self.conn.cursor()
        cur.executemany("INSERT INTO station VALUES ( ?,?,?,?,?,?)",self.stationNames);
        self.conn.commit()
        cur.close()

    def stationLocation2DB(self):

        cur = self.conn.cursor()
        cur.execute("SELECT  s.name,s.key FROM station s WHERE s.key  NOT  IN (SELECT l.key FROM station_location l)")

        location = []
        for i in cur.fetchall():
            alistLocal = self.gdmap.getStationLocation(i[0])
            if len(alistLocal) ==6:
                alistLocal.insert(0,i[0])
                alistLocal.insert(0,i[1])
                location.append(alistLocal)

                cur.execute("INSERT INTO station_location  VALUES ( ?,?,?,?,?,?,?,?)",alistLocal);
                self.conn.commit()
            else:
                self.errorStationNoLocation.append(alistLocal[0])
        cur.close()



if __name__ == '__main__':
    dbpath = 'D:\\work2017\\china_train'
    sn = Station(dbpath)
    print  '解析火车站：', len(sn.stationNames)

    sn.station2DB()
    sn.stationLocation2DB()











