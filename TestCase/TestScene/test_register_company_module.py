# coding:utf-8
# Name:test_register_company_module.py
# Author:qi.yu
# Time:2020/8/21 3:54 下午
# Description:

import pytest, allure
from Common.request import Request
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
import Common.consts
from TestApi.MuscatApi.muscat import Muscat
from TestApi.WorkflowApi.workflow_domain import WorkflowDomain
import Common.consts


class TestRegisterCompanyScene:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/RegisterComapnyScene/main_scene.yaml'))
    def test_main_scene(self, data):
        with allure.step('第一步：创建公司'):
            # 获取flow_id
            flow_id_res = Muscat(self.env).get_flow_id()

            # 发送验证码
            data['vcode']['headers']['x-flow-id'] = flow_id_res.json()['data']
            vcode_res = Muscat(self.env).vcode_api(data['vcode'])
            Assertions().assert_mode(vcode_res, data['vcode'])

            # 校验验证码
            data['vcode_check']['headers']['x-flow-id'] = flow_id_res.json()['data']
            vcode_check_res = Muscat(self.env).vcode_check_api(data['vcode_check'])
            Assertions().assert_mode(vcode_check_res, data['vcode_check'])

            # 注册公司
            data['register_company']['headers']['x-flow-id'] = flow_id_res.json()['data']
            regist_company_res = Muscat(self.env).register_comapny_api(data['register_company'])
            Assertions().assert_mode(regist_company_res, data['register_company'])

        with allure.step('第二步：校验是否生成默认审批流'):
            # 默认账单审批流判断
            data['default_bill_approval']['params']['coOrgId'] = regist_company_res.json()['data']['company_id']
            bill_approval_list_res = WorkflowDomain(self.env).bill_approval_list_api(data['default_bill_approval'])
            Assertions().assert_in_text(bill_approval_list_res.json()['data'], '默认账单审批流')

            # 默认用工申请审批流判断
            data['default_workforce_apply_approval']['params']['coOrgId'] = regist_company_res.json()['data'][
                'company_id']
            workforce_apply_approval_list_res = WorkflowDomain(self.env).workforce_apply_approval_list_api(
                data['default_workforce_apply_approval'])
            Assertions().assert_in_text(workforce_apply_approval_list_res.json()['data'], '默认用工申请审批流')

            # 默认用工登记审批流判断
            data['default_workforce_register_approval']['params']['coOrgId'] = regist_company_res.json()['data'][
                'company_id']
            workforce_register_approval_list_res = WorkflowDomain(self.env).workforce_register_approval_list_api(
                data['default_workforce_register_approval'])
            Assertions().assert_in_text(workforce_register_approval_list_res.json()['data'], '默认用工登记审批流')

        with allure.step('解散公司'):
            data['dissolve_company']['companyId'] = regist_company_res.json()['data']['company_id']
            dissolve_company_res = Muscat(self.env).dissolve_company(data['dissolve_company'])
            Assertions().assert_mode(dissolve_company_res, data['dissolve_company'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_register_company_module.py', '--env', 'test3'])