# coding:utf-8
# Name:workforce_apply.py
# Author:qi.yu
# Time:2020/7/16 10:31 上午
from TestApi.consts_api import Const


class WorkforceApply(Const):

    def __init__(self):
        super().__init__()

    # 提交用工申请接口
    def send_apply_api(self, url_path, data):
        url = url_path + data['url']
        res = self.request.send_request_method(method='post', url=url, json=data['body'], headers=self.headers)
        return res

    # 获取用工申请列表接口
    def apply_list_api(self, url_path, data):
        url = url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'], headers=self.headers)
        return res

    # 获取用工申请详情接口
    def apply_detail_api(self, url_path, data):
        url = url_path + data['url'] + str(data['application_id'])
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res

    # 停止申请接口
    def stop_apply_api(self, url_path, data):
        url = url_path + data['url'] + str(data['application_id'])
        res = self.request.send_request_method('put', url=url, headers=self.headers)
        return res
