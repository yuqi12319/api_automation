# coding:utf-8
# Name:bubble.py
# Author:qi.yu
# Time:2020/8/26 5:18 下午
# Description: 气泡

from TestApi.consts_api import Const


class Bubble(Const):

    def __init__(self, env):
        super().__init__(env)

    def get_web_bubbles(self, data):
        url = self.url_path + '/dukang-attendance/bubbles'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

