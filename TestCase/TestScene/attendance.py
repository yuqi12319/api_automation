# coding:utf-8
# Name:attendance.py.py
# Author:qi.yu
# Time:2020/9/14 10:29 上午
# Description:

import random

from Common.log import MyLog
from Common.operation_assert import Assertions

from TestApi.AttendanceApi.attendance_group_api import AttendanceGroupApi
from TestApi.AttendanceApi.clock_api import ClockApi
from TestApi.AttendanceApi.holiday_api import HolidayApi
from TestApi.AttendanceApi.shift_api import ShiftApi


def get_attendance_group_list(env, company_id, employee_id):
    data = dict()
    data['params'] = dict()
    data['params']['company_id'] = company_id
    data['params']['employeeId'] = employee_id
    data['params']['limit'] = 10
    data['params']['offset'] = 0
    get_attendance_group_list_res = AttendanceGroupApi(env).get_attendance_group_list(data)
    Assertions().assert_code(get_attendance_group_list_res.status_code, 200)
    Assertions().assert_text(get_attendance_group_list_res.json()['errcode'], '0')
    return get_attendance_group_list_res.json()


# 添加考勤地点
def add_attendance_location(env, company_id):
    data = dict()
    data['body'] = dict()
    data['body']['address_detail'] = '延安中路841号'
    data['body']['address_name'] = '东方海外大厦'
    data['body']['company_id'] = company_id
    data['body']['distance'] = '300'
    data['body']['latitude'] = 31.22336
    data['body']['longitude'] = 121.45441
    data['body']['shortName'] = random.randint(100, 999)
    add_attendance_location_res = ClockApi(env).add_pincoordinate(data)
    Assertions().assert_code(add_attendance_location_res.status_code, 200)
    Assertions().assert_text(add_attendance_location_res.json()['errcode'], '0')
    if add_attendance_location_res.json()['data']['pin_coordinate_id']:
        MyLog().info('考勤地点添加成功')
    else:
        MyLog().error('考勤地点添加失败')
    return add_attendance_location_res.json()


def get_company_shift(env, company_id, attendance_group_id):
    data = dict()
    data['params'] = dict()
    data['params']['company_id'] = company_id
    data['params']['attendanceId'] = attendance_group_id
    get_company_shift_res = ShiftApi(env).get_company_shift(data)
    Assertions().assert_code(get_company_shift_res.status_code, 200)
    Assertions().assert_text(get_company_shift_res.json()['errcode'], '0')
    return get_company_shift_res.json()


def get_overtime_rule_list(env, company_id):
    data = dict()
    data['params'] = dict()
    data['params']['company_id'] = company_id
    get_overtime_rule_list_res = AttendanceGroupApi(env).get_overtime_rule_list(data)
    Assertions().assert_code(get_overtime_rule_list_res.status_code, 200)
    Assertions().assert_text(get_overtime_rule_list_res.json()['errcode'], '0')
    return get_overtime_rule_list_res.json()


def get_holiday_plan_list(env):
    get_holiday_plan_list_res = HolidayApi(env).get_holiday_plan_list()
    Assertions().assert_code(get_holiday_plan_list_res.status_code, 200)
    Assertions().assert_text(get_holiday_plan_list_res.json()['errcode'], '0')
    return get_holiday_plan_list_res.json()
