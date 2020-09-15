# coding:utf-8
# Name:leave_workflow_setting_api.py
# Author:qi.yu
# Time:2020/9/15 11:34 上午
# Description:

from TestApi.consts_api import Const


class LeaveWorkflowSettingApi(Const):
    def __init__(self, env):
        super().__init__(env)

    # 休假审批流列表信息查询接口
    def get_leave_approval_list_api(self, data):
        url = self.url_path + '/leave/leave_workflow_setting'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 添加修改休假审批流
    def post_leave_approval_api(self, data):
        url = self.url_path + '/leave/leave_workflow_setting'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 删除休假审批流
    def delete_leave_approval_api(self, data):
        url = self.url_path + '/leave/leave_workflow_setting'
        res = self.request.send_request_method('delete', url=url, json=data['body'], headers=self.headers)
        return res
