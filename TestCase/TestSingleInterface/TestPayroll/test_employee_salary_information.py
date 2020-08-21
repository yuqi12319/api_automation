# @Name:test_employee_salary_information.py
# @Author:Noah
# @Time:2020/8/6 1:59 下午
import allure
import pytest

from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Conf.config import Config
from TestApi.PayrollApi.employee_salary_information import EmployeeSalaryInformation


class TestEmployeeSalaryInformation:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @allure.title('获取员工薪资信息列表表头')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployeeSalaryInformation/get_employee_salary_information_list_head.yaml'))
    def test_employee_salary_employee_information(self, data):
        response = EmployeeSalaryInformation(self.env).get_employee_salary_information_list_head_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取员工薪资信息列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployeeSalaryInformation/get_employee_salary_information_list.yaml'))
    def test_employee_salary_information_list(self, data):
        response = EmployeeSalaryInformation(self.env).get_employee_salary_information_list_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取薪资信息个税主体和分部门列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'SingleInterfaceData/Payroll/EmployeeSalaryInformation/get_itEntitys_and_department_list.yaml'))
    def test_itEntitys_and_department_list(self, data):
        response = EmployeeSalaryInformation(self.env).get_itEntitys_and_departments_list_api(data)
        Assertions().assert_mode(response, data)
