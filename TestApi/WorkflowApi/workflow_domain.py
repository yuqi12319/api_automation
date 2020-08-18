# coding:utf-8
# Name:workflow_domain.py
# Author:qi.yu
# Time:2020/8/18 6:24 下午
# Description:

from TestApi.consts_api import Const


class WorkflowDomain(Const):
    def __init__(self, env):
        super().__init__(env)

    # 节点审批(同意，拒绝)
    def workflow_node_approve_api(self, data):
        url = self.url_path + '/dukang-workflow/api/task/complete'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 批量节点审批(同意，拒绝)
    def workflow_batch_node_approve_api(self, data):
        url = self.url_path + '/dukang-workflow/api/task/batchcomplete'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 根据组织架构节点获取对应审批流
    def workflow_approval_query(self, data):
        url = self.url_path + '/dukang-workflow/api/organizations/' + data[
            'organizationId'] + "/workflow/approval/query"
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res
