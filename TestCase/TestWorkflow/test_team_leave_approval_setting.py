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
    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test1')

    @allure.title("新增团队休假审批")
    @pytest.mark.parametrize("data", YamlHandle().read_yaml('Workflow/team_leave_approval_setting.yaml'))
    def test_team_leave_approval_setting(self, data):
        print(data)
        res = TeamLeaveApprovalSetting().creat_team_leave_approval(self.url_path, data)
        print(type(res))
        print(res.json())
        print(res.url)
        print(res.request)
        Assertions().assert_mode(res, data)

    @allure.title("获取团队休假审批列表")
    @pytest.mark.parametrize("data", YamlHandle().read_yaml('Workflow/get_team_leave_approval_list.yaml'))
    def test_get_team_leave_approval_list(self, data):

        print(data)
        res = TeamLeaveApprovalSetting().get_team_leave_approval(self.url_path, data)
        # getlist = res.json()
        # print(getlist.get("response").get("workflowSettingId"))
        print(res.json())
        print(res.url)
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
    pytest.main(['-s', 'test_overtime_apply.py'])

