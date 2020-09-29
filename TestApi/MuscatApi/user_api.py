# coding:utf-8
# Name:user_api.py
# Author:qi.yu
# Time:2020/9/29 5:00 下午
# Description:

from TestApi.consts_api import Const


class UserApi(Const):

    def __init__(self, env):
        super().__init__(env)

    def get_my_companies_api(self):
        url = self.url_path + '/muscat/my_companies_new'
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res
