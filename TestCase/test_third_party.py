# coding:utf-8
# Name:test_third_party.py
# Author:qi.yu
# Time:2020/7/7 2:16 下午


import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Robot.api_third_party import ThirdParty
import Common.operation_mysql as mysql


@pytest.fixture(scope='module')
def test_access_open_token():
    url = YamlHandle().read_yaml('ThirdParty/access_open_token.yaml')[0]['url']
    data = YamlHandle().read_yaml('ThirdParty/access_open_token.yaml')[0]['body']
    res = ThirdParty().access_open_token_api(url, data)
    Assertions().assert_text(res.json()['errcode'], '0')
    return res.json()['data']['accessToken']

class TestRefreshOpenToken:

    @allure.feature('第三方系统对接')
    @allure.title('刷新token接口')
    @pytest.mark.skip
    @pytest.mark.parametrize("data",YamlHandle().read_yaml('ThirdParty/refresh_open_token.yaml'))
    def test_refresh_open_token(self, data, test_access_open_token):
        url = data['url']
        data = data['body']
        data.update({'refreshOpenToken': test_access_open_token})
        res = ThirdParty().refresh_open_token_api(url, data)
        if Assertions().assert_code(res['code'], 200):
            Assertions().assert_text(res['json']['errcode'], '0')

class TestRegistCompany:

    @allure.feature('第三方系统对接')
    @allure.title('注册公司接口')
    @pytest.mark.parametrize("data", YamlHandle().read_yaml('ThirdParty/regist_company.yaml'))
    def test_regist_company(self, data, test_access_open_token):
        url = data['url'] + '?x-open-token=' + test_access_open_token
        res = ThirdParty().regist_company_api(url, data['body'])
        if Assertions().assert_code(res.status_code, 200):
            if data['expect']['assert_type'] == 'text_errcode':
                Assertions().assert_text(res.json()['errcode'], data['expect']['expect_result'])
            elif data['expect']['assert_type'] == 'text_errmsg':
                Assertions().assert_text(res.json()['errmsg'], data['expect']['expect_result'])

    def teardown_class(self):
        delect_sql_01 = 'delete from thirdcompanyid_companyid_map where third_co_org_id = "test01"'
        mysql.mysql_operate_insert_update_delete('dukang_businessentry_dktest', delete_sql=delect_sql_01)
        delect_sql_02 = 'delete from company where name = "test_company_01"'
        mysql.mysql_operate_insert_update_delete('bipo_lite_dktest', delete_sql=delect_sql_02)



if __name__ == '__main__':
    pytest.main(['-s', 'test_third_party.py'])
