# coding:utf-8
# Name:leave_info_api.py
# Author:qi.yu
# Time:2020/9/15 3:25 下午
# Description:

from TestApi.consts_api import Const


class LeaveInfoApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取员工休假记录
    def get_employee_leave_record_api(self, data):
        url = self.url_path + '/leave/employee_leave_records'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 获取员工假期额度
    def get_employee_leave_limit_api(self, data):
        url = self.url_path + '/leave/employee_leave_info'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
