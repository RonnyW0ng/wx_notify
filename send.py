# -*- coding: utf-8 -*-
# send.py

import web
from wx_apis import wxApi
from db import DB

class Sender(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) and 'key' in data.keys():
                self.get_open_id_by_key(data.key)
        except Exception as Argument:
            return Argument
    def get_open_id_by_key(self,key:str):
        db = DB('users')
        item = db.fetchRow({'key':key},**{'first':True})
        if item is not None and 'id' in item:
            open_id = item['open_id']
            wx_api = wxApi()
            wx_api.sendMsg(open_id,'来自web请求发送的信息')

            
