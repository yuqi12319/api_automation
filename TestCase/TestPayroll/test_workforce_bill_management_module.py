# @Author: Saco Song
# @Time: 2020/7/29-10:28 上午
# @Description:
import allure
import pytest

from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.PayrollApi.workforce_bill_management import WorkforceBillManagement


class TestBillManagement:
    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test2')

    @allure.title('获取绑定劳务公司列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('/Payroll/WorkforceBillManagement'
                                                            '/get_workforce_company_map.yaml'))
    def test_get_workforce_company_map(self, data):
        res = WorkforceBillManagement().get_workforce_company_map_api(self.url_path, data)
        Assertions().assert_mode(res, data)
