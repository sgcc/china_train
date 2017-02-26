# -*- coding: utf-8 -*-
import sys,time,re,json
import codecs,csv
import requests
import sqlite3
from api.Train12306Api import Train12306Api

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Trains:
    def __init__(self,filePath,stationName2Id,dataPath):

        self.conn = sqlite3.connect(dataPath + '/model/chinaTrain.db')
        self.conn.text_factory = str

        self.stationName2Id = stationName2Id

        self.stationNames = []
        self.trains=[]
        self.trainsKey = []
        self.trainChannel = {}

        self.errorTrains=[] # name to acronym error

        Url_trainInfo = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js?scriptVersion=1.0'
        r = requests.get(Url_trainInfo, verify=False).text

        bf = r[r.find('=')+1:]

        trainsMap = {}
        json_dic1 = json.loads(bf)
        for s in json_dic1:
            for rq in json_dic1[s]:
                for t in json_dic1[s][rq]:
                    codes,stations = t['station_train_code'].split("(")
                    beginS,endS = stations.split("-")
                    self.stationNames.append([t['train_no'],codes, beginS.replace(' ','').strip(),endS[:len(endS)-1].replace(' ','').strip() ])
                    trainsMap[t['train_no']] = [t['train_no'],codes,beginS.replace(' ','').strip(),endS[:len(endS)-1].replace(' ','').strip()]

        #车次|首发站|终点站
        for key, value in trainsMap.items():
            self.trains.append(value)

            try:
                self.trainsKey.append([
                    value[0],
                    self.stationName2Id[value[2]],
                    self.stationName2Id[value[3]],
                    value[2],
                    value[3]
                ])
            except Exception as e:
                self.errorTrains.append(value[1]);
                print e
        print self.errorTrains


        #生成通道
        self.makeChannel()

    def makeChannel(self):
        trainChannel = {}
        for tra in self.trains:
           if trainChannel.has_key((tra[1],tra[2])):
                trainList = trainChannel[(tra[1],tra[2])]
                trainList.append(tra)
                trainChannel[(tra[1],tra[2])] = trainList
           elif trainChannel.has_key((tra[2],tra[1])):
                trainList = trainChannel[(tra[2],tra[1])]
                trainList.append(tra)
                trainChannel[(tra[2],tra[1])] = trainList
           else:
               trainChannel[(tra[1],tra[2])] = [tra]

        print 'make channel:',len(trainChannel)
        self.trainChannel = trainChannel

    def toDB(self):

        cur = self.conn.cursor()
        amap = Train12306Api()
        for i in self.trainsKey:
            baseT,trainPath = amap.getTrainInfo(i)
            if len(baseT)==0:
                continue

            cur.execute("INSERT INTO train VALUES ( ?,?,?,?,?,?,?,?)", baseT)
            cur.executemany("INSERT INTO train_station VALUES ( ?,?,?,?,?,?,?)", trainPath)
            self.conn.commit()
        cur.close()

    def to_csv(self,savePath,lists):
        csvfile = file(savePath, 'wb')
        try:
            csvfile.write(codecs.BOM_UTF8) #中文处理
            writer = csv.writer(csvfile)
           # writer.writerow(['shader','file'])
            writer.writerows(lists)
        finally:
            csvfile.close()

    def trains_to_csv(self,savePath):
        self.to_csv(savePath,self.trains)
        print '保存trains scv文件成功(',len(self.trains),')'

    def channel_to_json(self,savePath):

        outJson = []
        for key, value in self.trainChannel.items():
            try:
                outJson.append({
                    'source':self.stationName2Id[key[0]],
                    'target':self.stationName2Id[key[1]],
                    'bName':key[0],
                    'eName':key[1],
                    'trains':value
                })
            except Exception as e:
                print e

        fp = open(savePath,'w')
        fp.write(json.dumps(outJson))
        fp.close()

        print '保存channel json文件成功(',len(self.trainChannel),')'



if __name__ == '__main__':

    paths = 'D:/work2017/12306/files/train_list.js'
    sn = Trains(paths,{})
    print  '解析火车次：', len(sn.stationNames)

    # savePaths = 'D:/work2017/12306/files/trainList.csv'
    # sn.trains_to_csv(savePaths)

    saveJsonPath = 'D:/work2017/12306/files/channels.json'
    sn.channel_to_json(saveJsonPath)
