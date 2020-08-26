# Name:LeaveApply.py
# Author:michelle.hou
# Time:2020-08-10 17:13

from TestApi.consts_api import Const


class LeaveFormApply(Const):
    def __init__(self, env):
        super().__init__(env)

    # 提交按天休假申请
    def send_leave_form(self, data):
        url = self.url_path + '/leave/leaveform'
        response = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return response

    #  提交按班次休假申请
    def send_leave_form_by_shift(self, data):
        url = self.url_path + '/leave/leaveform'
        response = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return response

    #  提交按小时休假申请
    def send_leave_form_by_hour(self, data):
        url = self.url_path + '/leave/leaveform'
        response = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return response
