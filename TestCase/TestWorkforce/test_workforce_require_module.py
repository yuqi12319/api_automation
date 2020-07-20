# coding:utf-8
# Name:test_workforce_require_module.py
# Author:qi.yu
# Time:2020/7/16 5:23 下午
import pytest
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Robot.Workforce.workforce_require import WorkforceRequire
from Conf.config import Config


class TestRequire:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test3')

    # @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceRequire/require_list.yaml'))
    def test_require_list(self, data):
        res = WorkforceRequire().require_list_api(self.url_path, data)
        Assertions().assert_mode(res, data)

    # @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceRequire/require_detail.yaml'))
    def test_require_detail(self, data):
        res = WorkforceRequire().require_detail_api(self.url_path, data)
        Assertions().assert_mode(res, data)

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main(['-s', 'test_workforce_require_module.py'])
