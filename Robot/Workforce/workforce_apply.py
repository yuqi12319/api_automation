# coding:utf-8
# Name:workforce_apply.py
# Author:qi.yu
# Time:2020/7/16 10:31 上午
from Common.request import Request

class WorkforceApply:

    def __init__(self):
        self.request = Request()

    #创建用工申请接口
    def send_apply_api(self,url,data,headers):
        res = self.request.send_request_method('post',url,data,headers)
