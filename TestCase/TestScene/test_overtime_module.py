# coding:utf-8
# Name:test_overtime_module.py
# Author:qi.yu
# Time:2020/9/3 11:13 上午
# Description:加班

import pytest, allure
import time,datetime
from Common import log
import random
import Common.consts
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.AttendanceApi.attendance_group_api import AttendanceGroupApi
from TestApi.AttendanceApi.clock_api import ClockApi
from TestApi.AttendanceApi.holiday_api import HolidayApi
from TestApi.AttendanceApi.shift_api import ShiftApi
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.MuscatApi.muscat import Muscat
from TestApi.AttendanceApi.overtime_api import OvertimeApi
from TestApi.AttendanceApi.workflow_api import WorkflowApi


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
                brief_profile_res = EmployeeApi(self.env).brief_profile_api(brief_profile_data)
                employee_id = brief_profile_res.json()['data']['employee_id']
            else:
                self.log.error('当前用户下没有公司列表')
        self.company_id = company_id
        self.employee_id = employee_id

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/Overtime/main_scene.yaml'))
    def test_main_scene(self, data):
        '''
        with allure.step('第一步：考勤组设置'):
            # 获取考勤组列表
            data['get_attendance_group_list']['params']['company_id'] = self.company_id
            data['get_attendance_group_list']['params']['employeeId'] = self.employee_id
            get_attendance_group_list_res = AttendanceGroupApi(self.env).get_attendance_group_list(
                data['get_attendance_group_list'])
            Assertions().assert_in_text(get_attendance_group_list_res.json()['data'], "默认考勤组")
            default_attendance_group_id = get_attendance_group_list_res.json()['data'][0]['attendanceGroupId']

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
            data['get_company_shift']['params']['attendanceId'] = default_attendance_group_id
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

            # 获取默认考勤组详情
            data['get_default_attendance_group_information']['attendancegroupId'] = default_attendance_group_id
            data['get_default_attendance_group_information']['params'][
                'attendancegroupId'] = default_attendance_group_id
            get_default_attendance_group_information_res = AttendanceGroupApi(
                self.env).get_attendance_group_information(data['get_default_attendance_group_information'])
            Assertions().assert_mode(get_default_attendance_group_information_res,
                                     data['get_default_attendance_group_information'])

            # 修改默认考勤组信息，将admin用户剔除默认考勤组
            data['update_default_attendance_group']['body']['attendanceDeductionSettingDto'] = get_default_attendance_group_information_res.json()['data']['attendanceDeductionSettingVo']
            data['update_default_attendance_group']['body']['companyId'] = self.company_id
            data['update_default_attendance_group']['body']['employeeId'] = self.employee_id
            data['update_default_attendance_group']['body']['holidayPlanId'] = get_holiday_plan_list_res.json()['data'][1]['id']
            data['update_default_attendance_group']['body']['id'] = default_attendance_group_id
            data['update_default_attendance_group']['body']['overtimeId'] = get_overtime_rule_list_res.json()['data'][1]['overtime_setting_id']
            data['update_default_attendance_group']['body']['shiftPlan']['MONDAY'] = get_company_shift_res.json()['data'][1]['id']
            data['update_default_attendance_group']['body']['shiftPlan']['TUESDAY'] = get_company_shift_res.json()['data'][1]['id']
            data['update_default_attendance_group']['body']['shiftPlan']['WEDNESDAY'] = get_company_shift_res.json()['data'][1]['id']
            data['update_default_attendance_group']['body']['shiftPlan']['THURSDAY'] = get_company_shift_res.json()['data'][1]['id']
            data['update_default_attendance_group']['body']['shiftPlan']['FRIDAY'] = get_company_shift_res.json()['data'][1]['id']
            data['update_default_attendance_group']['body']['shiftPlan']['SATURDAY'] = get_company_shift_res.json()['data'][0]['id']
            data['update_default_attendance_group']['body']['shiftPlan']['SUNDAY'] = get_company_shift_res.json()['data'][0]['id']
            update_attendance_group_res = AttendanceGroupApi(self.env).update_attendance_group(
                data['update_default_attendance_group'])
            Assertions().assert_text(update_attendance_group_res.json()['data'], str(default_attendance_group_id))

            # 新增固定班考勤组
            data['add_fixation_class_attendance_group']['body']['companyId'] = self.company_id
            data['add_fixation_class_attendance_group']['body']['employeeId'] = self.employee_id
            data['add_fixation_class_attendance_group']['body']['employeeIds'].append(self.employee_id)
            data['add_fixation_class_attendance_group']['body']['holidayPlanId'] = get_holiday_plan_list_res.json()['data'][1]['id']
            data['add_fixation_class_attendance_group']['body']['overtimeId'] = get_overtime_rule_list_res.json()['data'][0]['overtime_setting_id']
            data['add_fixation_class_attendance_group']['body']['pinCoordinateIds'].append(pin_coordinate_id)
            new_shift = []
            for item in get_company_shift_res.json()['data']:
                generator_id = ShiftApi(self.env).get_id_generator().json()['data']
                item['shiftId'] = generator_id
                item['id'] = generator_id
                item['employeeId'] = self.employee_id
                new_shift.append(item)
            data['add_fixation_class_attendance_group']['body']['shiftDtos'] = new_shift
            data['add_fixation_class_attendance_group']['body']['shiftPlan']['MONDAY'] = new_shift[1]['shiftId']
            data['add_fixation_class_attendance_group']['body']['shiftPlan']['TUESDAY'] = new_shift[1]['shiftId']
            data['add_fixation_class_attendance_group']['body']['shiftPlan']['WEDNESDAY'] = new_shift[1]['shiftId']
            data['add_fixation_class_attendance_group']['body']['shiftPlan']['THURSDAY'] = new_shift[1]['shiftId']
            data['add_fixation_class_attendance_group']['body']['shiftPlan']['FRIDAY'] = new_shift[1]['shiftId']
            data['add_fixation_class_attendance_group']['body']['shiftPlan']['SATURDAY'] = new_shift[0]['shiftId']
            data['add_fixation_class_attendance_group']['body']['shiftPlan']['SUNDAY'] = new_shift[0]['shiftId']
            add_fixation_class_attendance_group_res = AttendanceGroupApi(self.env).add_attendance_group(
                data['add_fixation_class_attendance_group'])
            Assertions().assert_mode(add_fixation_class_attendance_group_res,
                                     data['add_fixation_class_attendance_group'])
            fixation_class_attendance_group_id = add_fixation_class_attendance_group_res.json()['data']
        '''
        with allure.step('第二步：加班申请'):
            # 查询加班申请时间是否符合条件
            overtime_start = round(int(time.mktime(time.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + " 18:00:00", "%Y-%m-%d %H:%M:%S")))*1000)
            overtime_end = round(int(time.mktime(time.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + " 20:00:00", "%Y-%m-%d %H:%M:%S")))*1000)
            data['check_overtime']['params']['employee_id'] = self.employee_id
            data['check_overtime']['params']['overtime_start'] = overtime_start
            data['check_overtime']['params']['overtime_end'] = overtime_end
            check_overtime_res = OvertimeApi(self.env).check_overtime(data['check_overtime'])
            Assertions().assert_mode(check_overtime_res, data['check_overtime'])

            # 获取审批流信息
            data['get_workflow_approval']['organization_id'] = '733358092246319104'
            data['get_workflow_approval']['params']['employee_id'] = self.employee_id
            get_workflow_approval_res = WorkflowApi(self.env).get_workflow_approval(data['get_workflow_approval'])
            Assertions().assert_mode(get_workflow_approval_res, data['get_workflow_approval'])

            data['send_overtime_apply']['body']['org_id'] = self.company_id
            data['send_overtime_apply']['body']['employee_id'] = self.employee_id
            data['send_overtime_apply']['body']['start_time'] =  overtime_start
            data['send_overtime_apply']['body']['end_time'] = overtime_end
            data['send_overtime_apply']['body']['duration'] = (overtime_end - overtime_start)/1000
            approverDict = dict()
            approverDict['employee_id'] = get_workflow_approval_res.json()['data'][0]['id']
            data['send_overtime_apply']['body']['approverList'].append()
            # send_overtime_apply_res = OvertimeApi(self.env).send_overtime_apply_api(data['send_overtime_apply'])
            # Assertions().assert_mode(send_overtime_apply_res, data['send_overtime_apply'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_overtime_module.py', '--env', 'test3'])