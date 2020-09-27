# coding:utf-8
# Name:workflow_set_api.py
# Author:qi.yu
# Time:2020/9/23 11:20 上午
# Description:

from TestApi.consts_api import Const


class WorkflowSetApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 审批流列表信息查询
    def get_approval_list_api(self, data):
        url = self.url_path + '/dukang-workflow/api/workflow_setting/list'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 编辑审批流信息
    def update_approval(self, data):
        url = self.url_path + '/dukang-workflow/api/workflow_setting'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res
