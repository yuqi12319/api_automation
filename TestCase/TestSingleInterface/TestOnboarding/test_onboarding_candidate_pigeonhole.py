# @Author: Nigo Su
# @Time: 2020-08-04-16:37
# @Description:
import allure
import pytest

from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.OnboardingApi.onboarding_candidate_pigeonhole import OnboardingCandidatePigeonhole


@allure.feature("入职归档人员模块")
class TestCandidatePigeonhole:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @allure.title('操作人员归档')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('/Onboarding/put_candidate_pigeonhole.yaml'))
    def test_put_candidate_pigeonhole(self, data):
        res = OnboardingCandidatePigeonhole(self.env).put_candidate_pigeonhole_api(data)
        Assertions().assert_mode(res, data)

    @allure.title('获取归档人员列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('/Onboarding/get_pigeonhole_list.yaml'))
    def test_get_pigeonhole_list(self, data):
        res = OnboardingCandidatePigeonhole(self.env).get_pigeonhole_list_api(data)
        Assertions().assert_mode(res, data)

    @allure.title('还原归档人员')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('/Onboarding/put_pigeonhole_reduction.yaml'))
    def test_put_pigeonhole_reduction(self, data):
        res = OnboardingCandidatePigeonhole(self.env).put_pigeonhole_reduction_api(data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_onboarding_candidate_pigeonhole.py", "--env", "test1"])
