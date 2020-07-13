# coding:utf-8
# Name:test_third_party.py
# Author:qi.yu
# Time:2020/7/7 2:16 下午
from Common.operation_yaml import YamlHandle
from Robot.api_third_party import ThirdParty
from Common.request import Request

import pytest
from Common.request import Request
from Common.operation_assert import Assertions

class TestThirdParty:

    def test_get_open_token(self):
        url = YamlHandle('third_party.yaml').get_yaml_value_of_key()['access_open_token']['url']
        data = YamlHandle('third_party.yaml').get_yaml_value_of_key()['access_open_token']['data']
        res =Request().post_requests(url,data)
        if Assertions().assert_code(res['code'], 200):
            Assertions().assert_text(res['json']['errcode'],'0')
            return res

    def test_refresh_open_token(self):
        refreshToken = TestThirdParty().test_get_open_token()['json']['data']['refreshToken']
        url = YamlHandle('third_party.yaml').get_yaml_value_of_key()['refresh_open_token']['url']
        data = YamlHandle('third_party.yaml').get_yaml_value_of_key()['refresh_open_token']['data']
        data.update({'refreshOpenToken':refreshToken})
        res = Request().post_requests(url,data)
        if Assertions().assert_code(res['code'],200):
            Assertions().assert_text(res['json']['errcode'], '0')
            return res

    def test_regist_company(self):
        accessToken = ThirdParty.test_get_open_token()['json']['data']['accessToken']
        url = 'https://dktest-openapi.bipocloud.com/business/openbussiness/companies/registration?'+accessToken
        data = {

        }

if __name__ == '__main__':
    pytest.main(['test_third_party.py'])


