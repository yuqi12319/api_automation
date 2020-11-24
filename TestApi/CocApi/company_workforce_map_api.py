# coding:utf-8
# Name:company_workforce_map_api.py
# Author:qi.yu
# Time:2020/8/18 11:07 上午
# Description:

from TestApi.consts_api import Const


class CompanyWorkforceMapApi(Const):

    def __init__(self, env):
        super().__init__(env)

    def workforce_company_map_api(self, data):
        url = self.url_path + '/dukang-coc/api/company/workforce/map'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 新增公司关联关系
    def workforce_company_workforce_add_api(self, data):
        url = self.url_path + '/dukang-coc/api/company/workforce/add'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res