# coding:utf-8
# Name:test_fixation_class_clock_module.py
# Author:qi.yu
# Time:2020/8/31 3:21 下午
# Description:固定班制打卡

import pytest, allure
from Common.log import MyLog
import Common.consts
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.MuscatApi.muscat import Muscat
from TestApi.AttendanceApi.attendance_group_api import AttendanceGroupApi
from TestApi.AttendanceApi.clock_api import ClockApi
from TestCase.TestScene import attendance


class TestFixationClassClock:

    @pytest.fixture(scope='class')
    def setup_class(self, env):
        company_id = str()
        employee_id = str()
        if Common.consts.COMPANY_INFORMATION:
            company_id = Common.consts.COMPANY_INFORMATION[0]['company_id']
            employee_id = Common.consts.COMPANY_INFORMATION[0]['employee_id']
        else:
            my_companies_res = Muscat(env).get_my_companies_api()
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
    @pytest.mark.parametrize('data', YamlHandle().read_yaml("SceneData/FixationClassClock/main_scene.yaml"))
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

            # 修改默认考勤组信息
            data['update_default_attendance_group']['body']['attendanceDeductionSettingDto'] = get_default_attendance_group_information_res.json()['data']['attendanceDeductionSettingVo']
            data['update_default_attendance_group']['body']['companyId'] = setup_class[1]
            data['update_default_attendance_group']['body']['employeeId'] = setup_class[2]
            data['update_default_attendance_group']['body']['employeeIds'].append(setup_class[2])
            data['update_default_attendance_group']['body']['holidayPlanId'] = get_holiday_plan_list['data'][1]['id']
            data['update_default_attendance_group']['body']['id'] = default_attendance_group_id
            data['update_default_attendance_group']['body']['overtimeId'] = get_overtime_rule_list['data'][1][
                'overtime_setting_id']
            data['update_default_attendance_group']['body']['pinCoordinateIds'].append(add_attendance_location_id)
            data['update_default_attendance_group']['body']['shiftPlan']['MONDAY'] = get_company_shift['data'][1]['id']
            data['update_default_attendance_group']['body']['shiftPlan']['TUESDAY'] = get_company_shift['data'][1]['id']
            data['update_default_attendance_group']['body']['shiftPlan']['WEDNESDAY'] = get_company_shift['data'][1][
                'id']
            data['update_default_attendance_group']['body']['shiftPlan']['THURSDAY'] = get_company_shift['data'][1][
                'id']
            data['update_default_attendance_group']['body']['shiftPlan']['FRIDAY'] = get_company_shift['data'][1]['id']
            data['update_default_attendance_group']['body']['shiftPlan']['SATURDAY'] = get_company_shift['data'][0][
                'id']
            data['update_default_attendance_group']['body']['shiftPlan']['SUNDAY'] = get_company_shift['data'][0]['id']
            update_attendance_group_res = AttendanceGroupApi(setup_class[0]).update_attendance_group(
                data['update_default_attendance_group'])
            Assertions().assert_text(update_attendance_group_res.json()['data'], str(default_attendance_group_id))

        with allure.step('第二步：打卡'):
            data['clock']['body']['employee_id'] = setup_class[2]
            clock_res = ClockApi(setup_class[0]).clock(data['clock'])
            Assertions().assert_mode(clock_res, data['clock'])

        with allure.step('第三步：查询员工当天上下班打卡记录'):
            data['get_employee_clock_record']['employee_id'] = setup_class[2]
            get_employee_clock_record_res = ClockApi(setup_class[0]).get_employee_clock_record(
                data['get_employee_clock_record'])
            if get_employee_clock_record_res.json()['data'][1]['time']:
                pass
            else:
                MyLog().error('下班打卡失败')

        with allure.step('第四步：删除打卡坐标信息'):
            data['delete_pincoordinate']['pin_coordinate_id'] = add_attendance_location_id
            data['delete_pincoordinate']['params']['attendance_group_id'] = default_attendance_group_id
            delete_pincoordinate_res = ClockApi(setup_class[0]).delete_pincoordinate(data['delete_pincoordinate'])
            Assertions().assert_mode(delete_pincoordinate_res, data['delete_pincoordinate'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_fixation_class_clock_module.py', '--env', 'test3'])
