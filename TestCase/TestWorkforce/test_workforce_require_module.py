# coding:utf-8
# Name:test_workforce_require_module.py
# Author:qi.yu
# Time:2020/7/16 5:23 下午
import pytest
from Common.operation_yaml import YamlHandle
from Common.request import Request
from Common.operation_assert import Assertions
from Robot.Workforce.workforce_require import WorkforceRequire


class TestRequire:

    @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/SecondParty/require_list.yaml'))
    def test_require_list(self, data):
        res = WorkforceRequire().require_list_api(data)
        if Assertions().assert_code(res.status_code, 200):
            Assertions().assert_text(res.json()['errcode'], '0')

    # @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/SecondParty/require_detail.yaml'))
    def test_require_detail(self, data):
        res = WorkforceRequire().require_detail_api(data)
        if Assertions().assert_code(res.status_code, 200):
            Assertions().assert_text(res.json()['errcode'], '0')


if __name__ == '__main__':
    pytest.main(['-s', 'test_workforce_require_module.py'])
