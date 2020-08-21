# @Author: Saco Song
# @Time: 2020/7/29-10:28 上午
# @Description:
import os
import random
from hashlib import md5

import allure
import pytest

from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.PayrollApi.employer_company_workforce_bill_management import EmployerCompanyWorkforceBillManagement


class TestEmployerCompanyWorkforceBillManagement:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @allure.title('获取劳务公司列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployerCompanyWorkforceBillManagement/get_service_company_list.yaml'))
    def test_get_service_company_list(self, data):
        response = EmployerCompanyWorkforceBillManagement(self.env).get_service_company_list_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取员工所在部门面包屑')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployerCompanyWorkforceBillManagement/get_employee_department_crumb.yaml'))
    def test_get_employee_department_crumb(self, data):
        response = EmployerCompanyWorkforceBillManagement(self.env).get_employee_department_crumb(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取OSS凭据，上传用工账单附件，并下载校验')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployerCompanyWorkforceBillManagement/employer_company_workforce_bill_attachment_uploading_and_downloading.yaml'))
    def test_employer_company_workforce_bill_attachment_uploading_and_downloading(self, data):
        with allure.step('获取OSS凭据'):
            response = EmployerCompanyWorkforceBillManagement(self.env).get_oss_credential(data)
            Assertions().assert_mode(response, data)

        with allure.step('上传附件'):
            credential_data = response.json()['data']
            oss_host = str(credential_data['host']) + '/'
            oss_key = data['oss_data']['key'] + str(random.random()) + data['files']['name']
            file_path_downloading_from = oss_host + oss_key
            file_path_for_uploading = data['files']['file_path_for_uploading']

            with open(file_path_for_uploading, 'rb') as upload_file:
                response = EmployerCompanyWorkforceBillManagement(self.env).upload_file_to_oss(
                    oss_host, oss_key, credential_data['policy'], credential_data['accessKeyId'], '201',
                    credential_data['signature'], upload_file)
                Assertions().assert_code(response.status_code, 201)

        with allure.step('下载附件，并校验MD5值'):
            file_path_downloading_to = data['files']['file_path_downloading_to']

            EmployerCompanyWorkforceBillManagement(self.env).download_bill_attachment(
                file_path_downloading_from, file_path_downloading_to)
            with open(file_path_for_uploading, 'rb') as origin_file:
                origin_hash = md5()
                origin_hash.update(origin_file.read())
            with open(file_path_downloading_to, 'rb') as downloaded_file:
                downloaded_hash = md5()
                downloaded_hash.update(downloaded_file.read())
            assert origin_hash.hexdigest() == downloaded_hash.hexdigest()

        os.remove(file_path_downloading_to)

    @allure.title('获取用工账单列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployerCompanyWorkforceBillManagement/get_bill_list.yaml'))
    def test_get_bill_list(self, data):
        response = EmployerCompanyWorkforceBillManagement(self.env).get_bill_list_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取用工账单详情')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployerCompanyWorkforceBillManagement/get_bill_detail.yaml'))
    def test_get_bill_detail(self, data):
        response = EmployerCompanyWorkforceBillManagement(self.env).get_bill_detail_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取form表单工作流和抄送信息接口')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployerCompanyWorkforceBillManagement/get_form_of_workflow_and_cc.yaml'))
    def test_get_form_of_workflow_and_cc(self, data):
        response = EmployerCompanyWorkforceBillManagement(self.env).get_form_of_workflow_and_cc_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('点击账单的查看详情编辑账单接口')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/EmployerCompanyWorkforceBillManagement'
        '/edit_bill_by_click_detail.yaml'))
    def test_edit_bill_by_click_detail(self, data):
        response = EmployerCompanyWorkforceBillManagement(self.env).edit_bill_by_click_detail_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('生成用工账单（暂存）')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/EmployerCompanyWorkforceBillManagement'
        '/generate_workforce_bill.yaml'))
    def test_generate_workforce_bill(self, data):
        response = EmployerCompanyWorkforceBillManagement(self.env).generate_workforce_bill(data)
        Assertions().assert_mode(response, data)

    @allure.title('根据部门id和type获取审批流信息')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployerCompanyWorkforceBillManagement/get_approval_query_by_department_and_type.yaml'))
    def test_get_approval_query_by_department_and_type(self, data):
        response = EmployerCompanyWorkforceBillManagement(self.env).get_approval_query_by_department_and_type_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取待我审批账单个数')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployerCompanyWorkforceBillManagement/get_number_of_workforce_bills_waiting_for_my_approval.yaml'))
    def test_get_number_of_approval_waiting_for_me(self, data):
        response = EmployerCompanyWorkforceBillManagement(self.env).get_number_of_approval_waiting_for_me(data)
        Assertions().assert_mode(response, data)
