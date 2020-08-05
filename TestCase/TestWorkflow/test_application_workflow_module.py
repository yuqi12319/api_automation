# Name:test_application_workflow_module.py
# Author:lin
# Time:2020/8/5 10:18 上午

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Conf.config import Config
from TestApi.WorkflowApi.application_workflow import ApplicationWorkflow


class TestApplicationWorkfolw:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test3')

    @pytest.mark.skip
    @allure.title("待我审批")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workflow/ApplicationWorkflow/workflow_application.yaml'))
    def test_workflow_application_await(self, data):
        res = ApplicationWorkflow().workfolw_application(self.url_path, data, 'await')
        Assertions.assert_mode(res, data)

    @pytest.mark.skip
    @allure.title("抄送我的")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workflow/ApplicationWorkflow/workflow_application.yaml'))
    def test_workflow_application_cc(self, data):
        res = ApplicationWorkflow().workfolw_application(self.url_path, data, 'cc')
        Assertions.assert_mode(res, data)

    @pytest.mark.skip
    @allure.title('我通过的')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workflow/ApplicationWorkflow/workflow_application.yaml'))
    def test_workflow_application_pass(self, data):
        res = ApplicationWorkflow().workfolw_application(self.url_path, data, 'pass')
        Assertions.assert_mode(res, data)

    @allure.title('我拒绝的')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workflow/ApplicationWorkflow/workflow_application.yaml'))
    def test_workflow_application_refuse(self, data):
        res = ApplicationWorkflow().workfolw_application(self.url_path, data, 'refuse')
        Assertions.assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_application_workflow_module.py'])
