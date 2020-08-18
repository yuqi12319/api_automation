# coding:utf-8
# Name:commission.py
# Author:qi.yu
# Time:2020/8/18 11:16 上午
# Description:

from TestApi.consts_api import Const


class Commission(Const):

    def __init__(self, env):
        super().__init__(env)

    def positions(self, data):
        url = self.url_path + '/dukang-commission/positions'
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res
