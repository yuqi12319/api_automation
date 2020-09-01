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

    # 查询公司下坐标打卡位置列表
    def get_pincoordinate_list(self, data):
        url = self.url_path + '/dukang-attendance/api/clock/pincoordinate'
        res = self.request.send_request_method('post', url=url, params=data['params'], headers=self.headers)
        return res

    # 添加坐标打卡位置信息
    def add_pincoordinate(self, data):
        url = self.url_path + '/dukang-attendance/api/clock/pincoordinate'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res
