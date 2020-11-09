# coding:utf-8
# Name:consts_api.py
# Author:qi.yu
# Time:2020/7/22 3:27 下午

from Common.request import Request
from Conf.config import Config
from Common import log
import Common.consts


class Const(object):

    def __init__(self, env):
        self.request = Request()
        self.log = log.MyLog()
        if env == "test":
            self.url_path = Config().get_conf('test_env', 'test')
        elif env == "sandbox":
            self.url_path = Config().get_conf('test_env', 'sandbox')
        elif env == "test1":
            self.url_path = Config().get_conf('test_env', 'test1')
        elif env == "test2":
            self.url_path = Config().get_conf('test_env', 'test2')
        elif env == "test3":
            self.url_path = Config().get_conf('test_env', 'test3')
        elif env == "dev1":
            self.url_path = Config().get_conf('test_env', 'dev1')
        elif env == "dev2":
            self.url_path = Config().get_conf('test_env', 'dev2')
        elif env == "dev3":
            self.url_path = Config().get_conf('test_env', 'dev3')
        self.headers = dict()
        if Common.consts.ACCESS_TOKEN:
            self.headers['X-Dk-Token'] = Common.consts.ACCESS_TOKEN[0]
        else:
            self.log.debug('未登录')
