# -*- coding: utf-8 -*-

'''
12306 网站页面
https://kyfw.12306.cn/otn/czxx/init

对网页api的解释
https://www.v2ex.com/t/336932
https://zhuanlan.zhihu.com/p/20559891

zhihu上对12306的评价
https://www.zhihu.com/question/22451397/answer/29666652

'''
import requests
import sys,time,re,json

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Train12306Api:
    '''
    调用高德API接口获取火车站的经纬度
    '''

    def __init__(self):
        self.currentTime = '2017-02-19'
        self.errorTrain=[]

        self.Url_trainInfo = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo'


    def getTrainInfo(self,trainNo,fromStation,toStation):
        '''
        {"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"data":[{
        "start_station_name":"北京西","arrive_time":"----","station_train_code":"T3037","station_name":"北京西","train_class_name":"特快","service_type":"1","start_time":"00:50","stopover_time":"----","end_station_name":"汉口","station_no":"01","isEnabled":true},{"arrive_time":"02:10","station_name":"保定","start_time":"02:16","stopover_time":"6分钟","station_no":"02","isEnabled":true},{"arrive_time":"03:35","station_name":"石家庄","start_time":"03:43","stopover_time":"8分钟","station_no":"03","isEnabled":true},{"arrive_time":"04:37","station_name":"邢台","start_time":"04:41","stopover_time":"4分钟","station_no":"04","isEnabled":true},{"arrive_time":"05:16","station_name":"邯郸","start_time":"05:22","stopover_time":"6分钟","station_no":"05","isEnabled":true},{"arrive_time":"06:03","station_name":"安阳","start_time":"06:07","stopover_time":"4分钟","station_no":"06","isEnabled":true},{"arrive_time":"06:41","station_name":"鹤壁","start_time":"06:44","stopover_time":"3分钟","station_no":"07","isEnabled":true},{"arrive_time":"07:18","station_name":"新乡","start_time":"07:23","stopover_time":"5分钟","station_no":"08","isEnabled":true},{"arrive_time":"08:12","station_name":"郑州","start_time":"08:28","stopover_time":"16分钟","station_no":"09","isEnabled":true},{"arrive_time":"09:23","station_name":"许昌","start_time":"09:26","stopover_time":"3分钟","station_no":"10","isEnabled":true},{"arrive_time":"10:06","station_name":"漯河","start_time":"10:12","stopover_time":"6分钟","station_no":"11","isEnabled":true},{"arrive_time":"13:56","station_name":"汉口","start_time":"13:56","stopover_time":"----","station_no":"12","isEnabled":true}]},"messages":[],"validateMessages":{}}
        '''
        Url_trainInfo =  'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=' + trainNo  + '&from_station_telecode=' + fromStation  + '&to_station_telecode=' + toStation + '&depart_date=' + self.currentTime
        r = requests.get(Url_trainInfo,verify=False )

        #请求不成功
        if(r.status_code != 200):
            return  [],[]

        #没有符合条件的记录
        json_dic1 = json.loads(r.text)
        stations = []
        baseStation = []
        for s in json_dic1['data']['data']:

            if s['station_no'] =='01':
                baseStation = [
                    trainNo,
                    fromStation,
                    toStation,
                    s['station_train_code'],
                    s['train_class_name'],
                    s['service_type']
                ]
            stations.append( [
                trainNo,
                s['station_no'],
                s['isEnabled'],
                s['arrive_time'],
                s['station_name'],
                s['start_time'],
                s['stopover_time'],
            ])

        return  baseStation,stations

if __name__ == '__main__':



    print amap.getTrainInfo('11000C100302','CCT','HUL')