# coding:utf-8
# Name:api_thirdparty.py
# Author:qi.yu
# Time:2020/7/10 3:26 下午
from TestApi.consts_api import Const


class ThirdParty(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取access_token接口
    def get_access_token_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('post', url=url, json=data['body'])
        return res

    # 刷新access_token
    def refresh_open_token_api(self, data, access_token):
        body = data['body']
        body.update({'refreshOpenToken': access_token})
        res = self.request.send_request_method('post', data['url'], body)
        return res

    # 注册公司
    def regist_company_api(self, data, access_token):
        url = data['url'] + '?x-open-token=' + access_token
        res = self.request.send_request_method('post', url, data['body'])
        return res
