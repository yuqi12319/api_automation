# coding:utf-8
# Name:scheduling_clock_api.py
# Author:qi.yu
# Time:2020/9/2 2:20 下午
# Description:

from TestApi.consts_api import Const

class SchedulingClockApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 员工上下班打卡（排班制）
    def scheduling_clock(self, data):
        url = self.url_path + '/dukang-attendance/api/scheduling/clock'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 员工当天上下班打卡记录（排班制）
    def scheduling_clock_list(self, data):
        url = self.url_path + '/dukang-attendance/api/scheduling/clockList'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
