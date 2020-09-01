# Name:test_import_employee_module.py.py
# Author:lin
# Time:2020/9/1 3:50 下午

import pytest
import allure
import time
from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from TestApi.EmployeeApi.employee_domain import EmployeeDomain
import Common.consts


class TestImportEmployee:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('SceneData/OrganizationStructureScene/import_employee.yaml'))
    def test_main_scene(self, data):
        with allure.step("第一步，导入员工"):
            files = {'file': open('../../TestData/import_employee.xlsx', 'rb')}
            data['importEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
            import_employee_res = EmployeeDomain(self.env).batch_import_employee(data['importEmployee'], files)
            Assertions().assert_mode(import_employee_res, data['importEmployee'])

        with allure.step("第二步，获取导入的员工信息"):
            data['getImportEmployee']['headers']['x-dk-token'] = Common.consts.ACCESS_TOKEN[0]
            data['getImportEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
            get_import_employee_res = EmployeeDomain(self.env).batch_import_employee_1(data['getImportEmployee'])
            Assertions().assert_mode(get_import_employee_res, data['getImportEmployee'])

        with allure.step("第三步，确认导入员工信息"):
            data['correctEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
            data['correctEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
            correct_employee_res = EmployeeDomain(self.env).correct_employee(data['correctEmployee'])
            Assertions().assert_mode(correct_employee_res, data['correctEmployee'])


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_import_employee_module.py', '--env', 'test3'])
