# coding:utf-8
# Name:workflow_api.py
# Author:qi.yu
# Time:2020/9/3 4:44 下午
# Description:

from TestApi.consts_api import Const


class WorkflowApi(Const):

    def __init__(self, env):
        super().__init__(env)

    def get_workflow_approval(self, data):
        url = self.url_path + '/dukang-attendance/api/organizations/' + data['organization_id'] + '/workflow/approval'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
