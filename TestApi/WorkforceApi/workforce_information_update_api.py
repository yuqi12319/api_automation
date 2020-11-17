# coding:utf-8
# Name:workforce_information_update_api.py
# Author:qi.yu
# Time:2020/11/5 11:28 上午
# Description:

from TestApi.consts_api import Const

class WorkforceInformationUpdateApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 用工信息更新申请员工基本信息
    def get_update_employee_basic_api(self, data):
        url = self.url_path + '/dukang-workforce/api/workforce_update_records/employee_basic'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 新增用工基础信息更新
    def post_update_employee_basic_api(self, data):
        url = self.url_path + '/dukang-workforce/api/workforce_update_records/employee_basic'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 用工信息更新记录查询
    def get_workforce_update_list_api(self, data):
        url = self.url_path + '/dukang-workforce/api/workforce_update_records/search'
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'], headers=self.headers)
        return res

    # 用工基础信息更新详情
    def get_workforce_update_detail_api(self, data):
        url = self.url_path + '/dukang-workforce/api/workforce_update_records/employee_basic_detail'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res