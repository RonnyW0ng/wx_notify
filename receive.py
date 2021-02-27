# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import handle


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    # 使用第三方库处理xml数据
    xmlData = ET.fromstring(web_data)
    # 查找消息类型并转换成text(字符串类型)
    msg_type = xmlData.find('MsgType').text
    # 普通文字信息
    if msg_type == 'text':
        return TextMsg(xmlData)
    # 图片信息
    elif msg_type == 'image':
        return ImageMsg(xmlData)
    # 关注/取消关注信息
    elif msg_type == 'event':
        return EventMsg(xmlData)
    # # 语音信息
    # elif msg_type == 'voice':
    #     # todo
    #     pass
    # # 视频信息
    # elif msg_type == 'video':
    #     # todo
    #     pass
    # # 小视频信息
    # elif msg_type == 'shortvideo':
    #     # todo
    #     pass
    # # 地理位置
    # elif msg_type == 'location':
    #     # todo
    #     pass
    # # 链接
    # elif msg_type == 'link':
    #     # todo
    #     pass
    

class Msg(object):
    def __init__(self, xmlData):
        msg_type = xmlData.find('MsgType').text
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = msg_type
        self.Event = ''
        if msg_type != 'event':
            self.MsgId = xmlData.find('MsgId').text


class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")


class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

class EventMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self,xmlData)
        self.Event = xmlData.find('Event').text.encode("utf-8")