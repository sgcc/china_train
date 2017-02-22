
# -*- coding: utf-8 -*-

'''
参考：
https://www.keakon.net/2012/12/03/SQLAlchemy%E4%BD%BF%E7%94%A8%E7%BB%8F%E9%AA%8C
http://www.runoob.com/sqlite/sqlite-python.html
http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0014021031294178f993c85204e4d1b81ab032070641ce5000

flsk-sqlalvhemy
http://docs.jinkan.org/docs/flask-sqlalchemy/quickstart.html


'''

import sys,time,re,json
import codecs,csv

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
BaseModel = declarative_base()

# # 定义User对象:
# class Station(BaseModel):
#     # 表的名字:
#     __tablename__ = 'station'
#
#     # 表的结构:
#     namePY  = Column(String(20))
#     name    = Column(String(20))
#     key     = Column(String(20), primary_key=True)
#     py      = Column(String(20))
#     keyPY   = Column(String(20))
#     no      = Column(String(20))
#
# class StationLocation(BaseModel):
#     # 表的名字:
#     __tablename__ = 'station_location'
#
#     # 表的结构:
#     key         = Column(String(20), primary_key=True)
#     name        = Column(String(20))
#     stationName = Column(String(20))
#     lat         = Column(String(20))
#     lng         = Column(String(20))
#     province    =  Column(String(20))
#     city        =  Column(String(20))
#     area        =  Column(String(20))
#
# class Train(BaseModel):
#     # 表的名字:
#     __tablename__ = 'train'
#
#     # 表的结构:
#     train_no           = Column(String(20), primary_key=True)
#     start_station_name = Column(String(20))
#     end_station_name   = Column(String(20))
#     station_train_code = Column(String(20))
#     start_station_key  = Column(String(20))
#     end_station_key    = Column(String(20))
#     train_class_name   = Column(String(20))
#     service_type       = Column(String(20))

class Train_Station(BaseModel):
    # 表的名字:
    __tablename__ = 'train_station'

    # 表的结构:
    train_no     = Column(String(20),primary_key=True)
    station_no   = Column(String(20), primary_key=True)
    isEnabled    = Column(String(20))
    arrive_time  = Column(String(20))
    station_name = Column(String(20))
    start_time   = Column(String(20))
    stopover_time= Column(String(20))

class TrainModel:
    def __init__(self,path):
        dbpath = 'sqlite:///' + path + '//model//chinaTrain.db'

        # 初始化数据库连接:
        self.engine = create_engine(dbpath, echo=True)
        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=self.engine)

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)

if __name__ == '__main__':
    dbpath =  'D:\\work2017\\china_train'
    cr = TrainModel(dbpath)
    # cr.drop_db()
    cr.init_db()
    print 'init database OK'

