#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/20 3:03 下午
# @Author  : lin
# @FileName: test_reset_password.py
#


import pytest
from Conf.config import Config
from Common.request import Request
from Common.operation_yaml import YamlHandle


class TestReset:
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('TestApi/reset_password.yaml'))
    def test_reset_pass(self, data):
        url = Config().get_conf('test_env', 'test3') + data['url']
        headers = data['headers']
        headers.update({'X-DK-Token': YamlHandle().read_yaml('login.yaml')[0]['accessToken']})
        res = Request().send_request_method('put', url, data['body'], headers)

        print(res.json())

if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_reset_password.py'])
