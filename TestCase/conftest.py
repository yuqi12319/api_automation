# coding:utf-8
# Name:conftest.py
# Author:qi.yu
# Time:2020/7/2 4:53 下午
import pytest
from Common.request import *
from Conf.config import Config
from Common.operation_yaml import YamlHandle


@pytest.fixture(scope="session")
@pytest.mark.parametrize('data', YamlHandle().read_yaml('login.yaml'))
def login(data):
    url = Config().get_conf('test_env', 'test3') + data['url']
    res = Request().send_request_method('post', url, data['body'])
    access_token = res.json()['data']['accessToken']
    YamlHandle().write_yaml('login.yaml', 'accessToken', access_token)
