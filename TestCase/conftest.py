# coding:utf-8
# Name:conftest.py
# Author:qi.yu
# Time:2020/7/2 4:53 下午
import pytest
from Common.request import *
from Conf.config import Config
from Common.operation_yaml import YamlHandle


@pytest.fixture(scope="module")
def login():
    config = Config()
    url = config.get_conf_env('test2') + '/services/dukang-user/login'
    data = {
        'areaCode': '86',
        'clientId': 'gardenia',
        'password': '12345678',
        'username': '18373280066'
    }
    request = Request()
    res = request.post_requests(url, data)
    access_token = res['json']['data']['accessToken']
    YamlHandle().write_yaml('login.yaml', 'login', 'accessToken', access_token)
    return access_token

