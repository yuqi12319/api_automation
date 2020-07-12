# coding:utf-8
# Name:session.py
# Author:qi.yu
# Time:2020/6/24 2:41 下午

"""
封装获取cookie方法
"""

import requests
from Common import log
from Conf import config

class Session:
    def __init__(self):
        self.config = config.Config()
        self.log = log.MyLog()

    def get_session(self,env):
        """
        获取session
        :param env:环境变量
        :return:
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        if env == "test2":
            login_url = 'http://'+self.config.get_conf('private_test2','host')+self.config.get_conf('private_test2','loginHost')
            parm = self.config.get_conf('private_test2','loginInfo')
            session_debug = requests.session()
            response = session_debug.post(login_url,parm,headers=headers)
            print(response.cookies)
            return response.cookies.get_dict()


if __name__ == '__main__':
    ss = Session()
    a = ss.get_session('test2')
    print(a)
