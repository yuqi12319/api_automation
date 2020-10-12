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
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.UserApi.third_sys_user_api import ThirdSysUserApi


class TestLoginScene:
    @pytest.fixture(autouse=True)
    def setupClass(self, env):
        self.env = env
        self.log = log.MyLog()

    # @pytest.mark.dependency()
    @pytest.mark.skip
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
                brief_proile_res = EmployeeApi(self.env).brief_profile_api(data['brief_profile'])
                employee_id = brief_proile_res.json()['data']['employee_id']
            Common.consts.COMPANY_ID.append(company_id)
            Common.consts.EMPLOYEE_ID.append(employee_id)

        with allure.step('第三步：获取我的审批数量（气泡接口）'):
            data['get_web_buttles']['params']['coOrgId'] = company_id
            data['get_web_buttles']['params']['employeeId'] = employee_id
            get_web_buttles_res = Bubble(self.env).get_web_bubbles(data['get_web_buttles'])
            Assertions().assert_mode(get_web_buttles_res, data['get_web_buttles'])

        # with allure.step('第四步：修改手机号'):
        #     # 获取flow_id
        #     flow_id_res = Muscat(self.env).get_flow_id()
        #
        #     # 发送验证码
        #     data['vcode']['headers']['x-flow-id'] = flow_id_res.json()['data']
        #     vcode_res = Muscat(self.env).vcode_api(data['vcode'])
        #     Assertions().assert_mode(vcode_res, data['vcode'])
        #
        #     # 校验验证码
        #     data['vcode_check']['headers']['x-flow-id'] = flow_id_res.json()['data']
        #     data['vcode_check']['params']['mobile_number'] = data['vcode']['params']['mobile_number']
        #     vcode_check_res = Muscat(self.env).vcode_check_api(data['vcode_check'])
        #     Assertions().assert_mode(vcode_check_res, data['vcode_check'])
        #
        #     # 修改手机号
        #     data['change_phone_number']['body']['employeeId'] = employee_id
        #     data['change_phone_number']['body']['newNumber'] = data['vcode']['params']['mobile_number']
        #     change_phone_number_res = ThirdSysUserApi(self.env).change_phone_number_api(data['change_phone_number'])
        #     Assertions().assert_mode(change_phone_number_res, data['change_phone_number'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_login_module.py', '--env', 'test3'])
