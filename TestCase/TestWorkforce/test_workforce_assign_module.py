# coding:utf-8
# Name:test_workforce_assign_module.py
# Author:qi.yu
# Time:2020/7/22 2:08 下午

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.WorkforceApi.workforce_assign import WorkforceAssign
from Conf.config import Config


class TestAssign:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test3')

    # @pytest.mark.skip
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceAssign/assign_list.yaml'))
    def test_assgin_list(self, data):
        res = WorkforceAssign().assign_list_api(self.url_path, data)
        Assertions().assert_mode(res, data)

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceAssign/assign_detail.yaml'))
    def test_assgin_detail(self, data):
        res = WorkforceAssign().assign_detail_api(self.url_path, data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_workforce_assign_module.py"])
