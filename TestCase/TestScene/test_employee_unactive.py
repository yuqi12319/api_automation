# Name:test_employee_unactive.py
# Author:lin
# Time:2020/8/25 10:00 上午


import pytest
import allure
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions


class TestEmployeeActive:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.parametrize('data',YamlHandle().read_yaml('SceneData/EmployeeManagerScene'))
    def test_main_sence(self,data):
        with allure.step('第一步，获取员工未激活集合'):
