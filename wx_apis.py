# -*- coding: utf-8 -*-

from os import access
import requests
import json
import time
from db import DB


class wxApi():
    def GetAccessToken(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        payload = {
            'grant_type': 'client_credential',
            'appid': 'appid',
            'secret': 'secret'
        }

        old_access_token = self.saveAccessToken()
        if old_access_token == False:
            r = requests.get(url=url, params=payload)

            try:
                if r.status_code == 200:
                    r_dict = json.loads(r.text)
                    # 说明请求参数有误，返回没有access_token
                    if 'errcode' in r_dict:
                        return r_dict['errmsg']
                    # 请求成功， 处理access_token
                    else:
                        access_token = r_dict['access_token']
                        self.saveAccessToken(access_token)
                        return access_token
                else:
                    # todo
                    print(r.content)
            except Exception as e:
                return e.args
        else:
            return old_access_token

    def saveAccessToken(self, access_token=''):
        # 当前时间
        current_time = int(time.time())
        # 新建数据库连接
        #db = web.database(dbn='sqlite', db='./db.sqlite3')
        db = DB('access_token')
        # 查询数据库
        #r = db.select('access_token', where='id=1')
        item = db.fetchRow({'id':1},**{'first':True})
        #item = r.first()

        if item is not None and 'id' in item:
            if item['expire_time'] <= current_time:
                # 过期，重新入库
                if access_token:
                    db.update({'id':1},{
                        'access_token':access_token,
                        'expire_time':(current_time+7190)
                    })
                    # db.update('access_token', where='id=$id', vars={'id': 1}, access_token=access_token, expire_time=(current_time+7190))
                else:
                    return False
            else:
                # 没过期
                return item['access_token']
        else:
            if access_token:
                #db.insert('access_token', id=1, access_token=access_token,expire_time=(current_time+7190))
                db.insert({
                    'id':1,
                    'access_token':access_token,
                    'expire_time':(current_time+7190)
                })
                return access_token
            else:
                return False
    
    def sendMsg(self, open_id:str, msg:str):
        access_token = self.GetAccessToken()
        payload = {
            'touser': open_id,
            'msgtype': 'text',
            'text': {
                'content':'来自web的请求发的信息'
            }
        }
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}'
        requests.post(url,data=data)

