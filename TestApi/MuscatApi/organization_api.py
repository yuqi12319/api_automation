# coding:utf-8
# Name:organization_api.py
# Author:qi.yu
# Time:2020/10/26 6:35 下午
# Description:

from TestApi.consts_api import Const


class OrganizationApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取部门tree
    def get_organizations_tree_api(self, data):
        url = self.url_path + '/muscat/organizations/' + data['organization_id'] + '/tree'
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res

    # 获取公司组织架构
    def get_organization_chart_api(self, data):
        url = self.url_path + '/muscat/organizations/' + data['organization_id'] + '/chart'
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res