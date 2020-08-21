# Name:test_delete_approval.py
# Author:michelle.hou
# Time:2020-08-06 11:46
import allure
import pytest
from Common.operation_assert import *
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.Approval_Api.teamleaveform_setting import TeamLeaveApprovalSetting


class TestDeleteApproval:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @allure.title("删除团队休假审批列表")
    @pytest.mark.parametrize("data",YamlHandle().read_yaml('SingleInterfaceData/Approval/delete_team_leave_approval.yaml'))
    def test_team_leave_approval_setting(self, data):
        res = TeamLeaveApprovalSetting(self.env).delete_team_leave_approval(data)
        print(type(res))
        print(res.json())
        print(res.url)
        Assertions().assert_mode(res, data)

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main(['-s', 'test_overtime.py'])
