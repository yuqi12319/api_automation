# coding:utf-8
# Name:WorkforceRegister.py
# Author:qi.yu
# Time:2020/8/18 6:10 下午
# Description:

from TestApi.consts_api import Const


class WorkforceRegister(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取登记列表
    def get_register_list_api(self, data):
        url = self.url_path + '/dukang-workforce/api/information/search'
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'], headers=self.headers)
        return res

    # 获取登记详情
    def get_register_detail_api(self, data):
        url = self.url_path + '/dukang-workforce/api/information/details'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 提交登记
    def commit_register_api(self, data):
        url = self.url_path + '/dukang-workforce/api/information/add'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res