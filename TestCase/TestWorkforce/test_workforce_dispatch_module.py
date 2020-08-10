# coding:utf-8
# Name:test_workforce_dispatch_module.py
# Author:qi.yu
# Time:2020/7/22 2:08 下午

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.WorkforceApi.workforce_dispatch import WorkforceDispatch
from Common.operation_mysql import *


@allure.feature("劳务工派遣模块")
class TestAssign:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.skip
    @allure.story("劳务工派遣接口test")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceDispatch/dispatch.yaml'))
    def test_dispatch(self, data):
        res = WorkforceDispatch(self.env).dispatch_api(data)
        Assertions().assert_mode(res, data)
        # 删除派遣生成的db数据(派遣单，接收单，两者关联关系，派遣人员记录)
        if 'clear' in data.keys():
            selete_assign_sql = "SELECT id FROM workforce_working_assign WHERE workforce_ticket_id = %s" % (
            data['body']['workforceRequestId'])
            id_list = mysql_operate_select_fetchall('dukang_workforce_dktest3', select_sql=selete_assign_sql)

            delete_assign_map_sql = "DELETE FROM workforce_working_assign_map WHERE dispatch_working_assign_id = %s AND receive_working_assign_id = %s" % (
                id_list[0]['id'], id_list[1]['id'])
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_assign_map_sql)

            delete_assign_relation_sql = "DELETE FROM workforce_assign_relation WHERE working_assign_id in (%s, %s) AND employee_id in %s" % (
                id_list[0]['id'], id_list[1]['id'], tuple(data['body']['employeeIds']))
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_assign_relation_sql)

            delete_assign_sql = "DELETE FROM workforce_working_assign WHERE workforce_ticket_id = %s" % (
            data['body']['workforceRequestId'])
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_assign_sql)
        else:
            pass

    @allure.story("劳务工派遣列表test")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceDispatch/dispatch_list.yaml'))
    def test_dispatch_list(self, data):
        res = WorkforceDispatch(self.env).dispatch_list_api(data)
        allure.attach(res.text, "返回结果", allure.attachment_type.JSON)
        Assertions().assert_mode(res, data)

    @allure.story("劳务工派遣详情test")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceDispatch/dispatch_detail.yaml'))
    def test_dispatch_detail(self, data):
        res = WorkforceDispatch(self.env).dispatch_detail_api(data)
        allure.attach(res.text, "返回结果", allure.attachment_type.JSON)
        Assertions().assert_mode(res, data)

    @allure.story("派遣关联申请test")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceDispatch/relevance_apply.yaml'))
    def test_relevance_apply(self, data):
        res = WorkforceDispatch(self.env).relevance_apply_api(data)
        allure.attach(res.text, "返回结果", allure.attachment_type.JSON)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_workforce_dispatch_module.py::TestAssign::test_dispatch"])
