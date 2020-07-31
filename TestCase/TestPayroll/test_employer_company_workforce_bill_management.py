# @Author: Saco Song
# @Time: 2020/7/29-10:28 上午
# @Description:
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
