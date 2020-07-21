# coding:utf-8
# Name:workforce_apply.py
# Author:qi.yu
# Time:2020/7/16 10:31 上午
from Common.request import Request
from Conf.config import Config
from Common.operation_yaml import YamlHandle


class WorkforceApply:

    def __init__(self):
        self.request = Request()
        self.access_token = YamlHandle().read_yaml('login.yaml')[0]['accessToken']

    # 创建用工申请接口
    def send_apply_api(self, url_path, data):
        url = url_path + data['url']
        headers = data['headers']
        headers.update({'X-Dk-Token': self.access_token})
        res = self.request.send_request_method('post', url, data['body'], headers)
        return res

    def apply_list_api(self, url_path, data):
        url = url_path + data['url'] + '?offset=0&limit=20'
        headers = data['headers']
        headers.update({'X-Dk-Token': self.access_token})
        res = self.request.send_request_method('post', url, data['body'], headers)
        return res

    def apply_detail_api(self, url_path, data):
        url = url_path + data['url'] + str(data['applicationId'])
        headers = data['headers']
        headers.update({'X-Dk-Token': self.access_token})
        res = Request().send_request_method('get', url, headers=headers)
        return res
