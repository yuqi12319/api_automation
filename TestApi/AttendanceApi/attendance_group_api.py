# coding:utf-8
# Name:attendance_group_api.py
# Author:qi.yu
# Time:2020/8/31 3:34 下午
# Description:

from TestApi.consts_api import Const


class AttendanceGroupApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取考勤组列表
    def get_attendance_group_list(self, data):
        url = self.url_path + '/dukang-attendance/api/attendancegroup/allInfo'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 获取考勤组信息(for web)
    def get_attendance_group_information(self, data):
        url = self.url_path + '/dukang-attendance/api/attendancegroup/' + data['attendancegroupId'] + '/forWeb'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 删除考勤组
    def del_attendance_group(self, data):
        url = self.url_path + '/dukang-attendance/api/attendancegroup/' + data['attendancegroup_id']
        res = self.request.send_request_method('delete', url=url, json=data['body'], headers=self.headers)
        return res

    # 新增考勤组
    def add_attendance_group(self, data):
        url = self.url_path + '/dukang-attendance/api/attendancegroup/forWeb'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 修改考勤组
    def update_attendance_group(self, data):
        url = self.url_path + '/dukang-attendance/api/attendancegroup/forWeb'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 获取加班规则列表
    def get_overtime_rule_list(self, data):
        url = self.url_path + '/dukang-attendance/api/overtime_settings/setup'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
