# coding:utf-8
# Name:consts_api.py
# Author:qi.yu
# Time:2020/7/22 3:27 下午

from Common.request import Request
from Conf.config import Config
import Common.consts


class Const(object):

    def __init__(self, env):
        self.request = Request()
        if env == "test1":
            self.url_path = Config().get_conf('test_env', 'test1')
        elif env == "test2":
            self.url_path = Config().get_conf('test_env', 'test2')
        elif env == "test3":
            self.url_path = Config().get_conf('test_env', 'test3')
        else:
            self.url_path = Config().get_conf('test_env', 'test')
        self.headers = dict()
        self.headers['X-Dk-Token'] = Common.consts.ACCESS_TOKEN[0]
