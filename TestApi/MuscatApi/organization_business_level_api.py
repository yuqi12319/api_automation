# coding:utf-8
# Name:organization_business_level_api.py
# Author:qi.yu
# Time:2020/10/27 9:55 上午
# Description:

from TestApi.consts_api import Const


class OrganizationBusinessLevelApi(Const):

    def __init__(self, env):
        super().__init__(env)

    def get_organization_business_level_api(self, data):
        url = self.url_path + '/muscat/organization_business_level'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
