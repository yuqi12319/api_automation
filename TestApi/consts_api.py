# coding:utf-8
# Name:consts_api.py
# Author:qi.yu
# Time:2020/7/22 3:27 下午

from Common.request import Request
from Common.operation_yaml import YamlHandle


class Const(object):

    def __init__(self):
        self.request = Request()
        self.access_token = YamlHandle().read_yaml('login.yaml')[0]['accessToken']
        self.headers = dict()
        self.headers['X-Dk-Token'] = self.access_token
