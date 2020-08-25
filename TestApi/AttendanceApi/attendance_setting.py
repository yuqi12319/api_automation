# coding:utf-8
# Name:attendance_setting.py
# Author:qi.yu
# Time:2020/8/25 4:16 下午
# Description: 考勤组设置

from TestApi.consts_api import Const

class AttendanceSetting(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取考勤组列表接口
    def get_attendance_group_api(self, data):
        url = self.url_path + '/dukang-attendance/api/attendancegroup/allInfo'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res