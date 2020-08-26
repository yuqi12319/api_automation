# coding:utf-8
# Name:employee.py
# Author:qi.yu
# Time:2020/8/26 5:46 下午
# Description:

from TestApi.consts_api import Const

class Employee(Const):

    def __init__(self, env):
        super().__init__(env)

    def brief_proile_api(self, data):
        url = self.url_path + '/dukang-employee/employees/brief_profile'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res