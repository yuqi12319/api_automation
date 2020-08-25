# Name:init_payrollItem.py
# Author:lin
# Time:2020/8/3 3:26 下午


import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.request import Request
from Conf.config import Config
from TestApi.PayrollApi.init_payrollItem import InitPayrollItem
from Common.operation_assert import Assertions


##新建公司时，初始化薪资项

class Test_init_payrollItem:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @allure.title('新建公司时，初始化薪资项')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SingleInterfaceData/Payroll/init_payrollItem.yaml'))
    def test_init_payrollItem(self, data):
        res = InitPayrollItem(self.env).init_payrollItem(data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'init_payrollItem.py', '--env', 'test3'])
