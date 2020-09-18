# coding:utf-8
# Name:outgoing_form_api.py
# Author:qi.yu
# Time:2020/9/17 6:16 下午
# Description:

from TestApi.consts_api import Const

class OutgoingFormApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 发送外出流程申请
    def send_outgoing_apply_api(self, data):
        url = self.url_path + '/leave/outgoingform'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 取消外出流程申请
    def canceled_outgoing_apply_api(self, data):
        url = self.url_path + '/leave/outgoingform/' + data['outgoingFormId'] + '/canceled'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res