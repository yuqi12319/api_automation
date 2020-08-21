# coding:utf-8
# Name:workforce_employee_domain.py
# Author:qi.yu
# Time:2020/8/19 2:19 下午
# Description:

from TestApi.consts_api import Const


class WorkforceEmployeeDomain(Const):

    def __init__(self, env):
        super().__init__(env)

    def workforce_employees_free(self, data):
        url = self.url_path + '/dukang-employee/api/workforce/employees/free'
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res
