# coding:utf-8
# Name:test_payroll.py
# Author:qi.yu
# Time:2020/6/25 10:54 下午

import pytest
import allure

from Common.operation_assert import *
from Common.operation_yaml import YamlHandle
from Robot.api_robot import Payroll
from Conf.config import Config


class TestPayroll:
    @pytest.mark.high
    def test_payrollItem_list_api(self):
        url = Config().get_conf('test_env', 'test2') + YamlHandle().read_yaml('payroll.yaml')['payrollItem_list_api'][
            'url']
        data = YamlHandle().read_yaml('payroll.yaml')['payrollItem_list_api']['data']
        headers = {'x-dk-token': YamlHandle().read_yaml('login.yaml')['login']['accessToken']}
        res = Payroll().get_payrollItem_list_api(url, data, headers)
        Assertions().assert_code(res['json']['errcode'], '0')

    @pytest.mark.smoke
    def test_paygroup_list_api(self, login):
        url = Config().get_conf('test_env', 'test2') + YamlHandle().read_yaml('payroll.yaml')['paygroup_list_api'][
            'url']
        data = YamlHandle().read_yaml('payroll.yaml')['paygroup_list_api']['data']
        headers = YamlHandle().read_yaml('payroll.yaml')['paygroup_list_api']['headers']
        headers.update({'x-dk-token': YamlHandle().read_yaml('login.yaml')['login']['accessToken']})
        res = Payroll().get_paygroup_list_api(url, data, headers)
        Assertions().assert_code(res['json']['errcode'], '0')


if __name__ == '__main__':
    pytest.main(['-s', 'test_payroll.py'])