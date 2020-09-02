# coding:utf-8
# Name:shift_scheduling_api.py
# Author:qi.yu
# Time:2020/9/2 11:44 上午
# Description:

from TestApi.consts_api import Const


class ShiftSchedulingApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 添加和更新排班
    def add_and_update_shiftschedulingdraft(self, data):
        url = self.url_path + '/dukang-attendance/api/shiftschedulingdraft'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 发布排班
    def release_scheduling(self, data):
        url = self.url_path + '/dukang-attendance/api/shiftscheduling/release/' + data['attendanceGroupId']
        res = self.request.send_request_method('post', url=url, headers=self.headers)
        return res
