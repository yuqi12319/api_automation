# coding:utf-8
# Name:clock_api.py
# Author:qi.yu
# Time:2020/9/1 4:21 下午
# Description:

from TestApi.consts_api import Const


class ClockApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 员工上下班打卡
    def clock(self, data):
        url = self.url_path + '/dukang-attendance/api/clock'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 查询员工当天上下班打卡记录
    def get_employee_clock_record(self, data):
        url = self.url_path + '/dukang-attendance/api/clockinout/' + data['employee_id']
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
