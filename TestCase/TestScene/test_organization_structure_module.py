# Name:test_organization_structure_module.py
# Author:lin
# Time:2020/8/27 10:47 上午

import pytest
import allure
import time
import Common.consts
from urllib3 import encode_multipart_formdata

from Common.log import MyLog
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
import Common.operation_random
import Common.consts
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.EmployeeApi.employee_domain import EmployeeDomain
from TestApi.MuscatApi.user_api import UserApi


class TestOrganizationStructure:

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
    @pytest.mark.run(order=5)
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/OrganizationStructureScene/main_sence.yaml'))
    def test_main_scene(self, data, setup_class):

        with allure.step("第一步，获取部门下所有的子部门信息"):
            data['organizationsChildren']['coOrgId'] = setup_class[1]
            organization_children_res = EmployeeDomain(setup_class[0]).organizations_children(data['organizationsChildren'])
            Assertions().assert_mode(organization_children_res, data['organizationsChildren'])

        with allure.step("第二步，获取公司组织架构"):
            data['chart']['coOrgId'] = setup_class[1]
            chart_res = EmployeeDomain(setup_class[0]).organizations_chart(data['chart'])
            Assertions().assert_mode(chart_res, data['chart'])
            # Common.consts.COMPANY_CHART.append(chart_res.json()['data'])  # 存储员工数据

        with allure.step("第三步，修改公司信息,设置公司主管"):
            data['modify_companies']['coOrgId'] = setup_class[1]
            data['modify_companies']['body']['header_employee_id'] = chart_res.json()['data']['employees'][0][
                'id']
            modify_companies = EmployeeDomain(setup_class[0]).modify_companies(data['modify_companies'])
            Assertions().assert_mode(modify_companies, data['modify_companies'])

        with allure.step("第四步，获取层级结构"):
            # 灵活用工层级结构
            data['business_level']['params']['coOrgId'] = setup_class[1]
            data['business_level']['params']['type'] = 'WORKFORCE'
            workforce_departments_level_res = EmployeeDomain(setup_class[0]).departments_level(data['business_level'])
            Assertions().assert_mode(workforce_departments_level_res, data['business_level'])

            # 绩效层级结构
            data['business_level']['params']['coOrgId'] = setup_class[1]
            data['business_level']['params']['type'] = 'COMMISSION'
            commission_departments_level_res = EmployeeDomain(setup_class[0]).departments_level(data['business_level'])
            Assertions().assert_mode(commission_departments_level_res, data['business_level'])

        with allure.step("第五步，新增普通部门类型"):
            # 新增普通部门
            data['departments']['body']['business_type'] = 'GENERALDEPARTMENT'
            data['departments']['body']['code'] = Common.operation_random.random_code()
            data['departments']['body']['name'] = Common.operation_random.random_departments_name()
            data['departments']['body']['organizationBusinessLevelId'] = ''
            data['departments']['body']['parent_id'] = organization_children_res.json()['data'][0]['id']
            general_department_res = EmployeeDomain(setup_class[0]).departments(data['departments'])
            Assertions().assert_mode(general_department_res, data['departments'])

        with allure.step("第六步，新增灵活用工类型部门"):
            # 新增灵活用工类型部门
            data['departments']['body']['businessType'] = 'WORKFORCE'
            for item in range(len(workforce_departments_level_res.json()['data'])):
                data['departments']['body']['code'] = Common.operation_random.random_code()
                data['departments']['body']['name'] = Common.operation_random.random_departments_name()
                data['departments']['body']['organizationBusinessLevelId'] = workforce_departments_level_res.json()['data'][item]['id']
                if item == 0:
                    data['departments']['body']['parent_id'] = organization_children_res.json()['data'][0]['id']
                    workforce_departments_res = EmployeeDomain(setup_class[0]).departments(data['departments'])
                    Assertions().assert_mode(workforce_departments_res, data['departments'])
                else:
                    data['departments']['body']['parent_id'] = workforce_departments_res.json()['data']['department_id']
                    workforce_departments_res = EmployeeDomain(setup_class[0]).departments(data['departments'])
                    Assertions().assert_mode(workforce_departments_res, data['departments'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_organization_structure_module.py', '--env', 'test3'])
