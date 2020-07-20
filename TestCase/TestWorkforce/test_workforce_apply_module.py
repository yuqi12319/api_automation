# coding:utf-8
# Name:test_workforce_apply_module.py
# Author:qi.yu
# Time:2020/7/16 10:18 上午
import pytest
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Robot.Workforce.workforce_apply import WorkforceApply
from Conf.config import Config


class TestApply:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test3')

    # @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceApple/apply.yaml'))
    def test_send_apply(self, data):
        res = WorkforceApply().send_apply_api(self.url_path, data)
        Assertions().assert_mode(res, data)

    # @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceApple/apply_list.yaml'))
    def test_apply_list(self, data):
        res = WorkforceApply().apply_list_api(self.url_path, data)
        Assertions().assert_mode(res, data)

    # @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceApple/apply_detail.yaml'))
    def test_apply_detail(self, data):
        res = WorkforceApply().apply_detail_api(self.url_path, data)
        Assertions().assert_mode(res, data)

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_workforce_apply_module.py"])
