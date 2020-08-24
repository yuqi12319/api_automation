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

    # 获取flow_id接口
    def get_flow_id(self):
        url = self.url_path + '/muscat/get_flow_id'
        res = self.request.send_request_method('get', url=url)
        return res

    # 发送验证码接口
    def vcode_api(self, data):
        url = self.url_path + '/muscat/sms/vcode'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=data['headers'])
        print(res)
        return res

    # 校验验证码接口
    def vcode_check_api(self, data):
        url = self.url_path + '/muscat/sms/vcode_check'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=data['headers'])
        return res

    # 注册公司接口
    def register_comapny_api(self, data):
        url = self.url_path + '/muscat/companies/registration/second'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=data['headers'])
        return res

    # 解散公司
    def dissolve_company(self, data):
        url = self.url_path + '/muscat/companies/' + str(data['companyId']) + '/dissolvation'
        res = self.request.send_request_method('post', url=url, headers=self.headers)
        return res
