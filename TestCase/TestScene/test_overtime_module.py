# coding:utf-8
# Name:test_overtime_module.py
# Author:qi.yu
# Time:2020/9/3 11:13 上午
# Description:加班

import pytest, allure
from Common import log
import random
import Common.consts
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.AttendanceApi.attendance_group_api import AttendanceGroupApi
from TestApi.AttendanceApi.clock_api import ClockApi
from TestApi.AttendanceApi.holiday_api import HolidayApi
from TestApi.AttendanceApi.shift_api import ShiftApi
from TestApi.EmployeeApi.employee import Employee
from TestApi.MuscatApi.muscat import Muscat


class TestOvertime:

    @pytest.fixture(autouse=True)
    def precondition(self, env):
        self.env = env
        self.log = log.MyLog()
        if Common.consts.COMPANY_INFORMATION:
            company_id = Common.consts.COMPANY_INFORMATION[0]['company_id']
            employee_id = Common.consts.COMPANY_INFORMATION[0]['employee_id']
        else:
            my_companies_res = Muscat(self.env).get_my_companies_api()
            if my_companies_res.json()['data']:
                company_id = my_companies_res.json()['data'][0]['company_id']
                brief_profile_data = YamlHandle().read_yaml('SingleInterfaceData/Employee/brief_profile.yaml')[0]
                brief_profile_data['params']['company_id'] = company_id
                brief_profile_res = Employee(self.env).brief_profile_api(brief_profile_data)
                employee_id = brief_profile_res.json()['data']['employee_id']
            else:
                self.log.error('当前用户下没有公司列表')
        self.company_id = company_id
        self.employee_id = employee_id

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/Overtime/main_scene.yaml'))
    def test_main_scene(self, data):
        with allure.step('第一步：考勤组设置'):
            # 添加考勤地点
            data['add_pincoordinate']['body']['company_id'] = self.company_id
            data['add_pincoordinate']['body']['shortName'] = random.randint(1000, 9999)
            add_pincoordinate_res = ClockApi(self.env).add_pincoordinate(data['add_pincoordinate'])
            Assertions().assert_mode(add_pincoordinate_res, data['add_pincoordinate'])
            if add_pincoordinate_res.json()['data']['pin_coordinate_id']:
                pin_coordinate_id = add_pincoordinate_res.json()['data']['pin_coordinate_id']
            else:
                self.log.error('考勤地点添加失败')

            # 查询公司班次列表
            data['get_company_shift']['params']['company_id'] = self.company_id
            get_company_shift_res = ShiftApi(self.env).get_company_shift(data['get_company_shift'])
            Assertions().assert_mode(get_company_shift_res, data['get_company_shift'])

            # 获取加班规则列表
            data['get_overtime_rule_list']['params']['company_id'] = self.company_id
            get_overtime_rule_list_res = AttendanceGroupApi(self.env).get_overtime_rule_list(
                data['get_overtime_rule_list'])
            Assertions().assert_mode(get_overtime_rule_list_res, data['get_overtime_rule_list'])

            # 获取假期规则列表
            get_holiday_plan_list_res = HolidayApi(self.env).get_holiday_plan_list()
            Assertions().assert_mode(get_holiday_plan_list_res, data['get_holiday_plan_list'])

            # 添加排班制考勤组
            data['add_schedule_class_attendance_group']['body']['companyId'] = self.company_id
            data['add_schedule_class_attendance_group']['body']['employeeId'] = self.employee_id
            data['add_schedule_class_attendance_group']['body']['employeeIds'].append(self.employee_id)
            data['add_schedule_class_attendance_group']['body']['holidayPlanId'] = get_holiday_plan_list_res.json()['data'][1]['id']
            data['add_schedule_class_attendance_group']['body']['overtimeId'] = get_overtime_rule_list_res.json()['data'][0]['overtime_setting_id']
            data['add_schedule_class_attendance_group']['body']['pinCoordinateIds'].append(pin_coordinate_id)
            new_shift = []
            for item in get_company_shift_res.json()['data']:
                generator_id = ShiftApi(self.env).get_id_generator().json()['data']
                item['id'] = generator_id
                item['shiftId'] = generator_id
                item['employeeId'] = self.employee_id
                new_shift.append(item)
            data['add_schedule_class_attendance_group']['body']['shiftDtos'] = new_shift
            data['add_schedule_class_attendance_group']['body']['schedulingShiftIdList'].append(new_shift[1]['id'])
            add_schedule_class_attendance_group_res = AttendanceGroupApi(self.env).add_attendance_group(
                data['add_schedule_class_attendance_group'])
            Assertions().assert_mode(add_schedule_class_attendance_group_res,
                                     data['add_schedule_class_attendance_group'])
            schedule_class_attendance_group_id = add_schedule_class_attendance_group_res.json()['data']

        with allure.step('第二步：加班申请'):
            pass