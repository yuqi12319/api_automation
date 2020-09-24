# coding:utf-8
# Name:test_outgoing_module.py
# Author:qi.yu
# Time:2020/9/17 5:08 下午
# Description:
import datetime
import time

import allure
import pytest
import Common.consts
from Common.log import MyLog
from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from TestApi.AttendanceApi.attendance_group_api import AttendanceGroupApi
from TestApi.AttendanceApi.calendar_api import CalendarApi
from TestApi.AttendanceApi.clock_api import ClockApi
from TestApi.AttendanceApi.workflow_set_api import WorkflowSetApi
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.MuscatApi.muscat import Muscat
from TestApi.LeaveApi.outgoing_form_api import OutgoingFormApi
from TestApi.MuscatApi.notification_api import NotificationApi
from TestCase.TestScene import attendance


class TestOutgoing:

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
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/Outgoing/main_scene.yaml'))
    def test_main_scene(self, data, setup_class):
        with allure.step('第一步：获取加班默认审批流,修改审批人为指定人，自动审批通过'):
            # 获取默认外出审批流id
            data['outgoing_approval_list']['params']['company_id'] = setup_class[1]
            outgoing_approval_list_res = WorkflowSetApi(setup_class[0]).attendance_approval_list_api(
                data['outgoing_approval_list'])
            Assertions().assert_mode(outgoing_approval_list_res, data['outgoing_approval_list'])
            for item in outgoing_approval_list_res.json()['data']:
                if item['name'] == '默认外出审批流':
                    default_outgoing_approval_id = item['id']
                else:
                    MyLog().debug('当前公司无默认外出审批流')

            # 修改外出默认审批流，自动审批通过
            data['update_outgoing_approval']['workflow_setting_id'] = default_outgoing_approval_id
            data['update_outgoing_approval']['body']['approverlist'][0]['employee_id'] = setup_class[2]
            data['update_outgoing_approval']['body']['company_id'] = setup_class[1]
            data['update_outgoing_approval']['body']['orglist'][0]['co_org_id'] = setup_class[1]
            update_outgoing_approval_res = WorkflowSetApi(setup_class[0]).update_attendance_approval(
                data['update_outgoing_approval'])
            Assertions().assert_mode(update_outgoing_approval_res, data['update_outgoing_approval'])

        with allure.step('第二步：考勤组设置'):
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
            data['update_default_attendance_group']['body']['overtimeId'] = get_overtime_rule_list['data'][0][
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
            Assertions().assert_mode(update_attendance_group_res, data['update_default_attendance_group'])
            Assertions().assert_text(update_attendance_group_res.json()['data'], str(default_attendance_group_id))

        with allure.step('第三步：外出申请'):

            data['send_outgoing_apply']['body']['orgId'] = setup_class[1]
            data['send_outgoing_apply']['body']['employeeId'] = setup_class[2]
            data['send_outgoing_apply']['body']['beginDate'] = round(
                int(time.mktime(datetime.date.today().timetuple())) * 1000)
            data['send_outgoing_apply']['body']['endDate'] = round(
                int(time.mktime(datetime.date.today().timetuple())) * 1000)
            data['send_outgoing_apply']['body']['approverList'][0]['employee_id'] = setup_class[2]
            send_outgoing_apply_res = OutgoingFormApi(setup_class[0]).send_outgoing_apply_api(
                data['send_outgoing_apply'])
            Assertions().assert_mode(send_outgoing_apply_res, data['send_outgoing_apply'])
            send_outgoing_apply_id = send_outgoing_apply_res.json()['data']
            time.sleep(5)

        with allure.step('第四步：查看外出'):
            # 查看日历
            data['get_calendar_day_record']['body']['employeeId'] = setup_class[2]
            get_calendar_day_record_res = CalendarApi(setup_class[0]).get_calendar_day_record_api(
                data['get_calendar_day_record'])
            Assertions().assert_mode(get_calendar_day_record_res, data['get_calendar_day_record'])
            for item in get_calendar_day_record_res.json()['data']['outgoing']:
                if item['outgoingFormId'] == send_outgoing_apply_id:
                    Assertions().assert_text(item['status'], 'AGREED')
                    break

            # 我的审批
            data['my_approval']['params']['company_id'] = setup_class[1]
            my_approval_res = EmployeeApi(setup_class[0]).my_approval_api(data['my_approval'])
            Assertions().assert_mode(my_approval_res, data['my_approval'])
            for item in my_approval_res.json()['data']['myApprovalVoList']:
                if item['oa']['formId'] == send_outgoing_apply_id:
                    Assertions().assert_text(item['oa']['status'], '已通过')
                    break

            # 我的申请
            data['my_application']['params']['employee_id'] = setup_class[2]
            my_application_res = EmployeeApi(setup_class[0]).my_application_api(data['my_application'])
            Assertions().assert_mode(my_application_res, data['my_application'])
            for item in my_application_res.json()['data']['oaApprovalList']:
                if item['formId'] == send_outgoing_apply_id:
                    Assertions().assert_text(item['status'], '已通过')
                    break

            # 我的消息
            data['get_notifications_list']['params']['company_id'] = setup_class[1]
            get_notifications_list_res = NotificationApi(setup_class[0]).get_notifications_list_api(
                data['get_notifications_list'])
            Assertions().assert_mode(get_notifications_list_res, data['get_notifications_list'])
            for item in get_notifications_list_res.json()['data']['notificationList']:
                if item['eventId'] == send_outgoing_apply_id and item['operationType'] == 'OUTGOING':
                    break

        with allure.step('第五步：取消外出申请'):
            data['canceled_outgoing_apply']['outgoingFormId'] = send_outgoing_apply_id
            canceled_outgoing_apply_res = OutgoingFormApi(setup_class[0]).canceled_outgoing_apply_api(
                data['canceled_outgoing_apply'])
            Assertions().assert_mode(canceled_outgoing_apply_res, data['canceled_outgoing_apply'])

        with allure.step('第六步：删除位置打卡'):
            data['delete_pincoordinate']['pin_coordinate_id'] = add_attendance_location_id
            data['delete_pincoordinate']['params']['attendance_group_id'] = default_attendance_group_id
            delete_pincoordinate_res = ClockApi(setup_class[0]).delete_pincoordinate(data['delete_pincoordinate'])
            Assertions().assert_mode(delete_pincoordinate_res, data['delete_pincoordinate'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_outgoing_module.py', '--env', 'test1'])
