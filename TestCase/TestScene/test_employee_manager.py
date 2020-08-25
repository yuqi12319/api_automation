# Name:test_employee_unactive.py
# Author:lin
# Time:2020/8/25 10:00 上午


import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.EmployeeApi.workforce_employee_domain import WorkforceEmployeeDomain
from TestApi.MuscatApi.muscat import Muscat
import Common.consts


class TestEmployeeActive:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/EmployeeManagerScene/main_scene.yaml'))
    def test_main_sence(self, data):
        with allure.step('第一步，获取员工未激活集合'):
            # 获取flow_id
            flow_id_res = Muscat(self.env).get_flow_id()

            data['unactvie']['headers']['x-dk-token'] = Common.consts.ACCESS_TOKEN[0]
            employee_unactive_res = WorkforceEmployeeDomain(self.env).employee_unactice(data['unactvie'])
            print(employee_unactive_res)
        #
        # with allure.step('第二步，根据手机号获取验证码'):
        #     # 发送验证码
        #     data['vcode']['headers']['x-flow-id'] = flow_id_res.json()['data']
        #     vcode_res = Muscat(self.env).vcode_api(data['vcode'])
        #     Assertions().assert_mode(vcode_res, data['vcode'])
        #
        #     # 校验验证码
        #     data['vcode_check']['headers']['x-flow-id'] = flow_id_res.json()['data']
        #     vcode_check_res = Muscat(self.env).vcode_check_api(data['vcode_check'])
        #     Assertions().assert_mode(vcode_check_res, data['vcode_check'])

        with allure.step('第三部，校验员工是否能通过邀请链接加入到公司'):
            mobile = list()
            for i in range(len(employee_unactive_res.json()['data'])):
                mobile.append(employee_unactive_res.json()['data'][i]['mobile'])
            print(mobile)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_employee_manager.py', '--env', 'test3'])
