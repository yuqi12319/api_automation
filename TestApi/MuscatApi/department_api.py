# coding:utf-8
# Name:department_api.py
# Author:qi.yu
# Time:2020/10/26 4:15 下午
# Description:

from TestApi.consts_api import Const


class DepartmentApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 新增一个部门
    def add_department_api(self, data):
        url = self.url_path + '/muscat/departments'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res
