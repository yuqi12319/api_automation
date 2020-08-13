# Name:test_registration_workflow_module.py
# Author:lin
# Time:2020/8/12 5:42 下午

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.WorkflowApi.application_workflow import Workflow

# 登记审批流相关接口
class TestRegistrationWorkfolw:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.skip
    @allure.title("待我审批")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Workforce_Workflow/ApplicationWorkflow/workflow_registration_await.yaml'))
    def test_workflow_registration_await(self, data):
        res = Workflow(self.env).workflow_registration_await_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title("抄送我的")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Workforce_Workflow/RegistrationWorkflow/workflow_registration_cc.yaml'))
    def test_workflow_registration_cc(self, data):
        res = Workflow(self.env).workflow_registration_cc_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title('我通过的')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Workforce_Workflow/RegistrationWorkflow/workflow_registration_pass.yaml'))
    def test_workflow_registration_pass(self, data):
        res = Workflow(self.env).workflow_registration_pass_list_api(data)
        Assertions().assert_mode(res, data)

    @allure.title('我拒绝的')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Workforce_Workflow/RegistrationWorkflow/workflow_registration_refuse.yaml'))
    def test_workflow_registration_refuse(self, data):
        res = Workflow(self.env).workflow_registration_refuse_list_api(data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_registration_workflow_module.py'])
