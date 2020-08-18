# Name:test_workforce_workflow_module.py
# Author:lin
# Time:2020/8/5 10:18 上午

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.WorkforceApi.workforce_workflow import WorkforceWorkflow


class TestApplicationWorkflow:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.skip
    @allure.title("申请待我审批")
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('Workforce/WorkforceWorkflow/workflow_application_await.yaml'))
    def test_workflow_application_await(self, data):
        res = WorkforceWorkflow(self.env).workflow_application_await_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title("申请抄送我的")
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('Workforce/WorkforceWorkflow/workflow_application_await.yaml'))
    def test_workflow_application_cc(self, data):
        res = WorkforceWorkflow(self.env).workflow_application_cc_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title('申请我通过的')
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('Workforce/WorkforceWorkflow/workflow_application_await.yaml'))
    def test_workflow_application_pass(self, data):
        res = WorkforceWorkflow(self.env).workflow_application_pass_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title('申请我拒绝的')
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('Workforce/WorkforceWorkflow/workflow_application_await.yaml'))
    def test_workflow_application_refuse(self, data):
        res = WorkforceWorkflow(self.env).workflow_application_refuse_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title("登记待我审批")
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('Workforce/WorkforceWorkflow/workflow_registration_await.yaml'))
    def test_workflow_registration_await(self, data):
        res = WorkforceWorkflow(self.env).workflow_registration_await_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title("登记抄送我的")
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('Workforce/WorkforceWorkflow/workflow_registration_cc.yaml'))
    def test_workflow_registration_cc(self, data):
        res = WorkforceWorkflow(self.env).workflow_registration_cc_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title('登记我通过的')
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('Workforce/WorkforceWorkflow/workflow_registration_pass.yaml'))
    def test_workflow_registration_pass(self, data):
        res = WorkforceWorkflow(self.env).workflow_registration_pass_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title('登记我拒绝的')
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('Workforce/WorkforceWorkflow/workflow_registration_refuse.yaml'))
    def test_workflow_registration_refuse(self, data):
        res = WorkforceWorkflow(self.env).workflow_registration_refuse_list_api(data)
        Assertions().assert_mode(res, data)

    @allure.title('已有公司添加用工申请默认审批流')
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml(
                                 'Workforce/WorkforceWorkflow/workforce_application_workflow_default.yaml'))
    def test_set_workforce_application_workflow_default(self, data):
        res = WorkforceWorkflow(self.env).application_workflow_setting_default_api(data)
        Assertions().assert_mode(res, data)

    @allure.title('已有公司添加用工登记默认审批流')
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml(
                                 'Workforce/WorkforceWorkflow/workforce_registration_workflow_default.yaml'))
    def test_set_workforce_registration_workflow_default(self, data):
        res = WorkforceWorkflow(self.env).registration_workflow_setting_default_api(data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_workforce_workflow_module.py'])
