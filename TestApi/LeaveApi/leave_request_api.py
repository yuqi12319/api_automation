# coding:utf-8
# Name:leave_request_api.py
# Author:qi.yu
# Time:2020/9/14 3:22 下午
# Description:
from TestApi.consts_api import Const


class LeaveRequestApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 提交请假申请
    def apply_leave(self, data):
        url = self.url_path + '/leave/leaveform'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 根据ID获取休假form信息
    def get_leave_information(self, data):
        url = self.url_path + '/leave/leaveform/' + data['leaveFormId']
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 通过employeeid和processinstanceid完成任务（同意，拒绝）
    def leave_approval_result(self, data):
        url = self.url_path + '/leave/task/complete'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 取消休假流程申请
    def canceled_leave_apply(self, data):
        url = self.url_path + '/leave/leaveform/' + str(data['leaveFormId']) + '/canceled'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res
