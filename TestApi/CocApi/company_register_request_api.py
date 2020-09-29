# coding:utf-8
# Name:company_register_request_api.py
# Author:qi.yu
# Time:2020/9/29 4:16 下午
# Description:

from TestApi.consts_api import Const

class CompanyRegisterRequestApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 添加公司注册信息
    def add_company_register_api(self, data):
        url = self.url_path + '/dukang-coc/company_register_request'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 注册公司审批
    def company_register_approval_api(self, data):
        url = self.url_path + '/dukang-coc/company_register_request/approval'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res