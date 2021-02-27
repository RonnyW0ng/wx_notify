# -*- coding: utf-8 -*-

import hashlib
import web
import reply
import receive
from db import DB


def log_to_file(file_name, data):
    with open(file_name, 'w+') as file_handler:
        file_handler.write(str(data))
        file_handler.close()


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            return self.validation_wx_signature(data)
        except Exception as Argument:
            return Argument

    def validation_wx_signature(self, data):
        try:
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "replace your token"

            tmp_list = [token, timestamp, nonce]
            tmp_list.sort()
            tmp_str = ''.join(tmp_list)
            sha1 = hashlib.sha1(tmp_str.encode('utf-8'))
            # 不成功, 生成的sha1值对不上
            #sha1 = hashlib.sha1()
            # map(sha1.update,tmp_list)
            hashcode = sha1.hexdigest()
            #print(f"handle/GET func:{hashcode}")
            # 两值比对相同则是来自微信服务器的数据
            if hashcode == signature:
                return echostr
            else:
                raise Exception('验签失败1')
        except Exception as Argument:
            raise Exception('签名失败2')

    def POST(self):
        try:
            # get_data = web.input()
            # 接受来自微信的xml数据
            post_data = web.data()
            #log_to_file('xml_data.log', post_data)
            db = DB('users')

            # 调用receive模块的parse_xml方法处理xml数据
            rec_msg = receive.parse_xml(post_data)
            # 判断rec_msg是否是receive模块的Msg类的实例
            # rec_msg.MsgType是来自微信xml的数据
            if isinstance(rec_msg, receive.Msg):
                toUser = rec_msg.FromUserName  # 发消息的人
                fromUser = rec_msg.ToUserName  # 公众号本身
                if rec_msg.MsgType == 'text':
                    content = 'test'  # 回复的内容
                    if rec_msg.Content.decode('utf-8') == 'key':
                        # 返回用户对应的key
                        item = db.fetchRow({
                            'open_id':toUser
                            },**{
                                'first':True
                                })
                        content = '尚未找到你所对应的key, 请尝试联系管理员'
                        if 'open_id' in item:
                            content = item['key']

                    # 调用 reply模块的TestMsg进行回复
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                elif rec_msg.MsgType == 'image':
                    mediaId = rec_msg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                elif rec_msg.MsgType == 'event':
                    log_to_file('event.log', rec_msg.Event)
                    # log_to_file('event.log',rec_msg)
                    db = web.database(dbn='sqlite', db='./db.sqlite3')
                    event = rec_msg.Event.decode('utf-8')
                    if event == 'unsubscribe':
                        content = ''
                        db.update('users', where='open_id=$id', vars={
                            'id': toUser}, status=0)
                        # todo somethings
                    else:
                        r = db.select('users', where='open_id=$id',
                                      vars={'id': toUser})
                        item = r.first()
                        if item is None:
                            key_ = hashlib.md5(toUser.encode('utf-8'))
                            db.insert('users', open_id=toUser,
                                      key=key_.hexdigest())
                        else:
                            key_ = item['key']
                            db.update('users', where='open_id=$id', vars={
                                'id': toUser
                            }, status=1)
                        content = f'欢迎关注,你的key为\n{key_}'
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
            else:
                return ''
        except Exception as error:
            return error
