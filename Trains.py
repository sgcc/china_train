# -*- coding: utf-8 -*-
import sys,time,re,json
import codecs,csv

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Trains:
    def __init__(self,filePath,stationName2Id):

        self.stationName2Id = stationName2Id

        self.stationNames = []
        self.trains=[]
        self.trainsKey = []
        self.trainChannel = {}

        self.errorTrains=[] # name to acronym error

        f = open(filePath,'r')
        try:
            b1 = f.read()
            bf = b1[b1.find('=')+1:]
        finally:
            f.close()

        trainsMap = {}
        json_dic1 = json.loads(bf)
        for s in json_dic1:
            for rq in json_dic1[s]:
                for t in json_dic1[s][rq]:
                    codes,stations = t['station_train_code'].split("(")
                    beginS,endS = stations.split("-")
                    self.stationNames.append([t['train_no'],codes, beginS,endS[:len(endS)-1] ])
                    trainsMap[t['train_no']] = [t['train_no'],codes,beginS,endS[:len(endS)-1]]

        #车次|首发站|终点站
        for key, value in trainsMap.items():
            self.trains.append(value)

            try:
                self.trainsKey.append([
                    value[0],
                    self.stationName2Id[value[2]],
                    self.stationName2Id[value[3]],
                ])
            except Exception as e:
                self.errorTrains.append(value);
                print e



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
