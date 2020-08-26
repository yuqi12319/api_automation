# coding:utf-8
# Name:token.py
# Author:qi.yu
# Time:2020/8/26 3:25 下午
# Description:

from TestApi.consts_api import Const

class Token(Const):

    def __init__(self, env):
        super().__init__(env)

    def login(self, data):
        url = self.url_path + '/dukang-user/login'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res