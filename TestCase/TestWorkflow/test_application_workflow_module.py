# Name:test_application_workflow_module.py
# Author:lin
# Time:2020/8/5 10:18 上午

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.WorkflowApi.workforce_workflow import WorkforceWorkflow


class TestApplicationWorkflow:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.skip
    @allure.title("待我审批")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Workforce_Workflow/ApplicationWorkflow/workflow_application_await.yaml'))
    def test_workflow_application_await(self, data):
        res = WorkforceWorkflow(self.env).workflow_application_await_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title("抄送我的")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Workforce_Workflow/ApplicationWorkflow/workflow_application_await.yaml'))
    def test_workflow_application_cc(self, data):
        res = WorkforceWorkflow(self.env).workflow_application_cc_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title('我通过的')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Workforce_Workflow/ApplicationWorkflow/workflow_application_await.yaml'))
    def test_workflow_application_pass(self, data):
        res = WorkforceWorkflow(self.env).workflow_application_pass_list_api(data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title('我拒绝的')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        'Workforce_Workflow/ApplicationWorkflow/workflow_application_await.yaml'))
    def test_workflow_application_refuse(self, data):
        res = WorkforceWorkflow(self.env).workflow_application_refuse_list_api(data)
        Assertions().assert_mode(res, data)

    @allure.title('已有公司添加用工申请默认审批流')
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('Workforce/WorkflowDefault/application_workflow_default.yaml'))
    def test_application_workflow_setting_default(self, data):
        res = WorkforceWorkflow(self.env).application_workflow_setting_default_api(data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_application_workflow_module.py'])
