# @Name:test_employee_salary_information.py
# @Author:Noah
# @Time:2020/8/6 1:59 下午
import allure
import pytest

from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.PayrollApi.employee_salary_information import EmployeeSalaryInformation

class TestEmployeeSalaryInformation():

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = "test2"

    @allure.title('获取员工薪资信息列表表头')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Payroll/EmployeeSalaryInformation/get_employee_salary_information_list_head.yaml'))
    def test_employee_salary_employee_information(self, data):
        response = EmployeeSalaryInformation(self.env).get_employee_salary_information_list_head_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取员工薪资信息列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Payroll/EmployeeSalaryInformation/get_employee_salary_information_list.yaml'))
    def test_employee_salary_information_list(self, data):
        response = EmployeeSalaryInformation(self.env).get_employee_salary_information_list_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取薪资信息个税主体和分部门列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Payroll/EmployeeSalaryInformation/get_itEntitys_and_department_list.yaml'))
    def test_itEntitys_and_department_list(self, data):
        response = EmployeeSalaryInformation(self.env).get_itEntitys_and_departments_list_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取薪资账套列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Payroll/EmployeeSalaryInformation/get_paygroup_list.yaml'))
    def test_get_paygroup_list(self, data):
        response = EmployeeSalaryInformation(self.env).get_paygroup_list_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取固定工资列表')
    @pytest.mark.parametrize('data',YamlHandle().read_yaml(
        'Payroll/EmployeeSalaryInformation/get_baseSalary_list.yaml'))
    def test_get_baseSalary_list(self, data):
        response = EmployeeSalaryInformation(self.env).get_baseSalary_list_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取员工薪资信息中薪资项目列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Payroll/EmployeeSalaryInformation/get_payrollItem_list.yaml'))
    def test_get_payrollItem_list(self, data):
        response = EmployeeSalaryInformation(self.env).get_payrollItem_list_api(data)
        Assertions().assert_mode(response, data)

    @allure.title('获取员工薪资信息详情')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Payroll/EmployeeSalaryInformation/get_employee_salary_detail.yaml'))
    def test_get_employee_salary_detail(self, data):
        response = EmployeeSalaryInformation(self.env).get_employee_salary_detail_api(data)
        Assertions().assert_mode(response, data)



if __name__ == '__main__':
    pytest.main(["-sv", "test_employee_salary_information.py", "--env", "test2"])


