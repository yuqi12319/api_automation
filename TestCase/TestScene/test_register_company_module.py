# coding:utf-8
# Name:test_register_company_module.py
# Author:qi.yu
# Time:2020/8/21 3:54 下午
# Description: 注册公司

import pytest
import allure
from faker import Faker
import Common.consts
from Common.log import MyLog
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Common.operation_mysql import *
from Common.request import *
from TestApi.WorkflowApi.workflow_domain import WorkflowDomainApi
from TestApi.PayrollApi.payroll_setting import PayrollSetting
from TestApi.AttendanceApi.attendance_setting import AttendanceSetting
from TestApi.LeaveApi.leave_setting_api import LeaveSettingApi
from TestApi.CocApi.company_register_request_api import CompanyRegisterRequestApi
from TestApi.MuscatApi.user_api import UserApi
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.WorkflowApi.workflow_set_api import WorkflowSetApi


class TestRegisterCompanyScene:

    @pytest.fixture(scope='class')
    def setup_class(self, env):
        fake = Faker(locale='zh_CN')
        return env, fake

    @pytest.mark.smoke
    @pytest.mark.workforce
    @pytest.mark.workforce_smoke
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/RegisterComapnyScene/main_scene.yaml'))
    def test_main_scene(self, data, setup_class):
        env = setup_class[0]
        fake = setup_class[1]

        with allure.step('第一步：创建公司'):

            # 注册公司
            # company_name = 'test_company_' + str(int(time.time()))
            company_name = fake.company()
            data['register_company']['body']['name'] = company_name
            add_company_register_res = CompanyRegisterRequestApi(env).add_company_register_api(data['register_company'])
            Assertions().assert_mode(add_company_register_res, data['register_company'])

            select_comapny_id_sql = "SELECT * FROM company_register_request WHERE `name` = '%s'" % company_name
            mysql_name = 'dukang_coc_dk' + env
            register_company_result = mysql_operate_select_fetchone(mysql_name, select_sql=select_comapny_id_sql)
            # time.sleep(8)

            # 审核通过
            data['company_register_approval']['body']['id'] = register_company_result['id']
            company_register_approval_res = CompanyRegisterRequestApi(env).company_register_approval_api(data['company_register_approval'])
            Assertions().assert_mode(company_register_approval_res, data['company_register_approval'])
            # time.sleep(8)

            get_my_companies_res = UserApi(env).get_my_companies_api()
            for item in get_my_companies_res.json()['data']:
                if item['company_name'] == company_name:
                    company_id = item['company_id']
                    Common.consts.COMPANY_INFORMATION['company_name'] = company_name
                    Common.consts.COMPANY_INFORMATION['company_id'] = company_id
                    break
                MyLog().error('未找到注册公司')

            data['brief_profile']['params']['company_id'] = company_id
            brief_profile_res = EmployeeApi(env).brief_profile_api(data['brief_profile'])
            Assertions().assert_mode(brief_profile_res, data['brief_profile'])
            employee_id = brief_profile_res.json()['data']['employee_id']
            Common.consts.COMPANY_INFORMATION['employee_id'] = employee_id

        with allure.step('第二步：校验是否生成默认审批流'):
            # 默认账单审批流判断
            data['default_bill_approval']['params']['coOrgId'] = company_id
            allure.attach(str(data['default_bill_approval']), "请求数据", allure.attachment_type.JSON)
            bill_approval_list_res = WorkflowSetApi(env).get_approval_list_api(data['default_bill_approval'])
            allure.attach(bill_approval_list_res.text, "bill_approval_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_in_text(bill_approval_list_res.json()['data'], '默认账单审批流')

            # 默认用工申请审批流判断
            data['default_workforce_apply_approval']['params']['coOrgId'] = company_id
            allure.attach(str(data['default_workforce_apply_approval']), "请求数据", allure.attachment_type.JSON)
            workforce_apply_approval_list_res = WorkflowSetApi(env).get_approval_list_api(
                data['default_workforce_apply_approval'])
            allure.attach(workforce_apply_approval_list_res.text, "用工申请审批流列表接口result", allure.attachment_type.JSON)
            Assertions().assert_in_text(workforce_apply_approval_list_res.json()['data'], '默认用工申请审批流')
            for item in workforce_apply_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工申请审批流':
                    Common.consts.DEFAULT_WORKFLOW_SETTING_ID['workforce_application'] = item['workflowSettingId']
                    break
            else:
                MyLog().error('没有生成默认用工申请审批流')

            # 默认用工登记审批流判断
            data['default_workforce_register_approval']['params']['coOrgId'] = company_id
            allure.attach(str(data['default_workforce_register_approval']), "请求数据", allure.attachment_type.JSON)
            workforce_register_approval_list_res = WorkflowSetApi(env).get_approval_list_api(
                data['default_workforce_register_approval'])
            allure.attach(workforce_register_approval_list_res.text, "用工登记审批流列表接口result", allure.attachment_type.JSON)
            Assertions().assert_in_text(workforce_register_approval_list_res.json()['data'], '默认用工登记审批流')
            for item in workforce_register_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工登记审批流':
                    Common.consts.DEFAULT_WORKFLOW_SETTING_ID['workforce_register'] = item['workflowSettingId']
                    break
            else:
                MyLog().error('没有生成默认用工登记审批流')

            # 默认用工更新审批流判断
            data['default_workforce_update_approval']['params']['coOrgId'] = company_id
            allure.attach(str(data['default_workforce_update_approval']), "请求数据", allure.attachment_type.JSON)
            workforce_update_approval_list_res = WorkflowSetApi(env).get_approval_list_api(
                data['default_workforce_update_approval'])
            allure.attach(workforce_update_approval_list_res.text, "用工更新审批流列表接口result",
                          allure.attachment_type.JSON)
            Assertions().assert_in_text(workforce_update_approval_list_res.json()['data'], '默认用工更新审批流')
            for item in workforce_update_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工更新审批流':
                    Common.consts.DEFAULT_WORKFLOW_SETTING_ID['workforce_update'] = item['workflowSettingId']
                    break
            else:
                MyLog().error('没有生成默认用工更新审批流')

            # 默认报销审批流判断
            data['default_claim_approval']['params']['coOrgId'] = company_id
            allure.attach(str(data['default_claim_approval']), "请求数据", allure.attachment_type.JSON)
            claim_approval_list_res = WorkflowDomainApi(env).claim_approval_list_api(data['default_claim_approval'])
            allure.attach(claim_approval_list_res.text, "claim_approval_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_in_text(claim_approval_list_res.json()['data'], '默认报销审批流')

            # 默认请假审批流判断
            data['default_leave_approval']['params']['coOrgId'] = company_id
            allure.attach(str(data['default_leave_approval']), "请求数据", allure.attachment_type.JSON)
            leave_approval_list_res = WorkflowDomainApi(env).leave_approval_list_api(data['default_leave_approval'])
            allure.attach(leave_approval_list_res.text, "leave_approval_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_in_text(leave_approval_list_res.json()['data'], '默认请假审批流')

            # 默认加班,补卡,外出,离职审批流判断
            data['default_attendance_approval']['params']['company_id'] = company_id
            allure.attach(str(data['default_attendance_approval']), "请求数据", allure.attachment_type.JSON)
            attendance_approval_list_res = WorkflowDomainApi(env).attendance_approval_list_api(
                data['default_attendance_approval'])
            allure.attach(attendance_approval_list_res.text, "attendance_approval_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_in_text(attendance_approval_list_res.json()['data'], '默认加班审批流')
            Assertions().assert_in_text(attendance_approval_list_res.json()['data'], '默认外出审批流')
            Assertions().assert_in_text(attendance_approval_list_res.json()['data'], '默认补卡审批流')
            Assertions().assert_in_text(attendance_approval_list_res.json()['data'], '默认离职审批流')

        with allure.step('第三步：校验是否生成默认薪资项'):
            data['default_payroll_item']['params']['coOrgId'] = company_id
            allure.attach(str(data['default_payroll_item']), "请求数据", allure.attachment_type.JSON)
            payroll_item_list_res = PayrollSetting(env).payroll_item_list_api(data['default_payroll_item'])
            allure.attach(payroll_item_list_res.text, "payroll_item_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_in_text(payroll_item_list_res.json()['data'], '基本工资')
            Assertions().assert_in_text(payroll_item_list_res.json()['data'], '工作日加班费')
            Assertions().assert_in_text(payroll_item_list_res.json()['data'], '休息日加班费')
            Assertions().assert_in_text(payroll_item_list_res.json()['data'], '法定假日加班费')
            Assertions().assert_in_text(payroll_item_list_res.json()['data'], '事假')
            Assertions().assert_in_text(payroll_item_list_res.json()['data'], '病假')
            Assertions().assert_in_text(payroll_item_list_res.json()['data'], '缺勤')

        with allure.step('第四步：校验是否生成默认考勤组'):
            data['default_attendance_group']['params']['company_id'] = company_id
            data['default_attendance_group']['params']['employeeId'] = employee_id
            allure.attach(str(data['default_attendance_group']), "请求数据", allure.attachment_type.JSON)
            attendance_group_res = AttendanceSetting(env).get_attendance_group_api(
                data['default_attendance_group'])
            allure.attach(attendance_group_res.text, "get_attendance_group_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_in_text(attendance_group_res.json()['data'], '默认考勤组')

        with allure.step('第五步：校验是否生成默认休假组'):
            data['default_leave_group']['params']['companyId'] = company_id
            allure.attach(str(data['default_leave_group']), "请求数据", allure.attachment_type.JSON)
            leave_group_res = LeaveSettingApi(env).get_leave_group_api(data['default_leave_group'])
            allure.attach(leave_group_res.text, "get_leave_group_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_in_text(leave_group_res.json()['data'], '默认休假组')

        # with allure.step('解散公司'):
        #     data['dissolve_company']['companyId'] = company_id
        #     dissolve_company_res = Muscat(env).dissolve_company(data['dissolve_company'])
        #     Assertions().assert_mode(dissolve_company_res, data['dissolve_company'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_register_company_module.py::TestRegisterCompanyScene::test_main_scene', '--env', 'test3'])