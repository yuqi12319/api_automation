# Name:test_workforce_relation_add.py
# Author:lin
# Time:2020/8/3 2:09 下午

import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.WorkforceApi.workforce_apply import WorkforceApply
from Conf.config import Config


## 新增关联关系

class TestWorkforceAdd:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test3')

    @pytest.skip
    @allure.title("新增公司之间的关联关系")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/CompanyWorkforceMap/company_relation_add.yaml'))
    def test_company_workforce_add(self, data):
        res = WorkforceApply().company_workforce_add(self.url_path, data)
        Assertions().assert_mode(res, data)

    # @pytest.skip
    @allure.title('获取劳务公司')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(('Workforce/CompanyWorkforceMap/get_workforce_map.yaml')))
    def test_get_workforce(self, data):
        res = WorkforceApply().get_workforce_map(self.url_path, data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_workforce_relation_add.py'])
