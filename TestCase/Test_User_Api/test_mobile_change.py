#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/20 1:59 下午
# @Author  : lin
# @FileName: test_mobile_change.py


###修改手机号

import pytest
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from Common.request import Request


class TestChange:
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('TestApi/mobile_change.yaml'))
    def test_mobile_change(self, data):
        url = Config().get_conf('test_env', 'test3') + data['url']
        body = data['body']
        headers = data['headers']
        headers.update({'X-Dk-Token': YamlHandle().read_yaml('login.yaml')[0]['accessToken'],
                        'X-Flow-Id': '24d9729a37394ed4b3812b828db83394'})
        print(url, body, headers)
        res = Request().send_request_method('put', url, body, headers)
        print(res.json())


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_mobile_change.py'])
