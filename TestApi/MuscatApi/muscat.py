# coding:utf-8
# Name:muscat.py
# Author:qi.yu
# Time:2020/8/3 11:33 上午
# Description:

from TestApi.consts_api import Const


class Muscat(Const):
    def __init__(self, env):
        super().__init__(env)

    def get_my_companies_api(self):
        url = self.url_path + '/muscat/my_companies'
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res

    def company_guide_employeeid(self, data):
        url = self.url_path + '/muscat/company/guide/employeeid'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    def organizations(self, data):
        url = self.url_path + '/muscat/organizations/' + str(data['employeeid']) + '/trees'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res