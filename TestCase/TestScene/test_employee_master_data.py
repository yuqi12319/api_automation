# coding:utf-8
# Name:test_employee_master_data.py
# Author:qi.yu
# Time:2020/8/27 10:50 上午
# Description: 员工管理

import pytest, allure
from Common import log
import Common.consts
import random
import time
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.CommissionApi.positon import Position
from TestApi.EmployeeApi.employee import Employee
from TestApi.MuscatApi.muscat import Muscat
from TestApi.EmployeeApi.rank import Rank
from TestApi.EmployeeApi.cost_center import CostCenter
from TestApi.EmployeeApi.labor_contract_parties import LaborContractParties
from TestApi.EmployeeApi.profile import Profile
from TestApi.EmployeeApi.employee_contract import EmployeeContract


class TestEmployeeManager:

    @pytest.fixture(autouse=True)
    def setupClass(self, env):
        self.env = env
        self.log = log.MyLog()
        if Common.consts.COMPANY_INFORMATION:
            company_id = Common.consts.COMPANY_INFORMATION[0]['company_id']
            employee_id = Common.consts.COMPANY_INFORMATION[0]['employee_id']
        else:
            my_companies_res = Muscat(self.env).get_my_companies_api()
            if my_companies_res.json()['data']:
                company_id = my_companies_res.json()['data'][0]['company_id']
                brief_profile_data = YamlHandle().read_yaml('SingleInterfaceData/Employee/brief_profile.yaml')[0]
                brief_profile_data['params']['company_id'] = company_id
                brief_profile_res = Employee(self.env).brief_profile_api(brief_profile_data)
                employee_id = brief_profile_res.json()['data']['employee_id']
            else:
                self.log.error('当前用户下没有公司列表')
        self.company_id = company_id
        self.employee_id = employee_id

    # @pytest.mark.smoke
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/EmployeeMasterDataScene/main_scene.yaml'))
    def test_main_scene(self, data):

        with allure.step('第一步：获取第一页员工管理列表数据'):
            data['get_employee_manager_list']['params']['company_id'] = self.company_id
            data['get_employee_manager_list']['headers']['x-dk-token'] = Common.consts.ACCESS_TOKEN[0]
            get_employee_manager_list_res = Employee(self.env).get_employee_manager_list(
                data['get_employee_manager_list'])
            Assertions().assert_mode(get_employee_manager_list_res, data['get_employee_manager_list'])

        with allure.step('第二步：组织信息设置'):
            # 添加职级
            data['add_rank']['body']['coOrgId'] = self.company_id
            add_rank_res = Rank(self.env).add_rank_api(data['add_rank'])
            Assertions().assert_mode(add_rank_res, data['add_rank'])

            # 查看职级
            data['get_rank']['params']['coOrgId'] = self.company_id
            get_rank_res = Rank(self.env).get_rank_api(data['get_rank'])
            Assertions().assert_in_text(get_rank_res.json()['data'], data['add_rank']['body']['name'])

            # 添加职位
            data['add_position']['body']['coOrgId'] = self.company_id
            add_position_res = Position(self.env).add_position_api(data['add_position'])
            Assertions().assert_mode(add_position_res, data['add_position'])

            # 查看职位
            data['get_position']['body']['coOrgId'] = self.company_id
            get_position_res = Position(self.env).get_position_api(data['get_position'])
            Assertions().assert_in_text(get_position_res.json()['data'], data['add_position']['body']['name'])
            
            # 添加劳动合同主体
            data['add_laborcontractparties']['body']['coOrgId'] = self.company_id
            add_laborcontractparties_res = LaborContractParties(self.env).add_laborcontractparties_api(
                data['add_laborcontractparties'])
            Assertions().assert_mode(add_laborcontractparties_res, data['add_laborcontractparties'])

            # 查看劳动合同主体
            data['get_laborcontractparties']['params']['coOrgId'] = self.company_id
            get_laborcontractparties_res = LaborContractParties(self.env).get_laborcontractparties_api(
                data['get_laborcontractparties'])
            Assertions().assert_in_text(get_laborcontractparties_res.json()['data'], data['add_laborcontractparties']['body']['name'])

            # 添加成本中心
            data['add_costcenter']['body']['coOrgId'] = self.company_id
            add_costcenter_res = CostCenter(self.env).add_costcenter_api(data['add_costcenter'])
            Assertions().assert_mode(add_costcenter_res, data['add_costcenter'])

            # 查看成本中心
            data['get_costcenter']['params']['coOrgId'] = self.company_id
            get_costcenter_res = CostCenter(self.env).get_costcenter_api(data['get_costcenter'])
            Assertions().assert_in_text(get_costcenter_res.json()['data'], data['add_costcenter']['body']['name'])

        with allure.step('第三步：修改,查看员工信息'):
            # 获取员工组织信息
            data['get_employee_organization']['employee_id'] = self.employee_id
            data['get_employee_organization']['params']['company_id'] = self.company_id
            get_employee_organization_res = Employee(self.env).get_employee_organization_api(
                data['get_employee_organization'])
            Assertions().assert_mode(get_employee_organization_res, data['get_employee_organization'])

            # 修改员工组织信息
            data['update_employee_organization']['employee_id'] = self.employee_id
            data['update_employee_organization']['body']['department_ids'].append(
                get_employee_organization_res.json()['data']['department_infos'][0]['id'])
            data['update_employee_organization']['body']['department_infos'].append(
                get_employee_organization_res.json()['data']['department_infos'][0])
            data['update_employee_organization']['body']['employee_id'] = self.employee_id
            data['update_employee_organization']['body']['laborContractPartiesName'] = get_laborcontractparties_res.json()['data'][0]['name']
            update_employee_organization_res = Employee(self.env).update_employee_organization_api(
                data['update_employee_organization'])
            Assertions().assert_mode(update_employee_organization_res, data['update_employee_organization'])

            # 获取员工个人信息
            data['get_employee_information']['employee_id'] = self.employee_id
            get_employee_information_res = Employee(self.env).get_employee_information_api(
                data['get_employee_information'])
            Assertions().assert_mode(get_employee_information_res, data['get_employee_information'])

            # 修改员工个人信息
            data['update_employee_information']['body']['created_time'] = get_employee_information_res.json()['data'][
                'created_time']
            data['update_employee_information']['body']['updated_time'] = round(int(time.time()) * 1000)
            data['update_employee_information']['body']['displayName'] = get_employee_information_res.json()['data'][
                'displayName']
            data['update_employee_information']['body']['employeeId'] = self.employee_id
            data['update_employee_information']['body']['mobile_area_code'] = get_employee_information_res.json()['data']['mobile_area_code']
            data['update_employee_information']['body']['phone_number'] = get_employee_information_res.json()['data'][
                'phone_number']
            personEmail = str(random.randint(100, 999)) + '@' + str(random.randint(100, 999)) + '.com'
            data['update_employee_information']['body']['personEmail'] = personEmail
            update_employee_information_res = Employee(self.env).update_employee_information_api(
                data['update_employee_information'])
            Assertions().assert_mode(update_employee_information_res, data['update_employee_information'])

            # 修改员工教育信息
            data['update_employee_education']['body']['employeeId'] = self.employee_id
            major = str(random.randint(1000, 9999))
            data['update_employee_education']['body']['educations'][0]['major'] = major
            update_employee_education_res = Employee(self.env).update_employee_education_api(
                data['update_employee_education'])
            Assertions().assert_mode(update_employee_education_res, data['update_employee_education'])

            # 获取员工教育信息
            data['get_employee_education']['employee_id'] = self.employee_id
            get_employee_education_res = Employee(self.env).get_employee_education_api(data['get_employee_education'])
            Assertions().assert_in_text(get_employee_education_res.json()['data'], major)

            # 修改员工工作经历
            data['update_employee_work_experience']['body']['employeeId'] = self.employee_id
            company_name = str(random.randint(1000, 9999))
            data['update_employee_work_experience']['body']['work_experiences'][0]['company'] = company_name
            update_employee_work_experience_res = Employee(self.env).update_employee_work_experience_api(
                data['update_employee_work_experience'])
            Assertions().assert_mode(update_employee_work_experience_res, data['update_employee_work_experience'])

            # 获取员工工作信息
            data['get_employee_work_experience']['employee_id'] = self.employee_id
            get_employee_work_experience_res = Employee(self.env).get_employee_work_experience_api(
                data['get_employee_work_experience'])
            Assertions().assert_in_text(get_employee_work_experience_res.json()['data'], company_name)

            # 修改员工证件信息
            data['update_employee_certificate']['body']['employeeId'] = self.employee_id
            data['update_employee_certificate']['body']['employeeBankcardProfileDto']['employeeId'] = self.employee_id
            data['update_employee_certificate']['body']['employeeBankcardProfileDto']['employeeBankcardDto'][
                'employeeId'] = self.employee_id
            data['update_employee_certificate']['body']['employeeCertificateProfileDto'][
                'employeeId'] = self.employee_id
            data['update_employee_certificate']['body']['employeeCertificateProfileDto']['employeeCertificateDtoList'][0][
                'employeeId'] = self.employee_id
            certificate_name = str(random.randint(1000, 9999))
            data['update_employee_certificate']['body']['employeeCertificateProfileDto']['employeeCertificateDtoList'][0][
                'name'] = certificate_name
            data['update_employee_certificate']['body']['employeeSocialSecurityProvidentFundProfileDto'][
                'employeeId'] = self.employee_id
            data['update_employee_certificate']['body']['employeeSocialSecurityProvidentFundProfileDto'][
                'employeeSocialSecurityProvidentFundDto']['employeeId'] = self.employee_id
            update_employee_certificate_res = Profile(self.env).update_employee_certificate_api(
                data['update_employee_certificate'])
            Assertions().assert_mode(update_employee_certificate_res, data['update_employee_certificate'])

            # 获取员工证件信息
            data['get_employee_certificate']['params']['employeeId'] = self.employee_id
            get_employee_certificate_res = Profile(self.env).get_employee_certificate_api(
                data['get_employee_certificate'])
            Assertions().assert_in_text(get_employee_certificate_res.json()['data'], certificate_name)

            # 修改员工合同信息
            data['update_employee_contract']['body']['employeeId'] = self.employee_id
            data['update_employee_contract']['body']['employeeContractDtos'][0]['laborContractPartiesId'] = get_laborcontractparties_res.json()['data'][0]['id']
            today_time = round(int(time.time()) * 1000)
            data['update_employee_contract']['body']['employeeContractDtos'][0]['beginTime'] = today_time
            data['update_employee_contract']['body']['employeeContractDtos'][0]['endTime'] = today_time
            update_employee_contract_res = EmployeeContract(self.env).update_employee_contract_api(
                data['update_employee_contract'])
            Assertions().assert_mode(update_employee_contract_res, data['update_employee_contract'])

            # 获取员工合同信息
            data['get_employee_contract']['params']['employeeId'] = self.employee_id
            get_employee_contract_res = EmployeeContract(self.env).get_employee_contract_api(
                data['get_employee_contract'])
            Assertions().assert_in_text(get_employee_contract_res.json()['data'], str(today_time))


if __name__ == '__main__':
    pytest.main(['-sv', 'test_employee_master_data.py', '--env', 'test3'])
