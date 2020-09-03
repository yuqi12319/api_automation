# coding:utf-8
# Name:test_amend_attendance_module.py
# Author:qi.yu
# Time:2020/9/2 3:41 下午
# Description:补卡
import pytest, allure
from Common import log
import random
import Common.consts
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.EmployeeApi.employee import Employee
from TestApi.MuscatApi.muscat import Muscat


class TestAmendAttendance:

    @pytest.fixture(autouse=True)
    def precondition(self, env):
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

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/AmendAttendance/main_scene.yaml'))
    def test_main_scene(self, data):
        with allure.step('第一步：添加补卡审批流'):
            pass


if __name__ == '__main__':
    pytest.main(['-sv', 'test_amend_attendance_module.py', '--env', 'test3'])
