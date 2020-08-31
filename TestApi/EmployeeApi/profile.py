# coding:utf-8
# Name:profile.py
# Author:qi.yu
# Time:2020/8/28 2:16 下午
# Description:

from TestApi.consts_api import Const


class Profile(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取员工信息（证件信息）接口
    def get_employee_certificate_api(self, data):
        url = self.url_path + '/dukang-employee/employees/profile/bankcard/certificate/socialsecurityprovidentfund/photo'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 修改员工信息（证件信息）接口
    def update_employee_certificate_api(self, data):
        url = self.url_path + '/dukang-employee/employees/profile/bankcard/certificate/socialsecurityprovidentfund/photo'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res
