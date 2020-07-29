# @Author: Saco Song
# @Time: 2020/7/29-10:28 上午
# @Description:
import pytest

from Common.operation_yaml import YamlHandle


class TestBillManagement:
    @pytest.mark.parametrize('data',YamlHandle().read_yaml('/'))
    def test_get_workforce_company_map(self):
