# coding:utf-8
# Name:test_leave_module.py
# Author:qi.yu
# Time:2020/9/11 3:33 下午
# Description:休假模块

import pytest, allure, time, datetime
import Common.consts
from Common.log import MyLog
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.AttendanceApi.attendance_group_api import AttendanceGroupApi
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.LeaveApi.leave_setting_api import LeaveSettingApi
from TestApi.LeaveApi.leave_request_api import LeaveRequestApi
from TestApi.AttendanceApi.clock_api import ClockApi
from TestApi.AttendanceApi.calendar_api import CalendarApi
from TestApi.LeaveApi.leave_workflow_setting_api import LeaveWorkflowSettingApi
from TestApi.LeaveApi.leave_info_api import LeaveInfoApi
from TestCase.TestScene import attendance
from TestApi.MuscatApi.user_api import UserApi


class TestLeave:

    @pytest.fixture(scope='class')
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
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/LeaveScene/main_scene.yaml'))
    def test_main_scene(self, data, setup_class):
        with allure.step('第一步：添加休假组'):
            leave_group_name = 'leave_group_' + str(int(time.time()))
            data['add_leave_group']['body']['employeesDto']['employeeIds'].append(setup_class[2])
            data['add_leave_group']['body']['leaveGroupAnnualLeaveDto']['coOrgId'] = setup_class[1]
            data['add_leave_group']['body']['leaveGroupDto']['coOrgId'] = setup_class[1]
            data['add_leave_group']['body']['leaveGroupDto']['name'] = leave_group_name
            data['add_leave_group']['body']['name'] = leave_group_name
            add_leave_groups_res = LeaveSettingApi(setup_class[0]).add_leave_groups_api(data['add_leave_group'])
            Assertions().assert_mode(add_leave_groups_res, data['add_leave_group'])
            leave_groups_id = add_leave_groups_res.json()['data']
            # time.sleep(5)

        with allure.step('第二步：获取休假默认审批流,修改审批人为指定人，自动审批通过'):
            # 获取默认休假审批流id
            data['get_leave_approval']['params']['coOrgId'] = setup_class[1]
            get_leave_approval_res = LeaveWorkflowSettingApi(setup_class[0]).get_leave_approval_list_api(data['get_leave_approval'])
            Assertions().assert_mode(get_leave_approval_res, data['get_leave_approval'])
            for item in get_leave_approval_res.json()['data']:
                if item['name'] == '默认请假审批流':
                    default_leave_approval_id = item['id']
                    MyLog().info('有默认请假审批流')
                else:
                    MyLog().error('无默认请假审批流')

            # 修改默认审批流
            data['post_leave_approval']['body']['coOrgId'] = setup_class[1]
            data['post_leave_approval']['body']['leaveWorkflowSettingId'] = default_leave_approval_id
            data['post_leave_approval']['body']['leaveWorkflowSettingRules'][0]['rules'][0]['approvalParameters'].append(setup_class[2])
            data['post_leave_approval']['body']['orgIds'].append(setup_class[1])
            post_leave_approval_res = LeaveWorkflowSettingApi(setup_class[0]).post_leave_approval_api(data['post_leave_approval'])
            Assertions().assert_mode(post_leave_approval_res, data['post_leave_approval'])

        with allure.step('第三步：设置考勤组为固定班制'):
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
            data['update_default_attendance_group']['body']['attendanceDeductionSettingDto'] = \
                get_default_attendance_group_information_res.json()['data']['attendanceDeductionSettingVo']
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

        with allure.step('第四步：固定班制请假申请'):
            time.sleep(5)
            data['apply_leave']['body']['employeeId'] = setup_class[2]
            data['apply_leave']['body']['orgId'] = setup_class[1]
            leave_approval = dict()
            leave_approval['employee_id'] = setup_class[2]
            leave_approval['sort_order'] = 1
            data['apply_leave']['body']['approverList'].append(leave_approval)
            data['apply_leave']['body']['beginDate'] = round(int(time.mktime(datetime.date.today().timetuple())) * 1000)
            data['apply_leave']['body']['endDate'] = round(int(time.mktime(datetime.date.today().timetuple())) * 1000)
            apply_leave_res = LeaveRequestApi(setup_class[0]).apply_leave(data['apply_leave'])
            Assertions().assert_mode(apply_leave_res, data['apply_leave'])
            apply_leave_id = apply_leave_res.json()['data']

        with allure.step('第五步：查看记录'):
            # 查看打卡（无需打卡）
            data['get_employee_worktimeinfo']['employee_id'] = setup_class[2]
            get_employee_worktimeinfo_res = ClockApi(setup_class[0]).get_employee_worktimeinfo(
                data['get_employee_worktimeinfo'])
            Assertions().assert_mode(get_employee_worktimeinfo_res, data['get_employee_worktimeinfo'])
            Assertions().assert_in_text(get_employee_worktimeinfo_res.json()['data'], 'LEAVE')

            # 查看日历
            data['get_calendar_day_record']['body']['employeeId'] = setup_class[2]
            get_calendar_day_record_res = CalendarApi(setup_class[0]).get_calendar_day_record_api(
                data['get_calendar_day_record'])
            Assertions().assert_mode(get_calendar_day_record_res, data['get_calendar_day_record'])
            Assertions().assert_in_text(get_calendar_day_record_res.json()['data'], apply_leave_id)

            # 我的休假
            data['get_employee_leave_record']['params']['employee_id'] = setup_class[2]
            get_employee_leave_record_res = LeaveInfoApi(setup_class[0]).get_employee_leave_record_api(data['get_employee_leave_record'])
            Assertions().assert_in_text(get_employee_leave_record_res.json()['data'], apply_leave_id)

            # 我的审批
            data['my_approval']['params']['company_id'] = setup_class[1]
            my_approval_res = EmployeeApi(setup_class[0]).my_approval_api(data['my_approval'])
            Assertions().assert_in_text(my_approval_res.json()['data'], apply_leave_id)

            # 我的申请
            data['my_application']['params']['employee_id'] = setup_class[2]
            my_application_res = EmployeeApi(setup_class[0]).my_application_api(data['my_application'])
            Assertions().assert_in_text(my_application_res.json()['data'], apply_leave_id)

        with allure.step('第六步：取消休假申请'):
            data['canceled_leave_apply']['leaveFormId'] = apply_leave_id
            data['canceled_leave_apply']['body']['leaveFormId'] = apply_leave_id
            canceled_leave_apply_res = LeaveRequestApi(setup_class[0]).canceled_leave_apply(
                data['canceled_leave_apply'])
            Assertions().assert_mode(canceled_leave_apply_res, data['canceled_leave_apply'])

        with allure.step('第七步：删除新增休假组和位置打卡'):
            data['delete_leave_group']['leaveGroupId'] = leave_groups_id
            delete_leave_group_res = LeaveSettingApi(setup_class[0]).delete_leave_group(data['delete_leave_group'])
            Assertions().assert_mode(delete_leave_group_res, data['delete_leave_group'])

            data['delete_pincoordinate']['pin_coordinate_id'] = add_attendance_location_id
            data['delete_pincoordinate']['params']['attendance_group_id'] = default_attendance_group_id
            delete_pincoordinate_res = ClockApi(setup_class[0]).delete_pincoordinate(data['delete_pincoordinate'])
            Assertions().assert_mode(delete_pincoordinate_res, data['delete_pincoordinate'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_leave_module.py', '--env', 'test1'])
