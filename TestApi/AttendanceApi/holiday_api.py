# coding:utf-8
# Name:holiday_api.py
# Author:qi.yu
# Time:2020/9/1 3:41 下午
# Description:

from TestApi.consts_api import Const


class HolidayApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取假期规则列表
    def get_holiday_plan_list(self):
        url = self.url_path + '/dukang-attendance/api/holiday/plan'
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res