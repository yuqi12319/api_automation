# Name:test_organization_structure_module.py
# Author:lin
# Time:2020/8/27 10:47 上午

import pytest
import allure
import time
import Common.consts
from urllib3 import encode_multipart_formdata
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
import Common.operation_random
import Common.consts
from TestApi.EmployeeApi.employee_domain import EmployeeDomain


class TestOrganizationStructure:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/OrganizationStructureScene/main_sence.yaml'))
    def test_main_scene(self, data):
        # with allure.step("第一步，导入员工"):
        #     files = {'file': open('../../TestData/import_employee.xlsx', 'rb')}
        #     data['importEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
        #     import_employee_res = EmployeeDomain(self.env).batch_import_employee(data['importEmployee'], files)
        #     Assertions().assert_mode(import_employee_res, data['importEmployee'])
        #
        # with allure.step("第二步，获取导入的员工信息"):
        #     data['getImportEmployee']['headers']['x-dk-token'] = Common.consts.ACCESS_TOKEN[0]
        #     data['getImportEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
        #     get_import_employee_res = EmployeeDomain(self.env).batch_import_employee_1(data['getImportEmployee'])
        #     Assertions().assert_mode(get_import_employee_res, data['getImportEmployee'])
        #
        # with allure.step("第三步，确认导入员工信息"):
        #     data['correctEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
        #     data['correctEmployee']['params']['timestamp'] = int(round(time.time() * 1000))
        #     correct_employee_res = EmployeeDomain(self.env).correct_employee(data['correctEmployee'])
        #     Assertions().assert_mode(correct_employee_res, data['correctEmployee'])

        with allure.step("第四步，获取部门下所有的子部门信息"):
            data['organizationsChildren']['params']['timestamp'] = int(round(time.time() * 1000))
            organization_children_res = EmployeeDomain(self.env).organizations_children(data['organizationsChildren'])
            Assertions().assert_mode(organization_children_res, data['organizationsChildren'])

        with allure.step("第五步，获取公司组织架构"):
            data['chart']['params']['timestamp'] = int(round(time.time() * 1000))
            chart_res = EmployeeDomain(self.env).organizations_chart(data['chart'])
            Assertions().assert_mode(chart_res, data['chart'])
            Common.consts.COMPANY_CHART.append(chart_res.json()['data'])  # 存储员工数据
            print(Common.consts.COMPANY_CHART)

        with allure.step("第六步，修改公司信息"):
            data['modify_companies']['body']['header_employee_id'] = Common.consts.COMPANY_CHART[0]['employees'][0][
                'id']
            data['modify_companies']['params']['timestamp'] = int(round(time.time() * 1000))
            modify_companies = EmployeeDomain(self.env).modify_companies(data['modify_companies'])
            Assertions().assert_mode(modify_companies, data['modify_companies'])

        with allure.step("第七步，获取层级结构"):
            # 灵活用工层级结构
            data['business_level']['params']['timestamp'] = int(round(time.time() * 1000))
            data['business_level']['params']['type'] = 'WORKFORCE'
            # data['business_level']['params']['coOrgId'] =
            workforce_departments_level_res = EmployeeDomain(self.env).departments_level(data['business_level'])
            Assertions().assert_mode(workforce_departments_level_res, data['business_level'])

            # 绩效层级结构
            data['business_level']['params']['timestamp'] = int(round(time.time() * 1000))
            data['business_level']['params']['type'] = 'COMMISSION'
            # data['business_level']['params']['coOrgId'] =
            commission_departments_level_res = EmployeeDomain(self.env).departments_level(data['business_level'])
            Assertions().assert_mode(commission_departments_level_res, data['business_level'])

        with allure.step("第八步，新增普通部门类型"):
            # 新增普通部门
            data['departments']['params']['timestamp'] = int(round(time.time() * 1000))
            data['departments']['body']['business_type'] = 'GENERALDEPARTMENT'
            data['departments']['body']['code'] = Common.operation_random.random_code()
            data['departments']['body']['name'] = Common.operation_random.random_departments_name()
            data['departments']['body']['organizationBusinessLevelId'] = ''
            # print(organization_children_res.json()['data'][0]['id'])
            data['departments']['body']['parent_id'] = organization_children_res.json()['data'][0]['id']
            general_department_res = EmployeeDomain(self.env).departments(data['departments'])
            Assertions().assert_mode(general_department_res, data['departments'])

        with allure.step("第九步，新增灵活用工类型部门"):
            # 新增灵活用工类型部门
            data['departments']['body']['businessType'] = 'WORKFORCE'
            level = list()
            for item in range(len(workforce_departments_level_res.json()['data'])):
                data['departments']['params']['timestamp'] = int(round(time.time() * 1000))
                data['departments']['body']['code'] = Common.operation_random.random_code()
                data['departments']['body']['name'] = Common.operation_random.random_departments_name()
                data['departments']['body']['organizationBusinessLevelId'] = workforce_departments_level_res.json()['data'][item]['id']
                if item == 0:
                    data['departments']['body']['parent_id'] = organization_children_res.json()['data'][0]['id']
                    workforce_departments_res = EmployeeDomain(self.env).departments(data['departments'])
                    Assertions().assert_mode(workforce_departments_res, data['departments'])
                else:
                    data['departments']['body']['parent_id'] = workforce_departments_res.json()['data']['department_id']
                    workforce_departments_res = EmployeeDomain(self.env).departments(data['departments'])
                    Assertions().assert_mode(workforce_departments_res, data['departments'])



if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_organization_structure_module.py', '--env', 'test3'])
