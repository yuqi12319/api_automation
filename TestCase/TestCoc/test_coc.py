# coding:utf-8
# Name:test_coc.py
# Author:qi.yu
# Time:2020/8/18 5:28 下午
# Description:

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.CocApi.coc import Coc


class TestCoc:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.skip
    @allure.title('获取关联劳务公司')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Coc/workforce_company_map.yaml'))
    def test_workforce_company_map(self, data):
        res = Coc(self.env).workforce_company_map_api(data)
        Assertions().assert_mode(res, data)

    # @pytest.skip
    @allure.title("新增公司之间的关联关系")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Coc/workforce_company_relation_add.yaml'))
    def test_workforce_company_workforce_add(self, data):
        res = Coc(self.env).workforce_company_workforce_add(data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(['-sv', 'test_coc.py', "--env", "test"])
