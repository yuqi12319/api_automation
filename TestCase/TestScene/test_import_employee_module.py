# Name:test_import_employee_module.py.py
# Author:lin
# Time:2020/9/1 3:50 下午

import pytest
import allure
import time
from Common.log import MyLog
from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.EmployeeApi.employee_domain import EmployeeDomain
import Common.consts
from TestApi.MuscatApi.user_api import UserApi


class TestImportEmployee:

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
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('SceneData/ImportEmployeeScene/main_scene.yaml'))
    def test_main_scene(self, data, setup_class):
        with allure.step("第一步，导入员工"):
            # files = {'file': open('../../TestData/import_employee.xlsx', 'rb')}
            files = {'file': open('./TestData/import_employee.xlsx', 'rb')}
            data['importEmployee']['params']['coOrgId'] = setup_class[1]
            data['importEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
            import_employee_res = EmployeeDomain(setup_class[0]).batch_import_employee(data['importEmployee'], files)
            Assertions().assert_mode(import_employee_res, data['importEmployee'])

        with allure.step("第二步，获取导入的员工信息"):
            data['getImportEmployee']['headers']['x-dk-token'] = Common.consts.ACCESS_TOKEN[0]
            data['getImportEmployee']['params']['coOrgId'] = setup_class[1]
            data['getImportEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
            get_import_employee_res = EmployeeDomain(setup_class[0]).batch_import_employee_1(data['getImportEmployee'])
            Assertions().assert_mode(get_import_employee_res, data['getImportEmployee'])

        with allure.step("第三步，确认导入员工信息"):
            data['correctEmployee']['params']['coOrgId'] = setup_class[1]
            data['correctEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
            correct_employee_res = EmployeeDomain(setup_class[0]).correct_employee(data['correctEmployee'])
            Assertions().assert_mode(correct_employee_res, data['correctEmployee'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_import_employee_module.py', '--env', 'test3'])
