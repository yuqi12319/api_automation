# coding:utf-8
# Name:labor_contract_parties.py
# Author:qi.yu
# Time:2020/8/28 10:54 上午
# Description:

from TestApi.consts_api import Const


class LaborContractParties(Const):

    def __init__(self, env):
        super().__init__(env)

    def add_laborcontractparties_api(self, data):
        url = self.url_path + '/dukang-employee/laborcontractparties'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    def get_laborcontractparties_api(self, data):
        url = self.url_path + '/dukang-employee/laborcontractparties'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
