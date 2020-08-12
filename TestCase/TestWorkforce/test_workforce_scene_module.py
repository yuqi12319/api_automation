# coding:utf-8
# Name:test_workforce_scene_module.py
# Author:qi.yu
# Time:2020/7/29 3:25 下午
# Description:劳务工场景case

import pytest, allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Common.operation_mysql import *
from TestApi.WorkforceApi.workforce_apply import WorkforceApply
from TestApi.WorkforceApi.workforce_require import WorkforceRequire
from Common.request import Request
import Common.consts


@allure.feature("劳务工场景测试")
class TestWorkforceScene:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.skip
    @allure.story("主流程")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceScene/main_scene.yaml'))
    def test_main_scene(self, data):
        with allure.step('第一步：发送申请单'):
            send_apply_res = WorkforceApply(self.env).send_apply_api(data['send_apply'])
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第二步：获取申请列表'):
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            Assertions().assert_code(apply_list_res.status_code, 200)
            Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
            for item in apply_list_res.json()['data']:
                if item['joinDate'] == data['send_apply']['body']['joinDate']:
                    code = item['code']  # 获取申请id
                    break

        with allure.step('第三步：获取需求列表'):
            require_list_res = WorkforceRequire(self.env).require_list_api(data['require_list'])
            Assertions().assert_code(require_list_res.status_code, 200)
            Assertions().assert_in_text(require_list_res.json()['data'], str(code))

        def clear_data():  # 场景执行完毕清理数据操作
            delete_apply_sql = "DELETE FROM workforce_application WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_apply_sql)
            delete_require_sql = "DELETE FROM workforce_ticket WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_require_sql)

        clear_data()

    @pytest.mark.skip
    @allure.story("停止申请")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceScene/stop_apply.yaml'))
    def test_stop_apply(self, data):

        def precondition():

            headers = dict()
            headers['X-Dk-Token'] = Common.consts.ACCESS_TOKEN[0]
            my_companies_url = 'http://dktest3-workio.bipocloud.com/services/muscat/my_companies'
            my_companies_res = Request().get_requests(url=my_companies_url, headers=headers)
            print(my_companies_res.json())
            for item in my_companies_res.json()['data']:
                # 判断当前公司是否有关联劳务公司
                workforce_company_map_url = 'https://dktest3-workio.bipocloud.com/services/dukang-coc/api/company/workforce/map?coOrgId=' + str(
                    item['company_id'])
                workforce_company_map_res = Request().get_requests(url=workforce_company_map_url, headers=headers)
                if workforce_company_map_res.json()['data']:
                    print(workforce_company_map_res.json())
                else:
                    continue
                # 判断当前公司是否是职位信息
                positions_url = 'http://dktest3-workio.bipocloud.com/services/dukang-commission/positions?offset=0&limit=0'
                positions_body = {
                    'coOrgId': item['company_id']
                }
                positions_res = Request().post_requests(url=positions_url, json=positions_body, headers=headers)
                if positions_res.json()['data']:
                    print(positions_res.json())
                else:
                    continue
                # 获取当前员工id
                employeeid_url = 'https://dktest3-workio.bipocloud.com/services/muscat/company/guide/employeeid'
                employeeid_params = {
                    'company_id': item['company_id']
                }
                employeeid_res = Request().get_requests(url=employeeid_url, params=employeeid_params, headers=headers)
                # print(type(employeeid_res.json()['data']))
                # 判断当前公司是否有组织架构
                organizations_trees_url = 'https://dktest3-workio.bipocloud.com/services/muscat/organizations/' + \
                                          employeeid_res.json()['data'] + '/trees'
                organizations_trees_params = {
                    'coOrgId': item['company_id']
                }
                organizations_trees_res = Request().get_requests(url=organizations_trees_url,
                                                                 params=organizations_trees_params, headers=headers)
                if organizations_trees_res.json()['data']:
                    print(organizations_trees_res.json())
                else:
                    continue

                # 数据拼接
                data['send_apply']['body']['coOrgId'] = item['company_id']
                data['send_apply']['body']['coOrgName'] = item['company_name']
                data['send_apply']['body']['labourCompanyId'] = workforce_company_map_res.json()['data'][0][
                    'workforceCompanyId']
                data['send_apply']['body']['labourCompanyName'] = workforce_company_map_res.json()['data'][0][
                    'workforceCompanyName']
                # data['send_apply']['body']['organizationId'] = organizations_trees_res.json()['data'][0]['id']
                # data['send_apply']['body']['organizationName'] = organizations_trees_res.json()['data'][0]['name']
                data['send_apply']['body']['positionId'] = positions_res.json()['data']['positionVoList'][0][
                    'positionId']
                data['send_apply']['body']['positionName'] = positions_res.json()['data']['positionVoList'][0]['name']

        precondition()

        with allure.step('第一步：发送申请单'):
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            send_apply_res = WorkforceApply(self.env).send_apply_api(data['send_apply'])
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第二步：获取申请列表,判断是否有当前申请单'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_code(apply_list_res.status_code, 200)
            Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
            for item in apply_list_res.json()['data']:
                if item['joinDate'] == data['send_apply']['body']['joinDate']:
                    code = item['code']  # 获取申请id
                    application_id = item['applicationId']
                    break

        with allure.step('第三步：获取需求列表，判断乙方是否对应生成需求单'):
            allure.attach(str(data['require_list']), "请求数据", allure.attachment_type.JSON)
            require_list_res = WorkforceRequire(self.env).require_list_api(data['require_list'])
            allure.attach(require_list_res.text, "require_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_code(require_list_res.status_code, 200)
            Assertions().assert_in_text(require_list_res.json()['data'], str(code))

        with allure.step('第四步：停止用工申请'):
            data['stop_apply']['application_id'] = application_id
            allure.attach(str(data['stop_apply']), "请求数据", allure.attachment_type.JSON)
            stop_apply_res = WorkforceApply(self.env).stop_apply_api(data['stop_apply'])
            allure.attach(stop_apply_res.text, "stop_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(stop_apply_res, data['stop_apply'])

        with allure.step('第五步：重新获取申请列表，判断当前订单状态是否已停止'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            for item in apply_list_res.json()['data']:
                if item['code'] == code:
                    Assertions().assert_text(item['workflowStatus'], 'STOP')
                    break

        def clear_data():  # 场景执行完毕清理数据操作
            delete_apply_sql = "DELETE FROM workforce_application WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_apply_sql)
            delete_require_sql = "DELETE FROM workforce_ticket WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_require_sql)

        clear_data()


if __name__ == '__main__':
    pytest.main(["-sv", "test_workforce_scene_module.py", "--env", "test3"])
