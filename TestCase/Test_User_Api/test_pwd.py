#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/20 11:17 上午
# @Author  : lin
# @FileName: test_pwd.py

###校验用户是否存在

import pytest
from Common.operation_assert import Assertions
from Common.request import Request
from Common.operation_yaml import YamlHandle
from Conf.config import Config


class TestCheckPwd:

    @pytest.mark.parametrize('data', YamlHandle().read_yaml('TestApi/checkpwd.yaml'))
    def test_pwd(self, data):
        url = Config().get_conf('test_env', 'test3') + data['url']
        body = data['body']
        headers = data['headers']
        headers.update({'X-Dk-Token': YamlHandle().read_yaml('login.yaml')[0]['accessToken']})
        # print(YamlHandle().read_yaml('login.yaml'))
        res = Request().send_request_method('get', url, body, headers)
        print(res.json())
        if Assertions().assert_code(res.status_code, 200):
            Assertions().assert_text(res.json()['errcode'], '0')



if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_pwd.py'])
