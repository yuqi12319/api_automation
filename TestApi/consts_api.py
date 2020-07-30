# coding:utf-8
# Name:consts_api.py
# Author:qi.yu
# Time:2020/7/22 3:27 下午

from Common.request import Request
import Common.consts


class Const(object):

    def __init__(self):
        self.request = Request()
        self.headers = dict()
        self.headers['X-Dk-Token'] = Common.consts.ACCESS_TOKEN[0]
