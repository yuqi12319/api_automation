# coding:utf-8
# Name:test_register_company_module.py
# Author:qi.yu
# Time:2020/8/21 3:54 下午
# Description:薪酬设置
from TestApi.consts_api import Const


class PayrollSetting(Const):
    def __init__(self, env):
        super().__init__(env)

    # 薪资项目列表
    def payroll_item_list_api(self, data):
        url = self.url_path + '/dukang-payroll/payrollItem/list'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
