# coding:utf-8
# Name:workforce_receive.py
# Author:qi.yu
# Time:2020/8/24 11:43 上午
# Description:

from TestApi.consts_api import Const


class WorkforceRecevice(Const):

    def __init__(self, env):
        super().__init__(env)

    # 接收列表接口
    def recevice_list_api(self, data):
        url = self.url_path + '/dukang-workforce/api/receive/search'
        res = self.request.send_request_method('post', url=url, params=data['params'], headers=self.headers)
        return res

    # 接收详情接口
    def recevice_detail_api(self, data):
        url = self.url_path + '/dukang-workforce/api/receive/details'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 同意接收接口
    def agree_recevice_api(self, data):
        url = self.url_path + '/dukang-workforce/api/receive/confirm'
        res = self.request.send_request_method('put',url=url, json=data['body'], headers=self.headers)
        return res

    # 退回接收接口
    def refuse_recevice_api(self, data):
        url = self.url_path + '/dukang-workforce/api/receive/withdraw'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res
