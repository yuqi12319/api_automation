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

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Workforce/WorkforceStatus/query_employee_status.yaml'))
    def test_employee_status(self, data):
        res = QueryEmployeeStatus(self.env).test_query_status(data)
        Assertions().assert_code(res, 0)


if __name__ == '__main__':
    pytest.main(['-v', '-s', 'test_query_workforce_status.py'])
