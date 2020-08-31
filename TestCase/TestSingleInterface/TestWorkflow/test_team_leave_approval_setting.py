# Name:test_team_leave_approval_setting.py
# Author:michelle.hou
# Time:2020-08-05 17:18
import pytest
import allure
from Common.operation_assert import *
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.WorkflowApi.teamleaveform_setting import TeamLeaveApprovalSetting


@allure.feature('团队休假审批流设置')
class TestApprovalSetting:
    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @allure.title("新增团队休假审批")
    @pytest.mark.parametrize("data", YamlHandle().read_yaml('SingleInterfaceData/Workflow/team_leave_approval_setting.yaml'))
    def test_team_leave_approval_setting(self, data):
        res = TeamLeaveApprovalSetting(self.env).creat_team_leave_approval(data)
        Assertions().assert_mode(res, data)

    @allure.title("获取团队休假审批列表")
    @pytest.mark.parametrize("data", YamlHandle().read_yaml('SingleInterfaceData/Workflow/get_team_leave_approval_list.yaml'))
    def test_get_team_leave_approval_list(self, data):
        res = TeamLeaveApprovalSetting(self.env).get_team_leave_approval(data)
        getlist = res.json()
        num = getlist['data']['totalNum']
        if num is None:

            w_id = getlist['data']['workflowSettingVoList'][0]['workflowSettingId']
            print(w_id)
            # print("workflowSettingId= %s" % getlist['data']['workflowSettingVoList'][0]['workflowSettingId'])
            # a = YamlHandle().read_yaml('Workflow/delete_team_leave_approval.yaml')
            YamlHandle().write_yaml('Workflow/delete_team_leave_approval.yaml', 'url', '/dukang-workflow/api/workflow_setting/'+w_id)
            Assertions().assert_mode(res, data)
        else:
            print("团队休假列表为空，请检查")

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main(['-s', 'test_overtime_apply.py', '--env', 'test1'])

