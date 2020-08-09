# @Name:test_employee_salary_information.py
# @Author:Noah
# @Time:2020/8/6 1:59 下午
import allure
import pytest

from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Conf.config import Config
from TestApi.PayrollApi.employee_salary_information import EmployeeSalaryInformation

class TestEmployeeSalaryInformation():
    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test2')

    @allure.title('获取员工薪资信息列表表头')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Payroll/EmployeeSalaryInformation/employee_salary_information_list_head.yaml'))
    def test_employee_salary_employee_information(self, data):
        response = EmployeeSalaryInformation().get_employee_salary_information_list_head_api(self.url_path, data)
        Assertions().assert_mode(response, data)

    @allure.title('获取员工薪资信息列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Payroll/EmployeeSalaryInformation/employee_salary_information_list.yaml'))
    def test_employee_salary_information_list(self, data):
        response = EmployeeSalaryInformation().get_employee_salary_information_list_api(self.url_path, data)
        Assertions().assert_mode(response, data)

