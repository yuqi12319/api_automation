# coding:utf-8
# Name:conftest.py
# Author:qi.yu
# Time:2020/7/2 4:53 下午
import pytest
from Common.request import *
from Conf.config import Config

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

    res = Request().send_request_method('post', url=url, json=body)
    access_token = res.json()['data']['accessToken']
    Common.consts.ACCESS_TOKEN.append(access_token)