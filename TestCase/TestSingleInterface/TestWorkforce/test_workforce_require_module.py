# coding:utf-8
# Name:test_workforce_require_module.py
# Author:qi.yu
# Time:2020/7/16 5:23 下午
import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.WorkforceApi.workforce_ticket import WorkforceTicket


@allure.feature("乙方劳务工需求模块")
class TestRequire:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    # @pytest.mark.skip
    @allure.title("乙方劳务工需求列表")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SingleInterfaceData/Workforce/WorkforceRequire/require_list.yaml'))
    def test_require_list(self, data):
        res = WorkforceTicket(self.env).get_require_list_api(data)
        Assertions().assert_mode(res, data)

    # @pytest.mark.skip
    @allure.title("乙方劳务工需求详情")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SingleInterfaceData/Workforce/WorkforceRequire/require_detail.yaml'))
    def test_require_detail(self, data):
        res = WorkforceTicket(self.env).get_require_detail_api(data)
        Assertions().assert_mode(res, data)

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main(['-sv', 'test_workforce_require_module.py', "--env", "test3"])
