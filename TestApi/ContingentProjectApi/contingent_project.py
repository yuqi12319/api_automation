# coding:utf-8
# Name:contingent_project.py
# Author:qi.yu
# Time:2020/8/18 2:04 下午
# Description:

from TestApi.consts_api import Const


class ContingentProject(Const):

    def __init__(self, env):
        super().__init__(env)

    def project(self, data):
        url = self.url_path + "/dukang-contingent-project/api/project"
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res