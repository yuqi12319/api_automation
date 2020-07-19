# coding:utf-8
# Name:test_workforce_apply_module.py
# Author:qi.yu
# Time:2020/7/16 10:18 上午
import pytest
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Robot.Workforce.workforce_apply import WorkforceApply


class TestApply:

    @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/FirstParty/apply.yaml'))
    def test_send_apply(self, data):
        res = WorkforceApply().send_apply_api(data)
        if Assertions().assert_code(res.status_code, 200):
            Assertions().assert_text(res.json()['errcode'], '0')

    @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/FirstParty/apply_list.yaml'))
    def test_apply_list(self, data):
        res = WorkforceApply().apply_list_api(data)
        if Assertions().assert_code(res.status_code, 200):
            Assertions().assert_text(res.json()['errcode'], '0')

    @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/FirstParty/apply_detail.yaml'))
    def test_apply_detail(self, data):
        res = WorkforceApply().apply_detail_api(data)
        if Assertions().assert_code(res.status_code, 200):
            Assertions().assert_text(res.json()['errcode'], '0')


if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_workforce_apply_module.py"])
