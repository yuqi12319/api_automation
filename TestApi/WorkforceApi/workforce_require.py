5# coding:utf-8
# Name:workforce_require.py
# Author:qi.yu
# Time:2020/7/16 5:22 下午
from TestApi.consts_api import Const


class WorkforceRequire(Const):

    def __init__(self):
        super().__init__()

    # 获取用工需求列表接口
    def require_list_api(self, url_path, data):
        url = url_path + data['url']
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 获取用工需求详情接口
    def require_detail_api(self, url_path, data):
        url = url_path + data['url'] +str (data['applicationId'])
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res
