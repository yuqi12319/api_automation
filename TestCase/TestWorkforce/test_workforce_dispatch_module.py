# coding:utf-8
# Name:test_workforce_dispatch_module.py
# Author:qi.yu
# Time:2020/7/22 2:08 下午

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.WorkforceApi.workforce_dispatch import WorkforceDispatch
from Conf.config import Config


class TestAssign:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test3')

    # @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceAssign/dispatch_list.yaml'))
    def test_assign_list(self, data):
        res = WorkforceDispatch().dispatch_list_api(self.url_path, data)
        Assertions().assert_mode(res, data)

    # @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceAssign/dispatch_detail.yaml'))
    def test_assign_detail(self, data):
        res = WorkforceDispatch().dispatch_detail_api(self.url_path, data)
        Assertions().assert_mode(res, data)

    @pytest.mark.parametrize('data',YamlHandle().read_yaml('Workforce/WorkforceAssign/relevance_apply.yaml'))
    def test_relevance_apply(self, data):
        res = WorkforceDispatch().relevance_apply_api(self.url_path, data)
        Assertions().assert_mode(res,data)


if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_workforce_dispatch_module.py"])
