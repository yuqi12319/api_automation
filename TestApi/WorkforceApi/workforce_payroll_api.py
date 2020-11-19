# coding:utf-8
# Name:workforce_payroll_api.py
# Author:qi.yu
# Time:2020/11/18 3:14 下午
# Description:

from TestApi.consts_api import Const


class WorkforcePayrollApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取用工更新申请员工待遇信息
    def get_update_employee_payroll_api(self, data):
        url = self.url_path + '/dukang-workforce/api/workforce_payroll/employee_payroll'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 新增用工待遇信息更新
    def post_update_employee_payroll_api(self, data):
        url = self.url_path + '/dukang-workforce/api/workforce_payroll/employee_payroll'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res