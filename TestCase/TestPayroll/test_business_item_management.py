# @Author: Saco Song
# @Time: 2020/8/5-6:29 下午
# @Description:
import allure
import pytest

from Common.operation_assert import Assertions
from Common.operation_random import random_name, snowflake
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.PayrollApi.business_item_management import BusinessItemManagement


class TestBusinessItemManagement:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test2')

    @allure.title('新增保存业务项目')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('/Payroll/BusinessItemManagement/save_business_item.yaml'))
    def test_save_business_item(self, data):
        if data['body']['factorKey'] is None:
            data['body']['factorKey'] = snowflake()
        if data['body']['name'] is None:
            data['body']['name'] = random_name(with_gender=False) + random_name(with_gender=False)
        response = BusinessItemManagement().save_business_item(self.url_path, data)
        Assertions().assert_mode(response, data)

    @allure.title('新增保存业务项目：接口校验必填项')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/BusinessItemManagement/check_item_requiring_while_saving_business_item.yaml'))
    def test_check_item_requiring_while_saving_business_item(self, data):
        response = BusinessItemManagement().save_business_item(self.url_path, data)
        Assertions().assert_mode(response, data)
