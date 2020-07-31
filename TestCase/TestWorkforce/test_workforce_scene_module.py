# coding:utf-8
# Name:test_workforce_scene_module.py
# Author:qi.yu
# Time:2020/7/29 3:25 下午
# Description:劳务工场景case

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Conf.config import Config
from Common.operation_mysql import *
from TestApi.WorkforceApi.workforce_apply import WorkforceApply
from TestApi.WorkforceApi.workforce_require import WorkforceRequire


class TestWorkforceScene:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test3')

    @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceScene/main_scene.yaml'))
    def test_main_scene(self, data):
        with allure.step('第一步：发送申请单'):
            send_apply_res = WorkforceApply().send_apply_api(self.url_path, data['send_apply'])
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第二步：获取申请列表'):
            apply_list_res = WorkforceApply().apply_list_api(self.url_path, data['apply_list'])
            Assertions().assert_code(apply_list_res.status_code, 200)
            Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
            for item in apply_list_res.json()['data']:
                if item['joinDate'] == data['send_apply']['body']['joinDate']:
                    code = item['code']  # 获取申请id
                    break

        with allure.step('第三步：获取需求列表'):
            require_list_res = WorkforceRequire().require_list_api(self.url_path, data['require_list'])
            Assertions().assert_code(require_list_res.status_code, 200)
            Assertions().assert_in_text(require_list_res.json()['data'], str(code))

        def clear_data():  # 场景执行完毕清理数据操作
            delete_apply_sql = "DELETE FROM workforce_application WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_apply_sql)
            delete_require_sql = "DELETE FROM workforce_ticket WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_require_sql)

        clear_data()

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceScene/stop_apply.yaml'))
    def test_stop_apply(self, data):
        with allure.step('第一步：发送申请单'):
            send_apply_res = WorkforceApply().send_apply_api(self.url_path, data['send_apply'])
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第二步：获取申请列表,判断是否有当前申请单'):
            apply_list_res = WorkforceApply().apply_list_api(self.url_path, data['apply_list'])
            Assertions().assert_code(apply_list_res.status_code, 200)
            Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
            for item in apply_list_res.json()['data']:
                if item['joinDate'] == data['send_apply']['body']['joinDate']:
                    code = item['code']  # 获取申请id
                    application_id = item['applicationId']
                    break

        with allure.step('第三步：获取需求列表，判断乙方是否对应生成需求单'):
            require_list_res = WorkforceRequire().require_list_api(self.url_path, data['require_list'])
            Assertions().assert_code(require_list_res.status_code, 200)
            Assertions().assert_in_text(require_list_res.json()['data'], str(code))

        with allure.step('第四步：停止用工申请'):
            data['stop_apply']['application_id'] = application_id
            stop_apply_res = WorkforceApply().stop_apply_api(self.url_path, data['stop_apply'])
            Assertions().assert_mode(stop_apply_res, data['stop_apply'])

        with allure.step('第五步：重新获取申请列表，判断当前订单状态是否已停止'):
            apply_list_res = WorkforceApply().apply_list_api(self.url_path, data['apply_list'])
            for item in apply_list_res.json()['data']:
                if item['code'] == code:
                    Assertions().assert_text(item['workflowStatus'], 'STOP')
                    break

        def clear_data():   # 场景执行完毕清理数据操作
            delete_apply_sql = "DELETE FROM workforce_application WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_apply_sql)
            delete_require_sql = "DELETE FROM workforce_ticket WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_require_sql)
        clear_data()


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_workforce_scene_module.py'])
