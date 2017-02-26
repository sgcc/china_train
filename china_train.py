# -*- coding: utf-8 -*-
import sqlite3
import sys


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
        #self.station.stationLocation2DB()
        #self.station.stationLocation2DBByfile()

    def initTrain(self):
        self.t = Trains(self.appPath,self.station.stationName2Id,self.appPath)
        #self.t.toDB()


if __name__ == '__main__':
        dbpath = '/Users/yy/Documents/work2017/china_train'

        #初始化数据库
        ct = ChinaTrain(dbpath)
        # ct.initDB()

        #初始化车站
        ct.initStation()

        #to json
        saveJsonPath = '/Users/yy/Documents/work2017/china_train/file/trainStation.json'
        ct.station.station_to_json(saveJsonPath)

        # 初始化车次
        ct.initTrain()



