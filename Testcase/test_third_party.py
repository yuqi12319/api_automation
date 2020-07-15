# coding:utf-8
# Name:test_third_party.py
# Author:qi.yu
# Time:2020/7/7 2:16 下午


import pytest
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Robot.api_third_party import ThirdParty
import Common.operation_mysql as mysql


@pytest.fixture(scope='module')
def test_access_open_token():
    url = YamlHandle().read_yaml('third_party/access_open_token.yaml')['access_open_token_01']['url']
    data = YamlHandle().read_yaml('third_party/access_open_token.yaml')['access_open_token_01']['data']
    res = ThirdParty().access_open_token_api(url, data)
    Assertions().assert_text(res['json']['errcode'], '0')
    return res['json']['data']['accessToken']


class TestRefreshOpenToken:

    @pytest.mark.skip
    def test_refresh_open_token(self, test_access_open_token):
        url = YamlHandle().read_yaml('third_party/refresh_open_token.yaml')['refresh_open_token_01']['url']
        data = YamlHandle().read_yaml('third_party/refresh_open_token.yaml')['refresh_open_token_01']['data']
        data.update({'refreshOpenToken': test_access_open_token})
        res = ThirdParty().refresh_open_token_api(url, data)
        if Assertions().assert_code(res['code'], 200):
            Assertions().assert_text(res['json']['errcode'], '0')


class TestRegistCompany:

    # @pytest.mark.skip
    @pytest.mark.parametrize("url,data,expect", YamlHandle().read_yaml_return_list('third_party/regist_company.yaml'))
    def test_regist_company(self, url, data, expect, test_access_open_token):
        url = url + '?x-open-token=' + test_access_open_token
        res = ThirdParty().regist_company_api(url, data)
        if Assertions().assert_code(res['code'], 200):
            if expect['assert_type'] == 'text_errcode':
                Assertions().assert_text(res['json']['errcode'], expect['expect_result'])
            elif expect['assert_type'] == 'text_errmsg':
                Assertions().assert_text(res['json']['errmsg'], expect['expect_result'])

    def teardown_class(self):
        delect_sql_01 = 'delete from thirdcompanyid_companyid_map where third_co_org_id = "test01"'
        mysql.mysql_operate_insert_update_delete('dukang_businessentry_dktest', delete_sql=delect_sql_01)
        delect_sql_02 = 'delete from company where name = "test_company_01"'
        mysql.mysql_operate_insert_update_delete('bipo_lite_dktest', delete_sql=delect_sql_02)


if __name__ == '__main__':
    pytest.main(['-s', 'test_third_party.py'])
