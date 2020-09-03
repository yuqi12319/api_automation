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

    # 删除坐标打卡位置信息
    def delete_pincoordinate(self, data):
        url = self.url_path + '/dukang-attendance/api/clock/pincoordinate/' + data['pin_coordinate_id']
        res = self.request.send_request_method('delete', url=url, params=data['params'], headers=self.headers)
        return res
