5  # coding:utf-8
# Name:workforce_ticket.py
# Author:qi.yu
# Time:2020/7/16 5:22 下午
from TestApi.consts_api import Const


class WorkforceTicket(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取用工需求列表接口
    def get_require_list_api(self, data):
        url = self.url_path + "/dukang-workforce/api/workforce/require/form/ticket"
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 获取用工需求详情接口
    def get_require_detail_api(self, data):
        url = self.url_path + "/dukang-workforce/api/workforce/require/detail/" + str(data['id'])
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res
