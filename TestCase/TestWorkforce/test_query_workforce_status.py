# Name:test_query_workforce_status.py
# Author:lin
# Time:2020/7/29 2:41 下午

## 查询员工状态


import pytest
from TestApi.WorkforceApi.query_employee_status import QueryEmployeeStatus
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Conf.config import Config


class TestEmployeeStatus:
    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test3')

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceStatus/query_employee_status.yaml'))
    def test_employee_status(self, data):
        res = QueryEmployeeStatus().test_query_status(self.url_path, data)
        # Assertions().assert_code(res, 0)


if __name__ == '__main__':
    pytest.main(['-v', '-s', 'test_query_workforce_status.py'])
