# @Author: Leo Liu 
# @Time: 2020-07-29
# @Description: test case for thirdparty api


import pytest
from Conf.config import Config
from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from TestApi.OpenApi.api_thirdparty import ThirdParty


class TestThirdpartyApi:
    def setup_class(self):
        self.url_path = Config().get_conf('open_api_env', 'test')

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('OpenApi/Thirdparty/get_access_token.yaml'))
    def test_get_access_token(self, data):
        res = ThirdParty().get_access_token_api(self.url_path, data)
        Assertions().assert_mode(res, data)


if __name__ == '__main__':
    pytest.main(['-s', 'api_thirdparty.py'])
