# coding:utf-8
# Name:muscat.py
# Author:qi.yu
# Time:2020/8/3 11:33 上午
# Description:

from TestApi.consts_api import Const


class Muscat(Const):
    def __init__(self):
        super().__init__()

    def get_my_companies_api(self):
        url = "http://dktest3-workio.bipocloud.com/services/muscat/my_companies"
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res
