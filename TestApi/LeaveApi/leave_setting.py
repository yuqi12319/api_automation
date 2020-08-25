# coding:utf-8
# Name:leave_setting.py
# Author:qi.yu
# Time:2020/8/25 4:38 下午
# Description:休假组设置

from TestApi.consts_api import Const

class LeaveSetting(Const):

    def __init__(self, env):
        super().__init__(env)

    def get_leave_group_api(self, data):
        url = self.url_path + '/leave/leave_groups_for_web'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res