# Name:test_delete_leave_approval_setting.py
# Author:michelle.hou
# Time:2020-08-06 11:46
import allure
import pytest
from Common.operation_assert import *
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.WorkflowApi.teamleaveform_setting import TeamLeaveApprovalSetting


class TestDeleteApproval:
    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test1')

    @allure.title("删除团队休假审批列表")
    @pytest.mark.parametrize("data",YamlHandle().read_yaml('Workflow/delete_team_leave_approval.yaml'))
    def test_team_leave_approval_setting(self, data):
        print(data)
        res = TeamLeaveApprovalSetting().delete_team_leave_approval(self.url_path, data)
        print(type(res))
        print(res.json())
        print(res.url)
        Assertions().assert_mode(res, data)

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main(['-s', 'test_overtime_apply.py'])
