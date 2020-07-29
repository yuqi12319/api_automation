# coding:utf-8
# Name:test_workforce_apply_module.py
# Author:qi.yu
# Time:2020/7/16 10:18 上午
import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.WorkforceApi.workforce_apply import WorkforceApply
from Conf.config import Config
from Common.operation_mysql import *


@allure.feature("甲方劳务工申请模块")
class TestApply:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test3')

    @pytest.mark.skip
    @allure.title("甲方发送劳务工申请")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceApply/apply.yaml'))
    def test_send_apply(self, data):
        res = WorkforceApply().send_apply_api(self.url_path, data)
        Assertions().assert_mode(res, data)
        # 数据库清理(申请单，需求单)
        select_code_sql = "SELECT `code` FROM workforce_application ORDER BY created_time DESC LIMIT 1"
        code = mysql_operate_select_fetchone('dukang_workforce_dktest3',select_sql=select_code_sql)
        delete_application_sql = "DELETE FROM workforce_application WHERE `code` = %s" % (code['code'])
        mysql_operate_insert_update_delete('dukang_workforce_dktest3',delete_sql=delete_application_sql)
        delete_ticket_sql = "DELETE FROM workforce_ticket WHERE `code` = %s" % (code['code'])
        mysql_operate_insert_update_delete('dukang_workforce_dktest3',delete_sql=delete_ticket_sql)


    # @pytest.mark.skip
    @allure.title("甲方劳务工申请列表")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceApply/apply_list.yaml'))
    def test_apply_list(self, data):
        res = WorkforceApply().apply_list_api(self.url_path, data)
        Assertions().assert_mode(res, data)

    @pytest.mark.skip
    @allure.title("甲方劳务工申请详情")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceApply/apply_detail.yaml'))
    def test_apply_detail(self, data):
        res = WorkforceApply().apply_detail_api(self.url_path, data)
        Assertions().assert_mode(res, data)



if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_workforce_apply_module.py"])
