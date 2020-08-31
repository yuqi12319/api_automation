# coding:utf-8
# Name:positon.py
# Author:qi.yu
# Time:2020/8/28 10:36 上午
# Description:

from TestApi.consts_api import Const


class Position(Const):

    def __init__(self, env):
        super().__init__(env)

    #
    def add_position_api(self, data):
        url = self.url_path + '/dukang-commission/position'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    def get_position_api(self, data):
        url = self.url_path + '/dukang-commission/positions'
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res
