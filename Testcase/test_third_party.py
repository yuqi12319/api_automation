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
        url = YamlHandle().read_yaml('third_party.yaml')['access_open_token']['url']
        data = YamlHandle().read_yaml('third_party.yaml')['access_open_token']['data']
        res = Request().post_requests(url, data)
        if Assertions().assert_code(res['code'], 200):
            Assertions().assert_text(res['json']['errcode'], '0')
            return res

    def test_refresh_open_token(self):
        refresh_token = TestThirdParty().test_get_open_token()['json']['data']['refreshToken']
        url = YamlHandle().read_yaml('third_party.yaml')['refresh_open_token']['url']
        data = YamlHandle().read_yaml('third_party.yaml')['refresh_open_token']['data']
        data.update({'refreshOpenToken': refresh_token})
        res = Request().post_requests(url, data)
        if Assertions().assert_code(res['code'], 200):
            Assertions().assert_text(res['json']['errcode'], '0')
            return res

    # def test_regist_company(self):
    #     accessToken = ThirdParty.test_get_open_token()['json']['data']['accessToken']
    #     url = 'https://dktest-openapi.bipocloud.com/business/openbussiness/companies/registration
    #     data = {
    #
    #     }


if __name__ == '__main__':
    pytest.main(['test_third_party.py'])
