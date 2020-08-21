# @Author: Nigo Su
# @Time: 2020-08-04-11:16
# @Description:
import allure
import pytest

from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.OnboardingApi.onboarding_candidate import OnboardingCandidate


@allure.feature("入职候选人模块")
class TestCandidate:
    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @allure.title('获取候选人列表')
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SingleInterfaceData/Onboarding/get_candidate_list.yaml'))
    def test_get_candidate_list(self, data):
        res = OnboardingCandidate(self.env).get_candidate_list_api(data)
        Assertions().assert_mode(res, data)

    @allure.title("新增候选人信息")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SingleInterfaceData/Onboarding/post_add_candidate.yaml'))
    def test_add_candidate(self, data):
        res = OnboardingCandidate(self.env).post_add_candidate_api(data)
        Assertions().assert_mode(res, data)

    @allure.title("获取人员信息(包含offer和入职资料发送信息)")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SingleInterfaceData/Onboarding/get_candidate_detail.yaml'))
    def test_get_candidate_detail(self, data):
        res = OnboardingCandidate(self.env).get_candidate_detail_api(data)
        Assertions().assert_mode(res, data)

    @allure.title("修改人员信息")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SingleInterfaceData/Onboarding/put_candidate_detail.yaml'))
    def test_put_candidate_detail(self, data):
        res = OnboardingCandidate(self.env).put_candidate_detail_api(data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_onboarding_candidate.py", "--env", "test1"])
