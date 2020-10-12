# coding:utf-8
# Name:test_employee_master_data.py
# Author:qi.yu
# Time:2020/8/27 10:50 上午
# Description: 员工管理

import pytest, allure
from Common.log import MyLog
import Common.consts
import random
import time
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.CommissionApi.positon import Position
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.EmployeeApi.rank import Rank
from TestApi.EmployeeApi.cost_center import CostCenter
from TestApi.EmployeeApi.labor_contract_parties import LaborContractParties
from TestApi.EmployeeApi.profile import Profile
from TestApi.EmployeeApi.employee_contract import EmployeeContract
from TestApi.MuscatApi.user_api import UserApi


class TestEmployeeManager:

    @pytest.fixture(autouse=True)
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
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/EmployeeMasterDataScene/main_scene.yaml'))
    def test_main_scene(self, data, setup_class):

        with allure.step('第一步：获取第一页员工管理列表数据'):
            data['get_employee_manager_list']['params']['company_id'] = setup_class[1]
            data['get_employee_manager_list']['headers']['x-dk-token'] = Common.consts.ACCESS_TOKEN[0]
            get_employee_manager_list_res = EmployeeApi(setup_class[0]).get_employee_manager_list(
                data['get_employee_manager_list'])
            Assertions().assert_mode(get_employee_manager_list_res, 11)

        with allure.step('第二步：组织信息设置'):
            # 添加职级
            data['add_rank']['body']['coOrgId'] = setup_class[1]
            rank_name = '职级' + str(int(time.time()))
            data['add_rank']['body']['name'] = rank_name
            add_rank_res = Rank(setup_class[0]).add_rank_api(data['add_rank'])
            Assertions().assert_mode(add_rank_res, data['add_rank'])

            # 查看职级
            data['get_rank']['params']['coOrgId'] = setup_class[1]
            get_rank_res = Rank(setup_class[0]).get_rank_api(data['get_rank'])
            Assertions().assert_in_text(get_rank_res.json()['data'], rank_name)

            # 添加职位
            data['add_position']['body']['coOrgId'] = setup_class[1]
            position_name = '职位' + str(int(time.time()))
            data['add_position']['body']['name'] = position_name
            add_position_res = Position(setup_class[0]).add_position_api(data['add_position'])
            Assertions().assert_mode(add_position_res, data['add_position'])

            # 查看职位
            data['get_position']['body']['coOrgId'] = setup_class[1]
            get_position_res = Position(setup_class[0]).get_position_api(data['get_position'])
            Assertions().assert_in_text(get_position_res.json()['data'], position_name)
            
            # 添加劳动合同主体
            data['add_laborcontractparties']['body']['coOrgId'] = setup_class[1]
            laborcontractparties_name = '劳动合同主体' + str(int(time.time()))
            data['add_laborcontractparties']['body']['name'] =laborcontractparties_name
            add_laborcontractparties_res = LaborContractParties(setup_class[0]).add_laborcontractparties_api(
                data['add_laborcontractparties'])
            Assertions().assert_mode(add_laborcontractparties_res, data['add_laborcontractparties'])

            # 查看劳动合同主体
            data['get_laborcontractparties']['params']['coOrgId'] = setup_class[1]
            get_laborcontractparties_res = LaborContractParties(setup_class[0]).get_laborcontractparties_api(
                data['get_laborcontractparties'])
            Assertions().assert_in_text(get_laborcontractparties_res.json()['data'], laborcontractparties_name)

            # 添加成本中心
            data['add_costcenter']['body']['coOrgId'] = setup_class[1]
            costcenter_name = '成本中心' + str(int(time.time()))
            data['add_costcenter']['body']['name'] = costcenter_name
            add_costcenter_res = CostCenter(setup_class[0]).add_costcenter_api(data['add_costcenter'])
            Assertions().assert_mode(add_costcenter_res, data['add_costcenter'])

            # 查看成本中心
            data['get_costcenter']['params']['coOrgId'] = setup_class[1]
            get_costcenter_res = CostCenter(setup_class[0]).get_costcenter_api(data['get_costcenter'])
            Assertions().assert_in_text(get_costcenter_res.json()['data'], costcenter_name)

        with allure.step('第三步：修改,查看员工信息'):
            # 获取员工组织信息
            data['get_employee_organization']['employee_id'] = setup_class[2]
            data['get_employee_organization']['params']['company_id'] = setup_class[1]
            get_employee_organization_res = EmployeeApi(setup_class[0]).get_employee_organization_api(
                data['get_employee_organization'])
            Assertions().assert_mode(get_employee_organization_res, data['get_employee_organization'])

            # 修改员工组织信息
            data['update_employee_organization']['employee_id'] = setup_class[2]
            data['update_employee_organization']['body']['department_ids'].append(
                get_employee_organization_res.json()['data']['department_infos'][0]['id'])
            data['update_employee_organization']['body']['department_infos'].append(
                get_employee_organization_res.json()['data']['department_infos'][0])
            data['update_employee_organization']['body']['employee_id'] = setup_class[2]
            data['update_employee_organization']['body']['laborContractPartiesName'] = get_laborcontractparties_res.json()['data'][0]['name']
            update_employee_organization_res = EmployeeApi(setup_class[0]).update_employee_organization_api(
                data['update_employee_organization'])
            Assertions().assert_mode(update_employee_organization_res, data['update_employee_organization'])

            # 获取员工个人信息
            data['get_employee_information']['employee_id'] = setup_class[2]
            get_employee_information_res = EmployeeApi(setup_class[0]).get_employee_information_api(
                data['get_employee_information'])
            Assertions().assert_mode(get_employee_information_res, data['get_employee_information'])

            # 修改员工个人信息
            data['update_employee_information']['body']['created_time'] = get_employee_information_res.json()['data'][
                'created_time']
            data['update_employee_information']['body']['updated_time'] = round(int(time.time()) * 1000)
            data['update_employee_information']['body']['displayName'] = get_employee_information_res.json()['data'][
                'displayName']
            data['update_employee_information']['body']['employeeId'] = setup_class[2]
            data['update_employee_information']['body']['mobile_area_code'] = get_employee_information_res.json()['data']['mobile_area_code']
            data['update_employee_information']['body']['phone_number'] = get_employee_information_res.json()['data'][
                'phone_number']
            personEmail = str(random.randint(100, 999)) + '@' + str(random.randint(100, 999)) + '.com'
            data['update_employee_information']['body']['personEmail'] = personEmail
            update_employee_information_res = EmployeeApi(setup_class[0]).update_employee_information_api(
                data['update_employee_information'])
            Assertions().assert_mode(update_employee_information_res, data['update_employee_information'])

            # 修改员工教育信息
            data['update_employee_education']['body']['employeeId'] = setup_class[2]
            major = str(random.randint(1000, 9999))
            data['update_employee_education']['body']['educations'][0]['major'] = major
            update_employee_education_res = EmployeeApi(setup_class[0]).update_employee_education_api(
                data['update_employee_education'])
            Assertions().assert_mode(update_employee_education_res, data['update_employee_education'])

            # 获取员工教育信息
            data['get_employee_education']['employee_id'] = setup_class[2]
            get_employee_education_res = EmployeeApi(setup_class[0]).get_employee_education_api(data['get_employee_education'])
            Assertions().assert_in_text(get_employee_education_res.json()['data'], major)

            # 修改员工工作经历
            data['update_employee_work_experience']['body']['employeeId'] = setup_class[2]
            company_name = str(random.randint(1000, 9999))
            data['update_employee_work_experience']['body']['work_experiences'][0]['company'] = company_name
            update_employee_work_experience_res = EmployeeApi(setup_class[0]).update_employee_work_experience_api(
                data['update_employee_work_experience'])
            Assertions().assert_mode(update_employee_work_experience_res, data['update_employee_work_experience'])

            # 获取员工工作信息
            data['get_employee_work_experience']['employee_id'] = setup_class[2]
            get_employee_work_experience_res = EmployeeApi(setup_class[0]).get_employee_work_experience_api(
                data['get_employee_work_experience'])
            Assertions().assert_in_text(get_employee_work_experience_res.json()['data'], company_name)

            # 修改员工证件信息
            data['update_employee_certificate']['body']['employeeId'] = setup_class[2]
            data['update_employee_certificate']['body']['employeeBankcardProfileDto']['employeeId'] = setup_class[2]
            data['update_employee_certificate']['body']['employeeBankcardProfileDto']['employeeBankcardDto'][
                'employeeId'] = setup_class[2]
            data['update_employee_certificate']['body']['employeeCertificateProfileDto'][
                'employeeId'] = setup_class[2]
            data['update_employee_certificate']['body']['employeeCertificateProfileDto']['employeeCertificateDtoList'][0][
                'employeeId'] = setup_class[2]
            certificate_name = str(random.randint(1000, 9999))
            data['update_employee_certificate']['body']['employeeCertificateProfileDto']['employeeCertificateDtoList'][0][
                'name'] = certificate_name
            data['update_employee_certificate']['body']['employeeSocialSecurityProvidentFundProfileDto'][
                'employeeId'] = setup_class[2]
            data['update_employee_certificate']['body']['employeeSocialSecurityProvidentFundProfileDto'][
                'employeeSocialSecurityProvidentFundDto']['employeeId'] = setup_class[2]
            update_employee_certificate_res = Profile(setup_class[0]).update_employee_certificate_api(
                data['update_employee_certificate'])
            Assertions().assert_mode(update_employee_certificate_res, data['update_employee_certificate'])

            # 获取员工证件信息
            data['get_employee_certificate']['params']['employeeId'] = setup_class[2]
            get_employee_certificate_res = Profile(setup_class[0]).get_employee_certificate_api(
                data['get_employee_certificate'])
            Assertions().assert_in_text(get_employee_certificate_res.json()['data'], certificate_name)

            # 修改员工合同信息
            data['update_employee_contract']['body']['employeeId'] = setup_class[2]
            data['update_employee_contract']['body']['employeeContractDtos'][0]['laborContractPartiesId'] = get_laborcontractparties_res.json()['data'][0]['id']
            today_time = round(int(time.time()) * 1000)
            data['update_employee_contract']['body']['employeeContractDtos'][0]['beginTime'] = today_time
            data['update_employee_contract']['body']['employeeContractDtos'][0]['endTime'] = today_time
            update_employee_contract_res = EmployeeContract(setup_class[0]).update_employee_contract_api(
                data['update_employee_contract'])
            Assertions().assert_mode(update_employee_contract_res, data['update_employee_contract'])

            # 获取员工合同信息
            data['get_employee_contract']['params']['employeeId'] = setup_class[2]
            get_employee_contract_res = EmployeeContract(setup_class[0]).get_employee_contract_api(
                data['get_employee_contract'])
            # Assertions().assert_in_text(get_employee_contract_res.json()['data'], str(today_time))
            Assertions().assert_in_text(get_employee_contract_res.json()['data'], 1213141414)


if __name__ == '__main__':
    pytest.main(['-sv', 'test_employee_master_data.py', '--env', 'test3'])
