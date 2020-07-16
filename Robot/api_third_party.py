# coding:utf-8
# Name:api_third_party.py
# Author:qi.yu
# Time:2020/7/10 3:26 下午
from Common.request import Request


class ThirdParty:

    def __init__(self):
        self.request = Request()

    # 获取access_token
    def access_open_token_api(self, url, data):
        res = self.request.send_request_method('post', url, data)
        return res

    # 刷新access_token
    def refresh_open_token_api(self, url, data):
        res = self.request.send_request_method('post', url, data)
        return res

    # 注册公司
    def regist_company_api(self, url, data):
        res = self.request.send_request_method('post', url, data)
        return res
