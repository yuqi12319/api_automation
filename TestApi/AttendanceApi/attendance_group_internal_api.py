# coding:utf-8
# Name:attendance_group_internal_api.py
# Author:qi.yu
# Time:2020/8/31 3:42 下午
# Description:

from TestApi.consts_api import Const


class AttendanceGroupInternalApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 新增考勤组
    def add_attendance_group(self, data):
        url = self.url_path + '/dukang-attendance/intapi/attendancegroup/forweb'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 修改考勤组
    def update_attendance_group(self, data):
        url = self.url_path + '/dukang-attendance/intapi/attendancegroup/forweb'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

