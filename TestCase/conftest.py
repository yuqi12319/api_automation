# coding:utf-8
# Name:conftest.py
# Author:qi.yu
# Time:2020/7/2 4:53 下午
import pytest
from Common.request import *
from Conf.config import Config
from Common.operation_yaml import YamlHandle


# @pytest.mark.parametrize('data', YamlHandle().read_yaml('login.yaml'))
@pytest.fixture(autouse=True)
def login():
    url = Config().get_conf('test_env', 'test3') + '/dukang-user/login'
    body = {
        "areaCode": 86,
        "clientId": "gardenia",
        "password": 12345678,
        "username": 18373280066
        # "username": 13300001234
    }

    res = Request().send_request_method('post', url,  body)
    access_token = res.json()['data']['accessToken']
    YamlHandle().write_yaml('login.yaml', 'accessToken', access_token)
    # return access_token
