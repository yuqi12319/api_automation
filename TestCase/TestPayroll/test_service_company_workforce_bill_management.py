# @Author: Saco Song
# @Time: 2020/8/5-2:39 下午
# @Description:
import allure
import pytest

from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.PayrollApi.service_company_workforce_bill_management import ServiceCompanyWorkforceBillManagement


class TestServiceCompanyWorkforceBillManagement:
    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test2')

    @allure.title('提出账单异议')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml(
        '/Payroll/ServiceCompanyWorkforceBillManagement/submit_dissent_workforce_bill_form.yaml'))
    def test_submit_dissent_workforce_bill_form(self, data):
        response = ServiceCompanyWorkforceBillManagement().submit_dissent_workforce_bill_form(self.url_path, data)
        Assertions().assert_in_text(response.json(), data['expect']['assert_message'])

    @allure.title('获取劳务工账单列表')
    @pytest.mark.parametrize('data',YamlHandle().read_yaml(
        '/Payroll/ServiceCompanyWorkforceBillManagement/get_workforce_bill_list.yaml'))
    def test_get_workforce_bill_list(self, data):
        response = ServiceCompanyWorkforceBillManagement().get_laborer_bill_list_api(self.url_path, data)
        Assertions().assert_mode(response, data)
