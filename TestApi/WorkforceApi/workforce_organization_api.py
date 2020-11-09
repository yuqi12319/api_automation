# coding:utf-8
# Name:workforce_organization_api.py
# Author:qi.yu
# Time:2020/11/5 11:17 上午
# Description:

from TestApi.consts_api import Const


class WorkforceOrganizationApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 用工信息更新申请更新组织架构
    def get_update_workforce_organization_api(self, data):
        url = self.url_path + '/dukang-workforce/api/workforce_organization/organization_tree'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res