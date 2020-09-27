# coding:utf-8
# Name:attendance.py
# Author:qi.yu
# Time:2020/7/2 4:53 下午
import pytest
from Common.request import *
from Conf.config import Config


@pytest.fixture(scope="module", autouse=True)
def login():
    url = Config().get_conf('test_env', 'dev') + '/dukang-user/login'
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


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help="environment")


@pytest.fixture(scope="class")
def env(pytestconfig):
    return pytestconfig.getoption('--env')
