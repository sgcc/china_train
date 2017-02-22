# -*- coding: utf-8 -*-
import sqlite3
import sys

from api.Train12306Api import Train12306Api
from model.TrainModel import  TrainModel
from Station import Station
from Trains import Trains
import requests
import sys,time,re,json

reload(sys)
sys.setdefaultencoding( "utf-8" )

class ChinaTrain:
    def __init__(self, path):
        self.appPath = path

    def initDB(self):
        # 初始化数据库
        tModel = TrainModel(self.appPath)
        tModel.init_db()

    def initStation(self):
        self.station = Station(self.appPath)
        # self.station.station2DB()
        self.station.stationLocation2DB()

    def initTrain(self):
        self.t = Trains(self.appPath,self.station.stationName2Id)


if __name__ == '__main__':
        dbpath = 'D:\\work2017\\china_train'

        #初始化数据库
        ct = ChinaTrain(dbpath)
        # ct.initDB()

        #初始化车站
        ct.initStation()

        # 初始化车次
        ct.initTrain()

# conn = sqlite3.connect('D:/work2017/12306/data/trainModel/t12306.db')
# conn.text_factory = str
#
# paths = 'D:/work2017/12306/files/station_name.js'
# s = Station(paths)
#
# paths = 'D:/work2017/12306/files/train_list.js'
# t = Trains(paths,s.stationName2Id)
#
# cur = conn.cursor()
# amap = Train12306Api()
# for i in t.trainsKey:
#     baseT,trainPath = amap.getTrainInfo(i[0],i[1],i[2])
#     if len(baseT)==0:
#         continue
#
#     cur.execute("INSERT INTO train VALUES ( ?,?,?,?,?,?)", baseT)
#     cur.executemany("INSERT INTO train_station VALUES ( ?,?,?,?,?,?,?)", trainPath)
#     conn.commit()
# cur.close()




# saveJsonPath = 'D:/work2017/12306/files/channels.json'
# t.channel_to_json(saveJsonPath)

