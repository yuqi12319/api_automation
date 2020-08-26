# coding:utf-8
# Name:test_login_module.py
# Author:qi.yu
# Time:2020/8/26 3:04 下午
# Description: 登陆模块测试

import pytest, allure
import Common.consts
from Common import log
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.MuscatApi.muscat import Muscat
from TestApi.AttendanceApi.bubble import Bubble
from TestApi.EmployeeApi.employee import Employee


class TestLoginScene:
    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env
        self.log = log.MyLog()

    @pytest.mark.main
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/LoginScene/main_scene.yaml'))
    def test_main_scene(self, data):
        with allure.step('第一步：获取公司列表'):
            my_companies_res = Muscat(self.env).get_my_companies_api()
            if my_companies_res.json()['data']:
                pass
            else:
                self.log.error('当前用户下没有公司列表')

        with allure.step('第二步，进入指定公司'):
            if Common.consts.COMPANY_INFORMATION:
                company_id = Common.consts.COMPANY_INFORMATION[0]['company_id']
                employee_id = Common.consts.COMPANY_INFORMATION[0]['employee_id']
            else:
                company_id = my_companies_res.json()['data'][0]['company_id']
                data['brief_profile']['params']['company_id'] = company_id
                brief_proile_res = Employee(self.env).brief_proile_api(data['brief_profile'])
                employee_id = brief_proile_res.json()['data']['employee_id']

        with allure.step('第三步：获取我的审批数量（气泡接口）'):
            data['get_web_buttles']['params']['coOrgId'] = company_id
            data['get_web_buttles']['params']['employeeId'] = employee_id
            get_web_buttles_res = Bubble(self.env).get_web_bubbles(data['get_web_buttles'])
            Assertions().assert_mode(get_web_buttles_res, data['get_web_buttles'])

        with allure.step('第四步：修改手机号'):
            pass



if __name__ == '__main__':
    pytest.main(['-sv', 'test_login_module.py', '--env', 'test3'])
