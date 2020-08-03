# @Author: Saco Song
# @Time: 2020/7/29-10:28 上午
# @Description:
import random

import allure
import pytest

from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.PayrollApi.employer_company_workforce_bill_management import WorkforceBillManagement


class TestBillManagement:
    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test2')

    @allure.title('获取劳务公司列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/WorkforceBillManagement/EmployerCompanyWorkforceBillManagement/get_service_company_list.yaml'))
    def test_get_service_company_list(self, data):
        response = WorkforceBillManagement().get_service_company_list_api(self.url_path, data)
        Assertions().assert_mode(response, data)

    @allure.title('获取员工所在部门面包屑')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/WorkforceBillManagement/EmployerCompanyWorkforceBillManagement/get_employee_department_crumb.yaml'))
    def test_get_employee_department_crumb(self, data):
        response = WorkforceBillManagement().get_employee_department_crumb(self.url_path, data)
        Assertions().assert_mode(response, data)

    @allure.title('获取OSS凭据并上传用工账单附件')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/WorkforceBillManagement/EmployerCompanyWorkforceBillManagement/'
        'get_oss_credential_then_upload_bill_attachment.yaml'))
    def test_get_oss_credential(self, data):
        with allure.step('获取OSS凭据'):
            response = WorkforceBillManagement().get_oss_credential(self.url_path, data)
            Assertions().assert_mode(response, data)

        with allure.step('上传附件'):
            credential_data = response.json()['data']
            with open(
                    '/Users/sacosong/PycharmProjects/riesling-apitest/TestData/excel_for_uploading_bill_attachment.xlsx',
                    'rb') as upload_file:
                form_data = {'key': data['oss_data']['key'] + str(
                    random.random()) + '/' + 'TestData/excel_for_uploading_bill_attachment.xlsx',
                             'policy': credential_data['policy'], 'OSSAccessKeyId': credential_data['accessKeyId'],
                             'success_action_status': '201',
                             'signature': credential_data['signature'], 'file': upload_file}
                response = WorkforceBillManagement().upload_file_to_oss(str(credential_data['host']) + '/', form_data)
                Assertions().assert_code(response.status_code, 201)



    @allure.title('获取用工账单列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/WorkforceBillManagement/EmployerCompanyWorkforceBillManagement/get_bill_list.yaml'))
    def test_get_bill_list(self, data):
        response = WorkforceBillManagement().get_bill_list_api(self.url_path, data)
        Assertions().assert_mode(response, data)

    @allure.title('获取用工账单详情')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/WorkforceBillManagement/EmployerCompanyWorkforceBillManagement/get_bill_detail.yaml'))
    def test_get_bill_detail(self, data):
        response = WorkforceBillManagement().get_bill_detail_api(self.url_path, data)
        Assertions().assert_mode(response, data)

    @allure.title('获取form表单工作流和抄送信息接口')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/WorkforceBillManagement/EmployerCompanyWorkforceBillManagement/get_form_of_workflow_and_cc.yaml'))
    def test_get_form_of_workflow_and_cc(self, data):
        response = WorkforceBillManagement().get_form_of_workflow_and_cc_api(self.url_path, data)
        Assertions().assert_mode(response, data)

    @allure.title('点击账单的查看详情编辑账单接口')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/WorkforceBillManagement/EmployerCompanyWorkforceBillManagement/edit_bill_by_click_detail.yaml'))
    def test_edit_bill_by_click_detail(self, data):
        response = WorkforceBillManagement().edit_bill_by_click_detail_api(self.url_path, data)
        Assertions().assert_mode(response, data)




