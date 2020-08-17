# coding:utf-8
# Name:muscat.py
# Author:qi.yu
# Time:2020/8/3 11:33 上午
# Description:

from TestApi.consts_api import Const


class Muscat(Const):
    def __init__(self, env):
        super().__init__(env)

    def get_my_companies_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res
