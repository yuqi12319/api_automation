# coding:utf-8
# Name:test_schedule_class_clock_module.py
# Author:qi.yu
# Time:2020/9/1 6:21 下午
# Description:排班制打卡

import pytest, allure
import time, datetime
from Common.log import MyLog
import Common.consts
import random
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.AttendanceApi.attendance_group_api import AttendanceGroupApi
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.AttendanceApi.shift_scheduling_api import ShiftSchedulingApi
from TestApi.AttendanceApi.scheduling_clock_api import SchedulingClockApi
from TestApi.AttendanceApi.clock_api import ClockApi
from TestApi.MuscatApi.user_api import UserApi
from TestCase.TestScene import attendance


class TestScheduleClassClock:

    @pytest.fixture(autouse=True)
    def setup_class(self, env):
        company_id = str()
        employee_id = str()
        if Common.consts.COMPANY_INFORMATION:
            company_id = Common.consts.COMPANY_INFORMATION['company_id']
            employee_id = Common.consts.COMPANY_INFORMATION['employee_id']
        else:
            my_companies_res = UserApi(env).get_my_companies_api()
            if my_companies_res.json()['data']:
                company_id = my_companies_res.json()['data'][0]['company_id']
                brief_profile_data = YamlHandle().read_yaml('SingleInterfaceData/Employee/brief_profile.yaml')[0]
                brief_profile_data['params']['company_id'] = company_id
                brief_profile_res = EmployeeApi(env).brief_profile_api(brief_profile_data)
                employee_id = brief_profile_res.json()['data']['employee_id']
            else:
                MyLog().error('当前用户下没有公司列表')
        return env, company_id, employee_id

    @pytest.mark.smoke
    @pytest.mark.run(order=6)
    @pytest.mark.parametrize('data', YamlHandle().read_yaml("SceneData/ScheduleClassClock/main_scene.yaml"))
    def test_main_scene(self, data, setup_class):
        with allure.step('第一步：考勤组设置'):
            # 获取考勤组列表
            get_attendance_group_list = attendance.get_attendance_group_list(setup_class[0], setup_class[1],
                                                                             setup_class[2])
            Assertions().assert_in_text(get_attendance_group_list['data'], "默认考勤组")
            default_attendance_group_id = get_attendance_group_list['data'][0]['attendanceGroupId']

            # 添加考勤地点
            add_attendance_location = attendance.add_attendance_location(setup_class[0], setup_class[1])
            add_attendance_location_id = add_attendance_location['data']['pin_coordinate_id']

            # 查询公司班次列表
            get_company_shift = attendance.get_company_shift(setup_class[0], setup_class[1],
                                                             default_attendance_group_id)

            # 获取加班规则列表
            get_overtime_rule_list = attendance.get_overtime_rule_list(setup_class[0], setup_class[1])

            # 获取假期规则列表
            get_holiday_plan_list = attendance.get_holiday_plan_list(setup_class[0])

            # 获取默认考勤组详情
            data['get_default_attendance_group_information']['attendancegroupId'] = default_attendance_group_id
            data['get_default_attendance_group_information']['params'][
                'attendancegroupId'] = default_attendance_group_id
            get_default_attendance_group_information_res = AttendanceGroupApi(
                setup_class[0]).get_attendance_group_information(data['get_default_attendance_group_information'])
            Assertions().assert_mode(get_default_attendance_group_information_res,
                                     data['get_default_attendance_group_information'])

            # 将默认考勤组修改为排班制考勤组
            data['update_default_attendance_group']['body']['attendanceDeductionSettingDto'] = \
            get_default_attendance_group_information_res.json()['data']['attendanceDeductionSettingVo']
            data['update_default_attendance_group']['body']['companyId'] = setup_class[1]
            data['update_default_attendance_group']['body']['employeeId'] = setup_class[2]
            data['update_default_attendance_group']['body']['employeeIds'].append(setup_class[2])
            data['update_default_attendance_group']['body']['holidayPlanId'] = get_holiday_plan_list['data'][1]['id']
            data['update_default_attendance_group']['body']['id'] = default_attendance_group_id
            data['update_default_attendance_group']['body']['overtimeId'] = get_overtime_rule_list['data'][0][
                'overtime_setting_id']
            data['update_default_attendance_group']['body']['pinCoordinateIds'].append(add_attendance_location_id)
            data['update_default_attendance_group']['body']['schedulingShiftIdList'].append(get_company_shift['data'][1]['id'])
            update_attendance_group_res = AttendanceGroupApi(setup_class[0]).update_attendance_group(
                data['update_default_attendance_group'])
            Assertions().assert_text(update_attendance_group_res.json()['data'], str(default_attendance_group_id))

        with allure.step('第二步：排班'):
            # 排班
            data['add_and_update_shiftschedulingdraft']['body']['employeeShiftSchedulingDraftDtoList'][0][
                'attendanceGroupId'] = default_attendance_group_id
            data['add_and_update_shiftschedulingdraft']['body']['employeeShiftSchedulingDraftDtoList'][0][
                'employeeId'] = setup_class[2]
            data['add_and_update_shiftschedulingdraft']['body']['employeeShiftSchedulingDraftDtoList'][0][
                'shiftSchedulingDate'] = round(int(time.mktime(datetime.date.today().timetuple())) * 1000)
            data['add_and_update_shiftschedulingdraft']['body']['employeeShiftSchedulingDraftDtoList'][0][
                'shiftSchedulingDraftDtoList'][0]['offWorkPinCoordinateIdList'].append(add_attendance_location_id)
            data['add_and_update_shiftschedulingdraft']['body']['employeeShiftSchedulingDraftDtoList'][0][
                'shiftSchedulingDraftDtoList'][0]['toWorkPinCoordinateIdList'].append(add_attendance_location_id)
            data['add_and_update_shiftschedulingdraft']['body']['employeeShiftSchedulingDraftDtoList'][0][
                'shiftSchedulingDraftDtoList'][0]['shiftId'] = get_company_shift['data'][1]['id']
            add_and_update_shiftschedulingdraft_res = ShiftSchedulingApi(setup_class[0]).add_and_update_shiftschedulingdraft(
                data['add_and_update_shiftschedulingdraft'])
            Assertions().assert_mode(add_and_update_shiftschedulingdraft_res,
                                     data['add_and_update_shiftschedulingdraft'])

            # 发布排班
            data['release_scheduling']['attendanceGroupId'] = default_attendance_group_id
            release_scheduling_res = ShiftSchedulingApi(setup_class[0]).release_scheduling(data['release_scheduling'])
            Assertions().assert_mode(release_scheduling_res, data['release_scheduling'])

        with allure.step('第三步：打卡'):
            data['scheduling_clock']['body']['employeeId'] = setup_class[2]
            data['scheduling_clock']['body']['attendanceGroupId'] = default_attendance_group_id
            data['scheduling_clock']['body']['shiftId'] = get_company_shift['data'][1]['id']
            scheduling_clock_res = SchedulingClockApi(setup_class[0]).scheduling_clock(data['scheduling_clock'])
            Assertions().assert_mode(scheduling_clock_res, data['scheduling_clock'])

        with allure.step('第四步：查询员工当天上下班打卡记录'):
            data['scheduling_clock_list']['params']['employeeId'] = setup_class[2]
            scheduling_clock_list_res = SchedulingClockApi(setup_class[0]).scheduling_clock_list(
                data['scheduling_clock_list'])
            if scheduling_clock_list_res.json()['data']['schedulingClockList'][0]['clockOutRecord']['clockTime']:
                pass
            else:
                MyLog().error('排班制打卡失败')

        with allure.step('第五步：删除删除打卡坐标信息'):
            data['delete_pincoordinate']['pin_coordinate_id'] = add_attendance_location_id
            data['delete_pincoordinate']['params']['attendance_group_id'] = default_attendance_group_id
            delete_pincoordinate_res = ClockApi(setup_class[0]).delete_pincoordinate(data['delete_pincoordinate'])
            Assertions().assert_mode(delete_pincoordinate_res, data['delete_pincoordinate'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_schedule_class_clock_module.py', '--env', 'test3'])
