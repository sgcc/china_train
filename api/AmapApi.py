# -*- coding: utf-8 -*-

'''
高德页面参考
http://lbs.amap.com/dev/analysis#/quota?key=51ecfac48ea733868cccb021b058666f
http://lbs.amap.com/api/webservice/guide/api/search/

'''
import requests
import sys,time,re,json

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Amap:
    '''
    调用高德API接口获取火车站的经纬度
    '''

    def __init__(self):
      self.url = 'http://restapi.amap.com/v3/place/text'
      self.parameters  = {'key': '51ecfac48ea733868cccb021b058666f',
           'keywords': '', #火车站关键字
           'types':150200, #搜索类型为火车站
           'page':1, #获得第一分页数据
           'offset':1 #每页一条数据
           }

    def getStationLocation(self,keyword):

        #去记录中关键词有空格 如：38条‘海 口东’
        newKeyWord = keyword.replace(' ','')
        self.parameters["keywords"] =newKeyWord
        r = requests.get(self.url, params=self.parameters )

        #请求不成功
        if(r.status_code != 200):
            return  []

        #没有符合条件的记录
        json_dic1 = json.loads(r.text)
        if(json_dic1['count'] =='0'):
            return [keyword]

        for s in json_dic1['pois']:
            lon,lat = s['location'].split(",")
            return [s['name'],lon,lat,s['pname'],s['cityname'],s['adname']]


if __name__ == '__main__':

    amap = Amap()
    print amap.getStationLocation('海 口东')



#ss = '{"status":"1","count":"38","info":"OK","infocode":"10000","suggestion":{"keywords":[],"cities":[]},"pois":[{"id":"B000A833V8","name":"北京北站(装修中)","type":"交通设施服务;火车站;火车站","typecode":"150200","biz_type":[],"address":"北滨河路1号","location":"116.352994,39.945261","tel":"010-51866223","distance":[],"biz_ext":[],"pname":"北京市","cityname":"北京市","adname":"西城区","importance":[],"shopid":[],"poiweight":[]}]}'







