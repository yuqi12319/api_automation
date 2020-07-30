# coding:utf-8
# Name:workforce_dispatch.py
# Author:qi.yu
# Time:2020/7/22 2:16 下午

from TestApi.consts_api import Const


class WorkforceDispatch(Const):

    def __init__(self):
        super().__init__()

    # 劳务工派遣接口
    def dispatch_api(self, url_path, data):
        url = url_path + data['url']
        res = self.request.send_request_method('post',url=url, json=data['body'], headers=self.headers)
        return res

    # 获取劳务工派遣列表接口
    def dispatch_list_api(self, url_path, data):
        url = url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], headers=self.headers)
        return res

    # 获取劳务工派遣详情接口
    def dispatch_detail_api(self, url_path, data):
        url = url_path + data['url']
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 关联申请查询
    def relevance_apply_api(self, url_path, data):
        url = url_path + data['url']
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
