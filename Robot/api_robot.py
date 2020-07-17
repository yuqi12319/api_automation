# coding:utf-8
# Name:api_robot.py
# Author:qi.yu
# Time:2020/7/6 9:55 上午
from Common.request import Request
from Conf.config import *


class Payroll:

    def __init__(self):
        self.request = Request()

    def get_payrollItem_list_api(self, url, data, headers):
        res = self.request.get_requests(url=url, data=data, headers=headers)
        return res

    def get_paygroup_list_api(self, url, data, headers):
        res = self.request.get_requests(url, data, headers)
        return res
